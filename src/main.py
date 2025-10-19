"""Market Parser main entry point.

This file enables the standard Python convention:
    uv run main.py

It imports and calls the CLI main() function from the backend package.

Architecture:
    src/main.py → backend.cli.main() → CLI business logic

See Also:
    - backend.cli.main() - CLI entry point
    - backend.gradio_app.main() - Gradio entry point (if implemented)
"""

from backend.cli import main

if __name__ == "__main__":
    main()
