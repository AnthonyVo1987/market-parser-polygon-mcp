"""CLI financial analyst using OpenAI Agents SDK, GPT-5, and Polygon.io MCP server.

This script launches a stdio MCP server for Polygon.io tools, runs a single
analysis agent with an input guardrail to ensure finance-related prompts, and
renders only the agent's final output. Report saving functionality has been
removed as it's now handled by the GUI Copy/Export buttons.
"""

import asyncio
import json
import os

# import re  # Removed - no longer needed after removing save_analysis_report
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

        # Session management configuration
        self.cli_session_name: str = config_settings.backend["agent"]["cliSessionName"]
        self.session_timeout_minutes: int = config_settings.backend["agent"][
            "sessionTimeoutMinutes"
        ]
        self.session_cleanup_interval_minutes: int = config_settings.backend["agent"][
            "sessionCleanupIntervalMinutes"
        ]
        self.max_session_size: int = config_settings.backend["agent"]["maxSessionSize"]
        self.enable_session_persistence: bool = config_settings.backend["agent"][
            "enableSessionPersistence"
        ]
        self.enable_agent_caching: bool = config_settings.backend["agent"]["enableAgentCaching"]
        self.agent_cache_ttl: int = config_settings.backend["agent"]["agentCacheTTL"]
        self.max_cache_size: int = config_settings.backend["agent"]["maxCacheSize"]

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
        self.gpt5_nano_tpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Nano"][
            "tpm"
        ]
        self.gpt5_nano_rpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Nano"][
            "rpm"
        ]
        self.gpt5_mini_tpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Mini"][
            "tpm"
        ]
        self.gpt5_mini_rpm: int = config_settings.backend["security"]["rateLimiting"]["gpt5Mini"][
            "rpm"
        ]

        # Logging configuration from config file
        self.log_mode: str = config_settings.backend["logging"]["mode"]

        # Monitoring configuration
        self.enable_performance_monitoring: bool = config_settings.backend["monitoring"][
            "enablePerformanceMonitoring"
        ]
        self.enable_error_tracking: bool = config_settings.backend["monitoring"][
            "enableErrorTracking"
        ]
        self.enable_resource_monitoring: bool = config_settings.backend["monitoring"][
            "enableResourceMonitoring"
        ]
        self.monitoring_log_level: str = config_settings.backend["monitoring"]["logLevel"]
        self.metrics_retention_days: int = config_settings.backend["monitoring"][
            "metricsRetentionDays"
        ]

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
    if model == "gpt-5-mini":
        return {"tpm": settings.gpt5_mini_tpm, "rpm": settings.gpt5_mini_rpm}
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


# Agent caching for performance optimization
class AgentCache:
    """Agent cache for reusing agents with same parameters."""

    def __init__(self, cache_ttl: int = 300, max_size: int = 50):
        self.cache = {}
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
                logger.debug(f"Agent cache hit: {cache_key[:20]}...")
                return cached_agent
            else:
                # Remove expired entry
                del self.cache[cache_key]

        self.miss_count += 1
        logger.debug(f"Agent cache miss: {cache_key[:20]}...")
        return None

    def cache_agent(self, model: str, instructions: str, mcp_servers: list, agent):
        """Cache an agent with its parameters."""
        cache_key = self._generate_cache_key(model, instructions, mcp_servers)

        # Clean up cache if it's getting too large
        if len(self.cache) >= self.max_size:
            self._cleanup_cache()

        self.cache[cache_key] = (agent, time.time())
        logger.debug(f"Agent cached: {cache_key[:20]}...")

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

        logger.debug(f"Agent cache cleaned up: removed {items_to_remove} entries")

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
        logger.info(f"Agent cache cleared: {cleared_count} entries removed")
        return cleared_count


# Global agent cache instances
gui_agent_cache = None
cli_agent_cache = None


# MCP Server monitoring and health management
class MCPServerMonitor:
    """Monitor MCP server health and performance."""

    def __init__(self):
        self.health_checks = []
        self.error_count = 0
        self.last_health_check = None
        self.performance_metrics = []

    def log_health_check(self, server_name: str, is_healthy: bool, response_time: float = 0.0):
        """Log MCP server health check results."""
        self.health_checks.append(
            {
                "server_name": server_name,
                "is_healthy": is_healthy,
                "response_time": response_time,
                "timestamp": time.time(),
            }
        )
        self.last_health_check = time.time()

        if not is_healthy:
            self.error_count += 1
            logger.warning(f"MCP server {server_name} health check failed")
        else:
            logger.debug(f"MCP server {server_name} health check passed in {response_time:.3f}s")

    def log_performance_metric(
        self, server_name: str, operation: str, duration: float, success: bool
    ):
        """Log MCP server performance metrics."""
        self.performance_metrics.append(
            {
                "server_name": server_name,
                "operation": operation,
                "duration": duration,
                "success": success,
                "timestamp": time.time(),
            }
        )

        if not success:
            self.error_count += 1
            logger.error(
                f"MCP server {server_name} operation '{operation}' failed after {duration:.3f}s"
            )
        else:
            logger.debug(
                f"MCP server {server_name} operation '{operation}' completed in {duration:.3f}s"
            )

    def get_health_summary(self) -> dict:
        """Get MCP server health summary."""
        if not self.health_checks:
            return {"status": "unknown", "error_count": self.error_count}

        recent_checks = [
            check for check in self.health_checks if time.time() - check["timestamp"] < 3600
        ]  # Last hour

        if not recent_checks:
            return {"status": "unknown", "error_count": self.error_count}

        healthy_count = sum(1 for check in recent_checks if check["is_healthy"])
        total_count = len(recent_checks)
        health_rate = (healthy_count / total_count) * 100

        avg_response_time = sum(check["response_time"] for check in recent_checks) / total_count

        return {
            "status": (
                "healthy" if health_rate > 90 else "degraded" if health_rate > 70 else "unhealthy"
            ),
            "health_rate": round(health_rate, 2),
            "avg_response_time": round(avg_response_time, 3),
            "error_count": self.error_count,
            "total_checks": total_count,
        }

    def get_performance_summary(self) -> dict:
        """Get MCP server performance summary."""
        if not self.performance_metrics:
            return {}

        recent_metrics = [
            metric
            for metric in self.performance_metrics
            if time.time() - metric["timestamp"] < 3600
        ]  # Last hour

        if not recent_metrics:
            return {}

        successful_ops = [m for m in recent_metrics if m["success"]]
        avg_duration = (
            sum(m["duration"] for m in successful_ops) / len(successful_ops)
            if successful_ops
            else 0
        )
        success_rate = (len(successful_ops) / len(recent_metrics)) * 100

        return {
            "avg_operation_duration": round(avg_duration, 3),
            "success_rate": round(success_rate, 2),
            "total_operations": len(recent_metrics),
            "failed_operations": len(recent_metrics) - len(successful_ops),
        }


# Global MCP server monitor
mcp_server_monitor = MCPServerMonitor()


# MCP Server resource management
class MCPServerResourceManager:
    """Manage MCP server resources and memory."""

    def __init__(self):
        self.active_connections = 0
        self.max_connections = 10
        self.connection_pool = []
        self.memory_usage = 0

    def get_connection_stats(self) -> dict:
        """Get connection pool statistics."""
        return {
            "active_connections": self.active_connections,
            "max_connections": self.max_connections,
            "pool_size": len(self.connection_pool),
            "memory_usage_mb": round(self.memory_usage / 1024 / 1024, 2),
        }

    def check_resource_limits(self) -> bool:
        """Check if we're within resource limits."""
        return self.active_connections < self.max_connections

    def log_memory_usage(self, usage_bytes: int):
        """Log memory usage for monitoring."""
        self.memory_usage = usage_bytes
        if usage_bytes > 100 * 1024 * 1024:  # 100MB threshold
            logger.warning(f"MCP server memory usage high: {usage_bytes / 1024 / 1024:.2f}MB")

    def cleanup_resources(self):
        """Clean up MCP server resources."""
        self.connection_pool.clear()
        self.active_connections = 0
        self.memory_usage = 0
        logger.info("MCP server resources cleaned up")


# Global MCP server resource manager
mcp_resource_manager = MCPServerResourceManager()


# Performance monitoring and metrics
class PerformanceMetrics:
    """Performance metrics for monitoring system health."""

    def __init__(
        self,
        agent_creation_time: float = 0.0,
        session_access_time: float = 0.0,
        mcp_server_response_time: float = 0.0,
        cache_hit_rate: float = 0.0,
        memory_usage: float = 0.0,
        timestamp: float = None,
    ):
        self.agent_creation_time = agent_creation_time
        self.session_access_time = session_access_time
        self.mcp_server_response_time = mcp_server_response_time
        self.cache_hit_rate = cache_hit_rate
        self.memory_usage = memory_usage
        self.timestamp = timestamp or time.time()


class PerformanceMonitor:
    """Monitor system performance and health."""

    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.error_count = 0
        self.last_cleanup = time.time()

    def log_agent_creation_time(self, creation_time: float):
        """Log agent creation time for performance analysis."""
        self.metrics.append(
            PerformanceMetrics(agent_creation_time=creation_time, timestamp=time.time())
        )
        logger.debug(f"Agent creation time logged: {creation_time:.3f}s")

    def log_session_access_time(self, access_time: float):
        """Log session access time for performance analysis."""
        if self.metrics:
            self.metrics[-1].session_access_time = access_time
        logger.debug(f"Session access time logged: {access_time:.3f}s")

    def log_mcp_server_response_time(self, response_time: float):
        """Log MCP server response time for performance analysis."""
        if self.metrics:
            self.metrics[-1].mcp_server_response_time = response_time
        logger.debug(f"MCP server response time logged: {response_time:.3f}s")

    def log_cache_hit_rate(self, hit_rate: float):
        """Log cache hit rate for performance analysis."""
        if self.metrics:
            self.metrics[-1].cache_hit_rate = hit_rate
        logger.debug(f"Cache hit rate logged: {hit_rate:.2f}%")

    def log_memory_usage(self, memory_usage: float):
        """Log memory usage for performance analysis."""
        if self.metrics:
            self.metrics[-1].memory_usage = memory_usage
        logger.debug(f"Memory usage logged: {memory_usage:.2f}MB")

    def log_error(self, error_type: str, error_message: str):
        """Log system errors for monitoring."""
        self.error_count += 1
        logger.error(f"System error [{error_type}]: {error_message}")

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.metrics:
            return {"status": "no_data", "error_count": self.error_count}

        recent_metrics = [m for m in self.metrics if time.time() - m.timestamp < 3600]  # Last hour

        if not recent_metrics:
            return {"status": "no_recent_data", "error_count": self.error_count}

        return {
            "avg_agent_creation_time": round(
                sum(m.agent_creation_time for m in recent_metrics) / len(recent_metrics), 3
            ),
            "avg_session_access_time": round(
                sum(m.session_access_time for m in recent_metrics) / len(recent_metrics), 3
            ),
            "avg_mcp_server_response_time": round(
                sum(m.mcp_server_response_time for m in recent_metrics) / len(recent_metrics), 3
            ),
            "avg_cache_hit_rate": round(
                sum(m.cache_hit_rate for m in recent_metrics) / len(recent_metrics), 2
            ),
            "avg_memory_usage": round(
                sum(m.memory_usage for m in recent_metrics) / len(recent_metrics), 2
            ),
            "total_requests": len(recent_metrics),
            "error_count": self.error_count,
            "status": (
                "healthy"
                if self.error_count < 5
                else "degraded" if self.error_count < 20 else "unhealthy"
            ),
        }

    def cleanup_old_metrics(self):
        """Clean up old metrics to prevent memory growth."""
        current_time = time.time()
        if current_time - self.last_cleanup > 3600:  # Clean up every hour
            self.metrics = [
                m for m in self.metrics if current_time - m.timestamp < 86400
            ]  # Keep last 24 hours
            self.last_cleanup = current_time
            logger.debug(f"Performance metrics cleaned up, {len(self.metrics)} entries remaining")


# Global performance monitor
performance_monitor = PerformanceMonitor()

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


def get_enhanced_agent_instructions(user_input: str = ""):
    """
    Generate enhanced agent instructions with dynamic customization support.

    This function replaces the static get_enhanced_agent_instructions function
    with a dynamic version that supports user customization while maintaining
    backward compatibility.

    Args:
        user_input: Optional user input for customization

    Returns:
        Enhanced agent instructions string
    """
    try:
        # Import the dynamic prompt integration
        from .dynamic_prompt_integration import (
            get_enhanced_agent_instructions as dynamic_get_instructions,
        )

        return dynamic_get_instructions(user_input)
    except ImportError:
        # Fallback to static prompt for backward compatibility
        datetime_context = get_current_datetime_context()
        return f"""Quick Response Needed with minimal tool calls: You are a financial analyst with real-time market data access.

{datetime_context}

TOOLS: Polygon.io MCP server for live market data, prices, and financial information.

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: DATA FIRST → DETAILED ANALYSIS
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details

OUTPUT FORMAT:
A. DATA FIRST
- Format data in bullet point format with 2 decimal points max
- Provide cleaned up raw format data first, then verbal analysis
- Convert JSON response attributes to user-friendly terms
- Include relevant financial data and metrics

B. DETAILED ANALYSIS
- Provide Maximum of 3 KEY TAKEAWAYS/INSIGHTS in numbered/bullet point format
- No actionable recommendations
- Focus on the data only"""


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

    try:
        if shared_session is None:
            logger.warning("Session cleanup called but shared_session is None")
            return

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

        # Session health monitoring
        if hasattr(shared_session, "_session_data"):
            session_size = len(getattr(shared_session, "_session_data", {}))
            logger.debug(f"Session health: {session_size} entries")

            # Session error recovery - reset if corrupted
            if session_size > 1000:  # Unusually large session
                logger.warning("Session size exceeded threshold, resetting session")
                shared_session = SQLiteSession(settings.agent_session_name)
                logger.info("Session reset completed")

    except Exception as e:
        logger.error(f"Session cleanup error: {e}")
        # Session error recovery - recreate session on error
        try:
            shared_session = SQLiteSession(settings.agent_session_name)
            logger.info("Session recreated after cleanup error")
        except Exception as recovery_error:
            logger.error(f"Session recovery failed: {recovery_error}")


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
    global shared_mcp_server, shared_session, gui_agent_cache

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

        # Initialize agent cache for GUI
        if settings.enable_agent_caching:
            gui_agent_cache = AgentCache(
                cache_ttl=settings.agent_cache_ttl, max_size=settings.max_cache_size
            )
            logger.debug("🚀 GUI agent cache initialized")

        # Initialize MCP server
        mcp_start = time.time()
        shared_mcp_server = create_polygon_mcp_server()
        await shared_mcp_server.__aenter__()  # pylint: disable=unnecessary-dunder-call
        mcp_time = time.time() - mcp_start
        log_mcp_operation(logger, "MCP server initialization", mcp_time, True)

        # Log MCP server health check
        mcp_server_monitor.log_health_check("shared_mcp_server", True, mcp_time)

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

            # Log MCP server shutdown performance
            mcp_server_monitor.log_performance_metric(
                "shared_mcp_server", "shutdown", mcp_shutdown_time, True
            )

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
            # Start performance monitoring
            agent_creation_start = time.perf_counter()

            # MCP server health check and error recovery
            if shared_mcp_server is None:
                logger.error("MCP server is None, attempting recovery")
                performance_monitor.log_error(
                    "mcp_server_recovery", "MCP server was None, attempting recovery"
                )
                shared_mcp_server = create_polygon_mcp_server()
                await shared_mcp_server.__aenter__()
                mcp_server_monitor.log_health_check("shared_mcp_server", True, 0.0)

            # Get or create agent with caching
            analysis_agent = None
            if settings.enable_agent_caching and gui_agent_cache:
                # Try to get cached agent
                instructions = get_enhanced_agent_instructions()
                analysis_agent = gui_agent_cache.get_cached_agent(
                    model=settings.available_models[0],
                    instructions=instructions,
                    mcp_servers=[shared_mcp_server],
                )

            if analysis_agent is None:
                # Create new agent
                analysis_agent = Agent(
                    name="Financial Analysis Agent",
                    instructions=get_enhanced_agent_instructions(),
                    tools=[],  # Removed save_analysis_report - superseded by GUI Copy/Export buttons
                    mcp_servers=[shared_mcp_server],
                    model=settings.available_models[0],
                )

                # Cache the new agent
                if settings.enable_agent_caching and gui_agent_cache:
                    gui_agent_cache.cache_agent(
                        model=settings.available_models[0],
                        instructions=get_enhanced_agent_instructions(),
                        mcp_servers=[shared_mcp_server],
                        agent=analysis_agent,
                    )

            # Log agent creation time
            agent_creation_time = time.perf_counter() - agent_creation_start
            performance_monitor.log_agent_creation_time(agent_creation_time)

            # Log cache hit rate
            if settings.enable_agent_caching and gui_agent_cache:
                gui_cache_stats = gui_agent_cache.get_cache_stats()
                performance_monitor.log_cache_hit_rate(gui_cache_stats["hit_rate"])

            # Run the financial analysis agent with the direct prompt
            result = await Runner.run(
                analysis_agent, prompt_data["user_prompt"], session=shared_session
            )

            # Extract the response
            response_text = str(result.final_output)

        except Exception as e:
            logger.error(f"AI model call failed: {e}")
            performance_monitor.log_error("ai_model_call", f"AI model call failed: {str(e)}")
            response_text = f"Error: Unable to process request. {str(e)}"

        # Extract token count from OpenAI response metadata
        token_count = None
        input_tokens = None
        output_tokens = None

        if result and hasattr(result, "metadata") and result.metadata:
            # Try to extract token information from OpenAI response metadata
            if hasattr(result.metadata, "get"):
                token_count = result.metadata.get("tokenCount")
                input_tokens = result.metadata.get("inputTokens")
                output_tokens = result.metadata.get("outputTokens")
            elif hasattr(result.metadata, "usage"):
                # Handle OpenAI usage object format
                usage = result.metadata.usage
                if hasattr(usage, "total_tokens"):
                    token_count = usage.total_tokens
                if hasattr(usage, "prompt_tokens"):
                    input_tokens = usage.prompt_tokens
                if hasattr(usage, "completion_tokens"):
                    output_tokens = usage.completion_tokens

        # Create response metadata with timing and token information
        response_metadata = ResponseMetadata(
            model=settings.available_models[0],
            timestamp=datetime.now().isoformat(),
            processing_time=None,  # Will be set by middleware
            request_id=request_id,
            token_count=token_count,
        )

        # Log performance metrics for baseline measurement and monitoring
        logger.info(f"Performance metrics - Request processed, Request ID: {request_id}")

        # Log token usage if available in metadata
        if token_count:
            logger.info(
                f"Token usage - Input: {input_tokens or 'N/A'}, Output: {output_tokens or 'N/A'}, Total: {token_count}"
            )

        log_api_response(logger, 200, request_id=request_id)

        return ChatResponse(response=response_text, metadata=response_metadata)

    except HTTPException:
        raise
    except Exception as e:
        log_api_response(logger, 500, request_id=request_id)
        logger.error(
            "💥 Unhandled exception in chat endpoint: %s - %s",
            type(e).__name__,
            str(e),
            extra={
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

        # Log CLI MCP server initialization
        mcp_start = time.time()
        async with server:
            mcp_init_time = time.time() - mcp_start
            mcp_server_monitor.log_health_check("cli_mcp_server", True, mcp_init_time)
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
                        # Start timing for performance metrics
                        start_time = time.perf_counter()
                        agent_creation_start = time.perf_counter()

                        # Get or create agent with caching
                        analysis_agent = None
                        if settings.enable_agent_caching and cli_agent_cache:
                            # Try to get cached agent
                            instructions = get_enhanced_agent_instructions()
                            analysis_agent = cli_agent_cache.get_cached_agent(
                                model=settings.available_models[0],
                                instructions=instructions,
                                mcp_servers=[server],
                            )

                        if analysis_agent is None:
                            # Create new agent
                            analysis_agent = Agent(
                                name="Financial Analysis Agent",
                                instructions=get_enhanced_agent_instructions(),
                                tools=[],  # Removed save_analysis_report - superseded by GUI Copy/Export buttons
                                mcp_servers=[server],
                                model=settings.available_models[0],
                            )

                            # Cache the new agent
                            if settings.enable_agent_caching and cli_agent_cache:
                                cli_agent_cache.cache_agent(
                                    model=settings.available_models[0],
                                    instructions=get_enhanced_agent_instructions(),
                                    mcp_servers=[server],
                                    agent=analysis_agent,
                                )

                        # Log agent creation time
                        agent_creation_time = time.perf_counter() - agent_creation_start
                        performance_monitor.log_agent_creation_time(agent_creation_time)

                        # Log cache hit rate
                        if settings.enable_agent_caching and cli_agent_cache:
                            cli_cache_stats = cli_agent_cache.get_cache_stats()
                            performance_monitor.log_cache_hit_rate(cli_cache_stats["hit_rate"])

                        # Run the financial analysis agent with the direct prompt
                        result = await Runner.run(
                            analysis_agent, prompt_data["user_prompt"], session=cli_session
                        )

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
                        performance_monitor.log_error(
                            "cli_ai_model_call", f"CLI AI model call failed: {str(e)}"
                        )

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
