# TODO Task Plan: Implement Options Chain Tools

**Task:** Create `get_call_options_chain` and `get_put_options_chain` tools with full integration

**Status:** Planning Complete - Ready for Implementation

---

## 📋 IMPLEMENTATION CHECKLIST

### PHASE 1: ✅ RESEARCH (COMPLETED)

- [x] Research Polygon.io `list_snapshot_options_chain` API endpoint
- [x] Analyze existing tool patterns in `polygon_tools.py`
- [x] Study agent instruction structure in `agent_service.py`
- [x] Review test suite structure in `test_cli_regression.sh`
- [x] Understand response formatting requirements (2 decimal precision)

**Research Findings:**
- Polygon Python SDK method: `client.list_snapshot_options_chain(underlying_asset, params={})`
- Returns: `Iterator[OptionContractSnapshot]` with pagination
- Response includes: day, details, greeks, implied_volatility, open_interest
- Tool pattern: @function_tool, async, JSON returns, lazy client init
- Agent has 10 tools currently, will become 12 after additions

---

### PHASE 2: PLANNING (IN PROGRESS)

#### Tool Implementation Requirements

**Tool 1: `get_call_options_chain`**
- **Purpose:** Fetch 10 Call Option strike prices ABOVE current price
- **Location:** `src/backend/tools/polygon_tools.py`
- **Parameters:**
  - `ticker` (str, required): Stock ticker symbol
  - `current_price` (float, required): Current underlying stock price
  - `expiration_date` (str, required): Expiration date (YYYY-MM-DD format)
- **API Call Parameters (hardcoded):**
  - `strike_price.gte`: current_price
  - `expiration_date`: expiration_date
  - `contract_type`: "call"
  - `order`: "asc"
  - `limit`: 10
  - `sort`: "strike_price"
- **Response Format:**
  ```json
  {
    "ticker_symbol Call Options Chain: expiration_date": {
      "$strike1": {"close": X.XX, "delta": X.XX, "gamma": X.XX, "theta": X.XX, "implied_volatility": X.XX, "volume": XXXX, "open_interest": XXXX},
      "$strike2": {...}
    }
  }
  ```

**Tool 2: `get_put_options_chain`**
- **Purpose:** Fetch 10 Put Option strike prices BELOW current price
- **Location:** `src/backend/tools/polygon_tools.py`
- **Parameters:**
  - `ticker` (str, required): Stock ticker symbol
  - `current_price` (float, required): Current underlying stock price
  - `expiration_date` (str, required): Expiration date (YYYY-MM-DD format)
- **API Call Parameters (hardcoded):**
  - `strike_price.lte`: current_price
  - `expiration_date`: expiration_date
  - `contract_type`: "put"
  - `order`: "desc"
  - `limit`: 10
  - `sort`: "strike_price"
- **Response Format:**
  ```json
  {
    "ticker_symbol Put Options Chain: expiration_date": {
      "$strike1": {"close": X.XX, "delta": X.XX, "gamma": X.XX, "theta": X.XX, "implied_volatility": X.XX, "volume": XXXX, "open_interest": XXXX},
      "$strike2": {...}
    }
  }
  ```

---

### PHASE 3: IMPLEMENTATION

#### 3.1 Create Options Chain Tools

**File:** `src/backend/tools/polygon_tools.py`

- [ ] Use Serena `insert_after_symbol` to add `get_call_options_chain` after `get_ta_macd`
  - [ ] Add @function_tool decorator
  - [ ] Define async function with type hints
  - [ ] Add comprehensive docstring (Args, Returns, Note, Examples)
  - [ ] Implement logic:
    - [ ] Get Polygon client via `_get_polygon_client()`
    - [ ] Call `client.list_snapshot_options_chain()` with call parameters
    - [ ] Extract and format response data
    - [ ] Round all values to 2 decimals
    - [ ] Return JSON string with formatted chain
    - [ ] Handle errors with proper error JSON

- [ ] Use Serena `insert_after_symbol` to add `get_put_options_chain` after `get_call_options_chain`
  - [ ] Add @function_tool decorator
  - [ ] Define async function with type hints
  - [ ] Add comprehensive docstring (Args, Returns, Note, Examples)
  - [ ] Implement logic:
    - [ ] Get Polygon client via `_get_polygon_client()`
    - [ ] Call `client.list_snapshot_options_chain()` with put parameters
    - [ ] Extract and format response data
    - [ ] Round all values to 2 decimals
    - [ ] Return JSON string with formatted chain
    - [ ] Handle errors with proper error JSON

#### 3.2 Update Agent Service

**File:** `src/backend/services/agent_service.py`

- [ ] Use Serena `find_symbol` to locate import section (lines 7-17)
- [ ] Use Serena `replace_symbol_body` or Edit to add imports:
  ```python
  from ..tools.polygon_tools import (
      ...,
      get_call_options_chain,  # Add this
      get_put_options_chain,   # Add this
  )
  ```

- [ ] Use Serena to update agent tools list (lines 384-394):
  - [ ] Add `get_call_options_chain` to tools list
  - [ ] Add `get_put_options_chain` to tools list
  - [ ] Update comment: "Finnhub + Polygon direct API tools (1 Finnhub + 11 Polygon)" → "12 Polygon"

- [ ] Use Serena or Edit to update agent instructions (line 34):
  - [ ] Change tool count from 10 to 12
  - [ ] Update tool list to include: `get_call_options_chain, get_put_options_chain`

- [ ] Use Serena or Edit to add new RULE #9 for Options Chain queries:
  ```
  RULE #9: OPTIONS CHAIN = USE get_call_options_chain OR get_put_options_chain
  - If request asks for call options chain, use get_call_options_chain(ticker, current_price, expiration_date)
  - If request asks for put options chain, use get_put_options_chain(ticker, current_price, expiration_date)
  - Agent must determine: ticker, current_price (via get_stock_quote if needed), expiration_date
  - Call options: Strike prices ABOVE current price (ascending order)
  - Put options: Strike prices BELOW current price (descending order)
  - Returns formatted chain with Greeks, IV, volume, open interest
  - Examples:
    * "SPY Call Options Chain expiring Oct 10" → get_call_options_chain(ticker='SPY', current_price=673.0, expiration_date='2025-10-10')
    * "NVDA Put Options Chain expiring this Friday" → get_put_options_chain(ticker='NVDA', current_price=<current>, expiration_date=<this_friday>)
  ```

#### 3.3 Update Test Suite

**File:** `test_cli_regression.sh`

- [ ] Use Read to understand current test structure
- [ ] Use Serena `search_for_pattern` to locate SPY Technical Analysis test (around line 150-160)
- [ ] Use Edit to add 2 SPY options tests after SPY TA test:
  ```bash
  # Test X: SPY Call Options Chain
  echo "Test X: SPY Call Options Chain Expiring this Friday"
  echo "Get the SPY Call Options Chain Expiring this Friday" | uv run src/backend/main.py >> "$OUTPUT_FILE"

  # Test X+1: SPY Put Options Chain
  echo "Test X+1: SPY Put Options Chain Expiring this Friday"
  echo "Get the SPY Put Options Chain Expiring this Friday" | uv run src/backend/main.py >> "$OUTPUT_FILE"
  ```

- [ ] Use Serena `search_for_pattern` to locate NVDA Technical Analysis test
- [ ] Use Edit to add 2 NVDA options tests after NVDA TA test:
  ```bash
  # Test Y: NVDA Call Options Chain
  echo "Test Y: NVDA Call Options Chain Expiring this Friday"
  echo "Get the NVDA Call Options Chain Expiring this Friday" | uv run src/backend/main.py >> "$OUTPUT_FILE"

  # Test Y+1: NVDA Put Options Chain
  echo "Test Y+1: NVDA Put Options Chain Expiring this Friday"
  echo "Get the NVDA Put Options Chain Expiring this Friday" | uv run src/backend/main.py >> "$OUTPUT_FILE"
  ```

- [ ] Use Edit to update test count from 32 to 36 tests
- [ ] Use Edit to update test organization comment:
  ```bash
  # Test Organization: 36 total tests
  # - SPY Test Sequence: Tests 1-15 (15 tests - added 2 options tests)
  # - NVDA Test Sequence: Tests 16-30 (15 tests - added 2 options tests)
  # - Multi-Ticker Test Sequence: Tests 31-36 (6 tests)
  ```

---

### PHASE 4: 🔴 CLI TESTING (MANDATORY)

**🔴 CRITICAL: MUST RUN TESTS BEFORE PROCEEDING TO PHASE 5**

- [ ] Execute test suite: `./test_cli_regression.sh`
- [ ] Verify results:
  - [ ] All 36/36 tests PASS (100% success rate)
  - [ ] Test report generated in `test-reports/`
  - [ ] No errors or failures in output
  - [ ] Session persistence verified
- [ ] **CRITICAL VERIFICATION:** Actually VIEW the test responses for options chain tests
  - [ ] SPY Call Options test shows formatted chain with strike prices
  - [ ] SPY Put Options test shows formatted chain with strike prices
  - [ ] NVDA Call Options test shows formatted chain with strike prices
  - [ ] NVDA Put Options test shows formatted chain with strike prices
  - [ ] All responses show Greeks (delta, gamma, theta, vega)
  - [ ] All values rounded to 2 decimals
  - [ ] Response format matches specification in `new_research_details.md`
- [ ] Show test results to user:
  - [ ] Display test summary output
  - [ ] Show pass/fail counts
  - [ ] Provide test report file path
  - [ ] Show performance metrics (response times)
- [ ] If failures occur:
  - [ ] Analyze failure reasons
  - [ ] Fix code issues
  - [ ] Re-run tests until 100% pass rate achieved

**⚠️ DO NOT PROCEED TO PHASE 5 WITHOUT:**
- ✅ 36/36 tests PASSED
- ✅ Test results shown to user
- ✅ Test report path provided
- ✅ Options chain responses manually verified

---

### PHASE 5: UPDATE SERENA MEMORIES

**Only proceed after Phase 4 tests pass 100%**

- [ ] Use Serena `read_memory` to load `tech_stack.md`
- [ ] Use Serena `write_memory` to update `tech_stack.md`:
  - [ ] Update "Direct API Tools" section:
    - [ ] Change "Polygon Direct API (9 tools)" to "(11 tools)"
    - [ ] Add `get_call_options_chain` to tool list
    - [ ] Add `get_put_options_chain` to tool list
    - [ ] Update total tools from 10 to 12
  - [ ] Add new "Options Chain Tools" subsection:
    ```
    **Options Chain (2 tools - Added Oct 8, 2025):**
    - `get_call_options_chain` - Fetch 10 call option strikes above current price
    - `get_put_options_chain` - Fetch 10 put option strikes below current price
    ```
  - [ ] Update test suite section:
    - [ ] Change test count from 32 to 36
    - [ ] Update organization: SPY 15 + NVDA 15 + Multi 6
    - [ ] Add note about 4 new options chain tests
  - [ ] Update "Recent Updates" section with Oct 8, 2025 entry

---

### PHASE 6: FINAL GIT COMMIT

**🔴 ATOMIC COMMIT WORKFLOW - FOLLOW EXACTLY**

#### Step 1: Complete ALL Work FIRST (DO NOT stage yet)
- [ ] Verify all code changes complete
- [ ] Verify all tests passed
- [ ] Verify all documentation updated
- [ ] Verify all Serena memories updated
- [ ] **DO NOT RUN `git add` YET**

#### Step 2: Review All Changes
- [ ] Run `git status` to see all changed files
- [ ] Run `git diff` to review all changes
- [ ] Verify completeness:
  - [ ] Code: `polygon_tools.py` (2 new tools)
  - [ ] Agent: `agent_service.py` (imports, tools list, instructions)
  - [ ] Tests: `test_cli_regression.sh` (4 new tests, count updates)
  - [ ] Report: Test report file in `test-reports/`
  - [ ] Docs: `CLAUDE.md` (Last Completed Task updated)
  - [ ] Memory: `tech_stack.md` (tool count, test count updated)
  - [ ] Plan: `TODO_task_plan.md` (this file)

#### Step 3: Stage Everything at Once
- [ ] Run `git add -A` (FIRST and ONLY staging command)
- [ ] **This is the FIRST time running `git add`**

#### Step 4: Verify Staging
- [ ] Run `git status`
- [ ] Verify ALL files staged, NOTHING unstaged
- [ ] If anything missing, add it now

#### Step 5: Commit Immediately (within 60 seconds)
- [ ] Run commit command with HEREDOC message:
  ```bash
  git commit -m "$(cat <<'EOF'
  [OPTIONS-CHAIN] Implement Call & Put Options Chain tools with Polygon.io API

  - Create get_call_options_chain tool (10 strikes above current price)
  - Create get_put_options_chain tool (10 strikes below current price)
  - Both tools use Polygon.io list_snapshot_options_chain endpoint
  - Response formatting: Strike prices as keys with Greeks, IV, volume, OI
  - All values rounded to 2 decimals per specification
  - Update agent_service.py: Add imports, tools list, new RULE #9
  - Update tool count from 10 to 12 (1 Finnhub + 11 Polygon)
  - Add 4 new test cases to test_cli_regression.sh:
    - SPY Call Options Chain (Test 14)
    - SPY Put Options Chain (Test 15)
    - NVDA Call Options Chain (Test 27)
    - NVDA Put Options Chain (Test 28)
  - Update test count from 32 to 36 tests
  - Test organization: SPY 15 + NVDA 15 + Multi 6
  - Test results: 36/36 PASSED (100% success rate)
  - Update tech_stack.md: Tool count 10→12, test count 32→36
  - Update CLAUDE.md: Last Completed Task Summary

  Test Results:
  - Total: 36/36 PASSED
  - Success Rate: 100%
  - Average Response Time: X.XXs (EXCELLENT)
  - Test Report: test-reports/test_cli_regression_loopX_YYYY-MM-DD_HH-MM.log
  - Options Chain Verification: All 4 tests show formatted chains with Greeks

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>
  EOF
  )"
  ```

#### Step 6: Push Immediately
- [ ] Run `git push`
- [ ] Verify push successful

---

## 🎯 SUCCESS CRITERIA

**Task is complete when:**
- ✅ Both options chain tools implemented and working
- ✅ Agent service updated with new tools and instructions
- ✅ Test suite updated with 4 new test cases
- ✅ ALL 36/36 tests passing (100% success rate)
- ✅ Test results shown to user
- ✅ Options chain responses manually verified
- ✅ Serena memories updated
- ✅ CLAUDE.md updated with task summary
- ✅ Atomic git commit completed and pushed

---

## 📝 NOTES

- **Tool Pattern:** Follow existing pattern in `polygon_tools.py` (see `get_ta_sma` as reference)
- **Response Format:** Must match specification in `new_research_details.md` exactly
- **Decimal Precision:** All numeric values must be rounded to 2 decimals
- **Error Handling:** Comprehensive try/except with descriptive error JSON
- **Testing:** MANDATORY - cannot skip or claim completion without test execution
- **Commit Workflow:** Stage ONLY immediately before commit, never during development
