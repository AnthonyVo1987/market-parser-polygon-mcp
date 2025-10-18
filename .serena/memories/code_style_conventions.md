# Code Style and Conventions

## Python Code Style

### General Conventions
- **Line Length**: 100 characters max (configured in black, isort, pylint)
- **Python Version**: 3.10+ (target: 3.12.3)
- **Formatter**: black with `--line-length 100`
- **Import Sorter**: isort with `--profile black --line-length 100`
- **Linter**: pylint with custom configuration

### Import Organization (isort)
```python
# Standard library imports
import os
import sys
from typing import Dict, List, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rich.console import Console

# First-party imports
from src.backend.config import settings
from src.backend.utils import helpers

# Local imports
from .models import User
```

**Import Sections (in order):**
1. FUTURE
2. STDLIB
3. THIRDPARTY
4. FIRSTPARTY
5. LOCALFOLDER

**Known packages:**
- Third-party: `openai`, `pydantic`, `rich`, `fastapi`, `uvicorn`, `agents`, `gradio`
- First-party: `src`

### Naming Conventions

**Variables and Functions:**
- `snake_case` for variables and functions
- Descriptive names (e.g., `get_stock_quote`, `market_status`)
- Private functions prefixed with `_` (e.g., `_get_tradier_api_key`)

**Classes:**
- `PascalCase` for class names
- Descriptive names (e.g., `AgentService`, `TradierClient`)

**Constants:**
- `UPPER_SNAKE_CASE` for constants
- Defined at module level (e.g., `MAX_RESPONSE_TIME`, `DEFAULT_MODEL`)

**Type Hints:**
- Use type hints for function parameters and return types
- Import from `typing` module
- Example: `def get_quote(symbol: str) -> Dict[str, Any]:`

### Docstrings

**Format:** Generally minimal docstrings for prototyping
- Use docstrings for complex functions only
- Keep them concise and focused
- pylint configured with `missing-docstring` disabled

**Example:**
```python
def get_stock_quote(symbol: str) -> dict:
    """Get real-time stock quote for a symbol."""
    # Implementation
```

### Linting Configuration (.pylintrc)

**Disabled Checks (prototyping-friendly):**
- `missing-docstring` - Docstrings not required for all functions
- `invalid-name` - Flexible naming
- `too-few-public-methods` - Allow simple classes
- `too-many-arguments` - Allow many parameters for config
- `line-too-long` - Handled by black
- `broad-exception-caught` - Allow catching general exceptions

**Line Length:** 100 characters max

**Python Version:** 3.10

### Code Organization

**File Structure:**
```
src/backend/
├── main.py              # FastAPI app, endpoints, startup
├── cli.py              # CLI interface (CORE BUSINESS LOGIC)
├── gradio_app.py       # Gradio web UI (wraps CLI core)
├── config.py            # Configuration management
├── api_models.py        # Pydantic models for API
├── dependencies.py      # Dependency injection
├── services/           # Business logic
│   └── agent_service.py
├── tools/              # AI agent tools
│   ├── polygon_tools.py
│   └── tradier_tools.py
└── utils/              # Helper functions
```

**Module Organization:**
1. Imports (organized by isort)
2. Constants
3. Helper functions (private with `_` prefix)
4. Public functions
5. Classes (if any)
6. Main execution (if `__main__`)

## Git Conventions

### Commit Messages
```
[CATEGORY] Brief description

- Detailed change 1
- Detailed change 2
- Test results (if applicable)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Categories:**
- `[FEATURE]` - New features
- `[FIX]` - Bug fixes
- `[REFACTOR]` - Code refactoring
- `[DOCS]` - Documentation updates
- `[TEST]` - Testing updates
- `[PERF]` - Performance improvements
- `[INFRASTRUCTURE]` - Infrastructure/tooling
- `[SERENA]` - Serena memory updates

### Branch Naming
- `main` or `master` - Production branch
- `feature/feature-name` - Feature branches
- `fix/bug-name` - Bug fix branches

## Testing Conventions

### Test File Naming
- CLI tests: `test_cli_regression.sh`
- Test reports: `test-reports/` directory

### Test Prompts
- **Use standardized prompts only** (see `test_prompts.md`)
- **Format**: "Quick Response Needed with minimal tool calls: [query]"
- **Expected response time**: 6-10 seconds
- **Success rate**: 100%

## Quality Standards

### Python Quality
- **Pylint Score**: 10.00/10 (target)
- **Black**: All files formatted
- **isort**: All imports organized
- **Type Hints**: Used where helpful

### Performance Targets
- **Response Time**: < 10s (average ~9.67s)
- **Success Rate**: 100%
- **Gradio UI Load Time**: < 2s

## Gradio UI Conventions

### Component Naming
- Use descriptive names for Gradio components
- Follow Gradio best practices for ChatInterface
- Keep UI configuration in gradio_app.py

### UI Code Organization
```python
# 1. Imports
from gradio import ChatInterface
from .cli import initialize_persistent_agent, process_query_with_footer

# 2. Agent initialization
session = SQLiteSession("gradio_session")
agent = initialize_persistent_agent()

# 3. Handler functions
async def chat_with_agent(message, history):
    # Implementation
    pass

# 4. UI configuration
demo = ChatInterface(
    fn=chat_with_agent,
    title="Market Parser",
    # ... other config
)

# 5. Launch
if __name__ == "__main__":
    demo.launch()
```

### Gradio Best Practices
- **Wrap CLI core logic**: Never duplicate business logic
- **Stream responses**: Use `yield` for real-time updates
- **Keep it simple**: Gradio UI should be mostly configuration
- **Follow async patterns**: Use async/await for API calls

## Architecture Patterns

### CLI = Core, Gradio = Wrapper
```python
# CLI core (cli.py) - Single source of truth
def initialize_persistent_agent():
    """Create and configure agent."""
    pass

async def process_query_with_footer(agent, session, query):
    """Process query and return complete response with footer."""
    pass

# Gradio wrapper (gradio_app.py) - Import and call
from .cli import initialize_persistent_agent, process_query_with_footer

agent = initialize_persistent_agent()

async def chat_with_agent(message, history):
    response = await process_query_with_footer(agent, session, message)
    yield response
```

**Key Principle**: Zero code duplication between CLI and Gradio

## Notes

- **React/TypeScript removed**: React frontend completely retired (Oct 17, 2025)
- **Gradio only**: Gradio is the only web interface
- **No Node.js frontend**: package.json used for backend tooling only (markdown linting)
- **Python-first**: All UI code is Python (Gradio framework)
