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
