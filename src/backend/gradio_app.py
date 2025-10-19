"""Gradio ChatInterface for Market Parser.

This module provides a Gradio-based UI for Market Parser.
Following the same architecture pattern: import and call CLI core logic.

Architecture:
    CLI Core (cli.py) → process_query() → Gradio UI wrapper

Pattern: Wrap CLI core, no duplication

Usage:
    uv run python src/backend/gradio_app.py

Access: http://127.0.0.1:8000
"""

import asyncio
from typing import List

import gradio as gr
from agents import SQLiteSession

# Import CLI core functions (no duplication!)
try:
    # Try relative imports first (when run as module)
    from .cli import initialize_persistent_agent, process_query_with_footer
    from .config import settings
except ImportError:
    # Fallback to absolute imports (when run directly)
    from backend.cli import initialize_persistent_agent, process_query_with_footer
    from backend.config import settings

# Initialize agent
print("🚀 Initializing Market Parser Gradio Interface...")
session = SQLiteSession(settings.agent_session_name)
agent = initialize_persistent_agent()
print("✅ Agent initialized successfully")


async def chat_with_agent(message: str, history: List):
    """Process financial query using CLI core logic with footer.

    This function wraps the CLI core business logic (process_query_with_footer).
    NO logic duplication - calls shared function that returns complete response.

    Args:
        message: User's financial query
        history: Chat history (auto-managed by Gradio, unused here)

    Yields:
        Streaming response text chunks (with footer already included)

    Architecture Pattern:
        User Input → Gradio UI → chat_with_agent() → process_query_with_footer() (CLI core)
    """
    try:
        # Call CLI core function - returns complete response with footer
        complete_response = await process_query_with_footer(agent, session, message)

        # Gradio streaming: yield complete response to preserve Markdown table structure
        # Note: Sentence-based streaming was splitting on "|" which destroyed Markdown tables
        # since tables use "|" as column separators. Yielding complete response preserves formatting.
        yield complete_response

    except Exception as e:
        # Error handling with informative message
        error_msg = f"❌ Error: Unable to process request.\n\nDetails: {str(e)}"
        yield error_msg


# Create Gradio ChatInterface
demo = gr.ChatInterface(
    fn=chat_with_agent,
    type="messages",  # OpenAI-compatible message format
    chatbot=gr.Chatbot(
        render_markdown=True,      # Explicit Markdown rendering
        line_breaks=True,           # GitHub-flavored Markdown
        sanitize_html=True,         # Security
        height=600                  # Better table visibility
    ),
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

def main():
    """Main entry point for Market Parser Gradio interface.

    This function serves as the entry point for the console script defined
    in pyproject.toml: market-parser-gradio

    Features:
        - PWA (Progressive Web App) support - installable on desktop/mobile
        - Hot Reload - use 'uv run gradio src/backend/gradio_app.py' for dev mode
    """
    print("\n" + "="*60)
    print("🎨 Market Parser Gradio Interface")
    print("="*60)
    print("📍 Server: http://127.0.0.1:8000")
    print("🔄 Hot Reload: Use 'uv run gradio src/backend/gradio_app.py'")
    print("📱 PWA: Install from browser (Chrome/Edge install icon)")
    print("💡 Tip: Changes auto-reload on file save in hot reload mode")
    print("="*60 + "\n")

    demo.launch(
        server_name="127.0.0.1",
        server_port=8000,
        pwa=True,  # ⭐ Enable Progressive Web App functionality
        share=False,
        show_error=True,
        quiet=False,
        show_api=False,
        allowed_paths=[],
    )

if __name__ == "__main__":
    main()
