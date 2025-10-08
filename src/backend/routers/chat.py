"""Chat router for the Market Parser application."""

import time
import uuid
from datetime import datetime
from typing import Optional

from agents import Runner
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..api_models import ResponseMetadata
from ..config import settings
from ..dependencies import get_session
from ..services import create_agent
from ..utils.token_utils import (
    extract_token_count_from_context_wrapper,
    extract_token_usage_from_context_wrapper,
)

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


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


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Process a financial query and return the response using direct prompts."""
    # Get shared resources from dependency injection
    shared_session = get_session()

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
            # Get or create agent using factory function
            analysis_agent = create_agent()

            # Run the financial analysis agent with the user message
            result = await Runner.run(analysis_agent, stripped_message, session=shared_session)

            # Extract the response
            response_text = str(result.final_output)

        except Exception as e:
            response_text = f"Error: Unable to process request. {str(e)}"

        # Extract token data using official OpenAI Agents SDK
        token_usage = extract_token_usage_from_context_wrapper(result)

        # Extract individual token counts
        token_count = token_usage.get("total_tokens") if token_usage else None
        input_tokens = token_usage.get("input_tokens") if token_usage else None
        output_tokens = token_usage.get("output_tokens") if token_usage else None
        cached_input_tokens = token_usage.get("cached_input_tokens") if token_usage else None
        cached_output_tokens = token_usage.get("cached_output_tokens") if token_usage else None

        # Calculate processing time
        processing_time = time.perf_counter() - start_time

        # Create response metadata with timing and token information
        response_metadata = ResponseMetadata(
            model=settings.available_models[0],
            timestamp=datetime.now().isoformat(),
            processingTime=processing_time,
            requestId=request_id,
            tokenCount=token_count,  # Deprecated: kept for backward compatibility
            inputTokens=input_tokens,
            outputTokens=output_tokens,
            cachedInputTokens=cached_input_tokens,
            cachedOutputTokens=cached_output_tokens,
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
