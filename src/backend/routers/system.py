"""System status router for the Market Parser application."""

from fastapi import APIRouter, HTTPException, status

from ..api_models import SystemMetrics, SystemStatusResponse

router = APIRouter(prefix="/api/v1/system", tags=["System"])


@router.get("/status", response_model=SystemStatusResponse)
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
