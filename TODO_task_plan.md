# AI Agent Tool Descriptions Optimization - Implementation TODO Task Plan

## Overview

**Goal:** Optimize all 6 AI Agent Tool descriptions to reduce token usage by 60-70% while maintaining full functionality and regression test coverage.

**Current State:** 6 tools with ~2,670 tokens in descriptions
**Target State:** 6 tools with ~800-900 tokens in descriptions
**Expected Reduction:** ~1,870 tokens (70% reduction)

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
- **Use Standard Read/Write/Edit** only when Serena doesn't support the specific operation
- **NEVER stop using advanced tools** until task completion

---

## Phase 3: Implementation

### Step 1: Pre-Implementation Analysis

**Objective:** Verify current state and prepare for optimization

**Sub-tasks:**

1.1. **Use Sequential-Thinking** to plan implementation approach
   - Analyze research findings
   - Determine optimization order (which tool first)
   - Plan validation checkpoints

1.2. **Use Serena** to read all 6 tool descriptions
   - `mcp__serena__find_symbol(name_path="get_stock_quote", relative_path="src/backend/tools/tradier_tools.py", include_body=true)`
   - Repeat for all 6 tools
   - Document current token counts

1.3. **Create backup git commit** (optional safety measure)
   - `git add -A && git commit -m "[BACKUP] Before tool descriptions optimization"`
   - This allows easy rollback if needed

**Validation:** All 6 tool descriptions read and current state documented

---

### Step 2: Optimize tradier_tools.py - get_stock_quote()

**Current:** ~450 tokens (53 lines docstring)
**Target:** ~130 tokens (15-18 lines docstring)

**Sub-tasks:**

2.1. **Use Sequential-Thinking** to plan optimization for this specific tool
   - Analyze current description structure
   - Identify what to remove vs keep
   - Draft optimized version

2.2. **Draft optimized description:**
```python
"""Get real-time stock quote(s) for one or more tickers from Tradier API.

Args:
    ticker: Stock ticker symbol(s). Single: "AAPL" or multiple: "AAPL,TSLA,NVDA" (comma-separated, no spaces).

Returns:
    JSON string with quote data (ticker, current_price, change, percent_change, high, low, open, previous_close, source).
    Multiple tickers return array of quote objects.

Note: Handles up to 10 tickers. Real-time updates during market hours.
"""
```

2.3. **Use Serena** to replace symbol body
   - `mcp__serena__replace_symbol_body(name_path="get_stock_quote", relative_path="src/backend/tools/tradier_tools.py", body="[NEW BODY]")`
   - Replace entire function body including optimized docstring

2.4. **Verify replacement**
   - `mcp__serena__find_symbol(name_path="get_stock_quote", include_body=true)`
   - Confirm new description is correct

**Validation:** Tool description reduced from ~450 to ~130 tokens (71% reduction)

---

### Step 3: Optimize tradier_tools.py - get_options_expiration_dates()

**Current:** ~330 tokens (45 lines docstring)
**Target:** ~100 tokens (12-15 lines docstring)

**Sub-tasks:**

3.1. **Use Sequential-Thinking** to plan optimization

3.2. **Draft optimized description:**
```python
"""Get available options expiration dates for a ticker from Tradier API.

Args:
    ticker: Stock ticker symbol (e.g., "AAPL", "SPY").

Returns:
    JSON string with expiration dates array (ticker, expiration_dates[], count, source).
    Dates in YYYY-MM-DD format, sorted chronologically.

Note: Includes weekly and monthly expirations.
"""
```

3.3. **Use Serena** to replace symbol body
   - `mcp__serena__replace_symbol_body()`

3.4. **Verify replacement**

**Validation:** Tool description reduced from ~330 to ~100 tokens (70% reduction)

---

### Step 4: Optimize tradier_tools.py - get_stock_price_history()

**Current:** ~500 tokens (69 lines docstring)
**Target:** ~150 tokens (18-20 lines docstring)

**Sub-tasks:**

4.1. **Use Sequential-Thinking** to plan optimization

4.2. **Draft optimized description:**
```python
"""Get historical stock price data (OHLC bars) from Tradier API.

Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
    start_date: Start date in YYYY-MM-DD format.
    end_date: End date in YYYY-MM-DD format.
    interval: Time interval - "daily", "weekly", or "monthly".
              See RULE #3 for selection logic.

Returns:
    JSON string with historical OHLC data (ticker, interval, start_date, end_date, bars[], count, source).
    Each bar includes date, open, high, low, close, volume.

Note: Date range is inclusive. Tool auto-adjusts weekend dates to previous Friday.
"""
```

4.3. **Use Serena** to replace symbol body

4.4. **Verify replacement**

**Validation:** Tool description reduced from ~500 to ~150 tokens (70% reduction)

---

### Step 5: Optimize tradier_tools.py - get_options_chain_both()

**Current:** ~580 tokens (68 lines docstring)
**Target:** ~160 tokens (20-22 lines docstring)

**Sub-tasks:**

5.1. **Use Sequential-Thinking** to plan optimization

5.2. **Draft optimized description:**
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
    Both chains have identical strikes (10 above, 10 below current price).
    Columns: Strike, Bid, Ask, Delta, Volume, OI, IV, Gamma.

Note: Single API call fetches both chains. See RULE #5 for usage guidance.
"""
```

5.3. **Use Serena** to replace symbol body

5.4. **Verify replacement**

**Validation:** Tool description reduced from ~580 to ~160 tokens (72% reduction)

---

### Step 6: Optimize tradier_tools.py - get_market_status_and_date_time()

**Current:** ~370 tokens (52 lines docstring)
**Target:** ~110 tokens (13-15 lines docstring)

**Sub-tasks:**

6.1. **Use Sequential-Thinking** to plan optimization

6.2. **Draft optimized description:**
```python
"""Get current market status and date/time from Tradier API.

Args:
    None - retrieves current status automatically.

Returns:
    JSON string with market status and datetime (market_status, after_hours, early_hours, exchanges{}, server_time, date, time, source).

Note: Server time in UTC. Includes pre-market and after-market status.
"""
```

6.3. **Use Serena** to replace symbol body

6.4. **Verify replacement**

**Validation:** Tool description reduced from ~370 to ~110 tokens (70% reduction)

---

### Step 7: Optimize polygon_tools.py - get_ta_indicators()

**Current:** ~440 tokens (59 lines docstring)
**Target:** ~150 tokens (18-20 lines docstring)

**Sub-tasks:**

7.1. **Use Sequential-Thinking** to plan optimization

7.2. **Draft optimized description:**
```python
"""Get comprehensive technical analysis indicators (RSI, MACD, SMA, EMA) in a single call.

Consolidated tool replaces individual TA indicator tools with optimized batched API calls.

Indicators: RSI-14, MACD (12/26/9), SMA (5/10/20/50/200), EMA (5/10/20/50/200).

Args:
    ticker: Stock ticker symbol (e.g., "SPY", "AAPL").
    timespan: Aggregate window - "day", "minute", "hour", "week", "month" (default: "day").

Returns:
    Formatted markdown table with all 14 indicators (indicator, period, value, timestamp).
    Always returns last available data (even on weekends/holidays).

Note: 12 API calls in ~2-3 seconds with rate limit protection. Gracefully handles partial failures (displays N/A).
"""
```

7.3. **Use Serena** to replace symbol body

7.4. **Verify replacement**

**Validation:** Tool description reduced from ~440 to ~150 tokens (66% reduction)

---

### Step 8: Verify All Optimizations

**Objective:** Confirm all 6 tools have been optimized correctly

**Sub-tasks:**

8.1. **Use Sequential-Thinking** to review all changes
   - Analyze each optimized description
   - Verify token reduction achieved
   - Confirm essential information retained

8.2. **Use Serena** to read all 6 tool descriptions again
   - Verify all changes applied correctly
   - Check for any syntax errors
   - Confirm docstring format is valid

8.3. **Count total tokens saved**
   - Calculate actual token reduction
   - Compare against target (60-70% reduction)
   - Document final token counts

**Validation:** All 6 tools optimized, ~1,800-1,900 tokens saved (60-70% reduction)

---

## Phase 4: Testing

### Step 9: Manual CLI Testing (PER TOOL)

**Objective:** Test each tool individually with 1-2 representative prompts

**🔴 CRITICAL: These manual tests MUST pass before proceeding to regression testing 🔴**

**Sub-tasks:**

9.1. **Test get_stock_quote()**
   - Prompt 1: "Get AAPL stock quote"
   - Prompt 2: "Get quotes for SPY, QQQ, DIA"
   - **Verify:**
     - ✅ Agent selects get_stock_quote()
     - ✅ Single ticker returns correct data
     - ✅ Multiple tickers return array
     - ✅ Response formatting correct

9.2. **Test get_options_expiration_dates()**
   - Prompt 1: "Get options expiration dates for SPY"
   - **Verify:**
     - ✅ Agent selects get_options_expiration_dates()
     - ✅ Returns date array
     - ✅ Dates sorted chronologically

9.3. **Test get_stock_price_history()**
   - Prompt 1: "Stock price performance the last 5 trading days: SPY"
   - Prompt 2: "Stock price performance the last 2 weeks: NVDA"
   - **Verify:**
     - ✅ Agent selects get_stock_price_history()
     - ✅ Correct interval selected (daily for days, weekly for weeks)
     - ✅ OHLC data returned correctly
     - ✅ Date range correct

9.4. **Test get_options_chain_both()**
   - Prompt 1: "Get both call and put options chains for SPY expiring this Friday"
   - **Verify:**
     - ✅ Agent selects get_options_chain_both()
     - ✅ Agent gets current price first
     - ✅ Both call and put tables returned
     - ✅ 20 strikes each, centered around current price
     - ✅ Markdown tables preserved (NOT converted to bullets)

9.5. **Test get_market_status_and_date_time()**
   - Prompt 1: "Is the market open?"
   - Prompt 2: "What's today's date?"
   - **Verify:**
     - ✅ Agent selects get_market_status_and_date_time()
     - ✅ Returns market status
     - ✅ Returns date and time

9.6. **Test get_ta_indicators()**
   - Prompt 1: "Get technical analysis indicators for SPY"
   - **Verify:**
     - ✅ Agent selects get_ta_indicators()
     - ✅ Returns markdown table with 14 indicators
     - ✅ Table formatting preserved

**Validation:** All 6 tools tested manually, all tests pass

**🔴 IF ANY MANUAL TEST FAILS:**
1. Analyze why tool selection or response failed
2. Identify missing critical information in optimized description
3. Add back essential information
4. Re-test until all pass
5. **DO NOT proceed to Step 10 until all manual tests pass**

---

### Step 10: Full Regression Testing - Phase 1 (Automated Response Generation)

**Objective:** Execute full 37-test suite to generate all responses

**Sub-tasks:**

10.1. **Execute regression test suite**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

10.2. **Monitor test execution**
   - Watch for completion messages
   - Check for any script errors
   - Verify session persistence

10.3. **Verify test completion**
   - **Expected:** "37/37 COMPLETED" (all responses received)
   - **Check:** Test report file generated in test-reports/
   - **Note:** Average response time (should be ~10-11 seconds)

10.4. **Document Phase 1 results**
   - Test report path
   - Completion count (must be 37/37)
   - Average response time
   - Any script errors or warnings

**Validation:** 37/37 tests completed, test report generated

**🔴 IF PHASE 1 FAILS (less than 37/37 completed):**
1. Check for script errors
2. Check for API connection issues
3. Verify all tools are importable
4. Fix issues and re-run
5. **DO NOT proceed to Step 11 until Phase 1 shows 37/37**

---

### Step 11: Full Regression Testing - Phase 2 (Manual Verification)

**Objective:** Manually verify EACH of the 37 test responses for correctness

**🔴 CRITICAL: This is NOT optional - YOU MUST manually review EVERY test response 🔴**

**Why Grep is Insufficient:**
- ❌ Misses duplicate/unnecessary tool calls
- ❌ Misses wrong tool selection
- ❌ Misses data inconsistencies
- ❌ Only catches explicit error messages

**Sub-tasks:**

11.1. **Use Read tool to read test report file**
   - `Read(file_path="test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log")`
   - Read in sections (use offset and limit for large file)

11.2. **Apply 4-Point Verification Criteria to EACH test (1-37)**

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
   - Data formatting matches expected format (OHLC, tables, etc.)
   - No hallucinated data or made-up values
   - No cross-ticker contamination
   - Options chains show Bid/Ask columns (NOT midpoint)

**Criterion 4: Are there any errors?**
   - No error messages in response
   - No "data unavailable" messages
   - No RuntimeWarnings
   - No API errors

11.3. **Document EACH test result in a table**

| Test # | Test Name | Status | Tool(s) Called | Issue (if failed) | Failure Type |
|--------|-----------|--------|----------------|-------------------|--------------|
| 1 | Market_Status | ✅ PASS | get_market_status_and_date_time | - | - |
| 2 | SPY_Price | ✅ PASS | get_stock_quote | - | - |
| ... | ... | ... | ... | ... | ... |
| 37 | Multi_Options_Dates | ✅ PASS | 3× get_options_expiration_dates | - | - |

**Failure Types (if any):**
- Code Error: Syntax/runtime errors, import errors
- Logic Error (Duplicate Tool Call): Agent made unnecessary redundant API calls
- Logic Error (Wrong Tool): Agent called wrong tool for the query
- Data Error: Wrong data returned, cross-ticker contamination
- Response Error: Incomplete response, doesn't address query

11.4. **Answer Mandatory Checkpoint Questions**

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

**Validation:** All 37 tests manually verified, results table created, checkpoint questions answered

**🔴 IF ANY TESTS FAIL:**
1. Analyze which tool description optimization caused the failure
2. Identify missing critical information
3. Update tool description to restore essential information
4. Re-run manual CLI testing for that tool (Step 9.X)
5. Re-run full regression suite (Step 10)
6. Re-do Phase 2 manual verification (Step 11)
7. **DO NOT proceed to Phase 5 until 37/37 PASS**

---

### Step 12: Final Validation Before Commit

**Objective:** Confirm everything is ready for commit

**Sub-tasks:**

12.1. **Use Sequential-Thinking** to review entire implementation
   - All 6 tools optimized?
   - All manual tests passed?
   - All 37 regression tests passed with manual verification?
   - Token reduction target achieved?

12.2. **Verify test evidence**
   - Test report file exists
   - 37/37 completion confirmed
   - Phase 2 manual verification table complete
   - All checkpoint questions answered

12.3. **Check git status**
   - Which files have been modified?
   - Are there any untracked files?
   - Is everything ready to stage?

**Validation:** All requirements met, ready for Phase 5

---

## Phase 5: Final Commit

### Step 13: Update Documentation

**Objective:** Update CLAUDE.md with task completion summary

**Sub-tasks:**

13.1. **Read current CLAUDE.md Last Completed Task Summary section**
   - Find the section marked with `<!-- LAST_COMPLETED_TASK_START -->`

13.2. **Draft completion summary**
   - Include all 6 tool optimizations
   - Document token reduction achieved
   - Include test results (37/37 PASS with Phase 2 verification)
   - List files modified
   - Include risk assessment (VERY LOW)

13.3. **Use Edit tool to replace Last Completed Task Summary**
   - Replace content between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->`

**Validation:** CLAUDE.md updated with complete task summary

---

### Step 14: Atomic Git Commit Workflow

**Objective:** Create single atomic commit with ALL changes

**🔴 CRITICAL: Follow atomic commit workflow EXACTLY 🔴**

**Sub-tasks:**

14.1. **DO ALL WORK FIRST** (DO NOT stage anything yet)
   - ✅ All 6 tool descriptions optimized
   - ✅ All tests run and passing
   - ✅ CLAUDE.md updated
   - ✅ research_task_plan.md complete
   - ✅ TODO_task_plan.md complete
   - ⚠️ **DO NOT RUN `git add` YET**

14.2. **VERIFY EVERYTHING IS COMPLETE**
```bash
git status  # Review ALL changed/new files
git diff    # Review ALL changes
```
   - Ensure ALL work is done
   - Ensure ALL files are present

14.3. **STAGE EVERYTHING AT ONCE**
```bash
git add -A  # Stage ALL files in ONE command
```
   - ⚠️ This is the FIRST time you run `git add`
   - ⚠️ Stage ALL related files together

14.4. **VERIFY STAGING IMMEDIATELY**
```bash
git status  # Verify ALL files staged, NOTHING unstaged
```
   - If anything is missing: `git add [missing-file]`

14.5. **COMMIT IMMEDIATELY** (within 60 seconds of staging)
```bash
git commit -m "$(cat <<'EOF'
[TOOL_DESCRIPTIONS_OPTIMIZATION] Optimize tool descriptions - 70% token reduction

Phase 1-4 Complete: Research, Planning, Implementation, and Full Testing

Major Changes:
- Optimized 6 AI Agent Tool descriptions (tradier_tools.py + polygon_tools.py)
- Token reduction breakdown:
  * get_stock_quote: 450→130 tokens (71% reduction)
  * get_options_expiration_dates: 330→100 tokens (70% reduction)
  * get_stock_price_history: 500→150 tokens (70% reduction)
  * get_options_chain_both: 580→160 tokens (72% reduction)
  * get_market_status_and_date_time: 370→110 tokens (70% reduction)
  * get_ta_indicators: 440→150 tokens (66% reduction)

Optimization Strategy:
- Removed verbose JSON response examples (~900 tokens saved)
- Condensed "Use this tool when" sections (~175 tokens saved)
- Consolidated redundant notes (~350 tokens saved)
- Removed usage examples (~200 tokens saved)
- Simplified parameter descriptions (~100 tokens saved)
- Removed duplication with system instructions (~200 tokens saved)

Total Token Reduction:
- Before: ~2,670 tokens
- After: ~800 tokens
- Savings: ~1,870 tokens (70% reduction)

Testing Results:
- Phase 1: 37/37 automated test responses COMPLETED
- Phase 2: 37 tests manually verified with 4-point criteria
- 37/37 PASS (100% pass rate, 0 failures)
- Manual CLI testing: 6/6 tools tested and passing
- All tools correctly selected by agent
- All responses correctly formatted
- No regression detected

Files Modified:
- src/backend/tools/tradier_tools.py: 5 tool descriptions optimized
- src/backend/tools/polygon_tools.py: 1 tool description optimized
- CLAUDE.md: Updated with completion summary
- research_task_plan.md: Complete research findings
- TODO_task_plan.md: Detailed implementation checklist

Documentation:
- research_task_plan.md: Token inefficiency analysis and optimization strategy
- TODO_task_plan.md: Granular implementation steps
- Test report: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log

Risk Assessment: VERY LOW
- No functionality removed (docstring optimization only)
- All 37 regression tests pass with manual verification
- All tools maintain correct behavior
- Token efficiency improved 70% without regression

Performance Impact:
- Token reduction: 70% (from ~2,670 to ~800 tokens)
- Cost savings: Significant reduction in tokens per API call
- Maintenance: Simpler, more concise tool descriptions
- Clarity: More focused, less verbose descriptions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

14.6. **PUSH IMMEDIATELY**
```bash
git push
```

**Validation:** Atomic commit created and pushed to remote

---

## Success Criteria

### Quantitative Metrics

- ✅ **Token Reduction:** 60-70% achieved (~1,870 tokens saved)
- ✅ **Test Pass Rate:** 37/37 (100%) with Phase 2 manual verification
- ✅ **Tools Optimized:** 6/6 (100%)
- ✅ **Manual Tests:** 6/6 (100%) passed

### Qualitative Metrics

- ✅ **Improved Clarity:** Descriptions more concise and focused
- ✅ **Better Alignment:** Follows OpenAI best practices
- ✅ **No Regression:** All functionality maintained
- ✅ **Maintainability:** Simpler, easier to update

---

## Risk Mitigation

### If Tests Fail

**Symptom:** Agent doesn't select correct tool
**Solution:**
1. Review tool description - is purpose clear?
2. Add back critical "when to use" guidance
3. Ensure one-sentence description is action-oriented

**Symptom:** Agent misunderstands parameters
**Solution:**
1. Review parameter descriptions - are they clear?
2. Add back critical examples if needed
3. Ensure format guidance is present

**Symptom:** Output formatting breaks
**Solution:**
1. Review notes section - is critical formatting mentioned?
2. Add back essential formatting constraints
3. Ensure return description mentions key structure

### Rollback Plan

If optimization causes too many test failures:
1. Use git to restore previous version
2. Analyze which information was essential
3. Create less aggressive optimization
4. Re-test and iterate

---

## Timeline Estimate

- **Step 1-8 (Implementation):** 30-40 minutes
- **Step 9 (Manual CLI Testing):** 15-20 minutes
- **Step 10-11 (Regression Testing):** 20-30 minutes
- **Step 12 (Final Validation):** 5 minutes
- **Step 13-14 (Documentation & Commit):** 10-15 minutes
- **Total:** ~80-110 minutes

---

## Tools and Commands Reference

### Serena Tools

```python
# Read symbol
mcp__serena__find_symbol(name_path="get_stock_quote", relative_path="src/backend/tools/tradier_tools.py", include_body=true)

# Replace symbol body
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
- [ ] Step 1: Pre-implementation analysis complete
- [ ] Step 2: get_stock_quote() optimized and verified
- [ ] Step 3: get_options_expiration_dates() optimized and verified
- [ ] Step 4: get_stock_price_history() optimized and verified
- [ ] Step 5: get_options_chain_both() optimized and verified
- [ ] Step 6: get_market_status_and_date_time() optimized and verified
- [ ] Step 7: get_ta_indicators() optimized and verified
- [ ] Step 8: All optimizations verified, token counts confirmed

### Phase 4: Testing
- [ ] Step 9.1: get_stock_quote() manual testing (2 prompts) - PASS
- [ ] Step 9.2: get_options_expiration_dates() manual testing (1 prompt) - PASS
- [ ] Step 9.3: get_stock_price_history() manual testing (2 prompts) - PASS
- [ ] Step 9.4: get_options_chain_both() manual testing (1 prompt) - PASS
- [ ] Step 9.5: get_market_status_and_date_time() manual testing (2 prompts) - PASS
- [ ] Step 9.6: get_ta_indicators() manual testing (1 prompt) - PASS
- [ ] Step 10: Phase 1 regression testing - 37/37 COMPLETED
- [ ] Step 11: Phase 2 manual verification - 37/37 PASS with 4-point criteria
- [ ] Step 12: Final validation - all requirements met

### Phase 5: Final Commit
- [ ] Step 13: CLAUDE.md updated with completion summary
- [ ] Step 14.1: All work complete, no staging yet
- [ ] Step 14.2: Git status and diff reviewed
- [ ] Step 14.3: All files staged at once (git add -A)
- [ ] Step 14.4: Staging verified (git status)
- [ ] Step 14.5: Atomic commit created
- [ ] Step 14.6: Changes pushed to remote

---

## Next Steps

**Immediate Action:** Begin Phase 3 - Implementation (Step 1)

**Use Sequential-Thinking** to start the implementation:
- Analyze research findings
- Plan approach for first tool optimization
- Prepare for systematic execution of all steps

**Remember:** Use Serena tools for all code modifications, Sequential-Thinking for all planning and analysis.
