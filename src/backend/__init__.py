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
        create_polygon_mcp_server,
        finance_guardrail,
        print_error,
        print_guardrail_error,
        print_response,
        process_financial_query,
        save_analysis_report,
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
    from .api_models import (  # Enums; Core API models; Template management models; System status models; Error handling models; Utility models
        AnalysisType,
        AnalysisTypeDetectionRequest,
        AnalysisTypeDetectionResponse,
        APIErrorResponse,
        ButtonAnalysisRequest,
        ButtonAnalysisResponse,
        ChatAnalysisRequest,
        ChatAnalysisResponse,
        ChatMessage,
        ErrorDetail,
        FollowUpQuestionsResponse,
        GeneratePromptRequest,
        GeneratePromptResponse,
        PromptMode,
        PromptTemplateInfo,
        SuccessResponse,
        SystemHealthResponse,
        SystemMetrics,
        SystemStatusResponse,
        TemplateListResponse,
        TickerContextInfo,
        TickerExtractionRequest,
        TickerExtractionResponse,
        ValidationErrorResponse,
    )
except ImportError as e:
    # API models module may have dependency issues
    import warnings

    warnings.warn(
        f"API models imports failed: {e}. Some features may not be available.", ImportWarning
    )

try:
    from .prompt_templates import (  # Core classes; Enums; Utility functions
        PromptTemplate,
        PromptTemplateManager,
        PromptType,
        TickerContext,
        TickerExtractor,
        run_prompt_consistency_tests,
        test_dual_mode_behavior,
        validate_template_parsing_compatibility,
    )
except ImportError as e:
    # Prompt templates module may have dependency issues
    import warnings

    warnings.warn(
        f"Prompt templates imports failed: {e}. Template features may not be available.",
        ImportWarning,
    )

# Package metadata
__version__ = "1.0.0"
__author__ = "Market Parser Team"
__description__ = "OpenAI GPT-5 Financial Analyst SDK with Polygon.io MCP Integration"

# Main exports for easy importing
__all__ = [
    # FastAPI app
    "app",
    # Core functions
    "process_financial_query",
    "create_polygon_mcp_server",
    "cli_async",
    # Response utilities
    "print_response",
    "print_error",
    "print_guardrail_error",
    # Utility functions
    "save_analysis_report",
    "finance_guardrail",
    # Main models
    "FinanceOutput",
    "ChatRequest",
    "ChatResponse",
    # Analysis types
    "AnalysisType",
    "PromptMode",
    "PromptType",
    # API models
    "ChatMessage",
    "ChatAnalysisRequest",
    "ChatAnalysisResponse",
    "ButtonAnalysisRequest",
    "ButtonAnalysisResponse",
    "GeneratePromptRequest",
    "GeneratePromptResponse",
    # Template management
    "PromptTemplateManager",
    "PromptTemplate",
    "TickerExtractor",
    "TickerContext",
    "PromptTemplateInfo",
    "TemplateListResponse",
    # System monitoring
    "SystemHealthResponse",
    "SystemStatusResponse",
    "SystemMetrics",
    # Error handling
    "ErrorDetail",
    "APIErrorResponse",
    "ValidationErrorResponse",
    # Utility models
    "TickerContextInfo",
    "FollowUpQuestionsResponse",
    "SuccessResponse",
    "AnalysisTypeDetectionRequest",
    "AnalysisTypeDetectionResponse",
    "TickerExtractionRequest",
    "TickerExtractionResponse",
    # Testing utilities
    "run_prompt_consistency_tests",
    "validate_template_parsing_compatibility",
    "test_dual_mode_behavior",
]
