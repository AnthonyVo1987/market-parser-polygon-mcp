"""Error Response Utility Module.

This module provides standardized error response formatting for all tools.
Implements the DRY (Don't Repeat Yourself) principle by centralizing error
response creation logic that was previously duplicated 43 times across the codebase.

Created: October 18, 2025
Part of: Code Cleanup & Refactoring Phase 2
"""

import json
from typing import Any


def create_error_response(error_type: str, message: str, **extra_fields: Any) -> str:
    """Create standardized JSON error response.

    This function provides a single source of truth for error response formatting,
    replacing 43 duplicate instances across tradier_tools.py and polygon_tools.py.

    Args:
        error_type: Type of error (e.g., "Invalid ticker", "API request failed", "Timeout")
        message: Descriptive error message explaining what went wrong
        **extra_fields: Additional fields to include in the response (e.g., ticker, interval, date)

    Returns:
        JSON string with standardized error response format

    Examples:
        >>> create_error_response("Invalid ticker", "Ticker symbol cannot be empty", ticker="")
        '{"error": "Invalid ticker", "message": "Ticker symbol cannot be empty", "ticker": ""}'

        >>> create_error_response("Timeout", "Request timed out after 10s", ticker="SPY", timeout=10)
        '{"error": "Timeout", "message": "Request timed out after 10s", "ticker": "SPY", "timeout": 10}'

        >>> create_error_response("No data", "No options found for expiration", ticker="AAPL", date="2025-10-20")
        '{"error": "No data", "message": "No options found for expiration", "ticker": "AAPL", "date": "2025-10-20"}'

    Common Error Types:
        - "Invalid ticker": Ticker validation failed
        - "Configuration error": Missing API keys or config
        - "API request failed": HTTP request error
        - "Timeout": Request exceeded time limit
        - "Network error": Connection/network issues
        - "Unexpected error": Uncaught exceptions
        - "No data": API returned no data
        - "Invalid current price": Price validation failed
        - "Invalid expiration date": Date format/logic error
        - "Invalid interval": Interval parameter error
        - "Invalid dates": Date range error
        - "No call/put options found": Options chain empty
    """
    response = {
        "error": error_type,
        "message": message,
        **extra_fields
    }
    return json.dumps(response)
