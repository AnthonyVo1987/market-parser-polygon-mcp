"""
API Models for FastAPI Prompt Templates System

This module defines Pydantic models for request/response validation and documentation
for the FastAPI endpoints that expose PromptTemplateManager functionality.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

# AnalysisIntent removed as part of direct prompt system removal

# AnalysisType enum removed as part of direct prompt migration


# PromptMode enum removed as part of direct prompt migration


# Template Management Models


# TemplateListResponse removed as part of direct prompt migration


# GeneratePromptRequest removed as part of direct prompt migration


# GeneratePromptResponse removed as part of direct prompt migration


# Chat Analysis Models


class ChatMessage(BaseModel):
    """Chat message model"""

    content: str
    role: str = "user"
    timestamp: Optional[datetime] = None


# ChatAnalysisRequest removed as part of direct prompt migration


# ChatAnalysisResponse removed as part of direct prompt migration


# System Status Models


class SystemHealthResponse(BaseModel):
    """System health check response"""

    status: str = "healthy"
    message: str = "Financial Analysis API is running"
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"


class SystemMetrics(BaseModel):
    """System metrics and status"""

    api_version: str = "1.0.0"
    prompt_templates_loaded: int
    supported_analysis_types: List[str]
    uptime_seconds: Optional[float] = None
    last_restart: Optional[datetime] = None


class SystemStatusResponse(BaseModel):
    """System status response"""

    status: str
    metrics: SystemMetrics
    timestamp: datetime = Field(default_factory=datetime.now)


# Error Models


class ErrorDetail(BaseModel):
    """Error detail information"""

    type: str
    message: str
    field: Optional[str] = None


class APIErrorResponse(BaseModel):
    """Standard API error response"""

    error: str
    detail: Union[str, List[ErrorDetail]]
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)


class ValidationErrorResponse(BaseModel):
    """Validation error response"""

    message: str = "Validation error"
    errors: List[ErrorDetail]
    timestamp: datetime = Field(default_factory=datetime.now)


# Button-specific Models (for React frontend integration)


# ButtonAnalysisRequest removed as part of direct prompt migration


# ButtonAnalysisResponse removed as part of direct prompt migration


# Utility Models


# AnalysisTypeDetectionRequest removed as part of direct prompt migration


# AnalysisTypeDetectionResponse removed as part of direct prompt migration


class TickerExtractionRequest(BaseModel):
    """Request for ticker extraction from text"""

    text: str = Field(..., min_length=1)
    chat_history: Optional[List[ChatMessage]] = None


# Success Response Models


class SuccessResponse(BaseModel):
    """Generic success response"""

    success: bool = True
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


# ====== AI MODEL SELECTION MODELS ======


class CustomModel(BaseModel):
    """Base model with custom configuration for all API models"""

    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True, json_schema_extra={"example": {}}
    )


class AIModelId(str, Enum):
    """Enum for available AI models (GPT-5 only)"""

    GPT_5_NANO = "gpt-5-nano"
    # Removed GPT_5_MINI, GPT_4O and GPT_4O_MINI


class ResponseMetadata(BaseModel):
    """Metadata for API responses including timing and model information."""

    model: str
    timestamp: str
    processing_time: Optional[float] = Field(None, alias="processingTime")
    request_id: Optional[str] = Field(None, alias="requestId")
    token_count: Optional[int] = Field(None, alias="tokenCount")

    model_config = ConfigDict(populate_by_name=True, alias_generator=None)


class AIModel(CustomModel):
    """AI Model information with validation"""

    id: AIModelId = Field(..., description="Model identifier")
    name: str = Field(..., description="Display name", min_length=1, max_length=50)
    description: Optional[str] = Field(None, description="Model description", max_length=200)
    is_default: bool = Field(False, description="Whether this is the default model")
    cost_per_1k_tokens: Optional[float] = Field(None, ge=0, description="Cost per 1000 tokens")
    max_tokens: Optional[int] = Field(None, gt=0, description="Maximum tokens supported")

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is properly formatted"""
        return v.strip()


class ModelListResponse(CustomModel):
    """Response for listing available models"""

    models: List[AIModel]
    current_model: AIModelId
    total_count: int = Field(..., ge=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ModelSelectionRequest(CustomModel):
    """Request for selecting a model with validation"""

    model_id: AIModelId = Field(..., description="Model ID to select")


class ModelSelectionResponse(CustomModel):
    """Response for model selection"""

    success: bool
    message: str = Field(..., min_length=1)
    selected_model: AIModelId
    previous_model: Optional[AIModelId] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
