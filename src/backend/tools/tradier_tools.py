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
        interval: Time interval - "daily", "weekly", or "monthly" (default: "daily").

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
