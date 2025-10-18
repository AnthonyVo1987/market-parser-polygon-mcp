# Code Style Conventions - Updated October 2025

**Status:** Current with October 18, 2025 cleanup
**Language:** Python only (React/TypeScript retired)

---

## Python Code Style

### Line Length & Formatting
- **Line Length:** 100 characters (Black standard)
- **Indentation:** 4 spaces (no tabs)
- **Tool:** Black 23.12.0 (auto-formatting)

### Import Organization (isort)
- **Profile:** black
- **Order:** Future → Stdlib → Third-party → First-party → Local
- **Line Length:** 100 characters
- **Tool:** isort 5.13.0

**Example:**
```python
# Future imports
from __future__ import annotations

# Standard library
import asyncio
import json
from typing import Any

# Third-party
import gradio as gr
from openai import AsyncOpenAI
from pydantic import BaseModel

# First-party
from src.backend.config import settings
from src.backend.utils.response_utils import format_response

# Local
from .tools import polygon_tools, tradier_tools
```

### Naming Conventions

| Category | Convention | Examples |
|----------|-----------|----------|
| Functions | `snake_case` | `process_query`, `format_response` |
| Variables | `snake_case` | `api_key`, `market_status` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Classes | `PascalCase` | `ChatResponse`, `MarketData` |
| Private | `_prefix` | `_format_footer`, `_validate_input` |
| Dunder | `__dunder__` | `__init__`, `__name__` |

### Type Hints

**Enabled for:** `src/backend/*.py` and `src/backend/**/*.py`
**Disabled for:** `tests/` (gradual adoption)

**Examples:**
```python
# Function arguments and return types
async def process_query(
    agent: Agent,
    session: SQLiteSession,
    user_input: str
) -> str:
    """Process a user query and return formatted response."""
    ...

# Variable annotations
api_key: str = settings.openai_api_key
max_retries: int = 3
options_chain: dict[str, Any] = {}

# Optional types
from typing import Optional
result: Optional[str] = None

# Union types
response: str | dict = process_query(...)
```

### Docstrings

**Style:** Google-style docstrings (recommended)

**Function docstring:**
```python
def process_query_with_footer(
    agent: Agent,
    session: SQLiteSession,
    user_input: str
) -> str:
    """Process a financial query and return response with performance metrics.
    
    Args:
        agent: Persistent AI agent instance for this session
        session: SQLite session for maintaining conversation history
        user_input: User's natural language financial query
        
    Returns:
        Complete response including AI answer and performance footer
        
    Raises:
        ValueError: If user_input is empty
        APIError: If API call fails
    """
```

**Class docstring:**
```python
class ChatResponse(BaseModel):
    """Response model for chat operations.
    
    Attributes:
        message: The chat message content
        timestamp: ISO format timestamp
        model: AI model used for response
        tokens: Token usage information
    """
    message: str
    timestamp: str
    model: str
    tokens: dict[str, int]
```

---

## Code Organization Principles

### Single Source of Truth
- **CLI core** (`src/backend/cli.py`) owns ALL business logic
- **Gradio wrapper** (`src/backend/gradio_app.py`) imports and calls CLI functions
- **No duplication** between CLI and Gradio

**Pattern:**
```python
# CLI (src/backend/cli.py) - CORE LOGIC
async def process_query_with_footer(agent, session, user_input):
    """Core business logic."""
    response = await process_query(agent, session, user_input)
    footer = _format_performance_footer(response.metadata)
    return f"{response.text}\n\n{footer}"

# Gradio (src/backend/gradio_app.py) - WRAPPER ONLY
async def chat_with_agent(message, history):
    """Wrapper that calls CLI core."""
    response = await process_query_with_footer(agent, session, message)
    yield response  # Stream to UI
```

### Tool Functions

**Pure functions** that take clear inputs and return clear outputs

```python
# Good: Pure function
def get_stock_price(ticker: str) -> dict[str, float]:
    """Get stock price data."""
    # API call
    return {"open": 150.0, "close": 151.5}

# Bad: Side effects
def get_stock_price(ticker: str) -> None:
    """Get stock price and update global state."""
    global price_cache
    price_cache[ticker] = api_call(ticker)  # Side effect!
```

### Error Handling

**Use specific exceptions, not bare `except:`**

```python
# Good
try:
    response = await api.get_data()
except APIError as e:
    logger.error(f"API error: {e}")
    raise
except TimeoutError:
    logger.warning("Request timeout, retrying...")
    # Retry logic

# Bad
try:
    response = await api.get_data()
except Exception:
    pass  # Silently fails!
```

---

## File Structure Conventions

### Module Layout
```python
"""Module docstring at the top."""

# Imports organized by isort rules
from __future__ import annotations

import asyncio
from typing import Any

from openai import AsyncOpenAI
import gradio as gr

from src.backend.config import settings

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Classes (if any)
class MyClass:
    """Class docstring."""
    pass

# Public functions
async def public_function() -> str:
    """Public function docstring."""
    pass

# Private functions
def _private_function() -> None:
    """Private function docstring."""
    pass

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
```

---

## CLI vs Gradio Code

### CLI (src/backend/cli.py)
- **Focus:** Core business logic, input processing, output formatting
- **I/O:** stdin/stdout (terminal)
- **Error Handling:** User-facing error messages
- **Control:** Interactive loop in `cli_async()`

```python
async def cli_async():
    """Main CLI loop."""
    agent = initialize_persistent_agent()
    session = SQLiteSession("cli_session")
    
    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        
        response = await process_query_with_footer(agent, session, user_input)
        print(response)
```

### Gradio (src/backend/gradio_app.py)
- **Focus:** UI setup, streaming responses
- **I/O:** HTTP (Gradio interface)
- **Error Handling:** Gradio error display
- **Control:** ChatInterface callback

```python
async def chat_with_agent(message, history):
    """Gradio chat callback."""
    response = await process_query_with_footer(agent, session, message)
    yield response  # Stream response
```

**Rule:** Gradio should ONLY call CLI functions, never duplicate logic

---

## Common Patterns

### Async/Await
```python
# Use async for I/O operations
async def get_market_data(ticker: str) -> dict:
    """Fetch market data asynchronously."""
    async with AsyncOpenAI(api_key=settings.openai_api_key) as client:
        response = await client.chat.completions.create(...)
    return response.model_dump()
```

### Context Managers
```python
# Use context managers for resources
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_agent():
    """Manage agent lifecycle."""
    agent = initialize_persistent_agent()
    try:
        yield agent
    finally:
        await agent.cleanup()

# Usage
async with get_agent() as agent:
    response = await process_query(agent, ...)
```

### Type Guards
```python
# Use type guards for safety
from typing import TypeGuard

def is_market_data(obj: Any) -> TypeGuard[dict]:
    """Check if object is market data."""
    return isinstance(obj, dict) and "price" in obj and "timestamp" in obj

# Usage
if is_market_data(response):
    print(response["price"])
```

---

## Performance Considerations

### Don't
```python
# Bad: String concatenation in loops
response = ""
for item in items:
    response += format_item(item)  # Creates new string each time

# Bad: Loading entire file into memory
with open("large_file.txt") as f:
    content = f.read()
    process_all(content)
```

### Do
```python
# Good: Use list join
response = "".join(format_item(item) for item in items)

# Good: Stream processing
with open("large_file.txt") as f:
    for line in f:
        process_line(line)
```

---

## Comments & Documentation

### Comment Policy (Oct 18, 2025)

**Policy 1: No historical comments about retired components**
- **Rationale**: Comments should ONLY describe CURRENT code and architecture. Git history provides historical context.
- **Example**:
  ```python
  # ❌ Bad: Historical commentary
  # Note: This used to call the MCP server but was migrated to Direct API on Oct 2025
  def get_stock_data(ticker: str) -> dict:
      return tradier_api.get_quote(ticker)

  # ✅ Good: Describes current implementation
  def get_stock_data(ticker: str) -> dict:
      """Fetch stock data using Tradier Direct API."""
      return tradier_api.get_quote(ticker)
  ```

**Policy 2: No deprecation notices in code comments**
- **Rationale**: Git commit messages document deprecations. Code comments focus on current functionality.
- **Example**:
  ```python
  # ❌ Bad: Deprecation notice in comments
  # DEPRECATED: Use get_ta_indicators() instead (deprecated Oct 11, 2025)
  # This function will be removed in the next release
  def get_ta_sma(ticker: str) -> float:
      ...

  # ✅ Good: Remove deprecated code entirely, document in git commit
  # (No deprecated function exists in code)
  # Git commit message explains: "Removed deprecated TA tools, use get_ta_indicators()"
  ```

**Policy 3: Comments explain WHY, not WHAT**
- **Rationale**: Code should be self-documenting. Comments add context that code cannot express.

### When to Comment
```python
# Good: Explains WHY, not WHAT
# Polygon API rate limit is 5req/sec, so we batch requests
def batch_stock_requests(tickers: list[str], batch_size: int = 5) -> list:
    ...

# Bad: Explains what the code already shows
# Loop through tickers
for ticker in tickers:
    ...
```

### Log Levels
```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: Detailed info for debugging
logger.debug(f"Processing ticker {ticker}")

# INFO: General progress
logger.info(f"Initialized agent for session {session_id}")

# WARNING: Something unexpected but handled
logger.warning(f"Retrying failed request, attempt {attempt}")

# ERROR: Error that can be recovered
logger.error(f"API error: {error}", exc_info=True)

# CRITICAL: System cannot continue
logger.critical("Database connection failed, shutting down")
```

---

## Git Commit Message Style

**Format:**
```
[TAG] Descriptive message

- Change 1
- Change 2
- Change 3

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Common Tags:**
- `[FEATURE]` - New feature
- `[FIX]` - Bug fix
- `[REFACTOR]` - Code restructuring
- `[CLEANUP]` - Code cleanup, dead code removal
- `[DOCS]` - Documentation updates
- `[TEST]` - Testing updates
- `[PERF]` - Performance improvements

---

## DRY Principle & Helper Modules (Oct 18, 2025)

### Policy: Eliminate Code Duplication

**When to Create Helper Modules:**
- Pattern duplicated 3+ times across the codebase
- Pattern serves a clear, single purpose
- Pattern can be abstracted without over-engineering

**Helper Module Guidelines:**
1. **Single Responsibility** - Each helper does ONE thing well
2. **Type Hints Required** - All functions must have full type annotations
3. **Comprehensive Docstrings** - Explain purpose, parameters, returns, raises, examples
4. **Unit Testable** - Design for easy testing in isolation

**Example: Error Handling Helper (error_utils.py)**
```python
def create_error_response(
    error_type: str,
    message: str,
    status: str = "error",
    details: str | None = None
) -> dict[str, str]:
    """
    Create standardized error response format.

    Single source of truth for error handling across all tool functions.
    Eliminates 20+ duplicate error formatting blocks.

    Args:
        error_type: Category of error (e.g., "API error", "Validation error")
        message: Human-readable error message
        status: Response status (default: "error")
        details: Optional additional error context

    Returns:
        Standardized error dictionary

    Example:
        >>> create_error_response("Validation error", "Invalid ticker format")
        {"status": "error", "error_type": "Validation error", "message": "Invalid ticker format"}
    """
    ...
```

**Refactoring Workflow:**
1. **Identify Duplication** - Find patterns repeated 3+ times
2. **Extract to Helper** - Create centralized helper module
3. **Refactor Call Sites** - Update all tool functions to use helper
4. **Test Thoroughly** - Run full regression suite (39 tests)
5. **Document Impact** - Update memories with code reduction statistics

**Benefits:**
- **Maintainability**: Update logic in ONE place, not 20+ places
- **Consistency**: All functions behave identically
- **Testability**: Helper functions are unit testable
- **Readability**: Tool functions focus on business logic, not boilerplate

---

## Linting & Type Checking

### Run Before Commit
```bash
npm run lint:fix  # Auto-fix code style
uv run mypy src/backend/  # Type check
npm run lint      # Pylint check
```

### Pre-commit Hooks
- Python formatting (Black)
- Import sorting (isort)
- Trailing whitespace removal
- YAML validation
- JSON validation

---

**Last Updated:** October 18, 2025
**Python Version:** 3.12.3
**Status:** Current with cleanup
