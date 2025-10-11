# TODO Implementation Plan: Add Tradier Options Expiration Dates Tool

**Task**: Add new AI Agent Tool "get_options_expiration_dates" using Tradier Python Brokerage API

**Status**: Phase 2 - Planning Complete, Ready for Implementation

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE ENFORCEMENT

**YOU MUST use the following tools systematically throughout implementation:**

1. **Sequential-Thinking** - Use for:
   - Code structure analysis before writing
   - Decision-making for implementation approach
   - Verification of changes before committing

2. **Serena Tools** - Use for:
   - `find_symbol`: Locate existing functions to understand patterns
   - `get_symbols_overview`: Understand file structures
   - `insert_after_symbol`: Add new functions/imports
   - `replace_symbol_body`: Modify agent instructions
   - `write_memory`: Update project memories

3. **Standard Tools** - Use for:
   - `Read`: View file contents
   - `Edit`: Simple text modifications
   - `Bash`: Run tests and validation

**VIOLATION = FAILURE**: Using wrong tools or skipping tool usage will result in implementation failure.

---

## Phase 1: Research ✅ COMPLETE

- ✅ Researched Tradier API endpoint structure
- ✅ Analyzed existing tool patterns (finnhub_tools.py, polygon_tools.py)
- ✅ Reviewed OpenAI custom tools reference guide
- ✅ Understood agent service integration points
- ✅ Reviewed test suite structure

**Key Findings**:
- Tool Pattern: @function_tool decorator, async def, comprehensive docstring
- API Pattern: requests library with Bearer token authentication
- Integration: Import in agent_service.py, add to tools list, update instructions
- Testing: Add tests after "Technical Analysis" for SPY (Test 14) and NVDA (Test 30)

---

## Phase 2: Planning ✅ COMPLETE

**Implementation Strategy**:

### File Changes Required (5 files):
1. `src/backend/tools/tradier_tools.py` - NEW FILE
2. `src/backend/tools/__init__.py` - MODIFY
3. `src/backend/services/agent_service.py` - MODIFY
4. `test_cli_regression.sh` - MODIFY
5. `.env` - VERIFY (TRADIER_API_KEY exists)

### Agent Instructions Updates:
- Line 36: Update tool count (12 → 13)
- Line 35: Add Tradier mention to TOOLS description
- After RULE #9: Add RULE #10 for options expiration dates

---

## Phase 3: Implementation (PENDING - Use Tools Systematically)

### 🔴 CRITICAL: Use Sequential-Thinking Before Each Major Step

### Step 1: Create tradier_tools.py ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Sequential-Thinking to plan file structure
- ✅ Use Standard Write to create new file
- ✅ Follow finnhub_tools.py pattern exactly

**Implementation Checklist**:
```python
# File: src/backend/tools/tradier_tools.py

# 1. Module docstring (lines 1-4)
"""
Tradier custom tools for OpenAI AI Agent.
Provides options expiration dates via Tradier API.
"""

# 2. Imports (lines 6-9)
import json
import os
import requests
from agents import function_tool

# 3. Helper function for client/API key (lines 11-18)
def _get_tradier_api_key():
    """Get Tradier API key from environment.

    Lazy initialization ensures .env is loaded before accessing API key.
    """
    return os.getenv("TRADIER_API_KEY")

# 4. Main tool function (lines 20-120)
@function_tool
async def get_options_expiration_dates(ticker: str) -> str:
    """Get valid options expiration dates for a ticker from Tradier API.

    Use this tool when the user requests options expiration dates for a specific ticker.
    This provides all available expiration dates for options contracts on the underlying stock.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "SPY", "NVDA").
                Must be a valid ticker symbol.

    Returns:
        JSON string containing expiration dates array with format:
        {
            "ticker": "NVDA",
            "expiration_dates": [
                "2025-10-17",
                "2025-10-24",
                "2025-10-31",
                ...
            ],
            "count": 21,
            "source": "Tradier"
        }

        Or error format:
        {
            "error": "error_type",
            "message": "descriptive error message",
            "ticker": "SYMBOL"
        }

    Note:
        - Returns all available expiration dates for the ticker
        - Dates are in YYYY-MM-DD format
        - Dates are sorted chronologically (earliest to latest)
        - Includes weekly and monthly expiration dates
        - Data updates daily

    Examples:
        - "Get options expiration dates for SPY"
        - "What are the available expiration dates for NVDA options?"
        - "Show me TSLA options expiration dates"
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

        # Get API key
        api_key = _get_tradier_api_key()
        if not api_key:
            return json.dumps({
                "error": "Configuration error",
                "message": "TRADIER_API_KEY not found in environment",
                "ticker": ticker
            })

        # Call Tradier API
        url = f"https://api.tradier.com/v1/markets/options/expirations?symbol={ticker}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.get(url, headers=headers, timeout=10)

        # Check HTTP status
        if response.status_code != 200:
            return json.dumps({
                "error": "API request failed",
                "message": f"Tradier API returned status {response.status_code}",
                "ticker": ticker
            })

        # Parse response
        data = response.json()

        # Extract expiration dates
        expirations = data.get("expirations", {})
        dates = expirations.get("date", [])

        # Check if we got valid data
        if not dates:
            return json.dumps({
                "error": "No data",
                "message": f"No expiration dates available for ticker: {ticker}. Verify ticker symbol is valid.",
                "ticker": ticker
            })

        # Ensure dates is a list (API returns single string if only 1 date)
        if isinstance(dates, str):
            dates = [dates]

        # Format response
        return json.dumps({
            "ticker": ticker,
            "expiration_dates": dates,
            "count": len(dates),
            "source": "Tradier"
        })

    except requests.exceptions.Timeout:
        return json.dumps({
            "error": "Timeout",
            "message": f"Tradier API request timed out for {ticker}",
            "ticker": ticker
        })
    except requests.exceptions.RequestException as e:
        return json.dumps({
            "error": "Network error",
            "message": f"Failed to connect to Tradier API: {str(e)}",
            "ticker": ticker
        })
    except Exception as e:
        return json.dumps({
            "error": "Unexpected error",
            "message": f"Failed to retrieve expiration dates for {ticker}: {str(e)}",
            "ticker": ticker
        })
```

**Validation**:
- File created successfully
- Imports are correct
- Function signature matches pattern
- Docstring is comprehensive
- Error handling is robust

---

### Step 2: Update tools/__init__.py ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Serena `find_symbol` to see current __all__ list
- ✅ Use Standard Edit to add import and export

**Implementation**:
```python
# Add import
from .tradier_tools import get_options_expiration_dates

# Update __all__
__all__ = ["get_stock_quote", "get_options_expiration_dates"]
```

**Validation**:
- Import added correctly
- __all__ list updated
- No syntax errors

---

### Step 3: Import Tradier tool in agent_service.py ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Serena `find_symbol` to locate import section
- ✅ Use Serena `insert_after_symbol` OR Standard Edit to add import

**Implementation Location**: Line ~8 (after finnhub import)
```python
from ..tools.finnhub_tools import get_stock_quote
from ..tools.tradier_tools import get_options_expiration_dates  # NEW
from ..tools.polygon_tools import (
    get_call_options_chain,
    ...
)
```

**Validation**:
- Import added in correct location
- No circular imports
- No syntax errors

---

### Step 4: Add tool to agent tools list ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Serena `find_symbol` with name_path="create_agent" to locate function
- ✅ Use Sequential-Thinking to plan where to insert
- ✅ Use Serena `replace_symbol_body` OR Standard Edit to add to tools list

**Implementation Location**: Line ~478-490 in create_agent() function
```python
analysis_agent = Agent(
    name="Financial Analysis Agent",
    instructions=get_enhanced_agent_instructions(),
    tools=[
        get_stock_quote,
        get_options_expiration_dates,  # NEW - Add after get_stock_quote
        get_market_status_and_date_time,
        get_OHLC_bars_custom_date_range,
        ...
        get_call_options_chain,
        get_put_options_chain,
    ],
    model=settings.default_active_model,
    model_settings=get_optimized_model_settings(),
)
```

**Validation**:
- Tool added to list
- Proper position (after get_stock_quote)
- Comma syntax correct
- No syntax errors

---

### Step 5: Update agent instructions ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Sequential-Thinking to plan instruction updates
- ✅ Use Serena `find_symbol` with name_path="get_enhanced_agent_instructions"
- ✅ Use Serena `replace_symbol_body` OR Standard Edit to update

**Three Updates Required**:

#### Update 1: Tool count (Line 36)
**Before**:
```
🔴 CRITICAL: YOU MUST ONLY USE THE FOLLOWING 12 SUPPORTED TOOLS: [...]
```

**After**:
```
🔴 CRITICAL: YOU MUST ONLY USE THE FOLLOWING 13 SUPPORTED TOOLS: [get_stock_quote, get_options_expiration_dates, get_market_status_and_date_time, ...]
```

#### Update 2: TOOLS description (Line 35)
**Before**:
```
TOOLS: Use Finnhub for all ticker quotes (supports parallel calls), Polygon.io direct API for all market data (status/datetime/TA indicators/OHLC bars/options chains).
```

**After**:
```
TOOLS: Use Finnhub for all ticker quotes (supports parallel calls), Tradier for options expiration dates, Polygon.io direct API for all market data (status/datetime/TA indicators/OHLC bars/options chains).
```

#### Update 3: Add RULE #10 (After RULE #9, before emoji formatting section)
**Insert Location**: After line 273 (after RULE #9 ends)

**New Content**:
```python
RULE #10: OPTIONS EXPIRATION DATES = USE get_options_expiration_dates
- 🔴 **WHEN TO USE**: User requests available expiration dates for options contracts
- 🔴 **REQUIRED PARAMETER**: ticker (str) - Stock ticker symbol
- 🔴 **RESPONSE FORMAT**: JSON with array of expiration dates in YYYY-MM-DD format
- 🔴 **USE CASES**:
  - "What are the available expiration dates for SPY options?"
  - "Get options expiration dates for NVDA"
  - "Show me TSLA options expiration dates"
  - "When do AAPL options expire?"
- 🔴 **DATA SOURCE**: Tradier API (all available expiration dates)
- 🔴 **DATE FORMAT**: YYYY-MM-DD (chronologically sorted)
- 🔴 **INCLUDES**: Both weekly and monthly expirations
- 📊 **WORKFLOW**:
  1. Identify user is requesting expiration dates
  2. Extract ticker symbol from request
  3. Call get_options_expiration_dates(ticker='SYMBOL')
  4. Present dates in readable format
- 📊 **DISPLAY FORMAT**: Present dates as comma-separated list or bullet points
  - Example: "SPY options expiration dates: 2025-10-17, 2025-10-24, 2025-10-31, 2025-11-07..."
  - Or: "Available NVDA expiration dates:\n• 2025-10-17\n• 2025-10-24\n• 2025-10-31..."
- ❌ **COMMON MISTAKES**:
  - Using get_call_options_chain or get_put_options_chain when user only wants expiration dates
  - Not calling the tool when user asks about "when options expire"
  - Confusing expiration dates with options chain data

```

**Validation**:
- Tool count updated (12 → 13)
- Tool list includes get_options_expiration_dates
- TOOLS description mentions Tradier
- RULE #10 added with comprehensive guidance
- No formatting errors
- Instructions remain coherent

---

### Step 6: Update test_cli_regression.sh ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Sequential-Thinking to plan test insertion points
- ✅ Use Standard Read to review test structure
- ✅ Use Standard Edit to add new test cases

**Two Test Cases to Add**:

#### Test Case 1: SPY Options Expiration Dates
**Insert Location**: After Test 13 "Technical Analysis: $SPY" (becomes new Test 14)
**Shift existing tests**: Test 14→16 become Test 15→17

**Add to prompts array** (line ~84):
```bash
"Technical Analysis: \$SPY"
"Get options expiration dates for SPY"  # NEW TEST 14
"Get the SPY Call Options Chain Expiring this Friday"
```

**Add to test_names array** (line ~128):
```bash
"Test_13_SPY_Technical_Analysis"
"Test_14_SPY_Options_Expiration_Dates"  # NEW TEST NAME
"Test_15_SPY_Call_Options_Chain"  # RENUMBERED (was Test_14)
```

#### Test Case 2: NVDA Options Expiration Dates
**Insert Location**: After Test 29 "Technical Analysis: $NVDA" (becomes new Test 30)
**Shift existing tests**: Test 30→32 become Test 31→33

**Add to prompts array** (line ~101):
```bash
"Technical Analysis: \$NVDA"
"Get options expiration dates for NVDA"  # NEW TEST 30
"Get the NVDA Call Options Chain Expiring this Friday"
```

**Add to test_names array** (line ~145):
```bash
"Test_29_NVDA_Technical_Analysis"
"Test_30_NVDA_Options_Expiration_Dates"  # NEW TEST NAME
"Test_31_NVDA_Call_Options_Chain"  # RENUMBERED (was Test_30)
```

**Update Test Count**:
- Line 3: Comment "# CLI Test Regression Script - NEW 38-Test Suite" → "# CLI Test Regression Script - NEW 40-Test Suite"
- Line 16: "# - SPY Test Sequence: Tests 1-16" → "# - SPY Test Sequence: Tests 1-17"
- Line 17: "# - NVDA Test Sequence: Tests 17-32" → "# - NVDA Test Sequence: Tests 18-33"
- Line 18: "# - Multi-Ticker Test Sequence: Tests 33-38" → "# - Multi-Ticker Test Sequence: Tests 34-40"
- Line 19: "# Total: 38 tests per loop" → "# Total: 40 tests per loop"
- Line 159: "total_tests=${#prompts[@]}" (auto-calculated, no change needed)

**Validation**:
- 2 new test cases added (SPY + NVDA)
- Test numbers properly renumbered
- Total test count: 40 (was 38)
- Test sequence integrity maintained
- Comments updated

---

### Step 7: Verify .env has TRADIER_API_KEY ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Bash to check .env file

**Command**:
```bash
cat .env | grep TRADIER_API_KEY
```

**Expected Output**:
```
TRADIER_API_KEY=<your_key_here>
```

**If Missing**: Add to .env file (user must provide key)

**Validation**:
- TRADIER_API_KEY exists in .env
- Key value is not empty

---

## Phase 4: Testing (MANDATORY - DO NOT SKIP)

### 🔴 CRITICAL: Testing is REQUIRED for Task Completion

### Step 8: Quick CLI Test with 3 Tickers ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Bash to run CLI
- ✅ Test each ticker individually

**Test Commands**:
```bash
# Test 1: SPY
echo "Get options expiration dates for SPY" | uv run src/backend/main.py

# Test 2: NVDA
echo "Get options expiration dates for NVDA" | uv run src/backend/main.py

# Test 3: SOUN
echo "Get options expiration dates for SOUN" | uv run src/backend/main.py
```

**Expected Output for Each**:
- Ticker symbol confirmed
- Array of expiration dates in YYYY-MM-DD format
- Count of dates returned
- Source: "Tradier"
- Response time < 10s

**Validation**:
- All 3 tickers return valid data
- No errors or exceptions
- Dates are properly formatted
- Tool is working correctly

---

### Step 9: Run Full Test Suite ⏳ PENDING

**Tool Enforcement**:
- ✅ MANDATORY: Use Bash to execute test suite
- ✅ MANDATORY: Show results to user

**Command**:
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Expected Results**:
- **Total Tests**: 40/40 PASSED (100% success rate)
- **New Tests**: Test 14 (SPY expirations) and Test 30 (NVDA expirations) both PASS
- **Average Response Time**: < 15s (EXCELLENT rating)
- **Test Report**: `test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log`
- **Session Persistence**: VERIFIED (single session for all tests)

**IF ANY TEST FAILS**:
1. Review test report log file
2. Identify failure cause
3. Fix implementation
4. Re-run tests
5. Repeat until 100% pass rate

**Validation**:
- Test suite executed successfully
- 40/40 tests PASSED (100%)
- Test report generated
- Evidence provided to user
- Performance metrics acceptable

---

## Phase 5: Serena Project Memories Update

### Step 10: Update tech_stack.md Memory ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Serena `read_memory` to get current content
- ✅ Use Sequential-Thinking to plan updates
- ✅ Use Serena `write_memory` to save updates

**Updates Required**:

1. **Data Sources Section** (Line ~30):
   - Add Tradier to the list
   - Update tool counts

**Before**:
```markdown
- **Polygon.io**: Direct Python API integration (12 tools)
- **Finnhub**: Custom Python API integration (1 tool)
- **Total AI Agent Tools**: 12
```

**After**:
```markdown
- **Polygon.io**: Direct Python API integration (11 tools)
- **Finnhub**: Custom Python API integration (1 tool)
- **Tradier**: Custom Python API integration (1 tool)
- **Total AI Agent Tools**: 13 (updated Oct 10, 2025)
```

2. **Direct API Tools Section** (Line ~200):
   - Add new section for Tradier tools

**Add after "Finnhub Custom API (1 tool):"**:
```markdown
**Tradier Custom API (1 tool - Added Oct 10, 2025):**
- `get_options_expiration_dates` - Get all valid options expiration dates for a ticker
```

3. **Recent Updates Section** (at bottom):
   - Add entry for this change

**Add new entry**:
```markdown
### Tradier Options Expiration Tool (Oct 10, 2025)
- **Tool Added**: `get_options_expiration_dates`
- **Purpose**: Fetch all available options expiration dates for a ticker
- **API**: Tradier Brokerage API (markets/options/expirations endpoint)
- **Integration**: Custom Python tool using requests library
- **Authentication**: Bearer token via TRADIER_API_KEY env variable
- **Response Format**: JSON with array of dates in YYYY-MM-DD format
- **Agent Instructions**: New RULE #10 added for usage guidance
- **Test Coverage**: 2 new tests added (SPY Test 14, NVDA Test 30)
- **Total Tools**: 13 (was 12)
- **Test Results**: 40/40 PASSED (100% success rate)
```

**Validation**:
- tech_stack.md memory updated
- Tool counts accurate
- Tradier section added
- Recent updates documented

---

### Step 11: Update testing_procedures.md Memory ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Serena `read_memory` to get current content
- ✅ Use Sequential-Thinking to plan updates
- ✅ Use Serena `write_memory` to save updates

**Updates Required**:

1. **Test Coverage Section** (Line ~30):
   - Update test counts

**Before**:
```markdown
**Test Coverage (36 tests total - NEW Oct 8, 2025):**

1. **SPY Test Sequence (Tests 1-15)**:
...
2. **NVDA Test Sequence (Tests 16-30)**:
...
3. **Multi-Ticker Test Sequence (Tests 31-36)**:
```

**After**:
```markdown
**Test Coverage (40 tests total - UPDATED Oct 10, 2025):**

1. **SPY Test Sequence (Tests 1-17)**:
   - Market Status
   - Current Price: $SPY
   - Today's Closing Price: $SPY
   - Yesterday's Closing Price: $SPY
   - Last week's Performance: $SPY
   - Stock Price on the previous week's Friday: $SPY (dynamic date)
   - Daily Stock Price bars Analysis from the last 2 trading weeks: $SPY (dynamic date)
   - RSI-14: $SPY
   - MACD: $SPY
   - SMA 20/50/200: $SPY
   - EMA 20/50/200: SPY
   - Support & Resistance Levels: $SPY
   - Technical Analysis: $SPY
   - **Get options expiration dates for SPY** (NEW TEST 14)
   - Get First 3 Call Option Quotes expiring this Friday: $SPY
   - Get First 3 Put Option Quotes expiring this Friday: $SPY
   - Options Wall Analysis: $SPY

2. **NVDA Test Sequence (Tests 18-33)**:
   - Same pattern as SPY (16 tests)
   - **Get options expiration dates for NVDA** (NEW TEST 30)

3. **Multi-Ticker Test Sequence (Tests 34-40)**:
   - Market Status
   - Current Price: $WDC, $AMD, $GME
   - MACD Analysis: $WDC, $AMD, $GME
   - Average Trading Volume comparison: $WDC, $AMD, $GME
   - Technical Analysis: $WDC, $AMD, $GME
   - Relative Strength Analysis: $WDC, $AMD, $GME
   - Daily bars Analysis from the last 2 trading weeks: $WDC, $AMD, $GME
```

2. **Expected Performance Section**:
   - Update test counts

**Update all references**:
- "36 tests" → "40 tests"
- "36/36" → "40/40"

3. **Recent Updates Section** (at bottom):
   - Add entry for test changes

**Add new entry**:
```markdown
### Oct 10, 2025: Tradier Options Expiration Tests Added

**New Test Cases:**
- Test 14: SPY Options Expiration Dates
- Test 30: NVDA Options Expiration Dates

**Test Prompts:**
- "Get options expiration dates for SPY"
- "Get options expiration dates for NVDA"

**Purpose**: Validate new Tradier API integration for fetching options expiration dates

**Test Suite Updates:**
- Total tests: 38 → 40
- SPY sequence: 16 tests → 17 tests
- NVDA sequence: 16 tests → 17 tests (including renumbering)
- Multi-ticker: Unchanged (6 tests)

**Expected Output:**
- JSON with ticker, expiration_dates array, count, source
- Dates in YYYY-MM-DD format
- Response time < 10s
- No errors

**Test Results:**
- Total: 40/40 PASSED (100%)
- New tests: Both PASSED
- Performance: EXCELLENT rating maintained
```

**Validation**:
- testing_procedures.md memory updated
- Test counts accurate (40 total)
- New tests documented
- Test sequences properly renumbered

---

## Phase 6: Final Git Commit (Atomic Commit Workflow)

### 🔴 CRITICAL: Follow Proper Atomic Commit Workflow

### Step 12: Update CLAUDE.md Documentation ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Standard Edit to update CLAUDE.md

**Update Location**: Replace "Last Completed Task Summary" section (lines 12-179)

**New Content**: Create comprehensive summary following the template pattern

**Validation**:
- CLAUDE.md updated with complete task summary
- Test results included
- Performance metrics documented

---

### Step 13: Verify ALL Work Complete ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Bash to check git status
- ✅ Review all changes

**Commands**:
```bash
# Review all changed/new files
git status

# Review all changes in detail
git diff
```

**Checklist**:
- [ ] tradier_tools.py created
- [ ] tools/__init__.py updated
- [ ] agent_service.py updated (imports + tools list + instructions)
- [ ] test_cli_regression.sh updated (2 new tests)
- [ ] .env has TRADIER_API_KEY
- [ ] Quick CLI tests completed successfully
- [ ] Full test suite: 40/40 PASSED
- [ ] Test report generated
- [ ] tech_stack.md memory updated
- [ ] testing_procedures.md memory updated
- [ ] CLAUDE.md updated
- [ ] TODO_task_plan.md exists (this file)

**Validation**:
- ALL checklist items complete
- ALL files ready for commit
- NO unstaged changes remaining

---

### Step 14: Stage All Files At Once ⏳ PENDING

**Tool Enforcement**:
- ✅ CRITICAL: This is the FIRST time running git add
- ✅ Stage ALL files in ONE command

**Command**:
```bash
git add -A
```

**Validation**:
- All files staged
- Nothing left unstaged

---

### Step 15: Verify Staging Immediately ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Bash to verify staging

**Command**:
```bash
git status
```

**Expected Output**:
```
Changes to be committed:
  new file:   src/backend/tools/tradier_tools.py
  modified:   src/backend/tools/__init__.py
  modified:   src/backend/services/agent_service.py
  modified:   test_cli_regression.sh
  modified:   .serena/memories/tech_stack.md
  modified:   .serena/memories/testing_procedures.md
  modified:   CLAUDE.md
  new file:   TODO_task_plan.md
  new file:   test-reports/test_cli_regression_loop1_*.log
```

**Validation**:
- ALL changed files staged
- NOTHING unstaged
- Ready for commit

---

### Step 16: Create Atomic Commit IMMEDIATELY ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Bash to commit within 60 seconds of staging
- ✅ Use HEREDOC format for commit message

**Command**:
```bash
git commit -m "$(cat <<'EOF'
[TRADIER] Add options expiration dates tool for AI Agent

- Add new AI Agent tool: get_options_expiration_dates
- Integration: Tradier Brokerage API (markets/options/expirations)
- Authentication: Bearer token via TRADIER_API_KEY env variable
- Response format: JSON with array of dates in YYYY-MM-DD format
- Total tools: 12 → 13

Code Changes:
- NEW: src/backend/tools/tradier_tools.py (120 lines)
  - Async function with @function_tool decorator
  - Comprehensive error handling (timeout, network, validation)
  - Follows OpenAI custom tools best practices
- MODIFIED: src/backend/tools/__init__.py
  - Import get_options_expiration_dates
  - Export in __all__ list
- MODIFIED: src/backend/services/agent_service.py
  - Import Tradier tool
  - Add to agent tools list (position 2, after get_stock_quote)
  - Update TOOLS description (added Tradier mention)
  - Update tool count: 12 → 13 tools (line 36)
  - Add RULE #10: Options expiration dates usage guidance

Test Changes:
- MODIFIED: test_cli_regression.sh
  - Add Test 14: SPY options expiration dates
  - Add Test 30: NVDA options expiration dates
  - Update test counts: 38 → 40 tests
  - Renumber subsequent tests (14→17 become 15→18, etc.)
  - Update test sequence documentation

Test Results:
- Total: 40/40 PASSED (100% success rate)
- New Tests: Both PASSED (Test 14 SPY, Test 30 NVDA)
- Avg Response Time: [X.XX]s (EXCELLENT rating)
- Session Duration: [X] min [XX] sec
- Test Report: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log

Quick CLI Tests:
- SPY: ✅ Valid expiration dates returned
- NVDA: ✅ Valid expiration dates returned
- SOUN: ✅ Valid expiration dates returned

Documentation Updates:
- MODIFIED: .serena/memories/tech_stack.md
  - Add Tradier to Data Sources section
  - Update tool counts (12 → 13)
  - Add Tradier Custom API section
  - Document new tool in Recent Updates
- MODIFIED: .serena/memories/testing_procedures.md
  - Update test coverage section (38 → 40 tests)
  - Document new test cases (Test 14, Test 30)
  - Update test sequences and renumbering
  - Add Recent Updates entry
- MODIFIED: CLAUDE.md
  - Update Last Completed Task Summary section
  - Document complete implementation details
  - Include test results and validation

Implementation Details:
- Pattern: Followed finnhub_tools.py structure exactly
- API: Tradier markets/options/expirations endpoint
- Error Handling: Timeout, network, validation, empty data
- Response: JSON with ticker, expiration_dates, count, source
- Agent Instructions: RULE #10 provides comprehensive usage guidance
- Tool Position: After get_stock_quote (logical grouping)

Architecture:
- Direct API integration (no MCP)
- Async/await for non-blocking I/O
- Environment variable for API key
- Consistent with existing tool patterns

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Validation**:
- Commit created successfully
- Commit message comprehensive
- All files included in commit

---

### Step 17: Push to Remote IMMEDIATELY ⏳ PENDING

**Tool Enforcement**:
- ✅ Use Bash to push within 60 seconds of commit

**Command**:
```bash
git push
```

**Expected Output**:
```
Counting objects: X, done.
Delta compression using up to N threads.
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
Total X (delta Y), reused 0 (delta 0)
To github.com:user/market-parser-polygon-mcp.git
   abc1234..def5678  master -> master
```

**Validation**:
- Push successful
- All changes in remote repository
- Task COMPLETE

---

## Success Criteria

**Task is COMPLETE when ALL of the following are TRUE**:

✅ tradier_tools.py created with get_options_expiration_dates function
✅ tools/__init__.py exports new tool
✅ agent_service.py imports and registers tool
✅ Agent instructions updated (tool count, RULE #10)
✅ test_cli_regression.sh has 2 new tests (40 total)
✅ Quick CLI tests: SPY, NVDA, SOUN all return valid data
✅ Full test suite: 40/40 PASSED (100%)
✅ Test report generated and reviewed
✅ tech_stack.md memory updated
✅ testing_procedures.md memory updated
✅ CLAUDE.md Last Completed Task updated
✅ All files staged with git add -A
✅ Atomic commit created with comprehensive message
✅ Changes pushed to remote repository

---

## Tool Usage Tracking

**This plan enforces MANDATORY tool usage throughout implementation. Track usage here:**

### Phase 3: Implementation
- [ ] Sequential-Thinking: Plan tradier_tools.py structure
- [ ] Standard Write: Create tradier_tools.py
- [ ] Serena find_symbol: Locate __all__ in __init__.py
- [ ] Standard Edit: Update __init__.py
- [ ] Serena find_symbol: Locate import section in agent_service.py
- [ ] Serena insert_after_symbol OR Standard Edit: Add Tradier import
- [ ] Serena find_symbol: Locate create_agent function
- [ ] Sequential-Thinking: Plan tools list insertion
- [ ] Serena replace_symbol_body OR Standard Edit: Add to tools list
- [ ] Sequential-Thinking: Plan agent instructions updates
- [ ] Serena find_symbol: Locate get_enhanced_agent_instructions
- [ ] Serena replace_symbol_body OR Standard Edit: Update instructions
- [ ] Sequential-Thinking: Plan test insertions
- [ ] Standard Read: Review test structure
- [ ] Standard Edit: Add 2 new test cases
- [ ] Bash: Verify TRADIER_API_KEY in .env

### Phase 4: Testing
- [ ] Bash: Quick test SPY
- [ ] Bash: Quick test NVDA
- [ ] Bash: Quick test SOUN
- [ ] Bash: Run full test suite (MANDATORY)
- [ ] Bash: Review test results

### Phase 5: Serena Updates
- [ ] Serena read_memory: Get tech_stack.md content
- [ ] Sequential-Thinking: Plan tech_stack.md updates
- [ ] Serena write_memory: Update tech_stack.md
- [ ] Serena read_memory: Get testing_procedures.md content
- [ ] Sequential-Thinking: Plan testing_procedures.md updates
- [ ] Serena write_memory: Update testing_procedures.md

### Phase 6: Git Commit
- [ ] Standard Edit: Update CLAUDE.md
- [ ] Bash: git status (review changes)
- [ ] Bash: git diff (review details)
- [ ] Bash: git add -A (stage all at once)
- [ ] Bash: git status (verify staging)
- [ ] Bash: git commit (atomic commit)
- [ ] Bash: git push (immediate push)

**FAILURE = Not using tools as specified above**

---

## Implementation Status

**Current Phase**: Phase 2 - Planning ✅ COMPLETE
**Next Phase**: Phase 3 - Implementation ⏳ READY TO START

**Planning Complete**: All implementation steps documented with tool enforcement

**Ready for Phase 3**: Begin implementation following this plan systematically

---

**Last Updated**: October 10, 2025
**Status**: Planning Phase Complete, Implementation Phase Ready
