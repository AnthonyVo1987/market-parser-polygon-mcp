"""Hugging Face Spaces deployment entry point for Market Parser.

This file is specifically for HF Spaces deployment.
It imports and runs the main Gradio app from src/backend/gradio_app.py.

For local development, continue using:
    uv run python src/backend/gradio_app.py
    OR
    uv run market-parser-gradio

This file enables HF Spaces to run the app with cloud-compatible settings.
"""

# Import the demo from our main app
from backend.gradio_app import demo

# Launch with HF Spaces-compatible settings
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Required for HF Spaces (accept external connections)
        server_port=7860,        # HF Spaces default port
        share=False,             # Not needed in HF Spaces (already hosted)
        show_error=True,         # Show errors for debugging
    )
