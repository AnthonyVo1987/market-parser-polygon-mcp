"""
Polygon.io custom tools for OpenAI AI Agent.
Provides direct Polygon Python Library API access for market status, datetime, and technical indicators.
"""

import json
import os
from datetime import datetime

from agents import function_tool
from polygon import RESTClient


def _get_polygon_client():
    """Get Polygon client with API key from environment.

    Lazy initialization ensures .env is loaded before accessing API key.
    """
    api_key = os.getenv("POLYGON_API_KEY")
    return RESTClient(api_key=api_key)


@function_tool
async def get_market_status_and_date_time() -> str:
    """Get current market status and date/time from Polygon.io API.

    Use this tool when the user requests market status, trading hours,
    current date/time, or whether markets are open/closed.

    This tool provides real-time market status and server datetime via
    Polygon.io direct API, replacing the MCP-based get_market_status tool.

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
            "source": "Polygon.io"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "source": "Polygon.io"
        }

    Note:
        - Provides combined market status and datetime in single call
        - Data updates in real-time from Polygon.io servers
        - Includes pre-market (early_hours) and after-market (after_hours) status
        - Server time is in UTC timezone
        - This is a direct API call (not using MCP server)

    Examples:
        - "Is the market open?"
        - "What time is it?"
        - "Market status?"
        - "What's today's date?"
        - "Are markets open for trading?"
    """
    try:
        # Call Polygon API with lazy client initialization
        client = _get_polygon_client()
        market_status = client.get_market_status()

        # Check if API returned valid data
        if not market_status:
            return json.dumps(
                {
                    "error": "No data",
                    "message": "No market status data returned from Polygon.io API.",
                    "source": "Polygon.io",
                }
            )

        # Extract server time and parse for date/time components
        server_time = market_status.server_time or ""
        date_str = ""
        time_str = ""

        if server_time:
            try:
                # Parse ISO timestamp to extract date and time
                dt = datetime.fromisoformat(server_time.replace("Z", "+00:00"))
                date_str = dt.strftime("%Y-%m-%d")
                time_str = dt.strftime("%H:%M:%S")
            except (ValueError, AttributeError):
                # If parsing fails, use original string
                date_str = server_time.split("T")[0] if "T" in server_time else ""
                time_str = server_time.split("T")[1].replace("Z", "") if "T" in server_time else ""

        # Extract exchange statuses safely
        exchanges_data = {}
        if market_status.exchanges:
            exchanges_data = {
                "nasdaq": market_status.exchanges.nasdaq or "unknown",
                "nyse": market_status.exchanges.nyse or "unknown",
                "otc": market_status.exchanges.otc or "unknown",
            }

        # Format response
        return json.dumps(
            {
                "market_status": market_status.market or "unknown",
                "after_hours": market_status.after_hours or False,
                "early_hours": market_status.early_hours or False,
                "exchanges": exchanges_data,
                "server_time": server_time,
                "date": date_str,
                "time": time_str,
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        # Handle unexpected errors
        return json.dumps(
            {
                "error": "API request failed",
                "message": f"Failed to retrieve market status from Polygon.io: {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_ta_sma(ticker: str, timespan: str = "day", window: int = 50, limit: int = 10) -> str:
    """Get Simple Moving Average (SMA) indicator values from Polygon.io API.

    Use this tool when the user requests SMA, simple moving average, moving average,
    trend analysis, or support/resistance levels based on moving averages.

    The SMA is a widely used technical indicator that smooths price data by calculating
    the average price over a specified number of periods. It helps identify trends and
    potential support/resistance levels.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA")
        timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")
        window: Number of periods for SMA calculation (default: 50 for 50-day SMA)
        limit: Maximum number of data points to return (default: 10, max: 5000)

    Returns:
        JSON string containing SMA indicator values with format:
        {
            "status": "success",
            "indicator": "sma",
            "ticker": "SPY",
            "values": [
                {"timestamp": "2025-10-05T00:00:00Z", "value": 450.25},
                ...
            ],
            "parameters": {"timespan": "day", "window": 50},
            "count": 10,
            "source": "Polygon.io"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "source": "Polygon.io"
        }

    Note:
        - SMA smooths price fluctuations to identify trends
        - Commonly used windows: 20, 50, 200 days
        - Price above SMA = potential uptrend, below = potential downtrend
        - SMA can act as dynamic support/resistance
        - Data adjusted for splits by default

    Examples:
        - "SMA for SPY"
        - "50-day moving average AAPL"
        - "Simple moving average analysis NVDA"
        - "200-day SMA for market trend"
    """
    try:
        # Call Polygon API with lazy client initialization
        client = _get_polygon_client()
        sma_results = client.get_sma(ticker=ticker, timespan=timespan, window=window, limit=limit)

        # Check if API returned valid data
        if not sma_results or not hasattr(sma_results, "values"):
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No SMA data returned from Polygon.io for {ticker}.",
                    "source": "Polygon.io",
                }
            )

        # Extract values from results
        values = []
        if sma_results.values:
            for result in sma_results.values:
                values.append(
                    {
                        "timestamp": getattr(result, "timestamp", ""),
                        "value": getattr(result, "value", 0.0),
                    }
                )

        # Format response
        return json.dumps(
            {
                "status": "success",
                "indicator": "sma",
                "ticker": ticker,
                "values": values,
                "parameters": {"timespan": timespan, "window": window},
                "count": len(values),
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        # Handle unexpected errors
        return json.dumps(
            {
                "error": "API request failed",
                "message": f"Failed to retrieve SMA data from Polygon.io: {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_ta_ema(ticker: str, timespan: str = "day", window: int = 50, limit: int = 10) -> str:
    """Get Exponential Moving Average (EMA) indicator values from Polygon.io API.

    Use this tool when the user requests EMA, exponential moving average, or more
    responsive trend analysis compared to simple moving averages.

    The EMA gives more weight to recent prices, making it more responsive to price
    changes than SMA. It's commonly used for trend following and identifying
    potential entry/exit points.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "TSLA")
        timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")
        window: Number of periods for EMA calculation (default: 50 for 50-day EMA)
        limit: Maximum number of data points to return (default: 10, max: 5000)

    Returns:
        JSON string containing EMA indicator values with format:
        {
            "status": "success",
            "indicator": "ema",
            "ticker": "SPY",
            "values": [
                {"timestamp": "2025-10-05T00:00:00Z", "value": 452.30},
                ...
            ],
            "parameters": {"timespan": "day", "window": 50},
            "count": 10,
            "source": "Polygon.io"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "source": "Polygon.io"
        }

    Note:
        - EMA reacts faster to price changes than SMA
        - Commonly used windows: 12, 20, 26, 50 days
        - Popular for short-term trading strategies
        - Often used in combination (e.g., 12/26 EMA crossover for MACD)
        - Data adjusted for splits by default

    Examples:
        - "EMA for SPY"
        - "20-day exponential moving average TSLA"
        - "EMA analysis NVDA"
        - "12 and 26 EMA for crossover strategy"
    """
    try:
        # Call Polygon API with lazy client initialization
        client = _get_polygon_client()
        ema_results = client.get_ema(ticker=ticker, timespan=timespan, window=window, limit=limit)

        # Check if API returned valid data
        if not ema_results or not hasattr(ema_results, "values"):
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No EMA data returned from Polygon.io for {ticker}.",
                    "source": "Polygon.io",
                }
            )

        # Extract values from results
        values = []
        if ema_results.values:
            for result in ema_results.values:
                values.append(
                    {
                        "timestamp": getattr(result, "timestamp", ""),
                        "value": getattr(result, "value", 0.0),
                    }
                )

        # Format response
        return json.dumps(
            {
                "status": "success",
                "indicator": "ema",
                "ticker": ticker,
                "values": values,
                "parameters": {"timespan": timespan, "window": window},
                "count": len(values),
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        # Handle unexpected errors
        return json.dumps(
            {
                "error": "API request failed",
                "message": f"Failed to retrieve EMA data from Polygon.io: {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_ta_rsi(ticker: str, timespan: str = "day", window: int = 14, limit: int = 10) -> str:
    """Get Relative Strength Index (RSI) indicator values from Polygon.io API.

    Use this tool when the user requests RSI, relative strength index, overbought/oversold
    conditions, momentum analysis, or market strength indicators.

    The RSI is a momentum oscillator that measures the speed and magnitude of price changes.
    It ranges from 0 to 100, with readings above 70 indicating overbought conditions and
    below 30 indicating oversold conditions.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "NVDA", "AAPL")
        timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")
        window: Number of periods for RSI calculation (default: 14, standard RSI period)
        limit: Maximum number of data points to return (default: 10, max: 5000)

    Returns:
        JSON string containing RSI indicator values with format:
        {
            "status": "success",
            "indicator": "rsi",
            "ticker": "SPY",
            "values": [
                {"timestamp": "2025-10-05T00:00:00Z", "value": 62.45},
                ...
            ],
            "parameters": {"timespan": "day", "window": 14},
            "interpretation": {
                "overbought_threshold": 70,
                "oversold_threshold": 30
            },
            "count": 10,
            "source": "Polygon.io"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "source": "Polygon.io"
        }

    Note:
        - RSI ranges from 0 to 100
        - RSI > 70 = overbought (potential sell signal)
        - RSI < 30 = oversold (potential buy signal)
        - Standard period is 14 days
        - Divergences between RSI and price can indicate reversals
        - Data adjusted for splits by default

    Examples:
        - "RSI for SPY"
        - "Relative strength index NVDA"
        - "Is AAPL overbought or oversold?"
        - "RSI momentum analysis SPY"
    """
    try:
        # Call Polygon API with lazy client initialization
        client = _get_polygon_client()
        rsi_results = client.get_rsi(ticker=ticker, timespan=timespan, window=window, limit=limit)

        # Check if API returned valid data
        if not rsi_results or not hasattr(rsi_results, "values"):
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No RSI data returned from Polygon.io for {ticker}.",
                    "source": "Polygon.io",
                }
            )

        # Extract values from results
        values = []
        if rsi_results.values:
            for result in rsi_results.values:
                values.append(
                    {
                        "timestamp": getattr(result, "timestamp", ""),
                        "value": getattr(result, "value", 0.0),
                    }
                )

        # Format response
        return json.dumps(
            {
                "status": "success",
                "indicator": "rsi",
                "ticker": ticker,
                "values": values,
                "parameters": {"timespan": timespan, "window": window},
                "interpretation": {"overbought_threshold": 70, "oversold_threshold": 30},
                "count": len(values),
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        # Handle unexpected errors
        return json.dumps(
            {
                "error": "API request failed",
                "message": f"Failed to retrieve RSI data from Polygon.io: {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_ta_macd(
    ticker: str,
    timespan: str = "day",
    *,
    short_window: int = 12,
    long_window: int = 26,
    signal_window: int = 9,
    limit: int = 10,
) -> str:
    """Get MACD (Moving Average Convergence Divergence) indicator values from Polygon.io API.

    Use this tool when the user requests MACD, moving average convergence divergence,
    trend and momentum analysis, or buy/sell signal identification.

    The MACD is a trend-following momentum indicator that shows the relationship between
    two moving averages. It consists of the MACD line, signal line, and histogram, commonly
    used to identify trend changes and momentum shifts.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "TSLA")
        timespan: Aggregate time window - "day", "minute", "hour", "week", "month" (default: "day")
        short_window: Short EMA period (default: 12, standard fast period)
        long_window: Long EMA period (default: 26, standard slow period)
        signal_window: Signal line EMA period (default: 9, standard signal period)
        limit: Maximum number of data points to return (default: 10, max: 5000)

    Returns:
        JSON string containing MACD indicator values with format:
        {
            "status": "success",
            "indicator": "macd",
            "ticker": "SPY",
            "values": [
                {
                    "timestamp": "2025-10-05T00:00:00Z",
                    "macd": 2.34,
                    "signal": 1.87,
                    "histogram": 0.47
                },
                ...
            ],
            "parameters": {
                "timespan": "day",
                "short_window": 12,
                "long_window": 26,
                "signal_window": 9
            },
            "count": 10,
            "source": "Polygon.io"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "source": "Polygon.io"
        }

    Note:
        - MACD = 12 EMA - 26 EMA (default periods)
        - Signal = 9 EMA of MACD line
        - Histogram = MACD - Signal
        - MACD crossing above signal = bullish signal
        - MACD crossing below signal = bearish signal
        - Histogram shows momentum strength
        - Data adjusted for splits by default

    Examples:
        - "MACD for SPY"
        - "MACD analysis AAPL"
        - "Moving average convergence divergence TSLA"
        - "MACD crossover signals NVDA"
    """
    try:
        # Call Polygon API with lazy client initialization
        client = _get_polygon_client()
        macd_results = client.get_macd(
            ticker=ticker,
            timespan=timespan,
            short_window=short_window,
            long_window=long_window,
            signal_window=signal_window,
            limit=limit,
        )

        # Check if API returned valid data
        if not macd_results or not hasattr(macd_results, "values"):
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No MACD data returned from Polygon.io for {ticker}.",
                    "source": "Polygon.io",
                }
            )

        # Extract values from results
        values = []
        if macd_results.values:
            for result in macd_results.values:
                values.append(
                    {
                        "timestamp": getattr(result, "timestamp", ""),
                        "macd": getattr(result, "value", 0.0),
                        "signal": getattr(result, "signal", 0.0),
                        "histogram": getattr(result, "histogram", 0.0),
                    }
                )

        # Format response
        return json.dumps(
            {
                "status": "success",
                "indicator": "macd",
                "ticker": ticker,
                "values": values,
                "parameters": {
                    "timespan": timespan,
                    "short_window": short_window,
                    "long_window": long_window,
                    "signal_window": signal_window,
                },
                "count": len(values),
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        # Handle unexpected errors
        return json.dumps(
            {
                "error": "API request failed",
                "message": f"Failed to retrieve MACD data from Polygon.io: {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_stock_quote_multi(tickers: list[str], market_type: str = "stocks") -> str:
    """Get snapshot quotes for multiple ticker symbols from Polygon.io API.

    Use this tool when the user requests quotes for MULTIPLE ticker symbols
    (2 or more), market snapshots with multiple stocks, or comparative analysis
    across multiple tickers.

    This tool provides real-time snapshot data for multiple tickers in a single
    API call via Polygon.io direct API.

    Args:
        tickers: List of ticker symbols to get snapshots for (e.g., ["SPY", "QQQ", "IWM"])
        market_type: Asset class type - "stocks", "options", "forex", or "crypto" (default: "stocks")

    Returns:
        JSON string containing multi-ticker snapshot data with format:
        {
            "status": "success",
            "market_type": "stocks",
            "tickers": [
                {
                    "ticker": "SPY",
                    "day": {"c": 450.25, "h": 451.00, "l": 449.50, "o": 450.00, ...},
                    "min": {...},
                    "prevDay": {...},
                    "todaysChange": 2.50,
                    "todaysChangePerc": 0.56,
                    "updated": 1696531200000
                },
                ...
            ],
            "count": 3,
            "source": "Polygon.io"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "source": "Polygon.io"
        }

    Note:
        - Optimized for multiple ticker queries (2+ symbols)
        - Returns comprehensive snapshot data: day, minute, previous day
        - For SINGLE ticker quotes, use get_stock_quote() instead
        - Data updates in real-time from Polygon.io servers
        - This is a direct API call (not using MCP server)

    Examples:
        - "Stock Snapshot: SPY, QQQ, IWM"
        - "AAPL and MSFT prices"
        - "Market snapshot: TSLA, NVDA, AMD"
        - "Compare GOOGL, META, AMZN"
    """
    try:
        # Call Polygon API with lazy client initialization
        client = _get_polygon_client()
        snapshots = client.get_snapshot_all(market_type, tickers)

        # Check if API returned valid data
        if not snapshots:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No snapshot data returned from Polygon.io for {tickers}.",
                    "source": "Polygon.io",
                }
            )

        # Process snapshots into structured format
        ticker_data = []
        for snapshot in snapshots:
            ticker_info = {
                "ticker": getattr(snapshot, "ticker", ""),
                "day": {},
                "min": {},
                "prevDay": {},
                "todaysChange": getattr(snapshot, "todaysChange", 0.0),
                "todaysChangePerc": getattr(snapshot, "todaysChangePerc", 0.0),
                "updated": getattr(snapshot, "updated", 0),
            }

            # Extract day data
            if hasattr(snapshot, "day") and snapshot.day:
                day = snapshot.day
                ticker_info["day"] = {
                    "c": getattr(day, "c", 0.0),
                    "h": getattr(day, "h", 0.0),
                    "l": getattr(day, "l", 0.0),
                    "o": getattr(day, "o", 0.0),
                    "v": getattr(day, "v", 0),
                    "vw": getattr(day, "vw", 0.0),
                }

            # Extract minute data
            if hasattr(snapshot, "min") and snapshot.min:
                minute = snapshot.min
                ticker_info["min"] = {
                    "c": getattr(minute, "c", 0.0),
                    "h": getattr(minute, "h", 0.0),
                    "l": getattr(minute, "l", 0.0),
                    "o": getattr(minute, "o", 0.0),
                    "v": getattr(minute, "v", 0),
                }

            # Extract previous day data
            if hasattr(snapshot, "prevDay") and snapshot.prevDay:
                prev = snapshot.prevDay
                ticker_info["prevDay"] = {
                    "c": getattr(prev, "c", 0.0),
                    "h": getattr(prev, "h", 0.0),
                    "l": getattr(prev, "l", 0.0),
                    "o": getattr(prev, "o", 0.0),
                    "v": getattr(prev, "v", 0),
                    "vw": getattr(prev, "vw", 0.0),
                }

            ticker_data.append(ticker_info)

        return json.dumps(
            {
                "status": "success",
                "market_type": market_type,
                "tickers": ticker_data,
                "count": len(ticker_data),
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "error": "API Error",
                "message": f"Polygon.io API error: {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_options_quote_single(underlying_asset: str, option_contract: str) -> str:
    """
    Get snapshot quote for a single options contract from Polygon.io API.

    Use this tool when the user requests quotes for a SINGLE options contract,
    options snapshot with specific contract details, or options Greeks analysis.

    Args:
        underlying_asset: Underlying stock ticker symbol (e.g., "AAPL", "SPY")
        option_contract: Options contract identifier in format:
                        O:TICKER{YYMMDD}{C/P}{STRIKE*1000}
                        Example: "O:SPY251219C00650000" (SPY Dec 19 2025 $650 Call)

    Returns:
        JSON string with format:
        {
            "status": "success",
            "underlying_asset": "SPY",
            "contract": "O:SPY251219C00650000",
            "details": {
                "break_even_price": 655.50,
                "day": { "open": 10.50, "high": 11.20, ... },
                "greeks": { "delta": 0.65, "gamma": 0.02, ... },
                "implied_volatility": 0.25,
                "open_interest": 15000,
                "last_quote": { "bid": 10.80, "ask": 10.90, ... },
                "last_trade": { "price": 10.85, "size": 10, ... },
                "updated": 1704999600000
            },
            "source": "Polygon.io"
        }

        On error:
        {
            "error": "No data" | "API Error",
            "message": "Error description",
            "source": "Polygon.io"
        }

    Notes:
        - Options contract format: O:TICKER{YYMMDD}{C/P}{STRIKE*1000}
        - Greeks include: delta, gamma, theta, vega
        - Implied volatility returned as decimal (0.25 = 25%)
        - All prices in USD
        - Timestamps in milliseconds since epoch
        - Open interest updated once per day
        - Requires valid options contract identifier

    Examples:
        1. User: "Options quote for SPY December 650 call"
           Action: get_options_quote_single(
               underlying_asset='SPY',
               option_contract='O:SPY251219C00650000'
           )

        2. User: "Show me AAPL 180 put option snapshot"
           Action: get_options_quote_single(
               underlying_asset='AAPL',
               option_contract='O:AAPL251219P00180000'
           )

        3. User: "Greeks for TSLA call option O:TSLA251219C00300000"
           Action: get_options_quote_single(
               underlying_asset='TSLA',
               option_contract='O:TSLA251219C00300000'
           )

    Tool Selection Rules:
        ✅ Use THIS tool when:
           - User requests SINGLE options contract quote
           - User asks for options Greeks (delta, gamma, theta, vega)
           - User provides specific options contract identifier
           - User asks for implied volatility
           - User wants options snapshot with contract details

        ❌ Do NOT use for:
           - Multiple options contracts (use get_snapshot_all with market_type='options')
           - Stock quotes (use get_stock_quote for single, get_stock_quote_multi for multiple)
           - Historical options data (use OHLC bar tools)
    """
    try:
        client = _get_polygon_client()

        # Get options snapshot using Polygon client
        snapshot = client.get_snapshot_option(underlying_asset, option_contract)

        if not snapshot:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No snapshot data available for options contract '{option_contract}' on underlying asset '{underlying_asset}'.",
                    "source": "Polygon.io",
                }
            )

        # Extract option contract details
        contract_details = {
            "break_even_price": getattr(snapshot, "break_even_price", None),
            "day": {},
            "greeks": {},
            "implied_volatility": getattr(snapshot, "implied_volatility", None),
            "open_interest": getattr(snapshot, "open_interest", None),
            "last_quote": {},
            "last_trade": {},
            "updated": getattr(snapshot, "updated", 0),
        }

        # Extract day data if available
        day = getattr(snapshot, "day", None)
        if day:
            contract_details["day"] = {
                "open": getattr(day, "open", None),
                "high": getattr(day, "high", None),
                "low": getattr(day, "low", None),
                "close": getattr(day, "close", None),
                "volume": getattr(day, "volume", None),
                "vwap": getattr(day, "vwap", None),
            }

        # Extract Greeks if available
        greeks = getattr(snapshot, "greeks", None)
        if greeks:
            contract_details["greeks"] = {
                "delta": getattr(greeks, "delta", None),
                "gamma": getattr(greeks, "gamma", None),
                "theta": getattr(greeks, "theta", None),
                "vega": getattr(greeks, "vega", None),
            }

        # Extract last quote if available
        last_quote = getattr(snapshot, "last_quote", None)
        if last_quote:
            contract_details["last_quote"] = {
                "bid": getattr(last_quote, "bid", None),
                "ask": getattr(last_quote, "ask", None),
                "bid_size": getattr(last_quote, "bid_size", None),
                "ask_size": getattr(last_quote, "ask_size", None),
                "timeframe": getattr(last_quote, "timeframe", None),
            }

        # Extract last trade if available
        last_trade = getattr(snapshot, "last_trade", None)
        if last_trade:
            contract_details["last_trade"] = {
                "price": getattr(last_trade, "price", None),
                "size": getattr(last_trade, "size", None),
                "conditions": getattr(last_trade, "conditions", None),
                "exchange": getattr(last_trade, "exchange", None),
                "timeframe": getattr(last_trade, "timeframe", None),
            }

        return json.dumps(
            {
                "status": "success",
                "underlying_asset": underlying_asset,
                "contract": option_contract,
                "details": contract_details,
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "error": "API Error",
                "message": f"Polygon.io API error for options contract '{option_contract}': {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_OHLC_bars_custom_date_range(  # pylint: disable=too-many-positional-arguments
    ticker: str,
    from_date: str,
    to_date: str,
    timespan: str = "day",
    multiplier: int = 1,
    limit: int = 120,
) -> str:
    """
    Get OHLC (Open, High, Low, Close) aggregate bars for a custom date range from Polygon.io API.

    Use this tool when the user requests historical price data over a CUSTOM date range,
    multi-day/week/month analysis, or time series data between specific dates.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "SPY")
        from_date: Start date in YYYY-MM-DD format (e.g., "2024-01-01")
        to_date: End date in YYYY-MM-DD format (e.g., "2024-12-31")
        timespan: Bar timespan - "minute", "hour", "day", "week", "month", "quarter", "year"
                 (default: "day")
        multiplier: Size of timespan multiplier (e.g., 1 = 1 day, 5 = 5 days) (default: 1)
        limit: Maximum number of bars to return, max 50000 (default: 120)

    Returns:
        JSON string with format:
        {
            "status": "success",
            "ticker": "AAPL",
            "from_date": "2024-01-01",
            "to_date": "2024-12-31",
            "timespan": "day",
            "multiplier": 1,
            "bars": [
                {
                    "timestamp": 1704067200000,
                    "open": 150.25,
                    "high": 152.80,
                    "low": 149.50,
                    "close": 151.90,
                    "volume": 75000000,
                    "vwap": 151.20,
                    "transactions": 450000
                },
                ...
            ],
            "count": 120,
            "source": "Polygon.io"
        }

        On error:
        {
            "error": "No data" | "API Error",
            "message": "Error description",
            "source": "Polygon.io"
        }

    Notes:
        - Date format must be YYYY-MM-DD
        - Timestamps returned in milliseconds since epoch
        - VWAP = Volume Weighted Average Price
        - All prices in USD
        - Maximum 50,000 bars per request
        - Timespan options: minute, hour, day, week, month, quarter, year
        - Multiplier allows custom intervals (e.g., 5-minute bars = timespan='minute', multiplier=5)
        - Data availability depends on Polygon.io subscription tier

    Examples:
        1. User: "AAPL daily prices from January to March 2024"
           Action: get_OHLC_bars_custom_date_range(
               ticker='AAPL',
               from_date='2024-01-01',
               to_date='2024-03-31',
               timespan='day',
               multiplier=1
           )

        2. User: "SPY hourly bars for the last week of December 2024"
           Action: get_OHLC_bars_custom_date_range(
               ticker='SPY',
               from_date='2024-12-24',
               to_date='2024-12-31',
               timespan='hour',
               multiplier=1
           )

        3. User: "TSLA 5-minute bars on 2024-12-15"
           Action: get_OHLC_bars_custom_date_range(
               ticker='TSLA',
               from_date='2024-12-15',
               to_date='2024-12-15',
               timespan='minute',
               multiplier=5
           )

        4. User: "NVDA weekly candles Q1 2024"
           Action: get_OHLC_bars_custom_date_range(
               ticker='NVDA',
               from_date='2024-01-01',
               to_date='2024-03-31',
               timespan='week',
               multiplier=1
           )

    Tool Selection Rules:
        ✅ Use THIS tool when:
           - User requests historical data over CUSTOM date range
           - User specifies "from X to Y" dates
           - User asks for multi-day/week/month price history
           - User wants intraday data (minute/hour bars)
           - User needs time series analysis between specific dates

        ❌ Do NOT use for:
           - Single specific date (use get_OHLC_bars_specific_date)
           - Previous trading day close (use get_OHLC_bars_previous_close)
           - Real-time quotes (use get_stock_quote or get_stock_quote_multi)
           - Options data (use get_options_quote_single)
    """
    try:
        client = _get_polygon_client()

        # Get aggregate bars using Polygon client
        aggs = client.list_aggs(
            ticker=ticker,
            multiplier=multiplier,
            timespan=timespan,
            from_=from_date,
            to=to_date,
            limit=limit,
        )

        if not aggs:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No OHLC bar data available for ticker '{ticker}' from {from_date} to {to_date}.",
                    "source": "Polygon.io",
                }
            )

        # Extract bar data
        bars = []
        for agg in aggs:
            bar_data = {
                "timestamp": getattr(agg, "timestamp", 0),
                "open": getattr(agg, "open", None),
                "high": getattr(agg, "high", None),
                "low": getattr(agg, "low", None),
                "close": getattr(agg, "close", None),
                "volume": getattr(agg, "volume", None),
                "vwap": getattr(agg, "vwap", None),
                "transactions": getattr(agg, "transactions", None),
            }
            bars.append(bar_data)

        return json.dumps(
            {
                "status": "success",
                "ticker": ticker,
                "from_date": from_date,
                "to_date": to_date,
                "timespan": timespan,
                "multiplier": multiplier,
                "bars": bars,
                "count": len(bars),
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "error": "API Error",
                "message": f"Polygon.io API error for ticker '{ticker}' from {from_date} to {to_date}: {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_OHLC_bars_specific_date(ticker: str, date: str, adjusted: bool = True) -> str:
    """
    Get OHLC (Open, High, Low, Close) aggregate bars for a specific date from Polygon.io API.

    Use this tool when the user requests historical price data for a SINGLE SPECIFIC date,
    daily OHLC on exact date, or "what was the price on [date]" queries.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "SPY")
        date: Specific date in YYYY-MM-DD format (e.g., "2024-12-15")
        adjusted: Whether to adjust for splits and dividends (default: True)

    Returns:
        JSON string with format:
        {
            "status": "success",
            "ticker": "AAPL",
            "date": "2024-12-15",
            "adjusted": true,
            "bar": {
                "open": 150.25,
                "high": 152.80,
                "low": 149.50,
                "close": 151.90,
                "volume": 75000000,
                "vwap": 151.20,
                "transactions": 450000,
                "preMarket": 149.80,
                "afterHours": 152.10
            },
            "source": "Polygon.io"
        }

        On error:
        {
            "error": "No data" | "API Error",
            "message": "Error description",
            "source": "Polygon.io"
        }

    Notes:
        - Date format must be YYYY-MM-DD
        - Returns OHLC data for regular trading hours
        - May include pre-market and after-hours data if available
        - VWAP = Volume Weighted Average Price
        - All prices in USD
        - adjusted=True accounts for stock splits and dividends
        - Data only available for past trading days (not future dates)
        - Returns error for weekends/holidays when markets are closed

    Examples:
        1. User: "AAPL price on December 15, 2024"
           Action: get_OHLC_bars_specific_date(
               ticker='AAPL',
               date='2024-12-15',
               adjusted=True
           )

        2. User: "What was SPY OHLC on 2024-01-05?"
           Action: get_OHLC_bars_specific_date(
               ticker='SPY',
               date='2024-01-05',
               adjusted=True
           )

        3. User: "TSLA unadjusted price on 2024-06-10"
           Action: get_OHLC_bars_specific_date(
               ticker='TSLA',
               date='2024-06-10',
               adjusted=False
           )

        4. User: "Show me NVDA daily bar for yesterday" (assuming today is 2024-12-16)
           Action: get_OHLC_bars_specific_date(
               ticker='NVDA',
               date='2024-12-15',
               adjusted=True
           )

    Tool Selection Rules:
        ✅ Use THIS tool when:
           - User requests price data for SINGLE SPECIFIC date
           - User asks "what was the price on [date]"
           - User wants OHLC for exact trading day
           - User specifies single date like "December 15" or "2024-12-15"
           - User asks for "yesterday" or "last Friday" (convert to specific date)

        ❌ Do NOT use for:
           - Custom date ranges (use get_OHLC_bars_custom_date_range)
           - Previous trading day close (use get_OHLC_bars_previous_close)
           - Real-time quotes (use get_stock_quote or get_stock_quote_multi)
           - Multiple dates (use get_OHLC_bars_custom_date_range)
           - Options data (use get_options_quote_single)
    """
    try:
        client = _get_polygon_client()

        # Get daily OHLC aggregate using Polygon client
        agg = client.get_daily_open_close_agg(ticker=ticker, date=date, adjusted=adjusted)

        if not agg:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No OHLC bar data available for ticker '{ticker}' on date {date}. Market may have been closed.",
                    "source": "Polygon.io",
                }
            )

        # Extract bar data
        bar_data = {
            "open": getattr(agg, "open", None),
            "high": getattr(agg, "high", None),
            "low": getattr(agg, "low", None),
            "close": getattr(agg, "close", None),
            "volume": getattr(agg, "volume", None),
            "vwap": getattr(agg, "vwap", None),
            "transactions": getattr(agg, "transactions", None),
            "preMarket": getattr(agg, "preMarket", None),
            "afterHours": getattr(agg, "afterHours", None),
        }

        return json.dumps(
            {
                "status": "success",
                "ticker": ticker,
                "date": date,
                "adjusted": adjusted,
                "bar": bar_data,
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "error": "API Error",
                "message": f"Polygon.io API error for ticker '{ticker}' on date {date}: {str(e)}",
                "source": "Polygon.io",
            }
        )


@function_tool
async def get_OHLC_bars_previous_close(ticker: str, adjusted: bool = True) -> str:
    """
    Get OHLC (Open, High, Low, Close) aggregate bars for the previous trading day from Polygon.io API.

    Use this tool when the user requests the most recent completed trading day's data,
    "yesterday's close", "last trading day", or previous day OHLC information.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "SPY")
        adjusted: Whether to adjust for splits and dividends (default: True)

    Returns:
        JSON string with format:
        {
            "status": "success",
            "ticker": "AAPL",
            "adjusted": true,
            "bar": {
                "symbol": "AAPL",
                "open": 150.25,
                "high": 152.80,
                "low": 149.50,
                "close": 151.90,
                "volume": 75000000,
                "vwap": 151.20,
                "timestamp": 1704067200000,
                "transactions": 450000,
                "preMarket": 149.80,
                "afterHours": 152.10
            },
            "source": "Polygon.io"
        }

        On error:
        {
            "error": "No data" | "API Error",
            "message": "Error description",
            "source": "Polygon.io"
        }

    Notes:
        - Returns data for the most recent completed trading day
        - Automatically handles weekends/holidays (skips to last market day)
        - VWAP = Volume Weighted Average Price
        - All prices in USD
        - Timestamp in milliseconds since epoch
        - adjusted=True accounts for stock splits and dividends
        - May include pre-market and after-hours data if available
        - "Previous close" refers to the close of the last trading day

    Examples:
        1. User: "AAPL previous close"
           Action: get_OHLC_bars_previous_close(
               ticker='AAPL',
               adjusted=True
           )

        2. User: "What was SPY yesterday's OHLC?"
           Action: get_OHLC_bars_previous_close(
               ticker='SPY',
               adjusted=True
           )

        3. User: "Last trading day for TSLA"
           Action: get_OHLC_bars_previous_close(
               ticker='TSLA',
               adjusted=True
           )

        4. User: "NVDA unadjusted previous close"
           Action: get_OHLC_bars_previous_close(
               ticker='NVDA',
               adjusted=False
           )

        5. User: "Show me MSFT most recent completed trading day"
           Action: get_OHLC_bars_previous_close(
               ticker='MSFT',
               adjusted=True
           )

    Tool Selection Rules:
        ✅ Use THIS tool when:
           - User requests "previous close" or "previous day"
           - User asks for "yesterday's close" (when today is a trading day)
           - User wants "last trading day" OHLC
           - User asks for "most recent completed trading day"
           - User wants latest historical bar (not real-time)

        ❌ Do NOT use for:
           - Real-time current price (use get_stock_quote or get_stock_quote_multi)
           - Specific historical date (use get_OHLC_bars_specific_date)
           - Custom date ranges (use get_OHLC_bars_custom_date_range)
           - Multiple tickers (use get_stock_quote_multi then specify previous close in context)
           - Options data (use get_options_quote_single)
    """
    try:
        client = _get_polygon_client()

        # Get previous close aggregate using Polygon client
        agg = client.get_previous_close_agg(ticker=ticker, adjusted=adjusted)

        if not agg or len(agg) == 0:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No previous close bar data available for ticker '{ticker}'.",
                    "source": "Polygon.io",
                }
            )

        # Extract first result (previous close)
        prev_close = agg[0] if isinstance(agg, list) else agg

        # Extract bar data
        bar_data = {
            "symbol": getattr(prev_close, "symbol", ticker),
            "open": getattr(prev_close, "open", None),
            "high": getattr(prev_close, "high", None),
            "low": getattr(prev_close, "low", None),
            "close": getattr(prev_close, "close", None),
            "volume": getattr(prev_close, "volume", None),
            "vwap": getattr(prev_close, "vwap", None),
            "timestamp": getattr(prev_close, "timestamp", 0),
            "transactions": getattr(prev_close, "transactions", None),
            "preMarket": getattr(prev_close, "preMarket", None),
            "afterHours": getattr(prev_close, "afterHours", None),
        }

        return json.dumps(
            {
                "status": "success",
                "ticker": ticker,
                "adjusted": adjusted,
                "bar": bar_data,
                "source": "Polygon.io",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "error": "API Error",
                "message": f"Polygon.io API error for ticker '{ticker}' previous close: {str(e)}",
                "source": "Polygon.io",
            }
        )
