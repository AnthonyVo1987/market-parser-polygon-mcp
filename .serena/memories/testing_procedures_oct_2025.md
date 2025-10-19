# Testing Procedures - Updated October 2025

**Status:** Current with 39-test suite and Phase 2 manual verification
**Test Framework:** Custom CLI regression suite + pytest

---

## CLI Regression Test Suite (39 Tests)

### Overview
- **Location:** `test_cli_regression.sh`
- **Count:** 39 comprehensive financial tests
- **Mode:** Single persistent CLI session
- **Duration:** ~395 seconds (~6.5 minutes)

### Test Organization

**SPY Sequence (17 tests):**
1. Market Status
2. Current Price OHLC
3. Yesterday's Price OHLC
4. Last Week Performance OHLC
5. Previous Week Friday OHLC
6. Last 5 Trading Days OHLC
7. Past 2 Weeks OHLC
8. Past Month
9. Past 3 Months
10. TA Indicator DATA Only
11. Support & Resistance
12. Full TA Analysis
13. Options Expiration Dates
14. Call Options Chain
15. Put Options Chain
16. Options Wall Analysis
17. (Tests continue...)

**NVDA Sequence (17 tests):**
- Same as SPY but for $NVDA ticker

**Multi-Ticker Sequence (5 tests):**
- Tests with $WDC, $AMD, $SOUN combinations

### Running Tests

**Start the test suite:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Expected output:**
```
✅ Response received
⏱️  Response Time: 9.56s
📈 Performance: EXCELLENT (< 30s)

[After all 39 tests]
39/39 COMPLETED
Average Response Time: 9.56s
Overall Performance Rating: EXCELLENT
```

**Test report location:**
```bash
test-reports/test_cli_regression_loop1_2025-10-18_11-24.log
```

### Performance Targets

| Performance Level | Response Time |
|------------------|---------------|
| EXCELLENT | < 10s |
| GOOD | 10-15s |
| ACCEPTABLE | 15-20s |
| NEEDS IMPROVEMENT | > 20s |

**Current Baseline (Oct 19, 2025):** ~8s average (EXCELLENT)

---

## Two-Phase Testing Workflow

### Phase 1: Response Generation (AUTOMATED)

**What it does:**
- Runs all 39 tests
- Generates all 39 responses
- Tracks response times
- Creates test report

**What it does NOT do:**
- ❌ Does NOT verify response correctness
- ❌ Does NOT check tool calls for duplication/efficiency
- ❌ Does NOT validate data formatting
- ❌ Does NOT check for logic errors

**Success criteria:**
- 39/39 responses generated
- Average response time < 30s
- No timeouts

**Output:**
```
39/39 COMPLETED
Average Response Time: 8.21s
```

### Phase 2: Manual Verification (MANUAL - MANDATORY)

🔴 **CRITICAL: Grep commands are INSUFFICIENT and will miss failures. You MUST manually review EACH test response.**

**Why Grep Fails:**
- ❌ Misses duplicate/unnecessary tool calls (agent calling same tool twice)
- ❌ Misses wrong tool selection (agent calling wrong API for data)
- ❌ Misses data inconsistencies (cross-ticker contamination, wrong data returned)
- ❌ Only catches explicit error messages, not logic errors

**MANDATORY Process for EACH of the 39 Tests:**

#### **Step 1: Read Test Response Using Read Tool**
- Use `Read` tool to read the test log file section for each test
- Read lines corresponding to that test's Agent Response, Tools Used, and Performance Metrics
- **NO scripts, NO grep shortcuts - READ each test manually**

#### **Step 2: Apply 4-Point Verification Criteria**

For EACH test, you MUST verify ALL 4 criteria:

1. ✅ **Does the response address the query?**
   - Does the agent's response directly answer the test prompt?
   - Is the response relevant to the ticker(s) mentioned?
   - Is the response complete (not truncated)?

2. ✅ **Were the RIGHT tools called (not duplicate/unnecessary calls)?**
   - **Check conversation context**: If a previous test already retrieved data, agent should NOT call the same tool again
   - Example FAIL: Test 10 calls `get_ta_indicators()`, Test 12 should NOT call it again
   - Are the tools appropriate for the query (Tradier for quotes, Polygon for TA)?
   - Are there any redundant API calls?

3. ✅ **Is the data correct?**
   - Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
   - Data formatting matches expected format (OHLC, tables, etc.)
   - No hallucinated data or made-up values
   - No cross-ticker contamination (NVDA query shouldn't return SPY data)
   - Options chains show Bid/Ask columns (NOT midpoint)

4. ✅ **Are there any errors?**
   - No error messages in response
   - No "data unavailable" messages
   - No RuntimeWarnings
   - No API errors

#### **Step 3: Document Each Test Result**

Create a table documenting ALL 39 tests:

| Test # | Test Name | Status | Issue (if failed) | Failure Type |
|--------|-----------|--------|-------------------|--------------|
| 1 | Market_Status | ❌ FAIL | timezone import error | Code Error |
| 2 | SPY_Price | ✅ PASS | - | - |
| 10 | SPY_TA_Indicators | ✅ PASS | - | - |
| 12 | SPY_Full_TA | ❌ FAIL | Duplicate call to get_ta_indicators() | Logic Error (Duplicate Tool Call) |
| ... | ... | ... | ... | ... |

**Failure Types:**
- Code Error: Syntax/runtime errors, import errors
- Logic Error (Duplicate Tool Call): Agent made unnecessary redundant API calls
- Logic Error (Wrong Tool): Agent called wrong tool for the query
- Data Error: Wrong data returned, cross-ticker contamination
- Response Error: Incomplete response, doesn't address query

#### **Step 4: Final Checkpoint Questions**

Answer ALL checkpoint questions with evidence:

1. ✅ Did you READ all 39 test responses manually using the Read tool? **YES/NO**
2. ✅ Did you apply all 4 verification criteria to EACH test? **YES/NO**
3. ✅ How many tests PASSED all 4 criteria? **X/39 PASSED**
4. ✅ How many tests FAILED (any criterion)? **X/39 FAILED**
5. ✅ Did you document ALL failures with test #, issue, and failure type? **YES/NO + TABLE**

**🔴 CANNOT MARK TASK COMPLETE WITHOUT:**
- Reading all 39 test responses manually (using Read tool, NOT grep)
- Applying all 4 verification criteria to each test
- Documenting ALL 39 tests in a results table
- Providing failure count and failure details table
- Answering all 5 checkpoint questions with evidence

---

## Test Success Criteria

### ✅ Phase 1 Success
- [x] All 39 tests COMPLETED
- [x] Average response time < 30s
- [x] No timeouts or crashes
- [x] Test report generated

### ✅ Phase 2 Success
- [x] All 39 tests manually reviewed using Read tool
- [x] All 4 verification criteria applied to each test
- [x] All failures documented (or 0 failures confirmed)
- [x] All 5 checkpoint questions answered
- [x] Evidence provided for each answer

### ✅ Overall Test Success
- [x] Phase 1: 39/39 COMPLETED
- [x] Phase 2: X/39 PASS (with documented failures if any)
- [x] No functional impact on application
- [x] Ready for production deployment (if 39/39 PASS)

---

## Test Report Location & Format

### Report File
```
test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log
```

### Report Contents
- Test execution timestamp
- Total tests: 39
- Completed: X/39
- Average response time
- Performance rating
- Individual test results with responses, tool calls, performance metrics

### Reading the Report

**Manual review (REQUIRED):**
```bash
# Use Read tool to read test sections manually
# Example: Read lines 100-200 for Tests 1-3
Read file_path="/path/to/test-reports/test_cli_regression_loop1_*.log" offset=100 limit=100
```

**Quick error check (NOT SUFFICIENT for verification):**
```bash
# Find potential errors (but may miss logic errors!)
grep -i "error\|unavailable\|RuntimeWarning" test-reports/test_cli_regression_loop1_*.log

# Count occurrences (informational only)
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

🔴 **IMPORTANT:** Grep commands alone are NOT sufficient for Phase 2 verification. They miss duplicate tool calls and logic errors. You MUST manually review all 39 tests.

---

## Pytest (Unit Tests)

### Running Unit Tests
```bash
uv run pytest tests/ -v
```

### Test Organization
```
tests/
├── test_tools.py          # Tool function tests
├── test_utils.py          # Utility function tests
└── test_cli.py            # CLI core tests
```

### Common Assertions
```python
import pytest

async def test_process_query():
    """Test query processing."""
    agent = initialize_test_agent()
    session = SQLiteSession(":memory:")
    
    result = await process_query(agent, session, "test query")
    
    # Assertions
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
    assert "error" not in result.lower()

def test_format_response():
    """Test response formatting."""
    response = format_response("test", 123.45)
    
    assert "test" in response
    assert "123.45" in response
    assert "\n" in response
```

---

## Debugging Failed Tests

### If Test Hangs
```bash
# Kill hanging process
pkill -f "cli.py"

# Check port 8000
netstat -tlnp | grep 8000

# If port in use, kill it
lsof -ti :8000 | xargs kill -9
```

### If Test Times Out
- Response time > 60s = timeout
- Check API key validity
- Check network connectivity
- Check Polygon/Tradier APIs are responding

### If Test Returns Error
- Review test log for exact error message
- Check if API returned error
- Verify ticker symbols are valid
- Check date parameters are correct

### If Test Has Duplicate Tool Calls
- Review conversation history in test log
- Check if previous test already retrieved the data
- Agent should reuse data from conversation context
- File issue if agent makes unnecessary API calls

### View Raw CLI Output
```bash
# During test execution, monitor:
tail -f tmp/cli_output_loop1_*.log

# After test execution, review:
cat tmp/cli_output_loop1_2025-10-18_11-24.log
```

---

## Continuous Testing Workflow

### Before Each Commit
```bash
# 1. Auto-fix code style
npm run lint:fix

# 2. Run full test suite (Phase 1)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# 3. Run Phase 2 verification (MANDATORY MANUAL REVIEW)
# - Use Read tool to read all 39 test responses
# - Apply 4-point criteria to each test
# - Document results in table
# - Answer all 5 checkpoint questions

# 4. If all tests PASS Phase 2, commit changes
git add -A
git commit -m "message"
```

### Performance Monitoring
```bash
# Compare response times
echo "Baseline: 8.21s"
echo "Current:"
grep "Average Response Time" test-reports/test_cli_regression_loop1_*.log

# Alert if degradation > 10%
# 8.21s * 1.1 = 9.03s (acceptable)
# > 9.03s = performance degradation
```

---

## Test Environment

### System Info
```bash
# Python version
python3 --version  # Python 3.12.3

# uv version
uv --version       # uv 0.8.19

# Dependencies
uv pip list        # Show installed packages
```

### API Keys Required
```bash
# Must be set in .env
POLYGON_API_KEY=
OPENAI_API_KEY=
TRADIER_API_KEY=
```

---

## Troubleshooting Tests

| Issue | Cause | Solution |
|-------|-------|----------|
| 0/39 COMPLETED | API key invalid | Check .env file |
| Timeout (>60s) | API slow response | Wait and retry |
| "error unavailable" | Market data issue | Verify ticker symbols |
| Port 8000 in use | Gradio still running | Kill process: `pkill -f gradio` |
| Import errors | Wrong Python version | Use Python 3.12+ |
| Memory errors | Too many tests | Run smaller subset |
| Duplicate tool calls | Agent not reusing data | Logic error - review agent instructions |
| Cross-ticker data | Data contamination | Code error - review tool implementations |

---

**Last Updated:** October 19, 2025
**Test Suite:** 39 tests (EXCELLENT performance)
**Expected:** < 10s average response time
**Verification Method:** Manual review of all 39 tests (NO grep shortcuts)
**Status:** ✅ Process documented
