"""
Centralized logging utility for Market Parser backend.

Provides structured logging for FastAPI application with different log levels,
colored console output, and environment-specific configuration.

Usage:
    from src.backend.utils.logger import get_logger

    logger = get_logger(__name__)
    logger.info("API request received", extra={"endpoint": "/chat", "method": "POST"})
    logger.debug("MCP server response", extra={"response_time": 0.5, "tokens": 150})
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels."""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            colored_levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            record.levelname = colored_levelname

        # Format the message
        formatted = super().format(record)

        # Reset levelname to avoid issues with subsequent formatters
        record.levelname = levelname

        return formatted


class DebugFilter(logging.Filter):
    """Filter to add debug context information."""

    def filter(self, record: logging.LogRecord) -> bool:
        # Add timestamp for debugging
        record.debug_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        return True


def setup_logging(
    level: str = "INFO", log_to_file: bool = False, log_file_path: Optional[str] = None
) -> None:
    """
    Configure the logging system with colored console output.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to also log to a file
        log_file_path: Path to log file (defaults to logs/backend.log)
    """
    # Check for NONE mode first - completely disable logging
    log_mode = os.getenv("LOG_MODE", "").upper()
    if log_mode == "NONE":
        # Set logging to CRITICAL level to disable all lower-level logs
        # and skip all handler initialization for maximum performance
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.CRITICAL)
        # Remove any existing handlers to ensure no file I/O occurs
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        return
    
    # Get log level from environment or parameter
    log_level = os.getenv("LOG_LEVEL", level).upper()

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Remove existing handlers to avoid duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level, logging.INFO))

    # Format with colors and extra context
    console_format = "🔍 %(debug_timestamp)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
    if hasattr(logging, "_structlog_style"):
        console_format += " %(extra_data)s"

    console_formatter = ColoredFormatter(console_format)
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(DebugFilter())

    root_logger.addHandler(console_handler)

    # File handler (optional) - skip in NONE mode
    if log_to_file:
        if not log_file_path:
            os.makedirs("logs", exist_ok=True)
            log_file_path = "logs/backend.log"

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)  # Always log everything to file

        file_format = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
        file_formatter = logging.Formatter(file_format)
        file_handler.setFormatter(file_formatter)
        file_handler.addFilter(DebugFilter())

        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given module name.

    Args:
        name: Usually __name__ from the calling module

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_api_request(
    logger: logging.Logger,
    method: str,
    endpoint: str,
    user_message: Optional[str] = None,
    request_id: Optional[str] = None,
) -> None:
    """
    Log API request with structured data.

    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        user_message: User message (truncated for logging)
        request_id: Unique request identifier
    """
    extra_data = {"method": method, "endpoint": endpoint, "request_id": request_id}

    if user_message:
        # Truncate long messages for logging
        truncated_message = user_message[:100] + "..." if len(user_message) > 100 else user_message
        extra_data["user_message"] = truncated_message

    logger.info(f"🌐 API Request: {method} {endpoint}", extra=extra_data)


def log_api_response(
    logger: logging.Logger,
    status_code: int,
    response_time: float,
    token_count: Optional[int] = None,
    request_id: Optional[str] = None,
) -> None:
    """
    Log API response with performance metrics.

    Args:
        logger: Logger instance
        status_code: HTTP status code
        response_time: Response time in seconds
        token_count: Number of tokens used
        request_id: Unique request identifier
    """
    extra_data = {
        "status_code": status_code,
        "response_time": f"{response_time:.3f}s",
        "request_id": request_id,
    }

    if token_count:
        extra_data["tokens"] = token_count

    # Choose emoji based on status code
    if status_code < 300:
        emoji = "✅"
        level = logging.INFO
    elif status_code < 400:
        emoji = "⚠️"
        level = logging.WARNING
    else:
        emoji = "❌"
        level = logging.ERROR

    logger.log(
        level, f"{emoji} API Response: {status_code} in {response_time:.3f}s", extra=extra_data
    )


def log_mcp_operation(
    logger: logging.Logger,
    operation: str,
    duration: float,
    success: bool,
    error_message: Optional[str] = None,
) -> None:
    """
    Log MCP server operations with timing and status.

    Args:
        logger: Logger instance
        operation: MCP operation name
        duration: Operation duration in seconds
        success: Whether operation succeeded
        error_message: Error message if operation failed
    """
    extra_data = {"operation": operation, "duration": f"{duration:.3f}s", "success": success}

    if success:
        logger.info(f"🔌 MCP Operation: {operation} completed in {duration:.3f}s", extra=extra_data)
    else:
        extra_data["error"] = error_message
        logger.error(
            f"💥 MCP Operation: {operation} failed after {duration:.3f}s - {error_message}",
            extra=extra_data,
        )


def log_agent_processing(
    logger: logging.Logger, step: str, details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log agent processing steps for debugging.

    Args:
        logger: Logger instance
        step: Processing step description
        details: Additional details dictionary
    """
    # Skip expensive operations if debug logging is disabled
    if not logger.isEnabledFor(logging.DEBUG):
        return

    extra_data = {"step": step}
    if details:
        extra_data.update(details)

    logger.debug(f"🤖 Agent Processing: {step}", extra=extra_data)


# Initialize logging on module import based on environment
def _initialize_logging():
    """Initialize logging configuration on module import."""
    # Check for NONE mode first - if set, skip all logging setup
    log_mode = os.getenv("LOG_MODE", "").upper()
    if log_mode == "NONE":
        setup_logging()  # Will handle NONE mode internally
        return
    
    # Determine environment mode
    environment = os.getenv("ENVIRONMENT", "development").lower()
    debug_mode = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    # Set appropriate log levels based on environment
    if environment == "production":
        log_level = "WARNING"  # Only warnings and errors in production
    elif debug_mode or environment == "development":
        log_level = "DEBUG"    # Full debugging in development
    else:
        log_level = "INFO"     # Standard info level

    # Enable file logging in development for debugging
    log_to_file = debug_mode or os.getenv("LOG_TO_FILE", "false").lower() in ("true", "1", "yes")

    setup_logging(level=log_level, log_to_file=log_to_file)


# Auto-initialize logging when module is imported
_initialize_logging()
