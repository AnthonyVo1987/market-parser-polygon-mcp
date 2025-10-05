# Implementation Plan: Swap get_snapshot_ticker with Finnhub get_stock_quote Custom Tool

**Task**: Replace Polygon.io get_snapshot_ticker with Finnhub get_stock_quote custom tool
**Status**: Planning Phase - DO NOT IMPLEMENT YET - PENDING USER APPROVAL
**Last Updated**: 2025-10-04 (Updated with user adjustments)

---

## 📋 RESEARCH & ANALYSIS SUMMARY

### Finnhub API Research Findings

**Function Signature:**
```python
finnhub_client.quote(symbol: str) -> dict
```

**Setup Required:**
```python
import finnhub
finnhub_client = finnhub.Client(api_key="YOUR_API_KEY")
```

**API Response Format:**
```python
{
    "c": 178.50,     # Current price
    "d": 2.30,       # Change
    "dp": 1.31,      # Percent change
    "h": 179.20,     # High price of the day
    "l": 176.80,     # Low price of the day
    "o": 177.00,     # Open price of the day
    "pc": 176.20     # Previous close price
}
```

### Current Codebase Analysis

**AI Agent Structure:**
- Location: `src/backend/services/agent_service.py`
- Instructions Function: `get_enhanced_agent_instructions()` (lines 10-127)
- Agent Creation: `create_agent()` (lines 145-163)
- Current Tools: 9 Polygon.io MCP tools
- Custom Tools List: `tools=[]` (currently empty, line 157)

**Key Findings:**
- ✅ `.env` has `FINNHUB_API_KEY` configured
- ❌ No existing finnhub imports in codebase (brand new integration)
- ✅ Agent uses custom tools via `tools=[]` parameter
- ✅ Instructions follow strict rule-based format with examples

**Current Tool Count:** 9 Polygon.io MCP tools
**New Tool Count After Implementation:** 9 tools (8 MCP + 1 custom Finnhub)

**🔄 TOOL SWAP STRATEGY:**
- **REMOVE:** get_snapshot_ticker (Polygon.io MCP tool)
- **ADD:** get_stock_quote (Finnhub custom tool)
- **KEEP:** get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg, get_market_status
- **RESULT:** Single ticker queries use get_stock_quote; Multiple tickers use get_snapshot_all

---

## 🎯 IMPLEMENTATION PLAN - GRANULAR TASK CHECKLIST

### PHASE 1: DEPENDENCY SETUP

**1.1 Install Finnhub Python Library**
- [ ] Add `finnhub-python` to `pyproject.toml` dependencies
- [ ] Run `uv sync` to install package
- [ ] Verify installation with `uv pip list | grep finnhub`

**1.2 Verify Environment Configuration**
- [x] Confirm `.env` has `FINNHUB_API_KEY` (already verified)
- [ ] Load API key in config module if needed

---

### PHASE 2: CREATE CUSTOM TOOL

**2.1 Create New Tools Module**
- [ ] Create directory: `src/backend/tools/` (if not exists)
- [ ] Create file: `src/backend/tools/__init__.py`
- [ ] Create file: `src/backend/tools/finnhub_tools.py`

**2.2 Implement get_stock_quote Tool**

File: `src/backend/tools/finnhub_tools.py`

```python
"""
Finnhub custom tools for OpenAI AI Agent.
Provides real-time stock quote data via Finnhub API.
"""

import os
import json
import finnhub
from typing import Optional
from agents import function_tool


# Initialize Finnhub client with API key from environment
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


@function_tool
async def get_stock_quote(ticker: str) -> str:
    """Get real-time stock quote from Finnhub API.

    Use this tool when the user requests a stock quote, current price,
    or real-time market data for a single ticker symbol.

    This tool provides alternative real-time price data via Finnhub API,
    complementing the Polygon.io MCP tools.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "TSLA", "NVDA").
                Must be a valid ticker from major US exchanges.

    Returns:
        JSON string containing quote data with format:
        {
            "ticker": "AAPL",
            "current_price": 178.50,
            "change": 2.30,
            "percent_change": 1.31,
            "high": 179.20,
            "low": 176.80,
            "open": 177.00,
            "previous_close": 176.20,
            "source": "Finnhub"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "ticker": "SYMBOL"
        }

    Note:
        - Supports major US stock exchanges (NYSE, NASDAQ, etc.)
        - Data updates in real-time during market hours
        - Returns last available price when market is closed
        - Rate limits apply based on Finnhub API tier

    Examples:
        - "Get AAPL stock quote"
        - "What's the current price of TSLA?"
        - "NVDA quote"
    """
    try:
        # Validate ticker input
        if not ticker or not ticker.strip():
            return json.dumps({
                "error": "Invalid ticker",
                "message": "Ticker symbol cannot be empty",
                "ticker": ticker
            })

        # Clean ticker (uppercase, strip whitespace)
        ticker = ticker.strip().upper()

        # Call Finnhub API
        quote_data = finnhub_client.quote(ticker)

        # Check if API returned valid data
        if not quote_data or quote_data.get('c') == 0:
            return json.dumps({
                "error": "No data",
                "message": f"No quote data available for ticker: {ticker}. Verify ticker symbol is valid.",
                "ticker": ticker
            })

        # Format response
        return json.dumps({
            "ticker": ticker,
            "current_price": round(quote_data.get('c', 0), 2),
            "change": round(quote_data.get('d', 0), 2),
            "percent_change": round(quote_data.get('dp', 0), 2),
            "high": round(quote_data.get('h', 0), 2),
            "low": round(quote_data.get('l', 0), 2),
            "open": round(quote_data.get('o', 0), 2),
            "previous_close": round(quote_data.get('pc', 0), 2),
            "source": "Finnhub"
        })

    except Exception as e:
        # Handle unexpected errors
        return json.dumps({
            "error": "API request failed",
            "message": f"Failed to retrieve quote for {ticker}: {str(e)}",
            "ticker": ticker
        })
```

**Implementation Checklist:**
- [ ] Create `src/backend/tools/__init__.py`
- [ ] Create `src/backend/tools/finnhub_tools.py`
- [ ] Implement `get_stock_quote()` function with @function_tool decorator
- [ ] Add comprehensive docstring following Google style
- [ ] Implement error handling with JSON returns
- [ ] Add input validation (empty ticker check)
- [ ] Format all numeric values to 2 decimal places
- [ ] Include source field in response

---

### PHASE 3: INTEGRATE TOOL INTO AGENT

**3.1 Update Agent Service Imports**

File: `src/backend/services/agent_service.py`

- [ ] Add import at top of file:
```python
from ..tools.finnhub_tools import get_stock_quote
```

**3.2 Update create_agent() Function**

Location: `src/backend/services/agent_service.py` line 157

- [ ] Change `tools=[]` to `tools=[get_stock_quote]`

Before:
```python
tools=[],  # Removed save_analysis_report
```

After:
```python
tools=[get_stock_quote],  # Finnhub real-time quote tool
```

---

### PHASE 4: UPDATE AI AGENT INSTRUCTIONS

**4.1 Update Supported Tools List**

Location: `src/backend/services/agent_service.py` line 23-24

- [ ] REMOVE get_snapshot_ticker from supported tools list
- [ ] ADD get_stock_quote to supported tools list
- [ ] Keep tool count at 9

Before:
```python
🔴 CRITICAL: YOU MUST ONLY USE THE FOLLOWING 9 SUPPORTED TOOLS: [get_snapshot_ticker, get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg, get_market_status] 🔴
```

After:
```python
🔴 CRITICAL: YOU MUST ONLY USE THE FOLLOWING 9 SUPPORTED TOOLS: [get_stock_quote, get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg, get_market_status] 🔴
```

**4.2 Replace RULE #1 - Single Ticker Logic**

Location: `src/backend/services/agent_service.py` RULE #1 (~line 28-35)

- [ ] REPLACE get_snapshot_ticker references with get_stock_quote
- [ ] Update rule to use Finnhub instead of Polygon.io
- [ ] REMOVE market_type parameter (not needed for Finnhub)

Before:
```python
RULE #1: SINGLE TICKER = ALWAYS USE get_snapshot_ticker()
- If the request mentions ONLY ONE ticker symbol → MUST USE get_snapshot_ticker(ticker='SYMBOL', market_type='stocks')
- Examples: "NVDA price", "GME closing price", "TSLA snapshot", "AAPL data"
- ❌ NEVER use get_snapshot_all() for a single ticker
- ✅ ALWAYS use get_snapshot_ticker(ticker='SYMBOL', market_type='stocks') for one ticker
- 🔴 MANDATORY: ALWAYS include market_type='stocks' parameter (default to stocks unless explicitly options)
```

After:
```python
RULE #1: SINGLE TICKER = ALWAYS USE get_stock_quote()
- If the request mentions ONLY ONE ticker symbol → MUST USE get_stock_quote(ticker='SYMBOL')
- Examples: "NVDA price", "GME closing price", "TSLA snapshot", "AAPL data"
- ❌ NEVER use get_snapshot_all() for a single ticker
- ✅ ALWAYS use get_stock_quote(ticker='SYMBOL') for one ticker
- 📊 Uses Finnhub API for real-time quote data
- ✅ Returns: current price, change, percent change, high, low, open, previous close
```

**4.3 Update Tool Examples Section**

Location: `src/backend/services/agent_service.py` (~line 100)

- [ ] REPLACE all get_snapshot_ticker examples with get_stock_quote
- [ ] REMOVE market_type parameter from single ticker examples
- [ ] Keep get_snapshot_all examples unchanged

Before:
```python
EXAMPLES OF CORRECT TOOL CALLS:
✅ "NVDA price" → get_snapshot_ticker(ticker='NVDA', market_type='stocks')
✅ "GME closing price" → get_snapshot_ticker(ticker='GME', market_type='stocks')
✅ "TSLA snapshot" → get_snapshot_ticker(ticker='TSLA', market_type='stocks')
✅ "SPY, QQQ, IWM" → get_snapshot_all(tickers=['SPY','QQQ','IWM'], market_type='stocks')
✅ "AAPL and MSFT prices" → get_snapshot_all(tickers=['AAPL','MSFT'], market_type='stocks')

EXAMPLES OF INCORRECT TOOL CALLS:
❌ get_snapshot_ticker(ticker='NVDA') [MISSING market_type!]
❌ get_snapshot_all(tickers='SPY,QQQ,IWM') [WRONG format! Use list: ['SPY','QQQ','IWM']]
❌ get_snapshot_all(tickers=['GME']) for single ticker [WRONG! Use get_snapshot_ticker]
❌ Refusing "NVDA price" because market closed [NEVER refuse! Return last price]
```

After:
```python
EXAMPLES OF CORRECT TOOL CALLS:
✅ "NVDA price" → get_stock_quote(ticker='NVDA')
✅ "GME closing price" → get_stock_quote(ticker='GME')
✅ "TSLA snapshot" → get_stock_quote(ticker='TSLA')
✅ "AAPL data" → get_stock_quote(ticker='AAPL')
✅ "SPY, QQQ, IWM" → get_snapshot_all(tickers=['SPY','QQQ','IWM'], market_type='stocks')
✅ "AAPL and MSFT prices" → get_snapshot_all(tickers=['AAPL','MSFT'], market_type='stocks')

EXAMPLES OF INCORRECT TOOL CALLS:
❌ get_snapshot_all(tickers='SPY,QQQ,IWM') [WRONG format! Use list: ['SPY','QQQ','IWM']]
❌ get_snapshot_all(tickers=['GME']) for single ticker [WRONG! Use get_stock_quote]
❌ Refusing "NVDA price" because market closed [NEVER refuse! Return last price]
❌ Using get_snapshot_ticker [REMOVED! Use get_stock_quote for single tickers]
```

**4.4 Update Decision Tree**

Location: `src/backend/services/agent_service.py` (~line 95)

- [ ] Update decision tree to use get_stock_quote instead of get_snapshot_ticker
- [ ] Remove market_type parameter from single ticker decision

Before:
```python
📋 DECISION TREE FOR STOCK SNAPSHOTS:

Step 1: Count how many ticker symbols in the request
Step 2:
   - If count = 1 ticker → USE get_snapshot_ticker(ticker='SYMBOL', market_type='stocks')
   - If count ≥ 2 tickers → USE get_snapshot_all(tickers=['SYM1','SYM2',...], market_type='stocks')
Step 3: ALWAYS include market_type='stocks' (unless request explicitly mentions options)
Step 4: For get_snapshot_all(), ALWAYS use LIST format: ['SPY','QQQ'] NOT 'SPY,QQQ'
```

After:
```python
📋 DECISION TREE FOR STOCK QUOTES:

Step 1: Count how many ticker symbols in the request
Step 2:
   - If count = 1 ticker → USE get_stock_quote(ticker='SYMBOL')
   - If count ≥ 2 tickers → USE get_snapshot_all(tickers=['SYM1','SYM2',...], market_type='stocks')
Step 3: For get_snapshot_all(), ALWAYS include market_type='stocks' (unless request explicitly mentions options)
Step 4: For get_snapshot_all(), ALWAYS use LIST format: ['SPY','QQQ'] NOT 'SPY,QQQ'
```

---

### PHASE 5: TESTING & VALIDATION

**5.1 Unit Testing**
- [ ] Create test file: `tests/test_finnhub_tools.py`
- [ ] Test valid ticker: `get_stock_quote("AAPL")`
- [ ] Test invalid ticker: `get_stock_quote("INVALID_XYZ")`
- [ ] Test empty ticker: `get_stock_quote("")`
- [ ] Test API error handling
- [ ] Verify JSON response format
- [ ] Verify all numeric fields round to 2 decimals

**5.2 Integration Testing**
- [ ] Test tool integration with agent
- [ ] Verify get_snapshot_ticker is NOT in supported tools list
- [ ] Verify get_stock_quote IS in supported tools list
- [ ] Test agent can call get_stock_quote successfully
- [ ] Test single ticker query: "Get AAPL stock quote" → should use get_stock_quote
- [ ] Test single ticker query: "What's NVDA price?" → should use get_stock_quote
- [ ] Test multi ticker query: "SPY, QQQ, IWM prices" → should use get_snapshot_all
- [ ] Verify agent NEVER calls get_snapshot_ticker (removed from tools)
- [ ] Verify "Tools Used" section includes get_stock_quote for single ticker queries

**5.3 Manual Testing**
- [ ] Start backend server
- [ ] Test single ticker via CLI: "What's NVDA price?" → should use get_stock_quote
- [ ] Test single ticker via React UI: "Get AAPL stock quote" → should use get_stock_quote
- [ ] Test multi ticker via CLI: "SPY and QQQ prices" → should use get_snapshot_all
- [ ] Verify single ticker response includes all Finnhub fields (current_price, change, percent_change, etc.)
- [ ] Verify agent NEVER attempts to call get_snapshot_ticker
- [ ] Test during market hours
- [ ] Test after market close

---

### PHASE 6: DOCUMENTATION UPDATES

**6.1 Update CLAUDE.md**
- [ ] Update Last Completed Task Summary with tool swap details
- [ ] Document Finnhub integration (replaced Polygon.io get_snapshot_ticker)
- [ ] Note tool count remains at 9 (swap, not addition)
- [ ] Document single ticker now uses Finnhub instead of Polygon.io

**6.2 Update README (if exists)**
- [ ] Document Finnhub API requirement
- [ ] Add FINNHUB_API_KEY to environment variables section
- [ ] Update features list

**6.3 Create Serena Memory**
- [ ] Create memory file: `finnhub_tool_swap_oct_2025.md`
- [ ] Document get_snapshot_ticker → get_stock_quote swap
- [ ] Include tool usage examples and comparison
- [ ] Note integration points and why swap was made
- [ ] Document that single ticker queries now use Finnhub, multi ticker still uses Polygon.io

---

### PHASE 7: VALIDATION & CLEANUP

**7.1 Code Quality Checks**
- [ ] Run `npm run lint` to check TypeScript/JavaScript
- [ ] Run `uv run pylint src/backend/tools/finnhub_tools.py` for Python linting
- [ ] Run `npm run type-check` for TypeScript validation
- [ ] Fix any linting errors

**7.2 Final Verification**
- [ ] Confirm tool count: 9 (8 MCP + 1 custom Finnhub)
- [ ] Verify get_snapshot_ticker is completely removed from instructions
- [ ] Verify get_stock_quote is in supported tools list
- [ ] Verify imports work correctly
- [ ] Verify FINNHUB_API_KEY loads from .env
- [ ] Test agent creation without errors
- [ ] Verify all instructions updated correctly (RULE #1, examples, decision tree)

**7.3 Cleanup**
- [ ] Remove any debug print statements
- [ ] Remove any commented-out code
- [ ] Ensure consistent code formatting
- [ ] Update any outdated comments

---

## 📊 IMPLEMENTATION SUMMARY

**Files to Create:**
1. `src/backend/tools/__init__.py` (new)
2. `src/backend/tools/finnhub_tools.py` (new)
3. `tests/test_finnhub_tools.py` (new, optional)
4. `.serena/memories/finnhub_integration_oct_2025.md` (new)

**Files to Modify:**
1. `src/backend/services/agent_service.py` (add import, update create_agent, REPLACE get_snapshot_ticker with get_stock_quote in instructions)
2. `pyproject.toml` (add finnhub-python dependency)
3. `CLAUDE.md` (update Last Completed Task Summary with swap details)

**Dependencies to Add:**
1. `finnhub-python` package

**Environment Variables:**
- ✅ `FINNHUB_API_KEY` (already configured in .env)

**Total Tasks:** 50 checklist items across 7 phases

**Tool Architecture Change:**
- **BEFORE:** 9 tools (all Polygon.io MCP) - includes get_snapshot_ticker
- **AFTER:** 9 tools (8 Polygon.io MCP + 1 Finnhub custom) - get_stock_quote replaces get_snapshot_ticker

---

## 🔍 TECHNICAL SPECIFICATIONS

**Tool Name:** `get_stock_quote`
**Tool Type:** Custom OpenAI Agent Function Tool
**Decorator:** `@function_tool`
**Function Type:** `async`
**Parameters:** `ticker: str`
**Return Type:** `str` (JSON formatted)
**Error Handling:** Returns JSON with error details
**API Provider:** Finnhub
**API Endpoint:** `finnhub_client.quote(symbol)`

**Response Schema:**
```json
{
  "ticker": "string",
  "current_price": "number (2 decimals)",
  "change": "number (2 decimals)",
  "percent_change": "number (2 decimals)",
  "high": "number (2 decimals)",
  "low": "number (2 decimals)",
  "open": "number (2 decimals)",
  "previous_close": "number (2 decimals)",
  "source": "Finnhub"
}
```

**Error Response Schema:**
```json
{
  "error": "string",
  "message": "string",
  "ticker": "string"
}
```

---

## ⚠️ IMPORTANT NOTES

1. **NO IMPLEMENTATION YET**: This is the planning phase only. Awaiting user approval before proceeding.

2. **🔄 TOOL SWAP (NOT ADDITION)**: This implementation REPLACES get_snapshot_ticker with get_stock_quote. Tool count remains at 9.

3. **Single Ticker Strategy Change**:
   - **OLD:** Single ticker → Polygon.io get_snapshot_ticker
   - **NEW:** Single ticker → Finnhub get_stock_quote
   - **UNCHANGED:** Multiple tickers → Polygon.io get_snapshot_all

4. **API Rate Limits**: Finnhub API has rate limits depending on tier. Free tier typically allows 60 calls/minute.

5. **Error Handling**: All errors return JSON format (no exceptions) to ensure AI agent can process responses gracefully.

6. **Market Hours**: Tool works both during market hours (real-time) and after hours (returns last available price).

7. **Testing Priority**: Critical to verify agent NEVER attempts to call get_snapshot_ticker after swap. Must test single ticker queries use get_stock_quote.

8. **No market_type Parameter**: Finnhub's quote() doesn't need market_type parameter (simpler than Polygon.io)

---

## 🎯 SUCCESS CRITERIA

Implementation is successful when:

- ✅ Agent has 9 tools (8 MCP Polygon.io + 1 custom Finnhub)
- ✅ get_snapshot_ticker is COMPLETELY REMOVED from agent instructions
- ✅ get_stock_quote REPLACES get_snapshot_ticker in supported tools list
- ✅ Agent instructions updated: RULE #1 uses get_stock_quote (not get_snapshot_ticker)
- ✅ Decision tree updated to use get_stock_quote for single tickers
- ✅ All examples updated to use get_stock_quote instead of get_snapshot_ticker
- ✅ Tool returns properly formatted JSON responses
- ✅ Error handling works for invalid tickers
- ✅ Single ticker query: "Get AAPL price" → uses get_stock_quote (Finnhub)
- ✅ Multi ticker query: "SPY and QQQ prices" → uses get_snapshot_all (Polygon.io)
- ✅ Agent NEVER attempts to call get_snapshot_ticker (verification critical)
- ✅ "Tools Used" section correctly lists get_stock_quote for single ticker queries
- ✅ No linting errors or type check failures
- ✅ Documentation updated with swap details (CLAUDE.md, Serena memory)

---

**END OF IMPLEMENTATION PLAN**

*Awaiting user approval to proceed with implementation.*
