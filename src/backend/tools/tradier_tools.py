"""
Tradier custom tools for OpenAI AI Agent.
Provides options expiration dates via Tradier API.
"""

import asyncio
import json
import os
import time
from datetime import datetime, timedelta, timezone

import requests
from agents import function_tool

from .api_utils import TRADIER_TIMEOUT, create_tradier_headers
from .error_utils import create_error_response
from .formatting_helpers import create_options_chain_table, create_price_history_summary
from .validation_utils import validate_and_sanitize_ticker


def _get_tradier_api_key():
    """Get Tradier API key from environment.

    Lazy initialization ensures .env is loaded before accessing API key.
    """
    return os.getenv("TRADIER_API_KEY")


def _format_tradier_quote(quote: dict) -> dict:
    """Format Tradier quote data to match expected response structure.
    
    Args:
        quote: Raw quote data from Tradier API
        
    Returns:
        Formatted quote dictionary with standardized field names
    """
    return {
        "ticker": quote.get("symbol", ""),
        "current_price": round(quote.get("last", 0.0), 2),
        "change": round(quote.get("change", 0.0), 2),
        "percent_change": round(quote.get("change_percentage", 0.0), 2),
        "high": round(quote.get("high", 0.0), 2),
        "low": round(quote.get("low", 0.0), 2),
        "open": round(quote.get("open", 0.0), 2),
        "previous_close": round(quote.get("prevclose", 0.0), 2),
        "source": "Tradier"
    }


async def _get_stock_quote(ticker: str) -> str:
    """Get real-time stock quote from Tradier API (uncached implementation).

    Internal function that performs the actual API call without caching.
    Use get_stock_quote() instead for cached access.
    """
    try:
        # Validate and sanitize ticker input
        ticker, error = validate_and_sanitize_ticker(ticker)
        if error:
            return error

        # Get API key from environment
        api_key = os.getenv("TRADIER_API_KEY")
        if not api_key:
            return create_error_response(
                "Configuration error",
                "TRADIER_API_KEY not configured in environment",
                ticker=ticker,
            )

        # Build request to Tradier API
        url = "https://api.tradier.com/v1/markets/quotes"
        headers = create_tradier_headers(api_key)
        params = {"symbols": ticker}

        # Get aiohttp session from connection pool
        from .api_utils import get_connection_pool
        pool = get_connection_pool()
        session = await pool.get_session()

        # Make async API request with timeout
        async with session.get(url, headers=headers, params=params) as response:
            response.raise_for_status()
            data = await response.json()

        quotes_data = data.get("quotes", {}).get("quote")

        # Check if API returned valid data
        if not quotes_data:
            return create_error_response(
                "No data",
                f"No quote data available for ticker: {ticker}. Verify ticker symbol is valid.",
                ticker=ticker,
            )

        # Handle single vs multi-ticker response structure
        if isinstance(quotes_data, list):
            # Multi-ticker response - return array of formatted quotes
            results = []
            for quote in quotes_data:
                results.append(_format_tradier_quote(quote))
            return json.dumps(results, indent=2)
        else:
            # Single ticker response - return single formatted quote
            return json.dumps(_format_tradier_quote(quotes_data), indent=2)

    except asyncio.TimeoutError:
        return create_error_response(
            "Timeout",
            f"Request timed out while fetching quote for {ticker}",
            ticker=ticker,
        )
    except Exception as e:
        return create_error_response(
            "API request failed",
            f"Tradier API request failed: {str(e)}",
            ticker=ticker,
        )


@function_tool
async def get_stock_quote(ticker: str) -> str:
    """Get real-time stock quote(s) for one or more tickers from Tradier API.

    Args:
        ticker: Single "AAPL" or multiple "AAPL,TSLA,NVDA" (comma-separated, no spaces).

    Returns:
        JSON string with quote data (ticker, current_price, change, percent_change, high, low, open, previous_close, source).
        Multiple tickers return array of quote objects.

    Note: Handles up to 10 tickers. Real-time updates during market hours.
    """
    return await _get_stock_quote(ticker)


async def _get_options_expiration_dates(ticker: str) -> str:
    """Get valid options expiration dates for a ticker from Tradier API (uncached implementation).

    Internal function that performs the actual API call without caching.
    Use get_options_expiration_dates() instead for cached access.
    """
    try:
        # Validate and sanitize ticker input
        ticker, error = validate_and_sanitize_ticker(ticker)
        if error:
            return error

        # Get API key
        api_key = _get_tradier_api_key()
        if not api_key:
            return create_error_response(
                "Configuration error",
                "TRADIER_API_KEY not found in environment",
                ticker=ticker,
            )

        # Call Tradier API
        url = f"https://api.tradier.com/v1/markets/options/expirations?symbol={ticker}"
        headers = create_tradier_headers(api_key)

        # Get aiohttp session from connection pool
        from .api_utils import get_connection_pool
        pool = get_connection_pool()
        session = await pool.get_session()

        # Make async API request
        async with session.get(url, headers=headers) as response:
            # Check HTTP status
            if response.status != 200:
                return create_error_response(
                    "API request failed",
                    f"Tradier API returned status {response.status}",
                    ticker=ticker,
                )

            # Parse response
            data = await response.json()

        # Extract expiration dates
        expirations = data.get("expirations", {})
        dates = expirations.get("date", [])

        # Check if we got valid data
        if not dates:
            return create_error_response(
                "No data",
                f"No expiration dates available for ticker: {ticker}. Verify ticker symbol is valid.",
                ticker=ticker,
            )

        # Ensure dates is a list (API returns single string if only 1 date)
        if isinstance(dates, str):
            dates = [dates]

        # Format response
        return json.dumps(
            {
                "ticker": ticker,
                "expiration_dates": dates,
                "count": len(dates),
                "source": "Tradier",
            }
        )

    except asyncio.TimeoutError:
        return create_error_response(
            "Timeout",
            f"Tradier API request timed out for {ticker}",
            ticker=ticker,
        )
    except Exception as e:
        return create_error_response(
            "API request failed",
            f"Failed to retrieve expiration dates for {ticker}: {str(e)}",
            ticker=ticker,
        )


@function_tool
async def get_options_expiration_dates(ticker: str) -> str:
    """Get available options expiration dates for a ticker from Tradier API.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "SPY").

    Returns:
        JSON string with expiration dates array (ticker, expiration_dates[], count, source).
        Dates in YYYY-MM-DD format, sorted chronologically.

    Note: Includes weekly and monthly expirations.
    """
    return await _get_options_expiration_dates(ticker)


async def _get_stock_price_history(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "daily"
) -> str:
    """Get historical stock price data from Tradier API.

    Use this tool when the user requests historical stock prices, OHLC bars,
    price performance over time, or daily/weekly/monthly data.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA").
                Must be a valid ticker symbol.
        start_date: Start date in YYYY-MM-DD format (e.g., "2025-01-01").
        end_date: End date in YYYY-MM-DD format (e.g., "2025-01-10").
        interval: Time interval - "daily", "weekly", or "monthly".
                  SELECT INTELLIGENTLY based on user query timeframe:
                  - "daily" for queries about days/short periods (e.g., "last 5 days", "this week")
                  - "weekly" for queries about weeks (e.g., "last 2 weeks", "past month")
                  - "monthly" for queries about months/long periods (e.g., "last 3 months", "year to date")
                  Always choose based on query context.

    Returns:
        JSON string with historical OHLC data:
        {
            "ticker": "SPY",
            "interval": "daily",
            "start_date": "2025-01-01",
            "end_date": "2025-01-10",
            "bars": [
                {
                    "date": "2025-01-02",
                    "open": 589.39,
                    "high": 591.13,
                    "low": 580.5,
                    "close": 584.64,
                    "volume": 50203975
                },
                ...
            ],
            "count": 6,
            "source": "Tradier"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "ticker": "SYMBOL"
        }

    Note:
        - Supports daily, weekly, and monthly intervals
        - Date range is inclusive (includes start_date and end_date)
        - Data updates in real-time during market hours
        - Weekly bars show data for week ending on date
        - Monthly bars show data for month ending on date

    Examples:
        - "Stock price performance the last 5 trading days: SPY"
          → Agent calculates dates, uses interval="daily"
        - "Stock price performance the last 2 weeks: NVDA"
          → Agent calculates dates, uses interval="weekly"
        - "Stock price performance the last month: AAPL"
          → Agent calculates dates, uses interval="monthly"
    """
    try:
        # Validate and sanitize ticker input
        ticker, error = validate_and_sanitize_ticker(ticker)
        if error:
            return error

        # Validate interval
        valid_intervals = ["daily", "weekly", "monthly"]
        if interval not in valid_intervals:
            return create_error_response(
                "Invalid interval",
                f"Interval must be one of: {', '.join(valid_intervals)}. Got: {interval}",
                interval=interval,
                ticker=ticker,
            )

        # Validate dates (basic presence check)
        if not start_date or not end_date:
            return create_error_response(
                "Invalid dates",
                "Both start_date and end_date are required (YYYY-MM-DD format)",
                start_date=start_date,
                end_date=end_date,
                ticker=ticker,
            )

        # Weekend detection and date adjustment
        # Adjust dates if they fall on Saturday or Sunday to previous Friday
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")

            # Adjust start_date if weekend (Saturday=5, Sunday=6)
            if start_dt.weekday() == 5:  # Saturday
                start_dt = start_dt - timedelta(days=1)  # Move to Friday
            elif start_dt.weekday() == 6:  # Sunday
                start_dt = start_dt - timedelta(days=2)  # Move to Friday

            # Adjust end_date if weekend
            if end_dt.weekday() == 5:  # Saturday
                end_dt = end_dt - timedelta(days=1)  # Move to Friday
            elif end_dt.weekday() == 6:  # Sunday
                end_dt = end_dt - timedelta(days=2)  # Move to Friday

            # Convert back to string format
            start_date = start_dt.strftime("%Y-%m-%d")
            end_date = end_dt.strftime("%Y-%m-%d")
        except ValueError:
            # If date parsing fails, continue with original dates
            # API will return appropriate error
            pass

        # Get API key
        api_key = _get_tradier_api_key()
        if not api_key:
            return create_error_response(
                "Configuration error",
                "TRADIER_API_KEY not found in environment",
                ticker=ticker,
            )

        # Build request to Tradier API
        url = "https://api.tradier.com/v1/markets/history"
        headers = create_tradier_headers(api_key)
        params = {
            "symbol": ticker,
            "interval": interval,
            "start": start_date,
            "end": end_date,
        }

        # Get aiohttp session from connection pool
        from .api_utils import get_connection_pool
        pool = get_connection_pool()
        session = await pool.get_session()

        # Make async API request
        async with session.get(url, headers=headers, params=params) as response:
            # Check HTTP status
            if response.status != 200:
                return create_error_response(
                    "API request failed",
                    f"Tradier API returned status {response.status}",
                    ticker=ticker,
                    interval=interval,
                )

            # Parse response
            data = await response.json()

        history_data = data.get("history", {})
        bars_data = history_data.get("day", [])
        # Handle weekly/monthly: single dict vs daily: array of dicts
        if isinstance(bars_data, dict):
            bars_data = [bars_data]

        # Check if API returned data
        if not bars_data:
            return create_error_response(
                "No data",
                f"No historical data available for {ticker} from {start_date} to {end_date}. Verify ticker symbol and date range.",
                ticker=ticker,
                interval=interval,
                start_date=start_date,
                end_date=end_date,
            )

        # Format response with bars
        formatted_bars = []
        for bar in bars_data:
            formatted_bars.append(_format_tradier_history_bar(bar))

        # Return formatted markdown summary
        return create_price_history_summary(
            ticker=ticker,
            interval=interval,
            bars=formatted_bars,
            start_date=start_date,
            end_date=end_date,
        )

    except asyncio.TimeoutError:
        return create_error_response(
            "Timeout",
            f"Tradier API request timed out for {ticker}",
            ticker=ticker,
        )
    except Exception as e:
        return create_error_response(
            "API request failed",
            f"Failed to retrieve historical data for {ticker}: {str(e)}",
            ticker=ticker,
        )


@function_tool
async def get_stock_price_history(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "daily"
) -> str:
    """Get historical stock price data (OHLC bars) from Tradier API.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
        interval: "daily", "weekly", or "monthly". See RULE #3 for selection logic.

    Returns:
        JSON string with historical OHLC data (ticker, interval, start_date, end_date, bars[], count, source).
        Each bar includes date, open, high, low, close, volume.

    Note: Date range inclusive. Tool auto-adjusts weekend dates to previous Friday.
    """
    return await _get_stock_price_history(ticker, start_date, end_date, interval)


def _format_tradier_history_bar(bar: dict) -> dict:
    """Format Tradier history bar to consistent structure with rounded values.

    Args:
        bar: Raw bar data from Tradier API with fields:
             date, open, high, low, close, volume

    Returns:
        Formatted bar dictionary with rounded decimal values
    """
    return {
        "date": bar.get("date", ""),
        "open": round(bar.get("open", 0.0), 2),
        "high": round(bar.get("high", 0.0), 2),
        "low": round(bar.get("low", 0.0), 2),
        "close": round(bar.get("close", 0.0), 2),
        "volume": bar.get("volume", 0),
    }






async def _get_options_chain_both(
    ticker: str, current_price: float, expiration_date: str
) -> str:
    """Get both Call and Put Options Chains with 20 strikes each centered around current price (uncached implementation).

    Internal function that performs the actual API call without caching.
    Use get_options_chain_both() instead for cached access.

    Returns both call and put options chains in a single response with separate tables.
    Each chain shows 20 strikes (10 above + 10 below current price), sorted descending.
    """
    try:
        # Validate and sanitize ticker input
        ticker, error = validate_and_sanitize_ticker(ticker)
        if error:
            return error

        if current_price <= 0:
            return create_error_response(
                "Invalid current price",
                f"Current price {current_price} must be positive",
                ticker=ticker,
            )

        if not expiration_date:
            return create_error_response(
                "Invalid expiration date",
                "Expiration date is required (YYYY-MM-DD format)",
                ticker=ticker,
            )

        # Get API key
        api_key = _get_tradier_api_key()
        if not api_key:
            return create_error_response(
                "Configuration error",
                "TRADIER_API_KEY not found in environment",
                ticker=ticker,
            )

        # Build Tradier API request
        url = "https://api.tradier.com/v1/markets/options/chains"
        headers = create_tradier_headers(api_key)
        params = {
            "symbol": ticker,
            "expiration": expiration_date,
            "greeks": "true",  # Required for delta, gamma, theta, vega
        }

        # Get aiohttp session from connection pool
        from .api_utils import get_connection_pool
        pool = get_connection_pool()
        session = await pool.get_session()

        # Make async API request (SINGLE call fetches both calls and puts)
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                return create_error_response(
                    "API request failed",
                    f"Tradier API returned status {response.status}",
                    ticker=ticker,
                )

            # Parse response
            data = await response.json()

        options_data = data.get("options", {})
        option_list = options_data.get("option", [])

        if not option_list:
            return create_error_response(
                "No data",
                f"No options data found for {ticker} expiring {expiration_date}",
                ticker=ticker,
            )

        # Filter for CALL options and apply 20-strike centering
        call_options = [
            opt
            for opt in option_list
            if opt.get("option_type") == "call"
        ]

        if not call_options:
            return create_error_response(
                "No call options found",
                f"No call options found for {ticker}",
                ticker=ticker,
            )

        # Split call strikes above and below current price
        call_strikes_above = [opt for opt in call_options if opt.get("strike", 0) > current_price]
        call_strikes_below = [opt for opt in call_options if opt.get("strike", 0) < current_price]

        # Sort and select 10 from each side for calls
        call_strikes_above.sort(key=lambda x: x.get("strike", 0))  # Ascending
        call_strikes_above = call_strikes_above[:10]  # First 10 above

        call_strikes_below.sort(key=lambda x: x.get("strike", 0), reverse=True)  # Descending
        call_strikes_below = call_strikes_below[:10]  # First 10 below

        # Combine and sort DESCENDING for call options
        call_options = call_strikes_above + call_strikes_below
        call_options.sort(key=lambda x: x.get("strike", 0), reverse=True)

        # Filter for PUT options and apply 20-strike centering
        put_options = [
            opt
            for opt in option_list
            if opt.get("option_type") == "put"
        ]

        if not put_options:
            return create_error_response(
                "No put options found",
                f"No put options found for {ticker}",
                ticker=ticker,
            )

        # Split put strikes above and below current price
        put_strikes_above = [opt for opt in put_options if opt.get("strike", 0) > current_price]
        put_strikes_below = [opt for opt in put_options if opt.get("strike", 0) < current_price]

        # Sort and select 10 from each side for puts
        put_strikes_above.sort(key=lambda x: x.get("strike", 0))  # Ascending
        put_strikes_above = put_strikes_above[:10]  # First 10 above

        put_strikes_below.sort(key=lambda x: x.get("strike", 0), reverse=True)  # Descending
        put_strikes_below = put_strikes_below[:10]  # First 10 below

        # Combine and sort DESCENDING for put options
        put_options = put_strikes_above + put_strikes_below
        put_options.sort(key=lambda x: x.get("strike", 0), reverse=True)

        # Format call options data
        formatted_call_options = []
        for opt in call_options:
            strike = opt.get("strike", 0)
            bid = opt.get("bid", 0)
            ask = opt.get("ask", 0)

            greeks = opt.get("greeks", {})
            delta = greeks.get("delta", 0)
            gamma = greeks.get("gamma", 0)
            implied_vol = greeks.get("smv_vol", 0) * 100  # Convert to percentage

            volume = opt.get("volume", 0) or 0  # Handle None
            open_interest = opt.get("open_interest", 0) or 0  # Handle None

            formatted_call_options.append(
                {
                    "strike": round(strike, 2),
                    "bid": round(bid, 2),
                    "ask": round(ask, 2),
                    "delta": round(delta, 2),
                    "gamma": round(gamma, 2),
                    "implied_volatility": round(implied_vol, 2),
                    "volume": volume,
                    "open_interest": open_interest,
                }
            )

        # Format put options data
        formatted_put_options = []
        for opt in put_options:
            strike = opt.get("strike", 0)
            bid = opt.get("bid", 0)
            ask = opt.get("ask", 0)

            greeks = opt.get("greeks", {})
            delta = greeks.get("delta", 0)
            gamma = greeks.get("gamma", 0)
            implied_vol = greeks.get("smv_vol", 0) * 100  # Convert to percentage

            volume = opt.get("volume", 0) or 0  # Handle None
            open_interest = opt.get("open_interest", 0) or 0  # Handle None

            formatted_put_options.append(
                {
                    "strike": round(strike, 2),
                    "bid": round(bid, 2),
                    "ask": round(ask, 2),
                    "delta": round(delta, 2),
                    "gamma": round(gamma, 2),
                    "implied_volatility": round(implied_vol, 2),
                    "volume": volume,
                    "open_interest": open_interest,
                }
            )

        # Format call options chain table
        call_table = create_options_chain_table(
            ticker=ticker,
            option_type="call",
            expiration_date=expiration_date,
            current_price=current_price,
            options=formatted_call_options,
        )

        # Format put options chain table
        put_table = create_options_chain_table(
            ticker=ticker,
            option_type="put",
            expiration_date=expiration_date,
            current_price=current_price,
            options=formatted_put_options,
        )

        # Combine both tables with separator
        return f"{call_table}\n\n{put_table}"

    except asyncio.TimeoutError:
        return create_error_response(
            "Timeout",
            f"Tradier API request timed out for {ticker}",
            ticker=ticker,
        )
    except Exception as e:
        return create_error_response(
            "API request failed",
            f"Failed to retrieve options chains for {ticker}: {str(e)}",
            ticker=ticker,
        )


@function_tool
async def get_options_chain_both(
    ticker: str, current_price: float, expiration_date: str
) -> str:
    """Get both Call and Put Options Chains (20 strikes each, centered around current price).

    Use for comprehensive options analysis. Returns both chains in single API call.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
        current_price: Current price of underlying stock (must be > 0).
        expiration_date: Options expiration date in YYYY-MM-DD format. Get from get_options_expiration_dates() first.

    Returns:
        Formatted string with two markdown tables (Call and Put chains, 20 strikes each).
        Strikes centered around current price (10 above, 10 below).
        Columns: Strike, Bid, Ask, Delta, Volume, OI, IV, Gamma.

    Note: Single API call fetches both chains. See RULE #5 for usage guidance.
    """
    return await _get_options_chain_both(ticker, current_price, expiration_date)




# ============================================================================
# Market Status Functions (Migrated from polygon_tools.py - Uses Tradier API)
# ============================================================================

def _map_market_state(state: str) -> str:
    """Map market state to standardized response format.

    Args:
        state: Market state ("open", "closed", "pre", "post")

    Returns:
        Mapped market status ("open", "closed", "extended-hours")
    """
    if state == "open":
        return "open"
    elif state in ["pre", "post"]:
        return "extended-hours"
    else:  # closed
        return "closed"


async def _get_market_status_and_date_time() -> str:
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
            return create_error_response(
                "Configuration error",
                "TRADIER_API_KEY not configured in environment",
                source="Tradier"
            )

        # Build request to Tradier API
        url = "https://api.tradier.com/v1/markets/clock"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Get aiohttp session from connection pool
        from .api_utils import get_connection_pool
        pool = get_connection_pool()
        session = await pool.get_session()

        # Make async API request
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()

        clock_data = data.get("clock", {})

        # Check if API returned valid data
        if not clock_data:
            return create_error_response(
                "No data",
                "No clock data returned from Tradier API.",
                source="Tradier"
            )

        # Extract state and map to current response format
        state = clock_data.get("state", "closed")
        market_status = _map_market_state(state)
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

    except asyncio.TimeoutError:
        return create_error_response(
            "Timeout",
            "Request timed out while fetching market status",
            source="Tradier"
        )
    except Exception as e:
        return create_error_response(
            "API request failed",
            f"Failed to retrieve market status from Tradier: {str(e)}",
            source="Tradier"
        )


@function_tool
async def get_market_status_and_date_time() -> str:
    """Get current market status and date/time from Tradier API.

    Args:
        None - retrieves current status automatically.

    Returns:
        JSON string with market status and datetime (market_status, after_hours, early_hours, exchanges{}, server_time, date, time, source).

    Note: Server time in UTC. Includes pre-market and after-market status.
    """
    return await _get_market_status_and_date_time()
