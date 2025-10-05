"""
Polygon.io custom tools for OpenAI AI Agent.
Provides direct Polygon Python Library API access for market status and datetime.
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
