"""Gradio ChatInterface for Market Parser.

This module provides a Gradio-based UI alternative to the React frontend.
Following the same architecture pattern: import and call CLI core logic.

Architecture:
    CLI Core (cli.py) → process_query() → Gradio UI wrapper

Pattern: Same as React frontend - wrap CLI core, no duplication

Usage:
    uv run python src/backend/gradio_app.py

Access: http://127.0.0.1:7860
"""

import asyncio
import time
from typing import List

import gradio as gr
from agents import SQLiteSession

# Import CLI core functions (no duplication!)
try:
    # Try relative imports first (when run as module)
    from .cli import initialize_persistent_agent, process_query
    from .config import settings
    from .utils.token_utils import extract_token_usage_from_context_wrapper
except ImportError:
    # Fallback to absolute imports (when run directly)
    from backend.cli import initialize_persistent_agent, process_query
    from backend.config import settings
    from backend.utils.token_utils import extract_token_usage_from_context_wrapper

# Initialize agent (same pattern as FastAPI)
print("🚀 Initializing Market Parser Gradio Interface...")
session = SQLiteSession(settings.agent_session_name)
agent = initialize_persistent_agent()
print("✅ Agent initialized successfully")


async def chat_with_agent(message: str, history: List):
    """Process financial query using existing CLI core logic.

    This function wraps the CLI core business logic (process_query) to provide
    a Gradio-compatible interface. NO logic duplication - calls shared function.

    Args:
        message: User's financial query
        history: Chat history (auto-managed by Gradio, unused here)

    Yields:
        Streaming response text chunks with performance metrics footer

    Architecture Pattern:
        User Input → Gradio UI → chat_with_agent() → process_query() (CLI core)
    """
    try:
        # Measure processing time for performance metrics
        start_time = time.perf_counter()

        # Call shared CLI processing function (core business logic - no duplication)
        result = await process_query(agent, session, message)

        # Calculate processing time
        processing_time = time.perf_counter() - start_time

        # Extract response text
        response_text = str(result.final_output)

        # Extract token usage using shared CLI utility (zero duplication)
        token_usage = extract_token_usage_from_context_wrapper(result)

        # Get model name from settings
        model_name = settings.available_models[0]  # "gpt-5-nano"

        # Format performance metrics footer (matching CLI format)
        footer = "\n\nPerformance Metrics:\n"
        footer += f"   Response Time: {processing_time:.3f}s\n"

        # Add token information if available
        if token_usage:
            token_count = token_usage.get("total_tokens")
            input_tokens = token_usage.get("input_tokens")
            output_tokens = token_usage.get("output_tokens")
            cached_input = token_usage.get("cached_input_tokens", 0)
            cached_output = token_usage.get("cached_output_tokens", 0)

            if token_count:
                footer += f"   Tokens Used: {token_count:,}"

                if input_tokens and output_tokens:
                    footer += f" (Input: {input_tokens:,}, Output: {output_tokens:,})"

                    # Show cache hit information if tokens were cached
                    if cached_input > 0 or cached_output > 0:
                        cache_parts = []
                        if cached_input > 0:
                            cache_parts.append(f"Cached Input: {cached_input:,}")
                        if cached_output > 0:
                            cache_parts.append(f"Cached Output: {cached_output:,}")
                        footer += f" | {', '.join(cache_parts)}"

                footer += "\n"

        # Add model information
        footer += f"   Model: {model_name}\n"

        # Append footer to response
        response_with_footer = response_text + footer

        # Gradio streaming: yield progressive chunks for better UX
        # Split by sentences for natural streaming
        sentences = response_with_footer.replace(". ", ".|").split("|")
        accumulated = ""

        for sentence in sentences:
            accumulated += sentence
            yield accumulated
            # Small delay for smooth streaming effect
            await asyncio.sleep(0.05)

    except Exception as e:
        # Error handling with informative message
        error_msg = f"❌ Error: Unable to process request.\n\nDetails: {str(e)}"
        yield error_msg


# Create Gradio ChatInterface
demo = gr.ChatInterface(
    fn=chat_with_agent,
    type="messages",  # OpenAI-compatible message format
    title="🏦 Market Parser - Financial Analysis",
    description=(
        "Ask natural language questions about stocks, options, and market data. "
        "Powered by GPT-5-Nano and real-time data from Polygon.io and Tradier."
    ),
    examples=[
        ["What is Tesla's current stock price?"],
        ["Show me NVDA technical analysis with support and resistance levels"],
        ["Get SPY call options chain for next month"],
        ["Compare AMD and NVDA stock performance"],
        ["What are the latest market trends for WDC?"],
    ],
)

if __name__ == "__main__":
    # Launch Gradio interface
    print("\n" + "="*60)
    print("🎨 Market Parser Gradio Interface")
    print("="*60)
    print("📍 Server: http://127.0.0.1:7860")
    print("📖 Docs: See research_task_plan.md for details")
    print("🔄 Hot Reload: Use 'gradio src/backend/gradio_app.py'")
    print("="*60 + "\n")

    demo.launch(
        server_name="127.0.0.1",  # Localhost only (dev mode)
        server_port=7860,  # Gradio default port (separate from FastAPI:8000, React:3000)
        share=False,  # No public URL (dev mode)
        show_error=True,  # Show error messages in UI
        quiet=False,  # Show startup logs
        favicon_path=None,  # Use default Gradio favicon
        show_api=False,  # Don't show API documentation
        allowed_paths=[],  # No file serving (security)
    )
