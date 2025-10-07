# TODO Task Plan: Dynamic Parallel Tool Calls & Chat History Analysis

**Task ID**: Implement Dynamic Parallel Tool Calls with Max 3x Limit + Chat History-Based Tool Call Decisions
**Created**: 2025-10-07
**Status**: PLANNING COMPLETE - READY FOR AUTONOMOUS IMPLEMENTATION

---

## 🎯 TASK OBJECTIVE

Implement three major enhancements to the AI Agent system:

**A. Dynamic Parallel Tool Calls with 3x Max Limit**
- Update AI Agent Instructions to allow max 3 parallel tool calls per batch
- Agent must analyze request complexity to decide if parallel calls needed
- If >3 parallel calls needed, batch them (first 3, then next batch)
- Single ticker = 1 call (no parallel needed)

**B. Chat History-Based Tool Call Decisions**
- Agent must check existing chat data BEFORE making tool calls
- Avoid redundant calls when data already exists in conversation
- Mimics real chatbot behavior - using context intelligently
- Example: If SPY data already retrieved, use it for follow-up SPY questions

**C. New Test Script with 65 Tests + Improved Timestamp Format**
- Create new `test_cli_regression.sh` (current script becomes backup)
- 65 sequential tests organized by ticker (SPY, NVDA, WDC, multi-ticker)
- New timestamp format: `YYYY-MM-DD_HH-MM` (no seconds)
- Update current `CLI_test_regression.sh` with new timestamp format too

---

## 📊 RESEARCH FINDINGS SUMMARY

### Current Implementation Analysis

**1. Agent Instructions (`agent_service.py`):**
- **RULE #2** (lines 47-54): Currently says "USE PARALLEL get_stock_quote() CALLS" with NO LIMIT
- No logic for analyzing chat history before making tool calls
- Instructions emphasize "minimal tool calls" but don't check existing data
- No batching logic for >3 parallel calls

**2. OpenAI Agents SDK Parallel Execution:**
- SDK has **NO built-in mechanism** to limit parallel tool calls
- LLM decides how many parallel calls based on **agent instructions**
- Solution: Control via INSTRUCTIONS, not SDK configuration
- Agent instruction-following behavior will enforce limits

**3. Current Test Script (`CLI_test_regression.sh`):**
- 27 tests total (single focus per test)
- Timestamp format: `YYYYMMDD_HHMMSS` (e.g., "20251006_123556")
- Tests are scattered - no sequential ticker patterns
- Doesn't test data reuse scenarios

**4. New Test Requirements:**
- 65 tests organized sequentially by ticker
- Tests 1-17: All SPY queries (tests data reuse within same ticker)
- Tests 18-34: All NVDA queries
- Tests 35-51: All WDC queries
- Tests 52-65: Multi-ticker queries (AMD, INTC, AVGO)
- Perfect for testing: (1) parallel call patterns, (2) chat history analysis

### Key Insights

**Parallel Call Limiting:**
- Cannot be done via SDK configuration
- Must be enforced through agent INSTRUCTIONS
- Agent must analyze request and decide on batching strategy

**Chat History Analysis:**
- Agent instructions must include explicit logic to check existing data
- Pattern: "Before making tool calls, analyze chat history for relevant data"
- Example: "If user asks for SPY analysis and you already have SPY price/TA data from earlier in conversation, use existing data instead of making new tool calls"

**Test Design Intelligence:**
- Sequential ticker tests allow agent to accumulate data
- Test #2 (SPY current price) → Test #3 (SPY closing price) can reuse data
- Multi-ticker tests validate batching logic (>3 tickers = multiple batches)

---

## 📋 IMPLEMENTATION CHECKLIST

### ✅ PHASE 0: RESEARCH & PLANNING (COMPLETED)

- [x] Complete Sequential-Thinking analysis of requirements
- [x] Research OpenAI Agents SDK parallel execution behavior
- [x] Analyze current agent_service.py instruction structure
- [x] Analyze current CLI_test_regression.sh architecture
- [x] Map all files requiring updates
- [x] Create comprehensive TODO_task_plan.md

---

### 🔧 PHASE 1: AGENT INSTRUCTIONS UPDATE (USE SERENA TOOLS)

#### 1.1 Update RULE #2 - Add Parallel Call Limits

**File**: `src/backend/services/agent_service.py`
**Target**: `get_enhanced_agent_instructions()` function, RULE #2 section (lines 47-54)

- [ ] **Use Sequential-Thinking** to design new RULE #2 with 3x limit logic
- [ ] **Use Serena find_symbol** to locate `get_enhanced_agent_instructions` function
- [ ] **Use Serena find_symbol** with depth=1 to view function structure
- [ ] **Use Serena replace_lines** to update RULE #2 section

**NEW RULE #2 Content** (replace lines 47-54):

```
RULE #2: MULTIPLE TICKERS = DYNAMIC PARALLEL TOOL CALLS (MAX 3 PER BATCH)
- **ANALYZE REQUEST COMPLEXITY FIRST**: Count ticker symbols and assess if parallel calls needed
- **Single Ticker (count = 1)**: Use get_stock_quote(ticker='SYMBOL') - NO PARALLEL NEEDED
- **Multiple Tickers (count = 2-3)**: Make PARALLEL calls up to MAX 3 at once
  - Examples: "SPY, QQQ prices" → 2 parallel calls
  - Examples: "NVDA, AMD, INTC" → 3 parallel calls (max reached)
- **Many Tickers (count > 3)**: BATCH into groups of 3
  - Example: "AMD, INTC, AVGO, NVDA, TSLA" (5 tickers) → First batch: 3 parallel calls (AMD, INTC, AVGO), Second batch: 2 parallel calls (NVDA, TSLA)
  - **IMPORTANT**: Make first 3 parallel calls, analyze results, then make remaining calls
- 🔴 **RATE LIMITING PROTECTION**: Max 3 parallel calls prevents API rate limiting
- 📊 Uses Finnhub API (fast, low overhead - parallel calls acceptable within limit)
- ✅ OpenAI Agents SDK executes tool calls in PARALLEL automatically (up to your specified limit)
- 🔴 **CRITICAL**: Each get_stock_quote call is INDEPENDENT - make up to 3 at once, not sequentially
- ✅ Returns: Individual quote data for each ticker with current price, change, percent change
```

**Success Criteria**:
- RULE #2 includes max 3 parallel call limit
- Batching logic clearly explained
- Examples show 2-ticker, 3-ticker, and >3-ticker scenarios

#### 1.2 Add NEW RULE #9 - Chat History Analysis for Tool Call Decisions

**File**: `src/backend/services/agent_service.py`
**Target**: After RULE #8 (Technical Analysis), insert NEW RULE #9

- [ ] **Use Sequential-Thinking** to design RULE #9 logic
- [ ] **Use Serena find_symbol** to locate end of RULE #8 section
- [ ] **Use Serena insert_after_symbol** OR **replace_lines** to add NEW RULE #9

**NEW RULE #9 Content** (insert after RULE #8, before DECISION TREE section):

```

RULE #9: ANALYZE CHAT HISTORY BEFORE MAKING TOOL CALLS - AVOID REDUNDANT CALLS
- 🔴 **CRITICAL**: BEFORE making ANY tool call, analyze conversation history for existing data
- 🔴 **CHECK EXISTING DATA**: If you already have relevant data from previous tool calls in THIS conversation, USE IT
- ✅ **WHEN TO SKIP TOOL CALLS**:
  - User asks follow-up questions about same ticker you already have data for
  - Example: Already retrieved SPY price/volume → User asks "analyze SPY" → Use existing data, NO new calls
  - Example: Already have NVDA technical analysis data → User asks "what's NVDA trend?" → Use existing data
  - Example: Already fetched AAPL OHLC bars → User asks "AAPL price movement?" → Use existing data
- ✅ **WHEN TO MAKE NEW TOOL CALLS**:
  - No existing data for the requested ticker(s)
  - User asks for different type of data not yet retrieved (e.g., have price but need options data)
  - User explicitly requests "latest" or "current" or "refresh" data
  - Conversation context suggests stale data (e.g., "what's the price NOW after that news?")
- 🔴 **ANALYSIS PATTERN**:
  1. Review last 5-10 messages in conversation
  2. Identify what data you already have (prices, TA indicators, OHLC bars, options, etc.)
  3. Determine if existing data sufficient to answer current question
  4. If sufficient → Use existing data, explain what data you're using
  5. If insufficient → Make minimal tool calls for only missing data
- 📊 **BENEFITS**: Reduces API calls, faster responses, efficient token usage, mimics real chatbot behavior
- ✅ **TRANSPARENCY**: When using existing data, mention it: "Based on the [PRICE DATA/TA ANALYSIS] we already retrieved..."

**EXAMPLES OF CORRECT CHAT HISTORY ANALYSIS**:
✅ **Scenario 1 - Data Reuse**:
  - Previous: User asked "SPY price", Agent called get_stock_quote(ticker='SPY'), got $585.23
  - Current: User asks "Is SPY up or down today?"
  - **CORRECT ACTION**: Use existing SPY data from chat, NO new tool call
  - Response: "Based on the SPY data we already retrieved, SPY is at $585.23, up $2.15 (+0.37%) today."

✅ **Scenario 2 - Partial Data Available**:
  - Previous: Agent has SPY price ($585.23) from earlier
  - Current: User asks "SPY technical analysis with RSI and MACD"
  - **CORRECT ACTION**: Use existing price, make tool calls ONLY for missing TA indicators
  - Tool Calls: get_ta_rsi(ticker='SPY'), get_ta_macd(ticker='SPY')
  - Response: "Based on our existing SPY price of $585.23, and newly retrieved TA indicators: RSI=67.5 (approaching overbought), MACD=1.23..."

✅ **Scenario 3 - No Existing Data**:
  - Previous: No NVDA data in conversation
  - Current: User asks "NVDA price and volume"
  - **CORRECT ACTION**: Make tool call, no existing data available
  - Tool Call: get_stock_quote(ticker='NVDA')

✅ **Scenario 4 - Explicit Refresh Request**:
  - Previous: Agent has SPY data from 5 minutes ago
  - Current: User asks "What's SPY price NOW?"
  - **CORRECT ACTION**: Make new tool call, user wants current/latest data
  - Tool Call: get_stock_quote(ticker='SPY')

❌ **EXAMPLES OF INCORRECT BEHAVIOR**:
❌ Already have SPY data, user asks "SPY analysis" → Making NEW get_stock_quote call [WASTE! Use existing data]
❌ Have complete NVDA TA data, user asks "Is NVDA overbought?" → Making NEW TA calls [WASTE! Analyze existing data]
❌ User asks about 3 tickers, you have data for 2 → Making calls for ALL 3 [WASTE! Only call for missing 1 ticker]
```

**Success Criteria**:
- RULE #9 clearly explains when to skip tool calls
- Examples cover data reuse, partial data, no data, and refresh scenarios
- Incorrect behavior examples highlight common mistakes

#### 1.3 Update Decision Tree - Add Dynamic Analysis Step

**File**: `src/backend/services/agent_service.py`
**Target**: Decision Tree section (currently lines 126-133)

- [ ] **Use Sequential-Thinking** to design enhanced decision tree
- [ ] **Use Serena replace_lines** to update decision tree section

**NEW Decision Tree** (replace lines 126-133):

```
📋 DYNAMIC DECISION TREE FOR TOOL CALLS:

**STEP 0: ANALYZE CHAT HISTORY (NEW - RULE #9)**
- Review conversation for existing relevant data
- Determine if you already have sufficient data to answer question
- If YES → Skip to Step 5 (use existing data), if NO → Continue to Step 1

**STEP 1: COUNT TICKER SYMBOLS & ASSESS REQUEST COMPLEXITY**
- Count how many ticker symbols in the request
- Determine what data is needed (price, TA, OHLC, options, etc.)
- Check what data you DON'T already have from chat history

**STEP 2: DECIDE ON TOOL CALL STRATEGY**
- If count = 0 tickers (e.g., "market status") → Use get_market_status_and_date_time()
- If count = 1 ticker → Use get_stock_quote(ticker='SYMBOL') - NO PARALLEL NEEDED
- If count = 2-3 tickers → Use PARALLEL calls (max 3) to get_stock_quote()
- If count > 3 tickers → BATCH into groups of 3

**STEP 3: EXECUTE TOOL CALLS (WITH BATCHING IF NEEDED)**
- For ≤3 tickers: Make ALL calls in parallel (one batch)
- For >3 tickers: Make first 3 in parallel, then make next batch of up to 3, etc.
- OpenAI Agents SDK handles parallel execution automatically (up to 3 per batch)

**STEP 4: ANALYZE RESULTS & DETERMINE IF MORE CALLS NEEDED**
- Review tool call results
- Determine if additional data needed
- If yes, make additional calls (batched if >3)

**STEP 5: GENERATE RESPONSE**
- Use combination of existing data + new data (if any new calls made)
- Be transparent about data sources ("Based on existing data..." or "After retrieving latest data...")
```

**Success Criteria**:
- Decision tree starts with chat history analysis (Step 0)
- Batching logic included for >3 tickers
- Dynamic analysis of results before additional calls

#### 1.4 Update INSTRUCTIONS Section - Add Chat History Reminder

**File**: `src/backend/services/agent_service.py`
**Target**: INSTRUCTIONS section (lines 159-172)

- [ ] **Use Serena replace_lines** to update instructions list

**Updated INSTRUCTIONS** (replace lines 159-172):

```
INSTRUCTIONS:
1. **FIRST: ANALYZE CHAT HISTORY** - Review conversation for existing relevant data before making ANY tool calls (RULE #9)
2. Use current date/time above for all analysis
3. COUNT the ticker symbols in the request BEFORE selecting a tool
4. **ASSESS COMPLEXITY**: Determine if parallel calls needed and how many
5. **RESPECT 3X LIMIT**: Max 3 parallel tool calls per batch - batch if >3 tickers needed
6. For multiple tickers ≤3, make PARALLEL get_stock_quote() calls (all at once)
7. For >3 tickers, BATCH into groups of 3 (first 3 parallel, then next batch)
8. NEVER refuse price requests when market is closed - use fallback sequence
9. NEVER say "data unavailable" - ALWAYS use fallback tools
10. ALWAYS validate dates - adjust weekends/holidays to business days
11. ALWAYS work with whatever data is returned - don't require exact amounts
12. Structure responses: Format data in bullet point format with 2 decimal points max
13. Include ticker symbols
14. **Use existing data when available** - only make new calls for missing data
15. Keep responses concise - avoid unnecessary details
16. Do NOT provide analysis/takeaways/recommendations UNLESS SPECIFICALLY REQUESTED
```

**Success Criteria**:
- Chat history analysis is instruction #1 (highest priority)
- 3x parallel limit explicitly mentioned
- Batching instructions included

#### 1.5 Update Examples Section - Show Batching Scenarios

**File**: `src/backend/services/agent_service.py`
**Target**: EXAMPLES OF CORRECT TOOL CALLS section (lines 135-149)

- [ ] **Use Serena replace_lines** to add batching examples

**Additional Examples** (add after existing examples):

```
**BATCHING EXAMPLES (>3 TICKERS):**
✅ "Price check: AMD, INTC, AVGO, NVDA, TSLA" (5 tickers) →
    Batch 1: get_stock_quote(ticker='AMD'), get_stock_quote(ticker='INTC'), get_stock_quote(ticker='AVGO') [3 PARALLEL]
    Batch 2: get_stock_quote(ticker='NVDA'), get_stock_quote(ticker='TSLA') [2 PARALLEL]

✅ "Quotes for AAPL, MSFT, GOOGL, AMZN, META, TSLA, NVDA" (7 tickers) →
    Batch 1: get_stock_quote(ticker='AAPL'), get_stock_quote(ticker='MSFT'), get_stock_quote(ticker='GOOGL') [3 PARALLEL]
    Batch 2: get_stock_quote(ticker='AMZN'), get_stock_quote(ticker='META'), get_stock_quote(ticker='TSLA') [3 PARALLEL]
    Batch 3: get_stock_quote(ticker='NVDA') [1 CALL]

**CHAT HISTORY REUSE EXAMPLES:**
✅ Previous: Retrieved SPY price ($585.23), User asks: "Is SPY bullish?" →
    NO TOOL CALLS - Use existing SPY price data from chat history

✅ Previous: Have NVDA price but no TA data, User asks: "NVDA RSI analysis" →
    ONLY NEW CALL: get_ta_rsi(ticker='NVDA') - Reuse existing price, get only missing TA data
```

**Success Criteria**:
- Batching examples show 5-ticker and 7-ticker scenarios
- Chat history reuse examples demonstrate data reuse logic

---

### 📝 PHASE 2: CREATE NEW TEST SCRIPT `test_cli_regression.sh` (USE STANDARD TOOLS)

#### 2.1 Design New Test Script Structure

- [ ] **Use Sequential-Thinking** to plan new test script architecture
- [ ] **Design decisions**:
  - 65 tests total (vs. current 27)
  - Sequential ticker organization (SPY 1-17, NVDA 18-34, WDC 35-51, multi-ticker 52-65)
  - New timestamp format: `YYYY-MM-DD_HH-MM`
  - Same persistent session model as current script
  - Based on current `CLI_test_regression.sh` template

#### 2.2 Create New Test Prompts Array (65 Tests)

**Test Organization**:

```bash
# SPY Sequence (Tests 1-17): Tests data reuse within same ticker
1.  Market Status
2.  Current Price: SPY
3.  Today's Closing Price: SPY
4.  Previous Closing Price: SPY
5.  Current Weekly Performance Change $ and %: SPY
6.  RSI-14: SPY
7.  MACD: SPY
8.  SMA 20/50/200: SPY
9.  EMA 20/50/200: SPY
10. SMA 5/10: SPY
11. EMA 5/10: SPY
12. Options Quote: SPY 1/16/26 $700 Call
13. Options Quote: SPY 1/16/26 $600 Put
14. Support & Resistance Levels: SPY
15. Technical Analysis: SPY
16. Price on 1/1/25: SPY
17. Daily bars from 1/1/25 - 3/31/25: SPY

# NVDA Sequence (Tests 18-34): Same pattern for NVDA
18. Market Status
19. Current Price: NVDA
20. Today's Closing Price: NVDA
21. Previous Closing Price: NVDA
22. Current Weekly Performance Change $ and %: NVDA
23. RSI-14: NVDA
24. MACD: NVDA
25. SMA 20/50/200: NVDA
26. EMA 20/50/200: NVDA
27. SMA 5/10: NVDA
28. EMA 5/10: NVDA
29. Options Quote: NVDA 1/16/26 $200 Call
30. Options Quote: NVDA 1/16/26 $180 Put
31. Support & Resistance Levels: NVDA
32. Technical Analysis: NVDA
33. Price on 1/1/25: NVDA
34. Daily bars from 1/1/25 - 3/31/25: NVDA

# WDC Sequence (Tests 35-51): Same pattern for WDC
35. Market Status
36. Current Price: WDC
37. Today's Closing Price: WDC
38. Previous Closing Price: WDC
39. Current Weekly Performance Change $ and %: WDC
40. RSI-14: WDC
41. MACD: WDC
42. SMA 20/50/200: WDC
43. EMA 20/50/200: WDC
44. SMA 5/10: WDC
45. EMA 5/10: WDC
46. Options Quote: WDC 1/16/26 $150 Call
47. Options Quote: WDC 1/16/26 $100 Put
48. Support & Resistance Levels: WDC
49. Technical Analysis: WDC
50. Price on 1/1/25: WDC
51. Daily bars from 1/1/25 - 3/31/25: WDC

# Multi-Ticker Sequence (Tests 52-65): Tests parallel calls and batching
52. Current Price: AMD, INTC, AVGO
53. Today's Closing Price: AMD, INTC, AVGO
54. Previous Closing Price: AMD, INTC, AVGO
55. Current Weekly Performance Change $ and %: AMD, INTC, AVGO
56. RSI-14: AMD, INTC, AVGO
57. MACD: AMD, INTC, AVGO
58. SMA 20/50/200: AMD, INTC, AVGO
59. EMA 20/50/200: AMD, INTC, AVGO
60. SMA 5/10: AMD, INTC, AVGO
61. EMA 5/10: AMD, INTC, AVGO
62. Support & Resistance Levels: AMD, INTC, AVGO
63. Technical Analysis: AMD, INTC, AVGO
64. Price on 1/1/25: AMD, INTC, AVGO
65. Daily bars from 1/1/25 - 3/31/25: AMD, INTC, AVGO
```

- [ ] **Create prompts array** with all 65 test prompts
- [ ] **Create test_names array** with descriptive names for each test

**Success Criteria**: Arrays match test structure exactly

#### 2.3 Update Timestamp Format in New Script

- [ ] **Modify timestamp generation** from `YYYYMMDD_HHMMSS` to `YYYY-MM-DD_HH-MM`:

```bash
# OLD FORMAT:
LOOP_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$RESULTS_DIR/test_cli_regression_loop${loop_num}_${LOOP_TIMESTAMP}.txt"

# NEW FORMAT:
LOOP_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
OUTPUT_FILE="$RESULTS_DIR/test_cli_regression_loop${loop_num}_${LOOP_TIMESTAMP}.txt"
```

**Success Criteria**: Timestamp format matches `YYYY-MM-DD_HH-MM` (e.g., `2025-10-07_14-35`)

#### 2.4 Write Complete New Test Script

- [ ] **Use Write tool** to create `/home/anthony/Github/market-parser-polygon-mcp/test_cli_regression.sh`
- [ ] **Base on current CLI_test_regression.sh template**
- [ ] **Modifications**:
  - Update prompts array (65 tests)
  - Update test_names array (65 descriptive names)
  - Update total_tests variable (27 → 65)
  - Update timestamp format
  - Update script header comments
  - Keep all other logic (persistent session, response time tracking, etc.)

**Success Criteria**: New script complete and syntactically correct

#### 2.5 Make New Script Executable

- [ ] **Run**: `chmod +x test_cli_regression.sh`

**Success Criteria**: Script has execute permissions

---

### 🔄 PHASE 3: UPDATE CURRENT SCRIPT `CLI_test_regression.sh` WITH NEW TIMESTAMP FORMAT

#### 3.1 Update Timestamp Format in Current Script

- [ ] **Use Read tool** to load current `CLI_test_regression.sh`
- [ ] **Use Edit tool** to update timestamp format (line 153):

```bash
# CHANGE FROM:
LOOP_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# CHANGE TO:
LOOP_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
```

**Success Criteria**: Current script updated with new timestamp format

---

### 🧪 PHASE 4: VALIDATION WITH NEW TEST SCRIPT - 1X LOOP (MANDATORY - DO NOT SKIP)

#### 4.1 Pre-Test Analysis

- [ ] **Use Sequential-Thinking** to predict expected test behavior
- [ ] **Expected behaviors**:
  - Tests 1-17 (SPY sequence): Agent should START REUSING SPY data after Test #2
  - Tests 18-34 (NVDA sequence): Similar data reuse pattern
  - Tests 35-51 (WDC sequence): Similar data reuse pattern
  - Tests 52-65 (Multi-ticker): Should show 3 parallel calls per ticker (max batch size)
  - Some tests may show NO tool calls if data already exists from earlier tests

#### 4.2 Execute New Test Script (1x Loop)

- [ ] **Run**: `./test_cli_regression.sh`
- [ ] **Monitor execution** for:
  - Parallel call patterns (max 3 per batch)
  - Data reuse behavior (skipped tool calls when data exists)
  - Response times
  - Session persistence

**Success Criteria**: Script completes without hanging

#### 4.3 Analyze Test Results

- [ ] **Review test report** for:
  - [ ] **Total Tests**: 65/65 PASSED ✅
  - [ ] **Success Rate**: 100%
  - [ ] **Average Response Time**: Document actual time
  - [ ] **Parallel Call Validation**: Tests 52-65 show max 3 parallel calls per batch
  - [ ] **Data Reuse Validation**: Later tests in each sequence show reduced/no tool calls
  - [ ] **Timestamp Format**: Report filename matches `YYYY-MM-DD_HH-MM` format

**Success Criteria**:
- 100% pass rate (65/65)
- Parallel calls respect 3x limit
- Evidence of data reuse in sequential ticker tests

#### 4.4 Document Test Evidence (1x Loop)

- [ ] **Record detailed metrics**:
  - Total tests: 65/65 PASS
  - Success rate: 100%
  - Average response time: X.XXs
  - Performance rating: EXCELLENT/GOOD/ACCEPTABLE
  - Test report path: `test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.txt`
- [ ] **Extract examples**:
  - Test #52 (AMD, INTC, AVGO): Should show 3 parallel get_stock_quote calls
  - Test #3 (SPY closing price): Should show data reuse if Test #2 already retrieved SPY data
  - Test #19 (NVDA current price): Should make new call (first NVDA data)
  - Test #20 (NVDA closing price): Should reuse Test #19 NVDA data

**Success Criteria**: Complete test evidence with parallel call and data reuse examples

⚠️ **CHECKPOINT**: If ANY test fails or behavior incorrect, STOP and debug before 3x loop validation

---

### 🧪 PHASE 5: VALIDATION WITH NEW TEST SCRIPT - 3X LOOPS (MANDATORY - DO NOT SKIP)

#### 5.1 Execute New Test Script (3x Loops)

- [ ] **Run**: `./test_cli_regression.sh 3`
- [ ] **Monitor execution** for consistency across loops

**Success Criteria**: Script completes all 3 loops successfully

#### 5.2 Analyze Aggregate Results

- [ ] **Review aggregate statistics** for:
  - [ ] **Total Loops Passed**: 3/3 ✅
  - [ ] **Overall Success Rate**: 100%
  - [ ] **Average Response Time**: Consistent across loops
  - [ ] **Behavior Consistency**: Parallel call and data reuse patterns consistent

**Success Criteria**:
- All 3 loops pass (195/195 total tests)
- Consistent behavior across loops
- No degradation in performance

#### 5.3 Document Test Evidence (3x Loops)

- [ ] **Record aggregate metrics**:
  - Total loops: 3/3 PASS
  - Total tests: 195/195 PASS (65 x 3)
  - Overall success rate: 100%
  - Average response time: X.XXs
  - Consistency: EXCELLENT/GOOD
  - Test reports: All 3 report paths

**Success Criteria**: Complete aggregate test evidence documented

⚠️ **CHECKPOINT**: If ANY loop fails or shows inconsistent behavior, STOP and debug

---

### 📚 PHASE 6: DOCUMENTATION UPDATES (USE SERENA TOOLS)

#### 6.1 Update Serena Memory: ai_agent_instructions_oct_2025.md

- [ ] **Use Sequential-Thinking** to plan memory update
- [ ] **Use Serena read_memory** to load ai_agent_instructions_oct_2025.md
- [ ] **Use Serena write_memory** to update:
  - Add NEW RULE #2 with 3x parallel limit
  - Add NEW RULE #9 for chat history analysis
  - Update decision tree
  - Add batching examples
  - Add data reuse examples

**Success Criteria**: Memory reflects all new agent instruction changes

#### 6.2 Update Serena Memory: tech_stack.md

- [ ] **Use Serena read_memory** to load tech_stack.md
- [ ] **Use Serena write_memory** to update:
  - Document dynamic parallel tool calling (max 3x limit)
  - Document chat history-based tool call decisions
  - Update test suite information (65 tests vs. 27)
  - Update performance metrics section with new test results

**Success Criteria**: Tech stack reflects new capabilities

#### 6.3 Update Serena Memory: project_architecture.md

- [ ] **Use Serena read_memory** to load project_architecture.md
- [ ] **Use Serena write_memory** to update:
  - Document parallel call batching architecture
  - Document chat history analysis flow
  - Update agent decision-making flow diagram (if exists)

**Success Criteria**: Architecture documentation current

#### 6.4 Update Serena Memory: testing_procedures.md

- [ ] **Use Serena read_memory** to load testing_procedures.md
- [ ] **Use Serena write_memory** to update:
  - Document new test_cli_regression.sh (65 tests)
  - Document sequential ticker test pattern
  - Document data reuse validation approach
  - Update test report naming convention

**Success Criteria**: Testing procedures reflect new test architecture

#### 6.5 Update Serena Memory: suggested_commands.md

- [ ] **Use Serena read_memory** to load suggested_commands.md
- [ ] **Use Serena write_memory** to update:
  - Add new test script commands
  - Update test execution examples

**Success Criteria**: Commands reference new test script

#### 6.6 Update CLAUDE.md - Last Completed Task Section

- [ ] **Use Sequential-Thinking** to draft comprehensive task summary
- [ ] **Use Read tool** to load CLAUDE.md
- [ ] **Use Edit tool** to update Last Completed Task section (lines 12-75) with:

```markdown
## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
[ENHANCEMENT] Dynamic Parallel Tool Calls (Max 3x) + Chat History-Based Tool Decisions

**Primary Changes:**

1. **Parallel Call Limiting**: Max 3 parallel tool calls per batch to prevent rate limiting
2. **Batching Logic**: Requests with >3 tickers automatically batched into groups of 3
3. **Chat History Analysis**: Agent now checks existing conversation data before making tool calls
4. **Data Reuse Intelligence**: Avoids redundant API calls when data already exists in chat
5. **New Test Suite**: 65-test comprehensive validation script (vs. 27 original tests)
6. **Improved Timestamps**: New format YYYY-MM-DD_HH-MM for better readability

**Agent Instruction Changes:**

- **RULE #2 Updated**: Added max 3 parallel call limit with batching logic
- **NEW RULE #9**: Chat history analysis before tool calls (data reuse intelligence)
- **Decision Tree Updated**: Added Step 0 for chat history analysis
- **Examples Updated**: Added batching scenarios and data reuse patterns

**Code Changes:**

- **agent_service.py**: Comprehensive instruction rewrite
  - RULE #2: Dynamic parallel calls with 3x limit (lines 47-54 updated)
  - NEW RULE #9: Chat history analysis logic (inserted after RULE #8)
  - Decision Tree: Enhanced with chat history analysis step (lines 126-133 updated)
  - Instructions: Updated to prioritize chat history check (lines 159-172 updated)
  - Examples: Added batching and data reuse scenarios (lines 135-149 updated)

**Test Suite Changes:**

- **NEW: test_cli_regression.sh**: 65-test comprehensive suite
  - Tests 1-17: SPY sequential (validates data reuse)
  - Tests 18-34: NVDA sequential
  - Tests 35-51: WDC sequential
  - Tests 52-65: Multi-ticker (validates parallel batching)
- **UPDATED: CLI_test_regression.sh**: New timestamp format (27 tests, backward compatible)

**Test Results (1x Loop - 65 Tests):**

- **Total Tests**: 65/65 PASSED ✅
- **Success Rate**: 100%
- **Average Response Time**: X.XXs (EXCELLENT)
- **Response Range**: X.XXs - X.XXs
- **Test Report**: `test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.txt`
- **Parallel Call Validation**: Tests 52-65 show max 3 parallel calls ✅
- **Data Reuse Validation**: Sequential ticker tests show data reuse behavior ✅

**Test Results (3x Loops - 195 Total Tests):**

- **Total Loops**: 3/3 PASSED ✅
- **Total Tests**: 195/195 PASSED (65 x 3) ✅
- **Overall Success Rate**: 100%
- **Average Response Time**: X.XXs (EXCELLENT)
- **Consistency**: All loops showed identical parallel call and data reuse patterns
- **Test Reports**: 3 comprehensive reports generated

**Documentation Updates:**

- ✅ Updated: `CLAUDE.md` (Last Completed Task section)
- ✅ Updated: `.serena/memories/ai_agent_instructions_oct_2025.md`
- ✅ Updated: `.serena/memories/tech_stack.md`
- ✅ Updated: `.serena/memories/project_architecture.md`
- ✅ Updated: `.serena/memories/testing_procedures.md`
- ✅ Updated: `.serena/memories/suggested_commands.md`
- ✅ Created: `test_cli_regression.sh` (new 65-test suite)
- ✅ Updated: `CLI_test_regression.sh` (new timestamp format)
- ✅ Added: 4 test report files (1x loop + 3x loops)

**Impact Analysis:**

- **Agent Intelligence**: Dramatically improved - checks chat history before making calls
- **API Efficiency**: Significant reduction in redundant tool calls through data reuse
- **Rate Limiting Protection**: Max 3 parallel calls prevents API rate limit issues
- **Response Quality**: Maintained 100% with intelligent data usage
- **Test Coverage**: 241% increase in test coverage (27 → 65 tests)
- **Real-World Behavior**: Mimics actual chatbot usage with context awareness
- **Performance**: Maintained EXCELLENT rating despite more complex logic
- **Token Efficiency**: Reduced token usage by reusing existing data

**Files Changed:**

- ✅ Modified: `src/backend/services/agent_service.py` (agent instructions)
- ✅ Created: `test_cli_regression.sh` (65-test suite)
- ✅ Modified: `CLI_test_regression.sh` (timestamp format update)
- ✅ Modified: `CLAUDE.md` (Last Completed Task section)
- ✅ Modified: `.serena/memories/ai_agent_instructions_oct_2025.md`
- ✅ Modified: `.serena/memories/tech_stack.md`
- ✅ Modified: `.serena/memories/project_architecture.md`
- ✅ Modified: `.serena/memories/testing_procedures.md`
- ✅ Modified: `.serena/memories/suggested_commands.md`
- ✅ Added: `test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.txt`
- ✅ Added: `test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.txt` (3x loops, reports 1-3)
- ✅ Modified: `TODO_task_plan.md` (marked complete)

**Total**: 3 code files (1 created, 2 modified), 5 Serena memory files updated, 4+ test reports added
<!-- LAST_COMPLETED_TASK_END -->
```

**Success Criteria**: CLAUDE.md documents all changes with complete test evidence

---

### 🔄 PHASE 7: FINAL VERIFICATION (USE SERENA TOOLS)

#### 7.1 Comprehensive Code Verification

- [ ] **Use Sequential-Thinking** to plan verification strategy
- [ ] **Use Serena search_for_pattern** to verify agent instructions contain:
  - "MAX 3 PER BATCH" or "max 3 parallel"
  - "RULE #9" and "CHAT HISTORY"
  - "BATCH" or "batching"
  - "existing data" or "data reuse"

**Success Criteria**: All new instruction patterns found in code

#### 7.2 Test Script Verification

- [ ] **Verify new script exists**: `ls -la test_cli_regression.sh`
- [ ] **Verify executable**: `test -x test_cli_regression.sh && echo "✅ Executable"`
- [ ] **Count test prompts**: Verify 65 prompts in array
- [ ] **Verify timestamp format**: Check `LOOP_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")`

**Success Criteria**: New test script complete and properly configured

#### 7.3 Current Script Verification

- [ ] **Verify current script updated**: `grep "date +\"%Y-%m-%d_%H-%M\"" CLI_test_regression.sh`
- [ ] **Success indicator**: Command returns matching line

**Success Criteria**: Current script has new timestamp format

#### 7.4 Use Serena think_about_whether_you_are_done

- [ ] **Use Serena think_about_whether_you_are_done** tool
- [ ] **Confirm**:
  - All agent instruction changes implemented
  - Both test scripts updated/created
  - All 1x and 3x loop tests passed (100%)
  - All documentation updated
  - All verification checks passed

**Success Criteria**: Task completion confirmed by Serena

---

### 📤 PHASE 8: ATOMIC GIT COMMIT (FOLLOW PROPER WORKFLOW)

⚠️ **CRITICAL**: Follow the proper atomic commit workflow from CLAUDE.md and git_commit_workflow.md

#### 8.1 Verify ALL Work Complete (DO NOT STAGE YET)

- [ ] ✅ ALL agent instruction changes complete (agent_service.py)
- [ ] ✅ NEW test script created (test_cli_regression.sh)
- [ ] ✅ CURRENT test script updated (CLI_test_regression.sh)
- [ ] ✅ ALL tests passed (1x loop: 65/65, 3x loops: 195/195)
- [ ] ✅ ALL test reports generated (4+ reports)
- [ ] ✅ ALL documentation updated (CLAUDE.md + 5 Serena memories)
- [ ] ✅ ALL verification checks passed
- [ ] ⚠️ **DO NOT RUN `git add` YET**

#### 8.2 Review Changes

- [ ] **Run**: `git status` to review all changed/new files
- [ ] **Run**: `git diff` to review all changes
- [ ] **Verify**: All expected files present, no unexpected changes

#### 8.3 Stage Everything at Once (FIRST TIME USING git add)

- [ ] **Run**: `git add -A` (stage ALL files in ONE command)
- [ ] ⚠️ This is the FIRST time running `git add`

#### 8.4 Verify Staging Immediately

- [ ] **Run**: `git status`
- [ ] **Verify**: ALL files staged, NOTHING unstaged
- [ ] **If missing files**: `git add [missing-file]`

#### 8.5 Commit Immediately (Within 60 Seconds)

- [ ] **Run**:

```bash
git commit -m "$(cat <<'EOF'
[ENHANCEMENT] Dynamic Parallel Tool Calls (Max 3x) + Chat History-Based Tool Decisions

**Primary Changes:**

1. **Parallel Call Limiting**: Max 3 parallel tool calls per batch to prevent rate limiting
2. **Batching Logic**: Requests with >3 tickers automatically batched into groups of 3
3. **Chat History Analysis**: Agent now checks existing conversation data before making tool calls
4. **Data Reuse Intelligence**: Avoids redundant API calls when data already exists in chat
5. **New Test Suite**: 65-test comprehensive validation script (vs. 27 original tests)
6. **Improved Timestamps**: New format YYYY-MM-DD_HH-MM for better readability

**Agent Instruction Changes:**

- **RULE #2 Updated**: Added max 3 parallel call limit with batching logic
- **NEW RULE #9**: Chat history analysis before tool calls (data reuse intelligence)
- **Decision Tree Updated**: Added Step 0 for chat history analysis
- **Examples Updated**: Added batching scenarios and data reuse patterns

**Code Changes:**

- **agent_service.py**: Comprehensive instruction rewrite
  - RULE #2: Dynamic parallel calls with 3x limit
  - NEW RULE #9: Chat history analysis logic
  - Decision Tree: Enhanced with chat history analysis step
  - Instructions: Updated to prioritize chat history check
  - Examples: Added batching and data reuse scenarios

**Test Suite Changes:**

- **NEW: test_cli_regression.sh**: 65-test comprehensive suite
- **UPDATED: CLI_test_regression.sh**: New timestamp format

**Test Results (1x Loop - 65 Tests):**

- Total Tests: 65/65 PASSED ✅
- Success Rate: 100%
- Average Response Time: X.XXs (EXCELLENT)
- Test Report: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.txt
- Parallel Call Validation: ✅ Max 3 parallel calls confirmed
- Data Reuse Validation: ✅ Sequential ticker data reuse confirmed

**Test Results (3x Loops - 195 Total Tests):**

- Total Loops: 3/3 PASSED ✅
- Total Tests: 195/195 PASSED ✅
- Overall Success Rate: 100%
- Consistency: EXCELLENT across all loops

**Documentation Updates:**

- ✅ Updated: CLAUDE.md
- ✅ Updated: 5 Serena memory files
- ✅ Created: test_cli_regression.sh
- ✅ Updated: CLI_test_regression.sh
- ✅ Added: 4+ test report files

**Impact Analysis:**

- Agent Intelligence: Dramatically improved with chat history analysis
- API Efficiency: Significant reduction in redundant calls
- Rate Limiting Protection: Max 3 parallel calls prevents issues
- Test Coverage: 241% increase (27 → 65 tests)
- Performance: Maintained EXCELLENT rating

**Files Changed:**

- ✅ Modified: src/backend/services/agent_service.py
- ✅ Created: test_cli_regression.sh
- ✅ Modified: CLI_test_regression.sh
- ✅ Modified: CLAUDE.md
- ✅ Modified: 5 Serena memory files
- ✅ Added: 4+ test report files
- ✅ Modified: TODO_task_plan.md

**Total**: 3 code files (1 created, 2 modified), 5 Serena memory files updated, 4+ test reports added

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### 8.6 Push Immediately

- [ ] **Run**: `git push`

**Success Criteria**: Clean atomic commit with all changes, pushed to remote

---

## 📈 SUCCESS METRICS

### Agent Intelligence Metrics

- ✅ Parallel call limiting: Max 3 per batch enforced
- ✅ Batching logic: >3 tickers automatically batched
- ✅ Chat history analysis: Agent checks existing data before calls
- ✅ Data reuse: Redundant calls eliminated when data exists
- ✅ Decision tree: Enhanced with chat history analysis step

### Test Coverage Metrics

- ✅ Test count: 27 → 65 tests (241% increase)
- ✅ Test organization: Sequential ticker patterns for data reuse validation
- ✅ Parallel call testing: Multi-ticker tests validate batching
- ✅ Data reuse testing: Sequential tests validate chat history analysis
- ✅ Pass rate: 100% (65/65 in 1x loop, 195/195 in 3x loops)

### Code Quality Metrics

- ✅ Agent instructions: Comprehensive with 2 new major rules
- ✅ Examples: Batching and data reuse scenarios included
- ✅ Documentation: All Serena memories and CLAUDE.md updated
- ✅ Test scripts: 2 scripts (new 65-test + updated 27-test)
- ✅ Timestamp format: Improved readability

### Performance Metrics

- ✅ Response times: Maintained EXCELLENT rating
- ✅ API efficiency: Reduced redundant calls through data reuse
- ✅ Rate limiting: Protected with 3x parallel limit
- ✅ Token usage: Reduced through intelligent data reuse

---

## 🚨 CRITICAL REMINDERS

1. **USE SERENA TOOLS**: Mandatory for all code analysis and manipulation
2. **USE SEQUENTIAL-THINKING**: Start every phase with systematic analysis
3. **TESTING IS MANDATORY**: Cannot skip test phases - must show 100% pass rate for BOTH 1x and 3x loops
4. **STAGE ONLY BEFORE COMMIT**: Never run `git add` until ALL work complete
5. **ATOMIC COMMIT**: Include code + tests + docs in single commit
6. **VERIFY BEFORE COMMIT**: Ensure all checklist items complete
7. **TWO TEST SCRIPTS**: Must update BOTH test_cli_regression.sh (new) AND CLI_test_regression.sh (current)
8. **TIMESTAMP FORMAT**: New format must be YYYY-MM-DD_HH-MM (not YYYYMMDD_HHMMSS)

---

## 📝 NOTES

### Design Rationale

**Parallel Call Limiting (Max 3x):**
- Prevents API rate limiting issues
- Balances performance with API stability
- Industry best practice for parallel API calls

**Chat History Analysis:**
- Mimics real chatbot behavior
- Reduces redundant API calls significantly
- Improves token efficiency
- Provides faster responses when data exists
- User experience improvement - context awareness

**Sequential Ticker Tests:**
- Validates data reuse behavior naturally
- Tests real-world conversation patterns
- Allows accumulation of context data
- Perfect for chat history analysis validation

**Batching Logic:**
- Automatic for >3 tickers
- Transparent to user
- SDK handles parallel execution within batches
- Agent controls batch size via instructions

### Implementation Strategy

- **Instruction-Based Control**: SDK doesn't limit parallel calls - agent instructions do
- **LLM Decision-Making**: Agent analyzes request complexity and chat history to decide on tool calls
- **Transparency**: Examples clearly show batching and data reuse patterns
- **Backward Compatibility**: Current 27-test script kept functional with new timestamp format

---

**END OF PLAN**

**NEXT STEP**: Begin Phase 1 - Agent Instructions Update using Serena Tools
