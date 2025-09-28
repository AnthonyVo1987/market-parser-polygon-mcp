"""Health check router for the Market Parser application."""

from fastapi import APIRouter

from ..api_models import SystemHealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=SystemHealthResponse)
@router.get("/api/v1/health", response_model=SystemHealthResponse)
async def health_check():
    """Health check endpoint."""
    return SystemHealthResponse(
        status="healthy", message="Financial Analysis API is running", version="1.0.0"
    )