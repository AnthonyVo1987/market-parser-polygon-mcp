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
from ..dependencies import get_mcp_server, get_session
from ..services import create_agent, create_polygon_mcp_server

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
    shared_mcp_server = get_mcp_server()
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

            # MCP server health check and error recovery
            if shared_mcp_server is None:
                shared_mcp_server = create_polygon_mcp_server()
                await shared_mcp_server.__aenter__()  # pylint: disable=unnecessary-dunder-call

            # Get or create agent using factory function
            analysis_agent = create_agent(shared_mcp_server)

            # Run the financial analysis agent with the user message
            result = await Runner.run(analysis_agent, stripped_message, session=shared_session)

            # Extract the response
            response_text = str(result.final_output)

        except Exception as e:
            response_text = f"Error: Unable to process request. {str(e)}"

        # Extract token count from OpenAI response metadata
        token_count = None

        if result and hasattr(result, "metadata") and result.metadata:
            # Try to extract token information from OpenAI response metadata
            if hasattr(result.metadata, "get"):
                token_count = result.metadata.get("tokenCount")
            elif hasattr(result.metadata, "usage"):
                # Handle OpenAI usage object format
                usage = result.metadata.usage
                if hasattr(usage, "total_tokens"):
                    token_count = usage.total_tokens
                # Token usage tracking removed for performance

        # Calculate processing time
        processing_time = time.perf_counter() - start_time

        # Create response metadata with timing and token information
        response_metadata = ResponseMetadata(
            model=settings.available_models[0],
            timestamp=datetime.now().isoformat(),
            processingTime=processing_time,
            requestId=request_id,
            tokenCount=token_count,
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
