# Implementation Plan: Polygon Direct API Custom Tool - get_market_status_and_date_time

**Task:** Create custom tool `get_market_status_and_date_time` using Polygon Python Library direct API calls

**Research Phase:** ✅ COMPLETED
**Implementation Phase:** 🔴 NOT STARTED - AWAITING APPROVAL
**Status:** RESEARCH & PLANNING ONLY - NO CODE IMPLEMENTATION YET

---

## 📋 Research Summary

### Polygon API Research Findings

**API Method:** `client.get_market_status()`
- **Endpoint:** `/v1/marketstatus/now`
- **Client Initialization:** `RESTClient()` with `POLYGON_API_KEY` environment variable
- **Return Type:** `MarketStatus` model

**MarketStatus Response Structure:**
```python
{
    "after_hours": bool,           # Whether after-hours trading is active
    "currencies": {                # Currency market status
        "crypto": str,
        "fx": str
    },
    "early_hours": bool,          # Whether pre-market trading is active
    "exchanges": {                # Exchange status
        "nasdaq": str,            # "open", "closed", "extended-hours"
        "nyse": str,
        "otc": str
    },
    "indicesGroups": {            # Indices status
        "s_and_p": str,
        "nasdaq": str,
        "dow_jones": str,
        # ... more indices
    },
    "market": str,                # Overall market status: "open", "closed", "extended-hours"
    "server_time": str            # ISO timestamp from Polygon server
}
```

### Previous Implementation Pattern (Finnhub Reference)

**File Structure:**
- Location: `src/backend/tools/finnhub_tools.py`
- Pattern: @function_tool decorator with async function
- Client initialization: Lazy initialization with helper function
- Error handling: Try-except with JSON error responses
- Integration: Added to agent via `tools=[get_stock_quote]` in `create_agent()`

**Key Patterns:**
1. Lazy client initialization with helper function
2. Input validation before API calls
3. Comprehensive error handling with descriptive messages
4. JSON return format for structured data
5. Detailed docstring following Google style
6. Environment variable for API key

---

## ✅ Implementation Checklist

### PHASE 1: Create Polygon Tools File

- [ ] **Task 1.1:** Create new file `src/backend/tools/polygon_tools.py`
  - Location: `/home/anthony/Github/market-parser-polygon-mcp/src/backend/tools/polygon_tools.py`
  - Template: Follow finnhub_tools.py structure
  - Dependencies: `polygon`, `os`, `json`, `agents`

- [ ] **Task 1.2:** Add file-level docstring
  ```python
  """
  Polygon.io custom tools for OpenAI AI Agent.
  Provides direct Polygon Python Library API access for market status and datetime.
  """
  ```

- [ ] **Task 1.3:** Add required imports
  ```python
  import json
  import os
  from polygon import RESTClient
  from agents import function_tool
  ```

### PHASE 2: Implement Helper Function

- [ ] **Task 2.1:** Create `_get_polygon_client()` helper function
  - Purpose: Lazy initialization of Polygon client
  - Pattern: Same as `_get_finnhub_client()` from finnhub_tools.py
  - API Key: Get from `os.getenv("POLYGON_API_KEY")`
  - Return: `RESTClient` instance

  ```python
  def _get_polygon_client():
      """Get Polygon client with API key from environment.

      Lazy initialization ensures .env is loaded before accessing API key.
      """
      api_key = os.getenv("POLYGON_API_KEY")
      return RESTClient(api_key=api_key)
  ```

### PHASE 3: Implement Main Tool Function

- [ ] **Task 3.1:** Create `get_market_status_and_date_time()` function signature
  - Decorator: `@function_tool`
  - Function type: `async def`
  - Parameters: None (no parameters needed - retrieves current status)
  - Return type: `str` (JSON string)

- [ ] **Task 3.2:** Write comprehensive docstring
  - Style: Google-style docstring (per OPENAI_CUSTOM_TOOLS_REFERENCE.md)
  - Include: Purpose, when to use, return format, examples
  - Reference: Lines 368-390 from OPENAI_CUSTOM_TOOLS_REFERENCE.md

  **Required sections:**
  1. Summary: "Get current market status and datetime from Polygon.io API."
  2. Usage context: "Use this tool when the user requests market status, trading hours, current date/time, or whether markets are open/closed."
  3. Returns: JSON format specification
  4. Note: Limitations and data source info
  5. Examples: Query examples that trigger this tool

- [ ] **Task 3.3:** Implement function body with error handling

  **Error Handling Strategy (per reference docs):**
  1. Try-except block wrapping API call
  2. JSON error responses for all error cases
  3. Specific error types: API failures, empty data, validation errors

  **Implementation steps:**
  - [ ] 3.3a: Initialize Polygon client using helper function
  - [ ] 3.3b: Call `client.get_market_status()`
  - [ ] 3.3c: Validate response is not None/empty
  - [ ] 3.3d: Extract relevant fields from MarketStatus model
  - [ ] 3.3e: Format response as JSON with clear structure
  - [ ] 3.3f: Add try-except for exception handling
  - [ ] 3.3g: Return structured JSON error messages on failure

- [ ] **Task 3.4:** Design JSON response format

  **Success Response:**
  ```json
  {
      "market_status": "open" | "closed" | "extended-hours",
      "after_hours": true | false,
      "early_hours": true | false,
      "exchanges": {
          "nasdaq": "open" | "closed" | "extended-hours",
          "nyse": "open" | "closed" | "extended-hours",
          "otc": "open" | "closed" | "extended-hours"
      },
      "server_time": "2025-10-05T14:30:00Z",
      "date": "2025-10-05",
      "time": "14:30:00",
      "source": "Polygon.io"
  }
  ```

  **Error Response:**
  ```json
  {
      "error": "error_type",
      "message": "descriptive error message",
      "source": "Polygon.io"
  }
  ```

### PHASE 4: Integrate Tool into Agent

- [ ] **Task 4.1:** Update `src/backend/services/agent_service.py`
  - [ ] 4.1a: Add import statement
    ```python
    from ..tools.polygon_tools import get_market_status_and_date_time
    ```

  - [ ] 4.1b: Update `create_agent()` function - add tool to tools list
    ```python
    tools=[get_stock_quote, get_market_status_and_date_time],  # Added Polygon direct API tool
    ```

- [ ] **Task 4.2:** Update agent instructions in `get_enhanced_agent_instructions()`

  **Changes Required:**
  1. Update TOOLS section header to reflect new tool count (10 tools total)
  2. Update CRITICAL TOOL SELECTION RULES header
  3. **Replace RULE #4** - Change from MCP `get_market_status()` to custom `get_market_status_and_date_time()`

  **OLD RULE #4:**
  ```
  RULE #4: MARKET STATUS = ALWAYS USE get_market_status()
  - If the request asks about market open/closed status, hours, or trading sessions
  - Examples: "Is market open?", "Market status", "Trading hours"
  ```

  **NEW RULE #4:**
  ```
  RULE #4: MARKET STATUS & DATE/TIME = ALWAYS USE get_market_status_and_date_time()
  - If the request asks about market open/closed status, hours, trading sessions, current date, or current time
  - Examples: "Is market open?", "Market status", "Trading hours", "What's the date?", "Current time?"
  - 📊 Uses Polygon.io Direct API for real-time market status and server datetime
  - ✅ Returns: market status, exchange statuses, after_hours, early_hours, server_time with date and time
  ```

  - [ ] 4.2a: Update supported tools list from 9 to 10 tools
  - [ ] 4.2b: Replace `get_market_status` with `get_market_status_and_date_time` in tools list
  - [ ] 4.2c: Update RULE #4 with new tool name and capabilities
  - [ ] 4.2d: Update decision tree examples if referencing market status
  - [ ] 4.2e: Update "EXAMPLES OF CORRECT TOOL CALLS" section with new tool
  - [ ] 4.2f: Add to "Tools Used" transparency examples

### PHASE 5: Code Quality & Validation

- [ ] **Task 5.1:** Run Pylint on new file
  - Command: `pylint src/backend/tools/polygon_tools.py`
  - Target: 10.00/10 score (matching finnhub_tools.py standard)
  - Fix any linting issues identified

- [ ] **Task 5.2:** Verify imports work
  - Test import: `from src.backend.tools.polygon_tools import get_market_status_and_date_time`
  - Ensure no circular dependencies
  - Validate POLYGON_API_KEY environment variable is accessible

- [ ] **Task 5.3:** Type checking validation
  - Verify all type hints are correct
  - Check return type matches docstring specification
  - Ensure async/await usage is correct

### PHASE 6: Testing & Verification

- [ ] **Task 6.1:** Unit test the tool function directly
  - Test with valid POLYGON_API_KEY
  - Verify JSON response structure
  - Test error handling (invalid API key, network failure)
  - Validate datetime parsing from server_time field

- [ ] **Task 6.2:** Integration test with agent
  - Test queries: "Is the market open?", "What time is it?", "Market status?"
  - Verify tool is called correctly by agent
  - Check response includes all required fields
  - Validate no errors in agent execution

- [ ] **Task 6.3:** Compare with MCP tool behavior
  - Test same queries with old MCP-based get_market_status
  - Verify new tool provides equivalent or better data
  - Check response format is AI-friendly

### PHASE 7: Documentation Updates

- [ ] **Task 7.1:** Update CLAUDE.md
  - [ ] 7.1a: Update "Last Completed Task Summary" section
  - [ ] 7.1b: Document the Polygon direct API migration milestone
  - [ ] 7.1c: Update tool architecture description (10 tools: 7 MCP + 2 Finnhub + 1 Polygon direct)
  - [ ] 7.1d: Add migration notes about transitioning from MCP to direct API calls

- [ ] **Task 7.2:** Update README.md (if exists)
  - Update feature descriptions to mention Polygon direct API usage
  - Update environment variables section to ensure POLYGON_API_KEY is documented
  - Update tool count and capabilities

- [ ] **Task 7.3:** Add inline code comments
  - Document why direct API call is used instead of MCP
  - Explain datetime extraction from server_time field
  - Note this is first step in migration strategy

### PHASE 8: Environment Configuration

- [ ] **Task 8.1:** Verify .env file has POLYGON_API_KEY
  - Check `.env` file exists
  - Confirm `POLYGON_API_KEY` variable is set
  - Test API key is valid with test call

- [ ] **Task 8.2:** Update .env.example (if exists)
  - Add POLYGON_API_KEY with placeholder
  - Add comments explaining Polygon direct API usage
  - Document where to get API key

### PHASE 9: Deployment Preparation

- [ ] **Task 9.1:** Create migration notes
  - Document what changed: MCP get_market_status → Direct API get_market_status_and_date_time
  - Note impact: Additional datetime functionality
  - List benefits: Faster response, combined data, migration proof-of-concept

- [ ] **Task 9.2:** Update changelog
  - Add entry for new Polygon direct API tool
  - Note tool count change (9 → 10 tools)
  - Document migration strategy milestone

- [ ] **Task 9.3:** Pre-commit validation
  - Run all linters (pylint, type-check if configured)
  - Verify no breaking changes to existing tools
  - Test full application startup
  - Confirm both frontend and backend work correctly

---

## 🔧 Technical Implementation Details

### File Structure

```
src/backend/tools/
├── __init__.py                    # May need updating to export new tool
├── finnhub_tools.py              # Reference implementation (✅ existing)
└── polygon_tools.py              # ⭐ NEW FILE TO CREATE
```

### Dependencies

**Required Python Packages:**
- `polygon` (Polygon Python Library) - Should already be installed for MCP
- `agents` (OpenAI Agents SDK v0.2.9) - Already installed
- `os` (standard library)
- `json` (standard library)

**Environment Variables:**
- `POLYGON_API_KEY` - Must be set in .env file

### Integration Points

**Files to Modify:**
1. `src/backend/services/agent_service.py`
   - Import: Add get_market_status_and_date_time
   - create_agent(): Add to tools list
   - get_enhanced_agent_instructions(): Update RULE #4 and tool counts

**Files to Create:**
1. `src/backend/tools/polygon_tools.py`
   - New custom tool file with get_market_status_and_date_time function

**Files to Review (No Changes Expected):**
1. `src/backend/config.py` - API keys already configured
2. `.env` - POLYGON_API_KEY should already exist

---

## 📊 Expected Outcomes

### Tool Capabilities

**New Tool:** `get_market_status_and_date_time()`
- **Purpose:** Get current market status AND date/time in single call
- **Advantage:** Combines market status with server timestamp
- **Use Cases:**
  - "Is the market open?"
  - "What time is it?"
  - "Market status?"
  - "What's today's date?"
  - "Are markets open for trading?"

### Migration Benefits

1. **Proof of Concept:** First direct Polygon API tool (vs. MCP server tools)
2. **Performance:** Direct API may be faster than MCP routing
3. **Functionality:** Combined market status + datetime in one call
4. **Scalability:** Establishes pattern for future direct API migrations

### Tool Count Evolution

- **Before:** 9 tools (8 Polygon MCP + 1 Finnhub custom)
- **After:** 10 tools (7 Polygon MCP + 1 Finnhub custom + 1 Polygon direct + 1 removed MCP tool)
- **Net Change:** +1 total tool, migrated 1 MCP tool to direct API

---

## ⚠️ Important Notes

### Critical Success Factors

1. **No Code Implementation During Research Phase**
   - ✅ This document is PLANNING ONLY
   - ❌ No files created or modified yet
   - ⏳ Awaiting approval before proceeding to implementation

2. **Follow Established Patterns**
   - Use finnhub_tools.py as reference template
   - Follow OPENAI_CUSTOM_TOOLS_REFERENCE.md best practices
   - Maintain 10.00/10 Pylint score standard

3. **Error Handling**
   - All errors must return JSON (never raise exceptions to agent)
   - Provide descriptive error messages
   - Include error type classification

4. **Testing Requirements**
   - Unit test the tool function directly
   - Integration test with full agent
   - Verify no regression in existing tools

### Migration Strategy Context

**Current State:**
- 9 tools: 8 Polygon MCP + 1 Finnhub custom
- All Polygon data flows through MCP server

**Target State (This Task):**
- 10 tools: 7 Polygon MCP + 1 Finnhub custom + 1 Polygon direct
- Start migrating Polygon data to direct API calls

**Future State (TBD):**
- Fully migrate all Polygon tools to direct API
- Deprecate Polygon MCP server dependency
- Maintain only custom direct API tools

### Risk Mitigation

1. **API Key Validation:** Ensure POLYGON_API_KEY works before full implementation
2. **Response Format:** Validate MarketStatus model fields match documentation
3. **Backward Compatibility:** Ensure existing tools still work correctly
4. **Agent Behavior:** Test that agent selects correct tool for queries

---

## 📚 Reference Documentation

### Research Sources

1. **Polygon Python Library Documentation:**
   - Source: `mcp__docs-polygon-python__*` tools
   - Method: `client.get_market_status()`
   - Endpoint: `/v1/marketstatus/now`
   - Example: `examples/rest/stocks-market_status.py`

2. **Previous Implementation:**
   - File: `src/backend/tools/finnhub_tools.py` (commit c82b26e)
   - Pattern: @function_tool with async, JSON returns, error handling
   - Integration: `src/backend/services/agent_service.py`

3. **OpenAI Custom Tools Reference:**
   - File: `docs/OPENAI_CUSTOM_TOOLS_REFERENCE.md`
   - Guidelines: Tool creation, docstrings, error handling, best practices

### Key Reference Code

**Polygon Client Example:**
```python
from polygon import RESTClient

client = RESTClient()  # Uses POLYGON_API_KEY env var
result = client.get_market_status()
print(result)
```

**MarketStatus Model:**
```python
@modelclass
class MarketStatus:
    after_hours: Optional[bool] = None
    currencies: Optional[MarketCurrencies] = None
    early_hours: Optional[bool] = None
    exchanges: Optional[MarketExchanges] = None
    indicesGroups: Optional[MarketIndices] = None
    market: Optional[str] = None
    server_time: Optional[str] = None
```

---

## 🚀 Ready to Implement

### Prerequisites Checklist

- [x] Research completed on Polygon API
- [x] Reference implementation analyzed (Finnhub pattern)
- [x] Custom tools best practices reviewed
- [x] Response format designed
- [x] Integration points identified
- [x] Documentation plan created
- [x] Implementation plan approved

### Next Steps

1. **Await Approval:** Get confirmation to proceed with implementation
2. **Begin Phase 1:** Create polygon_tools.py file
3. **Follow Checklist:** Complete all tasks in sequential order
4. **Validate Each Phase:** Run linting and tests after each phase
5. **Update Documentation:** Keep CLAUDE.md updated with progress

---

**Status:** 📋 PLANNING COMPLETE - READY FOR IMPLEMENTATION
**Estimated Effort:** 2-3 hours for full implementation and testing
**Risk Level:** LOW - Following established patterns with proven API
