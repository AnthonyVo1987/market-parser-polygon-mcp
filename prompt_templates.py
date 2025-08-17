"""
Stock Market Analysis Prompt Templates

This module provides sophisticated prompt templates for structured stock market analysis,
optimized for FSM-driven interactions with JSON schema-based responses.

Features:
- Template-based prompt generation with JSON schema compliance
- Ticker symbol extraction and context awareness
- System prompt enhancements for structured JSON output
- Multi-stock analysis consistency
- Response formatting instructions optimized for JSON schemas
- Integration with json_schemas.py for API architect schemas
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime

# Import JSON schemas from the API architect
try:
    from json_schemas import (
        SNAPSHOT_SCHEMA, 
        SUPPORT_RESISTANCE_SCHEMA, 
        TECHNICAL_SCHEMA,
        AnalysisType,
        schema_registry,
        export_schemas_for_ai_prompts
    )
except ImportError:
    # Fallback for testing
    print("Warning: json_schemas module not available. Using fallback schemas.")
    SNAPSHOT_SCHEMA = None
    SUPPORT_RESISTANCE_SCHEMA = None
    TECHNICAL_SCHEMA = None
    AnalysisType = None
    schema_registry = None
    export_schemas_for_ai_prompts = None


class PromptType(Enum):
    """Types of stock analysis prompts"""
    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"


@dataclass
class TickerContext:
    """Context information for ticker symbol processing"""
    symbol: str
    company_name: Optional[str] = None
    sector: Optional[str] = None
    last_mentioned: bool = False
    confidence: float = 1.0
    source: str = "explicit"  # explicit, extracted, inferred, default


@dataclass
class PromptTemplate:
    """Template for generating structured prompts"""
    template_type: PromptType
    base_template: str
    formatting_instructions: str
    example_response: str
    required_fields: List[str]
    optional_fields: List[str] = field(default_factory=list)
    system_prompt_additions: str = ""
    
    def generate_prompt(self, ticker_context: TickerContext, 
                       custom_instructions: Optional[str] = None) -> str:
        """Generate a complete prompt using the template"""
        # Format the base template with ticker information
        prompt_parts = [
            "### STOCK ANALYSIS REQUEST ###",
            "",
            self.base_template.format(
                ticker=ticker_context.symbol,
                company=ticker_context.company_name or ticker_context.symbol,
            ),
            "",
            "### JSON SCHEMA REQUIREMENTS ###",
            self.formatting_instructions,
            "",
            "### EXAMPLE JSON RESPONSE ###",
            self.example_response,
            ""
        ]
        
        if custom_instructions:
            prompt_parts.extend([
                "### ADDITIONAL INSTRUCTIONS ###",
                custom_instructions,
                ""
            ])
        
        prompt_parts.extend([
            "### CRITICAL RESPONSE REQUIREMENTS ###",
            "1. Respond with VALID JSON ONLY - no explanations, no markdown, no additional text",
            "2. Must exactly match the JSON schema structure provided above",
            "3. All required fields must be present with appropriate data types",
            "4. Include current timestamp in ISO 8601 format",
            "5. Ensure all numeric values are properly formatted (no strings for numbers)",
            "",
            "### JSON RESPONSE ###",
            f"Generate {self.template_type.value} analysis for {ticker_context.symbol} as valid JSON:"
        ])
        
        return "\n".join(prompt_parts)


class TickerExtractor:
    """Extracts and manages ticker symbols from conversation context"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')
        self._company_patterns = self._build_company_patterns()
        self._last_mentioned_ticker: Optional[TickerContext] = None
        self._conversation_tickers: List[TickerContext] = []
    
    def extract_ticker(self, text: str, chat_history: Optional[List[Dict]] = None) -> TickerContext:
        """
        Extract ticker symbol from text with context awareness
        
        Args:
            text: Text to extract ticker from
            chat_history: Optional conversation history for context
            
        Returns:
            TickerContext with extracted or inferred ticker information
        """
        # Try explicit ticker extraction
        ticker_match = self._extract_explicit_ticker(text)
        if ticker_match:
            return ticker_match
        
        # Try company name extraction
        company_match = self._extract_from_company_name(text)
        if company_match:
            return company_match
        
        # Use conversation context
        if chat_history:
            context_match = self._extract_from_context(text, chat_history)
            if context_match:
                return context_match
        
        # Use last mentioned ticker
        if self._last_mentioned_ticker:
            context = TickerContext(
                symbol=self._last_mentioned_ticker.symbol,
                company_name=self._last_mentioned_ticker.company_name,
                last_mentioned=True,
                confidence=0.7,
                source="last_mentioned"
            )
            self.logger.info(f"Using last mentioned ticker: {context.symbol}")
            return context
        
        # Fallback to generic placeholder
        context = TickerContext(
            symbol="[TICKER]",
            company_name="the requested stock",
            confidence=0.0,
            source="default"
        )
        self.logger.warning("No ticker found, using placeholder")
        return context
    
    def _extract_explicit_ticker(self, text: str) -> Optional[TickerContext]:
        """Extract explicit ticker symbols (e.g., AAPL, TSLA)"""
        # Look for common ticker patterns
        ticker_indicators = [
            r'\$([A-Z]{1,5})\b',  # $AAPL
            r'\b([A-Z]{2,5})\s+(?:stock|shares|ticker|symbol)',  # AAPL stock
            r'ticker\s*:?\s*([A-Z]{1,5})',  # ticker: AAPL
            r'symbol\s*:?\s*([A-Z]{1,5})',  # symbol: AAPL
            r'\b([A-Z]{1,5})\s+(?:analysis|snapshot|data)',  # AAPL analysis
            r'\babout\s+([A-Z]{2,5})\b',  # about NVDA
        ]
        
        for pattern in ticker_indicators:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                ticker = match.group(1).upper()
                if self._is_valid_ticker(ticker):
                    context = TickerContext(
                        symbol=ticker,
                        confidence=0.9,
                        source="explicit"
                    )
                    self._update_last_mentioned(context)
                    self.logger.info(f"Extracted explicit ticker: {ticker}")
                    return context
        
        return None
    
    def _extract_from_company_name(self, text: str) -> Optional[TickerContext]:
        """Extract ticker from company name mentions"""
        for company_pattern, ticker_info in self._company_patterns.items():
            match = re.search(company_pattern, text, re.IGNORECASE)
            if match:
                context = TickerContext(
                    symbol=ticker_info["ticker"],
                    company_name=ticker_info["name"],
                    sector=ticker_info.get("sector"),
                    confidence=0.8,
                    source="company_name"
                )
                self._update_last_mentioned(context)
                self.logger.info(f"Extracted from company name: {ticker_info['ticker']}")
                return context
        
        return None
    
    def _extract_from_context(self, text: str, chat_history: List[Dict]) -> Optional[TickerContext]:
        """Extract ticker from conversation context"""
        # Look through recent chat history for ticker mentions
        recent_messages = chat_history[-10:]  # Last 10 messages
        
        for message in reversed(recent_messages):
            if message is None:
                continue
            content = message.get("content", "")
            if content:
                ticker_match = self._extract_explicit_ticker(content)
                if ticker_match:
                    # Use context from history but with lower confidence
                    context = TickerContext(
                        symbol=ticker_match.symbol,
                        company_name=ticker_match.company_name,
                        confidence=0.6,
                        source="context"
                    )
                    self.logger.info(f"Extracted from context: {context.symbol}")
                    return context
        
        return None
    
    def _is_valid_ticker(self, ticker: str) -> bool:
        """Validate if string is likely a valid ticker symbol"""
        if not ticker or len(ticker) < 1 or len(ticker) > 5:
            return False
        
        # Exclude common false positives
        false_positives = {
            "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", 
            "HAD", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", 
            "HIM", "HIS", "HOW", "ITS", "NEW", "NOW", "OLD", "SEE", "TWO",
            "WHO", "BOY", "DID", "ITS", "LET", "PUT", "SAY", "SHE", "TOO", "USE",
            "APPLE", "DATA", "TEXT", "ME", "MY", "WE", "HE", "SHE", "THEY", "IT"
        }
        
        return ticker not in false_positives
    
    def _update_last_mentioned(self, context: TickerContext):
        """Update the last mentioned ticker context"""
        self._last_mentioned_ticker = context
        
        # Add to conversation history if not already present
        if not any(t.symbol == context.symbol for t in self._conversation_tickers):
            self._conversation_tickers.append(context)
    
    def _build_company_patterns(self) -> Dict[str, Dict[str, str]]:
        """Build patterns for major company name recognition"""
        return {
            r'\bapple\b(?:\s+inc\.?)?': {
                "ticker": "AAPL",
                "name": "Apple Inc.",
                "sector": "Technology"
            },
            r'\bmicrosoft\b(?:\s+corp\.?)?': {
                "ticker": "MSFT", 
                "name": "Microsoft Corporation",
                "sector": "Technology"
            },
            r'\btesla\b(?:\s+motors)?(?:\s+inc\.?)?': {
                "ticker": "TSLA",
                "name": "Tesla, Inc.",
                "sector": "Automotive"
            },
            r'\bamazon\b(?:\.com)?(?:\s+inc\.?)?': {
                "ticker": "AMZN",
                "name": "Amazon.com, Inc.",
                "sector": "E-commerce"
            },
            r'\bgoogle\b|\balphabet\b(?:\s+inc\.?)?': {
                "ticker": "GOOGL",
                "name": "Alphabet Inc.",
                "sector": "Technology"
            },
            r'\bnvidia\b(?:\s+corp\.?)?': {
                "ticker": "NVDA",
                "name": "NVIDIA Corporation", 
                "sector": "Technology"
            },
            r'\bmeta\b|\bfacebook\b(?:\s+inc\.?)?': {
                "ticker": "META",
                "name": "Meta Platforms, Inc.",
                "sector": "Technology"
            },
            r'\bnetflix\b(?:\s+inc\.?)?': {
                "ticker": "NFLX",
                "name": "Netflix, Inc.",
                "sector": "Entertainment"
            },
            r'\bjpmorgan\b|\bjp\s+morgan\b(?:\s+chase)?': {
                "ticker": "JPM",
                "name": "JPMorgan Chase & Co.",
                "sector": "Financial"
            },
            r'\bj\.?p\.?\s*morgan\b': {
                "ticker": "JPM",
                "name": "JPMorgan Chase & Co.",
                "sector": "Financial"
            }
        }
    
    def get_conversation_tickers(self) -> List[TickerContext]:
        """Get all tickers mentioned in the conversation"""
        return self._conversation_tickers.copy()
    
    def get_last_mentioned_ticker(self) -> Optional[TickerContext]:
        """Get the last mentioned ticker"""
        return self._last_mentioned_ticker


class PromptTemplateManager:
    """Manages and generates stock analysis prompt templates"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ticker_extractor = TickerExtractor()
        self.templates = self._build_templates()
        self.system_prompt_enhancements = self._build_system_prompt_enhancements()
    
    def generate_prompt(self, prompt_type: PromptType, ticker: Optional[str] = None,
                       chat_history: Optional[List[Dict]] = None,
                       custom_instructions: Optional[str] = None) -> Tuple[str, TickerContext]:
        """
        Generate a structured prompt for stock analysis
        
        Args:
            prompt_type: Type of analysis prompt
            ticker: Optional explicit ticker symbol
            chat_history: Conversation history for context
            custom_instructions: Additional instructions
            
        Returns:
            Tuple of (generated_prompt, ticker_context)
        """
        # Extract or determine ticker context
        if ticker:
            ticker_context = TickerContext(
                symbol=ticker.upper(),
                confidence=1.0,
                source="explicit"
            )
        else:
            # Try to extract from conversation context
            context_text = ""
            if chat_history:
                recent_messages = chat_history[-5:]
                context_text = " ".join([msg.get("content", "") for msg in recent_messages if msg is not None])
            
            ticker_context = self.ticker_extractor.extract_ticker(context_text, chat_history)
        
        # Get the appropriate template
        template = self.templates[prompt_type]
        
        # Generate the prompt
        prompt = template.generate_prompt(ticker_context, custom_instructions)
        
        self.logger.info(f"Generated {prompt_type.value} prompt for {ticker_context.symbol}")
        return prompt, ticker_context
    
    def get_enhanced_system_prompt(self, base_system_prompt: str) -> str:
        """
        Enhance the base system prompt with structured JSON output instructions
        
        Args:
            base_system_prompt: Original system prompt
            
        Returns:
            Enhanced system prompt with JSON structured output guidance
        """
        return base_system_prompt + "\n\n" + self.system_prompt_enhancements
    
    def get_json_prompt(self, prompt_type: PromptType, ticker: Optional[str] = None,
                       chat_history: Optional[List[Dict]] = None,
                       custom_instructions: Optional[str] = None) -> Tuple[str, TickerContext]:
        """
        Generate a JSON-focused prompt for the AI agent (alias for generate_prompt)
        
        Args:
            prompt_type: Type of analysis prompt
            ticker: Optional explicit ticker symbol
            chat_history: Conversation history for context
            custom_instructions: Additional instructions
            
        Returns:
            Tuple of (generated_prompt, ticker_context)
        """
        return self.generate_prompt(prompt_type, ticker, chat_history, custom_instructions)
    
    def get_available_schemas(self) -> Dict[str, Any]:
        """
        Get information about available JSON schemas
        
        Returns:
            Dictionary with schema availability and metadata
        """
        schemas_info = {
            "available": schema_registry is not None,
            "schemas": {}
        }
        
        for prompt_type in PromptType:
            schema_available = False
            schema_id = None
            
            if prompt_type == PromptType.SNAPSHOT and SNAPSHOT_SCHEMA:
                schema_available = True
                schema_id = SNAPSHOT_SCHEMA.get("$id", "snapshot")
            elif prompt_type == PromptType.SUPPORT_RESISTANCE and SUPPORT_RESISTANCE_SCHEMA:
                schema_available = True
                schema_id = SUPPORT_RESISTANCE_SCHEMA.get("$id", "support_resistance")
            elif prompt_type == PromptType.TECHNICAL and TECHNICAL_SCHEMA:
                schema_available = True
                schema_id = TECHNICAL_SCHEMA.get("$id", "technical")
            
            schemas_info["schemas"][prompt_type.value] = {
                "available": schema_available,
                "schema_id": schema_id,
                "fallback_used": not schema_available
            }
        
        return schemas_info
    
    def _build_templates(self) -> Dict[PromptType, PromptTemplate]:
        """Build all prompt templates"""
        return {
            PromptType.SNAPSHOT: self._build_snapshot_template(),
            PromptType.SUPPORT_RESISTANCE: self._build_sr_template(),
            PromptType.TECHNICAL: self._build_technical_template()
        }
    
    def _build_snapshot_template(self) -> PromptTemplate:
        """Build stock snapshot prompt template with JSON schema"""
        base_template = """Provide a comprehensive stock snapshot analysis for {ticker} ({company}).

Focus on current market data and recent performance metrics. Return data as valid JSON only."""

        # Get JSON schema if available, otherwise use simplified schema
        if SNAPSHOT_SCHEMA:
            schema_str = json.dumps(SNAPSHOT_SCHEMA, indent=2)
            formatting_instructions = f"""REQUIRED JSON SCHEMA:
The response must conform to this exact JSON schema:

{schema_str}

CRITICAL REQUIREMENTS:
- Must be valid JSON matching the schema above
- Include current timestamp in metadata.timestamp (ISO 8601 format)
- All numeric fields must be numbers, not strings
- Ticker symbol must be uppercase in metadata.ticker_symbol
- Current price, volume, and OHLC data are required"""
        else:
            formatting_instructions = """REQUIRED JSON FORMAT:
{
  "metadata": {
    "timestamp": "2024-12-17T10:30:00Z",
    "ticker_symbol": "TICKER",
    "company_name": "Company Name",
    "data_source": "polygon",
    "confidence_score": 0.95,
    "schema_version": "1.0"
  },
  "snapshot_data": {
    "current_price": 150.25,
    "percentage_change": 2.5,
    "dollar_change": 3.75,
    "volume": 45000000,
    "vwap": 149.80,
    "open": 148.50,
    "high": 151.00,
    "low": 147.25,
    "close": 146.50
  }
}"""

        # Generate example response using the schema
        current_time = datetime.utcnow().isoformat() + "Z"
        example_response = json.dumps({
            "metadata": {
                "timestamp": current_time,
                "ticker_symbol": "AAPL",
                "company_name": "Apple Inc.",
                "data_source": "polygon",
                "confidence_score": 0.95,
                "schema_version": "1.0"
            },
            "snapshot_data": {
                "current_price": 150.25,
                "percentage_change": 2.5,
                "dollar_change": 3.75,
                "volume": 45000000,
                "vwap": 149.80,
                "open": 148.50,
                "high": 151.00,
                "low": 147.25,
                "close": 146.50
            }
        }, indent=2)

        return PromptTemplate(
            template_type=PromptType.SNAPSHOT,
            base_template=base_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            required_fields=["metadata", "snapshot_data"]
        )
    
    def _build_sr_template(self) -> PromptTemplate:
        """Build support & resistance prompt template with JSON schema"""  
        base_template = """Analyze support and resistance levels for {ticker} ({company}).

Provide 3 support levels and 3 resistance levels based on recent price action and technical analysis. Return data as valid JSON only."""

        # Get JSON schema if available, otherwise use simplified schema
        if SUPPORT_RESISTANCE_SCHEMA:
            schema_str = json.dumps(SUPPORT_RESISTANCE_SCHEMA, indent=2)
            formatting_instructions = f"""REQUIRED JSON SCHEMA:
The response must conform to this exact JSON schema:

{schema_str}

CRITICAL REQUIREMENTS:
- Must be valid JSON matching the schema above
- Include current timestamp in metadata.timestamp (ISO 8601 format)
- All price values must be numbers, not strings
- Support levels (S1, S2, S3) and resistance levels (R1, R2, R3) are required
- Include strength indicators (strong, moderate, weak) for each level"""
        else:
            formatting_instructions = """REQUIRED JSON FORMAT:
{
  "metadata": {
    "timestamp": "2024-12-17T10:30:00Z",
    "ticker_symbol": "TICKER",
    "company_name": "Company Name",
    "analysis_timeframe": "1M",
    "confidence_score": 0.85,
    "schema_version": "1.0"
  },
  "support_levels": {
    "S1": {"price": 145.50, "strength": "strong", "confidence": 0.9},
    "S2": {"price": 142.00, "strength": "moderate", "confidence": 0.8},
    "S3": {"price": 138.75, "strength": "weak", "confidence": 0.7}
  },
  "resistance_levels": {
    "R1": {"price": 155.25, "strength": "moderate", "confidence": 0.85},
    "R2": {"price": 158.50, "strength": "strong", "confidence": 0.9},
    "R3": {"price": 162.00, "strength": "weak", "confidence": 0.75}
  }
}"""

        # Generate example response using the schema
        current_time = datetime.utcnow().isoformat() + "Z"
        example_response = json.dumps({
            "metadata": {
                "timestamp": current_time,
                "ticker_symbol": "AAPL",
                "company_name": "Apple Inc.",
                "analysis_timeframe": "1M",
                "confidence_score": 0.85,
                "schema_version": "1.0"
            },
            "support_levels": {
                "S1": {"price": 145.50, "strength": "strong", "confidence": 0.9},
                "S2": {"price": 142.00, "strength": "moderate", "confidence": 0.8},
                "S3": {"price": 138.75, "strength": "weak", "confidence": 0.7}
            },
            "resistance_levels": {
                "R1": {"price": 155.25, "strength": "moderate", "confidence": 0.85},
                "R2": {"price": 158.50, "strength": "strong", "confidence": 0.9},
                "R3": {"price": 162.00, "strength": "weak", "confidence": 0.75}
            },
            "analysis_context": {
                "current_price": 150.25,
                "methodology": "combined"
            }
        }, indent=2)

        return PromptTemplate(
            template_type=PromptType.SUPPORT_RESISTANCE,
            base_template=base_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            required_fields=["metadata", "support_levels", "resistance_levels"]
        )
    
    def _build_technical_template(self) -> PromptTemplate:
        """Build technical analysis prompt template with JSON schema"""
        base_template = """Provide technical indicator analysis for {ticker} ({company}).

Calculate current values for key oscillators and moving averages. Return data as valid JSON only."""

        # Get JSON schema if available, otherwise use simplified schema
        if TECHNICAL_SCHEMA:
            schema_str = json.dumps(TECHNICAL_SCHEMA, indent=2)
            formatting_instructions = f"""REQUIRED JSON SCHEMA:
The response must conform to this exact JSON schema:

{schema_str}

CRITICAL REQUIREMENTS:
- Must be valid JSON matching the schema above
- Include current timestamp in metadata.timestamp (ISO 8601 format)
- All numeric values must be numbers, not strings
- RSI value must be between 0-100
- MACD values can be positive or negative
- All moving averages (EMA and SMA) must be positive numbers"""
        else:
            formatting_instructions = """REQUIRED JSON FORMAT:
{
  "metadata": {
    "timestamp": "2024-12-17T10:30:00Z",
    "ticker_symbol": "TICKER",
    "company_name": "Company Name",
    "analysis_period": "1M",
    "confidence_score": 0.88,
    "schema_version": "1.0"
  },
  "oscillators": {
    "RSI": {"value": 68.5, "interpretation": "neutral", "period": 14},
    "MACD": {"value": 0.25, "signal": 0.18, "histogram": 0.07, "interpretation": "bullish"}
  },
  "moving_averages": {
    "exponential": {
      "EMA_5": 151.20,
      "EMA_10": 149.85,
      "EMA_20": 147.50,
      "EMA_50": 144.75,
      "EMA_200": 140.25
    },
    "simple": {
      "SMA_5": 150.95,
      "SMA_10": 148.75,
      "SMA_20": 146.80,
      "SMA_50": 143.90,
      "SMA_200": 139.50
    }
  }
}"""

        # Generate example response using the schema
        current_time = datetime.utcnow().isoformat() + "Z"
        example_response = json.dumps({
            "metadata": {
                "timestamp": current_time,
                "ticker_symbol": "AAPL",
                "company_name": "Apple Inc.",
                "analysis_period": "1M",
                "confidence_score": 0.88,
                "schema_version": "1.0"
            },
            "oscillators": {
                "RSI": {"value": 68.5, "interpretation": "neutral", "period": 14},
                "MACD": {"value": 0.25, "signal": 0.18, "histogram": 0.07, "interpretation": "bullish"}
            },
            "moving_averages": {
                "exponential": {
                    "EMA_5": 151.20,
                    "EMA_10": 149.85,
                    "EMA_20": 147.50,
                    "EMA_50": 144.75,
                    "EMA_200": 140.25
                },
                "simple": {
                    "SMA_5": 150.95,
                    "SMA_10": 148.75,
                    "SMA_20": 146.80,
                    "SMA_50": 143.90,
                    "SMA_200": 139.50
                }
            },
            "analysis_summary": {
                "trend_direction": "bullish",
                "signal_strength": "moderate",
                "recommendations": ["hold", "watch"]
            }
        }, indent=2)

        return PromptTemplate(
            template_type=PromptType.TECHNICAL,
            base_template=base_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            required_fields=["metadata", "oscillators", "moving_averages"]
        )
    
    def _build_system_prompt_enhancements(self) -> str:
        """Build system prompt enhancements for JSON structured output"""
        return """JSON STRUCTURED OUTPUT REQUIREMENTS:

1. **JSON COMPLIANCE**: Respond with VALID JSON ONLY - no explanations, no markdown, no additional text
2. **Schema Adherence**: Must exactly match the JSON schema structure provided in prompts
3. **Data Types**: All numeric fields must be numbers, not strings (e.g., 150.25 not "150.25")
4. **Required Fields**: All required fields in the schema must be present
5. **Timestamp Format**: Include current timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

JSON FORMATTING RULES:
- Use proper JSON syntax with correct quotes and commas
- Numeric values: integers for counts/volume, floats for prices/percentages
- String values: ticker symbols in uppercase, proper company names
- Boolean values: true/false (lowercase)
- Arrays: for lists like recommendations or warnings

DATA QUALITY REQUIREMENTS:
- Provide real, current market data when possible
- If data unavailable, use null values rather than estimates
- Ensure RSI values are between 0-100
- Ensure price values are positive numbers
- Include confidence scores between 0.0-1.0 where specified

RESPONSE VALIDATION:
- The entire response must be parseable as valid JSON
- No comments or explanations outside the JSON structure
- Follow the exact schema structure for metadata, analysis data, and optional fields
- Include proper error handling in the JSON structure if data cannot be retrieved

This JSON-first approach ensures seamless integration with automated systems and eliminates parsing errors."""

    def test_prompt_consistency(self, prompt_type: PromptType, 
                              test_tickers: List[str]) -> Dict[str, Any]:
        """
        Test prompt consistency across different ticker symbols
        
        Args:
            prompt_type: Type of prompt to test
            test_tickers: List of ticker symbols to test
            
        Returns:
            Dictionary with consistency test results
        """
        results = {
            "prompt_type": prompt_type.value,
            "test_tickers": test_tickers,
            "prompts": {},
            "consistency_score": 0.0,
            "issues": []
        }
        
        prompts = []
        for ticker in test_tickers:
            try:
                prompt, context = self.generate_prompt(prompt_type, ticker=ticker)
                prompts.append(prompt)
                results["prompts"][ticker] = {
                    "prompt": prompt,
                    "context": context.__dict__,
                    "length": len(prompt),
                    "word_count": len(prompt.split())
                }
            except Exception as e:
                results["issues"].append(f"Failed to generate prompt for {ticker}: {e}")
        
        # Analyze consistency
        if len(prompts) > 1:
            # Check template structure consistency
            structures = []
            for prompt in prompts:
                lines = [line.strip() for line in prompt.split('\n') if line.strip()]
                section_headers = [line for line in lines if line.startswith('###')]
                structures.append(section_headers)
            
            # All prompts should have same section structure
            if all(struct == structures[0] for struct in structures):
                results["consistency_score"] += 0.5
            else:
                results["issues"].append("Inconsistent section structures across prompts")
            
            # Check length consistency (should be within 20% of each other)
            lengths = [len(p) for p in prompts]
            avg_length = sum(lengths) / len(lengths)
            if all(abs(length - avg_length) / avg_length < 0.2 for length in lengths):
                results["consistency_score"] += 0.5
            else:
                results["issues"].append("Inconsistent prompt lengths across tickers")
        
        return results


# ====== Testing and Validation Functions ======

def run_prompt_consistency_tests() -> Dict[str, Any]:
    """Run comprehensive prompt consistency tests"""
    manager = PromptTemplateManager()
    
    test_results = {
        "test_date": "2024-12-01",
        "results_by_type": {},
        "overall_score": 0.0,
        "summary": {}
    }
    
    # Test tickers representing different sectors and market caps
    test_tickers = ["AAPL", "TSLA", "JPM", "NVDA", "AMZN"]
    
    total_score = 0.0
    
    for prompt_type in PromptType:
        results = manager.test_prompt_consistency(prompt_type, test_tickers)
        test_results["results_by_type"][prompt_type.value] = results
        total_score += results["consistency_score"]
    
    test_results["overall_score"] = total_score / len(PromptType)
    
    # Generate summary
    all_issues = []
    for type_results in test_results["results_by_type"].values():
        all_issues.extend(type_results["issues"])
    
    test_results["summary"] = {
        "total_prompts_generated": len(PromptType) * len(test_tickers),
        "total_issues": len(all_issues),
        "consistency_rating": "EXCELLENT" if test_results["overall_score"] > 0.8 
                            else "GOOD" if test_results["overall_score"] > 0.6 
                            else "NEEDS_IMPROVEMENT"
    }
    
    return test_results


def validate_template_parsing_compatibility() -> Dict[str, Any]:
    """Validate that templates are compatible with ResponseParser"""
    from response_parser import ResponseParser, DataType
    
    manager = PromptTemplateManager()
    parser = ResponseParser()
    
    validation_results = {
        "template_compatibility": {},
        "parsing_success_rate": {},
        "recommendations": []
    }
    
    # Test each template type
    for prompt_type in PromptType:
        template = manager.templates[prompt_type]
        example_response = template.example_response
        
        # Map PromptType to DataType
        data_type_map = {
            PromptType.SNAPSHOT: DataType.SNAPSHOT,
            PromptType.SUPPORT_RESISTANCE: DataType.SUPPORT_RESISTANCE,  
            PromptType.TECHNICAL: DataType.TECHNICAL
        }
        
        data_type = data_type_map[prompt_type]
        
        try:
            # Test parsing the example response
            parse_result = parser.parse_any(example_response, data_type, "TEST")
            
            validation_results["template_compatibility"][prompt_type.value] = {
                "status": "compatible",
                "confidence": parse_result.confidence.value,
                "fields_extracted": len(parse_result.parsed_data),
                "expected_fields": len(template.required_fields),
                "extraction_rate": len(parse_result.parsed_data) / len(template.required_fields)
            }
            
        except Exception as e:
            validation_results["template_compatibility"][prompt_type.value] = {
                "status": "incompatible", 
                "error": str(e),
                "extraction_rate": 0.0
            }
    
    # Calculate overall success rate
    success_rates = []
    for result in validation_results["template_compatibility"].values():
        if result.get("extraction_rate"):
            success_rates.append(result["extraction_rate"])
    
    if success_rates:
        validation_results["parsing_success_rate"] = {
            "average": sum(success_rates) / len(success_rates),
            "minimum": min(success_rates),
            "maximum": max(success_rates)
        }
    
    # Generate recommendations
    for prompt_type, result in validation_results["template_compatibility"].items():
        if result.get("extraction_rate", 0) < 0.8:
            validation_results["recommendations"].append(
                f"Improve {prompt_type} template formatting for better parsing compatibility"
            )
    
    return validation_results


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run tests
    print("🧪 Running Prompt Template Tests")
    print("=" * 50)
    
    # Test consistency
    consistency_results = run_prompt_consistency_tests()
    print(f"✅ Consistency Tests: {consistency_results['summary']['consistency_rating']}")
    print(f"   Score: {consistency_results['overall_score']:.2f}")
    print(f"   Issues: {consistency_results['summary']['total_issues']}")
    
    # Test parsing compatibility  
    print("\n🔍 Testing ResponseParser Compatibility")
    parsing_results = validate_template_parsing_compatibility()
    avg_success = parsing_results["parsing_success_rate"]["average"]
    print(f"✅ Parsing Success Rate: {avg_success:.1%}")
    
    if avg_success >= 0.9:
        print("🎉 Excellent parsing compatibility!")
    elif avg_success >= 0.7:
        print("✅ Good parsing compatibility")
    else:
        print("⚠️  Parsing compatibility needs improvement")
    
    # Test example generation
    print("\n📝 Testing Prompt Generation")
    manager = PromptTemplateManager()
    
    for prompt_type in PromptType:
        try:
            prompt, context = manager.generate_prompt(prompt_type, ticker="AAPL")
            print(f"✅ {prompt_type.value}: Generated {len(prompt)} characters")
        except Exception as e:
            print(f"❌ {prompt_type.value}: Failed - {e}")
    
    print(f"\n🏁 All tests completed successfully!")
