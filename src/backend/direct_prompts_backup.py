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
        # Simple ticker extraction logic
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
        }

        for match in matches:
            if match not in false_positives:
                return match

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
        """Build system prompts for different analysis types"""
        return {
            AnalysisIntent.SNAPSHOT: """You are a financial analyst specializing in stock market snapshots.
Provide comprehensive, real-time market analysis with current price data, volume analysis, and key performance metrics.
Always include ticker symbols, use financial emojis (📈 for bullish, 📉 for bearish), and structure responses with:
🎯 KEY TAKEAWAYS (bullet points)
📊 DETAILED ANALYSIS (price, volume, trends)
⚠️ DISCLAIMER (standard financial disclaimer)

Focus on actionable insights for investors.""",
            AnalysisIntent.SUPPORT_RESISTANCE: """You are a technical analyst specializing in support and resistance levels.
Analyze key price levels where stocks find support (price floors) and resistance (price ceilings).
Always include ticker symbols, use financial emojis (📈 for bullish, 📉 for bearish), and structure responses with:
🎯 KEY TAKEAWAYS (bullet points)
📊 DETAILED ANALYSIS (support/resistance levels with explanations)
⚠️ DISCLAIMER (standard financial disclaimer)

Provide actionable trading insights based on technical analysis.""",
            AnalysisIntent.TECHNICAL: """You are a technical analyst specializing in comprehensive technical analysis.
Use key indicators like RSI, MACD, and moving averages to analyze momentum and trend direction.
Always include ticker symbols, use financial emojis (📈 for bullish, 📉 for bearish), and structure responses with:
🎯 KEY TAKEAWAYS (bullet points)
📊 DETAILED ANALYSIS (technical indicators and signals)
⚠️ DISCLAIMER (standard financial disclaimer)

Keep analysis concise but comprehensive, focusing on essential indicators.""",
            AnalysisIntent.GENERAL: """You are a financial assistant helping with general financial queries.
Provide helpful, informative responses about stocks, market data, financial analysis, and economic indicators.
Always include ticker symbols when relevant, use financial emojis (📈 for bullish, 📉 for bearish), and structure responses with:
🎯 KEY TAKEAWAYS (bullet points)
📊 DETAILED ANALYSIS (relevant financial information)
⚠️ DISCLAIMER (standard financial disclaimer)

Make responses educational and actionable for investors.""",
        }

    def _build_user_prompts(self) -> Dict[AnalysisIntent, str]:
        """Build user prompt templates for different analysis types"""
        return {
            AnalysisIntent.SNAPSHOT: """Provide a comprehensive stock snapshot analysis for: {message}

Include current market data, recent performance metrics, and clear explanations for investors.""",
            AnalysisIntent.SUPPORT_RESISTANCE: """Analyze key support and resistance levels for: {message}

Identify 3 support levels and 3 resistance levels with explanations of their significance for trading decisions.""",
            AnalysisIntent.TECHNICAL: """Provide comprehensive technical analysis for: {message}

Use key indicators including RSI, MACD, and moving averages. Explain momentum and trend direction with trading recommendations.""",
            AnalysisIntent.GENERAL: """Help with this financial query: {message}

Provide relevant analysis, data, and insights to help with this financial question.""",
        }
