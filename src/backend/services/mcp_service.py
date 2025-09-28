"""MCP server management for the Market Parser application."""

import os

from agents.mcp import MCPServerStdio

from ..config import settings


def create_polygon_mcp_server():
    """Create a stdio MCP server instance configured with POLYGON_API_KEY."""
    if not settings.polygon_api_key:
        raise ValueError("POLYGON_API_KEY not set in environment.")

    return MCPServerStdio(
        params={
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/polygon-io/mcp_polygon@v0.4.1",
                "mcp_polygon",
            ],
            "env": {**os.environ, "POLYGON_API_KEY": settings.polygon_api_key},
        },
        client_session_timeout_seconds=settings.mcp_timeout_seconds,
    )