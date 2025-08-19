"""
Stock Market Analysis Prompt Templates - Unified Conversational Architecture

This module provides sophisticated prompt templates for unified conversational financial analysis.
Removes JSON extraction attempts and focuses on enhanced conversational responses.

Features:
- Unified conversational prompt generation for all interactions
- Template-based prompt generation optimized for readability
- Ticker symbol extraction and context awareness
- Enhanced conversational formatting instructions
- Multi-stock analysis consistency
- Response formatting instructions optimized for natural language
- Removal of JSON schema dependencies for simplified architecture
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class PromptType(Enum):
    """Types of stock analysis prompts"""
    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"


class PromptMode(Enum):
    """Response modes for prompts - unified conversational"""
    CONVERSATIONAL = "conversational"    # Unified conversational response for all interactions


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
    """Template for generating unified conversational prompts"""
    template_type: PromptType
    conversational_template: str
    formatting_instructions: str
    example_response: str
    context_guidance: str = ""
    
    def generate_prompt(self, ticker_context: TickerContext, 
                       custom_instructions: Optional[str] = None,
                       mode: PromptMode = PromptMode.CONVERSATIONAL) -> str:
        """Generate a complete conversational prompt using the template"""
        
        # Unified conversational mode for all interactions
        prompt_parts = [
            self.conversational_template.format(
                ticker=ticker_context.symbol,
                company=ticker_context.company_name or ticker_context.symbol,
            ),
        ]
        
        if custom_instructions:
            prompt_parts.append(f"\nAdditional context: {custom_instructions}")
        
        # Add conversational formatting instructions
        prompt_parts.extend([
            "",
            self.formatting_instructions,
        ])
        
        if self.context_guidance:
            prompt_parts.extend([
                "",
                self.context_guidance
            ])
        
        # Add example for context
        if self.example_response:
            prompt_parts.extend([
                "",
                "Example response style:",
                self.example_response
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
    """Manages and generates unified conversational stock analysis prompt templates"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ticker_extractor = TickerExtractor()
        self.templates = self._build_templates()
    
    def generate_prompt(self, prompt_type: PromptType, ticker: Optional[str] = None,
                       chat_history: Optional[List[Dict]] = None,
                       custom_instructions: Optional[str] = None,
                       mode: PromptMode = PromptMode.CONVERSATIONAL) -> Tuple[str, TickerContext]:
        """
        Generate a unified conversational prompt for stock analysis
        
        Args:
            prompt_type: Type of analysis prompt
            ticker: Optional explicit ticker symbol
            chat_history: Conversation history for context
            custom_instructions: Additional instructions
            mode: PromptMode (always conversational)
            
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
        
        # Generate the prompt in specified mode
        prompt = template.generate_prompt(ticker_context, custom_instructions, mode)
        
        self.logger.info(f"Generated {prompt_type.value} conversational prompt for {ticker_context.symbol}")
        return prompt, ticker_context
    
    def generate_conversational_prompt(self, prompt_type: PromptType, ticker: Optional[str] = None,
                                      chat_history: Optional[List[Dict]] = None,
                                      custom_instructions: Optional[str] = None) -> Tuple[str, TickerContext]:
        """
        Generate a conversational prompt for any type of analysis request.
        
        Args:
            prompt_type: Type of analysis prompt
            ticker: Optional explicit ticker symbol
            chat_history: Conversation history for context
            custom_instructions: Additional instructions
            
        Returns:
            Tuple of (generated_prompt, ticker_context)
        """
        return self.generate_prompt(prompt_type, ticker, chat_history, custom_instructions, PromptMode.CONVERSATIONAL)
    
    def get_enhanced_system_prompt(self, base_system_prompt: str) -> str:
        """
        Enhance the base system prompt with conversational instructions
        
        Args:
            base_system_prompt: Original system prompt
            
        Returns:
            Enhanced system prompt with conversational guidance
        """
        conversational_enhancement = """

CONVERSATIONAL RESPONSE MODE:
- Provide helpful, informative responses in natural language
- Use clear, professional tone suitable for financial analysis
- Include relevant data and insights with enhanced formatting
- Make responses educational and actionable for investors
- Use emojis and structured formatting for better readability
- Do NOT return JSON - respond with well-formatted conversational text
- Focus on clarity, accuracy, and user-friendly explanations
"""
        return base_system_prompt + conversational_enhancement
    
    def detect_analysis_type(self, user_input: str) -> Optional[PromptType]:
        """
        Detect what type of analysis is being requested from user input
        
        Args:
            user_input: The input text
            
        Returns:
            PromptType if detected, None otherwise
        """
        user_lower = user_input.lower()
        
        # Check for different analysis type indicators
        if any(indicator in user_lower for indicator in 
               ["snapshot", "current price", "market data", "overview"]):
            return PromptType.SNAPSHOT
        elif any(indicator in user_lower for indicator in 
                 ["support", "resistance", "levels", "s&r"]):
            return PromptType.SUPPORT_RESISTANCE
        elif any(indicator in user_lower for indicator in 
                 ["technical", "rsi", "macd", "indicators", "ta"]):
            return PromptType.TECHNICAL
        
        return None
    
    
    def get_available_templates(self) -> Dict[str, Any]:
        """
        Get information about available conversational templates
        
        Returns:
            Dictionary with template availability and metadata
        """
        templates_info = {
            "mode": "conversational_only",
            "templates": {}
        }
        
        for prompt_type in PromptType:
            templates_info["templates"][prompt_type.value] = {
                "available": True,
                "type": "conversational",
                "enhanced_formatting": True
            }
        
        return templates_info
    
    def _build_templates(self) -> Dict[PromptType, PromptTemplate]:
        """Build all conversational prompt templates"""
        return {
            PromptType.SNAPSHOT: self._build_snapshot_template(),
            PromptType.SUPPORT_RESISTANCE: self._build_sr_template(),
            PromptType.TECHNICAL: self._build_technical_template()
        }
    
    def _build_snapshot_template(self) -> PromptTemplate:
        """Build stock snapshot conversational prompt template"""
        conversational_template = """Provide a comprehensive stock snapshot analysis for {ticker} ({company}).

IMPORTANT: Execute this analysis immediately without asking for confirmation. Provide the complete analysis directly.

Please include current market data and recent performance metrics. Focus on providing clear, actionable insights for investors."""
        
        formatting_instructions = """RESPONSE FORMATTING GUIDELINES:
- Start immediately with the analysis. Do NOT ask for user confirmation or clarification.
- Start with current price and percentage change
- Include trading volume and volume analysis
- Provide OHLC data (Open, High, Low, Close) with context
- Explain what the data means for potential investors
- Use emojis for EVERY bullet point
- Use **🟢 GREEN** for bullish indicators and **🔴 RED** for bearish indicators
- Use clear, professional language with proper formatting
- Include relevant market context and trends
- Make the analysis educational and actionable
- End each response with 2-3 relevant follow-up questions"""
        
        example_response = """📊 **Apple Inc. (AAPL) Market Snapshot**

💰 **Current Price:** $150.25 (+2.5% / +$3.75)
📈 **Trading Volume:** 45,000,000 shares (above average)
📊 **Daily Range:** $147.25 - $151.00
🏁 **Previous Close:** $146.50
⚖️ **VWAP:** $149.80

**Analysis:** Apple is showing strong bullish momentum with above-average volume support. The stock has broken above key resistance levels and is trading near daily highs, suggesting continued investor confidence."""
        
        context_guidance = """Provide the complete analysis without requesting additional input from the user. Focus on making the data accessible and meaningful for both novice and experienced investors. Explain the significance of price movements and volume patterns."""
        
        return PromptTemplate(
            template_type=PromptType.SNAPSHOT,
            conversational_template=conversational_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            context_guidance=context_guidance
        )
    
    def _build_sr_template(self) -> PromptTemplate:
        """Build support & resistance conversational prompt template"""
        conversational_template = """Analyze the key support and resistance levels for {ticker} ({company}).

IMPORTANT: Execute this analysis immediately without asking for confirmation. Provide the complete analysis directly.

Identify the most important price levels where the stock tends to find support (price floors) and resistance (price ceilings). Explain the significance of these levels for trading decisions."""
        
        formatting_instructions = """RESPONSE FORMATTING GUIDELINES:
- Start immediately with the analysis. Do NOT ask for user confirmation or clarification.
- Identify 3 key support levels and 3 key resistance levels
- Explain the strength of each level (strong, moderate, weak)
- Provide price targets with reasoning
- Explain the methodology used (technical analysis, historical data, etc.)
- Include current price context and trend analysis
- Use emojis for EVERY bullet point
- Use **🟢 GREEN** for bullish indicators and **🔴 RED** for bearish indicators
- Make recommendations clear and actionable for traders
- End each response with 2-3 relevant follow-up questions"""
        
        example_response = """🎯 **Apple Inc. (AAPL) Support & Resistance Analysis**

🔻 **Support Levels:**
• **S1: $145.50** (Strong) - 50-day moving average confluence
• **S2: $142.00** (Moderate) - Previous breakout level
• **S3: $138.75** (Weak) - Psychological support zone

🔺 **Resistance Levels:**
• **R1: $155.25** (Moderate) - Recent high rejection point
• **R2: $158.50** (Strong) - Key technical resistance
• **R3: $162.00** (Weak) - Long-term trend line

📈 **Current Price:** $150.25 (between S1 and R1)

**Trading Strategy:** Watch for bounces at support levels for long entries, and resistance levels for profit-taking opportunities."""
        
        context_guidance = """Provide the complete analysis without requesting additional input from the user. Focus on actionable trading insights and explain why these levels are significant based on technical analysis and market structure."""
        
        return PromptTemplate(
            template_type=PromptType.SUPPORT_RESISTANCE,
            conversational_template=conversational_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            context_guidance=context_guidance
        )
    
    def _build_technical_template(self) -> PromptTemplate:
        """Build technical analysis conversational prompt template"""
        conversational_template = """Provide a comprehensive technical analysis for {ticker} ({company}) using key indicators.

IMPORTANT: Execute this analysis immediately without asking for confirmation. Provide the complete analysis directly.

Analyze current technical indicators including RSI, MACD, and moving averages. Explain what these indicators suggest about the stock's momentum and trend direction."""
        
        formatting_instructions = """RESPONSE FORMATTING GUIDELINES:
- Start immediately with the analysis. Do NOT ask for user confirmation or clarification.
- Include key oscillators (RSI, MACD) with current values and interpretations
- Provide moving average analysis (short-term and long-term trends)
- Explain momentum and trend direction based on indicators
- Include bullish/bearish signals and their strength
- Provide trading recommendations based on technical setup
- Use emojis for EVERY bullet point
- Use **🟢 GREEN** for bullish indicators and **🔴 RED** for bearish indicators
- Make technical concepts accessible to both novice and experienced traders
- End each response with 2-3 relevant follow-up questions"""
        
        example_response = """🔍 **Apple Inc. (AAPL) Technical Analysis**

📈 **Momentum Indicators:**
• **RSI (14):** 68.5 - Approaching overbought territory, but still neutral
• **MACD:** 0.25 above signal line (0.18) - Bullish momentum confirmed

📊 **Moving Averages:**
• **Short-term:** Price above EMA-5 ($151.20) and EMA-10 ($149.85)
• **Medium-term:** Strong support at EMA-50 ($144.75)
• **Long-term:** Well above EMA-200 ($140.25) - Bullish trend intact

✨ **Analysis Summary:**
🔹 **Trend Direction:** Bullish with moderate momentum
🔹 **Signal Strength:** Moderate - watch for RSI divergence
🔹 **Recommendation:** Hold current positions, watch for pullback opportunities"""
        
        context_guidance = """Provide the complete analysis without requesting additional input from the user. Make technical analysis accessible and actionable. Explain what each indicator means and how it affects trading decisions."""
        
        return PromptTemplate(
            template_type=PromptType.TECHNICAL,
            conversational_template=conversational_template,
            formatting_instructions=formatting_instructions,
            example_response=example_response,
            context_guidance=context_guidance
        )
    

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


def test_dual_mode_behavior() -> Dict[str, Any]:
    """Test dual-mode prompt generation behavior"""
    manager = PromptTemplateManager()
    
    test_results = {
        "dual_mode_tests": {},
        "mode_detection_tests": {},
        "system_prompt_tests": {},
        "overall_success": True
    }
    
    # Test dual mode generation for each prompt type
    for prompt_type in PromptType:
        try:
            # Test button mode
            button_prompt, button_context = manager.generate_prompt(
                prompt_type, ticker="AAPL", mode=PromptMode.BUTTON_JSON
            )
            
            # Test user mode
            user_prompt, user_context = manager.generate_prompt(
                prompt_type, ticker="AAPL", mode=PromptMode.USER_TEXT
            )
            
            test_results["dual_mode_tests"][prompt_type.value] = {
                "button_mode": {
                    "length": len(button_prompt),
                    "has_json_instructions": "JSON" in button_prompt,
                    "has_schema": "SCHEMA" in button_prompt
                },
                "user_mode": {
                    "length": len(user_prompt),
                    "has_json_instructions": "JSON" in user_prompt,
                    "is_conversational": "conversational" in user_prompt.lower()
                },
                "different_outputs": button_prompt != user_prompt
            }
            
        except Exception as e:
            test_results["dual_mode_tests"][prompt_type.value] = {"error": str(e)}
            test_results["overall_success"] = False
    
    # Test mode detection
    test_inputs = [
        ("Tell me about AAPL", None, PromptMode.USER_TEXT),
        ("Generate snapshot analysis", None, PromptMode.BUTTON_JSON),
        ("What's the price of Tesla?", None, PromptMode.USER_TEXT),
        ("Any question", "snapshot", PromptMode.BUTTON_JSON),
    ]
    
    for input_text, button_context, expected_mode in test_inputs:
        detected_mode = manager.detect_prompt_source(input_text, button_context)
        test_results["mode_detection_tests"][input_text[:20]] = {
            "expected": expected_mode.value,
            "detected": detected_mode.value,
            "correct": detected_mode == expected_mode
        }
    
    # Test system prompt enhancement
    base_prompt = "You are a financial analyst."
    
    json_enhanced = manager.get_enhanced_system_prompt(base_prompt, PromptMode.BUTTON_JSON)
    text_enhanced = manager.get_enhanced_system_prompt(base_prompt, PromptMode.USER_TEXT)
    
    test_results["system_prompt_tests"] = {
        "json_mode_different": json_enhanced != base_prompt,
        "text_mode_different": text_enhanced != base_prompt,
        "modes_different": json_enhanced != text_enhanced,
        "json_has_json_instructions": "JSON" in json_enhanced,
        "text_has_conversational": "conversational" in text_enhanced.lower()
    }
    
    return test_results


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run tests
    print("🧪 Running Enhanced Dual-Mode Prompt Template Tests")
    print("=" * 60)
    
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
    
    # NEW: Test dual-mode behavior
    print("\n🔄 Testing Dual-Mode Behavior")
    dual_mode_results = test_dual_mode_behavior()
    print(f"✅ Dual-Mode Tests: {'PASSED' if dual_mode_results['overall_success'] else 'FAILED'}")
    
    # Test example generation in both modes
    print("\n📝 Testing Dual-Mode Prompt Generation")
    manager = PromptTemplateManager()
    
    for prompt_type in PromptType:
        try:
            # Test button mode
            button_prompt, context = manager.generate_button_prompt(prompt_type, ticker="AAPL")
            user_prompt, context = manager.generate_user_prompt(prompt_type, ticker="AAPL")
            
            print(f"✅ {prompt_type.value}:")
            print(f"   Button mode: {len(button_prompt)} chars (JSON focused)")
            print(f"   User mode: {len(user_prompt)} chars (conversational)")
            
        except Exception as e:
            print(f"❌ {prompt_type.value}: Failed - {e}")
    
    print(f"\n🏁 All enhanced dual-mode tests completed!")