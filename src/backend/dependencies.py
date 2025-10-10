"""Shared dependencies for the Market Parser application."""

from typing import Optional

from agents import Agent, SQLiteSession

# Global shared resources - will be set by main module
_shared_session: Optional[SQLiteSession] = None
_shared_agent: Optional[Agent] = None


def set_shared_resources(session: SQLiteSession, agent: Agent):
    """Set the shared resources for dependency injection.

    Args:
        session: The SQLite session for conversation memory
        agent: The persistent agent instance
    """
    global _shared_session, _shared_agent
    _shared_session = session
    _shared_agent = agent


def get_session() -> Optional[SQLiteSession]:
    """Get shared session instance.

    Returns:
        SQLiteSession instance or None if not set
    """
    return _shared_session


def get_agent() -> Agent:
    """Get shared agent instance.

    Returns:
        Agent: The persistent agent instance

    Raises:
        RuntimeError: If agent not initialized
    """
    if _shared_agent is None:
        raise RuntimeError("Shared agent not initialized")
    return _shared_agent
