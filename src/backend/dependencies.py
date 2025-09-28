"""Shared dependencies for the Market Parser application."""

from typing import Dict, Optional

from agents import SQLiteSession
from agents.mcp import MCPServerStdio

from .config import settings

# Global shared resources - will be set by main module
_shared_mcp_server: Optional[MCPServerStdio] = None
_shared_session: Optional[SQLiteSession] = None


def set_shared_resources(mcp_server: MCPServerStdio, session: SQLiteSession):
    """Set the shared resources for dependency injection."""
    global _shared_mcp_server, _shared_session
    _shared_mcp_server = mcp_server
    _shared_session = session


def get_model_rate_limits(model: str) -> Dict[str, int]:
    """Get rate limits for specific GPT-5 models.
    
    Args:
        model: The model name to get rate limits for
        
    Returns:
        Dictionary containing TPM and RPM limits
    """
    if model == "gpt-5-nano":
        return {"tpm": settings.gpt5_nano_tpm, "rpm": settings.gpt5_nano_rpm}
    if model == "gpt-5-mini":
        return {"tpm": settings.gpt5_mini_tpm, "rpm": settings.gpt5_mini_rpm}
    return {"tpm": settings.gpt5_nano_tpm, "rpm": settings.gpt5_nano_rpm}  # Default fallback


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