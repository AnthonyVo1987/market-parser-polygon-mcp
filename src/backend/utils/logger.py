"""
Minimal logging utility for Market Parser backend.

Provides essential error logging only for performance optimization.
"""

import logging
import os
from typing import Optional


def get_logger(name: str) -> logging.Logger:
    """
    Get a minimal logger instance for error logging only.

    Args:
        name: Usually __name__ from the calling module

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if not logger.handlers:
        # Only log errors and critical issues for performance
        logger.setLevel(logging.ERROR)

        # Simple console handler for errors only
        handler = logging.StreamHandler()
        handler.setLevel(logging.ERROR)

        # Simple format without colors or complex formatting
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Prevent propagation to avoid duplicate logs
        logger.propagate = False

    return logger


# Minimal helper functions for backward compatibility
def log_api_request(logger, method: str, endpoint: str, user_message: Optional[str] = None, request_id: Optional[str] = None):
    """Minimal API request logging - errors only."""
    pass  # No-op for performance


def log_api_response(logger, status_code: int, response_time: float, token_count: Optional[int] = None, request_id: Optional[str] = None):
    """Minimal API response logging - errors only."""
    if status_code >= 400:
        logger.error(f"API Error: {status_code} in {response_time:.3f}s")


def log_mcp_operation(logger, operation: str, duration: float, success: bool, error_message: Optional[str] = None):
    """Minimal MCP operation logging - errors only."""
    if not success:
        logger.error(f"MCP Operation failed: {operation} - {error_message}")


def log_agent_processing(logger, step: str, details=None):
    """Minimal agent processing logging - errors only."""
    pass  # No-op for performance