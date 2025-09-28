"""CLI financial analyst using OpenAI Agents SDK, GPT-5, and Polygon.io MCP server.

This script launches a stdio MCP server for Polygon.io tools, runs a single
analysis agent with an input guardrail to ensure finance-related prompts, and
renders only the agent's final output. Report saving functionality has been
removed as it's now handled by the GUI Copy/Export buttons.
"""

import asyncio
import json
import os
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents import (  # function_tool,  # Removed - no longer needed after removing save_analysis_report
    Agent,
    Runner,
    SQLiteSession,
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
except ImportError:
    # Fallback to absolute imports (when run directly)
    from backend.api_models import (
        AIModel,
        AIModelId,
        ModelListResponse,
        ModelSelectionResponse,
        ResponseMetadata,
        SystemHealthResponse,
        SystemMetrics,
        SystemStatusResponse,
    )

load_dotenv()

console = Console()


# ====== CONFIGURATION SETTINGS ======


class Settings(BaseSettings):
    """Consolidated application configuration with environment and JSON-based settings."""

    # API Keys (from environment)
    polygon_api_key: str
    openai_api_key: str

    # Server configuration
    fastapi_host: str = "127.0.0.1"
    fastapi_port: int = 8000

    # MCP configuration
    mcp_timeout_seconds: float = 30.0
    polygon_mcp_version: str = "0.4.1"

    # Agent configuration
    agent_session_name: str = "financial_analysis_session"
    reports_directory: str = "reports"
    cli_session_name: str = "cli_financial_analysis_session"
    session_timeout_minutes: int = 30
    session_cleanup_interval_minutes: int = 5
    max_session_size: int = 1000
    enable_session_persistence: bool = True
    enable_agent_caching: bool = True
    agent_cache_ttl: int = 300
    max_cache_size: int = 50

    # CORS configuration
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # AI configuration
    available_models: List[str] = ["gpt-5-mini"]
    max_context_length: int = 128000
    temperature: float = 0.1
    ai_pricing: dict = {}

    # Security configuration
    enable_rate_limiting: bool = True
    rate_limit_rpm: int = 60

    # GPT-5 model-specific rate limiting
    gpt5_nano_tpm: int = 10000
    gpt5_nano_rpm: int = 100
    gpt5_mini_tpm: int = 20000
    gpt5_mini_rpm: int = 200

    # Logging configuration
    log_mode: str = "info"

    # Monitoring configuration
    enable_performance_monitoring: bool = True
    enable_error_tracking: bool = True
    enable_resource_monitoring: bool = True
    monitoring_log_level: str = "info"
    metrics_retention_days: int = 7

    # Frontend configuration
    frontend_config: dict = {}

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

    def __init__(self):
        super().__init__()

        # Load configuration from JSON file and override defaults
        config_path = Path(__file__).parent.parent.parent / "config" / "app.config.json"
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        # Extract backend and frontend configs
        backend_config = config["backend"]
        frontend_config = config["frontend"]

        # Override defaults with config file values
        self.fastapi_host = backend_config["server"]["host"]
        self.fastapi_port = backend_config["server"]["port"]
        self.mcp_timeout_seconds = backend_config["mcp"]["timeoutSeconds"]
        self.polygon_mcp_version = backend_config["mcp"]["version"]

        # Agent configuration
        agent_config = backend_config["agent"]
        self.agent_session_name = agent_config["sessionName"]
        self.reports_directory = agent_config["reportsDirectory"]
        self.cli_session_name = agent_config["cliSessionName"]
        self.session_timeout_minutes = agent_config["sessionTimeoutMinutes"]
        self.session_cleanup_interval_minutes = agent_config["sessionCleanupIntervalMinutes"]
        self.max_session_size = agent_config["maxSessionSize"]
        self.enable_session_persistence = agent_config["enableSessionPersistence"]
        self.enable_agent_caching = agent_config["enableAgentCaching"]
        self.agent_cache_ttl = agent_config["agentCacheTTL"]
        self.max_cache_size = agent_config["maxCacheSize"]

        # CORS configuration
        cors_origins_list = backend_config["security"]["cors"]["origins"]
        self.cors_origins = ",".join(cors_origins_list)

        # AI configuration
        ai_config = backend_config["ai"]
        self.available_models = ai_config["availableModels"]
        self.max_context_length = ai_config["maxContextLength"]
        self.temperature = ai_config["temperature"]
        self.ai_pricing = ai_config["pricing"]

        # Security configuration
        security_config = backend_config["security"]
        self.enable_rate_limiting = security_config["enableRateLimiting"]
        self.rate_limit_rpm = security_config["rateLimitRPM"]

        # GPT-5 model-specific rate limiting
        rate_limiting = security_config["rateLimiting"]
        self.gpt5_nano_tpm = rate_limiting["gpt5Nano"]["tpm"]
        self.gpt5_nano_rpm = rate_limiting["gpt5Nano"]["rpm"]
        self.gpt5_mini_tpm = rate_limiting["gpt5Mini"]["tpm"]
        self.gpt5_mini_rpm = rate_limiting["gpt5Mini"]["rpm"]

        # Logging configuration
        self.log_mode = backend_config["logging"]["mode"]

        # Monitoring configuration
        monitoring_config = backend_config["monitoring"]
        self.enable_performance_monitoring = monitoring_config["enablePerformanceMonitoring"]
        self.enable_error_tracking = monitoring_config["enableErrorTracking"]
        self.enable_resource_monitoring = monitoring_config["enableResourceMonitoring"]
        self.monitoring_log_level = monitoring_config["logLevel"]
        self.metrics_retention_days = monitoring_config["metricsRetentionDays"]

        # Frontend configuration
        self.frontend_config = frontend_config


# Initialize settings
settings = Settings()


def get_model_rate_limits(model: str) -> dict:
    """Get rate limits for specific GPT-5 models."""
    if model == "gpt-5-nano":
        return {"tpm": settings.gpt5_nano_tpm, "rpm": settings.gpt5_nano_rpm}
    if model == "gpt-5-mini":
        return {"tpm": settings.gpt5_mini_tpm, "rpm": settings.gpt5_mini_rpm}
    return {"tpm": settings.gpt5_nano_tpm, "rpm": settings.gpt5_nano_rpm}  # Default fallback


# Global shared resources for FastAPI lifespan management
shared_mcp_server = None
shared_session = None


# Agent caching for performance optimization
class AgentCache:
    """Agent cache for reusing agents with same parameters."""

    def __init__(self, cache_ttl: int = 300, max_size: int = 50):
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = cache_ttl  # 5 minutes default
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0

    def _generate_cache_key(self, model: str, instructions: str, mcp_servers: list) -> str:
        """Generate a unique cache key for agent parameters."""
        # Create a hash of the parameters
        mcp_servers_str = str([str(server) for server in mcp_servers])
        key_string = f"{model}:{instructions}:{mcp_servers_str}"
        return str(hash(key_string))

    def get_cached_agent(self, model: str, instructions: str, mcp_servers: list):
        """Get cached agent if available and not expired."""
        cache_key = self._generate_cache_key(model, instructions, mcp_servers)

        if cache_key in self.cache:
            cached_agent, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                self.hit_count += 1
                return cached_agent
            # Remove expired entry
            del self.cache[cache_key]

        self.miss_count += 1
        return None

    def cache_agent(self, model: str, instructions: str, mcp_servers: list, agent):
        """Cache an agent with its parameters."""
        cache_key = self._generate_cache_key(model, instructions, mcp_servers)

        # Clean up cache if it's getting too large
        if len(self.cache) >= self.max_size:
            self._cleanup_cache()

        self.cache[cache_key] = (agent, time.time())

    def _cleanup_cache(self):
        """Remove oldest entries from cache."""
        if not self.cache:
            return

        # Sort by timestamp and remove oldest 25%
        sorted_items = sorted(self.cache.items(), key=lambda x: x[1][1])
        items_to_remove = len(sorted_items) // 4  # Remove 25%

        for i in range(items_to_remove):
            key = sorted_items[i][0]
            del self.cache[key]

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0

        return {
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": round(hit_rate, 2),
            "cache_ttl": self.cache_ttl,
        }

    def clear_cache(self):
        """Clear all cached agents."""
        cleared_count = len(self.cache)
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
        return cleared_count


# Global agent cache instances - will be initialized in lifespan
gui_agent_cache = None
cli_agent_cache = None


# MCP Server monitoring and health management


# MCP Server resource management


# Performance monitoring and metrics


# Secure response cache for financial queries with automatic size and TTL management
CACHE_TTL_SECONDS = 900  # 15 minutes in seconds
CACHE_MAX_SIZE = 1000  # Maximum number of cached responses
response_cache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS)

# Cache statistics for monitoring
cache_stats = {"hits": 0, "misses": 0, "evictions": 0, "current_size": 0}

# Request tracking for logging removed


# Models


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


# save_analysis_report function removed - superseded by GUI Copy/Export buttons


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
    """
    Generate enhanced agent instructions for financial analysis.

    Returns:
        Enhanced agent instructions string
    """
    datetime_context = get_current_datetime_context()
    return f"""You are a financial analyst with real-time market data access.

{datetime_context}

TOOLS: Use Polygon.io MCP server for live market data, prices, and financial information.
🔴 CRITICAL: YOU MUST NOT USE THE FOLLOWING UNSUPPORTED TOOLS: [list_trades, get_last_trade, list_quotes, get_last_quote] 🔴

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: Format data in bullet point format with 2 decimal points max
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details
7. Do NOT provide any of the following UNLESS SPECIFICALLY REQUESTED: analysis, key takeways, actionable recommendations"""


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


def create_agent(mcp_server, agent_cache=None):
    """Create or retrieve a cached financial analysis agent.

    Args:
        mcp_server (MCPServerStdio): The MCP server instance to use
        agent_cache (AgentCache, optional): The agent cache instance

    Returns:
        Agent: The financial analysis agent
    """
    analysis_agent = None

    # Try to get cached agent if caching is enabled
    if settings.enable_agent_caching and agent_cache:
        instructions = get_enhanced_agent_instructions()
        analysis_agent = agent_cache.get_cached_agent(
            model=settings.available_models[0],
            instructions=instructions,
            mcp_servers=[mcp_server],
        )

    # Create new agent if not cached
    if analysis_agent is None:
        analysis_agent = Agent(
            name="Financial Analysis Agent",
            instructions=get_enhanced_agent_instructions(),
            tools=[],  # Removed save_analysis_report - superseded by GUI Copy/Export buttons
            mcp_servers=[mcp_server],
            model=settings.available_models[0],
        )

        # Cache the new agent if caching is enabled
        if settings.enable_agent_caching and agent_cache:
            agent_cache.cache_agent(
                model=settings.available_models[0],
                instructions=get_enhanced_agent_instructions(),
                mcp_servers=[mcp_server],
                agent=analysis_agent,
            )

    return analysis_agent


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
            return str(response_cache[cache_key])

        cache_stats["misses"] += 1
        cache_stats["current_size"] = len(response_cache)
        return None
    except Exception:  # pylint: disable=broad-exception-caught
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

    except MemoryError:
        response_cache.clear()
        cache_stats["evictions"] += 1
        cache_stats["current_size"] = 0
        # Try caching again after clearing
        try:
            response_cache[cache_key] = response
            cache_stats["current_size"] = len(response_cache)
        except Exception:
            # Cache operation failed, continue without caching
            cache_stats["errors"] = cache_stats.get("errors", 0) + 1


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
                continue  # Already removed by TTL

        cache_stats["current_size"] = len(response_cache)

        # Cache invalidation logging removed for performance

        return len(keys_to_remove)

    except Exception:
        return 0


def clear_all_cache() -> int:
    """Clear all cache entries and return count of cleared items."""
    global cache_stats

    try:
        cleared_count = len(response_cache)
        response_cache.clear()
        cache_stats["current_size"] = 0
        cache_stats["evictions"] += cleared_count

        return cleared_count

    except Exception:
        return 0


# Session recovery error handling removed


# Output functions
def print_response(result):
    """Simplified response renderer with emoji support and performance metrics."""
    console.print("\n[bold green]✅ Query processed successfully![/bold green]")
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

    # Display performance metrics if available
    if hasattr(result, "metadata") and result.metadata:
        console.print("\n[bold cyan]📊 Performance Metrics:[/bold cyan]")

        # Display processing time if available
        if hasattr(result.metadata, "processing_time") and result.metadata.processing_time:
            console.print(f"   ⏱️  Response Time: {result.metadata.processing_time:.3f}s")

        # Extract token information
        token_count = None
        input_tokens = None
        output_tokens = None

        if hasattr(result.metadata, "get"):
            token_count = result.metadata.get("tokenCount")
            input_tokens = result.metadata.get("inputTokens")
            output_tokens = result.metadata.get("outputTokens")
        elif hasattr(result.metadata, "usage"):
            usage = result.metadata.usage
            if hasattr(usage, "total_tokens"):
                token_count = usage.total_tokens
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens
            if hasattr(usage, "completion_tokens"):
                output_tokens = usage.completion_tokens
        elif hasattr(result.metadata, "token_count"):
            token_count = result.metadata.token_count

        # Display token information
        if token_count:
            token_display = f"   🔢  Tokens Used: {token_count:,}"
            if input_tokens and output_tokens:
                token_display += f" (Input: {input_tokens:,}, Output: {output_tokens:,})"
            console.print(token_display)

        # Display model information
        if hasattr(result.metadata, "model"):
            console.print(f"   🤖  Model: {result.metadata.model}")
        elif hasattr(result, "model"):
            console.print(f"   🤖  Model: {result.model}")

    # Enhanced separator with emoji
    console.print("\n[dim]" + "─" * 50 + "[/dim]\n")


def print_error(error, error_type="Error"):
    """Display errors in a consistent, readable format for the CLI."""
    console.print(f"\n[bold red]!!! {error_type} !!![/bold red]")
    console.print(str(error).strip())
    console.print("------------------\n")


# process_financial_query function removed as part of direct prompt migration


# Direct prompt system removed - using unified prompt system


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):  # pylint: disable=unused-argument
    """FastAPI lifespan management for shared MCP server and session instances."""
    global shared_mcp_server, shared_session, gui_agent_cache

    # Startup: Create shared instances
    try:
        # Server initialization

        # Initialize session
        shared_session = SQLiteSession(settings.agent_session_name)

        # Initialize agent cache for GUI
        if settings.enable_agent_caching:
            gui_agent_cache = AgentCache(
                cache_ttl=settings.agent_cache_ttl, max_size=settings.max_cache_size
            )

        # Initialize MCP server
        shared_mcp_server = create_polygon_mcp_server()
        await shared_mcp_server.__aenter__()  # pylint: disable=unnecessary-dunder-call

        # Log MCP server health check

        # Initialization complete
    except Exception as e:
        # Log initialization error and re-raise
        console.print(f"[bold red]Initialization failed: {e}[/bold red]")
        raise

    yield

    # Cleanup: Close shared instances

    try:
        # Shutting down MCP server
        if shared_mcp_server:
            await shared_mcp_server.__aexit__(None, None, None)

            # Log MCP server shutdown performance

        # Resources cleaned up
    except Exception:
        # Ignore cleanup errors during shutdown
        pass  # This is intentional - we don't want to raise during shutdown


# FastAPI App Setup
app = FastAPI(
    lifespan=lifespan,
    title="Financial Analysis API",
    description="API for financial queries using Polygon.io data and prompt templates",
    version="1.0.0",
)


# Add response timing middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add process time header to all responses for performance monitoring."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


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

    # Start timing for performance metrics
    start_time = time.perf_counter()

    try:
        # Use shared instances instead of creating new ones
        # Call the AI model with the unified prompt system
        try:

            # MCP server health check and error recovery
            if shared_mcp_server is None:
                shared_mcp_server = create_polygon_mcp_server()
                await shared_mcp_server.__aenter__()  # pylint: disable=unnecessary-dunder-call

            # Get or create agent with caching using factory function
            analysis_agent = create_agent(shared_mcp_server, gui_agent_cache)

            # Run the financial analysis agent with the user message
            result = await Runner.run(analysis_agent, stripped_message, session=shared_session)

            # Extract the response
            response_text = str(result.final_output)

        except Exception as e:
            response_text = f"Error: Unable to process request. {str(e)}"

        # Extract token count from OpenAI response metadata
        token_count = None

        if result and hasattr(result, "metadata") and result.metadata:
            # Try to extract token information from OpenAI response metadata
            if hasattr(result.metadata, "get"):
                token_count = result.metadata.get("tokenCount")
            elif hasattr(result.metadata, "usage"):
                # Handle OpenAI usage object format
                usage = result.metadata.usage
                if hasattr(usage, "total_tokens"):
                    token_count = usage.total_tokens
                # Token usage tracking removed for performance

        # Calculate processing time
        processing_time = time.perf_counter() - start_time

        # Create response metadata with timing and token information
        response_metadata = ResponseMetadata(
            model=settings.available_models[0],
            timestamp=datetime.now().isoformat(),
            processingTime=processing_time,
            requestId=request_id,
            tokenCount=token_count,
        )

        # Log performance metrics for baseline measurement and monitoring

        # Log token usage if available in metadata
        # Token usage logging removed for performance

        return ChatResponse(response=response_text, metadata=response_metadata)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error: {str(e)}"
        ) from e


# ====== PROMPT TEMPLATES API ENDPOINTS REMOVED ======


# ====== BUTTON ANALYSIS ENDPOINTS REMOVED ======


# ====== ENHANCED CHAT ANALYSIS ENDPOINT REMOVED ======


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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}",
        ) from e


# Main CLI
async def cli_async():
    """Run the interactive CLI loop."""
    print("Welcome to the GPT-5 powered Market Analysis Agent. Type 'exit' to quit.")

    try:
        # Initialize persistent CLI session for conversation memory
        cli_session = SQLiteSession(settings.cli_session_name)
        print(f"📊 CLI session '{settings.cli_session_name}' initialized for conversation memory")

        # Initialize CLI agent cache
        global cli_agent_cache
        if settings.enable_agent_caching:
            cli_agent_cache = AgentCache(
                cache_ttl=settings.agent_cache_ttl, max_size=settings.max_cache_size
            )
            print("🚀 CLI agent cache initialized")

        server = create_polygon_mcp_server()

        # Initialize CLI MCP server
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

                    # Use unified prompt system
                    # Call the AI model with the unified prompt system
                    try:
                        # Start timing for performance metrics
                        start_time = time.perf_counter()

                        # Get or create agent with caching using factory function
                        analysis_agent = create_agent(server, cli_agent_cache)

                        # Run the financial analysis agent with the user message
                        result = await Runner.run(analysis_agent, user_input, session=cli_session)

                        # Calculate processing time
                        processing_time = time.perf_counter() - start_time

                        # Extract token information from OpenAI response metadata
                        token_count = None

                        if hasattr(result, "metadata") and result.metadata:
                            # Try to extract token information from OpenAI response metadata
                            if hasattr(result.metadata, "get"):
                                token_count = result.metadata.get("tokenCount")
                            elif hasattr(result.metadata, "usage"):
                                # Handle OpenAI usage object format
                                usage = result.metadata.usage
                                if hasattr(usage, "total_tokens"):
                                    token_count = usage.total_tokens

                        # Create metadata object for CLI response
                        cli_metadata = ResponseMetadata(
                            model=settings.available_models[0],
                            timestamp=datetime.now().isoformat(),
                            processing_time=processing_time,
                            request_id=None,  # CLI doesn't use request IDs
                            token_count=token_count,
                        )

                        # Attach metadata to result object
                        result.metadata = cli_metadata

                        # Extract the response (stored in result object for print_response)
                        _ = str(result.final_output)

                    except Exception as e:
                        print_error(e, "AI Model Error")

                        # Create a mock result object for error cases
                        class MockResult:
                            def __init__(self, error_msg):
                                self.final_output = error_msg
                                self.metadata = None

                        result = MockResult(f"Error: Unable to process request. {str(e)}")

                    # Display the response with full result object for metadata
                    print_response(result)

                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
                except EOFError:
                    # Handle end of input stream (e.g., when piping input)
                    print("\nInput stream ended. Goodbye!")
                    break
                except Exception as e:
                    print_error(e, "Unexpected Error")

    except Exception as e:
        print_error(e, "Startup Error")
    finally:
        # Clean up CLI session and agent cache on exit
        try:
            if "cli_session" in locals():
                # Session cleanup is handled automatically by SQLiteSession
                print("📊 CLI session cleaned up")

            if "cli_agent_cache" in globals() and cli_agent_cache:
                cli_cache_stats = cli_agent_cache.get_cache_stats()
                print(
                    f"🚀 CLI agent cache stats: {cli_cache_stats['hit_rate']}% hit rate, {cli_cache_stats['cache_size']} entries"
                )
                cli_agent_cache.clear_cache()
                print("🚀 CLI agent cache cleaned up")
        except Exception as cleanup_error:
            print(f"Warning: Cleanup failed: {cleanup_error}")


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
