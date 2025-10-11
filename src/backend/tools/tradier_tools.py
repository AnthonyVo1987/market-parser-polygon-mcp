"""
Tradier custom tools for OpenAI AI Agent.
Provides options expiration dates via Tradier API.
"""

import json
import os

import requests
from agents import function_tool


def _get_tradier_api_key():
    """Get Tradier API key from environment.

    Lazy initialization ensures .env is loaded before accessing API key.
    """
    return os.getenv("TRADIER_API_KEY")


@function_tool
async def get_options_expiration_dates(ticker: str) -> str:
    """Get valid options expiration dates for a ticker from Tradier API.

    Use this tool when the user requests options expiration dates for a specific ticker.
    This provides all available expiration dates for options contracts on the underlying stock.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "SPY", "NVDA").
                Must be a valid ticker symbol.

    Returns:
        JSON string containing expiration dates array with format:
        {
            "ticker": "NVDA",
            "expiration_dates": [
                "2025-10-17",
                "2025-10-24",
                "2025-10-31",
                ...
            ],
            "count": 21,
            "source": "Tradier"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "ticker": "SYMBOL"
        }

    Note:
        - Returns all available expiration dates for the ticker
        - Dates are in YYYY-MM-DD format
        - Dates are sorted chronologically (earliest to latest)
        - Includes weekly and monthly expiration dates
        - Data updates daily

    Examples:
        - "Get options expiration dates for SPY"
        - "What are the available expiration dates for NVDA options?"
        - "Show me TSLA options expiration dates"
    """
    try:
        # Validate ticker input
        if not ticker or not ticker.strip():
            return json.dumps(
                {
                    "error": "Invalid ticker",
                    "message": "Ticker symbol cannot be empty",
                    "ticker": ticker,
                }
            )

        # Clean ticker (uppercase, strip whitespace)
        ticker = ticker.strip().upper()

        # Get API key
        api_key = _get_tradier_api_key()
        if not api_key:
            return json.dumps(
                {
                    "error": "Configuration error",
                    "message": "TRADIER_API_KEY not found in environment",
                    "ticker": ticker,
                }
            )

        # Call Tradier API
        url = f"https://api.tradier.com/v1/markets/options/expirations?symbol={ticker}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        response = requests.get(url, headers=headers, timeout=10)

        # Check HTTP status
        if response.status_code != 200:
            return json.dumps(
                {
                    "error": "API request failed",
                    "message": f"Tradier API returned status {response.status_code}",
                    "ticker": ticker,
                }
            )

        # Parse response
        data = response.json()

        # Extract expiration dates
        expirations = data.get("expirations", {})
        dates = expirations.get("date", [])

        # Check if we got valid data
        if not dates:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No expiration dates available for ticker: {ticker}. Verify ticker symbol is valid.",
                    "ticker": ticker,
                }
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

    except requests.exceptions.Timeout:
        return json.dumps(
            {
                "error": "Timeout",
                "message": f"Tradier API request timed out for {ticker}",
                "ticker": ticker,
            }
        )
    except requests.exceptions.RequestException as e:
        return json.dumps(
            {
                "error": "Network error",
                "message": f"Failed to connect to Tradier API: {str(e)}",
                "ticker": ticker,
            }
        )
    except Exception as e:
        return json.dumps(
            {
                "error": "Unexpected error",
                "message": f"Failed to retrieve expiration dates for {ticker}: {str(e)}",
                "ticker": ticker,
            }
        )


@function_tool
async def get_stock_price_history(
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
        # Validate ticker input
        if not ticker or not ticker.strip():
            return json.dumps(
                {
                    "error": "Invalid ticker",
                    "message": "Ticker symbol cannot be empty",
                    "ticker": ticker,
                }
            )

        # Clean ticker (uppercase, strip whitespace)
        ticker = ticker.strip().upper()

        # Validate interval
        valid_intervals = ["daily", "weekly", "monthly"]
        if interval not in valid_intervals:
            return json.dumps(
                {
                    "error": "Invalid interval",
                    "message": f"Interval must be one of: {', '.join(valid_intervals)}. Got: {interval}",
                    "interval": interval,
                    "ticker": ticker,
                }
            )

        # Validate dates (basic presence check)
        if not start_date or not end_date:
            return json.dumps(
                {
                    "error": "Invalid dates",
                    "message": "Both start_date and end_date are required (YYYY-MM-DD format)",
                    "start_date": start_date,
                    "end_date": end_date,
                    "ticker": ticker,
                }
            )

        # Get API key
        api_key = _get_tradier_api_key()
        if not api_key:
            return json.dumps(
                {
                    "error": "Configuration error",
                    "message": "TRADIER_API_KEY not found in environment",
                    "ticker": ticker,
                }
            )

        # Build request to Tradier API
        url = "https://api.tradier.com/v1/markets/history"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        params = {
            "symbol": ticker,
            "interval": interval,
            "start": start_date,
            "end": end_date,
        }

        # Make API request with timeout
        response = requests.get(url, headers=headers, params=params, timeout=10)

        # Check HTTP status
        if response.status_code != 200:
            return json.dumps(
                {
                    "error": "API request failed",
                    "message": f"Tradier API returned status {response.status_code}",
                    "ticker": ticker,
                    "interval": interval,
                }
            )

        # Parse response
        data = response.json()
        history_data = data.get("history", {})
        bars_data = history_data.get("day", [])

        # Check if API returned data
        if not bars_data:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No historical data available for {ticker} from {start_date} to {end_date}. Verify ticker symbol and date range.",
                    "ticker": ticker,
                    "interval": interval,
                    "start_date": start_date,
                    "end_date": end_date,
                }
            )

        # Format response with bars
        formatted_bars = []
        for bar in bars_data:
            formatted_bars.append(_format_tradier_history_bar(bar))

        return json.dumps(
            {
                "ticker": ticker,
                "interval": interval,
                "start_date": start_date,
                "end_date": end_date,
                "bars": formatted_bars,
                "count": len(formatted_bars),
                "source": "Tradier",
            },
            indent=2,
        )

    except requests.exceptions.Timeout:
        return json.dumps(
            {
                "error": "Timeout",
                "message": f"Tradier API request timed out for {ticker}",
                "ticker": ticker,
            }
        )
    except requests.exceptions.RequestException as e:
        return json.dumps(
            {
                "error": "Network error",
                "message": f"Failed to connect to Tradier API: {str(e)}",
                "ticker": ticker,
            }
        )
    except Exception as e:
        return json.dumps(
            {
                "error": "Unexpected error",
                "message": f"Failed to retrieve historical data for {ticker}: {str(e)}",
                "ticker": ticker,
            }
        )


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


@function_tool
async def get_call_options_chain(
    ticker: str, current_price: float, expiration_date: str
) -> str:
    """Get Call Options Chain with 10 strike prices above current underlying price.

    Use this tool when the user requests call options data for a specific ticker
    and expiration date. Returns bid, ask, and greeks for 10 strikes above current price.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA").
                Must be a valid ticker symbol.
        current_price: Current underlying stock price (used for filtering strikes).
                       Get this from get_stock_quote first.
        expiration_date: Options expiration date in YYYY-MM-DD format.
                         Use get_options_expiration_dates to find valid dates.

    Returns:
        JSON string with options chain data formatted as markdown table:
        {
            "ticker": "SPY",
            "option_type": "call",
            "current_price": 671.16,
            "expiration_date": "2025-10-17",
            "options": [
                {
                    "strike": 672.00,
                    "bid": 1.04,
                    "ask": 1.10,
                    "delta": 0.38,
                    "gamma": 0.10,
                    "theta": -0.70,
                    "vega": 0.12,
                    "implied_volatility": 11.00,
                    "volume": 135391,
                    "open_interest": 16023
                },
                ...
            ],
            "count": 10,
            "source": "Tradier"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "ticker": "SYMBOL"
        }

    Note:
        - Returns 10 strikes with strike price >= current_price
        - Strikes sorted ascending (lowest to highest)
        - Filters full chain client-side to prevent context overload
        - Bid/Ask prices instead of single "Price" field
        - Implied volatility expressed as percentage
        - Requires greeks=true parameter for Tradier API

    Example:
        User: "Show me SPY call options chain for October 17"
        Agent: First calls get_stock_quote to get current price (e.g., 671.16)
        Agent: Then calls get_call_options_chain(ticker="SPY", current_price=671.16,
               expiration_date="2025-10-17")
    """
    try:
        # Validate inputs
        if not ticker or not ticker.strip():
            return json.dumps(
                {
                    "error": "Invalid ticker",
                    "message": "Ticker symbol cannot be empty",
                    "ticker": ticker,
                }
            )

        ticker = ticker.strip().upper()

        if current_price <= 0:
            return json.dumps(
                {
                    "error": "Invalid current price",
                    "message": f"Current price {current_price} must be positive",
                    "ticker": ticker,
                }
            )

        if not expiration_date:
            return json.dumps(
                {
                    "error": "Invalid expiration date",
                    "message": "Expiration date is required (YYYY-MM-DD format)",
                    "ticker": ticker,
                }
            )

        # Get API key
        api_key = _get_tradier_api_key()
        if not api_key:
            return json.dumps(
                {
                    "error": "Configuration error",
                    "message": "TRADIER_API_KEY not found in environment",
                    "ticker": ticker,
                }
            )

        # Build Tradier API request
        url = "https://api.tradier.com/v1/markets/options/chains"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        params = {
            "symbol": ticker,
            "expiration": expiration_date,
            "greeks": "true",  # Required for delta, gamma, theta, vega
        }

        # Make API request
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            return json.dumps(
                {
                    "error": "API request failed",
                    "message": f"Tradier API returned status {response.status_code}",
                    "ticker": ticker,
                }
            )

        # Parse response
        data = response.json()
        options_data = data.get("options", {})
        option_list = options_data.get("option", [])

        if not option_list:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No options data found for {ticker} expiring {expiration_date}",
                    "ticker": ticker,
                }
            )

        # Filter for CALL options with strike >= current_price
        call_options = [
            opt
            for opt in option_list
            if opt.get("option_type") == "call"
            and opt.get("strike", 0) >= current_price
        ]

        if not call_options:
            return json.dumps(
                {
                    "error": "No call options found",
                    "message": f"No call options found with strike >= {current_price}",
                    "ticker": ticker,
                }
            )

        # Sort by strike ascending and take first 10
        call_options.sort(key=lambda x: x.get("strike", 0))
        call_options = call_options[:10]

        # Format options data
        formatted_options = []
        for opt in call_options:
            strike = opt.get("strike", 0)
            bid = opt.get("bid", 0)
            ask = opt.get("ask", 0)

            greeks = opt.get("greeks", {})
            delta = greeks.get("delta", 0)
            gamma = greeks.get("gamma", 0)
            theta = greeks.get("theta", 0)
            vega = greeks.get("vega", 0)
            implied_vol = greeks.get("smv_vol", 0) * 100  # Convert to percentage

            volume = opt.get("volume", 0) or 0  # Handle None
            open_interest = opt.get("open_interest", 0) or 0  # Handle None

            formatted_options.append(
                {
                    "strike": round(strike, 2),
                    "bid": round(bid, 2),
                    "ask": round(ask, 2),
                    "delta": round(delta, 2),
                    "gamma": round(gamma, 2),
                    "theta": round(theta, 2),
                    "vega": round(vega, 2),
                    "implied_volatility": round(implied_vol, 2),
                    "volume": volume,
                    "open_interest": open_interest,
                }
            )

        return json.dumps(
            {
                "ticker": ticker,
                "option_type": "call",
                "current_price": current_price,
                "expiration_date": expiration_date,
                "options": formatted_options,
                "count": len(formatted_options),
                "source": "Tradier",
            },
            indent=2,
        )

    except requests.exceptions.Timeout:
        return json.dumps(
            {
                "error": "Timeout",
                "message": f"Tradier API request timed out for {ticker}",
                "ticker": ticker,
            }
        )
    except requests.exceptions.RequestException as e:
        return json.dumps(
            {
                "error": "Network error",
                "message": f"Failed to connect to Tradier API: {str(e)}",
                "ticker": ticker,
            }
        )
    except Exception as e:
        return json.dumps(
            {
                "error": "Unexpected error",
                "message": f"Failed to retrieve call options chain for {ticker}: {str(e)}",
                "ticker": ticker,
            }
        )


@function_tool
async def get_put_options_chain(
    ticker: str, current_price: float, expiration_date: str
) -> str:
    """Get Put Options Chain with 10 strike prices below current underlying price.

    Use this tool when the user requests put options data for a specific ticker
    and expiration date. Returns bid, ask, and greeks for 10 strikes below current price.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA").
                Must be a valid ticker symbol.
        current_price: Current underlying stock price (used for filtering strikes).
                       Get this from get_stock_quote first.
        expiration_date: Options expiration date in YYYY-MM-DD format.
                         Use get_options_expiration_dates to find valid dates.

    Returns:
        JSON string with options chain data formatted as markdown table:
        {
            "ticker": "SPY",
            "option_type": "put",
            "current_price": 671.16,
            "expiration_date": "2025-10-17",
            "options": [
                {
                    "strike": 671.00,
                    "bid": 1.34,
                    "ask": 1.40,
                    "delta": -0.54,
                    "gamma": 0.14,
                    "theta": -0.51,
                    "vega": 0.15,
                    "implied_volatility": 8.00,
                    "volume": 109250,
                    "open_interest": 13803
                },
                ...
            ],
            "count": 10,
            "source": "Tradier"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "ticker": "SYMBOL"
        }

    Note:
        - Returns 10 strikes with strike price <= current_price
        - Strikes sorted descending (highest to lowest)
        - Filters full chain client-side to prevent context overload
        - Bid/Ask prices instead of single "Price" field
        - Implied volatility expressed as percentage
        - Requires greeks=true parameter for Tradier API

    Example:
        User: "Show me SPY put options chain for October 17"
        Agent: First calls get_stock_quote to get current price (e.g., 671.16)
        Agent: Then calls get_put_options_chain(ticker="SPY", current_price=671.16,
               expiration_date="2025-10-17")
    """
    try:
        # Validate inputs
        if not ticker or not ticker.strip():
            return json.dumps(
                {
                    "error": "Invalid ticker",
                    "message": "Ticker symbol cannot be empty",
                    "ticker": ticker,
                }
            )

        ticker = ticker.strip().upper()

        if current_price <= 0:
            return json.dumps(
                {
                    "error": "Invalid current price",
                    "message": f"Current price {current_price} must be positive",
                    "ticker": ticker,
                }
            )

        if not expiration_date:
            return json.dumps(
                {
                    "error": "Invalid expiration date",
                    "message": "Expiration date is required (YYYY-MM-DD format)",
                    "ticker": ticker,
                }
            )

        # Get API key
        api_key = _get_tradier_api_key()
        if not api_key:
            return json.dumps(
                {
                    "error": "Configuration error",
                    "message": "TRADIER_API_KEY not found in environment",
                    "ticker": ticker,
                }
            )

        # Build Tradier API request
        url = "https://api.tradier.com/v1/markets/options/chains"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        params = {
            "symbol": ticker,
            "expiration": expiration_date,
            "greeks": "true",  # Required for delta, gamma, theta, vega
        }

        # Make API request
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            return json.dumps(
                {
                    "error": "API request failed",
                    "message": f"Tradier API returned status {response.status_code}",
                    "ticker": ticker,
                }
            )

        # Parse response
        data = response.json()
        options_data = data.get("options", {})
        option_list = options_data.get("option", [])

        if not option_list:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No options data found for {ticker} expiring {expiration_date}",
                    "ticker": ticker,
                }
            )

        # Filter for PUT options with strike <= current_price
        put_options = [
            opt
            for opt in option_list
            if opt.get("option_type") == "put" and opt.get("strike", 0) <= current_price
        ]

        if not put_options:
            return json.dumps(
                {
                    "error": "No put options found",
                    "message": f"No put options found with strike <= {current_price}",
                    "ticker": ticker,
                }
            )

        # Sort by strike DESCENDING (highest to lowest for puts) and take first 10
        put_options.sort(key=lambda x: x.get("strike", 0), reverse=True)
        put_options = put_options[:10]

        # Format options data
        formatted_options = []
        for opt in put_options:
            strike = opt.get("strike", 0)
            bid = opt.get("bid", 0)
            ask = opt.get("ask", 0)

            greeks = opt.get("greeks", {})
            delta = greeks.get("delta", 0)
            gamma = greeks.get("gamma", 0)
            theta = greeks.get("theta", 0)
            vega = greeks.get("vega", 0)
            implied_vol = greeks.get("smv_vol", 0) * 100  # Convert to percentage

            volume = opt.get("volume", 0) or 0  # Handle None
            open_interest = opt.get("open_interest", 0) or 0  # Handle None

            formatted_options.append(
                {
                    "strike": round(strike, 2),
                    "bid": round(bid, 2),
                    "ask": round(ask, 2),
                    "delta": round(delta, 2),
                    "gamma": round(gamma, 2),
                    "theta": round(theta, 2),
                    "vega": round(vega, 2),
                    "implied_volatility": round(implied_vol, 2),
                    "volume": volume,
                    "open_interest": open_interest,
                }
            )

        return json.dumps(
            {
                "ticker": ticker,
                "option_type": "put",
                "current_price": current_price,
                "expiration_date": expiration_date,
                "options": formatted_options,
                "count": len(formatted_options),
                "source": "Tradier",
            },
            indent=2,
        )

    except requests.exceptions.Timeout:
        return json.dumps(
            {
                "error": "Timeout",
                "message": f"Tradier API request timed out for {ticker}",
                "ticker": ticker,
            }
        )
    except requests.exceptions.RequestException as e:
        return json.dumps(
            {
                "error": "Network error",
                "message": f"Failed to connect to Tradier API: {str(e)}",
                "ticker": ticker,
            }
        )
    except Exception as e:
        return json.dumps(
            {
                "error": "Unexpected error",
                "message": f"Failed to retrieve put options chain for {ticker}: {str(e)}",
                "ticker": ticker,
            }
        )
