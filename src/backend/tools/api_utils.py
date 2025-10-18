"""API Request Utility Module.

This module provides standardized API request utilities for external data sources.
Implements the DRY (Don't Repeat Yourself) principle by centralizing API header
generation that was previously duplicated 6 times across tool files.

Created: October 18, 2025
Part of: Code Cleanup & Refactoring Phase 2
"""

# API Request Timeout Constants (seconds)
TRADIER_TIMEOUT = 10
POLYGON_TIMEOUT = 10
DEFAULT_TIMEOUT = 10


def create_tradier_headers(api_key: str) -> dict:
    """Create standard Tradier API request headers.

    This function provides a single source of truth for Tradier header generation,
    replacing 5 duplicate header dict constructions across tradier_tools.py.

    Args:
        api_key: Tradier API key for authorization

    Returns:
        Dictionary with Accept and Authorization headers for Tradier API requests

    Examples:
        >>> create_tradier_headers("test_key_12345")
        {'Accept': 'application/json', 'Authorization': 'Bearer test_key_12345'}

    Usage Pattern:
        ```python
        headers = create_tradier_headers(api_key)
        response = requests.get(url, headers=headers, params=params, timeout=TRADIER_TIMEOUT)
        ```
    """
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
