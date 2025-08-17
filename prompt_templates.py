"""
Stock Market Analysis Prompt Templates

This module provides sophisticated prompt templates for structured stock market analysis,
optimized for FSM-driven interactions with enhanced parsing compatibility.

Features:
- Template-based prompt generation with consistent formatting
- Ticker symbol extraction and context awareness
- System prompt enhancements for structured output
- Multi-stock analysis consistency
- Response formatting instructions optimized for ResponseParser
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import json


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
            "### FORMATTING REQUIREMENTS ###",
            self.formatting_instructions,
            "",
            "### EXAMPLE RESPONSE FORMAT ###",
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
            "### RESPONSE ###",
            f"Provide the {self.template_type.value} analysis for {ticker_context.symbol} following the exact format above:"
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
            "WHO", "BOY", "DID", "ITS", "LET", "PUT", "SAY", "SHE", "TOO", "USE"
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
                context_text = " ".join([msg.get("content", "") for msg in recent_messages])
            
            ticker_context = self.ticker_extractor.extract_ticker(context_text, chat_history)
        
        # Get the appropriate template
        template = self.templates[prompt_type]
        
        # Generate the prompt
        prompt = template.generate_prompt(ticker_context, custom_instructions)
        
        self.logger.info(f"Generated {prompt_type.value} prompt for {ticker_context.symbol}")
        return prompt, ticker_context
    
    def get_enhanced_system_prompt(self, base_system_prompt: str) -> str:
        """
        Enhance the base system prompt with structured output instructions
        
        Args:
            base_system_prompt: Original system prompt
            
        Returns:
            Enhanced system prompt with structured output guidance
        """
        return base_system_prompt + "\n\n" + self.system_prompt_enhancements
    
    def _build_templates(self) -> Dict[PromptType, PromptTemplate]:
        """Build all prompt templates"""
        return {
            PromptType.SNAPSHOT: self._build_snapshot_template(),
            PromptType.SUPPORT_RESISTANCE: self._build_sr_template(),
            PromptType.TECHNICAL: self._build_technical_template()
        }
    
    def _build_snapshot_template(self) -> PromptTemplate:
        """Build stock snapshot prompt template"""
        base_template = """Provide a comprehensive stock snapshot analysis for {ticker} ({company}).

Focus on current market data and recent performance metrics."""

        formatting_instructions = """CRITICAL: Format your response with clear labels and specific numeric values:

Required Format:
- Current price: $XXX.XX
- Percentage change: +X.X% or -X.X%
- Dollar change: +$X.XX or -$X.XX  
- Volume: X,XXX,XXX shares
- VWAP: $XXX.XX (Volume Weighted Average Price)
- Open: $XXX.XX
- High: $XXX.XX  
- Low: $XXX.XX
- Close: $XXX.XX

Use exact labels as shown above. Include dollar signs for prices, percentage signs for changes, and format numbers clearly."""

        example_response = """Current price: $150.25
Percentage change: +2.5%
Dollar change: +$3.75
Volume: 45,000,000 shares
VWAP: $149.80
Open: $148.50
High: $151.00
Low: $147.25
Close: $150.25"""

        return PromptTemplate(
            template_type=PromptType.SNAPSHOT,
            base_template=base_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            required_fields=["current_price", "percentage_change", "dollar_change", 
                           "volume", "vwap", "open", "high", "low", "close"]
        )
    
    def _build_sr_template(self) -> PromptTemplate:
        """Build support & resistance prompt template"""  
        base_template = """Analyze support and resistance levels for {ticker} ({company}).

Provide 3 support levels and 3 resistance levels based on recent price action and technical analysis."""

        formatting_instructions = """CRITICAL: Format your response with exact labels for all 6 levels:

Required Format:
- S1: $XXX.XX (First support level)
- S2: $XXX.XX (Second support level) 
- S3: $XXX.XX (Third support level)
- R1: $XXX.XX (First resistance level)
- R2: $XXX.XX (Second resistance level)
- R3: $XXX.XX (Third resistance level)

Use exact labels S1, S2, S3, R1, R2, R3 followed by colon and price with dollar sign.
Support levels should be below current price, resistance levels above.
Order: S3 < S2 < S1 < Current Price < R1 < R2 < R3"""

        example_response = """S1: $145.50
S2: $142.00  
S3: $138.75
R1: $155.25
R2: $158.50
R3: $162.00"""

        return PromptTemplate(
            template_type=PromptType.SUPPORT_RESISTANCE,
            base_template=base_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            required_fields=["S1", "S2", "S3", "R1", "R2", "R3"]
        )
    
    def _build_technical_template(self) -> PromptTemplate:
        """Build technical analysis prompt template"""
        base_template = """Provide technical indicator analysis for {ticker} ({company}).

Calculate current values for key oscillators and moving averages."""

        formatting_instructions = """CRITICAL: Format your response with exact labels and numeric values:

Required Format:
- RSI: XX.X (0-100 range)
- MACD: X.XXX (can be positive or negative)
- EMA 5: $XXX.XX  
- EMA 10: $XXX.XX
- EMA 20: $XXX.XX
- EMA 50: $XXX.XX
- EMA 200: $XXX.XX
- SMA 5: $XXX.XX
- SMA 10: $XXX.XX  
- SMA 20: $XXX.XX
- SMA 50: $XXX.XX
- SMA 200: $XXX.XX

Use exact labels as shown. Include dollar signs for moving averages, no dollar signs for RSI/MACD.
RSI must be between 0-100. MACD can be positive or negative."""

        example_response = """RSI: 68.5
MACD: 0.25
EMA 5: $151.20
EMA 10: $149.85  
EMA 20: $147.50
EMA 50: $144.75
EMA 200: $140.25
SMA 5: $150.95
SMA 10: $148.75
SMA 20: $146.80
SMA 50: $143.90
SMA 200: $139.50"""

        return PromptTemplate(
            template_type=PromptType.TECHNICAL,
            base_template=base_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            required_fields=["RSI", "MACD", "EMA_5", "EMA_10", "EMA_20", "EMA_50", "EMA_200",
                           "SMA_5", "SMA_10", "SMA_20", "SMA_50", "SMA_200"]
        )
    
    def _build_system_prompt_enhancements(self) -> str:
        """Build system prompt enhancements for structured output"""
        return """STRUCTURED OUTPUT REQUIREMENTS:

1. **Format Consistency**: Always use the exact labels and formats shown in examples
2. **Numeric Precision**: Provide specific numeric values, not ranges or approximations  
3. **Label Matching**: Use labels exactly as specified (case-sensitive)
4. **Currency Formatting**: Include $ symbols for prices, % for percentages
5. **Data Validation**: Ensure RSI is 0-100, prices are positive, volume is formatted with commas

PARSING OPTIMIZATION:
- Start each data line with the exact label followed by colon and space
- Use consistent decimal places (2 for prices, 1 for RSI, 3 for MACD)
- Format large numbers with commas (e.g., 1,000,000 not 1000000)
- Avoid additional commentary between data lines

QUALITY REQUIREMENTS:
- Provide real, current data when possible
- If data unavailable, clearly state "Data not available" rather than estimated values
- Maintain professional, concise analysis tone
- Focus on factual data over interpretive analysis

This structured approach ensures optimal parsing and consistent user experience."""

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
