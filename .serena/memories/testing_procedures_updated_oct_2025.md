# Testing Procedures - Updated October 2025

**Status:** Current with 39-test suite and Phase 2 verification
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

**Current Baseline (Oct 18, 2025):** 9.56s average (EXCELLENT)

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
- ❌ Does NOT check tool calls
- ❌ Does NOT validate data formatting

**Success criteria:**
- 39/39 responses generated
- Average response time < 30s
- No timeouts

**Output:**
```
39/39 COMPLETED
Average Response Time: 9.56s
```

### Phase 2: Manual Verification (MANUAL - MANDATORY)

**Phase 2a: Error Detection (MANDATORY GREP COMMANDS)**

Run these 3 commands and SHOW output:

```bash
# Command 1: Find all errors/failures
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log

# Command 2: Count 'data unavailable' errors
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log

# Command 3: Count completed tests
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Expected results:**
- Command 1: Zero matches (no errors)
- Command 2: 0 (zero "data unavailable" errors)
- Command 3: 40 (39 tests + 1 summary line)

**If errors found:**
Create failure table with evidence:

| Test # | Test Name | Line # | Error Message | Tool Call |
|--------|-----------|--------|---------------|-----------|
| 3 | SPY_Yesterday_OHLC | 157 | data unavailable | get_stock_price(...) |

**Phase 2b: Document Failures**

If errors found in Phase 2a:
- Document exact error message
- Record line number
- Identify failed tool call
- Create failure table with evidence

If NO errors found:
- Explicitly state: "✅ 0 failures found"
- Confirm: "All grep commands returned zero errors"

**Phase 2c: Verify Response Correctness**

For each test response, verify:
1. ✅ Response directly addresses prompt query
2. ✅ Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
3. ✅ Appropriate tool calls made (Polygon, Tradier)
4. ✅ Data formatting correct (OHLC, tables, etc.)
5. ✅ No hallucinated data or made-up values
6. ✅ Options chains show Bid/Ask columns (NOT midpoint)
7. ✅ Technical analysis includes proper indicators
8. ✅ Response is complete (not truncated)

**Phase 2d: Answer Checkpoint Questions**

All 5 must be answered with evidence:

1. **Did you RUN the 3 mandatory grep commands?**
   - Answer: YES/NO
   - Evidence: [Paste all grep outputs]

2. **Did you DOCUMENT all failures found?**
   - Answer: YES/NO
   - Evidence: [Show failure table OR "0 failures"]

3. **Failure count from grep -c "data unavailable":**
   - Answer: [X failures]
   - Evidence: [Show grep -c output]

4. **Tests that generated responses:**
   - Answer: [X/39 COMPLETED]
   - Evidence: [Show grep -c "COMPLETED" output]

5. **Tests that PASSED verification:**
   - Answer: [X/39 PASS]
   - Evidence: [39 minus failure count]

---

## Test Success Criteria

### ✅ Phase 1 Success
- [x] All 39 tests COMPLETED
- [x] Average response time < 30s
- [x] No timeouts or crashes
- [x] Test report generated

### ✅ Phase 2 Success
- [x] All 3 grep commands executed
- [x] Grep output documented
- [x] All failures identified (or 0 failures confirmed)
- [x] All 5 checkpoint questions answered
- [x] Evidence provided for each answer

### ✅ Overall Test Success
- [x] Phase 1: 39/39 COMPLETED
- [x] Phase 2: 39/39 PASS (0 errors detected)
- [x] No functional impact on application
- [x] Ready for production deployment

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
- Failed: 0
- Average response time: 9.56s
- Performance rating: EXCELLENT
- Individual test results with response times

### Reading the Report
```bash
# View full report
cat test-reports/test_cli_regression_loop1_2025-10-18_11-24.log

# Find specific test
grep "Test 15" test-reports/test_cli_regression_loop1_*.log

# Count errors
grep -i "error\|unavailable" test-reports/test_cli_regression_loop1_*.log | wc -l
```

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
- Review grep output for exact error message
- Check if API returned error
- Verify ticker symbols are valid
- Check date parameters are correct

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

# 3. Run Phase 2 verification (manual)
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log

# 4. If all green, commit changes
git add -A
git commit -m "message"
```

### Performance Monitoring
```bash
# Compare response times
echo "Baseline: 9.56s"
echo "Current:"
grep "Average Response Time" test-reports/test_cli_regression_loop1_*.log

# Alert if degradation > 10%
# 9.56s * 1.1 = 10.52s (acceptable)
# > 10.52s = performance degradation
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

---

**Last Updated:** October 18, 2025
**Test Suite:** 39 tests (EXCELLENT performance)
**Expected:** < 10s average response time
**Status:** ✅ All tests passing
