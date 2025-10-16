"""CLI financial analyst using OpenAI Agents SDK, GPT-5, and Polygon.io MCP server.

This script launches a stdio MCP server for Polygon.io tools, runs a single
analysis agent with an input guardrail to ensure finance-related prompts, and
renders only the agent's final output. Report saving functionality has been
removed as it's now handled by the GUI Copy/Export buttons.
"""

import asyncio
import os
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from agents import SQLiteSession
from dotenv import load_dotenv

# FastAPI imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import configuration from separate module
try:
    # Try relative imports first (when run as module)
    from .cli import cli_async, initialize_persistent_agent
    from .config import settings
    from .dependencies import set_shared_resources
    from .routers import chat_router, health_router
except ImportError:
    # Fallback to absolute imports (when run directly)
    from backend.cli import cli_async, initialize_persistent_agent
    from backend.config import settings
    from backend.dependencies import set_shared_resources
    from backend.routers import chat_router, health_router

load_dotenv()

# Global shared resources for FastAPI lifespan management
shared_session = None
shared_agent = None


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):  # pylint: disable=unused-argument
    """FastAPI lifespan management for shared session and agent instances.
    
    Following the architecture principle from commit b866f0a:
    - CLI owns core business logic (initialize_persistent_agent function)
    - FastAPI imports and calls this function (no duplication)
    """
    global shared_session, shared_agent

    # Startup: Create shared instances
    try:
        # Initialize session
        shared_session = SQLiteSession(settings.agent_session_name)
        
        # Initialize persistent agent using shared CLI function (no duplication)
        shared_agent = initialize_persistent_agent()

        # Set shared resources for dependency injection
        set_shared_resources(shared_session, shared_agent)

        print("✅ FastAPI initialized with persistent agent (following b866f0a pattern)")
    except Exception as e:
        # Log initialization error and re-raise
        print(f"Initialization failed: {e}")
        raise

    yield

    # Cleanup: Close shared instances (if needed in future)

    # Cleanup: Close shared instances (if needed in future)


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

# Include all routers
app.include_router(chat_router)
app.include_router(health_router)

# Serve React static files in production
static_dir = Path(__file__).parent.parent.parent / "dist"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


if __name__ == "__main__":
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
