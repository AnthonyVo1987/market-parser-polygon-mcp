"""Shared dependencies for the Market Parser application."""

from typing import Optional

from agents import SQLiteSession

# Global shared resources - will be set by main module
_shared_session: Optional[SQLiteSession] = None


def set_shared_resources(session: SQLiteSession):
    """Set the shared resources for dependency injection."""
    global _shared_session
    _shared_session = session


def get_session() -> Optional[SQLiteSession]:
    """Get shared session instance.

    Returns:
        SQLiteSession instance or None if not set
    """
    return _shared_session
