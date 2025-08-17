# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market Parser is a Python CLI and web GUI application for natural language financial queries using the Polygon.io MCP server and OpenAI's gpt-5-nano via the Pydantic AI Agent Framework. The application allows users to ask questions about stock market data in natural language and receive formatted responses.

## Development Environment

This project uses `uv` for dependency management and Python package execution. All dependencies are managed through `pyproject.toml`.

### Required Environment Variables

Create a `.env` file in the project root with:
```env
POLYGON_API_KEY=your_polygon_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
# Optional: pricing for cost estimates (USD)
OPENAI_GPT5_NANO_INPUT_PRICE_PER_1M=0.10
OPENAI_GPT5_NANO_OUTPUT_PRICE_PER_1M=0.40
```

## Common Development Commands

### Running the Application
- **CLI interface**: `uv run market_parser_demo.py`
- **Web GUI interface**: `uv run chat_ui.py` (opens at http://127.0.0.1:7860)

### Testing
- **Run tests**: `uv run pytest` (pytest is in dev dependencies)
- **Install dev dependencies**: `uv install --dev`

### Environment Management
- **Install dependencies**: `uv install`
- **Update dependencies**: `uv lock --upgrade`
- **Check environment**: `uv --version` and verify `.env` file exists

## Code Architecture

### Core Components

1. **market_parser_demo.py**: CLI application entry point
   - Contains `TokenCostTracker` class for usage/cost tracking
   - Implements `create_polygon_mcp_server()` factory function
   - Main async CLI loop with Rich console formatting

2. **chat_ui.py**: Gradio web interface
   - Reuses server factory and cost tracking from CLI
   - Implements async message handling for web interface
   - Provides chat export functionality

### Key Architectural Patterns

- **MCP Server Integration**: Uses Pydantic AI's MCP server integration to connect with Polygon.io
- **Async Agent Framework**: Built on Pydantic AI with OpenAI Responses API model
- **Cost Tracking**: Comprehensive token usage and cost tracking across sessions
- **Shared Components**: CLI and GUI share the same agent configuration and MCP server setup

### Dependencies & Technologies

- **Core Framework**: `pydantic-ai-slim[openai,mcp]` for AI agent orchestration
- **Web Interface**: `gradio>=4.0.0` for the GUI
- **CLI Formatting**: `rich` for terminal output formatting
- **Environment**: `python-dotenv` for configuration management
- **External APIs**: Polygon.io MCP server via uvx, OpenAI gpt-5-nano model

### System Prompt Configuration

The agent uses a consistent system prompt across both interfaces:
```
"You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. Use the latest data available. Always double check your math. For any questions about the current date, use the 'get_today_date' tool. For long or complex queries, break the query into logical subtasks and process each subtask in order."
```

## File Structure

- `market_parser_demo.py` - CLI application
- `chat_ui.py` - Web GUI application  
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Lock file for reproducible builds
- `docs/` - Documentation including feature specifications and deployment guides
- `examples/rest/` - Example implementations
- `images/` - Project assets

## Future Development

The `docs/FEATURE_SCOPE_STOCK_DATA_GUI.md` contains detailed specifications for planned GUI enhancements including:
- Structured data display components
- Finite State Machine architecture for button-triggered actions
- Technical indicator displays
- Support/resistance level visualization

When implementing new features, refer to existing patterns in the shared agent configuration and cost tracking systems.