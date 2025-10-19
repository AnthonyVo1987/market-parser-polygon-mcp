# Code Style Conventions - October 2025

**Last Updated:** October 18, 2025
**Architecture:** Python-only full-stack (React and FastAPI removed)
**Python Version:** 3.10+

---

## Python Code Style

### PEP 8 Compliance

- **Follow:** PEP 8 (Python Enhancement Proposal 8)
- **Tool:** pylint, black, isort
- **Line Length:** 88 characters (Black default)
- **Indentation:** 4 spaces (NOT tabs)

### Naming Conventions

```python
# Functions and variables: snake_case
def get_stock_price(ticker):
    user_input = input()
    return result

# Classes: PascalCase
class MarketAnalyzer:
    pass

# Constants: UPPER_CASE
MAX_RETRIES = 5
API_TIMEOUT = 10

# Private methods/attributes: _leading_underscore
def _private_helper():
    pass

class Example:
    def __init__(self):
        self._private_var = 123
```

### Type Hints (Mandatory)

```python
# Functions: Include return type
def calculate_average(values: list[float]) -> float:
    return sum(values) / len(values)

# Function with multiple parameters
def get_stock_data(ticker: str, period: int = 30) -> dict:
    pass

# Optional values
def find_user(user_id: int | None = None) -> dict | None:
    pass

# Class methods
class Agent:
    def __init__(self, name: str, api_key: str) -> None:
        self.name = name
        self.api_key = api_key

    def process_query(self, query: str) -> str:
        pass
```

### Docstrings (Google Style)

```python
def get_technical_indicators(ticker: str, timespan: str = "day") -> dict:
    """Get comprehensive technical analysis indicators.

    Retrieves RSI, MACD, SMA, and EMA indicators for a given ticker.

    Args:
        ticker: Stock ticker symbol (e.g., "SPY", "AAPL")
        timespan: Aggregate time window - "day", "minute", "hour", "week", "month"

    Returns:
        Dictionary with indicator values and timestamps:
        {
            "rsi": {"value": 62.45, "timestamp": "2025-10-18"},
            "macd": {"value": 2.34, "signal": 1.87, "histogram": 0.47},
            "sma_5": {"value": 654.23, "timestamp": "2025-10-18"},
            ...
        }

    Raises:
        ValueError: If ticker is empty or invalid format
        requests.RequestException: If API request fails

    Examples:
        >>> indicators = get_technical_indicators("SPY")
        >>> print(indicators["rsi"]["value"])
        62.45
    """
```

### Import Organization

```python
# 1. Standard library imports (alphabetical)
import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Optional

# 2. Third-party imports (alphabetical)
import requests
from pydantic import BaseModel

# 3. Local imports (relative imports for backend package)
from .cli import main, process_query
from .tools.polygon_tools import get_ta_indicators
from .utils.response_utils import format_response
```

### Error Handling

```python
# Use centralized error_utils.py (Oct 18, 2025)
from .tools.error_utils import create_error_response

# Before (duplicate error handling):
def get_price(ticker: str):
    if not ticker or not ticker.strip():
        return {
            "error": "Invalid ticker",
            "message": "Ticker cannot be empty"
        }

# After (using helper - Oct 18, 2025):
def get_price(ticker: str):
    ticker_clean = ticker.strip().upper()
    if not ticker_clean:
        return create_error_response(
            "Invalid ticker",
            "Ticker cannot be empty",
            ticker=ticker
        )
```

### Input Validation

```python
# Use centralized validation_utils.py (Oct 18, 2025)
from .tools.validation_utils import validate_and_sanitize_ticker

# Before (duplicate validation):
def get_quote(ticker: str):
    ticker = ticker.strip().upper()
    if not ticker:
        return {"error": "Invalid ticker"}

# After (using helper - Oct 18, 2025):
def get_quote(ticker: str):
    ticker_validated, error = validate_and_sanitize_ticker(ticker)
    if error:
        return error
```

### API Headers

```python
# Use centralized api_utils.py (Oct 18, 2025)
from .tools.api_utils import create_tradier_headers, TRADIER_TIMEOUT

# Before (duplicate header builders):
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

# After (using helper - Oct 18, 2025):
headers = create_tradier_headers(api_key)
timeout = TRADIER_TIMEOUT
```

---

## File Organization

### Backend Tools Structure (Oct 18, 2025)

```
src/backend/tools/
├── __init__.py
├── tradier_tools.py           # 5 Tradier API tools (refactored)
├── polygon_tools.py           # 2 Polygon API tools (refactored)
├── error_utils.py             # Error response formatting (new Oct 18)
├── validation_utils.py        # Ticker validation (new Oct 18)
├── api_utils.py               # API header helpers (new Oct 18)
└── formatting_helpers.py      # Formatting utilities
```

### Import Paths (Relative Imports)

```python
# From backend/cli.py
from .tools.polygon_tools import get_ta_indicators
from .tools.error_utils import create_error_response
from .services import create_agent

# From backend/tools/tradier_tools.py
from .error_utils import create_error_response
from .validation_utils import validate_and_sanitize_ticker
from .api_utils import create_tradier_headers
```

---

## Code Quality Standards

### Linting with Pylint

```bash
npm run lint              # Check code quality
npm run lint:fix          # Auto-fix with black + isort
```

**Target Score:** 9.0/10 or higher
**Current Score:** 9.61/10 (excellent)

### Type Checking with MyPy

```bash
uv run mypy src/backend/
```

**Standard:** Strict type checking
**Requirement:** All functions have type hints

### Formatting with Black

```bash
black --line-length 88 src/backend/
```

**Line Length:** 88 characters
**Integration:** `npm run lint:fix` runs automatically

### Import Sorting with isort

```bash
isort --profile black src/backend/
```

**Profile:** Black-compatible
**Integration:** `npm run lint:fix` runs automatically

---

## DRY Principle (Don't Repeat Yourself) - Oct 18, 2025 ⭐

### Problem: Code Duplication

**Before Oct 18:** 43+ duplicate code patterns across tool functions

**Examples:**
- Error response formatting duplicated 20+ times
- Ticker validation duplicated 15+ times
- API header generation duplicated 8+ times

### Solution: Centralized Helpers (Oct 18, 2025)

**error_utils.py** - Standardized error responses
```python
def create_error_response(error_type: str, message: str, **extra_fields) -> dict:
    """Single source of truth for error formatting."""
    return {
        "error": error_type,
        "message": message,
        **extra_fields
    }
```

**validation_utils.py** - Ticker validation
```python
def validate_and_sanitize_ticker(ticker: str) -> tuple[str, Optional[dict]]:
    """Single source of truth for validation."""
    if not ticker or not ticker.strip():
        return "", create_error_response("Invalid ticker", "Cannot be empty", ticker=ticker)
    return ticker.strip().upper(), None
```

**api_utils.py** - API utilities
```python
def create_tradier_headers(api_key: str) -> dict:
    """Single source of truth for API headers."""
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
```

### Refactoring Pattern

**Before (Duplicate):**
```python
def get_stock_quote(ticker):
    # Duplicate validation
    ticker = ticker.strip().upper()
    if not ticker:
        return {"error": "Invalid", "message": "Empty"}
    
    # Duplicate header builder
    headers = {
        "Authorization": f"Bearer {key}",
        "Accept": "application/json"
    }
```

**After (Centralized - Oct 18):**
```python
def get_stock_quote(ticker):
    # Use centralized validation
    ticker_validated, error = validate_and_sanitize_ticker(ticker)
    if error:
        return error
    
    # Use centralized header builder
    headers = create_tradier_headers(api_key)
```

### Benefits of DRY Principle (Oct 18, 2025)

1. **Single Source of Truth** - Update logic in ONE place
2. **Consistency** - All functions use same formatting
3. **Maintainability** - Easier to fix bugs and add features
4. **Testability** - Helpers can be unit tested independently
5. **Code Reduction** - -390 lines net reduction (~20%)

---

## Testing & Validation

### Unit Testing

```python
# pytest tests/test_validation_utils.py
def test_validate_ticker_valid():
    result, error = validate_and_sanitize_ticker("spy")
    assert result == "SPY"
    assert error is None

def test_validate_ticker_invalid():
    result, error = validate_and_sanitize_ticker("")
    assert result == ""
    assert error is not None
```

### CLI Regression Tests

```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Tests:** 39 comprehensive tests
**Coverage:** Market status, OHLC data, technical analysis, options chains
**Target:** 100% pass rate

### Code Quality Checks

```bash
npm run check:all          # Run all checks
npm run lint              # Linting
npm run type-check        # Type checking
npm run format            # Formatting (dry run)
npm run lint:fix          # Format + lint auto-fix
```

---

## Comments & Documentation

### When to Comment

```python
# Good: Explains WHY (not WHAT)
# Use limit=10 to fetch recent data even on weekends/holidays
results = client.get_rsi(ticker, limit=10)

# Bad: Explains WHAT (code already does this)
# Get RSI with limit 10
results = client.get_rsi(ticker, limit=10)
```

### Multi-line Comments

```python
"""
This function:
1. Validates the ticker symbol
2. Fetches price data from Tradier API
3. Formats response with performance metrics
"""
```

### No Legacy Comments

**October 18, 2025 Decision:** Remove all historical/deprecation comments

```python
# Don't leave these:
# DEPRECATED: Old implementation using xyz
# TODO: Remove this when React frontend is retired
# NOTE: This was for FastAPI compatibility

# Clean comments only:
# Comment on current business logic
```

---

## Performance Considerations

### Async/Await

```python
# Use async for I/O operations
async def get_multiple_prices(tickers: list[str]) -> list[dict]:
    """Fetch prices for multiple tickers concurrently."""
    tasks = [get_price(ticker) for ticker in tickers]
    return await asyncio.gather(*tasks)
```

### Error Handling

```python
# Catch specific exceptions
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.Timeout:
    return create_error_response("Timeout", "Request exceeded time limit")
except requests.RequestException as e:
    return create_error_response("API error", f"Request failed: {str(e)}")
```

---

## Git Commit Guidelines

### Commit Message Format

```
[TAG] Brief description

- Change 1
- Change 2

Reference: Issue #123

Generated with Claude Code
```

### Commit Tags

- `[FEATURE]` - New feature
- `[FIX]` - Bug fix
- `[REFACTOR]` - Code refactoring
- `[TEST]` - Test additions/updates
- `[DOCS]` - Documentation updates
- `[CLEANUP]` - Code cleanup without functional changes

### Atomic Commits

- Stage all files at once: `git add -A`
- Commit immediately: `git commit -m "message"`
- Push immediately: `git push`

---

## Summary

| Standard | Rule |
|----------|------|
| **Language** | Python 3.10+ |
| **Style** | PEP 8 |
| **Type Hints** | Mandatory (all functions) |
| **Docstrings** | Google style (all public functions) |
| **Line Length** | 88 chars (Black) |
| **Imports** | Relative (local), organized groups |
| **Error Handling** | Use error_utils.py (centralized) |
| **Validation** | Use validation_utils.py (centralized) |
| **API Utils** | Use api_utils.py (centralized) |
| **Linting** | 9.0+/10 target (current: 9.61/10) |
| **DRY Principle** | No code duplication (Oct 18, 2025) |
| **Comments** | No legacy/deprecation comments |
| **Testing** | 39-test CLI regression suite |

---

**Last Updated:** October 18, 2025 (after DRY refactoring and entry points implementation)
**Python Standards:** ✅ Full PEP 8 compliance
**Code Quality:** ✅ 9.61/10 linting score
**Test Coverage:** ✅ 39/39 tests passing
