"""
Finnhub custom tools for OpenAI AI Agent.
Provides real-time stock quote data via Finnhub API.
"""

import json
import os

import finnhub
from agents import function_tool


def _get_finnhub_client():
    """Get Finnhub client with API key from environment.

    Lazy initialization ensures .env is loaded before accessing API key.
    """
    api_key = os.getenv("FINNHUB_API_KEY")
    return finnhub.Client(api_key=api_key)


@function_tool
async def get_stock_quote(ticker: str) -> str:
    """Get real-time stock quote from Finnhub API.

    Use this tool when the user requests a stock quote, current price,
    or real-time market data for a single ticker symbol.

    This tool provides real-time price data via Finnhub API,
    replacing the Polygon.io get_snapshot_ticker tool.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "TSLA", "NVDA").
                Must be a valid ticker from major US exchanges.

    Returns:
        JSON string containing quote data with format:
        {
            "ticker": "AAPL",
            "current_price": 178.50,
            "change": 2.30,
            "percent_change": 1.31,
            "high": 179.20,
            "low": 176.80,
            "open": 177.00,
            "previous_close": 176.20,
            "source": "Finnhub"
        }

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
        - Rate limits apply based on Finnhub API tier

    Examples:
        - "Get AAPL stock quote"
        - "What's the current price of TSLA?"
        - "NVDA quote"
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

        # Call Finnhub API with lazy client initialization
        client = _get_finnhub_client()
        quote_data = client.quote(ticker)

        # Check if API returned valid data
        if not quote_data or quote_data.get("c") == 0:
            return json.dumps(
                {
                    "error": "No data",
                    "message": f"No quote data available for ticker: {ticker}. Verify ticker symbol is valid.",
                    "ticker": ticker,
                }
            )

        # Format response
        return json.dumps(
            {
                "ticker": ticker,
                "current_price": round(quote_data.get("c", 0), 2),
                "change": round(quote_data.get("d", 0), 2),
                "percent_change": round(quote_data.get("dp", 0), 2),
                "high": round(quote_data.get("h", 0), 2),
                "low": round(quote_data.get("l", 0), 2),
                "open": round(quote_data.get("o", 0), 2),
                "previous_close": round(quote_data.get("pc", 0), 2),
                "source": "Finnhub",
            }
        )

    except Exception as e:
        # Handle unexpected errors
        return json.dumps(
            {
                "error": "API request failed",
                "message": f"Failed to retrieve quote for {ticker}: {str(e)}",
                "ticker": ticker,
            }
        )
