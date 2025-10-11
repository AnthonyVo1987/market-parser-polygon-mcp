# TODO: Tradier API Migration Implementation Plan

**Status:** Planning Complete - Ready for Implementation
**Created:** October 10, 2025
**Task:** Migrate `get_stock_quote` and `get_market_status_and_date_time` tools from Finnhub/Polygon to Tradier API

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
- Tradier API endpoints identified and analyzed
- Current implementations reviewed (finnhub_tools.py, polygon_tools.py)
- Agent instructions analyzed (RULE #1, #2, #3)
- Edge cases and error handling requirements documented
- Response structure differences understood (single object vs multi array)
- Backward compatibility requirements defined

---

## Phase 2: Planning ✅ COMPLETE

**Status:** ✅ Complete
**Output:** This implementation plan

---

## Phase 3: Implementation 🔴 START HERE

### 3.1: Environment Setup

**Task:** Add TRADIER_API_KEY to environment configuration

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan environment setup strategy
- [ ] Use **Read** to check current .env file structure
- [ ] Use **Edit** to add TRADIER_API_KEY to .env file
- [ ] Use **Bash** to verify .env file has new key

**Steps:**
1. [ ] Read `.env` file to understand current structure
2. [ ] Add `TRADIER_API_KEY=your_key_here` line to `.env`
3. [ ] Verify `.env` file has all required keys (TRADIER_API_KEY, POLYGON_API_KEY, OPENAI_API_KEY)
4. [ ] Document environment setup in comments

**Success Criteria:**
- [ ] TRADIER_API_KEY present in .env
- [ ] No duplicate entries
- [ ] File format preserved

---

### 3.2: Migrate get_stock_quote Tool

**Task:** Replace Finnhub implementation with Tradier API in finnhub_tools.py

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan migration strategy and edge case handling
- [ ] Use **Serena find_symbol** to locate get_stock_quote function
- [ ] Use **Serena replace_symbol_body** to replace function implementation
- [ ] Use **Serena find_referencing_symbols** to check if any other code references this function
- [ ] Use **Read** to verify changes after implementation

**Steps:**
1. [ ] **Sequential-Thinking**: Analyze migration strategy
   - Single vs multi-ticker response handling
   - URL encoding approach
   - Error handling strategy
   - Backward compatibility preservation

2. [ ] **Read Current Implementation:**
   - [ ] Use Serena find_symbol with `name_path="/get_stock_quote"`, `relative_path="src/backend/tools/finnhub_tools.py"`, `include_body=True`
   - [ ] Analyze current function signature and return format

3. [ ] **Design New Implementation:**
   - [ ] Parameter: Keep `ticker: str` for single ticker backward compatibility
   - [ ] Support comma-separated tickers: "SPY,NVDA,SOUN"
   - [ ] Implement response structure detection:
     ```python
     if isinstance(data['quotes']['quote'], list):
         # Multi-ticker response
     else:
         # Single ticker response
     ```
   - [ ] Map Tradier fields to current response format:
     - `symbol` → `ticker`
     - `last` → `current_price`
     - `change` → `change`
     - `change_percentage` → `percent_change`
     - `high` → `high`
     - `low` → `low`
     - `open` → `open`
     - `prevclose` → `previous_close`

4. [ ] **Implement New Function:**
   ```python
   @function_tool
   async def get_stock_quote(ticker: str) -> str:
       """Get real-time stock quote from Tradier API.

       Use this tool when the user requests a stock quote, current price,
       or real-time market data for one or more ticker symbols.

       Args:
           ticker: Stock ticker symbol(s). Can be:
                   - Single ticker: "AAPL"
                   - Multiple tickers: "AAPL,TSLA,NVDA" (comma-separated)
                   Must be valid ticker(s) from major US exchanges.

       Returns:
           JSON string containing quote data. For single ticker:
           {
               "ticker": "AAPL",
               "current_price": 178.50,
               "change": 2.30,
               "percent_change": 1.31,
               "high": 179.20,
               "low": 176.80,
               "open": 177.00,
               "previous_close": 176.20,
               "source": "Tradier"
           }

           For multiple tickers, returns array of quote objects.
       """
       try:
           # Get API key from environment
           api_key = os.getenv("TRADIER_API_KEY")
           if not api_key:
               return json.dumps({"error": "TRADIER_API_KEY not configured"})

           # Build request
           url = "https://api.tradier.com/v1/markets/quotes"
           headers = {
               "Accept": "application/json",
               "Authorization": f"Bearer {api_key}"
           }
           params = {"symbols": ticker}  # requests handles URL encoding

           # Make request
           response = requests.get(url, headers=headers, params=params, timeout=10)
           response.raise_for_status()

           data = response.json()
           quotes_data = data.get("quotes", {}).get("quote")

           if not quotes_data:
               return json.dumps({"error": "No quote data returned"})

           # Handle single vs multi-ticker response
           if isinstance(quotes_data, list):
               # Multi-ticker response
               results = []
               for quote in quotes_data:
                   results.append(_format_tradier_quote(quote))
               return json.dumps(results, indent=2)
           else:
               # Single ticker response
               return json.dumps(_format_tradier_quote(quotes_data), indent=2)

       except requests.exceptions.RequestException as e:
           return json.dumps({"error": f"Tradier API request failed: {str(e)}"})
       except Exception as e:
           return json.dumps({"error": f"Unexpected error: {str(e)}"})

   def _format_tradier_quote(quote: dict) -> dict:
       """Format Tradier quote data to match current response structure."""
       return {
           "ticker": quote.get("symbol", ""),
           "current_price": quote.get("last", 0.0),
           "change": quote.get("change", 0.0),
           "percent_change": quote.get("change_percentage", 0.0),
           "high": quote.get("high", 0.0),
           "low": quote.get("low", 0.0),
           "open": quote.get("open", 0.0),
           "previous_close": quote.get("prevclose", 0.0),
           "source": "Tradier"
       }
   ```

5. [ ] **Replace Function Using Serena:**
   - [ ] Use Serena replace_symbol_body with `name_path="/get_stock_quote"`, `relative_path="src/backend/tools/finnhub_tools.py"`, `body="<new implementation>"`

6. [ ] **Add Helper Function:**
   - [ ] Use Serena insert_after_symbol to add `_format_tradier_quote` helper function after `get_stock_quote`

7. [ ] **Update Imports:**
   - [ ] Check if `requests` is already imported in finnhub_tools.py
   - [ ] Check if `os` is already imported
   - [ ] Add imports if needed using Serena insert_before_symbol

8. [ ] **Verify Implementation:**
   - [ ] Use Read to review entire finnhub_tools.py file
   - [ ] Verify function signature unchanged (backward compatibility)
   - [ ] Verify error handling comprehensive
   - [ ] Verify response format matches current structure

**Success Criteria:**
- [ ] Function accepts single ticker: "AAPL"
- [ ] Function accepts multi-ticker: "AAPL,TSLA,NVDA"
- [ ] Response structure matches current format
- [ ] Error handling for authentication, network, invalid ticker
- [ ] Timeout set to 10 seconds
- [ ] No Finnhub SDK dependencies remaining

---

### 3.3: Migrate get_market_status_and_date_time Tool

**Task:** Replace Polygon implementation with Tradier API in polygon_tools.py

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan timestamp conversion and state mapping strategy
- [ ] Use **Serena find_symbol** to locate get_market_status_and_date_time function
- [ ] Use **Serena replace_symbol_body** to replace function implementation
- [ ] Use **Read** to verify changes after implementation

**Steps:**
1. [ ] **Sequential-Thinking**: Analyze migration strategy
   - Tradier state to current response mapping
   - Unix timestamp to ISO datetime conversion
   - early_hours and after_hours flag logic
   - Exchange status population strategy

2. [ ] **Read Current Implementation:**
   - [ ] Use Serena find_symbol with `name_path="/get_market_status_and_date_time"`, `relative_path="src/backend/tools/polygon_tools.py"`, `include_body=True`
   - [ ] Analyze current function signature and return format

3. [ ] **Design New Implementation:**
   - [ ] State mapping:
     - "open" → market_status="open"
     - "closed" → market_status="closed"
     - "pre" → market_status="extended-hours", early_hours=true
     - "post" → market_status="extended-hours", after_hours=true
   - [ ] Timestamp conversion:
     - Tradier: Unix epoch milliseconds (1760140800001)
     - Target: ISO datetime "2025-10-05T14:30:00Z"
     - Python: `datetime.fromtimestamp(timestamp/1000, tz=timezone.utc).isoformat()`
   - [ ] Exchange status: Use overall market state for all exchanges (backward compatibility)

4. [ ] **Implement New Function:**
   ```python
   @function_tool
   async def get_market_status_and_date_time() -> str:
       """Get current market status and date/time from Tradier API.

       Returns:
           JSON string containing market status and datetime with format:
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
               "source": "Tradier"
           }
       """
       try:
           # Get API key from environment
           api_key = os.getenv("TRADIER_API_KEY")
           if not api_key:
               return json.dumps({"error": "TRADIER_API_KEY not configured"})

           # Build request
           url = "https://api.tradier.com/v1/markets/clock"
           headers = {
               "Accept": "application/json",
               "Authorization": f"Bearer {api_key}"
           }

           # Make request
           response = requests.get(url, headers=headers, timeout=10)
           response.raise_for_status()

           data = response.json()
           clock_data = data.get("clock", {})

           if not clock_data:
               return json.dumps({"error": "No clock data returned"})

           # Map Tradier state to current response format
           state = clock_data.get("state", "closed")
           market_status = _map_tradier_state(state)
           early_hours = (state == "pre")
           after_hours = (state == "post")

           # Convert Unix timestamp to ISO datetime
           timestamp = clock_data.get("timestamp", 0)
           server_time_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
           server_time = server_time_dt.isoformat()
           date_str = server_time_dt.strftime("%Y-%m-%d")
           time_str = server_time_dt.strftime("%H:%M:%S")

           # Build response with exchange status (use overall state for all)
           exchange_status = market_status

           return json.dumps({
               "market_status": market_status,
               "after_hours": after_hours,
               "early_hours": early_hours,
               "exchanges": {
                   "nasdaq": exchange_status,
                   "nyse": exchange_status,
                   "otc": exchange_status
               },
               "server_time": server_time,
               "date": date_str,
               "time": time_str,
               "source": "Tradier"
           }, indent=2)

       except requests.exceptions.RequestException as e:
           return json.dumps({"error": f"Tradier API request failed: {str(e)}"})
       except Exception as e:
           return json.dumps({"error": f"Unexpected error: {str(e)}"})

   def _map_tradier_state(state: str) -> str:
       """Map Tradier market state to current response format."""
       if state == "open":
           return "open"
       elif state in ["pre", "post"]:
           return "extended-hours"
       else:  # closed
           return "closed"
   ```

5. [ ] **Replace Function Using Serena:**
   - [ ] Use Serena replace_symbol_body with `name_path="/get_market_status_and_date_time"`, `relative_path="src/backend/tools/polygon_tools.py"`, `body="<new implementation>"`

6. [ ] **Add Helper Function:**
   - [ ] Use Serena insert_after_symbol to add `_map_tradier_state` helper function after `get_market_status_and_date_time`

7. [ ] **Update Imports:**
   - [ ] Check current imports in polygon_tools.py
   - [ ] Ensure `datetime`, `timezone` imported from datetime module
   - [ ] Ensure `requests` imported
   - [ ] Ensure `os` imported
   - [ ] Add missing imports using Serena insert_before_symbol

8. [ ] **Verify Implementation:**
   - [ ] Use Read to review entire polygon_tools.py file
   - [ ] Verify function signature unchanged (backward compatibility)
   - [ ] Verify timestamp conversion correct
   - [ ] Verify state mapping handles all cases
   - [ ] Verify response format matches current structure

**Success Criteria:**
- [ ] Function returns market status ("open", "closed", "extended-hours")
- [ ] Correctly sets early_hours flag when state="pre"
- [ ] Correctly sets after_hours flag when state="post"
- [ ] Timestamp converts correctly to ISO format
- [ ] Date and time fields extracted correctly
- [ ] Exchange status populated for backward compatibility
- [ ] No Polygon SDK dependencies remaining for this function

---

### 3.4: Update Agent Instructions

**Task:** Update RULE #1, #2, and #3 in agent_service.py to reflect Tradier API usage

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan instruction updates strategy
- [ ] Use **Serena search_for_pattern** to locate RULE #1, #2, #3 in agent_service.py
- [ ] Use **Edit** to update agent instructions (multi-line text replacement)
- [ ] Use **Read** to verify changes after implementation

**Steps:**
1. [ ] **Sequential-Thinking**: Analyze instruction update strategy
   - Decide whether to merge RULE #1 and #2 or keep separate
   - Plan wording changes for Tradier API references
   - Ensure multi-ticker support clearly documented

2. [ ] **Locate Current Instructions:**
   - [ ] Use Serena search_for_pattern with `substring_pattern="RULE #1: SINGLE TICKER"`, `relative_path="src/backend/services/agent_service.py"`, `context_lines_before=2`, `context_lines_after=10`
   - [ ] Use Serena search_for_pattern with `substring_pattern="RULE #2: MULTIPLE TICKERS"`, `relative_path="src/backend/services/agent_service.py"`, `context_lines_before=2`, `context_lines_after=10`
   - [ ] Use Serena search_for_pattern with `substring_pattern="RULE #3: MARKET STATUS"`, `relative_path="src/backend/services/agent_service.py"`, `context_lines_before=2`, `context_lines_after=10`

3. [ ] **Update RULE #1:**
   - [ ] Change title from "SINGLE TICKER" to "STOCK QUOTE (SINGLE OR MULTI-TICKER)"
   - [ ] Update: "📊 Uses Finnhub API" → "📊 Uses Tradier API"
   - [ ] Add note about multi-ticker support: "Supports comma-separated tickers (e.g., 'AAPL,TSLA,NVDA')"
   - [ ] Keep same use case description and examples

   **New RULE #1:**
   ```
   RULE #1: STOCK QUOTE (SINGLE OR MULTI-TICKER) = ALWAYS USE get_stock_quote()
   - If the request mentions ONE OR MORE ticker symbols → MUST USE get_stock_quote(ticker='SYMBOL') or get_stock_quote(ticker='SYM1,SYM2,SYM3')
   - 📊 Uses Tradier API for real-time quote data
   - ✅ Supports single ticker: get_stock_quote(ticker='AAPL')
   - ✅ Supports multiple tickers: get_stock_quote(ticker='AAPL,TSLA,NVDA') (comma-separated, no spaces)
   - ✅ Returns: current price, change, percent change, high, low, open, previous close
   ```

4. [ ] **Update RULE #2:**
   - [ ] Keep rule separate for clarity (backward compatibility)
   - [ ] Update to reference Tradier's native multi-ticker support
   - [ ] Remove parallel call instructions
   - [ ] Emphasize single tool call with comma-separated tickers

   **New RULE #2:**
   ```
   RULE #2: MULTIPLE TICKERS = SINGLE TOOL CALL WITH COMMA-SEPARATED TICKERS
   - **ANALYZE REQUEST COMPLEXITY FIRST**: Count ticker symbols in user request
   - **Single Ticker (count = 1)**: Use get_stock_quote(ticker='SYMBOL')
   - **Multiple Tickers (count = 2+)**: Use SINGLE CALL with comma-separated tickers
     - Example: get_stock_quote(ticker='AAPL,TSLA,NVDA')
     - Format: Comma-separated, NO SPACES between tickers
     - Maximum: No hard limit, but keep under 10 tickers for performance
   - 📊 Uses Tradier API (supports native multi-ticker queries - NO parallel calls needed)
   - ✅ Returns: Array of quote objects, one per ticker
   ```

5. [ ] **Update RULE #3:**
   - [ ] Update: "Uses Polygon.io Direct API" → "Uses Tradier API"
   - [ ] Keep same use case description
   - [ ] Update response field descriptions if needed

   **New RULE #3:**
   ```
   RULE #3: MARKET STATUS & DATE/TIME = ALWAYS USE get_market_status_and_date_time()
   - If the request asks about market open/closed status, hours, trading sessions, current date, or current time
   - 📊 Uses Tradier API for real-time market status and server datetime
   - ✅ Returns: market status, exchange statuses, after_hours, early_hours, server_time with date and time
   ```

6. [ ] **Apply Changes:**
   - [ ] Use Edit to replace RULE #1 text
   - [ ] Use Edit to replace RULE #2 text
   - [ ] Use Edit to replace RULE #3 text

7. [ ] **Verify Changes:**
   - [ ] Use Read to review updated agent_service.py
   - [ ] Verify all Finnhub references removed
   - [ ] Verify all Polygon references removed (for these tools)
   - [ ] Verify instructions are clear and unambiguous

**Success Criteria:**
- [ ] RULE #1 updated to reflect Tradier API and multi-ticker support
- [ ] RULE #2 updated to remove parallel calls, emphasize single call with comma-separated tickers
- [ ] RULE #3 updated to reflect Tradier API
- [ ] No references to Finnhub or Polygon for these specific tools
- [ ] Instructions clear and consistent with new implementation

---

## Phase 4: Testing 🔴 MANDATORY - DO NOT SKIP

### 4.1: Quick Manual Testing

**Task:** Test each tool individually with CLI to verify basic functionality

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan testing strategy and analyze test results
- [ ] Use **Bash** to run CLI tests
- [ ] Use **Read** to review test output logs

**Steps:**
1. [ ] **Sequential-Thinking**: Plan testing strategy
   - Test order: Single ticker → Multi-ticker → Market status
   - Expected response format verification
   - Error case testing

2. [ ] **Test get_stock_quote - Single Ticker:**
   - [ ] Run: `uv run src/backend/main.py` with prompt "Get quote for SPY"
   - [ ] Verify response has all 8 fields
   - [ ] Verify source="Tradier"
   - [ ] Check response time
   - [ ] Save output for review

3. [ ] **Test get_stock_quote - Multi-Ticker:**
   - [ ] Run: `uv run src/backend/main.py` with prompt "Get quotes for SPY, NVDA, SOUN"
   - [ ] Verify response is array of quote objects
   - [ ] Verify all 3 tickers present
   - [ ] Verify each has all 8 fields
   - [ ] Check response time
   - [ ] Save output for review

4. [ ] **Test get_market_status_and_date_time:**
   - [ ] Run: `uv run src/backend/main.py` with prompt "Is the market open?"
   - [ ] Verify market_status field present
   - [ ] Verify date and time fields present
   - [ ] Verify exchange statuses present
   - [ ] Check response time
   - [ ] Save output for review

5. [ ] **Test All Required Tickers:**
   - [ ] SPY: "Get quote for SPY"
   - [ ] NVDA: "Get quote for NVDA"
   - [ ] SOUN: "Get quote for SOUN"
   - [ ] QQQ: "Get quote for QQQ"
   - [ ] IWM: "Get quote for IWM"
   - [ ] Multi: "Get quotes for SPY, NVDA, SOUN, QQQ, IWM"

6. [ ] **Sequential-Thinking**: Analyze test results
   - Check if all responses match expected format
   - Verify Tradier API is being called
   - Identify any unexpected behavior
   - Plan fixes if needed

**Success Criteria:**
- [ ] All single ticker tests return correct format
- [ ] Multi-ticker test returns array of quotes
- [ ] Market status test returns correct format
- [ ] All responses use source="Tradier"
- [ ] No errors or exceptions
- [ ] Response times reasonable (<3 seconds)

---

### 4.2: Regression Test Suite

**Task:** Run full test_cli_regression.sh suite to ensure no breaking changes

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to analyze test results and diagnose failures
- [ ] Use **Bash** to run test suite
- [ ] Use **Read** to review test report
- [ ] Use **Bash** to fix issues if tests fail

**Steps:**
1. [ ] **Sequential-Thinking**: Plan regression testing approach
   - Understand current test suite structure
   - Plan for 100% pass rate requirement
   - Strategy for diagnosing failures if they occur

2. [ ] **Run Full Test Suite:**
   ```bash
   chmod +x test_cli_regression.sh && ./test_cli_regression.sh
   ```

3. [ ] **Review Test Results:**
   - [ ] Use Read to review test report in test-reports/ directory
   - [ ] Verify 100% success rate (X/X PASSED)
   - [ ] Check average response time
   - [ ] Check session persistence
   - [ ] Identify any failures or errors

4. [ ] **If Tests Fail:**
   - [ ] **Sequential-Thinking**: Analyze failure patterns
     - Identify which tests failed
     - Determine root cause
     - Plan fix strategy
   - [ ] Fix identified issues using appropriate tools
   - [ ] Re-run test suite
   - [ ] Repeat until 100% pass rate achieved

5. [ ] **Document Test Results:**
   - [ ] Note test report file path
   - [ ] Note pass/fail counts
   - [ ] Note average response time
   - [ ] Note any performance changes vs baseline

**Success Criteria:**
- [ ] 100% test pass rate (38/38 PASSED or similar)
- [ ] Test report generated in test-reports/
- [ ] No errors or failures in output
- [ ] Response times within acceptable range (≤12 seconds average)
- [ ] Session persistence verified

**🔴 ENFORCEMENT:**
- [ ] Code without test execution = Code NOT implemented
- [ ] No test results = Task INCOMPLETE
- [ ] Cannot proceed to next phase without 100% pass rate
- [ ] Must show test evidence to user

---

### 4.3: Edge Case Testing

**Task:** Test error handling and edge cases

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan edge case testing
- [ ] Use **Bash** to run edge case tests
- [ ] Use **Read** to review error responses

**Steps:**
1. [ ] **Sequential-Thinking**: Plan edge case testing
   - Invalid ticker
   - Empty ticker string
   - Missing API key scenario
   - Network error simulation

2. [ ] **Test Invalid Ticker:**
   - [ ] Run: `uv run src/backend/main.py` with prompt "Get quote for INVALIDTICKER123"
   - [ ] Verify graceful error handling
   - [ ] Verify error message is clear

3. [ ] **Test Empty Ticker:**
   - [ ] Run: `uv run src/backend/main.py` with prompt "Get quote for "
   - [ ] Verify graceful error handling

4. [ ] **Test Missing API Key (if possible):**
   - [ ] Temporarily remove TRADIER_API_KEY from .env
   - [ ] Run test
   - [ ] Verify error message indicates missing API key
   - [ ] Restore API key

5. [ ] **Document Edge Case Results:**
   - [ ] Note error handling behavior
   - [ ] Verify user-friendly error messages
   - [ ] Identify any improvements needed

**Success Criteria:**
- [ ] Invalid ticker returns clear error message
- [ ] Empty ticker handled gracefully
- [ ] Missing API key error is informative
- [ ] No crashes or unhandled exceptions

---

## Phase 5: Serena Project Memories Update

### 5.1: Update tech_stack.md Memory

**Task:** Document Tradier API integration in Serena memory

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to plan memory update content
- [ ] Use **Serena read_memory** to read current tech_stack.md
- [ ] Use **Serena write_memory** to update tech_stack.md

**Steps:**
1. [ ] **Sequential-Thinking**: Plan memory update
   - What information to add
   - Where to add it in existing structure
   - How to format for future reference

2. [ ] **Read Current Memory:**
   - [ ] Use Serena read_memory with `memory_file_name="tech_stack.md"`

3. [ ] **Update Memory:**
   - [ ] Use Serena write_memory with `memory_name="tech_stack.md"`
   - [ ] Add section: "Tradier API Integration"
   - [ ] Document:
     - Tools migrated: get_stock_quote, get_market_status_and_date_time
     - Tradier endpoints used
     - Migration date
     - Key implementation details
     - Multi-ticker support
     - Backward compatibility notes

**Success Criteria:**
- [ ] tech_stack.md updated with Tradier integration details
- [ ] Information complete and accurate
- [ ] Formatted consistently with existing content

---

### 5.2: Update testing_procedures.md Memory (if exists)

**Task:** Document new testing requirements for Tradier tools

**Mandatory Tool Usage:**
- [ ] Use **Serena list_memories** to check if testing_procedures.md exists
- [ ] Use **Sequential-Thinking** to plan testing documentation
- [ ] Use **Serena read_memory** to read current testing_procedures.md (if exists)
- [ ] Use **Serena write_memory** to update testing_procedures.md

**Steps:**
1. [ ] **Check Memory Exists:**
   - [ ] Use Serena list_memories
   - [ ] Identify if testing_procedures.md or similar exists

2. [ ] **If Exists:**
   - [ ] Use Serena read_memory
   - [ ] **Sequential-Thinking**: Plan updates
   - [ ] Use Serena write_memory to add:
     - Tradier API testing requirements
     - Multi-ticker test cases
     - Edge case test scenarios

**Success Criteria:**
- [ ] Testing procedures updated (if memory exists)
- [ ] Tradier testing documented
- [ ] Multi-ticker testing documented

---

## Phase 6: Final Git Commit 🔴 ATOMIC COMMIT WORKFLOW

### 6.1: Pre-Commit Verification

**Task:** Verify ALL work is complete before staging

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to verify completion checklist
- [ ] Use **Bash** to run git status and git diff
- [ ] Use **Read** to review any uncertain changes

**Steps:**
1. [ ] **Sequential-Thinking**: Verify completion
   - Check all implementation steps complete
   - Check all tests passed
   - Check all documentation updated
   - Check all Serena memories updated

2. [ ] **Verify Work Complete:**
   - [ ] All code changes done (finnhub_tools.py, polygon_tools.py, agent_service.py)
   - [ ] All tests run and passing (100% success rate)
   - [ ] All documentation updated (CLAUDE.md if needed)
   - [ ] All Serena memories updated (tech_stack.md, testing_procedures.md)
   - [ ] .env file has TRADIER_API_KEY
   - [ ] This TODO_task_plan.md updated with completion status

3. [ ] **Review Changes:**
   ```bash
   git status  # See all changed files
   git diff    # Review all changes
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
- [ ] Use **Sequential-Thinking** if any issues arise

**Steps:**
1. [ ] **Stage Everything at Once:**
   ```bash
   git add -A  # Stage ALL files in ONE command
   ```
   - [ ] This is the FIRST time running `git add`
   - [ ] All related files staged together

2. [ ] **Verify Staging Immediately:**
   ```bash
   git status  # Verify ALL files staged, NOTHING unstaged
   ```
   - [ ] If anything missing: `git add [missing-file]`

3. [ ] **Commit Immediately (within 60 seconds):**
   ```bash
   git commit -m "$(cat <<'EOF'
   [TRADIER] Migrate get_stock_quote and get_market_status_and_date_time to Tradier API

   - Migrate get_stock_quote from Finnhub to Tradier API
     - Add multi-ticker support (comma-separated tickers)
     - Handle single object vs array response structure
     - Map Tradier fields to current response format
     - Update source field to "Tradier"

   - Migrate get_market_status_and_date_time from Polygon to Tradier API
     - Map Tradier state ("open", "closed", "pre", "post") to current format
     - Convert Unix timestamp to ISO datetime
     - Populate exchange statuses for backward compatibility
     - Update source field to "Tradier"

   - Update agent instructions (RULE #1, #2, #3)
     - RULE #1: Expand to support multi-ticker
     - RULE #2: Update to use single call with comma-separated tickers
     - RULE #3: Update Polygon reference to Tradier

   - Add TRADIER_API_KEY to .env

   - Testing results:
     - All single ticker tests PASSED (SPY, NVDA, SOUN, QQQ, IWM)
     - Multi-ticker test PASSED (SPY,NVDA,SOUN,QQQ,IWM)
     - Market status test PASSED
     - Full regression suite: X/X PASSED (100% success rate)
     - Test report: test-reports/test_cli_regression_loopX_2025-10-10_XX-XX.log

   - Update Serena memories:
     - tech_stack.md: Document Tradier API integration
     - testing_procedures.md: Add Tradier testing requirements (if exists)

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
- [ ] All files staged in single `git add -A` command
- [ ] Commit created within 60 seconds of staging
- [ ] Commit message comprehensive and accurate
- [ ] Push successful
- [ ] No uncommitted changes remaining

---

## Phase 7: Task Completion Verification

### 7.1: Final Checklist

**Mandatory Tool Usage:**
- [ ] Use **Sequential-Thinking** to verify all phases complete

**Final Verification:**
- [ ] Phase 1: Research ✅
- [ ] Phase 2: Planning ✅
- [ ] Phase 3: Implementation ✅
  - [ ] Environment setup complete
  - [ ] get_stock_quote migrated
  - [ ] get_market_status_and_date_time migrated
  - [ ] Agent instructions updated
- [ ] Phase 4: Testing ✅
  - [ ] Quick manual tests passed
  - [ ] Regression suite 100% pass rate
  - [ ] Edge cases tested
- [ ] Phase 5: Serena Updates ✅
  - [ ] tech_stack.md updated
  - [ ] testing_procedures.md updated (if exists)
- [ ] Phase 6: Git Commit ✅
  - [ ] Atomic commit complete
  - [ ] Push successful

**Success Criteria:**
- [ ] All phases complete
- [ ] All tools working with Tradier API
- [ ] All tests passing
- [ ] All documentation updated
- [ ] All changes committed and pushed
- [ ] Task complete ✅

---

## Summary

**Migration Overview:**
- **Tool 1:** get_stock_quote (Finnhub → Tradier)
  - Added multi-ticker support
  - Maintained backward compatibility
  - Updated agent instructions

- **Tool 2:** get_market_status_and_date_time (Polygon → Tradier)
  - Mapped state to current format
  - Converted timestamp format
  - Maintained backward compatibility

**Key Achievements:**
- ✅ Tradier API integration complete
- ✅ Multi-ticker support added to get_stock_quote
- ✅ All tests passing (100% success rate)
- ✅ Agent instructions updated
- ✅ Documentation updated
- ✅ Atomic commit complete

**Files Modified:**
1. src/backend/tools/finnhub_tools.py
2. src/backend/tools/polygon_tools.py
3. src/backend/services/agent_service.py
4. .env
5. .serena/memories/tech_stack.md
6. .serena/memories/testing_procedures.md (if exists)

**Testing:**
- Single ticker tests: SPY, NVDA, SOUN, QQQ, IWM ✅
- Multi-ticker test: SPY,NVDA,SOUN,QQQ,IWM ✅
- Market status test ✅
- Full regression suite: 100% pass rate ✅
