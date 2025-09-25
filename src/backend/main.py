"""CLI financial analyst using OpenAI Agents SDK, GPT-5, and Polygon.io MCP server.

This script launches a stdio MCP server for Polygon.io tools, runs a single
analysis agent with an input guardrail to ensure finance-related prompts, and
renders only the agent's final output. Users can optionally save analyses as
Markdown reports in the `reports/` directory.
"""

import asyncio
import json
import os
import re
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from agents import (
    Agent,
    GuardrailFunctionOutput,
    Runner,
    SQLiteSession,
    function_tool,
)
from agents.mcp import MCPServerStdio
from cachetools import TTLCache
from dotenv import load_dotenv

# FastAPI imports
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from rich.console import Console
from rich.markdown import Markdown

try:
    # Try relative imports first (when run as module)
    from .api_models import (
        AIModel,
        AIModelId,
        ModelListResponse,
        ModelSelectionResponse,
        ResponseMetadata,
        SystemHealthResponse,
        SystemMetrics,
        SystemStatusResponse,
    )
    from .direct_prompts import DirectPromptManager
    from .utils.logger import (
        get_logger,
        log_api_request,
        log_api_response,
        log_mcp_operation,
    )
except ImportError:
    # Fallback to absolute imports (when run directly)
    from api_models import (
        AIModel,
        AIModelId,
        ModelListResponse,
        ModelSelectionResponse,
        ResponseMetadata,
        SystemHealthResponse,
        SystemMetrics,
        SystemStatusResponse,
    )
    from direct_prompts import DirectPromptManager
    from utils.logger import (
        get_logger,
        log_api_request,
        log_api_response,
        log_mcp_operation,
    )

load_dotenv()

console = Console()
logger = get_logger(__name__)


# ====== CONFIGURATION SETTINGS ======


class EnvironmentSettings(BaseSettings):
    """Environment-only settings for API keys."""

    # API Keys (from environment only)
    polygon_api_key: str
    openai_api_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


class ConfigSettings:
    """Configuration settings loaded from config/app.config.json."""

    def __init__(self):
        config_path = Path(__file__).parent.parent.parent / "config" / "app.config.json"
        with open(config_path, encoding="utf-8") as f:
            self.config = json.load(f)

        # Backend settings
        self.backend = self.config["backend"]
        self.frontend = self.config["frontend"]


class Settings:
    """Application configuration with JSON-based configuration."""

    def __init__(self):
        # Load environment settings for API keys
        env_settings = EnvironmentSettings()

        # Load configuration from JSON file
        config_settings = ConfigSettings()

        # Server configuration from config file
        self.fastapi_host: str = config_settings.backend["server"]["host"]
        self.fastapi_port: int = config_settings.backend["server"]["port"]

        # API Keys from environment
        self.polygon_api_key: str = env_settings.polygon_api_key
        self.openai_api_key: str = env_settings.openai_api_key

        # Application configuration from config file
        self.mcp_timeout_seconds: float = config_settings.backend["mcp"]["timeoutSeconds"]
        self.agent_session_name: str = config_settings.backend["agent"]["sessionName"]
        self.reports_directory: str = config_settings.backend["agent"]["reportsDirectory"]

        # CORS configuration from config file
        cors_origins_list = config_settings.backend["security"]["cors"]["origins"]
        self.cors_origins: str = ",".join(cors_origins_list)

        # Available models from config file
        self.available_models: List[str] = config_settings.backend["ai"]["availableModels"]

        # AI configuration from config file
        self.max_context_length: int = config_settings.backend["ai"]["maxContextLength"]
        self.temperature: float = config_settings.backend["ai"]["temperature"]
        self.ai_pricing: dict = config_settings.backend["ai"]["pricing"]

        # Security configuration from config file
        self.enable_rate_limiting: bool = config_settings.backend["security"]["enableRateLimiting"]
        self.rate_limit_rpm: int = config_settings.backend["security"]["rateLimitRPM"]

        # GPT-5 model-specific rate limiting from config file
        self.gpt5_nano_tpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Nano"]["tpm"]
        self.gpt5_nano_rpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Nano"]["rpm"]
        self.gpt5_mini_tpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Mini"]["tpm"]
        self.gpt5_mini_rpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Mini"]["rpm"]

        # Logging configuration from config file
        self.log_mode: str = config_settings.backend["logging"]["mode"]

        # MCP configuration from config file
        self.polygon_mcp_version: str = config_settings.backend["mcp"]["version"]

        # Frontend configuration from config file
        self.frontend_config = config_settings.frontend


# Initialize settings
settings = Settings()


def get_model_rate_limits(model: str) -> dict:
    """Get rate limits for specific GPT-5 models."""
    if model == "gpt-5-nano":
        return {"tpm": settings.gpt5_nano_tpm, "rpm": settings.gpt5_nano_rpm}
    elif model == "gpt-5-mini":
        return {"tpm": settings.gpt5_mini_tpm, "rpm": settings.gpt5_mini_rpm}
    else:
        return {"tpm": settings.gpt5_nano_tpm, "rpm": settings.gpt5_nano_rpm}  # Default fallback


def validate_request_size(request_tokens: int, model: str) -> bool:
    """Validate request size against model-specific TPM limits."""
    limits = get_model_rate_limits(model)
    return bool(request_tokens <= limits["tpm"])


def get_model_tpm_limit(model: str) -> int:
    """Get TPM limit for specific model."""
    limits = get_model_rate_limits(model)
    return int(limits["tpm"])

# Global shared resources for FastAPI lifespan management
shared_mcp_server = None
shared_session = None

# Secure response cache for financial queries with automatic size and TTL management
CACHE_TTL_SECONDS = 900  # 15 minutes in seconds
CACHE_MAX_SIZE = 1000  # Maximum number of cached responses
response_cache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS)

# Cache statistics for monitoring
cache_stats = {"hits": 0, "misses": 0, "evictions": 0, "current_size": 0}

# Request tracking for logging
active_requests: dict[str, dict] = {}


# Models
class FinanceOutput(BaseModel):
    """Structured result from the guardrail check."""

    is_about_finance: bool
    reasoning: str


# Legacy models for backward compatibility
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str
    model: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str
    success: bool = True
    error: Optional[str] = None
    metadata: Optional[ResponseMetadata] = None


@function_tool
async def save_analysis_report(
    content: str, title: Optional[str] = None, category: str = "general"
) -> str:
    """Persist a Markdown report to `reports/<timestamp>_<title>.md`."""
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    title = title or f"analysis_{timestamp}"
    safe_title = re.sub(r"[^\w\s-]", "", title).replace(" ", "_")
    filepath = reports_dir / f"{timestamp}_{safe_title}.md"

    content = f"""# {title}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Category:** {category}

---

{content}

---
*Report generated by Market Analysis Agent*
"""

    filepath.write_text(content, encoding="utf-8")
    return f"Report saved: {filepath}"


def get_current_datetime_context():
    """Generate current date/time context for AI agent prompts."""
    now = datetime.now()
    return f"""
CURRENT DATE AND TIME CONTEXT:
- Today's date: {now.strftime('%A, %B %d, %Y')}
- Current time: {now.strftime('%I:%M %p %Z')}
- ISO format: {now.strftime('%Y-%m-%d %H:%M:%S')}
- Market status: {'Open' if now.weekday() < 5 and 9 <= now.hour < 16 else 'Closed'}

IMPORTANT: Always use the current date and time above for all financial analysis. 
Do NOT use training data cutoff dates or outdated information.
"""


def get_enhanced_agent_instructions():
    """Generate enhanced agent instructions with current date/time context and tool awareness."""
    datetime_context = get_current_datetime_context()
    return f"""Quick Response Needed with minimal tool calls: You are a professional financial analyst with access to real-time market data tools.

{datetime_context}

TOOL AVAILABILITY:
You have access to the following real-time data tools:
- Polygon.io MCP server for live market data, stock prices, and financial information
- Real-time price quotes, market snapshots, and historical data
- Current market status and trading hours information
- Live financial news and market updates

INSTRUCTIONS:
1. ALWAYS use the current date and time provided above for all analysis
2. Use the available real-time data tools to gather current market information
3. Provide accurate, data-driven financial analysis and insights
4. Focus on actionable insights and clear explanations
5. When referencing dates, use the current date context provided above
6. Do NOT rely on training data cutoff dates or outdated information
7. RESPOND QUICKLY with minimal tool calls to improve response latency

Remember: You have access to real-time market data - use it to provide current, accurate analysis. Prioritize speed and efficiency in your responses."""


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="""Classify if the user query is finance-related.
    Include: stocks, ETFs, crypto, forex, market news, fundamentals, economic
    indicators, ROI calcs, corporate actions.
    Exclude: non-financial topics (cooking, general trivia, unrelated tech).
    Disambiguate: if term (e.g., Apple, Tesla) could be both, check for finance
    context words (price, market, earnings, shares). If unclear, return non-finance.
    Output: is_about_finance: bool, reasoning: brief why/why not.""",
    output_type=FinanceOutput,
    model=settings.available_models[0],
)

# Main financial analysis agent
finance_analysis_agent = Agent(
    name="Financial Analysis Agent",
    instructions=get_enhanced_agent_instructions(),
    tools=[save_analysis_report],
    model=settings.available_models[0],
)


async def finance_guardrail(context, agent, input_data):  # pylint: disable=unused-argument
    """Validate that the prompt is finance-related before running the agent."""
    result = await Runner.run(guardrail_agent, input_data, context=context)
    final_output = result.final_output_as(FinanceOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_about_finance,
    )


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




def generate_cache_key(query: str, ticker: str = "") -> str:
    """Generate a consistent cache key for financial queries.

    Optimized implementation without crypto overhead as recommended by security review.
    """
    return f"{query.lower().strip()}:{ticker.upper().strip()}"


def get_cached_response(cache_key: str) -> Optional[str]:
    """Get cached response if still valid with proper error handling."""
    global cache_stats

    try:
        if cache_key in response_cache:
            cache_stats["hits"] += 1
            cache_stats["current_size"] = len(response_cache)
            logger.info(f"Cache hit for key: {cache_key[:20]}...")
            return str(response_cache[cache_key])

        cache_stats["misses"] += 1
        cache_stats["current_size"] = len(response_cache)
        return None
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(f"Cache retrieval error: {e}")
        cache_stats["misses"] += 1
        return None


def cache_response(cache_key: str, response: str):
    """Cache a response with proper error handling and monitoring."""
    global cache_stats

    try:
        # Check if this will cause an eviction
        if len(response_cache) >= CACHE_MAX_SIZE and cache_key not in response_cache:
            cache_stats["evictions"] += 1

        response_cache[cache_key] = response
        cache_stats["current_size"] = len(response_cache)

        logger.info(f"Cached response for key: {cache_key[:20]}... (size: {len(response_cache)})")

    except MemoryError:
        logger.error("Cache memory exhausted - clearing cache")
        response_cache.clear()
        cache_stats["evictions"] += 1
        cache_stats["current_size"] = 0
        # Try caching again after clearing
        try:
            response_cache[cache_key] = response
            cache_stats["current_size"] = len(response_cache)
        except Exception as e:
            logger.error(f"Failed to cache response after cleanup: {e}")
    except Exception as e:
        logger.error(f"Cache storage error: {e}")


def invalidate_cache_by_ticker(ticker: str) -> int:
    """Invalidate all cache entries for a specific ticker."""
    global cache_stats

    try:
        ticker_upper = ticker.upper().strip()
        keys_to_remove = [key for key in response_cache.keys() if key.endswith(f":{ticker_upper}")]

        for key in keys_to_remove:
            try:
                del response_cache[key]
            except KeyError:
                pass  # Already removed by TTL

        cache_stats["current_size"] = len(response_cache)

        if keys_to_remove:
            logger.info(f"Invalidated {len(keys_to_remove)} cache entries for ticker {ticker}")

        return len(keys_to_remove)

    except Exception as e:
        logger.error(f"Cache invalidation error for ticker {ticker}: {e}")
        return 0


def clear_all_cache() -> int:
    """Clear all cache entries and return count of cleared items."""
    global cache_stats

    try:
        cleared_count = len(response_cache)
        response_cache.clear()
        cache_stats["current_size"] = 0
        cache_stats["evictions"] += cleared_count

        logger.info(f"Cleared all {cleared_count} cache entries")
        return cleared_count

    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return 0


def cleanup_session_periodically():
    """Clean up old session data to prevent memory leaks."""
    global shared_session

    if hasattr(shared_session, "_session_data"):
        # Keep only last 100 conversation turns to prevent memory growth
        session_data = getattr(shared_session, "_session_data", {})
        if isinstance(session_data, dict) and len(session_data) > 100:
            # Keep only the most recent entries
            sorted_keys = sorted(session_data.keys())
            keys_to_remove = sorted_keys[:-50]  # Keep last 50 entries

            for key in keys_to_remove:
                del session_data[key]

            logger.info(f"Cleaned up {len(keys_to_remove)} old session entries")


# Output functions
def print_response(result):
    """Simplified response renderer with emoji support."""
    console.print("\n[bold green]✔ Query processed successfully![/bold green]")
    console.print("[bold]Agent Response:[/bold]\n")

    # Extract content
    final_output = getattr(result, "final_output", result)
    final_text = str(final_output)

    # Check if content has markdown-like formatting
    has_markdown = any(tag in final_text for tag in ["#", "*", "`", "-", ">"])

    if has_markdown:
        # Use Markdown rendering for structured content
        console.print(Markdown(final_text))
    else:
        # Use direct printing with Rich markup for better emoji support
        console.print(final_text)

    # Enhanced separator with emoji
    console.print("\n[dim]" + "─" * 50 + "[/dim]\n")


def print_error(error, error_type="Error"):
    """Display errors in a consistent, readable format for the CLI."""
    console.print(f"\n[bold red]!!! {error_type} !!![/bold red]")
    console.print(str(error).strip())
    console.print("------------------\n")


def print_guardrail_error(exception):
    """Explain why a prompt was blocked by the finance guardrail."""
    console.print("\n[bold yellow]⚠ Guardrail Triggered[/bold yellow]")
    console.print("[yellow]This query is not related to finance.[/yellow]")
    if hasattr(exception, "output_info") and exception.output_info:
        console.print(f"[dim]Reasoning: {exception.output_info.reasoning}[/dim]")
    console.print(
        "[dim]Please ask about stock prices, market data, financial analysis, "
        "economic indicators, or company financials.[/dim]"
    )
    console.print("------------------\n")


# process_financial_query function removed as part of direct prompt migration


# Initialize direct prompt system
direct_prompt_manager = DirectPromptManager()


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):  # pylint: disable=unused-argument
    """FastAPI lifespan management for shared MCP server and session instances."""
    global shared_mcp_server, shared_session

    startup_start = time.time()
    logger.info(
        "🚀 FastAPI application startup initiated - host: %s, port: %s, model: %s, session: %s",
        settings.fastapi_host,
        settings.fastapi_port,
        settings.available_models[0],
        settings.agent_session_name,
    )

    # Startup: Create shared instances
    try:
        # Server initialization

        # Initialize session
        session_start = time.time()
        shared_session = SQLiteSession(settings.agent_session_name)
        session_time = time.time() - session_start
        logger.debug("📊 SQLite session initialized in %.3fs", session_time)

        # Initialize MCP server
        mcp_start = time.time()
        shared_mcp_server = create_polygon_mcp_server()
        await shared_mcp_server.__aenter__()  # pylint: disable=unnecessary-dunder-call
        mcp_time = time.time() - mcp_start
        log_mcp_operation(logger, "MCP server initialization", mcp_time, True)

        startup_time = time.time() - startup_start
        logger.info(
            "✅ FastAPI application startup completed in %.3fs - session: %.3fs, mcp: %.3fs",
            startup_time,
            session_time,
            mcp_time,
        )

        # Initialization complete
    except Exception as e:
        startup_time = time.time() - startup_start
        logger.error(
            "❌ FastAPI startup failed after %.3fs - error: %s (%s)",
            startup_time,
            str(e),
            type(e).__name__,
        )
        logger.error(f"Failed to initialize shared resources: {e}")
        raise

    yield

    # Cleanup: Close shared instances
    shutdown_start = time.time()
    logger.info("🔄 FastAPI application shutdown initiated")

    try:
        # Shutting down MCP server
        if shared_mcp_server:
            mcp_shutdown_start = time.time()
            await shared_mcp_server.__aexit__(None, None, None)
            mcp_shutdown_time = time.time() - mcp_shutdown_start
            log_mcp_operation(logger, "MCP server shutdown", mcp_shutdown_time, True)

        shutdown_time = time.time() - shutdown_start
        logger.info(
            f"✅ FastAPI application shutdown completed in {shutdown_time:.3f}s",
            {"shutdown_time": f"{shutdown_time:.3f}s"},
        )

        # Resources cleaned up
    except Exception as e:
        shutdown_time = time.time() - shutdown_start
        logger.error(
            f"❌ FastAPI shutdown failed after {shutdown_time:.3f}s",
            {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "shutdown_time": f"{shutdown_time:.3f}s",
            },
        )
        logger.error(f"Error during cleanup: {e}")


# FastAPI App Setup
app = FastAPI(
    lifespan=lifespan,
    title="Financial Analysis API",
    description="API for financial queries using Polygon.io data and prompt templates",
    version="1.0.0",
)

# Dynamic CORS configuration using settings
# Supports both explicit origins and regex for development flexibility
if settings.cors_origins:
    # Parse comma-separated origins from settings
    cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Fallback to regex pattern for any localhost/127.0.0.1 port
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1):\d+$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Process a financial query and return the response using direct prompts."""
    global shared_mcp_server, shared_session

    request_id = str(uuid.uuid4())[:8]

    log_api_request(logger, "POST", "/chat", request.message, request_id)

    # Enhanced input validation for empty and whitespace-only inputs
    if not request.message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty. Please enter a financial question.",
        )

    stripped_message = request.message.strip()
    if len(stripped_message) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query must be at least 2 characters long. Please enter a valid financial question.",
        )

    # Check for whitespace-only or control character inputs
    if not stripped_message or stripped_message.isspace():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty or contain only whitespace. Please enter a valid financial question.",
        )

    # Initialize result variable
    result = None
    response_text = ""

    try:
        # Use shared instances instead of creating new ones
        # Detect analysis intent
        analysis_intent = direct_prompt_manager.detect_analysis_intent(stripped_message)

        # Generate direct prompt
        prompt_data = direct_prompt_manager.generate_direct_prompt(
            stripped_message, analysis_intent
        )

        # Extract ticker if present (for future use)
        _ = direct_prompt_manager.extract_ticker_from_message(stripped_message)

        # Call the AI model with the direct prompt
        try:
            # Create dynamic agent with MCP server for market data access
            analysis_agent = Agent(
                name="Financial Analysis Agent",
                instructions=get_enhanced_agent_instructions(),
                tools=[save_analysis_report],
                mcp_servers=[shared_mcp_server],
                model=settings.available_models[0],
            )

            # Run the financial analysis agent with the direct prompt
            result = await Runner.run(
                analysis_agent, prompt_data["user_prompt"], session=shared_session
            )

            # Extract the response
            response_text = str(result.final_output)

        except Exception as e:
            logger.error(f"AI model call failed: {e}")
            response_text = f"Error: Unable to process request. {str(e)}"

        # Log performance metrics for baseline measurement and monitoring
        logger.info(
            f"Performance metrics - Request processed, Request ID: {request_id}"
        )

        # Log token usage if available in metadata
        if result and hasattr(result, "metadata") and result.metadata and result.metadata.get("tokenCount"):
            logger.info(
                f"Token usage - Input: {result.metadata.get('inputTokens', 'N/A')}, Output: {result.metadata.get('outputTokens', 'N/A')}, Total: {result.metadata.get('tokenCount', 'N/A')}"
            )

        log_api_response(logger, 200, request_id=request_id)

        return ChatResponse(response=response_text)

    except HTTPException:
        raise
    except Exception as e:
        log_api_response(logger, 500, request_id=request_id)
        logger.error(
            f"💥 Unhandled exception in chat endpoint",
            {
                "request_id": request_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error: {str(e)}"
        ) from e


# ====== PROMPT TEMPLATES API ENDPOINTS REMOVED ======
# Removed as part of direct prompt migration


# ====== BUTTON ANALYSIS ENDPOINTS REMOVED ======
# Removed as part of direct prompt migration


# ====== ENHANCED CHAT ANALYSIS ENDPOINT REMOVED ======
# Removed as part of direct prompt migration


# ====== SYSTEM STATUS ENDPOINTS ======


@app.get("/api/v1/system/status", response_model=SystemStatusResponse)
async def get_system_status():
    """Get detailed system status and metrics."""
    try:
        metrics = SystemMetrics(
            api_version="1.0.0",
            prompt_templates_loaded=0,  # Direct prompts implemented
            supported_analysis_types=[],  # Direct prompts don't use predefined types
        )

        return SystemStatusResponse(status="operational", metrics=metrics)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve system status: {str(e)}",
        ) from e


# ====== LEGACY COMPATIBILITY ENDPOINTS REMOVED ======
# Removed as part of direct prompt migration


# ====== HEALTH CHECK ENDPOINTS ======


@app.get("/health", response_model=SystemHealthResponse)
@app.get("/api/v1/health", response_model=SystemHealthResponse)
async def health_check():
    """Health check endpoint."""
    return SystemHealthResponse(
        status="healthy", message="Financial Analysis API is running", version="1.0.0"
    )


# ====== AI MODEL MANAGEMENT ENDPOINTS ======


# Dependency for validating model selection
async def valid_model_id(model_id: AIModelId) -> AIModelId:
    """Validate that the requested model exists and is available"""
    if model_id.value not in settings.available_models:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid model ID: {model_id.value}"
        )
    return model_id


# Model management router
model_router = APIRouter(prefix="/api/v1/models", tags=["AI Models"])


@model_router.get(
    "",
    response_model=ModelListResponse,
    summary="List available AI models",
    description="Get list of all available AI models with current selection",
    responses={
        status.HTTP_200_OK: {
            "model": ModelListResponse,
            "description": "Successfully retrieved model list",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Failed to retrieve models"},
    },
)
async def get_available_models():
    """Get list of available AI models"""
    try:
        models = [
            AIModel(
                id=AIModelId.GPT_5_NANO,
                name="GPT-5 Nano",
                description="Fast and efficient model for quick responses",
                is_default=True,
                cost_per_1k_tokens=0.15,
                max_tokens=4096,
            ),
            AIModel(
                id=AIModelId.GPT_5_MINI,
                name="GPT-5 Mini",
                description="Balanced performance model",
                is_default=False,
                cost_per_1k_tokens=0.25,
                max_tokens=8192,
            ),
            # Removed GPT_4O and GPT_4O_MINI models
        ]

        return ModelListResponse(
            models=models,
            current_model=AIModelId(settings.available_models[0]),
            total_count=len(models),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve models: {str(e)}",
        ) from e


@model_router.post(
    "/select",
    response_model=ModelSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Select an AI model",
    description="Change the active AI model for subsequent requests",
    responses={
        status.HTTP_200_OK: {
            "model": ModelSelectionResponse,
            "description": "Model successfully selected",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid model ID provided"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Failed to select model"},
    },
)
async def select_model(model_id: AIModelId = Depends(valid_model_id)):
    """Select an AI model for use"""
    try:
        # Note: Model selection is now managed by the AI Model Selector feature
        # This endpoint is kept for backward compatibility but doesn't change global settings
        return ModelSelectionResponse(
            success=True,
            message=f"Model {model_id.value} selected for this request",
            selected_model=model_id,
            previous_model=None,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to select model: {str(e)}",
        ) from e


# Add router to app
app.include_router(model_router)

# Cache Management API Endpoints (Security Review Priority 1 fixes)


@app.get("/api/v1/cache/metrics")
async def get_cache_metrics():
    """Get cache performance metrics and statistics."""
    global cache_stats

    return {
        "cache_stats": cache_stats,
        "cache_config": {
            "max_size": CACHE_MAX_SIZE,
            "ttl_seconds": CACHE_TTL_SECONDS,
        },
        "status": "healthy",
    }


@app.delete("/api/v1/cache/ticker/{ticker}")
async def invalidate_ticker_cache(ticker: str):
    """Invalidate all cache entries for a specific ticker symbol."""
    try:
        cleared_count = invalidate_cache_by_ticker(ticker)
        return {
            "success": True,
            "message": f"Invalidated {cleared_count} cache entries for ticker {ticker.upper()}",
            "cleared_count": cleared_count,
            "ticker": ticker.upper(),
        }
    except Exception as e:
        logger.error(f"Failed to invalidate cache for ticker {ticker}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to invalidate cache: {str(e)}",
        ) from e


@app.delete("/api/v1/cache/all")
async def clear_all_cache_endpoint():
    """Clear all cached responses. Use with caution."""
    try:
        cleared_count = clear_all_cache()
        return {
            "success": True,
            "message": f"Cleared all {cleared_count} cache entries",
            "cleared_count": cleared_count,
        }
    except Exception as e:
        logger.error(f"Failed to clear all cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}",
        ) from e


# Main CLI
async def cli_async():
    """Run the interactive CLI loop."""
    print("Welcome to the GPT-5 powered Market Analysis Agent. Type 'exit' to quit.")

    try:
        server = create_polygon_mcp_server()

        async with server:
            while True:
                try:
                    user_input = input("> ").strip()
                    if user_input.lower() == "exit":
                        print("Goodbye!")
                        break

                    if not user_input or len(user_input.strip()) < 2:
                        print("Please enter a valid query (at least 2 characters).")
                        continue

                    # Use direct prompt system
                    analysis_intent = direct_prompt_manager.detect_analysis_intent(user_input)
                    prompt_data = direct_prompt_manager.generate_direct_prompt(
                        user_input, analysis_intent
                    )
                    _ = direct_prompt_manager.extract_ticker_from_message(user_input)

                    # Call the AI model with the direct prompt
                    try:
                        # Create dynamic agent with MCP server for market data access
                        analysis_agent = Agent(
                            name="Financial Analysis Agent",
                            instructions=get_enhanced_agent_instructions(),
                            tools=[save_analysis_report],
                            mcp_servers=[server],
                            model=settings.available_models[0],
                        )

                        # Run the financial analysis agent with the direct prompt
                        result = await Runner.run(
                            analysis_agent, prompt_data["user_prompt"], session=None
                        )

                        # Extract the response
                        response_text = str(result.final_output)

                    except Exception as e:
                        print_error(e, "AI Model Error")
                        response_text = f"Error: Unable to process request. {str(e)}"

                    # Display the response
                    print_response(response_text)

                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
                except Exception as e:
                    print_error(e, "Unexpected Error")

    except Exception as e:
        print_error(e, "Startup Error")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        # Run as FastAPI server
        import uvicorn

        # Starting FastAPI server

        uvicorn.run(
            "main:app",
            host=settings.fastapi_host,
            port=settings.fastapi_port,
            reload=True,
            timeout_keep_alive=120,
        )
    else:
        # Run as CLI
        asyncio.run(cli_async())
