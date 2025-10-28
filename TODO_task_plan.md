# TODO Task Plan: AI Agent System Instructions Optimization

## Plan Overview

**Objective:** Implement optimized AI Agent System Instructions with 30-40% token reduction while maintaining 100% regression test coverage (all 37 tests must pass).

**Strategy:** Systematic rule-by-rule consolidation using Sequential-Thinking and Serena tools throughout the entire implementation process.

**Total Phases:** 5 (Research ✅ Complete → Planning → Implementation → Testing → Commit)

---

## Phase 1: Research ✅ COMPLETE

- [x] Read new_research_details.md
- [x] Use Sequential-Thinking to analyze scope
- [x] Locate AI Agent System Instructions file
- [x] Read get_enhanced_agent_instructions function
- [x] Identify redundant/duplicate rules
- [x] Research best practices (OpenAI Agents + 2025 industry)
- [x] Analyze all 13 RULES for consolidation
- [x] Document findings in research_task_plan.md

**Result:** Comprehensive research plan with 30-40% token reduction opportunity identified.

---

## Phase 2: Planning (CURRENT PHASE)

### Checklist

- [x] Delete current TODO_task_plan.md
- [x] Generate granular implementation plan
- [ ] Present plan to user for review and approval
- [ ] Await user approval before proceeding to Phase 3

---

## Phase 3: Implementation 🔴 DO NOT START UNTIL USER APPROVES PLAN 🔴

### Prerequisites
- [ ] User has reviewed and approved this TODO plan
- [ ] User has confirmed understanding of implementation strategy

### 🔴 CRITICAL: MANDATORY TOOL USAGE ENFORCEMENT

**YOU MUST use Sequential-Thinking and Serena tools throughout ENTIRE implementation:**

- **START every implementation step** with Sequential-Thinking for systematic approach
- **Use Serena tools** for code analysis and symbol manipulation
- **Use Sequential-Thinking repeatedly** for complex reasoning and validation
- **NEVER stop using advanced tools** until implementation complete

---

### Step 3.1: Preparation & Backup

#### 3.1.1: Use Sequential-Thinking to plan implementation approach
- [ ] Sequential-Thinking: Analyze implementation strategy
- [ ] Sequential-Thinking: Plan rule-by-rule consolidation sequence
- [ ] Sequential-Thinking: Identify potential issues and mitigations

#### 3.1.2: Create git backup before ANY changes
- [ ] Bash: `git status` - verify clean working directory
- [ ] Bash: `git add -A` - stage any uncommitted work
- [ ] Bash: `git commit -m "[BACKUP] Before AI agent instructions optimization"`
- [ ] Bash: `git log -1` - verify backup commit created

#### 3.1.3: Use Serena tools to analyze current structure
- [ ] Serena: `find_symbol` - locate get_enhanced_agent_instructions function
- [ ] Serena: Read function body with `include_body=true`
- [ ] Sequential-Thinking: Analyze current structure before modifications

---

### Step 3.2: Implement New Rule Structure (9 Rules)

**🔴 CRITICAL: Use Sequential-Thinking at START of EACH rule consolidation**

---

#### 3.2.1: Consolidate RULE #1 (Stock Quotes) - Merges old RULE #1 + #2

**Before Implementation:**
- [ ] Sequential-Thinking: Plan consolidation of old RULE #1 + #2
- [ ] Sequential-Thinking: Validate no functionality will be lost

**Implementation:**
- [ ] Serena: `find_symbol` - locate old RULE #1 section in function
- [ ] Identify lines: Old RULE #1 (~lines 23-68) + Old RULE #2 (~lines 70-105)
- [ ] Replace with new consolidated RULE #1:
  ```markdown
  RULE #1: STOCK QUOTES = USE get_stock_quote()

  When to Use: User requests price, quote, snapshot, or ticker data

  Tool: get_stock_quote(ticker: str)

  Ticker Format:
  - Single ticker: ticker='SPY'
  - Multiple tickers: ticker='SPY,QQQ,IWM' (comma-separated, no spaces)
  - Uses Tradier API (supports native multi-ticker)

  Examples:
  ✅ "NVDA price" → get_stock_quote(ticker='NVDA')
  ✅ "SPY, QQQ prices" → get_stock_quote(ticker='SPY,QQQ')

  Returns: Price, change, %, high, low, open, previous close
  ```

**Validation:**
- [ ] Sequential-Thinking: Verify consolidated rule maintains all logic
- [ ] Check: Single-ticker examples preserved
- [ ] Check: Multi-ticker comma-separated format documented
- [ ] Check: Tradier API mention preserved
- [ ] Lines saved: ~40 lines (80 → 40)

---

#### 3.2.2: Keep RULE #2 (Market Status & Time) - Old RULE #3 unchanged

**Before Implementation:**
- [ ] Sequential-Thinking: Confirm no changes needed to market status rule

**Implementation:**
- [ ] Serena: Locate old RULE #3 section (~lines 107-127)
- [ ] Renumber as RULE #2 (no content changes)
- [ ] Validate tool name: get_market_status_and_date_time()

**Validation:**
- [ ] Sequential-Thinking: Verify rule remains clear and concise
- [ ] Check: Tool name correct
- [ ] Check: Use cases documented
- [ ] Lines: ~20 lines (no change)

---

#### 3.2.3: Consolidate RULE #3 (Historical Price Data) - Merges old RULE #4 + #11

**🔴 MOST SIGNIFICANT CONSOLIDATION - SAVE ~105 LINES**

**Before Implementation:**
- [ ] Sequential-Thinking: Plan consolidation of old RULE #4 + verbose RULE #11
- [ ] Sequential-Thinking: Design concise interval selection table

**Implementation:**
- [ ] Serena: Locate old RULE #4 section (~lines 129-209)
- [ ] Serena: Locate old RULE #11 section (~lines 463-548, 85 verbose lines!)
- [ ] Replace both with new consolidated RULE #3:
  ```markdown
  RULE #3: HISTORICAL PRICE DATA = USE get_stock_price_history()

  Tool: get_stock_price_history(ticker, start_date, end_date, interval)

  Parameters:
  - ticker (str): Stock ticker symbol
  - start_date (str): YYYY-MM-DD format
  - end_date (str): YYYY-MM-DD format
  - interval (str): "daily", "weekly", or "monthly"

  Interval Selection (Pattern Matching):
  | User Query Contains | Interval Value |
  |---------------------|---------------|
  | "week"/"weeks"/"weekly" | "weekly" |
  | "month"/"months"/"monthly" | "monthly" |
  | "day"/"days"/"daily"/"yesterday" | "daily" (default) |

  Date Calculation:
  - Tool auto-adjusts weekend dates to previous Friday
  - Calculate from current date (see datetime context at top)

  Examples:
  ✅ "Last week: SPY" → interval="weekly" (contains "week")
  ✅ "Past 5 days: NVDA" → interval="daily" (contains "days")
  ✅ "Last month: AAPL" → interval="monthly" (contains "month")

  Display: Copy tool response exactly (pre-formatted markdown)
  ```

**Validation:**
- [ ] Sequential-Thinking: Verify interval table covers all test cases
- [ ] Check: Week pattern → weekly (Test 5-7, 19-21, 33-35)
- [ ] Check: Month pattern → monthly (tests covered)
- [ ] Check: Day pattern → daily (default, tests covered)
- [ ] Check: Weekend handling documented
- [ ] Check: Display instruction preserved (table formatting)
- [ ] Lines saved: **~105 lines (165 → 60)**

---

#### 3.2.4: Streamline RULE #4 (Technical Analysis) - Reduces old RULE #7

**Before Implementation:**
- [ ] Sequential-Thinking: Plan reduction of verbose RULE #7
- [ ] Sequential-Thinking: Identify which examples to keep (most essential)

**Implementation:**
- [ ] Serena: Locate old RULE #7 section (~lines 211-331, 120 lines)
- [ ] Reduce examples, keep core logic
- [ ] Replace with streamlined RULE #4:
  ```markdown
  RULE #4: TECHNICAL ANALYSIS

  ACTION 1: GET TA Indicators
  - Tool: get_ta_indicators(ticker)
  - Omit timespan parameter (defaults to 'day')
  - Returns: Pre-formatted markdown table (RSI, MACD, SMA, EMA)
  - Display: Copy table exactly as returned

  ACTION 2: ANALYZE TA Data
  - Use ALL available data (not just TA indicators)
  - Check chat history first for existing data
  - Required topics (4 minimum):
    1. Trends (SMA/EMA analysis)
    2. Volatility (price swings, risk)
    3. Momentum (RSI, MACD interpretation)
    4. Trading Patterns (support/resistance, crossovers)

  Examples:
  ✅ "Get TA for SPY" → get_ta_indicators(ticker='SPY')
  ✅ "Perform TA for SPY" → Holistic analysis with 4 topics
  ```

**Validation:**
- [ ] Sequential-Thinking: Verify ACTION 1 vs ACTION 2 distinction clear
- [ ] Check: GET data logic preserved (Test 10)
- [ ] Check: ANALYZE data logic preserved (Test 12, 24-26)
- [ ] Check: Holistic approach documented (4 topics)
- [ ] Check: Chat history check documented
- [ ] Check: Table display instruction preserved
- [ ] Lines saved: ~40 lines (120 → 80)

---

#### 3.2.5: Consolidate RULE #5 (Options Tools) - Merges old RULE #9 + #10

**Before Implementation:**
- [ ] Sequential-Thinking: Plan consolidation of options tools
- [ ] Sequential-Thinking: Identify shared date handling logic

**Implementation:**
- [ ] Serena: Locate old RULE #9 section (~lines 393-458, 65 lines)
- [ ] Serena: Locate old RULE #10 section (~lines 460-485, 25 lines)
- [ ] Replace both with consolidated RULE #5:
  ```markdown
  RULE #5: OPTIONS TOOLS

  TOOL 1: get_options_chain_both(ticker, current_price, expiration_date)
  - Use for ALL options chain requests (calls, puts, or both)
  - Returns both call and put chains in single response
  - Requires current_price (use get_stock_quote if needed)
  - Date format: YYYY-MM-DD

  TOOL 2: get_options_expiration_dates(ticker)
  - Use when user requests available expiration dates
  - Returns: Array of dates in YYYY-MM-DD format
  - Includes weekly and monthly expirations

  Shared Date Handling:
  - "this Friday" → Calculate next Friday in YYYY-MM-DD
  - "Oct 10" → Convert to YYYY-MM-DD (2025-10-10)

  Examples:
  ✅ "Both chains for SPY" → get_options_chain_both(...)
  ✅ "SPY expiration dates" → get_options_expiration_dates(ticker='SPY')

  Display: Copy tool responses exactly (pre-formatted markdown tables)
  ```

**Validation:**
- [ ] Sequential-Thinking: Verify both tools documented clearly
- [ ] Check: get_options_chain_both primary tool (Test 14, 28)
- [ ] Check: get_options_expiration_dates documented
- [ ] Check: Date handling logic preserved
- [ ] Check: Table display instruction preserved
- [ ] Lines saved: ~20 lines (90 → 70)

---

#### 3.2.6: Consolidate RULE #6 (Chat History & Tool Efficiency) - Merges old RULE #8 + decision tree

**🔴 CRITICAL FOR TEST 11 (Support & Resistance)

**Before Implementation:**
- [ ] Sequential-Thinking: Plan consolidation of chat history logic
- [ ] Sequential-Thinking: Ensure Test 11 scenario explicitly documented

**Implementation:**
- [ ] Serena: Locate old RULE #8 section (~lines 333-403, 70 lines)
- [ ] Serena: Locate final decision tree STEP 0 (~lines 620-650)
- [ ] Replace with consolidated RULE #6:
  ```markdown
  RULE #6: CHAT HISTORY & TOOL EFFICIENCY

  Before ANY tool call:
  1. Review last 5-10 messages in conversation
  2. Identify what data you already have
  3. Determine if existing data is sufficient

  When to SKIP tool calls:
  - Already have relevant data for same ticker(s)
  - User asks follow-up question about existing data
  - Example: Have SPY price/TA → User asks "SPY trend?" → Use existing data
  - 🔴 CRITICAL: Have SPY SMA/EMA/RSI/MACD → User asks "Support & Resistance" → NO NEW CALLS

  When to MAKE new tool calls:
  - No existing data for requested ticker(s)
  - User requests different data type not yet retrieved
  - User explicitly requests "latest"/"current"/"refresh"

  Transparency:
  - When using existing data: "Based on the [data] we already retrieved..."
  - When making new calls: "After retrieving latest data..."

  Examples:
  ✅ Previous: Have SPY price, User: "Is SPY up?" → NO TOOL CALL, use existing
  ✅ Previous: Have SPY price, User: "SPY full TA" → ONLY call get_ta_indicators
  ❌ Previous: Have SPY TA, User: "SPY support/resistance" → NEW TA CALLS [WASTE!]
  ```

**Validation:**
- [ ] Sequential-Thinking: Verify Test 11 scenario explicitly covered
- [ ] Check: "Support & Resistance" example included
- [ ] Check: Chat history review logic preserved
- [ ] Check: When to SKIP vs MAKE logic clear
- [ ] Check: Transparency requirements documented
- [ ] Lines saved: ~40 lines (90 → 50)

---

#### 3.2.7: Consolidate RULE #7 (Error & Data Handling) - Merges old RULE #5 + #6 + #13

**Before Implementation:**
- [ ] Sequential-Thinking: Plan consolidation of error handling rules
- [ ] Sequential-Thinking: Ensure fallback sequence preserved

**Implementation:**
- [ ] Serena: Locate old RULE #5 section (~lines 211-226, 15 lines)
- [ ] Serena: Locate old RULE #6 section (~lines 228-253, 25 lines)
- [ ] Serena: Locate old RULE #13 section (~lines 593-613, 20 lines)
- [ ] Replace all three with consolidated RULE #7:
  ```markdown
  RULE #7: ERROR & DATA HANDLING

  Work with Available Data:
  - ALWAYS use whatever data is returned
  - If request 2 weeks but get 1 week → PROCEED with 1 week
  - NEVER require exact data counts

  Market Closed Fallback Sequence:
  1. Try get_stock_quote (returns last trade when closed)
  2. If fails, try get_stock_price_history for last 5 days
  3. Only after all fallbacks fail, explain limitation

  Error Transparency:
  - ALWAYS report EXACT verbatim error message
  - NEVER use vague phrases: "API Issue", "data unavailable"
  - Include complete error for debugging

  Examples:
  ✅ "API Error: 'str' object has no attribute 'get'" (exact error)
  ❌ "There was an API issue" (too vague)
  ```

**Validation:**
- [ ] Sequential-Thinking: Verify all error handling scenarios covered
- [ ] Check: Work with available data philosophy preserved
- [ ] Check: Market closed fallback sequence documented
- [ ] Check: Error transparency requirement preserved
- [ ] Lines saved: ~25 lines (60 → 35)

---

#### 3.2.8: Keep RULE #8 (Single-Ticker Tool Constraint) - Old RULE #12 unchanged

**Before Implementation:**
- [ ] Sequential-Thinking: Confirm importance of single-ticker constraint

**Implementation:**
- [ ] Serena: Locate old RULE #12 section (~lines 550-570, 20 lines)
- [ ] Renumber as RULE #8 (no content changes)
- [ ] Validate constraint examples preserved

**Validation:**
- [ ] Sequential-Thinking: Verify constraint clear for all tools
- [ ] Check: Tool list documented (get_stock_price_history, get_ta_indicators, etc.)
- [ ] Check: Parallel call pattern documented for multi-ticker
- [ ] Check: Critical for Tests 33-35 (multi-ticker historical)
- [ ] Lines: ~20 lines (no change)

---

#### 3.2.9: Create NEW RULE #9 (Output Formatting) - Extracted from multiple rules

**🔴 NEW RULE - Extract repeated formatting instructions**

**Before Implementation:**
- [ ] Sequential-Thinking: Plan extraction of all formatting instructions
- [ ] Sequential-Thinking: Identify all locations with table preservation logic

**Implementation:**
- [ ] Extract table formatting from old RULE #4, #7, #9
- [ ] Extract emoji guidelines from scattered locations
- [ ] Extract tool transparency from final section
- [ ] Create new consolidated RULE #9:
  ```markdown
  RULE #9: OUTPUT FORMATTING

  Table Preservation (ALL TOOLS):
  - When tool returns markdown table → Copy exactly as returned
  - ❌ DO NOT reformat to bullet points
  - ❌ DO NOT convert to plain text
  - ❌ DO NOT remove headers/rows
  - ✅ Preserve markdown syntax with pipe separators (|)
  - Applies to: Options chains, price history, TA indicators, any tool-generated table

  Lists vs Tables Decision:
  - Use lists (bullets/numbered): Simple responses, 1-5 items, single ticker
  - Use tables: Complex data, 6+ items, multi-ticker comparisons, OHLC bars

  Emoji Usage:
  - Financial: 📊 (data), 📈 (bullish), 📉 (bearish), 💹 (financial)
  - Status: ✅ (positive), ⚠️ (caution), 🔴 (critical), 🟢 (good)
  - Use sparingly: 2-5 emojis per response max

  Tool Call Transparency:
  - END of EVERY response: List tools used with reasoning
  - If no tool calls: "No tool calls needed - using existing data from previous queries"

  Format:
  ---
  **Tools Used:**
  - `tool_name(parameters)` - Reasoning for selection
  ```

**Validation:**
- [ ] Sequential-Thinking: Verify all formatting guidelines consolidated
- [ ] Check: Table preservation rule applies to ALL tools
- [ ] Check: Lists vs tables logic clear
- [ ] Check: Emoji guidelines concise
- [ ] Check: Tool transparency requirement documented
- [ ] Lines saved: ~35 lines (consolidates 85 lines scattered → 50 lines)

---

### Step 3.3: Remove Redundant Sections

**Before Implementation:**
- [ ] Sequential-Thinking: Identify all redundant sections to remove

**Implementation:**
- [ ] Serena: Locate and remove old final decision tree (redundant with RULE #6)
- [ ] Serena: Remove redundant formatting sections (now in RULE #9)
- [ ] Serena: Remove verbose emoji sections (consolidated in RULE #9)

**Validation:**
- [ ] Sequential-Thinking: Verify no functionality lost by removing redundant sections
- [ ] Check: All decision logic preserved in RULE #6
- [ ] Check: All formatting logic preserved in RULE #9

---

### Step 3.4: Final Structure Validation

**Before Validation:**
- [ ] Sequential-Thinking: Plan comprehensive validation strategy
- [ ] Sequential-Thinking: Prepare test scenarios for manual CLI testing

**Validation:**
- [ ] Serena: `find_symbol` - read complete updated function
- [ ] Count total lines: Target ~400-450 lines (from 657)
- [ ] Verify all 9 RULES present and correctly numbered
- [ ] Verify no duplicate formatting instructions
- [ ] Verify datetime context preserved at top
- [ ] Verify function structure intact (def, docstring, return)

**Line Count Validation:**
- [ ] Old structure: 657 lines
- [ ] New structure: ~425 lines
- [ ] Reduction: ~230 lines (35%)
- [ ] Sequential-Thinking: Verify reduction meets 30-40% target

---

### Step 3.5: Manual CLI Testing (Before Regression Suite)

**🔴 CRITICAL: MUST PASS BEFORE PROCEEDING TO PHASE 4**

**Strategy:** Test 1-2 prompts per rule to validate agent understands new structure

**Before Testing:**
- [ ] Sequential-Thinking: Plan manual test prompts covering all 9 rules
- [ ] Sequential-Thinking: Define pass criteria for each test

**Test Execution:**

#### Test Set 1: RULE #1 (Stock Quotes)
- [ ] Test Prompt 1.1: "Stock Snapshot: SPY"
  - Expected: get_stock_quote(ticker='SPY')
  - Validation: Single ticker handled correctly
- [ ] Test Prompt 1.2: "Prices for AAPL, MSFT, GOOGL"
  - Expected: get_stock_quote(ticker='AAPL,MSFT,GOOGL')
  - Validation: Multi-ticker comma-separated format used

#### Test Set 2: RULE #2 (Market Status)
- [ ] Test Prompt 2.1: "Is the market open?"
  - Expected: get_market_status_and_date_time()
  - Validation: Correct tool called

#### Test Set 3: RULE #3 (Historical Price Data)
- [ ] Test Prompt 3.1: "Last week's Performance OHLC: SPY"
  - Expected: interval="weekly" (contains "week")
  - Validation: Interval pattern matching working
- [ ] Test Prompt 3.2: "Stock Price Performance the last 5 Trading Days: NVDA"
  - Expected: interval="daily" (contains "days")
  - Validation: Daily interval selected correctly

#### Test Set 4: RULE #4 (Technical Analysis)
- [ ] Test Prompt 4.1: "Get technical analysis for SPY"
  - Expected: get_ta_indicators(ticker='SPY')
  - Validation: GET action recognized
- [ ] Test Prompt 4.2: "Perform full technical analysis for NVDA"
  - Expected: Holistic analysis with 4 topics (Trends, Volatility, Momentum, Trading Patterns)
  - Validation: ANALYZE action recognized, all 4 topics covered

#### Test Set 5: RULE #5 (Options Tools)
- [ ] Test Prompt 5.1: "Get both Call and Put Options Chains Expiring this Friday: SPY"
  - Expected: get_options_chain_both(ticker='SPY', current_price=..., expiration_date='...')
  - Validation: Correct tool used, both chains returned

#### Test Set 6: RULE #6 (Chat History & Tool Efficiency)
- [ ] Test Prompt 6.1: First query: "Get TA for SPY", Second query: "What's SPY trend?"
  - Expected: Second query uses existing TA data, NO new tool calls
  - Validation: Chat history reuse working
- [ ] Test Prompt 6.2: First query: "SPY price and TA", Second query: "Support & Resistance Levels: SPY"
  - Expected: Second query uses existing data, NO new TA calls
  - Validation: **CRITICAL TEST 11 scenario - must NOT make redundant calls**

#### Test Set 7: RULE #7 (Error & Data Handling)
- [ ] Test Prompt 7.1: "NVDA price" (when market closed)
  - Expected: Uses fallback sequence, provides last available price
  - Validation: No refusal, fallback working

#### Test Set 8: RULE #8 (Single-Ticker Constraint)
- [ ] Test Prompt 8.1: "Last week's Performance OHLC: WDC, AMD, SOUN"
  - Expected: 3 parallel calls to get_stock_price_history (one per ticker)
  - Validation: Parallel calls for multi-ticker historical data

#### Test Set 9: RULE #9 (Output Formatting)
- [ ] Test Prompt 9.1: Any options chain query
  - Expected: Markdown table preserved exactly as returned
  - Validation: Table NOT reformatted to bullets
- [ ] Test Prompt 9.2: Any query
  - Expected: "Tools Used:" section at end with reasoning
  - Validation: Tool transparency working

**Manual Testing Validation:**
- [ ] Sequential-Thinking: Analyze all manual test results
- [ ] All tests passed: Proceed to Phase 4 (Regression Testing)
- [ ] Any test failed: Fix issue, re-run failed test, repeat until all pass
- [ ] Sequential-Thinking: Document any issues discovered and fixes applied

**🔴 GATE: DO NOT PROCEED TO PHASE 4 UNTIL ALL MANUAL TESTS PASS**

---

## Phase 4: Regression Testing 🔴 MANDATORY CHECKPOINT

### 🔴 CRITICAL: TWO-PHASE TESTING WORKFLOW

**Phase 4 enforces the mandatory testing workflow from CLAUDE.md:**
1. **Phase 1:** Automated response generation (test suite execution)
2. **Phase 2:** Manual verification of EACH test response (correctness validation)

---

### Step 4.1: Phase 1 - Automated Response Generation

**Before Execution:**
- [ ] Sequential-Thinking: Plan regression testing strategy
- [ ] Sequential-Thinking: Review test suite to understand all 37 test scenarios

**Execution:**
- [ ] Bash: `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
- [ ] Wait for completion: All 37 tests execute in persistent session
- [ ] Save test report path (e.g., `test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log`)

**Phase 1 Validation:**
- [ ] Test suite completed: X/37 tests received responses
- [ ] Test report generated successfully
- [ ] No script errors or crashes
- [ ] Session persistence verified (single session for all tests)

**Phase 1 Deliverables:**
- [ ] Test completion count: ___/37 COMPLETED
- [ ] Test report path: test-reports/test_cli_regression_loop1___________.log
- [ ] Min response time: ___s
- [ ] Max response time: ___s
- [ ] Average response time: ___s

**🔴 LIMITATION:** Phase 1 script CANNOT validate response correctness - only confirms responses received

---

### Step 4.2: Phase 2 - Manual Verification of ALL 37 Tests

**🔴 CRITICAL: You MUST manually review EACH of the 37 test responses**

**Why Grep is INSUFFICIENT:**
- ❌ Misses duplicate/unnecessary tool calls (agent calling same tool twice)
- ❌ Misses wrong tool selection (agent calling wrong API for data)
- ❌ Misses data inconsistencies (cross-ticker contamination, wrong data)
- ❌ Only catches explicit error messages, not logic errors

**MANDATORY Process for EACH of the 37 Tests:**

#### Step 2A: Read Test Response Using Read Tool
- [ ] Use `Read` tool to read test log file section for each test
- [ ] Read lines corresponding to test's Agent Response, Tools Used, Performance Metrics
- [ ] **NO scripts, NO grep shortcuts - READ each test manually**

#### Step 2B: Apply 4-Point Verification Criteria (PER TEST)

**For EACH test, verify ALL 4 criteria:**

1. **✅ Does the response address the query?**
   - [ ] Agent's response directly answers test prompt
   - [ ] Response relevant to ticker(s) mentioned
   - [ ] Response complete (not truncated)

2. **✅ Were the RIGHT tools called (not duplicate/unnecessary calls)?**
   - [ ] **Check conversation context**: If previous test already retrieved data, agent should NOT call same tool again
   - [ ] Tools appropriate for query (Tradier for quotes, Polygon for TA)
   - [ ] No redundant API calls

3. **✅ Is the data correct?**
   - [ ] Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
   - [ ] Data formatting matches expected format (OHLC, tables, etc.)
   - [ ] No hallucinated data or made-up values
   - [ ] No cross-ticker contamination (NVDA query shouldn't return SPY data)
   - [ ] Options chains show Bid/Ask columns (NOT midpoint)

4. **✅ Are there any errors?**
   - [ ] No error messages in response
   - [ ] No "data unavailable" messages
   - [ ] No RuntimeWarnings
   - [ ] No API errors

#### Step 2C: Document Each Test Result

**Create verification table for ALL 37 tests:**

| Test # | Test Name | Status | Issue (if failed) | Failure Type |
|--------|-----------|--------|-------------------|--------------|
| 1 | Market_Status | PASS/FAIL | - | - |
| 2 | SPY_Price | PASS/FAIL | - | - |
| ... | ... | ... | ... | ... |
| 37 | ... | PASS/FAIL | - | - |

**Failure Types:**
- Code Error: Syntax/runtime errors, import errors
- Logic Error (Duplicate Tool Call): Unnecessary redundant API calls
- Logic Error (Wrong Tool): Agent called wrong tool for query
- Data Error: Wrong data returned, cross-ticker contamination
- Response Error: Incomplete response, doesn't address query

#### Step 2D: Critical Tests to Verify (High Priority)

**MUST verify these tests explicitly:**

- [ ] **Test 1:** Market Status
  - Tool: get_market_status_and_date_time()
  - Validation: Market status returned, date/time included

- [ ] **Test 2:** Stock Snapshot: SPY
  - Tool: get_stock_quote(ticker='SPY')
  - Validation: Single ticker format, price data returned

- [ ] **Test 5-7:** Daily/Weekly intervals
  - Tool: get_stock_price_history(..., interval='daily'/'weekly')
  - Validation: Correct interval based on query pattern

- [ ] **Test 10:** Get TA Indicators: SPY
  - Tool: get_ta_indicators(ticker='SPY')
  - Validation: TA table returned, NOT reformatted

- [ ] **Test 11:** Support & Resistance Levels: SPY
  - **CRITICAL:** Should NOT make new TA calls if already have SPY SMA/EMA/RSI/MACD
  - Validation: Uses existing data, NO redundant calls

- [ ] **Test 12:** Perform Full TA: SPY
  - Tools: Check if get_ta_indicators needed OR uses existing data
  - Validation: Holistic analysis with 4 topics (Trends, Volatility, Momentum, Trading Patterns)

- [ ] **Test 14:** Both Call and Put Options Chains: SPY
  - Tool: get_options_chain_both(ticker='SPY', ...)
  - Validation: Both call and put tables returned

- [ ] **Test 16:** Stock Snapshot: NVDA
  - Tool: get_stock_quote(ticker='NVDA')
  - Validation: Single ticker format

- [ ] **Test 19-21:** More interval tests
  - Validation: Correct interval pattern matching

- [ ] **Test 28:** Both Call and Put Options Chains: NVDA
  - Tool: get_options_chain_both(ticker='NVDA', ...)
  - Validation: Both call and put tables returned

- [ ] **Test 33-35:** Multi-ticker historical data
  - Tools: Parallel calls to get_stock_price_history (one per ticker)
  - Validation: Single-ticker constraint respected

#### Step 2E: Verification Summary

**After reviewing ALL 37 tests, document:**

- [ ] Total tests PASSED: ___/37
- [ ] Total tests FAILED: ___/37
- [ ] Pass rate: ___%

**If ANY tests failed:**
- [ ] Document ALL failures in table with test #, issue, and failure type
- [ ] Analyze root cause (rule unclear? logic missing? example needed?)
- [ ] Fix issues in agent instructions
- [ ] Re-run FULL test suite (Phase 1 + Phase 2)
- [ ] Repeat until 100% pass rate

**🔴 GATE: CANNOT PROCEED TO PHASE 5 WITHOUT 100% PASS RATE**

---

### Step 4.3: Final Checkpoint Questions

**Answer ALL checkpoint questions with evidence:**

1. **✅ Did you READ all 37 test responses manually using the Read tool?**
   - [ ] YES / NO
   - Evidence: ___

2. **✅ Did you apply all 4 verification criteria to EACH test?**
   - [ ] YES / NO
   - Evidence: ___

3. **✅ How many tests PASSED all 4 criteria?**
   - [ ] ___/37 PASSED

4. **✅ How many tests FAILED (any criterion)?**
   - [ ] ___/37 FAILED

5. **✅ Did you document ALL failures with test #, issue, and failure type?**
   - [ ] YES / NO + TABLE ATTACHED

**🔴 CANNOT MARK TASK COMPLETE WITHOUT:**
- Reading all 37 test responses manually (using Read tool, NOT grep)
- Applying all 4 verification criteria to each test
- Documenting ALL 37 tests in results table
- Providing failure count and failure details table
- Answering all 5 checkpoint questions with evidence

---

## Phase 5: Final Git Commit 🔴 PROPER ATOMIC COMMIT WORKFLOW

### 🔴 CRITICAL: Stage ONLY Immediately Before Commit

**CORRECT Workflow (follow EXACTLY):**

---

### Step 5.1: Complete ALL Work FIRST (DO NOT stage anything yet)

**Before ANY staging:**
- [ ] Sequential-Thinking: Verify ALL work complete before staging
- [ ] ALL code changes complete (agent_service.py modified)
- [ ] ALL tests passing (37/37 with Phase 2 verification complete)
- [ ] ALL documentation updated (see Step 5.2)
- [ ] NO `git add` commands run yet

---

### Step 5.2: Update ALL Documentation

**Update CLAUDE.md:**
- [ ] Sequential-Thinking: Plan CLAUDE.md updates
- [ ] Update "Last Completed Task Summary" section with optimization details
- [ ] Include before/after line counts (657 → ~425 lines)
- [ ] Include token reduction (30-40%, ~230 lines saved)
- [ ] Include test results (37/37 PASSED)
- [ ] Include rule consolidation summary (13 → 9 RULES)
- [ ] Include key optimizations applied

**Example CLAUDE.md update:**
```markdown
<!-- LAST_COMPLETED_TASK_START -->
[OPTIMIZE_AI_AGENT_INSTRUCTIONS] AI Agent System Instructions Optimization - 35% Token Reduction

**Summary:** Successfully optimized AI Agent System Instructions from 657 lines to ~425 lines (35% reduction) while maintaining 100% regression test coverage. Consolidated 13 RULES into 9 well-organized rules, removing verbose examples and redundant formatting instructions. All 37 regression tests passed with Phase 2 manual verification complete.

**Optimization Details:**
- **Before:** 657 lines, 13 RULES, ~8,000-10,000 tokens
- **After:** ~425 lines, 9 RULES, ~5,500-6,500 tokens
- **Reduction:** 230 lines (35%), ~2,500-3,500 tokens saved

**Major Consolidations:**
1. RULE #1 + #2 → Stock Quotes (single rule, -40 lines)
2. RULE #4 + #11 → Historical Price Data with interval table (-105 lines)
3. RULE #9 + #10 → Options Tools (-20 lines)
4. RULE #5 + #6 + #13 → Error & Data Handling (-25 lines)
5. NEW RULE #9: Output Formatting (extracted from multiple rules, -35 lines)

**Testing Results:**
- ✅ Phase 1: 37/37 automated tests completed
- ✅ Phase 2: Manual verification of all 37 test responses (100% pass rate)
- ✅ Average response time: X.XXs
- ✅ Test report: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log

**Files Modified:**
- ✅ src/backend/services/agent_service.py (get_enhanced_agent_instructions function optimized)
- ✅ CLAUDE.md (this summary)
- ✅ research_task_plan.md (comprehensive research findings)
- ✅ TODO_task_plan.md (granular implementation plan)

**Code Quality:**
- ✅ No syntax errors
- ✅ No functionality lost
- ✅ Better organization improves agent understanding
- ✅ 35% token reduction = significant cost savings at scale

**Performance Impact:**
- Per test run: 111,000 input tokens saved (37 queries × 3,000 tokens)
- Production (1,000 daily queries): 3,000,000 tokens saved per day
<!-- LAST_COMPLETED_TASK_END -->
```

---

### Step 5.3: Verify EVERYTHING Complete

**Before staging:**
- [ ] Sequential-Thinking: Comprehensive review of all changes
- [ ] Bash: `git status` - review ALL changed/new files
- [ ] Bash: `git diff src/backend/services/agent_service.py` - review code changes
- [ ] Bash: `git diff CLAUDE.md` - review documentation updates
- [ ] Verify test report file exists: test-reports/test_cli_regression_loop1_*.log
- [ ] Verify all work done, nothing left pending

**Files to commit (checklist):**
- [ ] src/backend/services/agent_service.py (optimized instructions)
- [ ] CLAUDE.md (last completed task summary)
- [ ] research_task_plan.md (research findings)
- [ ] TODO_task_plan.md (this implementation plan)
- [ ] test-reports/test_cli_regression_loop1_*.log (test evidence)

---

### Step 5.4: Stage EVERYTHING AT ONCE

**🔴 CRITICAL: This is the FIRST time you run `git add`**

- [ ] Bash: `git add -A` - stage ALL files in ONE command
- [ ] **Verify this is the FIRST `git add` of this task**

---

### Step 5.5: Verify Staging IMMEDIATELY

**Immediately after staging:**
- [ ] Bash: `git status` - verify ALL files staged, NOTHING unstaged
- [ ] Check: src/backend/services/agent_service.py staged
- [ ] Check: CLAUDE.md staged
- [ ] Check: research_task_plan.md staged
- [ ] Check: TODO_task_plan.md staged
- [ ] Check: test-reports/*.log staged
- [ ] If anything missing: `git add [missing-file]`

---

### Step 5.6: Commit IMMEDIATELY (within 60 seconds of staging)

**Commit message template:**
```bash
git commit -m "$(cat <<'EOF'
[OPTIMIZE_AI_AGENT_INSTRUCTIONS] AI Agent System Instructions Optimization - 35% Token Reduction

- Consolidated 13 RULES into 9 well-organized rules (~425 lines from 657)
- Merged RULE #1 + #2 → Stock Quotes (single rule)
- Merged RULE #4 + #11 → Historical Price Data with concise interval table
- Merged RULE #9 + #10 → Options Tools (shared date handling)
- Merged RULE #5 + #6 + #13 → Error & Data Handling
- Created NEW RULE #9: Output Formatting (extracted from multiple rules)
- Removed verbose examples (kept 2-3 essential per rule)
- Eliminated redundant formatting instructions across rules
- Streamlined Technical Analysis rule (reduced 120 → 80 lines)
- Token reduction: ~230 lines saved (35% reduction, ~2,500-3,500 tokens)

Testing Results:
✅ Manual CLI testing: All 9 rules validated (1-2 prompts per rule)
✅ Phase 1 automated testing: 37/37 tests completed
✅ Phase 2 manual verification: 100% pass rate (all 37 tests reviewed)
✅ Test report: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log
✅ Average response time: X.XXs (EXCELLENT performance)
✅ Critical Test 11 (Support & Resistance) verified: No redundant TA calls

Files Modified:
- src/backend/services/agent_service.py (optimized get_enhanced_agent_instructions)
- CLAUDE.md (last completed task summary)
- research_task_plan.md (comprehensive research findings)
- TODO_task_plan.md (granular implementation plan)
- test-reports/test_cli_regression_loop1_*.log (test evidence)

Code Quality:
✅ No functionality lost (all 37 tests pass)
✅ Better organization improves agent clarity
✅ Significant cost savings at scale (3M tokens/day for 1k queries)
✅ Follows 2025 best practices for prompt optimization

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Execute commit:**
- [ ] Bash: Run commit command with template above
- [ ] Replace YYYY-MM-DD_HH-MM with actual test report timestamp
- [ ] Replace X.XXs with actual average response time
- [ ] Sequential-Thinking: Verify commit message accurate and complete

---

### Step 5.7: Verify Commit Created

**Immediately after commit:**
- [ ] Bash: `git log -1` - verify commit created with correct message
- [ ] Bash: `git show --stat` - verify all expected files in commit
- [ ] Sequential-Thinking: Review commit to ensure completeness

---

### Step 5.8: Push IMMEDIATELY

**Push to remote:**
- [ ] Bash: `git push`
- [ ] Verify push successful (no errors)
- [ ] Sequential-Thinking: Confirm task completion

---

## What Belongs in Atomic Commit

**✅ MUST INCLUDE:**
- ✅ Code changes (src/backend/services/agent_service.py)
- ✅ Test reports (test-reports/*.log - evidence of passing tests)
- ✅ Documentation updates (CLAUDE.md, research_task_plan.md, TODO_task_plan.md)

**❌ NEVER DO THIS:**
- ❌ Stage files early during development
- ❌ Stage files "as you go"
- ❌ Run `git add` before ALL work is complete
- ❌ Delay between `git add` and `git commit`
- ❌ Commit without test reports
- ❌ Commit without documentation updates

---

## Final Task Completion Checklist

### Research Phase ✅
- [x] Research complete
- [x] research_task_plan.md created

### Planning Phase
- [x] TODO_task_plan.md created
- [ ] Plan presented to user for review
- [ ] User approval received

### Implementation Phase (Pending User Approval)
- [ ] All 9 RULES implemented
- [ ] Redundant sections removed
- [ ] Manual CLI testing complete (all tests passed)

### Testing Phase (Pending User Approval)
- [ ] Phase 1: Test suite executed (37/37 completed)
- [ ] Phase 2: Manual verification (100% pass rate, all 37 tests reviewed)
- [ ] Test report generated
- [ ] All checkpoint questions answered

### Commit Phase (Pending User Approval)
- [ ] ALL work complete (code + tests + docs)
- [ ] git status reviewed
- [ ] git add -A (FIRST and ONLY staging)
- [ ] git status verified (all staged)
- [ ] git commit with proper message
- [ ] git push successful

---

## Success Criteria Summary

**✅ Task complete when:**
1. AI Agent System Instructions optimized (657 → ~425 lines, 35% reduction)
2. All 9 consolidated RULES implemented correctly
3. Manual CLI testing passed (1-2 prompts per rule, all working)
4. Phase 1 automated testing: 37/37 tests completed
5. Phase 2 manual verification: 100% pass rate (all 37 tests reviewed with 4-point criteria)
6. All 5 checkpoint questions answered with evidence
7. Documentation updated (CLAUDE.md, research_task_plan.md, TODO_task_plan.md)
8. Atomic git commit created with all changes
9. Changes pushed to remote repository

**Token Savings Achieved:** ~2,500-3,500 tokens per query (35% reduction)
**Functionality Preserved:** 100% (all 37 tests pass)
**Organization Improved:** 13 → 9 well-structured rules

---

## Risk Mitigation Summary

**Risk Level:** LOW

**Mitigations Applied:**
1. ✅ Comprehensive research phase before implementation
2. ✅ Manual CLI testing before regression suite
3. ✅ Phase 2 manual verification (not just automated)
4. ✅ Sequential-Thinking used throughout for systematic approach
5. ✅ Serena tools used for precise code manipulation
6. ✅ Git backup created before any changes
7. ✅ Rollback plan defined (revert to backup commit if >5 tests fail)

**Rollback Plan:**
- If >3 tests fail in manual CLI testing → investigate and fix before regression suite
- If >5 tests fail in regression suite → rollback to backup commit and re-analyze
- Backup commit: `[BACKUP] Before AI agent instructions optimization`

---

## End of TODO Task Plan

**Next Action:** Present this plan to user for review and approval before proceeding to Phase 3 (Implementation).

🔴 **DO NOT START IMPLEMENTATION UNTIL USER APPROVES THIS PLAN** 🔴
