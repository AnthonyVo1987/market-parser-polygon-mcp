# Testing Procedures and Validation

## Test Scripts Available

### 1. Persistent Session Test (RECOMMENDED)
**Script:** `test_7_prompts_persistent_session.sh`

**Purpose:** Tests all 7 standardized prompts in a SINGLE CLI session with proper session persistence validation.

**Features:**
- ✅ All 7 tests run sequentially in ONE session
- ✅ Accurate response time tracking (30-90s responses)
- ✅ Session persistence validation (verifies count = 1)
- ✅ No false failure detection
- ✅ Comprehensive test reports

**Usage:**
```bash
./test_7_prompts_persistent_session.sh
```

**Expected Execution:**
- Duration: 2-5 minutes (all 7 tests)
- Session count: 1 (verified)
- Success rate: 100% (7/7 tests pass)
- Response times: 6-31s per test (varies with API)

**Test Results (3 Validation Runs):**

| Run | Tests Passed | Session Count | Avg Response Time | Total Duration | Performance |
|-----|--------------|---------------|-------------------|----------------|-------------|
| 1 | 7/7 (100%) | 1 ✅ | 20.49s | 146.74s | EXCELLENT |
| 2 | 7/7 (100%) | 1 ✅ | 18.00s | 129.26s | EXCELLENT |
| 3 | 7/7 (100%) | 1 ✅ | 15.29s | 109.55s | EXCELLENT |

**Consistency:** 100% pass rate across all 3 validation runs

### 2. Legacy Test Script (NOT RECOMMENDED)
**Script:** `test_7_prompts_comprehensive.sh`

**Issues:**
- ❌ Runs each test in SEPARATE CLI session (7 sessions total)
- ❌ Incorrect response time calculation
- ❌ Does not test session persistence
- ❌ Not representative of actual user behavior

**DO NOT USE** - Kept for reference only

## The 7 Standardized Test Prompts

Based on `tests/playwright/test_prompts.md`:

1. **Test 1 - Market Status Query**
   - Prompt: "What the current Market Status, Date, & Time: Open, Closed, After-Hours, Pre-market, Overnight?"
   - Expected: Market status, date, time information
   - Typical Response Time: 19-21s

2. **Test 2 - Single Stock Snapshot (NVDA)**
   - Prompt: "Single Stock Snapshot Price NVDA"
   - Expected: NVDA price, change, volume, day range
   - Typical Response Time: 23-31s

3. **Test 3 - Full Market Snapshot (SPY/QQQ/IWM)**
   - Prompt: "Full Market Snapshot Price: SPY, QQQ, IWM"
   - Expected: Prices for all 3 major ETFs
   - Typical Response Time: 17-23s

4. **Test 4 - Closing Price Query (GME)**
   - Prompt: "GME closing price today"
   - Expected: GME closing price
   - Typical Response Time: 17-20s

5. **Test 5 - Performance Analysis (SOUN)**
   - Prompt: "SOUN Price performance this week"
   - Expected: Weekly performance metrics
   - Typical Response Time: 13-16s

6. **Test 6 - Support/Resistance (NVDA)**
   - Prompt: "NVDA Price Support & Resistance Levels"
   - Expected: Technical support/resistance levels
   - Typical Response Time: 7-13s

7. **Test 7 - Technical Analysis (SPY)**
   - Prompt: "SPY Price Technical Analysis"
   - Expected: Technical analysis metrics
   - Typical Response Time: 6-21s

## Test Output Files

**Location:** `test-reports/`

**Naming Convention:**
- Persistent Session: `persistent_session_test_YYYYMMDD_HHMMSS.txt`
- Legacy Script: `comprehensive_7_prompts_test_YYYYMMDD_HHMMSS.txt`

**Report Contents:**
- Test execution timestamp
- Individual test results with response times
- Performance classification (EXCELLENT/GOOD/ACCEPTABLE/SLOW)
- Session persistence validation
- Response time statistics (min/max/avg)
- Overall performance rating
- Full CLI output for debugging

## Performance Benchmarks

### Response Time Classification

| Category | Time Range | Rating |
|----------|-----------|--------|
| EXCELLENT | < 30s | ✅ Expected for most queries |
| GOOD | 30-45s | ✅ Acceptable for complex queries |
| ACCEPTABLE | 45-90s | ⚠️ May need optimization |
| SLOW | > 90s | ❌ Needs investigation |

### Expected Performance

**Average Response Time:** 15-20s
**Min Response Time:** 6-8s (simple queries)
**Max Response Time:** 25-32s (complex multi-stock queries)
**Total Session Duration:** 110-150s for all 7 tests

## Session Persistence Validation

**How It Works:**
1. Script counts occurrences of "CLI session 'cli_session' initialized"
2. Expected count: 1 (all tests in same session)
3. If count > 1: Session persistence FAILED
4. If count = 1: Session persistence VERIFIED ✅

**Why It Matters:**
- Real users have persistent chat sessions
- Testing must match actual usage patterns
- Session context should be maintained across queries
- Separate sessions don't test conversation memory

## Running Tests

### Quick Test
```bash
./test_7_prompts_persistent_session.sh
```

### Sanity Check (3 Runs)
```bash
./test_7_prompts_persistent_session.sh
./test_7_prompts_persistent_session.sh
./test_7_prompts_persistent_session.sh
```

### Viewing Results
```bash
# List recent test reports
ls -lt test-reports/persistent_session_test_*.txt | head -5

# View specific report
cat test-reports/persistent_session_test_20251004_140707.txt

# View raw CLI output
cat /tmp/cli_output_20251004_140707.log
```

## Troubleshooting

### Issue: Test Timeout
**Cause:** Response times > 120s (max configured)
**Solution:** Increase MAX_RESPONSE_TIME in script or check API connectivity

### Issue: Session Count > 1
**Cause:** CLI is restarting between prompts
**Solution:** Verify input file has all prompts with single "exit" at end

### Issue: Missing Response Times
**Cause:** CLI output format changed
**Solution:** Check raw output log, update parsing logic if needed

### Issue: Tests Fail
**Cause:** API errors, connectivity issues, or CLI crashes
**Solution:** Check raw output log for error messages, verify API keys in .env

## Integration with Development Workflow

### When to Run Tests

**Required:**
- Before committing changes to CLI or backend
- After modifying agent service or MCP integration
- Before creating pull requests
- After updating OpenAI Agents SDK

**Recommended:**
- After changing prompt templates
- After modifying API models or response formatting
- During performance optimization work
- When investigating user-reported issues

### Pre-Commit Checklist

See `task_completion_checklist.md` for full checklist. Testing requirements:

```bash
# Run persistent session test
./test_7_prompts_persistent_session.sh

# Verify all 7 tests pass
# Verify session count = 1
# Check performance ratings (most should be EXCELLENT)
```

## Test Script Implementation Details

### Input File Generation
```bash
# Creates single input file with all prompts
for prompt in "${prompts[@]}"; do
    echo "$prompt" >> "$INPUT_FILE"
done
echo "exit" >> "$INPUT_FILE"  # Only one exit at the end
```

### CLI Execution
```bash
# Single CLI invocation with all prompts
$CLI_CMD < "$INPUT_FILE" > "$RAW_OUTPUT" 2>&1 &
CLI_PID=$!
wait $CLI_PID
```

### Response Time Extraction
```bash
# Parse output for response times
while IFS= read -r line; do
    if echo "$line" | grep -q "Response Time:"; then
        rt=$(echo "$line" | grep -o '[0-9]\+\.[0-9]\+' | head -1)
        response_times+=("$rt")
    fi
done < "$RAW_OUTPUT"
```

### Session Validation
```bash
# Count session initializations
session_count=$(grep -c "CLI session 'cli_session' initialized" "$RAW_OUTPUT")
if [ "$session_count" -eq 1 ]; then
    echo "✅ Session Persistence: VERIFIED"
fi
```

## Future Enhancements

Potential improvements for testing infrastructure:

1. **Parallel Testing** - Run multiple test suites concurrently
2. **Performance Regression Detection** - Alert if avg response time increases
3. **API Mocking** - Test without live API calls for faster iteration
4. **CI/CD Integration** - Automated testing on push/PR
5. **Historical Trending** - Track performance metrics over time
6. **Load Testing** - Test concurrent user scenarios
7. **Error Injection** - Test error handling and recovery

## API Usage Considerations

**Note:** Each test run makes 7 real API calls to:
- Polygon.io (financial data)
- OpenAI (GPT-5-Nano)

**Cost Implications:**
- Polygon.io: Counts toward API rate limits
- OpenAI: Tokens consumed (avg ~35,000 per full test run)

**Best Practice:** Run tests when needed, not continuously. Use mocked data for frequent development testing.