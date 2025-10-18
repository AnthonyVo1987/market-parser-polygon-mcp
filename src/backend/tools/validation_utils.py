"""Input Validation Utility Module.

This module provides standardized input validation and sanitization for tool parameters.
Implements the DRY (Don't Repeat Yourself) principle by centralizing validation logic
that was previously duplicated 5 times across tradier_tools.py.

Created: October 18, 2025
Part of: Code Cleanup & Refactoring Phase 2
"""

from typing import Optional
from .error_utils import create_error_response


def validate_and_sanitize_ticker(ticker: str) -> tuple[str, Optional[str]]:
    """Validate and sanitize ticker symbol.

    This function provides a single source of truth for ticker validation,
    replacing 5 duplicate validation blocks across tradier_tools.py.

    Args:
        ticker: Raw ticker symbol input (may contain whitespace, mixed case)

    Returns:
        Tuple of (sanitized_ticker, error_response):
        - If validation passes: (ticker.strip().upper(), None)
        - If validation fails: ("", error_json_string)

    Examples:
        >>> validate_and_sanitize_ticker("spy")
        ('SPY', None)

        >>> validate_and_sanitize_ticker("  NVDA  ")
        ('NVDA', None)

        >>> validate_and_sanitize_ticker("")
        ('', '{"error": "Invalid ticker", "message": "Ticker symbol cannot be empty", "ticker": ""}')

        >>> validate_and_sanitize_ticker(None)
        ('', '{"error": "Invalid ticker", "message": "Ticker symbol cannot be empty", "ticker": null}')

    Usage Pattern:
        ```python
        ticker, error = validate_and_sanitize_ticker(ticker)
        if error:
            return error
        # Continue with validated ticker
        ```
    """
    if not ticker or not ticker.strip():
        return "", create_error_response(
            "Invalid ticker",
            "Ticker symbol cannot be empty",
            ticker=ticker
        )

    return ticker.strip().upper(), None
