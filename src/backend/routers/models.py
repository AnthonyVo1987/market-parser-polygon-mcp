"""Models router for the Market Parser application."""

from fastapi import APIRouter, Depends, HTTPException, status

from ..api_models import (
    AIModel,
    AIModelId,
    ModelListResponse,
    ModelSelectionResponse,
)
from ..config import settings

router = APIRouter(prefix="/api/v1/models", tags=["AI Models"])


async def valid_model_id(model_id: AIModelId) -> AIModelId:
    """Validate that the requested model exists and is available"""
    if model_id.value not in settings.available_models:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid model ID: {model_id.value}"
        )
    return model_id


@router.get(
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


@router.post(
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