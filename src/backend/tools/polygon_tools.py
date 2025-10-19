"""
Polygon.io custom tools for OpenAI AI Agent.
Provides direct Polygon Python Library API access for market status, datetime, and technical indicators.
"""

import asyncio
import json
import os
import time
from datetime import datetime, timezone

import requests
from agents import function_tool
from polygon import RESTClient

from .error_utils import create_error_response
from .formatting_helpers import create_ta_indicators_table


def _get_polygon_client():
    """Get Polygon client with API key from environment.

    Lazy initialization ensures .env is loaded before accessing API key.
    """
    api_key = os.getenv("POLYGON_API_KEY")
    return RESTClient(api_key=api_key)


async def _get_ta_indicators(ticker: str, timespan: str = "day") -> str:
    """Get comprehensive technical analysis indicators in a single call.

    This consolidated tool retrieves ALL TA indicators with optimized batched API calls
    and returns a formatted markdown table. Replaces individual get_ta_sma, get_ta_ema,
    get_ta_rsi, and get_ta_macd tools.

    Indicators Retrieved:
    - RSI-14 (Relative Strength Index)
    - MACD (12/26/9) with signal line and histogram
    - SMA (Simple Moving Averages): 5, 10, 20, 50, 200-period
    - EMA (Exponential Moving Averages): 5, 10, 20, 50, 200-period

    Performance Optimization:
    - Batched API calls with rate limit protection
    - Batch 1: RSI + MACD (2 parallel calls)
    - Batch 2: SMA 5/10/20/50/200 (5 parallel calls)
    - Batch 3: EMA 5/10/20/50/200 (5 parallel calls)
    - 1-second delays between batches prevent rate limiting
    - Total: 12 API calls in ~2-3 seconds
    - Requests limit=10 per indicator to ensure LAST AVAILABLE data (even on weekends/holidays)

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA")
        timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")

    Returns:
        Formatted markdown table string with all 14 indicators or error message

    Example Output:
        📊 Technical Analysis Indicators - SPY
        Current Date: 2025-10-11

        | Indicator | Period | Value | Timestamp |
        |-----------|--------|-------|-----------|
        | RSI       | 14     | 62.45 | 2025-10-11 |
        | MACD      | 12/26  | 2.34  | 2025-10-11 |
        | Signal    | 9      | 1.87  | 2025-10-11 |
        | Histogram | -      | 0.47  | 2025-10-11 |
        | SMA       | 5      | 654.23 | 2025-10-11 |
        ...

        Source: Polygon.io API

    Note:
        - ALWAYS returns last available data (even on weekends/holidays/market closures)
        - Uses limit=10 to fetch recent historical data, returns most recent value
        - Gracefully handles partial failures (displays N/A only if indicator genuinely unavailable)
        - Single tool call from agent perspective (all complexity in Python)
        - Rate limit safe with batched calls and delays
        - Formatted output ready for display

    Examples:
        - "Get technical analysis indicators for SPY"
        - "Show me TA indicators for NVDA"
        - "Technical analysis data for AAPL"
    """
    try:
        # Sanitize ticker - remove any invalid characters that might have been added
        ticker = str(ticker).strip().strip("'}?").strip('"').strip("'").upper()

        # Sanitize timespan - default to 'day' if empty or invalid
        timespan = str(timespan).strip() if timespan else "day"
        if not timespan or timespan in ["", "None", "null"]:
            timespan = "day"

        client = _get_polygon_client()

        # Batch 1: Momentum indicators (RSI + MACD)
        # Use limit=10 to ensure we get the most recent available data even on weekends/holidays
        try:
            batch1_results = await asyncio.gather(
                asyncio.to_thread(client.get_rsi, ticker=ticker, timespan=timespan, window=14, limit=10),
                asyncio.to_thread(
                    client.get_macd,
                    ticker=ticker,
                    timespan=timespan,
                    short_window=12,
                    long_window=26,
                    signal_window=9,
                    limit=10
                ),
                return_exceptions=True
            )
            rsi_result, macd_result = batch1_results
        except Exception as e:
            rsi_result = e
            macd_result = e

        # Rate limit protection
        await asyncio.sleep(1)

        # Batch 2: Simple Moving Averages (5, 10, 20, 50, 200)
        # Use limit=10 to ensure we get the most recent available data even on weekends/holidays
        try:
            batch2_results = await asyncio.gather(
                asyncio.to_thread(client.get_sma, ticker=ticker, timespan=timespan, window=5, limit=10),
                asyncio.to_thread(client.get_sma, ticker=ticker, timespan=timespan, window=10, limit=10),
                asyncio.to_thread(client.get_sma, ticker=ticker, timespan=timespan, window=20, limit=10),
                asyncio.to_thread(client.get_sma, ticker=ticker, timespan=timespan, window=50, limit=10),
                asyncio.to_thread(client.get_sma, ticker=ticker, timespan=timespan, window=200, limit=10),
                return_exceptions=True
            )
            sma_5, sma_10, sma_20, sma_50, sma_200 = batch2_results
        except Exception as e:
            sma_5 = sma_10 = sma_20 = sma_50 = sma_200 = e

        # Rate limit protection
        await asyncio.sleep(1)

        # Batch 3: Exponential Moving Averages (5, 10, 20, 50, 200)
        # Use limit=10 to ensure we get the most recent available data even on weekends/holidays
        try:
            batch3_results = await asyncio.gather(
                asyncio.to_thread(client.get_ema, ticker=ticker, timespan=timespan, window=5, limit=10),
                asyncio.to_thread(client.get_ema, ticker=ticker, timespan=timespan, window=10, limit=10),
                asyncio.to_thread(client.get_ema, ticker=ticker, timespan=timespan, window=20, limit=10),
                asyncio.to_thread(client.get_ema, ticker=ticker, timespan=timespan, window=50, limit=10),
                asyncio.to_thread(client.get_ema, ticker=ticker, timespan=timespan, window=200, limit=10),
                return_exceptions=True
            )
            ema_5, ema_10, ema_20, ema_50, ema_200 = batch3_results
        except Exception as e:
            ema_5 = ema_10 = ema_20 = ema_50 = ema_200 = e

        # Process RSI result
        rsi_data = None
        if not isinstance(rsi_result, Exception) and rsi_result and hasattr(rsi_result, "values") and rsi_result.values:
            result = rsi_result.values[0]
            rsi_data = {
                "value": getattr(result, "value", None),
                "timestamp": getattr(result, "timestamp", "N/A")
            }

        # Process MACD result
        macd_data = None
        if not isinstance(macd_result, Exception) and macd_result and hasattr(macd_result, "values") and macd_result.values:
            result = macd_result.values[0]
            macd_data = {
                "macd": getattr(result, "value", None),
                "signal": getattr(result, "signal", None),
                "histogram": getattr(result, "histogram", None),
                "timestamp": getattr(result, "timestamp", "N/A")
            }

        # Process SMA results
        sma_values = []
        for window, sma_result in [(5, sma_5), (10, sma_10), (20, sma_20), (50, sma_50), (200, sma_200)]:
            if not isinstance(sma_result, Exception) and sma_result and hasattr(sma_result, "values") and sma_result.values:
                result = sma_result.values[0]
                sma_values.append({
                    "window": window,
                    "value": getattr(result, "value", None),
                    "timestamp": getattr(result, "timestamp", "N/A")
                })

        # Process EMA results
        ema_values = []
        for window, ema_result in [(5, ema_5), (10, ema_10), (20, ema_20), (50, ema_50), (200, ema_200)]:
            if not isinstance(ema_result, Exception) and ema_result and hasattr(ema_result, "values") and ema_result.values:
                result = ema_result.values[0]
                ema_values.append({
                    "window": window,
                    "value": getattr(result, "value", None),
                    "timestamp": getattr(result, "timestamp", "N/A")
                })

        # Build indicators dict for formatter
        indicators = {
            "rsi": rsi_data,
            "macd": macd_data,
            "sma_values": sma_values,
            "ema_values": ema_values
        }

        # Return formatted markdown table
        return create_ta_indicators_table(ticker, indicators)

    except Exception as e:
        return f"❌ Error retrieving technical analysis indicators for {ticker}: {str(e)}\n\nSource: Polygon.io API"


@function_tool
async def get_ta_indicators(ticker: str, timespan: str = "day") -> str:
    """Get comprehensive technical analysis indicators in a single call.

    This consolidated tool retrieves ALL TA indicators with optimized batched API calls
    and returns a formatted markdown table. Replaces individual get_ta_sma, get_ta_ema,
    get_ta_rsi, and get_ta_macd tools.

    Indicators Retrieved:
    - RSI-14 (Relative Strength Index)
    - MACD (12/26/9) with signal line and histogram
    - SMA (Simple Moving Averages): 5, 10, 20, 50, 200-period
    - EMA (Exponential Moving Averages): 5, 10, 20, 50, 200-period

    Performance Optimization:
    - Batched API calls with rate limit protection
    - Batch 1: RSI + MACD (2 parallel calls)
    - Batch 2: SMA 5/10/20/50/200 (5 parallel calls)
    - Batch 3: EMA 5/10/20/50/200 (5 parallel calls)
    - 1-second delays between batches prevent rate limiting
    - Total: 12 API calls in ~2-3 seconds
    - Requests limit=10 per indicator to ensure LAST AVAILABLE data (even on weekends/holidays)

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA")
        timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")

    Returns:
        Formatted markdown table string with all 14 indicators or error message

    Example Output:
        📊 Technical Analysis Indicators - SPY
        Current Date: 2025-10-11

        | Indicator | Period | Value | Timestamp |
        |-----------|--------|-------|-----------|
        | RSI       | 14     | 62.45 | 2025-10-11 |
        | MACD      | 12/26  | 2.34  | 2025-10-11 |
        | Signal    | 9      | 1.87  | 2025-10-11 |
        | Histogram | -      | 0.47  | 2025-10-11 |
        | SMA       | 5      | 654.23 | 2025-10-11 |
        ...

        Source: Polygon.io API

    Note:
        - ALWAYS returns last available data (even on weekends/holidays/market closures)
        - Uses limit=10 to fetch recent historical data, returns most recent value
        - Gracefully handles partial failures (displays N/A only if indicator genuinely unavailable)
        - Single tool call from agent perspective (all complexity in Python)
        - Rate limit safe with batched calls and delays
        - Formatted output ready for display

    Examples:
        - "Get technical analysis indicators for SPY"
        - "Show me TA indicators for NVDA"
        - "Technical analysis data for AAPL"
    """
    return await _get_ta_indicators(ticker, timespan)


