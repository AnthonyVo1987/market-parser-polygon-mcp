# TODO: Tradier Historical Pricing API Migration Implementation Plan

**Status:** Planning Complete - Ready for Implementation
**Created:** October 10, 2025
**Task:** Migrate Polygon OHLC tools to single Tradier `get_stock_price_history` tool with multi-interval support

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE ENFORCEMENT

**YOU MUST use tools AS OFTEN AS NEEDED throughout the ENTIRE implementation:**

1. **Sequential-Thinking** - Use for:
   - Complex problem analysis
   - Implementation strategy decisions
   - Error diagnosis and debugging
   - Edge case handling
   - Max 8 thoughts per use, can invoke multiple times

2. **Serena Tools** - Use for:
   - Code analysis (find_symbol, get_symbols_overview)
   - Symbol manipulation (replace_symbol_body, insert_after_symbol)
   - Pattern search with context (search_for_pattern)
   - Finding references (find_referencing_symbols)
   - Memory management (write_memory, read_memory)

3. **Standard Tools** - Use for:
   - Simple file reads (Read)
   - Simple file writes (Write)
   - Simple file edits (Edit)
   - Bash commands (Bash)

**VIOLATION PENALTIES:**
- Using tools only once = FAILING
- Following rigid order instead of using as needed = FAILING
- Not using tools throughout entire process = FAILING
- Using wrong tool for operation (e.g., Standard for batch operations) = FAILING

**SUCCESS CRITERIA:**
- Tools used MULTIPLE times throughout task
- Tools used in DIFFERENT orders based on need
- CONTINUOUS tool usage from start to finish
- CORRECT tool selection based on operation type

---

## Phase 1: Research ✅ COMPLETE

**Status:** ✅ Complete
**Findings:**
- Tradier `/v1/markets/history` endpoint supports daily, weekly, monthly intervals
- Single tool can replace 3 Polygon OHLC tools
- Response structure: `{"history": {"day": [...]}}`  (always "day" key regardless of interval)
- Date format: YYYY-MM-DD (ISO 8601)
- Fields: date, open, high, low, close, volume (standard 6 fields)
- New capabilities: weekly and monthly intervals not available in Polygon tools
- Tool consolidation: 3 → 1 tool (net reduction of 2 tools, total: 11 tools)

**Current Polygon Tools to be Removed:**
1. `get_OHLC_bars_custom_date_range` - Custom date range, daily bars
2. `get_OHLC_bars_specific_date` - Specific single date
3. `get_OHLC_bars_previous_close` - Previous close bar

**New Tradier Tool to be Created:**
1. `get_stock_price_history` - All date ranges, all intervals (daily/weekly/monthly)

---

## Phase 2: Planning ✅ COMPLETE

**Status:** ✅ Complete
**Output:** This implementation plan

---

## Phase 3: Implementation 🔴 START HERE

### 3.1: Create New Tradier Tool

**Task:** Implement `get_stock_price_history` in tradier_tools.py

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan tool implementation strategy
- [ ] Use **Serena get_symbols_overview** to analyze tradier_tools.py structure
- [ ] Use **Serena find_symbol** to locate existing tools for reference
- [ ] Use **Serena insert_after_symbol** to add new tool
- [ ] Use **Read** to verify implementation

**Steps:**
1. [ ] **Sequential-Thinking**: Analyze implementation strategy
   - Tool function signature design
   - Parameter validation approach
   - Interval selection logic
   - Date format handling
   - Response structure formatting
   - Error handling strategy

2. [ ] **Analyze Current tradier_tools.py:**
   - [ ] Use Serena get_symbols_overview with `relative_path="src/backend/tools/tradier_tools.py"`
   - [ ] Identify where to insert new function
   - [ ] Review existing helper functions for pattern consistency

3. [ ] **Design New Tool Function:**
   ```python
   @function_tool
   async def get_stock_price_history(
       ticker: str,
       start_date: str,
       end_date: str,
       interval: str = "daily"
   ) -> str:
       """Get historical stock price data from Tradier API.

       Use this tool when the user requests historical stock prices, OHLC bars,
       or performance data for a specific time period.

       Args:
           ticker: Stock ticker symbol (e.g., "SPY", "AAPL", "NVDA")
           start_date: Start date in YYYY-MM-DD format (e.g., "2025-01-01")
           end_date: End date in YYYY-MM-DD format (e.g., "2025-01-10")
           interval: Time interval - "daily", "weekly", or "monthly" (default: "daily")

       Returns:
           JSON string with historical OHLC data:
           {
               "ticker": "SPY",
               "interval": "daily",
               "start_date": "2025-01-01",
               "end_date": "2025-01-10",
               "bars": [
                   {
                       "date": "2025-01-02",
                       "open": 589.39,
                       "high": 591.13,
                       "low": 580.5,
                       "close": 584.64,
                       "volume": 50203975
                   },
                   ...
               ],
               "count": 6,
               "source": "Tradier"
           }

       Examples:
           - "Stock price performance last 5 trading days: SPY"
             → interval="daily", calculate last 5 trading days
           - "Stock price performance last 2 weeks: NVDA"
             → interval="weekly", calculate last 2 weeks
           - "Stock price performance last month: AAPL"
             → interval="monthly", calculate last month
       """
       try:
           # Validate ticker
           if not ticker or not ticker.strip():
               return json.dumps({
                   "error": "Invalid ticker",
                   "message": "Ticker symbol cannot be empty",
                   "ticker": ticker
               })

           ticker = ticker.strip().upper()

           # Validate interval
           valid_intervals = ["daily", "weekly", "monthly"]
           if interval not in valid_intervals:
               return json.dumps({
                   "error": "Invalid interval",
                   "message": f"Interval must be one of: {', '.join(valid_intervals)}",
                   "interval": interval
               })

           # Validate date format (basic check)
           if not start_date or not end_date:
               return json.dumps({
                   "error": "Invalid dates",
                   "message": "Start date and end date are required (YYYY-MM-DD format)",
                   "start_date": start_date,
                   "end_date": end_date
               })

           # Get API key
           api_key = os.getenv("TRADIER_API_KEY")
           if not api_key:
               return json.dumps({
                   "error": "Configuration error",
                   "message": "TRADIER_API_KEY not configured in environment",
                   "ticker": ticker
               })

           # Build request
           url = "https://api.tradier.com/v1/markets/history"
           headers = {
               "Accept": "application/json",
               "Authorization": f"Bearer {api_key}"
           }
           params = {
               "symbol": ticker,
               "interval": interval,
               "start": start_date,
               "end": end_date
           }

           # Make API request
           response = requests.get(url, headers=headers, params=params, timeout=10)
           response.raise_for_status()

           data = response.json()
           history_data = data.get("history", {})
           bars_data = history_data.get("day", [])

           # Check if API returned data
           if not bars_data:
               return json.dumps({
                   "error": "No data",
                   "message": f"No historical data available for {ticker} from {start_date} to {end_date}",
                   "ticker": ticker,
                   "interval": interval
               })

           # Format response
           formatted_bars = []
           for bar in bars_data:
               formatted_bars.append(_format_tradier_history_bar(bar))

           return json.dumps({
               "ticker": ticker,
               "interval": interval,
               "start_date": start_date,
               "end_date": end_date,
               "bars": formatted_bars,
               "count": len(formatted_bars),
               "source": "Tradier"
           }, indent=2)

       except requests.exceptions.Timeout:
           return json.dumps({
               "error": "Timeout",
               "message": f"Request timed out while fetching history for {ticker}",
               "ticker": ticker
           })
       except requests.exceptions.RequestException as e:
           return json.dumps({
               "error": "API request failed",
               "message": f"Tradier API request failed: {str(e)}",
               "ticker": ticker
           })
       except Exception as e:
           return json.dumps({
               "error": "Unexpected error",
               "message": f"Failed to retrieve history for {ticker}: {str(e)}",
               "ticker": ticker
           })


   def _format_tradier_history_bar(bar: dict) -> dict:
       """Format Tradier history bar to consistent structure.

       Args:
           bar: Raw bar data from Tradier API

       Returns:
           Formatted bar dictionary with rounded values
       """
       return {
           "date": bar.get("date", ""),
           "open": round(bar.get("open", 0.0), 2),
           "high": round(bar.get("high", 0.0), 2),
           "low": round(bar.get("low", 0.0), 2),
           "close": round(bar.get("close", 0.0), 2),
           "volume": bar.get("volume", 0)
       }
   ```

4. [ ] **Insert New Function:**
   - [ ] Use Serena insert_after_symbol to add `get_stock_price_history` after `get_market_status_and_date_time`
   - [ ] Use Serena insert_after_symbol to add `_format_tradier_history_bar` helper after `get_stock_price_history`

5. [ ] **Verify Implementation:**
   - [ ] Use Read to review tradier_tools.py
   - [ ] Verify function signature correct
   - [ ] Verify parameter validation comprehensive
   - [ ] Verify error handling complete
   - [ ] Verify response format consistent

**Success Criteria:**
- [ ] `get_stock_price_history` function added to tradier_tools.py
- [ ] Helper function `_format_tradier_history_bar` added
- [ ] All parameters validated (ticker, start_date, end_date, interval)
- [ ] Error handling comprehensive (timeout, network, invalid ticker, invalid dates)
- [ ] Response format includes ticker, interval, dates, bars array, count, source
- [ ] Timeout set to 10 seconds

---

### 3.2: Remove Old Polygon OHLC Tools

**Task:** Delete 3 Polygon OHLC tools from polygon_tools.py

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan removal strategy and verify no breaking changes
- [ ] Use **Serena find_symbol** to locate each function
- [ ] Use **Serena find_referencing_symbols** to check for references
- [ ] Use **Edit** to delete function definitions
- [ ] Use **Read** to verify deletions

**Steps:**
1. [ ] **Sequential-Thinking**: Plan removal strategy
   - Identify exact function names and locations
   - Check for any references in other code
   - Plan for clean deletion without breaking remaining tools
   - Verify imports still needed

2. [ ] **Locate Functions to Delete:**
   - [ ] Use Serena find_symbol with `name_path="/get_OHLC_bars_custom_date_range"`, `relative_path="src/backend/tools/polygon_tools.py"`, `include_body=True`
   - [ ] Use Serena find_symbol with `name_path="/get_OHLC_bars_specific_date"`, `relative_path="src/backend/tools/polygon_tools.py"`, `include_body=True`
   - [ ] Use Serena find_symbol with `name_path="/get_OHLC_bars_previous_close"`, `relative_path="src/backend/tools/polygon_tools.py"`, `include_body=True`
   - [ ] Note line ranges for each function

3. [ ] **Check for References:**
   - [ ] Use Serena find_referencing_symbols for `get_OHLC_bars_custom_date_range`
   - [ ] Use Serena find_referencing_symbols for `get_OHLC_bars_specific_date`
   - [ ] Use Serena find_referencing_symbols for `get_OHLC_bars_previous_close`
   - [ ] Verify only agent_service.py references exist (will be updated)

4. [ ] **Delete Functions:**
   - [ ] Use Edit to delete `get_OHLC_bars_custom_date_range` function (including @function_tool decorator and docstring)
   - [ ] Use Edit to delete `get_OHLC_bars_specific_date` function
   - [ ] Use Edit to delete `get_OHLC_bars_previous_close` function

5. [ ] **Verify Deletions:**
   - [ ] Use Read to review polygon_tools.py
   - [ ] Verify 3 functions deleted
   - [ ] Verify remaining Polygon tools intact (TA indicators, options chains)
   - [ ] Verify no orphaned imports or helper functions

**Success Criteria:**
- [ ] `get_OHLC_bars_custom_date_range` deleted
- [ ] `get_OHLC_bars_specific_date` deleted
- [ ] `get_OHLC_bars_previous_close` deleted
- [ ] Remaining Polygon tools still present and intact
- [ ] File structure clean (no orphaned code)

---

### 3.3: Update Tool Exports

**Task:** Update `__init__.py` to export new tool and remove old tools

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan export updates
- [ ] Use **Read** to check current exports
- [ ] Use **Edit** to update exports
- [ ] Use **Read** to verify changes

**Steps:**
1. [ ] **Sequential-Thinking**: Plan export updates
   - Add new Tradier tool export
   - Remove 3 Polygon tool exports
   - Verify tool count correct

2. [ ] **Read Current Exports:**
   - [ ] Use Read to view `src/backend/tools/__init__.py`
   - [ ] Identify current imports from tradier_tools
   - [ ] Identify current imports from polygon_tools

3. [ ] **Update Exports:**
   - [ ] Use Edit to add `get_stock_price_history` to tradier_tools imports
   - [ ] Use Edit to remove `get_OHLC_bars_custom_date_range` from polygon_tools imports
   - [ ] Use Edit to remove `get_OHLC_bars_specific_date` from polygon_tools imports
   - [ ] Use Edit to remove `get_OHLC_bars_previous_close` from polygon_tools imports
   - [ ] Use Edit to update `__all__` list (add new, remove 3 old)

4. [ ] **Verify Exports:**
   - [ ] Use Read to review __init__.py
   - [ ] Verify `get_stock_price_history` exported
   - [ ] Verify 3 old tools not exported
   - [ ] Verify other tools still exported correctly

**Success Criteria:**
- [ ] `get_stock_price_history` added to exports
- [ ] 3 old OHLC tools removed from exports
- [ ] `__all__` list updated correctly
- [ ] No export errors

---

### 3.4: Update Agent Instructions

**Task:** Update agent_service.py with new RULE for historical data and remove old rules

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan instruction changes
- [ ] Use **Serena search_for_pattern** to locate relevant rules
- [ ] Use **Edit** to update agent instructions
- [ ] Use **Read** to verify changes

**Steps:**
1. [ ] **Sequential-Thinking**: Plan instruction updates
   - Design new RULE for historical data with interval selection logic
   - Identify all locations referencing old OHLC tools
   - Plan date calculation examples
   - Plan interval selection guidelines

2. [ ] **Locate Current Instructions:**
   - [ ] Use Serena search_for_pattern to find OHLC bar references
   - [ ] Use Serena search_for_pattern to find "get_OHLC_bars" mentions
   - [ ] Identify RULE section for OHLC bars
   - [ ] Identify examples section with OHLC examples

3. [ ] **Design New RULE:**
   ```
   RULE #X: HISTORICAL STOCK PRICES = ALWAYS USE get_stock_price_history()
   - If the request asks for historical stock prices, OHLC bars, price performance over time, or daily/weekly/monthly data
   - Examples: "Last 5 trading days", "Last 2 weeks performance", "Last month prices", "Daily bars from X to Y"
   - 📊 Uses Tradier API for historical pricing data
   - ✅ Supports multiple intervals: daily, weekly, monthly
   - ✅ Parameters: ticker (str), start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), interval (daily/weekly/monthly)
   - ✅ Returns: Array of OHLC bars with date, open, high, low, close, volume

   **INTERVAL SELECTION LOGIC:**
   - **Daily interval** - Use when:
     - Request mentions "days", "trading days", "daily bars"
     - Time period is less than 2 weeks
     - Daily precision is needed
     - Examples: "last 5 trading days", "daily bars last week"

   - **Weekly interval** - Use when:
     - Request mentions "weeks", "weekly bars", "weekly performance"
     - Time period is 2 weeks to 3 months
     - Weekly summary is appropriate
     - Examples: "last 2 weeks", "weekly performance last month"

   - **Monthly interval** - Use when:
     - Request mentions "month", "monthly bars", "monthly performance"
     - Time period is greater than 3 months
     - Monthly summary is appropriate
     - Examples: "last month", "monthly bars last 6 months"

   **DATE CALCULATION EXAMPLES:**
   - "Last 5 trading days" → interval="daily", start_date=(today - 7 days), end_date=today
   - "Last 2 weeks" → interval="weekly", start_date=(today - 14 days), end_date=today
   - "Last month" → interval="monthly", start_date=(today - 30 days), end_date=today
   - "From 2025-01-01 to 2025-01-10" → interval="daily", start_date="2025-01-01", end_date="2025-01-10"

   **COMMON MISTAKES TO AVOID:**
   - ❌ Using old get_OHLC_bars_* tools (REMOVED - use get_stock_price_history)
   - ❌ Not calculating date range for relative queries ("last 5 days")
   - ❌ Wrong interval for time period (daily for 6 months)
   - ❌ Wrong date format (must be YYYY-MM-DD)
   ```

4. [ ] **Remove Old RULE:**
   - [ ] Locate RULE section for OHLC bars (if exists as dedicated rule)
   - [ ] Use Edit to delete old RULE
   - [ ] Or use Edit to replace old RULE with new RULE

5. [ ] **Update Tool Count Comment:**
   - [ ] Locate tools list comment in agent_service.py
   - [ ] Update: "13 tools" → "11 tools"
   - [ ] Update: "2 Tradier + 10 Polygon" → "3 Tradier + 8 Polygon" (or similar)

6. [ ] **Update Examples Section:**
   - [ ] Find examples mentioning OHLC bars
   - [ ] Update: "Daily bars last 2 weeks" → "Stock price performance last 5 trading days"
   - [ ] Add: "Stock price performance last 2 weeks" (weekly example)
   - [ ] Add: "Stock price performance last month" (monthly example)

7. [ ] **Update Decision Tree (if exists):**
   - [ ] Find decision tree section
   - [ ] Update historical data query handling
   - [ ] Add interval selection logic

8. [ ] **Verify Changes:**
   - [ ] Use Read to review agent_service.py
   - [ ] Verify new RULE added
   - [ ] Verify old RULE removed
   - [ ] Verify examples updated
   - [ ] Verify tool count correct

**Success Criteria:**
- [ ] New RULE for get_stock_price_history added with comprehensive interval selection logic
- [ ] Old RULE for OHLC bars removed
- [ ] Tool count updated (13 → 11)
- [ ] Examples updated (3 new examples per ticker)
- [ ] No references to old get_OHLC_bars_* tools
- [ ] Date calculation examples clear
- [ ] Interval selection guidelines comprehensive

---

### 3.5: Update Agent Tools List

**Task:** Update tools list in agent_service.py to include new tool and remove old tools

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to locate tools list
- [ ] Use **Serena search_for_pattern** to find tools array
- [ ] Use **Edit** to update tools list
- [ ] Use **Read** to verify changes

**Steps:**
1. [ ] **Sequential-Thinking**: Plan tools list update
   - Locate tools array in create_agent() function
   - Identify correct position for new tool
   - Plan for clean removal of 3 old tools

2. [ ] **Locate Tools List:**
   - [ ] Use Serena search_for_pattern with `substring_pattern="tools=["` or `substring_pattern="get_stock_quote"` in agent_service.py
   - [ ] Identify tools list array
   - [ ] Note current tool order

3. [ ] **Update Tools List:**
   - [ ] Use Edit to add `get_stock_price_history` to tools array (after get_market_status_and_date_time)
   - [ ] Use Edit to remove `get_OHLC_bars_custom_date_range` from tools array
   - [ ] Use Edit to remove `get_OHLC_bars_specific_date` from tools array
   - [ ] Use Edit to remove `get_OHLC_bars_previous_close` from tools array

4. [ ] **Update Import Statement:**
   - [ ] Locate import statement for polygon_tools in agent_service.py
   - [ ] Use Edit to add `get_stock_price_history` to tradier_tools imports
   - [ ] Use Edit to remove 3 old OHLC tools from polygon_tools imports

5. [ ] **Verify Changes:**
   - [ ] Use Read to review agent_service.py
   - [ ] Verify new tool in tools array
   - [ ] Verify 3 old tools removed
   - [ ] Verify imports correct
   - [ ] Verify no syntax errors

**Success Criteria:**
- [ ] `get_stock_price_history` added to tools array
- [ ] 3 old OHLC tools removed from tools array
- [ ] Import statements updated correctly
- [ ] Tools array has correct tool count (11 tools total)
- [ ] No syntax errors

---

## Phase 4: Testing 🔴 MANDATORY - DO NOT SKIP

### 4.1: Quick Manual Testing

**Task:** Test new tool with CLI for basic functionality

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan testing strategy
- [ ] Use **Bash** to run CLI tests
- [ ] Use **Read** to review test output

**Steps:**
1. [ ] **Sequential-Thinking**: Plan testing approach
   - Test daily interval with 5 days
   - Test weekly interval
   - Test monthly interval
   - Verify response format
   - Check error handling

2. [ ] **Test Daily Interval (5 Trading Days):**
   - [ ] Run: `uv run src/backend/main.py` with prompt "Stock price performance the last 5 trading days: SPY"
   - [ ] Verify response has ~5 bars (accounting for weekends)
   - [ ] Verify interval="daily"
   - [ ] Verify each bar has date, open, high, low, close, volume
   - [ ] Verify source="Tradier"
   - [ ] Check response time (<10 seconds)

3. [ ] **Test Weekly Interval:**
   - [ ] Run: `uv run src/backend/main.py` with prompt "Stock price performance the last 2 weeks: NVDA"
   - [ ] Verify response has 2 weekly bars
   - [ ] Verify interval="weekly"
   - [ ] Verify each bar aggregates weekly data
   - [ ] Check response time

4. [ ] **Test Monthly Interval:**
   - [ ] Run: `uv run src/backend/main.py` with prompt "Stock price performance the last month: AAPL"
   - [ ] Verify response has monthly bar data
   - [ ] Verify interval="monthly"
   - [ ] Verify aggregation correct
   - [ ] Check response time

5. [ ] **Test All Required Tickers:**
   - [ ] SPY: "Stock price performance the last 5 trading days: SPY"
   - [ ] NVDA: "Stock price performance the last 5 trading days: NVDA"

6. [ ] **Sequential-Thinking**: Analyze test results
   - Verify all responses match expected format
   - Verify Tradier API being called
   - Identify any issues
   - Plan fixes if needed

**Success Criteria:**
- [ ] Daily interval test returns ~5 bars
- [ ] Weekly interval test returns 2 weekly bars
- [ ] Monthly interval test returns monthly data
- [ ] All responses have correct format
- [ ] All responses use source="Tradier"
- [ ] No errors or exceptions
- [ ] Response times reasonable (<10 seconds)

---

### 4.2: Update Test Suite

**Task:** Update test_cli_regression.sh with new test cases

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan test updates
- [ ] Use **Read** to review current test suite
- [ ] Use **Edit** to update test cases
- [ ] Use **Bash** to verify test syntax

**Steps:**
1. [ ] **Sequential-Thinking**: Plan test suite updates
   - Locate old OHLC test cases
   - Design 3 new test cases (daily, weekly, monthly)
   - Ensure test names consistent
   - Plan test order

2. [ ] **Read Current Test Suite:**
   - [ ] Use Read to view test_cli_regression.sh
   - [ ] Find test cases with "Daily Stock Price bars Analysis from the last 2 trading weeks"
   - [ ] Note line numbers for SPY and NVDA test cases

3. [ ] **Update SPY Test Sequence:**
   - [ ] Locate: `echo "📋 Test 7: Daily Stock Price bars Analysis from the last 2 trading weeks: \$SPY"`
   - [ ] Replace with:
     ```bash
     echo "📋 Test 7: Stock Price Performance the last 5 Trading Days: \$SPY"
     echo "Stock Price Performance the last 5 Trading Days: \$SPY" | timeout 60 uv run src/backend/main.py 2>&1
     ```
   - [ ] Add new Test 8 (after Test 7):
     ```bash
     echo "📋 Test 8: Stock Price Performance the last 2 Weeks: \$SPY"
     echo "Stock Price Performance the last 2 Weeks: \$SPY" | timeout 60 uv run src/backend/main.py 2>&1
     ```
   - [ ] Add new Test 9 (after Test 8):
     ```bash
     echo "📋 Test 9: Stock Price Performance the last month: \$SPY"
     echo "Stock Price Performance the last month: \$SPY" | timeout 60 uv run src/backend/main.py 2>&1
     ```
   - [ ] Renumber subsequent tests (old Test 8 → Test 10, etc.)

4. [ ] **Update NVDA Test Sequence:**
   - [ ] Locate: `echo "📋 Test 24: Daily Stock Price bars Analysis from the last 2 trading weeks: \$NVDA"`
   - [ ] Replace with similar 3-test pattern:
     ```bash
     echo "📋 Test 25: Stock Price Performance the last 5 Trading Days: \$NVDA"
     echo "Stock Price Performance the last 5 Trading Days: \$NVDA" | timeout 60 uv run src/backend/main.py 2>&1

     echo "📋 Test 26: Stock Price Performance the last 2 Weeks: \$NVDA"
     echo "Stock Price Performance the last 2 Weeks: \$NVDA" | timeout 60 uv run src/backend/main.py 2>&1

     echo "📋 Test 27: Stock Price Performance the last month: \$NVDA"
     echo "Stock Price Performance the last month: \$NVDA" | timeout 60 uv run src/backend/main.py 2>&1
     ```
   - [ ] Renumber subsequent tests

5. [ ] **Update Test Counter:**
   - [ ] Find total test count declaration
   - [ ] Update: 40 tests → 44 tests (added 4 new tests, replaced 2 old)
   - [ ] Update any test count references in script

6. [ ] **Verify Test Syntax:**
   - [ ] Use Bash to run: `bash -n test_cli_regression.sh` (syntax check)
   - [ ] Fix any syntax errors

7. [ ] **Verify Changes:**
   - [ ] Use Read to review test_cli_regression.sh
   - [ ] Verify 3 new tests per ticker (6 total new tests)
   - [ ] Verify test numbering sequential
   - [ ] Verify test descriptions match requested format
   - [ ] Verify test counter updated

**Success Criteria:**
- [ ] SPY test sequence has 3 new tests (5 days, 2 weeks, 1 month)
- [ ] NVDA test sequence has 3 new tests
- [ ] Old "last 2 trading weeks" tests replaced
- [ ] Test numbering sequential
- [ ] Total test count: 44 tests
- [ ] Syntax valid (bash -n passes)

---

### 4.3: Run Full Regression Test Suite

**Task:** Execute complete test suite and verify 100% pass rate

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to analyze test results
- [ ] Use **Bash** to run test suite
- [ ] Use **Read** to review test report

**Steps:**
1. [ ] **Sequential-Thinking**: Plan regression testing
   - Expect 44 tests total
   - Plan for 100% pass rate requirement
   - Strategy for diagnosing failures

2. [ ] **Run Full Test Suite:**
   ```bash
   chmod +x test_cli_regression.sh && ./test_cli_regression.sh
   ```

3. [ ] **Review Test Results:**
   - [ ] Use Read to review test report in test-reports/ directory
   - [ ] Verify 44/44 tests PASSED (100% success rate)
   - [ ] Check average response time (target: ≤12 seconds)
   - [ ] Check session persistence verified
   - [ ] Identify any failures or errors

4. [ ] **If Tests Fail:**
   - [ ] **Sequential-Thinking**: Analyze failure patterns
     - Identify which tests failed
     - Determine root cause
     - Plan fix strategy
   - [ ] Fix identified issues
   - [ ] Re-run test suite
   - [ ] Repeat until 100% pass rate

5. [ ] **Document Test Results:**
   - [ ] Note test report file path
   - [ ] Note pass/fail counts (must be 44/44)
   - [ ] Note average response time
   - [ ] Note any performance changes vs baseline

**Success Criteria:**
- [ ] 44/44 tests PASSED (100% success rate)
- [ ] Test report generated in test-reports/
- [ ] No errors or failures in output
- [ ] Response times within acceptable range (≤12 seconds average)
- [ ] Session persistence verified
- [ ] New tests (5 days, 2 weeks, 1 month) all PASSED

**🔴 ENFORCEMENT:**
- [ ] Code without test execution = Code NOT implemented
- [ ] No test results = Task INCOMPLETE
- [ ] Cannot proceed without 100% pass rate
- [ ] Must show test evidence to user

---

## Phase 5: Serena Project Memories Update

### 5.1: Update tech_stack.md Memory

**Task:** Document Tradier historical pricing integration in Serena memory

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan memory update
- [ ] Use **Serena read_memory** to read current tech_stack.md
- [ ] Use **Edit** or **Write** to update tech_stack.md (use Edit for targeted changes)

**Steps:**
1. [ ] **Sequential-Thinking**: Plan memory update
   - What information to add
   - Where to add it (in existing Tradier section)
   - How to format for clarity

2. [ ] **Read Current Memory:**
   - [ ] Use Serena read_memory with `memory_file_name="tech_stack.md"`
   - [ ] Locate "Tradier API Migration" or recent updates section

3. [ ] **Update Memory:**
   - [ ] Use Edit to add new section: "Tradier Historical Pricing Migration (Oct 10, 2025)"
   - [ ] Document:
     - Tool created: `get_stock_price_history`
     - Tools removed: 3 Polygon OHLC tools
     - Tradier endpoint: `/v1/markets/history`
     - Intervals supported: daily, weekly, monthly
     - Migration date: October 10, 2025
     - Key benefits: Tool consolidation (3 → 1), new weekly/monthly capabilities
     - Backward compatibility notes: Full replacement, no breaking changes
     - Test results: 44/44 PASSED, X.XXs average
     - Tool count update: 13 → 11 tools total

**Success Criteria:**
- [ ] tech_stack.md updated with historical pricing migration details
- [ ] Information complete and accurate
- [ ] Formatted consistently with existing content
- [ ] New section added to "Data Sources" or "Recent Updates" area

---

## Phase 6: Final Git Commit 🔴 ATOMIC COMMIT WORKFLOW

### 6.1: Pre-Commit Verification

**Task:** Verify ALL work complete before staging

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to verify completion
- [ ] Use **Bash** to run git status and git diff
- [ ] Use **Read** to review any uncertain changes

**Steps:**
1. [ ] **Sequential-Thinking**: Verify completion checklist
   - All implementation steps complete
   - All tests passed
   - All documentation updated
   - All Serena memories updated

2. [ ] **Verify Work Complete:**
   - [ ] New tool created (tradier_tools.py)
   - [ ] 3 old tools removed (polygon_tools.py)
   - [ ] Exports updated (__init__.py)
   - [ ] Agent instructions updated (agent_service.py)
   - [ ] Agent tools list updated (agent_service.py)
   - [ ] Test suite updated (test_cli_regression.sh)
   - [ ] All tests run and passing (44/44 success)
   - [ ] Serena memory updated (tech_stack.md)
   - [ ] This TODO_task_plan.md updated

3. [ ] **Review Changes:**
   ```bash
   git status  # See all changed files
   git diff --stat  # Summary of changes
   ```

4. [ ] **Verify Nothing Staged Yet:**
   - [ ] Confirm staging area is EMPTY
   - [ ] ⚠️ DO NOT run `git add` yet

**Success Criteria:**
- [ ] All work verified complete
- [ ] All changes reviewed
- [ ] Staging area still EMPTY
- [ ] Ready for atomic commit

---

### 6.2: Atomic Commit and Push

**Task:** Stage ALL files at once, commit immediately, push immediately

**Mandatory Tool Usage:**
- [ ] Use **Bash** for git commands

**Steps:**
1. [ ] **Stage Everything at Once:**
   ```bash
   git add -A  # Stage ALL files in ONE command
   ```

2. [ ] **Verify Staging Immediately:**
   ```bash
   git status  # Verify ALL files staged, NOTHING unstaged
   ```

3. [ ] **Commit Immediately (within 60 seconds):**
   ```bash
   git commit -m "$(cat <<'EOF'
   [TRADIER] Migrate Polygon OHLC tools to Tradier historical pricing API

   Migration Summary:
   - Created new get_stock_price_history tool (Tradier API)
   - Removed 3 Polygon OHLC tools (consolidation 3→1)
   - Added multi-interval support (daily, weekly, monthly)
   - Tool count reduced from 13 to 11 tools

   New Tool Implementation (tradier_tools.py):
   - get_stock_price_history: Unified historical pricing tool
     - Parameters: ticker, start_date, end_date, interval
     - Intervals: daily (default), weekly, monthly
     - Response: ticker, interval, dates, bars array, count, source
     - API: https://api.tradier.com/v1/markets/history
     - Features: Date range flexibility, interval selection, OHLC bars

   Tools Removed (polygon_tools.py):
   - get_OHLC_bars_custom_date_range (replaced by get_stock_price_history)
   - get_OHLC_bars_specific_date (replaced by get_stock_price_history)
   - get_OHLC_bars_previous_close (replaced by get_stock_price_history)

   Agent Instruction Updates (agent_service.py):
   - New RULE: Historical stock prices with interval selection logic
   - Interval guidelines: daily (<2 weeks), weekly (2 weeks-3 months), monthly (>3 months)
   - Date calculation examples for relative queries
   - Removed old OHLC bars rule
   - Updated tool count: 13 → 11 tools
   - Updated examples: 3 new test cases per ticker

   Test Suite Updates (test_cli_regression.sh):
   - Total tests: 40 → 44 tests (added 4 new interval tests)
   - SPY sequence: Added 3 tests (5 days, 2 weeks, 1 month)
   - NVDA sequence: Added 3 tests (5 days, 2 weeks, 1 month)
   - Replaced "last 2 trading weeks" with "last 5 trading days"

   Test Results (44/44 PASSED - 100% success rate):
   - Total tests: 44 (SPY 19 + NVDA 19 + Multi 6)
   - Success rate: 100%
   - Avg response time: X.XXs (EXCELLENT rating)
   - Session duration: X min XX sec
   - New tests validated:
     - Daily interval (5 trading days): PASSED
     - Weekly interval (2 weeks): PASSED
     - Monthly interval (1 month): PASSED
   - Test report: test-reports/test_cli_regression_loop1_2025-10-10_XX-XX.log

   Key Benefits:
   - Tool consolidation: 3 separate tools → 1 unified tool
   - New capabilities: Weekly and monthly intervals
   - Improved flexibility: Single tool handles all date ranges
   - Better performance: Fewer tool decisions for agent
   - Cleaner architecture: Tradier for real-time data, Polygon for TA indicators

   Files Modified:
   - src/backend/tools/tradier_tools.py (added get_stock_price_history)
   - src/backend/tools/polygon_tools.py (removed 3 OHLC tools)
   - src/backend/tools/__init__.py (updated exports)
   - src/backend/services/agent_service.py (new RULE, updated tools list)
   - test_cli_regression.sh (44 tests, added 4 new interval tests)
   - .serena/memories/tech_stack.md (documented migration)
   - TODO_task_plan.md (implementation plan)

   Data Sources Update:
   - Tradier: 4 tools (quotes, market status, options expiration, historical pricing)
   - Polygon: 8 tools (TA indicators, options chains)
   - Total: 11 tools (reduced from 13)

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

4. [ ] **Push Immediately:**
   ```bash
   git push
   ```

**Success Criteria:**
- [ ] All files staged in single command
- [ ] Commit created within 60 seconds
- [ ] Commit message comprehensive
- [ ] Push successful
- [ ] No uncommitted changes

---

## Phase 7: Task Completion Verification

### 7.1: Final Checklist

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to verify all phases complete

**Final Verification:**
- [ ] Phase 1: Research ✅
- [ ] Phase 2: Planning ✅
- [ ] Phase 3: Implementation ✅
  - [ ] New tool created (get_stock_price_history)
  - [ ] 3 old tools removed
  - [ ] Exports updated
  - [ ] Agent instructions updated
  - [ ] Tools list updated
- [ ] Phase 4: Testing ✅
  - [ ] Manual tests passed
  - [ ] Test suite updated (44 tests)
  - [ ] Regression suite 100% pass rate
- [ ] Phase 5: Serena Updates ✅
  - [ ] tech_stack.md updated
- [ ] Phase 6: Git Commit ✅
  - [ ] Atomic commit complete
  - [ ] Push successful

**Success Criteria:**
- [ ] All phases complete
- [ ] New tool working with Tradier API
- [ ] All tests passing (44/44)
- [ ] All documentation updated
- [ ] All changes committed and pushed
- [ ] Task complete ✅

---

## Summary

**Migration Overview:**
- **New Tool:** `get_stock_price_history` (Tradier API)
  - Unified historical pricing with multi-interval support
  - Replaces 3 separate Polygon OHLC tools
  - Intervals: daily, weekly, monthly
  - Full date range flexibility

**Tools Removed:**
1. `get_OHLC_bars_custom_date_range` (Polygon)
2. `get_OHLC_bars_specific_date` (Polygon)
3. `get_OHLC_bars_previous_close` (Polygon)

**Key Achievements:**
- ✅ Tool consolidation (3 → 1)
- ✅ Tool count reduction (13 → 11)
- ✅ New weekly/monthly capabilities
- ✅ Single unified interface for all historical data
- ✅ Agent instructions updated with interval selection logic
- ✅ Test suite expanded (40 → 44 tests)
- ✅ All tests passing (100% success rate)
- ✅ Documentation updated

**Files Modified:**
1. src/backend/tools/tradier_tools.py (new tool)
2. src/backend/tools/polygon_tools.py (3 tools removed)
3. src/backend/tools/__init__.py (exports updated)
4. src/backend/services/agent_service.py (new RULE, tools list updated)
5. test_cli_regression.sh (44 tests, 4 new interval tests)
6. .serena/memories/tech_stack.md (migration documented)
7. TODO_task_plan.md (this file)

**Testing:**
- Total tests: 44 (SPY 19 + NVDA 19 + Multi 6)
- New test cases per ticker:
  - "Stock Price Performance the last 5 Trading Days" (daily)
  - "Stock Price Performance the last 2 Weeks" (weekly)
  - "Stock Price Performance the last month" (monthly)
- Expected: 100% pass rate
- Expected: ≤12 seconds average response time
