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
    AsyncOpenAI,
    GuardrailFunctionOutput,
    InputGuardrail,
    ModelSettings,
    Runner,
    SQLiteSession,
    function_tool,
    trace,
)
from agents.exceptions import InputGuardrailTripwireTriggered
from agents.mcp import MCPServerStdio
from agents.models.openai_responses import OpenAIResponsesModel
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
        AnalysisType,
        ButtonAnalysisRequest,
        ButtonAnalysisResponse,
        ChatAnalysisRequest,
        ChatAnalysisResponse,
        GeneratePromptRequest,
        GeneratePromptResponse,
        ModelListResponse,
        ModelSelectionResponse,
        PromptMode,
        PromptTemplateInfo,
        ResponseMetadata,
        SystemHealthResponse,
        SystemMetrics,
        SystemStatusResponse,
        TemplateListResponse,
        TickerContextInfo,
    )
    from .prompt_templates import PromptTemplateManager, PromptType, TickerExtractor
    from .utils.logger import (
        get_logger,
        log_agent_processing,
        log_api_request,
        log_api_response,
        log_mcp_operation,
    )
except ImportError:
    # Fallback to absolute imports (when run directly)
    from api_models import (
        AIModel,
        AIModelId,
        AnalysisType,
        ButtonAnalysisRequest,
        ButtonAnalysisResponse,
        ChatAnalysisRequest,
        ChatAnalysisResponse,
        GeneratePromptRequest,
        GeneratePromptResponse,
        ModelListResponse,
        ModelSelectionResponse,
        PromptMode,
        PromptTemplateInfo,
        ResponseMetadata,
        SystemHealthResponse,
        SystemMetrics,
        SystemStatusResponse,
        TemplateListResponse,
        TickerContextInfo,
    )
    from prompt_templates import PromptTemplateManager, PromptType, TickerExtractor
    from utils.logger import (
        get_logger,
        log_agent_processing,
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
        cors_origins = config_settings.backend["security"]["cors"]["origins"]
        self.cors_origins: str = ",".join(cors_origins)

        # Available models from config file
        self.available_models: List[str] = config_settings.backend["ai"]["availableModels"]

        # AI configuration from config file
        self.max_context_length: int = config_settings.backend["ai"]["maxContextLength"]
        self.ai_pricing: dict = config_settings.backend["ai"]["pricing"]

        # Security configuration from config file
        self.enable_rate_limiting: bool = config_settings.backend["security"]["enableRateLimiting"]
        self.rate_limit_rpm: int = config_settings.backend["security"]["rateLimitRPM"]

        # Logging configuration from config file
        self.log_mode: str = config_settings.backend["logging"]["mode"]

        # MCP configuration from config file
        self.polygon_mcp_version: str = config_settings.backend["mcp"]["version"]

        # Frontend configuration from config file
        self.frontend_config = config_settings.frontend


# Initialize settings
settings = Settings()

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
                "git+https://github.com/polygon-io/mcp_polygon@v0.4.0",
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
            return response_cache[cache_key]

        cache_stats["misses"] += 1
        cache_stats["current_size"] = len(response_cache)
        return None
    except Exception as e:
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


async def process_financial_query(
    query: str,
    session: SQLiteSession,
    server,
    request_id: Optional[str] = None,
    model: Optional[str] = None,
) -> dict:
    """Process a financial query using the agent system with caching.

    Args:
        query: The user's query
        session: SQLite session for database operations
    server: MCP server instance
    request_id: Optional request ID for tracking
    model: Optional AI model to use (defaults to first available model from config)

    Returns:
        dict: {
            'success': bool,
            'response': str,
            'error': str or None,
            'error_type': str or None
        }
    """
    start_time = time.time()
    if not request_id:
        request_id = str(uuid.uuid4())[:8]

    # Use provided model or default
    active_model = model if model else settings.available_models[0]

    # Extract ticker from query for cache key generation
    ticker_match = re.search(r"\b([A-Z]{1,5})\b", query.upper())
    ticker = ticker_match.group(1) if ticker_match else ""

    # Check cache first
    cache_key = generate_cache_key(query, ticker)
    cached_response = get_cached_response(cache_key)

    if cached_response:
        processing_time = time.time() - start_time
        log_agent_processing(
            logger,
            "Cache hit - returning cached response",
            {
                "request_id": request_id,
                "cache_key": cache_key[:8],
                "processing_time": f"{processing_time:.3f}s",
            },
        )
        return {"success": True, "response": cached_response, "error": None, "error_type": None}

    # Clean up session periodically
    cleanup_session_periodically()

    log_agent_processing(
        logger,
        "Starting financial query processing",
        {
            "request_id": request_id,
            "query_length": len(query),
            "session_name": session.session_name if hasattr(session, "session_name") else "unknown",
        },
    )

    try:
        with trace("Polygon.io Demo"):
            analysis_agent = Agent(
                name="Financial Analysis Agent",
                instructions=(
                    "Financial analysis agent. Steps:\n"
                    "1. Verify finance-related using guardrail\n"
                    "2. Call Polygon tools precisely; pull the minimal required data.\n"
                    "3. Handle invalid tickers gracefully with clear error messages.\n"
                    "4. Include disclaimers.\n"
                    "5. Offer to save reports if not asked by the user to save a report.\n\n"
                    "FORMATTING REQUIREMENTS:\n"
                    "- ALWAYS start responses with '🎯 KEY TAKEAWAYS' section using bullet points\n"
                    "- ALWAYS explicitly mention ticker symbols throughout the response\n"
                    "- Follow this exact structure: 🎯 KEY TAKEAWAYS, 📊 DETAILED ANALYSIS, ⚠️ DISCLAIMER\n"
                    "- Use financial emojis throughout: 📈 (bullish), 📉 (bearish), "
                    "💰 (money/profit), 💸 (loss), 🏢 (company), 📊 (data/analysis)\n"
                    "- Structure responses with proper sections and line spacing for readability\n"
                    "- Use emoji bullet points in lists instead of regular bullets\n"
                    "- Indicate market sentiment clearly with 📈 BULLISH or 📉 BEARISH "
                    "labels where appropriate\n"
                    "- Use sentiment emojis directly in content: 📈 for bullish/positive "
                    "indicators, 📉 for bearish/negative indicators\n"
                    "- Place emojis at the beginning of relevant bullet points and "
                    "statements for immediate visual sentiment\n"
                    "- Example format: '📈 AAPL Strong growth momentum detected' or "
                    "'📉 TSLA Declining revenue trend observed'\n"
                    "- Use 📊 for neutral analysis, 💰 for profit/gains, 💸 for "
                    "losses, 🏢 for company info\n"
                    "- End with standard disclaimers in a clearly formatted section\n\n"
                    "RULES:\n"
                    "Double-check math; limit news to ≤3 articles/ticker in date range.\n"
                    "If the user asks to save a report, save it to the reports folder "
                    "using the save_analysis_report tool.\n"
                    "When using any polygon.io data tools, be mindful of how much "
                    "data you pull based \n"
                    "on the users input to minimize context being exceeded.\n"
                    "If data unavailable or tool fails, explain gracefully — never fabricate.\n"
                    "For invalid ticker symbols, respond with: 'The ticker symbol [TICKER] "
                    "could not be found or may not be valid. Please verify the symbol and try again.'\n"
                    "Validate ticker symbols before making API calls when possible.\n"
                    "TOOLS:\n"
                    "Polygon.io data, save_analysis_report\n"
                    "Disclaimer: Not financial advice. For informational purposes only."
                ),
                mcp_servers=[server],
                tools=[save_analysis_report],
                input_guardrails=[InputGuardrail(guardrail_function=finance_guardrail)],
                model=OpenAIResponsesModel(model=active_model, openai_client=AsyncOpenAI()),
                model_settings=ModelSettings(truncation="auto"),
            )
            log_agent_processing(
                logger,
                "Running analysis agent",
                {"request_id": request_id, "model": active_model},
            )

            output = await Runner.run(analysis_agent, query, session=session)
            final_output = getattr(output, "final_output", output)

            processing_time = time.time() - start_time
            log_agent_processing(
                logger,
                "Agent processing completed successfully",
                {
                    "request_id": request_id,
                    "processing_time": f"{processing_time:.3f}s",
                    "response_length": len(str(final_output)),
                },
            )

            # Cache the successful response
            response_text = str(final_output)

            # Create metadata for response
            response_metadata = ResponseMetadata(
                model=active_model,
                timestamp=datetime.now().isoformat(),
                response_time=f"{processing_time:.3f}s",
                processing_time=processing_time,
                request_id=request_id,
            )

            # Append model name, timestamp, and response time to response
            response_text_with_metadata = f"{response_text}\n\n[{response_metadata.model}] | {response_metadata.timestamp} | {response_metadata.response_time}"
            cache_response(cache_key, response_text_with_metadata)

            return {
                "success": True,
                "response": response_text_with_metadata,
                "error": None,
                "error_type": None,
                "metadata": response_metadata,
            }
    except InputGuardrailTripwireTriggered as e:
        processing_time = time.time() - start_time
        reasoning = ""
        if hasattr(e, "output_info") and e.output_info:  # pylint: disable=no-member
            reasoning = f" Reasoning: {e.output_info.reasoning}"  # pylint: disable=no-member

        error_msg = (
            f"This query is not related to finance.{reasoning} "
            "Please ask about stock prices, market data, financial analysis, "
            "economic indicators, or company financials."
        )

        log_agent_processing(
            logger,
            "Guardrail triggered - non-finance query",
            {
                "request_id": request_id,
                "processing_time": f"{processing_time:.3f}s",
                "reasoning": reasoning.strip(),
                "query_preview": query[:50] + "..." if len(query) > 50 else query,
            },
        )

        return {
            "success": False,
            "response": "",
            "error": error_msg,
            "error_type": "guardrail",
        }
    except Exception as e:  # pylint: disable=broad-exception-caught
        processing_time = time.time() - start_time
        log_agent_processing(
            logger,
            "Agent processing failed with exception",
            {
                "request_id": request_id,
                "processing_time": f"{processing_time:.3f}s",
                "error_type": type(e).__name__,
                "error_message": str(e)[:200] + "..." if len(str(e)) > 200 else str(e),
            },
        )

        return {"success": False, "response": "", "error": str(e), "error_type": "agent_error"}


# Initialize prompt template system
prompt_manager = PromptTemplateManager()
ticker_extractor = TickerExtractor()


@asynccontextmanager
async def lifespan(app: FastAPI):
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
        await shared_mcp_server.__aenter__()
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
    """Process a financial query and return the response."""
    global shared_mcp_server, shared_session

    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

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

    try:
        # Use shared instances instead of creating new ones
        # Use provided model or default to first available model
        active_model = request.model if request.model else settings.available_models[0]
        result = await process_financial_query(
            stripped_message, shared_session, shared_mcp_server, request_id, active_model
        )

        response_time = time.time() - start_time

        if result["success"]:
            log_api_response(logger, 200, response_time, request_id=request_id)
            return ChatResponse(response=result["response"], metadata=result.get("metadata"))

        if result["error_type"] == "guardrail":
            response_time = time.time() - start_time
            log_api_response(logger, 400, response_time, request_id=request_id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

        response_time = time.time() - start_time
        log_api_response(logger, 500, response_time, request_id=request_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent error: {result['error']}",
        )

    except HTTPException:
        raise
    except Exception as e:  # pylint: disable=broad-exception-caught
        response_time = time.time() - start_time
        log_api_response(logger, 500, response_time, request_id=request_id)
        logger.error(
            f"💥 Unhandled exception in chat endpoint",
            {
                "request_id": request_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "response_time": f"{response_time:.3f}s",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error: {str(e)}"
        ) from e


# ====== NEW PROMPT TEMPLATES API ENDPOINTS ======


@app.get("/api/v1/prompts/templates", response_model=TemplateListResponse)
async def get_prompt_templates():
    """List all available prompt templates."""
    try:
        # Convert to response format
        templates = {}
        for template_type in AnalysisType:
            templates[template_type.value] = PromptTemplateInfo(
                templateId=template_type,
                available=True,
                mode=PromptMode.CONVERSATIONAL,
                enhanced_formatting=True,
                description=f"{template_type.value.replace('_', ' ').title()} analysis template",
            )

        return TemplateListResponse(
            mode="conversational_only", templates=templates, total_count=len(templates)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve templates: {str(e)}",
        ) from e


@app.post("/api/v1/prompts/generate", response_model=GeneratePromptResponse)
async def generate_prompt_endpoint(request: GeneratePromptRequest):
    """Generate a prompt using the specified template and parameters."""
    try:
        # Convert AnalysisType to PromptType
        prompt_type_map = {
            AnalysisType.SNAPSHOT: PromptType.SNAPSHOT,
            AnalysisType.SUPPORT_RESISTANCE: PromptType.SUPPORT_RESISTANCE,
            AnalysisType.TECHNICAL: PromptType.TECHNICAL,
        }

        prompt_type = prompt_type_map[request.template_type]

        # Generate the prompt
        generated_prompt, ticker_context = prompt_manager.generate_prompt(
            prompt_type=prompt_type,
            ticker=request.ticker,
            custom_instructions=request.custom_instructions,
        )

        # Convert ticker context to response format
        ticker_info = TickerContextInfo(
            symbol=ticker_context.symbol,
            company_name=ticker_context.company_name,
            sector=ticker_context.sector,
            last_mentioned=ticker_context.last_mentioned,
            confidence=ticker_context.confidence,
            source=ticker_context.source,
        )

        return GeneratePromptResponse(
            prompt=generated_prompt,
            ticker_context=ticker_info,
            template_type=request.template_type,
            mode=request.mode,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate prompt: {str(e)}",
        ) from e


# ====== UNIFIED BUTTON ANALYSIS ENDPOINT ======


@app.post("/api/v1/analysis/{analysis_type}", response_model=ButtonAnalysisResponse)
async def get_button_analysis(analysis_type: AnalysisType, request: ButtonAnalysisRequest):
    """Unified endpoint for all button-triggered analysis requests."""
    global shared_mcp_server, shared_session

    # Validate ticker input
    if not request.ticker or len(request.ticker.strip()) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ticker symbol is required for {analysis_type.value} analysis.",
        )

    ticker = request.ticker.strip().upper()

    # Basic ticker validation (alphanumeric, 1-10 characters typically)
    if not ticker.replace(".", "").replace("-", "").isalnum() or len(ticker) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ticker symbol format: {ticker}. Please use a valid stock symbol.",
        )

    try:
        # Generate appropriate query based on analysis type
        query_templates = {
            AnalysisType.SNAPSHOT: (
                f"Provide a comprehensive stock snapshot analysis for {ticker}. "
                "Include current price, volume, OHLC data, and recent performance metrics "
                "with clear explanations."
            ),
            AnalysisType.SUPPORT_RESISTANCE: (
                f"Analyze key support and resistance levels for {ticker}. "
                "Identify 3 support levels and 3 resistance levels with explanations "
                "of their significance for trading decisions."
            ),
            AnalysisType.TECHNICAL: (
                f"Provide comprehensive technical analysis for {ticker} using "
                "key indicators including RSI, MACD, and moving averages. Explain momentum "
                "and trend direction with trading recommendations."
            ),
        }

        query = query_templates[analysis_type]

        # Use shared instances instead of creating new ones
        result = await process_financial_query(
            query, shared_session, shared_mcp_server, None, settings.available_models[0]
        )

        if result["success"]:
            return ButtonAnalysisResponse(
                analysis=result["response"],
                ticker=ticker,
                analysis_type=analysis_type,
                success=True,
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{analysis_type.value.title()} analysis failed: {result['error']}",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{analysis_type.value.title()} analysis error: {str(e)}",
        ) from e


# Legacy endpoints for backward compatibility (redirect to unified endpoint)
@app.post("/api/v1/analysis/snapshot", response_model=ButtonAnalysisResponse)
async def get_stock_snapshot_legacy(request: ButtonAnalysisRequest):
    """Legacy endpoint - redirects to unified endpoint."""
    return await get_button_analysis(AnalysisType.SNAPSHOT, request)


@app.post("/api/v1/analysis/support-resistance", response_model=ButtonAnalysisResponse)
async def get_support_resistance_legacy(request: ButtonAnalysisRequest):
    """Legacy endpoint - redirects to unified endpoint."""
    return await get_button_analysis(AnalysisType.SUPPORT_RESISTANCE, request)


@app.post("/api/v1/analysis/technical", response_model=ButtonAnalysisResponse)
async def get_technical_analysis_legacy(request: ButtonAnalysisRequest):
    """Legacy endpoint - redirects to unified endpoint."""
    return await get_button_analysis(AnalysisType.TECHNICAL, request)


# ====== ENHANCED CHAT ANALYSIS ======


@app.post("/api/v1/analysis/chat", response_model=ChatAnalysisResponse)
async def process_chat_analysis(request: ChatAnalysisRequest):
    """Process a chat message with financial analysis using the agent system."""
    global shared_mcp_server, shared_session

    try:
        # Detect analysis type if not provided
        analysis_type = request.analysis_type
        if analysis_type is None:
            detected_type = prompt_manager.detect_analysis_type(request.message)
            if detected_type:
                analysis_type_map = {
                    PromptType.SNAPSHOT: AnalysisType.SNAPSHOT,
                    PromptType.SUPPORT_RESISTANCE: AnalysisType.SUPPORT_RESISTANCE,
                    PromptType.TECHNICAL: AnalysisType.TECHNICAL,
                }
                analysis_type = analysis_type_map.get(detected_type)

        # Convert chat history to the format expected by the system
        chat_history = None
        if request.chat_history:
            chat_history = [
                {"content": msg.content, "role": msg.role} for msg in request.chat_history
            ]

        # Use shared instances instead of creating new ones
        result = await process_financial_query(
            request.message.strip(),
            shared_session,
            shared_mcp_server,
            None,
            settings.available_models[0],
        )

        if result["success"]:
            # Extract ticker if possible
            ticker_context = ticker_extractor.extract_ticker(request.message, chat_history)

            return ChatAnalysisResponse(
                response=result["response"],
                analysis_type=analysis_type,
                ticker_detected=(
                    ticker_context.symbol if ticker_context.symbol != "[TICKER]" else None
                ),
                confidence=ticker_context.confidence,
                follow_up_questions=(
                    [
                        f"Would you like a detailed technical analysis for "
                        f"{ticker_context.symbol}?",
                        f"Should we examine support and resistance levels for "
                        f"{ticker_context.symbol}?",
                        "Would you like to analyze a different stock?",
                    ]
                    if ticker_context.symbol != "[TICKER]"
                    else [
                        "Which stock would you like to analyze?",
                        "Would you like a market snapshot or technical analysis?",
                    ]
                ),
                success=True,
            )

        if result["error_type"] == "guardrail":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {result['error']}",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat analysis failed: {str(e)}",
        ) from e


# ====== SYSTEM STATUS ENDPOINTS ======


@app.get("/api/v1/system/status", response_model=SystemStatusResponse)
async def get_system_status():
    """Get detailed system status and metrics."""
    try:
        metrics = SystemMetrics(
            api_version="1.0.0",
            prompt_templates_loaded=len(PromptType),
            supported_analysis_types=list(AnalysisType),
        )

        return SystemStatusResponse(status="operational", metrics=metrics)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve system status: {str(e)}",
        ) from e


# ====== LEGACY COMPATIBILITY ENDPOINTS ======


@app.get("/templates")
async def get_templates_legacy():
    """Legacy endpoint for template data (redirects to v1 API)."""
    try:
        # Get templates using the same logic as the v1 endpoint
        templates = []
        for template_type in AnalysisType:
            templates.append(
                {
                    "id": template_type.value,
                    "type": template_type.value,
                    "name": f"{template_type.value.replace('_', ' ').title()} Analysis",
                    "description": f"{template_type.value.replace('_', ' ').title()} analysis template",
                    "template": f"Provide {template_type.value.replace('_', ' ')} analysis for {{ticker}}",
                    "icon": (
                        "📈"
                        if template_type == AnalysisType.SNAPSHOT
                        else "🔧" if template_type == AnalysisType.TECHNICAL else "🎯"
                    ),
                    "requiresTicker": True,
                    "followUpQuestions": [
                        "Would you like more details on this analysis?",
                        "Should we analyze another stock?",
                    ],
                }
            )

        return {"success": True, "templates": templates, "total_count": len(templates)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve templates: {str(e)}",
        ) from e


@app.get("/analysis-tools")
async def get_analysis_tools_legacy():
    """Legacy endpoint for analysis tools data."""
    try:
        analysis_tools = []
        for template_type in AnalysisType:
            analysis_tools.append(
                {
                    "id": template_type.value,
                    "name": f"{template_type.value.replace('_', ' ').title()} Analysis",
                    "description": f"Get {template_type.value.replace('_', ' ')} analysis for any stock",
                    "icon": (
                        "📈"
                        if template_type == AnalysisType.SNAPSHOT
                        else "🔧" if template_type == AnalysisType.TECHNICAL else "🎯"
                    ),
                    "endpoint": f"/api/v1/analysis/{template_type.value.replace('_', '-')}",
                    "requiresTicker": True,
                    "category": "financial_analysis",
                }
            )

        return {"success": True, "tools": analysis_tools, "total_count": len(analysis_tools)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve analysis tools: {str(e)}",
        ) from e


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
            AIModel(
                id=AIModelId.GPT_4O,
                name="GPT-4o",
                description="Advanced model for complex tasks",
                is_default=False,
                cost_per_1k_tokens=2.50,
                max_tokens=4096,
            ),
            AIModel(
                id=AIModelId.GPT_4O_MINI,
                name="GPT-4o Mini",
                description="Cost-effective advanced model",
                is_default=False,
                cost_per_1k_tokens=0.15,
                max_tokens=16384,
            ),
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
        session = SQLiteSession(settings.agent_session_name)
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

                    # Use the shared processing function
                    result = await process_financial_query(
                        user_input, session, server, None, settings.available_models[0]
                    )
                    print("\r", end="")

                    if result["success"]:
                        # Create a mock output object for print_response compatibility
                        class MockOutput:
                            """Mock output object for print_response compatibility."""

                            def __init__(self, response):
                                self.final_output = response

                        print_response(MockOutput(result["response"]))
                    else:
                        if result["error_type"] == "guardrail":
                            # Create a mock exception for print_guardrail_error compatibility
                            class MockException:
                                """Mock exception for print_guardrail_error compatibility."""

                                def __init__(self, error_msg):
                                    # Extract reasoning if present
                                    if " Reasoning: " in error_msg:
                                        reasoning = error_msg.split(" Reasoning: ", 1)[1].split(
                                            " Please ask about", 1
                                        )[0]

                                        class OutputInfo:
                                            """Mock output info for error reasoning."""

                                            def __init__(self, reasoning):
                                                self.reasoning = reasoning

                                        self.output_info = OutputInfo(reasoning)
                                    else:
                                        self.output_info = None

                            print_guardrail_error(MockException(result["error"]))
                        else:
                            print_error(result["error"], "Agent Error")

                except (EOFError, KeyboardInterrupt):
                    print("\nGoodbye!")
                    break
                except Exception as e:
                    print_error(e, "Unexpected Error")

    except Exception as e:
        print_error(e, "Setup Error")
    finally:
        print("Market Analysis Agent shutdown complete")


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
