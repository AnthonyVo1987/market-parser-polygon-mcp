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


# ============================================================================
# Phase 1: Connection Pooling Infrastructure (October 19, 2025)
# ============================================================================

import aiohttp
from typing import Optional


class APIConnectionPool:
    """
    Singleton connection pool for API requests.

    Provides persistent HTTP sessions with connection pooling for:
    - Polygon.io API
    - Tradier API
    - Other external APIs
    """

    _instance: Optional['APIConnectionPool'] = None

    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize connection pool if not already done."""
        if self._initialized:
            return

        # Create aiohttp session with connection pooling
        self.session: Optional[aiohttp.ClientSession] = None
        self._initialized = True

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session with connection pooling.

        Returns:
            aiohttp.ClientSession: HTTP session with connection pooling configured

        Configuration:
            - limit=100: Max 100 concurrent connections
            - limit_per_host=10: Max 10 connections per host
            - ttl_dns_cache=300: Cache DNS entries for 5 minutes
            - timeout=30s: Overall request timeout
        """
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    limit=100,          # Max 100 concurrent connections
                    limit_per_host=10,  # Max 10 per host
                    ttl_dns_cache=300,  # Cache DNS for 5 minutes
                ),
                timeout=aiohttp.ClientTimeout(total=30),  # 30s timeout
            )
        return self.session

    async def close(self):
        """Close HTTP session and cleanup resources."""
        if self.session and not self.session.closed:
            await self.session.close()


# Singleton instance
_connection_pool: Optional[APIConnectionPool] = None


def get_connection_pool() -> APIConnectionPool:
    """Get singleton connection pool instance.

    Returns:
        APIConnectionPool: The global connection pool singleton

    Usage:
        pool = get_connection_pool()
        session = await pool.get_session()
        async with session.get(url) as response:
            data = await response.json()
    """
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = APIConnectionPool()
    return _connection_pool
