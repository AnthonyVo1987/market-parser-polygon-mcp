"""Chat router for the Market Parser application."""

import time
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..api_models import ResponseMetadata
from ..cli import process_query_with_footer
from ..dependencies import get_agent, get_session

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
    """Process a financial query and return the complete response with footer.

    Following the architecture principle "CLI = core, GUI = wrapper":
    - Calls process_query_with_footer() from CLI core
    - Returns complete response with performance metrics footer included
    - No metadata extraction needed - footer is part of response text
    """
    # Get shared resources from dependency injection
    shared_session = get_session()
    shared_agent = get_agent()

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

    try:
        # Call CLI core function - returns complete response with footer
        complete_response = await process_query_with_footer(
            shared_agent,
            shared_session,
            stripped_message
        )

        # Return complete response (footer already included in text)
        return ChatResponse(response=complete_response, metadata=None)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {str(e)}"
        ) from e
