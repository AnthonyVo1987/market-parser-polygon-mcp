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
from typing import List

import gradio as gr
from agents import SQLiteSession

# Import CLI core functions (no duplication!)
try:
    # Try relative imports first (when run as module)
    from .cli import initialize_persistent_agent, process_query
    from .config import settings
except ImportError:
    # Fallback to absolute imports (when run directly)
    from backend.cli import initialize_persistent_agent, process_query
    from backend.config import settings

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
        Streaming response text chunks

    Architecture Pattern:
        User Input → Gradio UI → chat_with_agent() → process_query() (CLI core)
    """
    try:
        # Call shared CLI processing function (core business logic - no duplication)
        result = await process_query(agent, session, message)

        # Extract response
        response_text = str(result.final_output)

        # Gradio streaming: yield progressive chunks for better UX
        # Split by sentences for natural streaming
        sentences = response_text.replace(". ", ".|").split("|")
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
