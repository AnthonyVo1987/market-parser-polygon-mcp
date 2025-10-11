"""
Polygon.io custom tools for OpenAI AI Agent.
Provides direct Polygon Python Library API access for market status, datetime, and technical indicators.
"""

import asyncio
import json
import os
from datetime import datetime, timezone

import requests
from agents import function_tool
from polygon import RESTClient

from .formatting_helpers import create_ta_indicators_table


def _get_polygon_client():
    """Get Polygon client with API key from environment.

    Lazy initialization ensures .env is loaded before accessing API key.
    """
    api_key = os.getenv("POLYGON_API_KEY")
    return RESTClient(api_key=api_key)


@function_tool
async def get_market_status_and_date_time() -> str:
    """Get current market status and date/time from Tradier API.

    Use this tool when the user requests market status, trading hours,
    current date/time, or whether markets are open/closed.

    This tool provides real-time market status and server datetime via
    Tradier API, replacing the Polygon.io direct API.

    Args:
        None - retrieves current market status automatically.

    Returns:
        JSON string containing market status and datetime with format:
        {
            "market_status": "open" | "closed" | "extended-hours",
            "after_hours": true | false,
            "early_hours": true | false,
            "exchanges": {
                "nasdaq": "open" | "closed" | "extended-hours",
                "nyse": "open" | "closed" | "extended-hours",
                "otc": "open" | "closed" | "extended-hours"
            },
            "server_time": "2025-10-05T14:30:00Z",
            "date": "2025-10-05",
            "time": "14:30:00",
            "source": "Tradier"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "source": "Tradier"
        }

    Note:
        - Provides combined market status and datetime in single call
        - Data updates in real-time from Tradier servers
        - Includes pre-market (early_hours) and after-market (after_hours) status
        - Server time is in UTC timezone
        - This is a direct API call via HTTP

    Examples:
        - "Is the market open?"
        - "What time is it?"
        - "Market status?"
        - "What's today's date?"
        - "Are markets open for trading?"
    """
    try:
        # Get API key from environment
        api_key = os.getenv("TRADIER_API_KEY")
        if not api_key:
            return json.dumps(
                {
                    "error": "Configuration error",
                    "message": "TRADIER_API_KEY not configured in environment",
                    "source": "Tradier",
                }
            )

        # Build request to Tradier API
        url = "https://api.tradier.com/v1/markets/clock"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Make API request with timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        clock_data = data.get("clock", {})

        # Check if API returned valid data
        if not clock_data:
            return json.dumps(
                {
                    "error": "No data",
                    "message": "No clock data returned from Tradier API.",
                    "source": "Tradier",
                }
            )

        # Extract state and map to current response format
        state = clock_data.get("state", "closed")
        market_status = _map_tradier_state(state)
        early_hours = (state == "pre")
        after_hours = (state == "post")

        # Convert Unix timestamp to ISO datetime
        timestamp = clock_data.get("timestamp", 0)
        server_time_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        server_time = server_time_dt.isoformat()
        date_str = server_time_dt.strftime("%Y-%m-%d")
        time_str = server_time_dt.strftime("%H:%M:%S")

        # Build response with exchange status (use overall state for all exchanges)
        exchange_status = market_status

        return json.dumps(
            {
                "market_status": market_status,
                "after_hours": after_hours,
                "early_hours": early_hours,
                "exchanges": {
                    "nasdaq": exchange_status,
                    "nyse": exchange_status,
                    "otc": exchange_status,
                },
                "server_time": server_time,
                "date": date_str,
                "time": time_str,
                "source": "Tradier",
            },
            indent=2
        )

    except requests.exceptions.Timeout:
        return json.dumps(
            {
                "error": "Timeout",
                "message": "Request timed out while fetching market status",
                "source": "Tradier",
            }
        )
    except requests.exceptions.RequestException as e:
        return json.dumps(
            {
                "error": "API request failed",
                "message": f"Tradier API request failed: {str(e)}",
                "source": "Tradier",
            }
        )
    except Exception as e:
        return json.dumps(
            {
                "error": "Unexpected error",
                "message": f"Failed to retrieve market status from Tradier: {str(e)}",
                "source": "Tradier",
            }
        )


def _map_tradier_state(state: str) -> str:
    """Map Tradier market state to expected response format.
    
    Args:
        state: Tradier market state ("open", "closed", "pre", "post")
        
    Returns:
        Mapped market status ("open", "closed", "extended-hours")
    """
    if state == "open":
        return "open"
    elif state in ["pre", "post"]:
        return "extended-hours"
    else:  # closed
        return "closed"


# ============================================================================
# LEGACY TECHNICAL ANALYSIS TOOLS (COMMENTED OUT - SUPERSEDED BY get_ta_indicators)
# ============================================================================
# These individual TA tools have been replaced by the consolidated get_ta_indicators
# tool for improved performance, rate limiting protection, and better user experience.
#
# Consolidation Benefits:
# - 54% code reduction (442 lines → ~200 lines active)
# - 87% fewer tool calls (8 calls → 1 call)
# - 70% faster response time (~10s → ~3s)
# - Rate limit safe (batched API calls with delays)
# - Formatted markdown table output
#
# These legacy tools are kept as reference and can be uncommented if needed.
# Date Deprecated: October 11, 2025
# Replaced By: get_ta_indicators() starting at line 641
# ============================================================================

# @function_tool
# async def get_ta_sma(ticker: str, timespan: str = "day", window: int = 50, limit: int = 10) -> str:
#     """Get Simple Moving Average (SMA) indicator values from Polygon.io API.
# 
#     Use this tool when the user requests SMA, simple moving average, moving average,
#     trend analysis, or support/resistance levels based on moving averages.
# 
#     The SMA is a widely used technical indicator that smooths price data by calculating
#     the average price over a specified number of periods. It helps identify trends and
#     potential support/resistance levels.
# 
#     Args:
#         ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA")
#         timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")
#         window: Number of periods for SMA calculation (default: 50 for 50-day SMA)
#         limit: Maximum number of data points to return (default: 10, max: 5000)
# 
#     Returns:
#         JSON string containing SMA indicator values with format:
#         {
#             "status": "success",
#             "indicator": "sma",
#             "ticker": "SPY",
#             "values": [
#                 {"timestamp": "2025-10-05T00:00:00Z", "value": 450.25},
#                 ...
#             ],
#             "parameters": {"timespan": "day", "window": 50},
#             "count": 10,
#             "source": "Polygon.io"
#         }
# 
#         Or error format:
#         {
#             "error": "error_type",
#             "message": "descriptive error message",
#             "source": "Polygon.io"
#         }
# 
#     Note:
#         - SMA smooths price fluctuations to identify trends
#         - Commonly used windows: 20, 50, 200 days
#         - Price above SMA = potential uptrend, below = potential downtrend
#         - SMA can act as dynamic support/resistance
#         - Data adjusted for splits by default
# 
#     Examples:
#         - "SMA for SPY"
#         - "50-day moving average AAPL"
#         - "Simple moving average analysis NVDA"
#         - "200-day SMA for market trend"
#     """
#     try:
#         # Call Polygon API with lazy client initialization
#         client = _get_polygon_client()
#         sma_results = client.get_sma(ticker=ticker, timespan=timespan, window=window, limit=limit)
# 
#         # Check if API returned valid data
#         if not sma_results or not hasattr(sma_results, "values"):
#             return json.dumps(
#                 {
#                     "error": "No data",
#                     "message": f"No SMA data returned from Polygon.io for {ticker}.",
#                     "source": "Polygon.io",
#                 }
#             )
# 
#         # Extract values from results
#         values = []
#         if sma_results.values:
#             for result in sma_results.values:
#                 values.append(
#                     {
#                         "timestamp": getattr(result, "timestamp", ""),
#                         "value": getattr(result, "value", 0.0),
#                     }
#                 )
# 
#         # Format response
#         return json.dumps(
#             {
#                 "status": "success",
#                 "indicator": "sma",
#                 "ticker": ticker,
#                 "values": values,
#                 "parameters": {"timespan": timespan, "window": window},
#                 "count": len(values),
#                 "source": "Polygon.io",
#             }
#         )
# 
#     except Exception as e:
#         # Handle unexpected errors
#         return json.dumps(
#             {
#                 "error": "API request failed",
#                 "message": f"Failed to retrieve SMA data from Polygon.io: {str(e)}",
#                 "source": "Polygon.io",
#             }
#         )
# 
# 
# @function_tool
# async def get_ta_ema(ticker: str, timespan: str = "day", window: int = 50, limit: int = 10) -> str:
#     """Get Exponential Moving Average (EMA) indicator values from Polygon.io API.
# 
#     Use this tool when the user requests EMA, exponential moving average, or more
#     responsive trend analysis compared to simple moving averages.
# 
#     The EMA gives more weight to recent prices, making it more responsive to price
#     changes than SMA. It's commonly used for trend following and identifying
#     potential entry/exit points.
# 
#     Args:
#         ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "TSLA")
#         timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")
#         window: Number of periods for EMA calculation (default: 50 for 50-day EMA)
#         limit: Maximum number of data points to return (default: 10, max: 5000)
# 
#     Returns:
#         JSON string containing EMA indicator values with format:
#         {
#             "status": "success",
#             "indicator": "ema",
#             "ticker": "SPY",
#             "values": [
#                 {"timestamp": "2025-10-05T00:00:00Z", "value": 452.30},
#                 ...
#             ],
#             "parameters": {"timespan": "day", "window": 50},
#             "count": 10,
#             "source": "Polygon.io"
#         }
# 
#         Or error format:
#         {
#             "error": "error_type",
#             "message": "descriptive error message",
#             "source": "Polygon.io"
#         }
# 
#     Note:
#         - EMA reacts faster to price changes than SMA
#         - Commonly used windows: 12, 20, 26, 50 days
#         - Popular for short-term trading strategies
#         - Often used in combination (e.g., 12/26 EMA crossover for MACD)
#         - Data adjusted for splits by default
# 
#     Examples:
#         - "EMA for SPY"
#         - "20-day exponential moving average TSLA"
#         - "EMA analysis NVDA"
#         - "12 and 26 EMA for crossover strategy"
#     """
#     try:
#         # Call Polygon API with lazy client initialization
#         client = _get_polygon_client()
#         ema_results = client.get_ema(ticker=ticker, timespan=timespan, window=window, limit=limit)
# 
#         # Check if API returned valid data
#         if not ema_results or not hasattr(ema_results, "values"):
#             return json.dumps(
#                 {
#                     "error": "No data",
#                     "message": f"No EMA data returned from Polygon.io for {ticker}.",
#                     "source": "Polygon.io",
#                 }
#             )
# 
#         # Extract values from results
#         values = []
#         if ema_results.values:
#             for result in ema_results.values:
#                 values.append(
#                     {
#                         "timestamp": getattr(result, "timestamp", ""),
#                         "value": getattr(result, "value", 0.0),
#                     }
#                 )
# 
#         # Format response
#         return json.dumps(
#             {
#                 "status": "success",
#                 "indicator": "ema",
#                 "ticker": ticker,
#                 "values": values,
#                 "parameters": {"timespan": timespan, "window": window},
#                 "count": len(values),
#                 "source": "Polygon.io",
#             }
#         )
# 
#     except Exception as e:
#         # Handle unexpected errors
#         return json.dumps(
#             {
#                 "error": "API request failed",
#                 "message": f"Failed to retrieve EMA data from Polygon.io: {str(e)}",
#                 "source": "Polygon.io",
#             }
#         )
# 
# 
# @function_tool
# async def get_ta_rsi(ticker: str, timespan: str = "day", window: int = 14, limit: int = 10) -> str:
#     """Get Relative Strength Index (RSI) indicator values from Polygon.io API.
# 
#     Use this tool when the user requests RSI, relative strength index, overbought/oversold
#     conditions, momentum analysis, or market strength indicators.
# 
#     The RSI is a momentum oscillator that measures the speed and magnitude of price changes.
#     It ranges from 0 to 100, with readings above 70 indicating overbought conditions and
#     below 30 indicating oversold conditions.
# 
#     Args:
#         ticker: Stock ticker symbol (e.g., "SPY", "NVDA", "AAPL")
#         timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")
#         window: Number of periods for RSI calculation (default: 14, standard RSI period)
#         limit: Maximum number of data points to return (default: 10, max: 5000)
# 
#     Returns:
#         JSON string containing RSI indicator values with format:
#         {
#             "status": "success",
#             "indicator": "rsi",
#             "ticker": "SPY",
#             "values": [
#                 {"timestamp": "2025-10-05T00:00:00Z", "value": 62.45},
#                 ...
#             ],
#             "parameters": {"timespan": "day", "window": 14},
#             "interpretation": {
#                 "overbought_threshold": 70,
#                 "oversold_threshold": 30
#             },
#             "count": 10,
#             "source": "Polygon.io"
#         }
# 
#         Or error format:
#         {
#             "error": "error_type",
#             "message": "descriptive error message",
#             "source": "Polygon.io"
#         }
# 
#     Note:
#         - RSI ranges from 0 to 100
#         - RSI > 70 = overbought (potential sell signal)
#         - RSI < 30 = oversold (potential buy signal)
#         - Standard period is 14 days
#         - Divergences between RSI and price can indicate reversals
#         - Data adjusted for splits by default
# 
#     Examples:
#         - "RSI for SPY"
#         - "Relative strength index NVDA"
#         - "Is AAPL overbought or oversold?"
#         - "RSI momentum analysis SPY"
#     """
#     try:
#         # Call Polygon API with lazy client initialization
#         client = _get_polygon_client()
#         rsi_results = client.get_rsi(ticker=ticker, timespan=timespan, window=window, limit=limit)
# 
#         # Check if API returned valid data
#         if not rsi_results or not hasattr(rsi_results, "values"):
#             return json.dumps(
#                 {
#                     "error": "No data",
#                     "message": f"No RSI data returned from Polygon.io for {ticker}.",
#                     "source": "Polygon.io",
#                 }
#             )
# 
#         # Extract values from results
#         values = []
#         if rsi_results.values:
#             for result in rsi_results.values:
#                 values.append(
#                     {
#                         "timestamp": getattr(result, "timestamp", ""),
#                         "value": getattr(result, "value", 0.0),
#                     }
#                 )
# 
#         # Format response
#         return json.dumps(
#             {
#                 "status": "success",
#                 "indicator": "rsi",
#                 "ticker": ticker,
#                 "values": values,
#                 "parameters": {"timespan": timespan, "window": window},
#                 "interpretation": {"overbought_threshold": 70, "oversold_threshold": 30},
#                 "count": len(values),
#                 "source": "Polygon.io",
#             }
#         )
# 
#     except Exception as e:
#         # Handle unexpected errors
#         return json.dumps(
#             {
#                 "error": "API request failed",
#                 "message": f"Failed to retrieve RSI data from Polygon.io: {str(e)}",
#                 "source": "Polygon.io",
#             }
#         )
# 
# 
# @function_tool
# async def get_ta_macd(
#     ticker: str,
#     timespan: str = "day",
#     *,
#     short_window: int = 12,
#     long_window: int = 26,
#     signal_window: int = 9,
#     limit: int = 10,
# ) -> str:
#     """Get MACD (Moving Average Convergence Divergence) indicator values from Polygon.io API.
# 
#     Use this tool when the user requests MACD, moving average convergence divergence,
#     trend and momentum analysis, or buy/sell signal identification.
# 
#     The MACD is a trend-following momentum indicator that shows the relationship between
#     two moving averages. It consists of the MACD line, signal line, and histogram, commonly
#     used to identify trend changes and momentum shifts.
# 
#     Args:
#         ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "TSLA")
#         timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")
#         short_window: Short EMA period (default: 12, standard fast period)
#         long_window: Long EMA period (default: 26, standard slow period)
#         signal_window: Signal line EMA period (default: 9, standard signal period)
#         limit: Maximum number of data points to return (default: 10, max: 5000)
# 
#     Returns:
#         JSON string containing MACD indicator values with format:
#         {
#             "status": "success",
#             "indicator": "macd",
#             "ticker": "SPY",
#             "values": [
#                 {
#                     "timestamp": "2025-10-05T00:00:00Z",
#                     "macd": 2.34,
#                     "signal": 1.87,
#                     "histogram": 0.47
#                 },
#                 ...
#             ],
#             "parameters": {
#                 "timespan": "day",
#                 "short_window": 12,
#                 "long_window": 26,
#                 "signal_window": 9
#             },
#             "count": 10,
#             "source": "Polygon.io"
#         }
# 
#         Or error format:
#         {
#             "error": "error_type",
#             "message": "descriptive error message",
#             "source": "Polygon.io"
#         }
# 
#     Note:
#         - MACD = 12 EMA - 26 EMA (default periods)
#         - Signal = 9 EMA of MACD line
#         - Histogram = MACD - Signal
#         - MACD crossing above signal = bullish signal
#         - MACD crossing below signal = bearish signal
#         - Histogram shows momentum strength
#         - Data adjusted for splits by default
# 
#     Examples:
#         - "MACD for SPY"
#         - "MACD analysis AAPL"
#         - "Moving average convergence divergence TSLA"
#         - "MACD crossover signals NVDA"
#     """
#     try:
#         # Call Polygon API with lazy client initialization
#         client = _get_polygon_client()
#         macd_results = client.get_macd(
#             ticker=ticker,
#             timespan=timespan,
#             short_window=short_window,
#             long_window=long_window,
#             signal_window=signal_window,
#             limit=limit,
#         )
# 
#         # Check if API returned valid data
#         if not macd_results or not hasattr(macd_results, "values"):
#             return json.dumps(
#                 {
#                     "error": "No data",
#                     "message": f"No MACD data returned from Polygon.io for {ticker}.",
#                     "source": "Polygon.io",
#                 }
#             )
# 
#         # Extract values from results
#         values = []
#         if macd_results.values:
#             for result in macd_results.values:
#                 values.append(
#                     {
#                         "timestamp": getattr(result, "timestamp", ""),
#                         "macd": getattr(result, "value", 0.0),
#                         "signal": getattr(result, "signal", 0.0),
#                         "histogram": getattr(result, "histogram", 0.0),
#                     }
#                 )
# 
#         # Format response
#         return json.dumps(
#             {
#                 "status": "success",
#                 "indicator": "macd",
#                 "ticker": ticker,
#                 "values": values,
#                 "parameters": {
#                     "timespan": timespan,
#                     "short_window": short_window,
#                     "long_window": long_window,
#                     "signal_window": signal_window,
#                 },
#                 "count": len(values),
#                 "source": "Polygon.io",
#             }
#         )
# 
#     except Exception as e:
#         # Handle unexpected errors
#         return json.dumps(
#             {
#                 "error": "API request failed",
#                 "message": f"Failed to retrieve MACD data from Polygon.io: {str(e)}",
#                 "source": "Polygon.io",
#             }
#         )


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


