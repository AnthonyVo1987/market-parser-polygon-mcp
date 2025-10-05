"""
OpenAI GPT-5 Financial Analyst SDK with Polygon.io MCP Integration

This package provides a comprehensive financial analysis system using OpenAI GPT-5,
Pydantic AI Agent Framework, and Polygon.io MCP server for real-time market data.

Key Features:
- CLI and FastAPI web interface for financial queries
- Emoji-based sentiment indicators and enhanced formatting
- Dual-mode response processing (JSON/conversational)
- Real-time market data via Polygon.io MCP server
- Comprehensive prompt template system for various analysis types
- Response formatting instructions optimized for natural language
- Removal of JSON schema dependencies for simplified architecture
"""

# Handle optional imports gracefully for development/testing environments
try:
    from .main import (  # FastAPI application instance; Core processing functions; CLI function; Response formatting utilities; Utility functions; Pydantic models for requests/responses
        ChatRequest,
        ChatResponse,
        FinanceOutput,
        app,
        cli_async,
        print_error,
        print_guardrail_error,
        print_response,
    )
except ImportError as e:
    # Development/testing environment - dependencies may not be installed
    import warnings

    warnings.warn(
        f"Main module imports failed: {e}. This is expected in development "
        "environments without full dependencies.",
        ImportWarning,
    )

try:
    from .api_models import (  # Core API models; System status models; Error handling models; Utility models
        APIErrorResponse,
        ChatMessage,
        ErrorDetail,
        FollowUpQuestionsResponse,
        SuccessResponse,
        SystemHealthResponse,
        SystemMetrics,
        SystemStatusResponse,
        ValidationErrorResponse,
    )
except ImportError as e:
    # API models module may have dependency issues
    import warnings

    warnings.warn(
        f"API models imports failed: {e}. Some features may not be available.", ImportWarning
    )

# Prompt templates module removed as part of direct prompt migration

# Package metadata
__version__ = "1.0.0"
__author__ = "Market Parser Team"
__description__ = "OpenAI GPT-5 Financial Analyst SDK with Polygon.io MCP Integration"

# Main exports for easy importing
__all__ = [
    # FastAPI app
    "app",
    # Core functions
    "cli_async",
    # Response utilities
    "print_response",
    "print_error",
    "print_guardrail_error",
    # Utility functions
    # Main models
    "FinanceOutput",
    "ChatRequest",
    "ChatResponse",
    # System monitoring
    "SystemHealthResponse",
    "SystemStatusResponse",
    "SystemMetrics",
    # Error handling
    "ErrorDetail",
    "APIErrorResponse",
    "ValidationErrorResponse",
    # Utility models
    "FollowUpQuestionsResponse",
    "SuccessResponse",
]
