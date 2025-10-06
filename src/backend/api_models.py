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


class ResponseMetadata(BaseModel):
    """Metadata for API responses including timing and model information."""

    model: str
    timestamp: str
    processing_time: Optional[float] = Field(None, alias="processingTime")
    request_id: Optional[str] = Field(None, alias="requestId")
    token_count: Optional[int] = Field(None, alias="tokenCount")  # Deprecated: use input/output tokens
    input_tokens: Optional[int] = Field(None, alias="inputTokens")
    output_tokens: Optional[int] = Field(None, alias="outputTokens")

    model_config = ConfigDict(populate_by_name=True, alias_generator=None)
