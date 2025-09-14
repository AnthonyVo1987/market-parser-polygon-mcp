"""
API Models for FastAPI Prompt Templates System

This module defines Pydantic models for request/response validation and documentation
for the FastAPI endpoints that expose PromptTemplateManager functionality.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class AnalysisType(str, Enum):
    """Analysis types supported by the system"""

    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"


class PromptMode(str, Enum):
    """Response modes for prompts"""

    CONVERSATIONAL = "conversational"


# Template Management Models


class PromptTemplateInfo(BaseModel):
    """Information about a prompt template"""

    template_type: AnalysisType = Field(alias="templateId")
    available: bool = True
    mode: PromptMode = PromptMode.CONVERSATIONAL
    enhanced_formatting: bool = True
    description: Optional[str] = None


class TemplateListResponse(BaseModel):
    """Response for listing available templates"""

    mode: str = "conversational_only"
    templates: Dict[str, PromptTemplateInfo]
    total_count: int


class GeneratePromptRequest(BaseModel):
    """Request model for generating a prompt"""
    
    class Config:
        allow_population_by_field_name = True

    template_type: AnalysisType = Field(alias="templateId")
    ticker: Optional[str] = Field(None, description="Stock ticker symbol (e.g., AAPL)")
    custom_instructions: Optional[str] = Field(None, description="Additional custom instructions")
    mode: PromptMode = PromptMode.CONVERSATIONAL

    @validator("ticker")
    @classmethod
    def validate_ticker(cls, v):
        """Validate ticker symbol format and constraints."""
        if v is not None:
            # Basic ticker validation
            v = v.strip().upper()
            if len(v) < 1 or len(v) > 5:
                raise ValueError("Ticker symbol must be 1-5 characters")
            if not v.isalpha():
                raise ValueError("Ticker symbol must contain only letters")
        return v


class TickerContextInfo(BaseModel):
    """Ticker context information"""

    symbol: str
    company_name: Optional[str] = None
    sector: Optional[str] = None
    last_mentioned: bool = False
    confidence: float
    source: str


class GeneratePromptResponse(BaseModel):
    """Response for prompt generation"""

    prompt: str
    ticker_context: TickerContextInfo
    template_type: AnalysisType
    mode: PromptMode
    generated_at: datetime = Field(default_factory=datetime.now)


# Chat Analysis Models


class ChatMessage(BaseModel):
    """Chat message model"""

    content: str
    role: str = "user"
    timestamp: Optional[datetime] = None


class ChatAnalysisRequest(BaseModel):
    """Request model for chat analysis"""

    message: str = Field(..., min_length=2, description="User query or message")
    chat_history: Optional[List[ChatMessage]] = Field(
        default=None, description="Previous chat history"
    )
    analysis_type: Optional[AnalysisType] = Field(
        None, description="Specific analysis type if known"
    )

    @validator("message")
    @classmethod
    def validate_message(cls, v):
        """Validate message content length and format."""
        if len(v.strip()) < 2:
            raise ValueError("Message must be at least 2 characters long")
        return v.strip()


class ChatAnalysisResponse(BaseModel):
    """Response for chat analysis"""

    response: str
    analysis_type: Optional[AnalysisType] = None
    ticker_detected: Optional[str] = None
    confidence: float = 1.0
    follow_up_questions: Optional[List[str]] = None
    generated_at: datetime = Field(default_factory=datetime.now)
    success: bool = True


class FollowUpQuestionsResponse(BaseModel):
    """Response for follow-up questions"""

    questions: List[str]
    context: Optional[str] = None
    analysis_type: Optional[AnalysisType] = None


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
    supported_analysis_types: List[AnalysisType]
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


class ButtonAnalysisRequest(BaseModel):
    """Request model for button-triggered analysis"""

    ticker: str = Field(..., description="Stock ticker symbol")
    analysis_type: AnalysisType

    @validator("ticker")
    @classmethod
    def validate_ticker(cls, v):
        """Validate ticker symbol format for button analysis requests."""
        v = v.strip().upper()
        if len(v) < 1 or len(v) > 5:
            raise ValueError("Ticker symbol must be 1-5 characters")
        if not v.isalpha():
            raise ValueError("Ticker symbol must contain only letters")
        return v


class ButtonAnalysisResponse(BaseModel):
    """Response for button-triggered analysis"""

    analysis: str
    ticker: str
    analysis_type: AnalysisType
    generated_at: datetime = Field(default_factory=datetime.now)
    success: bool = True


# Utility Models


class AnalysisTypeDetectionRequest(BaseModel):
    """Request for detecting analysis type from user input"""

    user_input: str = Field(..., min_length=1)


class AnalysisTypeDetectionResponse(BaseModel):
    """Response for analysis type detection"""

    detected_type: Optional[AnalysisType] = None
    confidence: float = 0.0
    reasoning: Optional[str] = None


class TickerExtractionRequest(BaseModel):
    """Request for ticker extraction from text"""

    text: str = Field(..., min_length=1)
    chat_history: Optional[List[ChatMessage]] = None


class TickerExtractionResponse(BaseModel):
    """Response for ticker extraction"""

    ticker_context: TickerContextInfo
    extraction_successful: bool
    reasoning: Optional[str] = None


# Success Response Models


class SuccessResponse(BaseModel):
    """Generic success response"""

    success: bool = True
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)