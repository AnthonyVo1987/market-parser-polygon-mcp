"""Routers package for the Market Parser application."""

from .chat import router as chat_router
from .health import router as health_router
from .system import router as system_router

__all__ = ["chat_router", "health_router", "system_router"]
