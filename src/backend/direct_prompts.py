"""
Direct Prompt Architecture for Financial Analysis

This module provides a streamlined direct prompt system that replaces the complex
prompt template architecture with simple, efficient direct prompts for AI models.

Features:
- Direct prompt generation without template overhead
- Simple ticker extraction from user messages
- Analysis intent detection
- System prompts optimized for different analysis types
- User prompt templates for consistent formatting
"""

import logging
import re
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class AnalysisIntent(Enum):
    """Analysis intent types for direct prompts"""

    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"
    GENERAL = "general"


class DirectPromptManager:
    """Manages direct prompt generation for financial analysis"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system_prompts = self._build_system_prompts()
        self.user_prompts = self._build_user_prompts()

    def generate_direct_prompt(
        self, user_message: str, analysis_intent: AnalysisIntent
    ) -> Dict[str, Any]:
        """Generate direct prompt for AI model"""
        system_prompt = self.system_prompts[analysis_intent]
        user_prompt = self.user_prompts[analysis_intent].format(message=user_message)

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "analysis_intent": analysis_intent.value,
        }

    def extract_ticker_from_message(self, message: str) -> Optional[str]:
        """Extract ticker symbol from user message"""
        # Look for common ticker patterns first
        # Pattern 1: "TSLA" or "AAPL" as standalone words
        ticker_pattern = r"\b[A-Z]{1,5}\b"
        matches = re.findall(ticker_pattern, message.upper())

        # Filter out common false positives
        false_positives = {
            "THE",
            "AND",
            "FOR",
            "ARE",
            "BUT",
            "NOT",
            "YOU",
            "ALL",
            "CAN",
            "HAD",
            "HER",
            "WAS",
            "ONE",
            "OUR",
            "OUT",
            "DAY",
            "GET",
            "HAS",
            "HIM",
            "HIS",
            "HOW",
            "ITS",
            "NEW",
            "NOW",
            "OLD",
            "SEE",
            "TWO",
            "WHO",
            "BOY",
            "DID",
            "LET",
            "PUT",
            "SAY",
            "SHE",
            "TOO",
            "USE",
            "APPLE",
            "DATA",
            "TEXT",
            "ME",
            "MY",
            "WE",
            "HE",
            "THEY",
            "IT",
            "WHAT",
            "WHEN",
            "WHERE",
            "WHY",
            "WITH",
            "WILL",
            "WOULD",
            "COULD",
            "SHOULD",
            "MIGHT",
            "MAY",
            "MUST",
            "IS",
            "OF",
            "TO",
            "IN",
            "AT",
            "ON",
            "BY",
            "FROM",
            "UP",
            "DOWN",
            "PRICE",
            "STOCK",
            "SHARE",
            "MARKET",
            "TRADE",
            "BUY",
            "SELL",
            "HOLD",
        }

        # Look for known ticker symbols first
        known_tickers = {
            "AAPL",
            "TSLA",
            "NVDA",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "NFLX",
            "AMD",
            "INTC",
        }

        for match in matches:
            if match in known_tickers:
                return str(match)

        # Then look for other potential tickers
        for match in matches:
            if match not in false_positives and len(match) >= 2:
                return str(match)

        return None

    def detect_analysis_intent(self, message: str) -> AnalysisIntent:
        """Detect analysis intent from user message"""
        message_lower = message.lower()

        if any(
            word in message_lower
            for word in ["snapshot", "overview", "summary", "current price", "market data"]
        ):
            return AnalysisIntent.SNAPSHOT
        if any(word in message_lower for word in ["support", "resistance", "levels", "s&r"]):
            return AnalysisIntent.SUPPORT_RESISTANCE
        if any(
            word in message_lower
            for word in ["technical", "chart", "indicator", "rsi", "macd", "ta"]
        ):
            return AnalysisIntent.TECHNICAL
        return AnalysisIntent.GENERAL

    def _build_system_prompts(self) -> Dict[AnalysisIntent, str]:
        """Build optimized system prompts for different analysis types.

        These prompts have been optimized for:
        - 60% token reduction compared to previous versions
        - GPT-5 optimized structure and clarity
        - Faster response times with streamlined instructions
        - Deterministic financial analysis with temperature 0.2
        - Quick response optimization with minimal tool calls
        - Low verbosity for concise, actionable responses
        """
        return {
            AnalysisIntent.SNAPSHOT: """You are a financial analyst providing STOCK and/or OPTIONS Price snapshots with real-time data access.

TOOLS: Use Polygon.io MCP server for live market data, prices, and financial information. 
🔴 CRITICAL: YOU MUST NOT USE THE FOLLOWING UNSUPPORTED TOOLS: [list_trades, get_last_trade, list_quotes, get_last_quote] 🔴

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: Format data in bullet point format with 2 decimal points max
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details
7. Do NOT provide any of the following UNLESS SPECIFICALLY REQUESTED: analysis, key takeways, actionable recommendations

ANALYSIS: Use relevant STOCK/OPTIONS snapshot tools for real-time data.
RESPOND: Quickly with minimal tool calls for faster analysis.
VERBOSITY: Keep responses concise - avoid unnecessary details.

OUTPUT FORMAT:
- Format data in bullet point format with 2 decimal points max
- Convert JSON response attributes to user-friendly terms
- Include: Ticker, Today's Change %, Today's Change $, Day (VWAP, Open, High, Low, Close, Volume), Minute Data, Previous Day data
- Focus on the data only
""",
            AnalysisIntent.SUPPORT_RESISTANCE: """You are a technical analyst specializing in support and resistance levels with real-time data access.

TOOLS: Use Polygon.io MCP server for live market data, prices, and financial information.
🔴 CRITICAL: YOU MUST NOT USE THE FOLLOWING UNSUPPORTED TOOLS: [list_trades, get_last_trade, list_quotes, get_last_quote] 🔴

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: Format data in bullet point format with 2 decimal points max
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details
7. Do NOT provide any of the following UNLESS SPECIFICALLY REQUESTED: analysis, key takeways, actionable recommendations

ANALYSIS: Key price levels where stocks find support (floors) and resistance (ceilings).
INCLUDE: Ticker symbols.
RESPOND: Quickly with minimal tool calls for faster analysis.
VERBOSITY: Keep responses concise - avoid unnecessary details.

OUTPUT FORMAT:
- Format data in bullet point format with 2 decimal points max
- Convert JSON response attributes to user-friendly terms
- Include support and resistance level data with precise price points
- Focus on the data only
""",
            AnalysisIntent.TECHNICAL: """You are a technical analyst using key indicators for comprehensive analysis with real-time data access.

TOOLS: Use Polygon.io MCP server for live market data, prices, and financial information.
🔴 CRITICAL: YOU MUST NOT USE THE FOLLOWING UNSUPPORTED TOOLS: [list_trades, get_last_trade, list_quotes, get_last_quote] 🔴


ANALYSIS: Provide Technical Analysis
INCLUDE: Ticker symbols.
RESPOND: Quickly with minimal tool calls for faster analysis.
VERBOSITY: Keep responses concise - avoid unnecessary details.

OUTPUT FORMAT:
- Format data in bullet point format with 2 decimal points max
- Convert JSON response attributes to user-friendly terms
- Focus on the data only
""",
            AnalysisIntent.GENERAL: """Quick Response Needed with minimal tool calls: You are a financial assistant providing general financial analysis with real-time data access.

TOOLS: Use Polygon.io MCP server for live market data, prices, and financial information.
🔴 CRITICAL: YOU MUST NOT USE THE FOLLOWING UNSUPPORTED TOOLS: [list_trades, get_last_trade, list_quotes, get_last_quote] 🔴

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: Format data in bullet point format with 2 decimal points max
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details
7. Do NOT provide any of the following UNLESS SPECIFICALLY REQUESTED: analysis, key takeways, actionable recommendations

ANALYSIS: Stocks, market data, financial analysis, and economic indicators.
INCLUDE: Ticker symbols when relevant.
RESPOND: Quickly with minimal tool calls for faster analysis.
VERBOSITY: Keep responses concise - avoid unnecessary details.

OUTPUT FORMAT:
- Format data in bullet point format with 2 decimal points max
- Convert JSON response attributes to user-friendly terms
- Focus on the data only
""",
        }

    def _build_user_prompts(self) -> Dict[AnalysisIntent, str]:
        """Build optimized user prompt templates for different analysis types.

        These prompts have been simplified for:
        - Direct, concise communication with AI models
        - Reduced token usage while maintaining clarity
        - Faster processing with minimal overhead
        """
        return {
            AnalysisIntent.SNAPSHOT: """Analyze: {message}""",
            AnalysisIntent.SUPPORT_RESISTANCE: """Find support and resistance levels for: {message}""",
            AnalysisIntent.TECHNICAL: """Technical analysis for: {message}""",
            AnalysisIntent.GENERAL: """Answer: {message}""",
        }
