# Holistic Cross-Component Optimization - Implementation TODO Task Plan

## Overview

**Goal:** Eliminate cross-component duplication between AI Agent Tool Descriptions and System Instructions to reduce token usage while maintaining full functionality and regression test coverage.

**Current State:** 88 tokens duplicated across 16 locations in 2 components
**Target State:** Centralized "COMMON FORMATS" section with references from tools/rules
**Expected Reduction:** ~58 tokens net savings (88 tokens removed - 30 tokens added for section)

**Key Strategy:** Create centralized format specifications that both tool descriptions and system instructions reference, instead of repeating format details in multiple locations.

**Phases:**
1. ✅ Phase 1: Research (COMPLETED)
2. ✅ Phase 2: Planning (CURRENT - Generating this plan)
3. ⏭️ Phase 3: Implementation
4. ⏭️ Phase 4: Testing
5. ⏭️ Phase 5: Final Commit

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE ENFORCEMENT

**YOU MUST use Sequential-Thinking and Serena tools throughout ENTIRE implementation:**

- **START every phase** with Sequential-Thinking for systematic approach
- **Use Serena tools** for code analysis (`mcp__serena__find_symbol`, `mcp__serena__replace_symbol_body`)
- **Use Sequential-Thinking** repeatedly for complex reasoning and planning
- **Use Standard Edit** for multi-line replacements in docstrings/instructions
- **NEVER stop using advanced tools** until task completion

---

## Phase 3: Implementation

### Step 1: Pre-Implementation Verification

**Objective:** Verify research findings and prepare for implementation

**Sub-tasks:**

1.1. **Use Sequential-Thinking** to review implementation approach
   - Confirm all 12 modifications are clearly defined
   - Verify modification order (Common Formats first, then tools, then rules)
   - Plan validation checkpoints

1.2. **Read current state of all 3 files**
   - `Read(file_path="src/backend/services/agent_service.py")`
   - `Read(file_path="src/backend/tools/tradier_tools.py")`
   - `Read(file_path="src/backend/tools/polygon_tools.py")`
   - Document current line numbers for all changes

1.3. **Verify research findings match current state**
   - Confirm "YYYY-MM-DD format" appears in expected locations
   - Confirm "comma-separated, no spaces" appears in expected locations
   - Confirm "Formatted" prefix appears in expected locations

**Validation:** All 3 files read, current state matches research findings

---

### Step 2: Add COMMON FORMATS Section to agent_service.py

**Objective:** Create centralized format specifications section

**Current State (Line ~30):**
```python
def get_enhanced_agent_instructions():
    """
    Generate enhanced agent instructions for financial analysis.

    Returns:
        Enhanced agent instructions string
    """
    datetime_context = get_current_datetime_context()
    return f"""You are a financial analyst with real-time market data access.

{datetime_context}

🔴🔴🔴 CRITICAL TOOL SELECTION RULES - READ CAREFULLY 🔴🔴🔴
```

**New State (Insert after line ~30, before CRITICAL TOOL SELECTION RULES):**
```python
def get_enhanced_agent_instructions():
    """
    Generate enhanced agent instructions for financial analysis.

    Returns:
        Enhanced agent instructions string
    """
    datetime_context = get_current_datetime_context()
    return f"""You are a financial analyst with real-time market data access.

{datetime_context}

📋 COMMON FORMATS (Reference for all tools and rules):
- Date Format: YYYY-MM-DD (e.g., "2025-10-28")
- Multi-Ticker Format: Comma-separated, no spaces (e.g., "SPY,QQQ,IWM")
- Table Format: Markdown tables with pipe separators (|)

🔴🔴🔴 CRITICAL TOOL SELECTION RULES - READ CAREFULLY 🔴🔴🔴
```

**Sub-tasks:**

2.1. **Use Sequential-Thinking** to verify placement strategy
   - Section appears AFTER datetime_context (dynamic info first)
   - Section appears BEFORE rules (so rules can reference it)
   - Section is visually distinct with emoji prefix

2.2. **Use Edit tool** to insert COMMON FORMATS section
   - Find exact line with `{datetime_context}`
   - Insert new section after datetime_context and before CRITICAL TOOL SELECTION RULES
   - Use Edit tool with old_string = section from datetime_context to CRITICAL RULES
   - Use new_string = same section WITH Common Formats added

2.3. **Verify insertion**
   - Read agent_service.py again
   - Confirm COMMON FORMATS section appears in correct location
   - Confirm formatting is correct (emoji, bullets, examples)

**Validation:** COMMON FORMATS section added, +30 tokens, section appears before all rules

**Token Impact:** +30 tokens (new content)

---

### Step 3: Optimize get_stock_quote() in tradier_tools.py

**Current Docstring (Lines ~73-78):**
```python
"""Get real-time stock quote(s) for one or more tickers from Tradier API.

Args:
    ticker: Stock ticker symbol(s). Single: "AAPL" or multiple: "AAPL,TSLA,NVDA" (comma-separated, no spaces).

Returns:
    JSON string with quote data (ticker, current_price, change, percent_change, high, low, open, previous_close, source).
```

**New Docstring:**
```python
"""Get real-time stock quote(s) for one or more tickers from Tradier API.

Args:
    ticker: Stock ticker symbol(s). Single: "AAPL" or multiple: "AAPL,TSLA,NVDA" (see Common Formats).

Returns:
    JSON string with quote data (ticker, current_price, change, percent_change, high, low, open, previous_close, source).
```

**Sub-tasks:**

3.1. **Use Serena** to read current function
   - `mcp__serena__find_symbol(name_path="get_stock_quote", relative_path="src/backend/tools/tradier_tools.py", include_body=true)`
   - Verify current docstring content

3.2. **Use Edit tool** to update docstring
   - old_string: 'ticker: Stock ticker symbol(s). Single: "AAPL" or multiple: "AAPL,TSLA,NVDA" (comma-separated, no spaces).'
   - new_string: 'ticker: Stock ticker symbol(s). Single: "AAPL" or multiple: "AAPL,TSLA,NVDA" (see Common Formats).'

3.3. **Verify change**
   - Use Serena to read function again
   - Confirm "(see Common Formats)" appears instead of "(comma-separated, no spaces)"

**Validation:** Docstring updated, -8 tokens saved

**Token Impact:** -8 tokens

---

### Step 4: Optimize get_options_expiration_dates() in tradier_tools.py

**Current Docstring (Lines ~122-127):**
```python
"""Get available options expiration dates for a ticker from Tradier API.

Args:
    ticker: Stock ticker symbol (e.g., "AAPL", "SPY").

Returns:
    JSON string with expiration dates array (ticker, expiration_dates[], count, source).
    Dates in YYYY-MM-DD format, sorted chronologically.
```

**New Docstring:**
```python
"""Get available options expiration dates for a ticker from Tradier API.

Args:
    ticker: Stock ticker symbol (e.g., "AAPL", "SPY").

Returns:
    JSON string with expiration dates array (ticker, expiration_dates[], count, source).
    Dates sorted chronologically (see Common Formats).
```

**Sub-tasks:**

4.1. **Use Serena** to read current function
   - `mcp__serena__find_symbol(name_path="get_options_expiration_dates", relative_path="src/backend/tools/tradier_tools.py", include_body=true)`

4.2. **Use Edit tool** to update docstring
   - old_string: 'Dates in YYYY-MM-DD format, sorted chronologically.'
   - new_string: 'Dates sorted chronologically (see Common Formats).'

4.3. **Verify change**
   - Use Serena to read function again
   - Confirm updated wording

**Validation:** Docstring updated, -7 tokens saved

**Token Impact:** -7 tokens

---

### Step 5: Optimize get_stock_price_history() in tradier_tools.py

**Current Docstring (Lines ~141-149):**
```python
"""Get historical stock price data (OHLC bars) from Tradier API.

Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
    start_date: Start date in YYYY-MM-DD format.
    end_date: End date in YYYY-MM-DD format.
    interval: Time interval - "daily", "weekly", or "monthly".
              See RULE #3 for selection logic.
```

**New Docstring:**
```python
"""Get historical stock price data (OHLC bars) from Tradier API.

Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
    start_date: Start date (see Common Formats).
    end_date: End date (see Common Formats).
    interval: Time interval - "daily", "weekly", or "monthly".
              See RULE #3 for selection logic.
```

**Sub-tasks:**

5.1. **Use Serena** to read current function
   - `mcp__serena__find_symbol(name_path="get_stock_price_history", relative_path="src/backend/tools/tradier_tools.py", include_body=true)`

5.2. **Use Edit tool** to update docstring (2 parameters)
   - First change:
     - old_string: 'start_date: Start date in YYYY-MM-DD format.'
     - new_string: 'start_date: Start date (see Common Formats).'
   - Second change:
     - old_string: 'end_date: End date in YYYY-MM-DD format.'
     - new_string: 'end_date: End date (see Common Formats).'

5.3. **Verify changes**
   - Use Serena to read function again
   - Confirm both parameters updated

**Validation:** Docstring updated (2 parameters), -10 tokens saved

**Token Impact:** -10 tokens

---

### Step 6: Optimize get_options_chain_both() in tradier_tools.py

**Current Docstring (Lines ~175-195, focusing on lines ~182 and ~188):**
```python
"""Get both Call and Put Options Chains (20 strikes each, centered around current price).

Use for comprehensive options analysis. Returns both chains in single API call.

Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
    current_price: Current price of underlying stock (must be > 0).
    expiration_date: Options expiration date in YYYY-MM-DD format.
                     Get from get_options_expiration_dates() first.

Returns:
    Formatted string with two markdown tables:
    - Call options chain (20 strikes, sorted descending)
    - Put options chain (20 strikes, sorted descending)
```

**New Docstring:**
```python
"""Get both Call and Put Options Chains (20 strikes each, centered around current price).

Use for comprehensive options analysis. Returns both chains in single API call.

Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
    current_price: Current price of underlying stock (must be > 0).
    expiration_date: Options expiration date (see Common Formats).
                     Get from get_options_expiration_dates() first.

Returns:
    String with two markdown tables:
    - Call options chain (20 strikes, sorted descending)
    - Put options chain (20 strikes, sorted descending)
```

**Sub-tasks:**

6.1. **Use Serena** to read current function
   - `mcp__serena__find_symbol(name_path="get_options_chain_both", relative_path="src/backend/tools/tradier_tools.py", include_body=true)`

6.2. **Use Edit tool** to update docstring (2 locations)
   - First change (parameter):
     - old_string: 'expiration_date: Options expiration date in YYYY-MM-DD format.'
     - new_string: 'expiration_date: Options expiration date (see Common Formats).'
   - Second change (returns):
     - old_string: 'Formatted string with two markdown tables:'
     - new_string: 'String with two markdown tables:'

6.3. **Verify changes**
   - Use Serena to read function again
   - Confirm both locations updated

**Validation:** Docstring updated (2 locations), -10 tokens saved

**Token Impact:** -10 tokens

---

### Step 7: Optimize get_ta_indicators() in polygon_tools.py

**Current Docstring (Lines ~114-120):**
```python
"""Get comprehensive technical analysis indicators (RSI, MACD, SMA, EMA) in a single call.

Consolidated tool replaces individual TA indicator tools with optimized batched API calls.

Indicators: RSI-14, MACD (12/26/9), SMA (5/10/20/50/200), EMA (5/10/20/50/200).

Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
    timespan: Aggregate window - "day", "minute", "hour", "week", "month" (default: "day").

Returns:
    Formatted markdown table with all 14 indicators (indicator, period, value, timestamp).
```

**New Docstring:**
```python
"""Get comprehensive technical analysis indicators (RSI, MACD, SMA, EMA) in a single call.

Consolidated tool replaces individual TA indicator tools with optimized batched API calls.

Indicators: RSI-14, MACD (12/26/9), SMA (5/10/20/50/200), EMA (5/10/20/50/200).

Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
    timespan: Aggregate window - "day", "minute", "hour", "week", "month" (default: "day").

Returns:
    Markdown table with all 14 indicators (indicator, period, value, timestamp).
```

**Sub-tasks:**

7.1. **Use Serena** to read current function
   - `mcp__serena__find_symbol(name_path="get_ta_indicators", relative_path="src/backend/tools/polygon_tools.py", include_body=true)`

7.2. **Use Edit tool** to update docstring
   - old_string: 'Formatted markdown table with all 14 indicators'
   - new_string: 'Markdown table with all 14 indicators'

7.3. **Verify change**
   - Use Serena to read function again
   - Confirm "Formatted" removed

**Validation:** Docstring updated, -3 tokens saved

**Token Impact:** -3 tokens

---

### Step 8: Optimize RULE #1 in agent_service.py

**Current Content (Line ~42):**
```python
RULE #1: STOCK QUOTES = USE get_stock_quote()

When to Use: User requests price, quote, snapshot, or ticker data

Tool: get_stock_quote(ticker: str)

Ticker Format:
- Single ticker: ticker='SPY'
- Multiple tickers: ticker='SPY,QQQ,IWM' (comma-separated, no spaces)
- Uses Tradier API (supports native multi-ticker in one call)
```

**New Content:**
```python
RULE #1: STOCK QUOTES = USE get_stock_quote()

When to Use: User requests price, quote, snapshot, or ticker data

Tool: get_stock_quote(ticker: str)

Ticker Format:
- Single ticker: ticker='SPY'
- Multiple tickers: ticker='SPY,QQQ,IWM' (see Common Formats)
- Uses Tradier API (supports native multi-ticker in one call)
```

**Sub-tasks:**

8.1. **Use Sequential-Thinking** to verify change context
   - This is first rule modification
   - Change should be minimal (only format reference)

8.2. **Use Edit tool** to update RULE #1
   - old_string: "Multiple tickers: ticker='SPY,QQQ,IWM' (comma-separated, no spaces)"
   - new_string: "Multiple tickers: ticker='SPY,QQQ,IWM' (see Common Formats)"

8.3. **Verify change**
   - Read agent_service.py
   - Confirm RULE #1 updated correctly

**Validation:** RULE #1 updated, -8 tokens saved

**Token Impact:** -8 tokens

---

### Step 9: Optimize RULE #3 in agent_service.py

**Current Content (Lines ~68-73):**
```python
Tool: get_stock_price_history(ticker, start_date, end_date, interval)

Parameters:
- ticker (str): Stock ticker symbol
- start_date (str): YYYY-MM-DD format
- end_date (str): YYYY-MM-DD format
- interval (str): "daily", "weekly", or "monthly"
```

**New Content:**
```python
Tool: get_stock_price_history(ticker, start_date, end_date, interval)

Parameters:
- ticker (str): Stock ticker symbol
- start_date (str): Date format (see Common Formats)
- end_date (str): Date format (see Common Formats)
- interval (str): "daily", "weekly", or "monthly"
```

**Sub-tasks:**

9.1. **Use Sequential-Thinking** to verify change scope
   - Two parameter descriptions changing
   - Only format references, not functionality

9.2. **Use Edit tool** to update RULE #3 (2 changes)
   - First change:
     - old_string: 'start_date (str): YYYY-MM-DD format'
     - new_string: 'start_date (str): Date format (see Common Formats)'
   - Second change:
     - old_string: 'end_date (str): YYYY-MM-DD format'
     - new_string: 'end_date (str): Date format (see Common Formats)'

9.3. **Verify changes**
   - Read agent_service.py
   - Confirm both parameters in RULE #3 updated

**Validation:** RULE #3 updated (2 parameters), -10 tokens saved

**Token Impact:** -10 tokens

---

### Step 10: Optimize RULE #5 in agent_service.py

**Current Content (Lines ~116-133):**
```python
RULE #5: OPTIONS TOOLS

TOOL 1: get_options_chain_both(ticker, current_price, expiration_date)
- Use for ALL options chain requests (calls, puts, or both)
- Returns both call and put chains in single response
- Requires current_price (use get_stock_quote if needed)
- Date format: YYYY-MM-DD

TOOL 2: get_options_expiration_dates(ticker)
- Use when user requests available expiration dates
- Returns: Array of dates in YYYY-MM-DD format

Shared Date Handling:
- "this Friday" → Calculate next Friday in YYYY-MM-DD
- "Oct 10" → Convert to YYYY-MM-DD (2025-10-10)
```

**New Content:**
```python
RULE #5: OPTIONS TOOLS

TOOL 1: get_options_chain_both(ticker, current_price, expiration_date)
- Use for ALL options chain requests (calls, puts, or both)
- Returns both call and put chains in single response
- Requires current_price (use get_stock_quote if needed)

TOOL 2: get_options_expiration_dates(ticker)
- Use when user requests available expiration dates
- Returns: Array of dates (see Common Formats)

Shared Date Handling:
- "this Friday" → Calculate next Friday (see Common Formats)
- "Oct 10" → Convert to date format (see Common Formats)
```

**Sub-tasks:**

10.1. **Use Sequential-Thinking** to verify change scope
   - Removing entire "Date format: YYYY-MM-DD" line
   - Updating 2 other date format references

10.2. **Use Edit tool** to update RULE #5 (3 changes)
   - First change (remove line):
     - old_string: Lines from "- Date format: YYYY-MM-DD\n\nTOOL 2:"
     - new_string: Lines without date format line: "\n\nTOOL 2:"
   - Second change:
     - old_string: 'Returns: Array of dates in YYYY-MM-DD format'
     - new_string: 'Returns: Array of dates (see Common Formats)'
   - Third change:
     - old_string: '"this Friday" → Calculate next Friday in YYYY-MM-DD'
     - new_string: '"this Friday" → Calculate next Friday (see Common Formats)'

10.3. **Verify changes**
   - Read agent_service.py
   - Confirm all 3 locations in RULE #5 updated

**Validation:** RULE #5 updated (removed 1 line, updated 2 references), -12 tokens saved

**Token Impact:** -12 tokens

---

### Step 11: (Optional) Optimize RULE #9 in agent_service.py

**Current Content (Line ~203):**
```python
Table Preservation (ALL TOOLS):
- When tool returns markdown table → Copy exactly as returned
- ❌ DO NOT reformat to bullet points, plain text, or any other format
```

**New Content:**
```python
Table Preservation (ALL TOOLS):
- When tool returns table → Copy exactly as returned
- ❌ DO NOT reformat to bullet points, plain text, or any other format
```

**Sub-tasks:**

11.1. **Use Sequential-Thinking** to evaluate if change is worthwhile
   - Only saves 2 tokens
   - "markdown table" is more specific than "table"
   - Decision: SKIP this optional optimization (keep specificity)

**Validation:** SKIPPED - Preserving "markdown table" for clarity

**Token Impact:** 0 tokens (skipped)

---

### Step 12: Verify All Optimizations Complete

**Objective:** Confirm all 11 modifications applied correctly

**Sub-tasks:**

12.1. **Use Sequential-Thinking** to review all changes
   - 1 addition (Common Formats section): +30 tokens
   - 6 tool docstring modifications: -38 tokens
   - 4 system rule modifications: -30 tokens (8+10+12+0)
   - Net savings: 68 tokens removed - 30 tokens added = 38 tokens net saved

12.2. **Read all 3 modified files**
   - agent_service.py: Verify Common Formats section + 4 rule changes
   - tradier_tools.py: Verify 4 tool docstring changes
   - polygon_tools.py: Verify 1 tool docstring change

12.3. **Document token impact**
   - Common Formats section: +30 tokens
   - Tool optimizations: -38 tokens (get_stock_quote -8, get_options_expiration_dates -7, get_stock_price_history -10, get_options_chain_both -10, get_ta_indicators -3)
   - Rule optimizations: -30 tokens (RULE #1 -8, RULE #3 -10, RULE #5 -12)
   - **Net total: -38 tokens saved (68 removed - 30 added)**

**Validation:** All 11 modifications complete, -38 tokens net saved

---

## Phase 4: Testing

### Step 13: Manual CLI Testing (5 Targeted Prompts)

**Objective:** Validate format handling with representative prompts covering all format types

**🔴 CRITICAL: These manual tests MUST pass before proceeding to regression testing 🔴**

**Sub-tasks:**

13.1. **Test Multi-Ticker Format**
   - Start CLI: `uv run main.py`
   - Prompt: "Get quotes for SPY, QQQ, IWM"
   - **Verify:**
     - ✅ Agent calls get_stock_quote(ticker='SPY,QQQ,IWM')
     - ✅ Agent understands comma-separated format
     - ✅ Returns 3 quote objects
     - ✅ No format errors

13.2. **Test Date Format (Parameters)**
   - Prompt: "Stock price performance from 2025-10-01 to 2025-10-28: SPY"
   - **Verify:**
     - ✅ Agent calls get_stock_price_history() with correct dates
     - ✅ Agent understands YYYY-MM-DD format
     - ✅ Returns OHLC bars for date range
     - ✅ No date parsing errors

13.3. **Test Date Format (Returns)**
   - Prompt: "Get options expiration dates for NVDA"
   - **Verify:**
     - ✅ Agent calls get_options_expiration_dates()
     - ✅ Returns dates in YYYY-MM-DD format
     - ✅ Dates sorted chronologically
     - ✅ Agent recognizes format in response

13.4. **Test Date Format (Options)**
   - Prompt: "Get both call and put options chains for SPY expiring 2025-11-01"
   - **Verify:**
     - ✅ Agent calls get_stock_quote() first (for current_price)
     - ✅ Agent calls get_options_chain_both() with expiration_date='2025-11-01'
     - ✅ Agent understands date parameter format
     - ✅ Returns both call and put tables
     - ✅ No date format errors

13.5. **Test Markdown Table Format**
   - Prompt: "Get TA for AAPL"
   - **Verify:**
     - ✅ Agent calls get_ta_indicators()
     - ✅ Returns markdown table with 14 indicators
     - ✅ Table formatting preserved (pipe separators)
     - ✅ No table formatting issues

**Validation:** All 5 manual tests pass, no format understanding issues

**🔴 IF ANY MANUAL TEST FAILS:**
1. Analyze why format understanding failed
2. Check if Common Formats section is visible to agent
3. Check if tool/rule references Common Formats correctly
4. Add back missing critical information if needed
5. Re-test until all pass
6. **DO NOT proceed to Step 14 until all manual tests pass**

---

### Step 14: Full Regression Testing - Phase 1 (Automated Response Generation)

**Objective:** Execute full 37-test suite to generate all responses

**Sub-tasks:**

14.1. **Execute regression test suite**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

14.2. **Monitor test execution**
   - Watch for completion messages
   - Check for any script errors
   - Verify session persistence
   - Note response times

14.3. **Verify test completion**
   - **Expected:** "37/37 COMPLETED" (all responses received)
   - **Check:** Test report file generated in test-reports/
   - **Note:** Average response time (should be ~10-11 seconds)

14.4. **Document Phase 1 results**
   - Test report path
   - Completion count (must be 37/37)
   - Average response time
   - Min/max response times
   - Any script errors or warnings

**Validation:** 37/37 tests completed, test report generated

**🔴 IF PHASE 1 FAILS (less than 37/37 completed):**
1. Check for script errors
2. Check for API connection issues
3. Check for import errors (Common Formats section syntax)
4. Verify all tools are importable
5. Fix issues and re-run
6. **DO NOT proceed to Step 15 until Phase 1 shows 37/37**

---

### Step 15: Full Regression Testing - Phase 2 (Manual Verification)

**Objective:** Manually verify EACH of the 37 test responses for correctness

**🔴 CRITICAL: This is NOT optional - YOU MUST manually review EVERY test response 🔴**

**Why Grep is Insufficient:**
- ❌ Misses duplicate/unnecessary tool calls
- ❌ Misses wrong tool selection
- ❌ Misses data inconsistencies
- ❌ Only catches explicit error messages, not logic errors

**Sub-tasks:**

15.1. **Use Read tool to read test report file**
   - `Read(file_path="test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log")`
   - Read in sections if file is large (use offset and limit)

15.2. **Apply 4-Point Verification Criteria to EACH test (1-37)**

For EACH test, verify ALL 4 criteria:

**Criterion 1: Does the response address the query?**
   - Is the agent's response relevant to the test prompt?
   - Is the response complete (not truncated)?
   - Does it answer what was asked?

**Criterion 2: Were the RIGHT tools called (no duplicate/unnecessary calls)?**
   - **Check conversation context**: If previous test retrieved data, agent should NOT call same tool again
   - Are the tools appropriate for the query?
   - Are there any redundant API calls?
   - Example FAIL: Test 10 calls `get_ta_indicators()`, Test 12 should NOT call it again

**Criterion 3: Is the data correct?**
   - Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
   - Data formatting matches expected format (OHLC, tables, dates in YYYY-MM-DD)
   - No hallucinated data or made-up values
   - No cross-ticker contamination
   - Options chains show Bid/Ask columns (NOT midpoint)

**Criterion 4: Are there any errors?**
   - No error messages in response
   - No "data unavailable" messages
   - No RuntimeWarnings
   - No API errors
   - No format parsing errors

15.3. **Document EACH test result in a table**

| Test # | Test Name | Status | Tool(s) Called | Issue (if failed) | Failure Type |
|--------|-----------|--------|----------------|-------------------|--------------|
| 1 | Market_Status | ✅ PASS | get_market_status_and_date_time | - | - |
| 2 | SPY_Price | ✅ PASS | get_stock_quote | - | - |
| 3 | Multi_Ticker_Prices | ✅ PASS | get_stock_quote | - | - |
| ... | ... | ... | ... | ... | ... |
| 37 | Multi_Options_Dates | ✅ PASS | 3× get_options_expiration_dates | - | - |

**Failure Types (if any):**
- Code Error: Syntax/runtime errors, import errors
- Logic Error (Duplicate Tool Call): Agent made unnecessary redundant API calls
- Logic Error (Wrong Tool): Agent called wrong tool for the query
- Data Error: Wrong data returned, cross-ticker contamination
- Response Error: Incomplete response, doesn't address query
- Format Error: Agent doesn't understand format references (NEW for this task)

15.4. **Answer Mandatory Checkpoint Questions**

**Question 1:** ✅ Did you READ all 37 test responses manually using the Read tool?
**Answer:** [YES/NO]

**Question 2:** ✅ Did you apply all 4 verification criteria to EACH test?
**Answer:** [YES/NO]

**Question 3:** ✅ How many tests PASSED all 4 criteria?
**Answer:** [X/37 PASSED]

**Question 4:** ✅ How many tests FAILED (any criterion)?
**Answer:** [X/37 FAILED]

**Question 5:** ✅ Did you document ALL failures with test #, issue, and failure type?
**Answer:** [YES/NO + Provide table of failures]

**Question 6:** ✅ Were there any format understanding issues (agent confused by Common Formats references)?
**Answer:** [YES/NO + Details if yes]

**Validation:** All 37 tests manually verified, results table created, checkpoint questions answered

**🔴 IF ANY TESTS FAIL:**
1. Analyze which modification caused the failure
2. If format error: Check if Common Formats section is clear enough
3. If tool selection error: Check if tool docstrings have enough context
4. If data error: Check if format specifications are being followed
5. Update tool/rule to restore essential information
6. Re-run manual CLI testing for affected format (Step 13.X)
7. Re-run full regression suite (Step 14)
8. Re-do Phase 2 manual verification (Step 15)
9. **DO NOT proceed to Phase 5 until 37/37 PASS**

---

### Step 16: Final Validation Before Commit

**Objective:** Confirm everything is ready for commit

**Sub-tasks:**

16.1. **Use Sequential-Thinking** to review entire implementation
   - All 11 modifications applied? (1 addition + 6 tools + 4 rules)
   - All manual tests passed? (5/5)
   - All 37 regression tests passed with manual verification? (37/37)
   - Token reduction achieved? (-38 tokens net)
   - No format understanding issues?

16.2. **Verify test evidence**
   - Test report file exists
   - 37/37 completion confirmed
   - Phase 2 manual verification table complete with all 37 tests
   - All checkpoint questions answered
   - No format-related failures

16.3. **Check git status**
   - Which files have been modified?
   - Are there any untracked files?
   - Is everything ready to stage?

16.4. **Final checklist:**
   - ✅ Common Formats section added to agent_service.py
   - ✅ 6 tool docstrings optimized (tradier_tools.py: 4, polygon_tools.py: 1)
   - ✅ 4 system rules optimized (RULE #1, #3, #5)
   - ✅ 5 manual CLI tests passed
   - ✅ 37 regression tests passed with Phase 2 verification
   - ✅ -38 tokens net saved
   - ✅ No functionality regression
   - ✅ No format understanding issues

**Validation:** All requirements met, ready for Phase 5

---

## Phase 5: Final Commit

### Step 17: Update Documentation

**Objective:** Update CLAUDE.md with task completion summary

**Sub-tasks:**

17.1. **Read current CLAUDE.md Last Completed Task Summary section**
   - Find the section marked with `<!-- LAST_COMPLETED_TASK_START -->`

17.2. **Draft completion summary**
   - Title: "[HOLISTIC_OPTIMIZATION] Cross-Component Token Optimization - Centralized Format Specifications"
   - Include all 11 modifications (1 addition + 6 tools + 4 rules)
   - Document token impact breakdown
   - Include test results (5/5 manual + 37/37 regression with Phase 2 verification)
   - List files modified
   - Include risk assessment (VERY LOW)
   - Performance impact details

17.3. **Use Edit tool to replace Last Completed Task Summary**
   - Replace content between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->`

**Validation:** CLAUDE.md updated with complete task summary

---

### Step 18: Atomic Git Commit Workflow

**Objective:** Create single atomic commit with ALL changes

**🔴 CRITICAL: Follow atomic commit workflow EXACTLY 🔴**

**Sub-tasks:**

18.1. **DO ALL WORK FIRST** (DO NOT stage anything yet)
   - ✅ Common Formats section added
   - ✅ All 6 tool docstrings optimized
   - ✅ All 4 system rules optimized
   - ✅ All tests run and passing (5 manual + 37 regression)
   - ✅ CLAUDE.md updated
   - ✅ research_task_plan.md complete
   - ✅ TODO_task_plan.md complete
   - ⚠️ **DO NOT RUN `git add` YET**

18.2. **VERIFY EVERYTHING IS COMPLETE**
```bash
git status  # Review ALL changed/new files
git diff    # Review ALL changes
```
   - Ensure ALL work is done
   - Ensure ALL files are present
   - Expected files to be modified:
     - src/backend/services/agent_service.py
     - src/backend/tools/tradier_tools.py
     - src/backend/tools/polygon_tools.py
     - CLAUDE.md
     - research_task_plan.md
     - TODO_task_plan.md

18.3. **STAGE EVERYTHING AT ONCE**
```bash
git add -A  # Stage ALL files in ONE command
```
   - ⚠️ This is the FIRST time you run `git add`
   - ⚠️ Stage ALL related files together

18.4. **VERIFY STAGING IMMEDIATELY**
```bash
git status  # Verify ALL files staged, NOTHING unstaged
```
   - If anything is missing: `git add [missing-file]`
   - Confirm all 6 files staged

18.5. **COMMIT IMMEDIATELY** (within 60 seconds of staging)
```bash
git commit -m "$(cat <<'EOF'
[HOLISTIC_OPTIMIZATION] Cross-Component Token Optimization - Centralized Format Specifications

Phase 1-4 Complete: Research, Planning, Implementation, and Full Testing

Major Changes:
- Created centralized "COMMON FORMATS" section in agent instructions
- Optimized 6 tool docstrings to reference Common Formats (removed duplication)
- Optimized 4 system instruction rules to reference Common Formats
- Eliminated cross-component duplication between tools and instructions

Token Optimization Breakdown:
- Common Formats section added: +30 tokens
- Tool docstring optimizations: -38 tokens
  * get_stock_quote: -8 tokens (comma-separated format → reference)
  * get_options_expiration_dates: -7 tokens (YYYY-MM-DD → reference)
  * get_stock_price_history: -10 tokens (2 date parameters → references)
  * get_options_chain_both: -10 tokens (date param + "Formatted" removal)
  * get_ta_indicators: -3 tokens ("Formatted" removal)
- System rule optimizations: -30 tokens
  * RULE #1: -8 tokens (comma-separated format → reference)
  * RULE #3: -10 tokens (2 date parameters → references)
  * RULE #5: -12 tokens (removed format line + 2 references)

Net Token Savings:
- Duplicates removed: 68 tokens
- New content added: 30 tokens
- Net savings: 38 tokens (~1.5% reduction)

Cross-Component Duplication Eliminated:
- "YYYY-MM-DD format" appeared in 7 locations → Now 1 centralized definition
- "comma-separated, no spaces" appeared in 3 locations → Now 1 centralized definition
- "Formatted" prefix appeared in 3 locations → Removed (redundant with table format)

Testing Results:
- Manual CLI Testing: 5/5 targeted format prompts PASSED
  * Multi-ticker format test: PASSED
  * Date parameter format test: PASSED
  * Date return format test: PASSED
  * Options date format test: PASSED
  * Markdown table format test: PASSED
- Phase 1 (Automated): 37/37 test responses COMPLETED
- Phase 2 (Manual Verification): 37/37 tests PASSED with 4-point criteria
- Zero format understanding issues detected
- Zero functionality regressions
- All tools correctly selected by agent
- All responses correctly formatted

Files Modified:
- src/backend/services/agent_service.py: Added Common Formats section + 4 rule optimizations
- src/backend/tools/tradier_tools.py: 4 tool docstring optimizations
- src/backend/tools/polygon_tools.py: 1 tool docstring optimization
- CLAUDE.md: Updated with completion summary
- research_task_plan.md: Complete cross-component duplication analysis
- TODO_task_plan.md: Detailed implementation checklist

Documentation:
- research_task_plan.md: Duplication matrix analysis and consolidation strategy
- TODO_task_plan.md: Granular 18-step implementation plan
- Test report: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log

Risk Assessment: VERY LOW
- No functionality removed (format consolidation only)
- All format information still present, just centralized
- All 37 regression tests pass with manual verification
- All tools maintain correct behavior
- Agent correctly understands Common Formats references
- Token efficiency improved without regression

Performance Impact:
- Token reduction: 38 tokens net saved (~1.5% reduction)
- Cost savings: Small but measurable reduction per API call
- Maintainability: Single source of truth for formats (easier to update)
- Clarity: Centralized format specifications improve discoverability
- Scalability: Pattern can be applied to future cross-component optimizations

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

18.6. **PUSH IMMEDIATELY**
```bash
git push
```

**Validation:** Atomic commit created and pushed to remote

---

## Success Criteria

### Quantitative Metrics

- ✅ **Token Reduction:** -38 tokens net saved (68 removed - 30 added)
- ✅ **Test Pass Rate:** 37/37 (100%) with Phase 2 manual verification
- ✅ **Manual Tests:** 5/5 (100%) format tests passed
- ✅ **Modifications:** 11/11 (100%) complete (1 addition + 6 tools + 4 rules)

### Qualitative Metrics

- ✅ **Improved Maintainability:** Single source of truth for format specifications
- ✅ **Better Discoverability:** Centralized Common Formats section
- ✅ **No Regression:** All functionality maintained
- ✅ **Scalable Pattern:** Can apply to future cross-component optimizations

---

## Risk Mitigation

### If Tests Fail

**Symptom:** Agent doesn't understand Common Formats references
**Solution:**
1. Review Common Formats section - is it clear and prominent?
2. Check if section appears BEFORE any references to it
3. Consider adding more examples to Common Formats section
4. Ensure emoji prefix makes section visually distinct

**Symptom:** Format parsing errors in responses
**Solution:**
1. Review which format is causing issues
2. Check if Common Formats definition is complete
3. Add back explicit format in tool/rule if Common Formats reference is unclear
4. Re-test affected format

**Symptom:** Tool selection errors
**Solution:**
1. Review tool docstrings - is purpose still clear?
2. Check if removing format details removed critical context
3. Add back essential tool selection context if needed

### Rollback Plan

If optimization causes test failures that can't be resolved:
1. Use git to restore previous version
2. Analyze which format references were unclear
3. Create more explicit Common Formats section
4. Re-test and iterate
5. Consider partial rollback (keep some explicit formats in tools)

---

## Timeline Estimate

- **Step 1-12 (Implementation):** 45-60 minutes (11 modifications across 3 files)
- **Step 13 (Manual CLI Testing):** 15-20 minutes (5 format tests)
- **Step 14-15 (Regression Testing):** 25-35 minutes (37 tests + manual verification)
- **Step 16 (Final Validation):** 5 minutes
- **Step 17-18 (Documentation & Commit):** 10-15 minutes
- **Total:** ~100-135 minutes

---

## Tools and Commands Reference

### Serena Tools

```python
# Read symbol
mcp__serena__find_symbol(name_path="get_stock_quote", relative_path="src/backend/tools/tradier_tools.py", include_body=true)

# Replace symbol body (NOT used for docstring-only changes)
mcp__serena__replace_symbol_body(name_path="get_stock_quote", relative_path="src/backend/tools/tradier_tools.py", body="[NEW BODY]")
```

### Sequential-Thinking

```python
# Start every phase with sequential thinking
mcp__sequential-thinking__sequentialthinking(
    thought="Analyze current step and plan approach...",
    nextThoughtNeeded=true,
    thoughtNumber=1,
    totalThoughts=5
)
```

### Standard Edit Tool

```python
# Use for docstring and instruction modifications
Edit(file_path="src/backend/tools/tradier_tools.py",
     old_string="ticker: Stock ticker symbol(s). Single: \"AAPL\" or multiple: \"AAPL,TSLA,NVDA\" (comma-separated, no spaces).",
     new_string="ticker: Stock ticker symbol(s). Single: \"AAPL\" or multiple: \"AAPL,TSLA,NVDA\" (see Common Formats).")
```

### Testing Commands

```bash
# Manual CLI testing
uv run main.py

# Regression testing
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

### Git Commands

```bash
# Check status
git status
git diff

# Stage all
git add -A

# Commit
git commit -m "message"

# Push
git push
```

---

## Completion Checklist

### Phase 3: Implementation
- [ ] Step 1: Pre-implementation verification complete
- [ ] Step 2: Common Formats section added to agent_service.py (+30 tokens)
- [ ] Step 3: get_stock_quote() optimized (-8 tokens)
- [ ] Step 4: get_options_expiration_dates() optimized (-7 tokens)
- [ ] Step 5: get_stock_price_history() optimized (-10 tokens)
- [ ] Step 6: get_options_chain_both() optimized (-10 tokens)
- [ ] Step 7: get_ta_indicators() optimized (-3 tokens)
- [ ] Step 8: RULE #1 optimized (-8 tokens)
- [ ] Step 9: RULE #3 optimized (-10 tokens)
- [ ] Step 10: RULE #5 optimized (-12 tokens)
- [ ] Step 11: RULE #9 optimization SKIPPED (0 tokens)
- [ ] Step 12: All optimizations verified, token counts confirmed (-38 net)

### Phase 4: Testing
- [ ] Step 13.1: Multi-ticker format test - PASS
- [ ] Step 13.2: Date parameter format test - PASS
- [ ] Step 13.3: Date return format test - PASS
- [ ] Step 13.4: Options date format test - PASS
- [ ] Step 13.5: Markdown table format test - PASS
- [ ] Step 14: Phase 1 regression testing - 37/37 COMPLETED
- [ ] Step 15: Phase 2 manual verification - 37/37 PASS with 4-point criteria
- [ ] Step 16: Final validation - all requirements met

### Phase 5: Final Commit
- [ ] Step 17: CLAUDE.md updated with completion summary
- [ ] Step 18.1: All work complete, no staging yet
- [ ] Step 18.2: Git status and diff reviewed
- [ ] Step 18.3: All files staged at once (git add -A)
- [ ] Step 18.4: Staging verified (git status)
- [ ] Step 18.5: Atomic commit created
- [ ] Step 18.6: Changes pushed to remote

---

## Next Steps

**Immediate Action:** Begin Phase 3 - Implementation (Step 1)

**Use Sequential-Thinking** to start the implementation:
- Review research findings from Phase 1
- Plan approach for first modification (Common Formats section)
- Prepare for systematic execution of all 11 modifications

**Remember:**
- Use Serena tools for reading code symbols
- Use Edit tool for docstring and instruction modifications
- Use Sequential-Thinking for all planning and analysis
- Follow atomic commit workflow for final commit
