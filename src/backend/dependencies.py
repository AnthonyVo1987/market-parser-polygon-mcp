"""Shared dependencies for the Market Parser application."""

from typing import Optional

from agents import SQLiteSession
from agents.mcp import MCPServerStdio

# Global shared resources - will be set by main module
_shared_mcp_server: Optional[MCPServerStdio] = None
_shared_session: Optional[SQLiteSession] = None


def set_shared_resources(mcp_server: MCPServerStdio, session: SQLiteSession):
    """Set the shared resources for dependency injection."""
    global _shared_mcp_server, _shared_session
    _shared_mcp_server = mcp_server
    _shared_session = session


def get_mcp_server() -> Optional[MCPServerStdio]:
    """Get shared MCP server instance.

    Returns:
        MCPServerStdio instance or None if not set
    """
    return _shared_mcp_server


def get_session() -> Optional[SQLiteSession]:
    """Get shared session instance.

    Returns:
        SQLiteSession instance or None if not set
    """
    return _shared_session
