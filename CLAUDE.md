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
- **Web GUI interface**: `uv run chat_ui.py` (opens at <http://127.0.0.1:7860>)

### Testing

- **Run tests**: `uv run pytest` (pytest is in dev dependencies)
- **Run specific test**: `uv run pytest path/to/test_file.py`
- **Run integration tests**: `uv run pytest test_*integration*.py`
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

2. **chat_ui.py**: Enhanced Gradio web interface with comprehensive features
   - 🧠 **FSM-Driven State Management** - Robust workflow with state transitions
   - 📊 **Structured Stock Analysis** - Dedicated buttons for Snapshot, S&R, Technical Analysis  
   - 🎯 **Context-Aware Prompts** - Intelligent ticker extraction and structured prompts
   - ⏳ **Real-time Processing Status** - Loading states with step-by-step progress
   - 🛡️ **Advanced Error Handling** - User-friendly messages and graceful recovery
   - 📈 **Enhanced Data Display** - DataFrames with confidence scoring and warnings
   - 🔍 **Debug Monitoring** - FSM state tracking and system diagnostics
   - 💾 **Export Functionality** - Enhanced markdown export with detailed formatting
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

```text
"You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. Use the latest data available. Always double check your math. For any questions about the current date, use the 'get_today_date' tool. For long or complex queries, break the query into logical subtasks and process each subtask in order."
```

## File Structure

- `market_parser_demo.py` - CLI application
- `chat_ui.py` - Web GUI application (primary enhanced version)
- `chat_ui_enhanced.py`, `chat_ui_final.py` - Archived GUI versions
- `stock_data_fsm/` - Finite State Machine module for GUI state management
  - `states.py` - Application states enum and context data classes
  - `transitions.py` - State transition rules and validation logic
  - `manager.py` - Main FSM controller with transition orchestration
  - `tests/` - Comprehensive test suite for FSM components
- `prompt_templates.py` - Structured prompt templates for analysis types
- `response_parser.py` - Response parsing utilities for structured data extraction
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Lock file for reproducible builds
- `docs/` - Documentation including feature specifications and deployment guides
- `test_*.py` - Test files including integration and unit tests
- `images/` - Project assets

## Development Patterns

### MCP Server Integration
The project uses the Polygon.io MCP server via `uvx` for real-time financial data access. The `create_polygon_mcp_server()` function in `market_parser_demo.py:16` handles server initialization and connection management.

### State Management (GUI)
The `stock_data_fsm` module implements a deterministic finite state machine for robust GUI workflow management:
- States are defined in `stock_data_fsm/states.py:12` with `AppState` enum
- Transitions managed by `StateManager` class in `stock_data_fsm/manager.py:25`
- Context data flows through `StateContext` objects for stateful operations

### Agent Configuration
Both CLI and GUI share identical agent setup with:
- Model: `gpt-5-nano` via OpenAI Responses API
- System prompt focused on financial analysis accuracy
- Token cost tracking via `TokenCostTracker` class

### Testing Strategy
- Unit tests for FSM components in `stock_data_fsm/tests/`
- Integration tests: `test_integration.py` and `test_actual_integration.py`
- Module-specific tests: `test_prompt_templates.py`, `test_response_parser.py`

## Future Development

The `docs/FEATURE_SCOPE_STOCK_DATA_GUI.md` contains detailed specifications for planned GUI enhancements including:

- Structured data display components
- Finite State Machine architecture for button-triggered actions
- Technical indicator displays
- Support/resistance level visualization

When implementing new features, refer to existing patterns in the shared agent configuration and cost tracking systems.

## Important Development Notes

- **Environment Setup**: Create `.env` file with required API keys before running applications (see template in Required Environment Variables section)
- **External Dependencies**: The Polygon.io MCP server requires `uvx` to be available in the system PATH
- **Architecture Preservation**: All file modifications during development should preserve the FSM state management patterns
- **Cost Tracking**: Token cost tracking is enabled by default - check `TokenCostTracker` usage when adding new agent interactions
- **Model Configuration**: Default model is `gpt-5-nano` but can be overridden via `OPENAI_MODEL` environment variable