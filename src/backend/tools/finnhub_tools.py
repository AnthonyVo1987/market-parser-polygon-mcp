"""
Tradier custom tools for OpenAI AI Agent.
Provides real-time stock quote data via Tradier API.
"""

import json
import os

import requests
from agents import function_tool


@function_tool
async def get_stock_quote(ticker: str) -> str:
    """Get real-time stock quote from Tradier API.

    Use this tool when the user requests a stock quote, current price,
    or real-time market data for one or more ticker symbols.

    This tool provides real-time price data via Tradier API,
    supporting both single and multiple ticker queries.

    Args:
        ticker: Stock ticker symbol(s). Can be:
                - Single ticker: "AAPL"
                - Multiple tickers: "AAPL,TSLA,NVDA" (comma-separated, no spaces)
                Must be valid ticker(s) from major US exchanges.

    Returns:
        JSON string containing quote data.
        
        For single ticker:
        {
            "ticker": "AAPL",
            "current_price": 178.50,
            "change": 2.30,
            "percent_change": 1.31,
            "high": 179.20,
            "low": 176.80,
            "open": 177.00,
            "previous_close": 176.20,
            "source": "Tradier"
        }

        For multiple tickers, returns array of quote objects.

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "ticker": "SYMBOL"
        }

    Note:
        - Supports major US stock exchanges (NYSE, NASDAQ, etc.)
        - Data updates in real-time during market hours
        - Returns last available price when market is closed
        - Handles up to 10 tickers per request for optimal performance

    Examples:
        - "Get AAPL stock quote"
        - "What's the current price of TSLA?"
        - "Get quotes for AAPL, TSLA, NVDA"
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

        # Get API key from environment
        api_key = os.getenv("TRADIER_API_KEY")
        if not api_key:
            return json.dumps(
                {
                    "error": "Configuration error",
                    "message": "TRADIER_API_KEY not configured in environment",
                    "ticker": ticker,
                }
            )

        # Build request to Tradier API
        url = "https://api.tradier.com/v1/markets/quotes"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        params = {"symbols": ticker}  # requests handles URL encoding

        # Make API request with timeout
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        quotes_data = data.get("quotes", {}).get("quote")

        # Check if API returned valid data
        if not quotes_data:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No quote data available for ticker: {ticker}. Verify ticker symbol is valid.",
                    "ticker": ticker,
                }
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

    except requests.exceptions.Timeout:
        return json.dumps(
            {
                "error": "Timeout",
                "message": f"Request timed out while fetching quote for {ticker}",
                "ticker": ticker,
            }
        )
    except requests.exceptions.RequestException as e:
        return json.dumps(
            {
                "error": "API request failed",
                "message": f"Tradier API request failed: {str(e)}",
                "ticker": ticker,
            }
        )
    except Exception as e:
        return json.dumps(
            {
                "error": "Unexpected error",
                "message": f"Failed to retrieve quote for {ticker}: {str(e)}",
                "ticker": ticker,
            }
        )


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
