"""Hugging Face Spaces deployment entry point for Market Parser.

This file is specifically for HF Spaces deployment.
It imports and runs the main Gradio app from src/backend/gradio_app.py.

For local development, continue using:
    uv run python src/backend/gradio_app.py
    OR
    uv run market-parser-gradio

This file enables HF Spaces to run the app with cloud-compatible settings.
"""

import sys
from pathlib import Path

# Add src directory to Python path so we can import backend
# This is necessary for HF Spaces deployment where app.py runs from project root
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

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
