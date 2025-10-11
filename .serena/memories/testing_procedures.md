# Testing Procedures and Validation

## Primary Test Script

### CLI Regression Test Suite (RECOMMENDED)
**Script:** `test_cli_regression.sh`

**Purpose:** Tests all 40 standardized prompts in a SINGLE CLI session with proper session persistence validation.

**Features:**
- ✅ All 40 tests run sequentially in ONE session
- ✅ Accurate response time tracking with awk-based calculations (reliable across all systems)
- ✅ Session persistence validation
- ✅ Comprehensive test reports with formatted output
- ✅ Performance classification
- ✅ Configurable loop count (1-10 runs)
- ✅ 2 decimal precision for all statistics
- ✅ Human-readable duration format (MM min SS sec)
- ✅ Dynamic relative dates (no hardcoded dates requiring updates)

**Usage:**
```bash
# Single test loop (40 tests)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Multiple test loops (e.g., 10 loops for baseline)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 10
```

**Test Coverage (40 tests total - Updated Oct 10, 2025):**

1. **SPY Test Sequence (Tests 1-17 - 17 tests)**:
   - Market Status
   - Current Price: $SPY
   - Today's Closing Price: $SPY
   - Yesterday's Closing Price: $SPY
   - Last week's Performance: $SPY
   - Stock Price on the previous week's Friday: $SPY (dynamic date)
   - Daily Stock Price bars Analysis from the last 2 trading weeks: $SPY (dynamic date)
   - RSI-14: $SPY
   - MACD: $SPY
   - SMA 20/50/200: $SPY
   - EMA 20/50/200: SPY
   - Support & Resistance Levels: $SPY
   - Technical Analysis: $SPY
   - **Get options expiration dates for SPY** (NEW Oct 10, 2025 - Test 14)
   - Get the SPY Call Options Chain Expiring this Friday (Test 15)
   - Get the SPY Put Options Chain Expiring this Friday (Test 16)
   - Analyze the Options Chain Data for SPY and provide potential Call & Put Wall(s) Strike Prices (Test 17)

2. **NVDA Test Sequence (Tests 18-34 - 17 tests)**:
   - Same pattern as SPY (17 tests)
   - Market Status through Technical Analysis (Tests 18-30)
   - **Get options expiration dates for NVDA** (NEW Oct 10, 2025 - Test 31)
   - Get the NVDA Call Options Chain Expiring this Friday (Test 32)
   - Get the NVDA Put Options Chain Expiring this Friday (Test 33)
   - Analyze the Options Chain Data for NVDA and provide potential Call & Put Wall(s) Strike Prices (Test 34)

3. **Multi-Ticker Test Sequence (Tests 35-40 - 6 tests)**:
   - Market Status
   - Current Price: $WDC, $AMD, $GME
   - Today's Closing Price: $WDC, $AMD, $GME
   - Yesterday's Closing Price: $WDC, $AMD, $GME
   - Last week's Performance: $WDC, $AMD, $GME
   - Daily bars Analysis from the last 2 trading weeks: $WDC, $AMD, $GME

**Expected Performance (Oct 10, 2025 - With Tradier Tool):**
- **Total Tests**: 40 per loop
- **Average Response Time**: 11.03s (EXCELLENT)
- **Performance Range**: 2.607s - 31.846s
- **Success Rate**: 100% (40/40 in validation)
- **Total Duration**: ~7 minutes per loop (40 tests)

**LATEST: Single-Loop Performance (Oct 10, 2025):**

| Loop | Tests Passed | Success Rate | Avg Response Time | Duration | Performance Rating |
|------|--------------|--------------|-------------------|----------|-------------------|
| 1 | 40/40 | 100% | 11.03s | 7 min 22 sec | EXCELLENT |

**Single-Loop Summary:**
- **Total Tests**: 40/40 PASSED (100%)
- **Overall Average**: 11.03s per query
- **Performance Rating**: EXCELLENT (< 20s threshold)
- **Test Execution Date**: October 10, 2025, 7:25 PM
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-10_19-25.log`
- **New Tests**: Tradier options expiration dates (Test 14: 8.596s, Test 31: 14.511s)

**Tradier Tool Integration (Oct 10, 2025):**
- **New Tool**: `get_options_expiration_dates` via Tradier Brokerage API
- **Test 14**: SPY Options Expiration Dates - PASS (8.596s, EXCELLENT)
- **Test 31**: NVDA Options Expiration Dates - PASS (14.511s, EXCELLENT)
- **Validation**: 40/40 tests PASSED with 11.03s avg (EXCELLENT rating)
- **Quick Tests**: SPY (31 dates), NVDA (21 dates), SOUN (11 dates) - All PASS

**Test Suite Evolution:**
- **Oct 8, 2025**: 36 tests (SPY 15 + NVDA 15 + Multi 6) - Service tier change to "default"
- **Oct 9, 2025**: 38 tests (SPY 16 + NVDA 16 + Multi 6) - Added options chain wall analysis tests
- **Oct 10, 2025**: 40 tests (SPY 17 + NVDA 17 + Multi 6) - Added Tradier expiration dates tests

## Test Script Implementation Details

### Calculation Engine (Critical: Oct 6, 2025 Fix)

**IMPORTANT:** The test script uses `awk` for ALL floating-point calculations to ensure universal compatibility across systems. DO NOT use `bc` (bash calculator) as it is not universally available.

**Why awk?**
- ✅ Universally available on all Unix/Linux systems
- ✅ Reliable floating-point arithmetic
- ✅ Never fails silently (unlike bc when missing)
- ✅ Consistent precision control

**Calculation Patterns Used:**

```bash
# Duration calculation (total test execution time)
total_duration=$(awk "BEGIN {printf \"%.2f\", $end_time - $start_time}")

# Duration formatting (convert to MM min SS sec)
duration_minutes=$(awk "BEGIN {printf \"%d\", $total_duration / 60}")
duration_seconds=$(awk "BEGIN {printf \"%d\", $total_duration % 60}")
duration_formatted="${duration_minutes} min ${duration_seconds} sec"

# Boolean comparison (e.g., for min/max detection)
if (( $(awk "BEGIN {print ($time < $min_time)}") )); then
    min_time=$time
fi

# Floating-point arithmetic with 2 decimal precision
total_time=$(awk "BEGIN {printf \"%.2f\", $total_time + $time}")

# Average calculation
avg_time=$(awk "BEGIN {printf \"%.2f\", $total_time / $count}")
```

**Historical Bug (Fixed Oct 6, 2025):**
- **Issue**: Script originally used `bc` for calculations, which silently failed when `bc` was not installed
- **Symptoms**: Total Duration: 0s, Avg Response Time: 0s, Min/Max stuck at same value
- **Root Cause**: `bc` not available on system, all `bc` calculations returned "0" or kept old values
- **Fix**: Replaced ALL `bc` usage with `awk` (14+ calculation points across 5 critical areas)
- **Validation**: 3-loop test confirmed all calculations working correctly, 10-loop test further validated accuracy

### Output Formatting (Oct 6, 2025 Enhancement)

**Precision:** All decimal values limited to 2 decimal places for readability
```bash
# Response time formatting
printf "%.2f" $response_time  # Output: 10.44s (not 10.443s)

# Statistical calculations
avg_time=$(awk "BEGIN {printf \"%.2f\", $total_time / $count}")
```

**Duration Format:** Human-readable "MM min SS sec" format
```bash
# Before (hard to read):
Total Session Duration: 442.010s

# After (human-readable):
Total Session Duration: 7 min 22 sec
```

### Input File Generation (Updated Oct 10, 2025)
```bash
# Array of all 40 prompts organized by ticker
prompts=(
    # SPY Test Sequence (Tests 1-17)
    "Market Status"
    "Current Price: \$SPY"
    "Today's Closing Price: \$SPY"
    # ... 10 more SPY tests ...
    "Technical Analysis: \$SPY"
    "Get options expiration dates for SPY"  # NEW Oct 10
    "Get the SPY Call Options Chain Expiring this Friday"
    "Get the SPY Put Options Chain Expiring this Friday"
    "Analyze the Options Chain Data for SPY and provide potential Call & Put Wall(s) Strike Prices"
    
    # NVDA Test Sequence (Tests 18-34)
    "Market Status"
    "Current Price: \$NVDA"
    # ... 11 more NVDA tests ...
    "Technical Analysis: \$NVDA"
    "Get options expiration dates for NVDA"  # NEW Oct 10
    "Get the NVDA Call Options Chain Expiring this Friday"
    "Get the NVDA Put Options Chain Expiring this Friday"
    "Analyze the Options Chain Data for NVDA and provide potential Call & Put Wall(s) Strike Prices"
    
    # Multi-Ticker Test Sequence (Tests 35-40)
    "Market Status"
    "Current Price: \$WDC, \$AMD, \$GME"
    # ... 4 more multi-ticker tests ...
)

# Create single input file
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

# Wait for completion with timeout
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

### Performance Classification
```bash
# Classify each response time using awk for comparison
if (( $(awk "BEGIN {print ($rt < 30)}") )); then
    classification="EXCELLENT"
elif (( $(awk "BEGIN {print ($rt < 45)}") )); then
    classification="GOOD"
elif (( $(awk "BEGIN {print ($rt < 90)}") )); then
    classification="ACCEPTABLE"
else
    classification="SLOW"
fi
```

## The 40 Standardized Test Prompts (Updated Oct 10, 2025)

### SPY Test Sequence (Tests 1-17)

1. **Market Status**
2. **Current Price: $SPY**
3. **Today's Closing Price: $SPY**
4. **Yesterday's Closing Price: $SPY**
5. **Last week's Performance: $SPY**
6. **Stock Price on the previous week's Friday: $SPY** (dynamic date)
7. **Daily Stock Price bars Analysis from the last 2 trading weeks: $SPY** (dynamic date)
8. **RSI-14: $SPY**
9. **MACD: $SPY**
10. **SMA 20/50/200: $SPY**
11. **EMA 20/50/200: SPY**
12. **Support & Resistance Levels: $SPY**
13. **Technical Analysis: $SPY**
14. **Get options expiration dates for SPY** (NEW Oct 10, 2025 - Tradier tool)
15. **Get the SPY Call Options Chain Expiring this Friday** (was Test 14 before Oct 10)
16. **Get the SPY Put Options Chain Expiring this Friday** (was Test 15 before Oct 10)
17. **Analyze the Options Chain Data for SPY and provide potential Call & Put Wall(s) Strike Prices** (was Test 16 before Oct 10, added Oct 9, 2025)

### NVDA Test Sequence (Tests 18-34)

18. **Market Status**
19. **Current Price: $NVDA**
20. **Today's Closing Price: $NVDA**
21. **Yesterday's Closing Price: $NVDA**
22. **Last week's Performance: $NVDA**
23. **Stock Price on the previous week's Friday: $NVDA** (dynamic date)
24. **Daily Stock Price bars Analysis from the last 2 trading weeks: $NVDA** (dynamic date)
25. **RSI-14: $NVDA**
26. **MACD: $NVDA**
27. **SMA 20/50/200: $NVDA**
28. **EMA 20/50/200: NVDA**
29. **Support & Resistance Levels: $NVDA**
30. **Technical Analysis: $NVDA**
31. **Get options expiration dates for NVDA** (NEW Oct 10, 2025 - Tradier tool)
32. **Get the NVDA Call Options Chain Expiring this Friday** (was Test 30 before Oct 10)
33. **Get the NVDA Put Options Chain Expiring this Friday** (was Test 31 before Oct 10)
34. **Analyze the Options Chain Data for NVDA and provide potential Call & Put Wall(s) Strike Prices** (was Test 32 before Oct 10, added Oct 9, 2025)

### Multi-Ticker Test Sequence (Tests 35-40)

35. **Market Status** (was Test 33 before Oct 10)
36. **Current Price: $WDC, $AMD, $GME** (was Test 34 before Oct 10)
37. **Today's Closing Price: $WDC, $AMD, $GME** (was Test 35 before Oct 10)
38. **Yesterday's Closing Price: $WDC, $AMD, $GME** (was Test 36 before Oct 10)
39. **Last week's Performance: $WDC, $AMD, $GME** (was Test 37 before Oct 10)
40. **Daily bars Analysis from the last 2 trading weeks: $WDC, $AMD, $GME** (was Test 38 before Oct 10)

**Note:** GME replaced INTC in multi-ticker sequence for better test coverage (Oct 8, 2025).

## New Test Cases

### Tradier Options Expiration Dates Tests (Added Oct 10, 2025)

**Test 14: SPY Options Expiration Dates**
- **Prompt**: "Get options expiration dates for SPY"
- **Purpose**: Validate Tradier tool fetches ALL available expiration dates for SPY
- **Expected Output**: List of dates in YYYY-MM-DD format with count and source
- **Test Results**: PASS (8.596s response time, EXCELLENT)
- **Data**: 31 expiration dates (includes weekly and monthly)

**Test 31: NVDA Options Expiration Dates**
- **Prompt**: "Get options expiration dates for NVDA"
- **Purpose**: Validate Tradier tool fetches ALL available expiration dates for NVDA
- **Expected Output**: List of dates in YYYY-MM-DD format with count and source
- **Test Results**: PASS (14.511s response time, EXCELLENT)
- **Data**: 21 expiration dates (includes weekly and monthly)

**Tradier Tool Details**:
- **Tool**: `get_options_expiration_dates`
- **API**: Tradier Brokerage API `/v1/markets/options/expirations`
- **Authentication**: Bearer token via TRADIER_API_KEY
- **Response Format**: JSON with expiration_dates array
- **Date Format**: YYYY-MM-DD (ISO 8601)
- **Sorting**: Chronologically (earliest to latest)
- **Data Updates**: Daily from Tradier

**Quick Validation Tests**:
- SPY: 31 expiration dates, 9.844s - PASS
- NVDA: 21 expiration dates, 6.842s - PASS
- SOUN: 11 expiration dates, 6.391s - PASS

### Options Chain Wall Analysis Tests (Added Oct 9, 2025)

**Test 17: SPY Options Chain Wall Analysis** (was Test 16 before Oct 10)
- **Prompt**: "Analyze the Options Chain Data for SPY and provide potential Call & Put Wall(s) Strike Prices"
- **Purpose**: Validate AI Agent can identify support/resistance levels from options chain data
- **Expected Output**: Call walls (resistance), Put walls (support), strike prices with OI/volume data

**Test 34: NVDA Options Chain Wall Analysis** (was Test 32 before Oct 10)
- **Prompt**: "Analyze the Options Chain Data for NVDA and provide potential Call & Put Wall(s) Strike Prices"
- **Purpose**: Validate AI Agent can identify support/resistance levels from options chain data
- **Expected Output**: Call walls (resistance), Put walls (support), strike prices with OI/volume data

## Test Output Files

**Location:** `test-reports/`

**Naming Convention:**
- Single loop: `test_cli_regression_loopN_YYYY-MM-DD_HH-MM.log`
- Example: `test_cli_regression_loop1_2025-10-10_19-25.log`

**Report Contents:**
- Test execution timestamp
- Loop number (if multi-loop)
- Individual test results with response times (2 decimal precision)
- Performance classification per test (EXCELLENT/GOOD/ACCEPTABLE/SLOW)
- Response time statistics (min/max/avg, 2 decimal places)
- Total session duration (MM min SS sec format)
- Overall performance rating
- Full CLI output for debugging

**Example Report (Oct 10, 2025 Format):**
```
=== CLI REGRESSION TEST REPORT (Loop 1/1) ===
Timestamp: Fri Oct 10 19:25:58 PDT 2025
Loop Number: 1/1
Total Tests: 40
Passed: 40
Failed: 0
Success Rate: 100%
Total Session Duration: 7 min 22 sec
Session Mode: PERSISTENT (single session)
Session Count Detected: 1
Loop Status: PASS

=== RESPONSE TIME ANALYSIS ===
Min Response Time: 2.61s
Max Response Time: 31.85s
Avg Response Time: 11.03s
Performance Rating: EXCELLENT

=== DETAILED TEST RESULTS ===
✅ Test 1 PASSED (5.03s) - EXCELLENT
✅ Test 2 PASSED (6.96s) - EXCELLENT
...
✅ Test 14 PASSED (8.60s) - EXCELLENT (NEW: SPY expiration dates)
...
✅ Test 31 PASSED (14.51s) - EXCELLENT (NEW: NVDA expiration dates)
...
✅ Test 40 PASSED (29.14s) - EXCELLENT
```

## Performance Benchmarks

### Response Time Classification

| Category | Time Range | Rating |
|----------|-----------|--------|
| EXCELLENT | < 30s | ✅ Expected for all queries |
| GOOD | 30-45s | ✅ Acceptable for complex queries |
| ACCEPTABLE | 45-90s | ⚠️ May need optimization |
| SLOW | > 90s | ❌ Needs investigation |

**Note:** EXCELLENT threshold is < 30s to accommodate the 40-test structure and service_tier "default" characteristics.

### Expected Performance (Oct 10, 2025 - With Tradier Tool)

**Individual Query Performance:**
- **Average**: 11.03s
- **Min**: 2.607s (simple queries)
- **Max**: 31.846s (complex multi-stock queries)
- **Rating**: EXCELLENT (< 30s threshold, 39/40 tests; 1 test at 31.8s GOOD)

**New Tradier Tool Performance:**
- **Test 14 (SPY)**: 8.596s (EXCELLENT)
- **Test 31 (NVDA)**: 14.511s (EXCELLENT)
- **Quick Tests**: 6.391s - 9.844s range (all EXCELLENT)

**Full Test Suite (40 tests):**
- **Duration**: ~7-8 minutes per loop
- **Success Rate**: 100%
- **Consistency**: Highly consistent

### Performance Trends

**Tradier Tool Integration (Oct 10, 2025):**
- **New Tool**: get_options_expiration_dates (1 tool, total 12→13)
- **New Tests**: 2 tests added (38→40 total)
- **Performance Impact**: Minimal (11.03s avg vs 11.05s baseline)
- **Validation**: 40/40 PASSED, 100% success rate

**Test Suite Restructuring Impact:**
- **Oct 8, 2025**: 36 tests (SPY 15 + NVDA 15 + Multi 6)
- **Oct 9, 2025**: 38 tests (SPY 16 + NVDA 16 + Multi 6) - Added wall analysis
- **Oct 10, 2025**: 40 tests (SPY 17 + NVDA 17 + Multi 6) - Added Tradier expiration dates

**Service Tier Change Impact (Oct 8, 2025):**
- **Before** (service_tier: "flex"): Rate limiting issues during prototyping
- **After** (service_tier: "default"): 36/36 PASSED, 10.44s avg, EXCELLENT rating
- **Reason**: "default" tier provides better performance for prototyping phase

**Architecture Milestones:**
- **Phase 4 Complete**: All tools migrated to Direct API
- **Phase 10 Complete**: Persistent Agent Architecture (50% token savings)
- **Phase 11 Complete**: Tradier Options Expiration Dates Tool (Oct 10, 2025)
- **MCP Server**: Completely removed
- **Performance**: 70% faster than legacy MCP architecture
- **Service Tier**: Optimized for prototyping (default tier)
- **Test Suite**: Restructured for sustainability (dynamic dates)

## Session Persistence Validation

**How It Works:**
1. Script creates single input file with all 40 prompts
2. Single CLI invocation processes all prompts
3. Script verifies session initialized only once
4. Expected: Session persists throughout all tests

**Validation Check:**
```bash
# Count session initializations in output
session_count=$(grep -c "CLI session 'cli_session' initialized" "$RAW_OUTPUT")

if [ "$session_count" -eq 1 ]; then
    echo "✅ Session Persistence: VERIFIED"
else
    echo "❌ Session Persistence: FAILED (count=$session_count)"
fi
```

**Why It Matters:**
- Real users have persistent chat sessions
- Testing must match actual usage patterns
- Session context maintained across queries
- Conversation memory tested

**Validation Status:** ✅ VERIFIED (40/40 tests in single session)

## Running Tests

### Quick Test (Single Loop - RECOMMENDED)
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

### Performance Validation (3 Loops)
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 3
```

### Performance Baseline (10 Loops - Comprehensive)
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 10
```

### Custom Loop Count
```bash
# 5 loops
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 5
```

### Viewing Results
```bash
# List recent test reports
ls -lt test-reports/test_cli_regression_*.log | head -5

# View specific report
cat test-reports/test_cli_regression_loop1_2025-10-10_19-25.log

# View latest report
cat $(ls -t test-reports/test_cli_regression_*.log | head -1)
```

## Troubleshooting

### Issue: Incorrect Calculations (Total Duration: 0s, Avg: 0s)
**Cause:** Missing `bc` dependency or using unreliable calculation method
**Solution:**
- ✅ **FIXED (Oct 6, 2025)**: Script now uses `awk` for all calculations
- ✅ No external dependencies required
- ✅ Works universally across all systems
- ✅ Validated with comprehensive testing

**Historical Note:** Earlier versions used `bc` which failed silently when not installed. All `bc` usage has been replaced with `awk` for reliability.

### Issue: Test Timeout
**Cause:** Response times > 120s (max configured)
**Solution:**
- Increase MAX_RESPONSE_TIME in script
- Check API connectivity
- Verify API keys in .env (including TRADIER_API_KEY)

### Issue: Session Count > 1
**Cause:** CLI restarting between prompts
**Solution:**
- Verify input file has all prompts with single "exit" at end
- Check CLI_CMD variable is correct
- Review raw output log for restart indicators

### Issue: Missing Response Times
**Cause:** CLI output format changed
**Solution:**
- Check raw output log
- Update parsing logic in script
- Verify CLI performance metrics are enabled

### Issue: Tests Fail
**Cause:** API errors, connectivity issues, or CLI crashes
**Solution:**
- Check raw output log for error messages
- Verify API keys: `cat .env | grep API_KEY`
- Test API connectivity
- Check OpenAI API status
- Check Tradier API status
- Verify service_tier configuration in agent_service.py
- Verify TRADIER_API_KEY is set in .env

### Issue: Tradier Tool Errors
**Cause:** TRADIER_API_KEY not set, invalid ticker, or API issues
**Solution:**
- Verify TRADIER_API_KEY in .env: `cat .env | grep TRADIER_API_KEY`
- Test Tradier API connectivity: `curl -H "Authorization: Bearer $TRADIER_API_KEY" "https://api.tradier.com/v1/markets/options/expirations?symbol=SPY"`
- Check ticker symbol validity (must be valid US stock with options)
- Review raw output log for specific error messages

### Issue: Inconsistent Performance
**Cause:** Network latency, API load, service_tier configuration
**Solution:**
- Run 3-loop validation to get average
- Run 10-loop baseline for comprehensive data
- Check for outliers > 40s (may indicate API issues)
- Verify service_tier is set to "default" for prototyping

## Integration with Development Workflow

### When to Run Tests (MANDATORY)

**Required:**
- ✅ Before committing changes to CLI or backend
- ✅ After modifying agent service or tool integration
- ✅ Before creating pull requests
- ✅ After updating OpenAI Agents SDK
- ✅ After adding/modifying AI agent tools
- ✅ Before marking any task as "complete"
- ✅ After changing service_tier configuration
- ✅ After modifying test suite structure
- ✅ After adding new API integrations (e.g., Tradier)

**Recommended:**
- After changing prompt templates
- After modifying API models or response formatting
- During performance optimization work
- When investigating user-reported issues
- After dependency updates

### Pre-Commit Checklist

See `task_completion_checklist.md` for full checklist. Testing requirements:

```bash
# 1. Run CLI regression test (single loop minimum, 3-loop recommended)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# 2. Verify results
# - All 40/40 tests PASSED (100% success rate)
# - Average response time < 30s (EXCELLENT rating)
# - Performance rating: EXCELLENT
# - Duration: ~7-8 minutes per loop
# - All statistics calculated correctly (no 0s or stuck values)

# 3. Include test report in commit
# - Test reports auto-saved to test-reports/
# - Include in git add before commit
```

**CRITICAL:** Test execution is MANDATORY before any commit. See enforcement rules in `task_completion_checklist.md`.

## Multi-Loop Testing

### Purpose
Multi-loop testing establishes performance baselines and validates consistency.

### Usage
```bash
# 3-loop validation (recommended for most changes)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 3

# 10-loop baseline (recommended for performance validation)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 10
```

### Output Format
Each loop generates separate report with aggregated summary showing 2 decimal precision and formatted duration:
```
Loop 1/3: 40/40 PASSED, Avg: 11.03s, Duration: 7 min 22 sec
Loop 2/3: 40/40 PASSED, Avg: 11.45s, Duration: 7 min 38 sec
Loop 3/3: 40/40 PASSED, Avg: 11.21s, Duration: 7 min 29 sec

Overall Aggregate Statistics:
- Total Tests: 120/120 PASSED (100%)
- Overall Average: 11.23s
- Min Average: 11.03s (Loop 1)
- Max Average: 11.45s (Loop 2)
```

### When to Run Multi-Loop Tests
- After major architectural changes (10 loops)
- After test script bug fixes (3 loops minimum)
- After service_tier configuration changes (3 loops minimum)
- Before production releases (10 loops)
- When validating performance optimizations (10 loops)
- To establish new performance baselines (10 loops)
- After adding new API integrations (3 loops minimum)

## API Usage Considerations

**Note:** Each test run makes 40+ real API calls to:
- **Polygon.io**: Financial data (11 tools)
- **Finnhub**: Stock quotes (1 tool)
- **Tradier**: Options expiration dates (1 tool, added Oct 10, 2025)
- **OpenAI**: GPT-5-Nano (AI agent with service_tier: "default")

**Cost Implications:**
- **Polygon.io**: Counts toward API rate limits
- **Finnhub**: Counts toward API rate limits
- **Tradier**: Counts toward API rate limits (2 calls per test run)
- **OpenAI**: Tokens consumed (~800-1500 per test, ~32,000-60,000 per full run)

**Best Practice:**
- Run single-loop validation before commits (mandatory)
- Run 3-loop validation for significant changes
- Run 10-loop baselines sparingly (major changes only)
- Monitor API usage and costs
- Consider API mocking for frequent development testing (future enhancement)

## Recent Updates and Changes

### Oct 10, 2025: Tradier Options Expiration Dates Tool Integration

**Tool Addition:**
- **Tool**: `get_options_expiration_dates` via Tradier Brokerage API
- **Purpose**: Fetch ALL valid options expiration dates for a ticker
- **Integration**: Direct HTTP API using requests library
- **Authentication**: Bearer token via TRADIER_API_KEY

**Test Suite Updates:**
- **Total Tests**: 38 → 40 tests
- **SPY Sequence**: 16 → 17 tests
- **NVDA Sequence**: 16 → 17 tests
- **Multi-Ticker Sequence**: 6 tests (unchanged)
- **New Tests**:
  - Test 14: SPY Options Expiration Dates (inserted after Test 13)
  - Test 31: NVDA Options Expiration Dates (inserted after Test 30)
- **Test Renumbering**: All tests after Test 13 shifted by +1

**Files Modified:**
- `test_cli_regression.sh`: Updated header comments, prompts array, test_names array (38→40 tests)
- `src/backend/tools/tradier_tools.py`: New tool implementation (156 lines)
- `src/backend/tools/__init__.py`: Export get_options_expiration_dates
- `src/backend/services/agent_service.py`: Import tool, add to tools list, RULE #10

**Test Results:**
- **Total**: 40/40 PASSED (100%)
- **Avg Response Time**: 11.03s (EXCELLENT)
- **Duration**: 7 min 22 sec
- **New Tests**:
  - Test 14: SPY - PASS (8.596s, EXCELLENT)
  - Test 31: NVDA - PASS (14.511s, EXCELLENT)
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-10_19-25.log`

**Quick Validation:**
- SPY: 31 expiration dates, 9.844s - PASS
- NVDA: 21 expiration dates, 6.842s - PASS
- SOUN: 11 expiration dates, 6.391s - PASS

### Oct 9, 2025: Options Chain Wall Analysis Tests

**Test Suite Updates:**
- **Total Tests**: 36 → 38 tests
- **New Tests**:
  - Test 16: SPY Options Chain Wall Analysis (now Test 17 after Oct 10)
  - Test 32: NVDA Options Chain Wall Analysis (now Test 34 after Oct 10)
- **Purpose**: Validate AI Agent can identify support/resistance levels from options chain data

### Oct 8, 2025: Test Suite Restructuring & Service Tier Change

**Service Tier Optimization:**
- **File**: `src/backend/services/agent_service.py:367`
- **Change**: `service_tier: "flex"` → `service_tier: "default"`
- **Reason**: Prototyping phase requires better performance; "flex" tier was causing compute resources rate limiting
- **Impact**: Improved response consistency and throughput
- **Validation**: 36/36 tests PASSED with 10.44s avg (EXCELLENT rating)

**Test Suite Restructuring:**
- **Previous**: 27 tests (mixed organization)
- **New**: 36 tests organized by ticker (SPY 15 + NVDA 15 + Multi 6)
- **Dynamic Dates**: Queries use relative dates instead of hardcoded dates
- **Sustainability**: No date updates required over time
- **Ticker Changes**: GME replaced INTC in multi-ticker sequence

### Oct 6, 2025: Calculation Engine Overhaul
**Issue:** All floating-point calculations failed silently due to missing `bc` dependency
**Fix:** Replaced ALL `bc` usage with `awk` (universally available)
**Validation:** 270-test baseline (10 loops) confirmed accuracy

### Oct 6, 2025: Output Formatting Enhancement
**Improvements:**
- Limited all decimal values to 2 decimal places
- Converted duration to "MM min SS sec" format
- Enhanced readability of all test reports

## Future Enhancements

Potential improvements for testing infrastructure:

1. **API Mocking** - Test without live API calls for faster iteration
2. **Parallel Testing** - Run multiple test suites concurrently
3. **Performance Regression Detection** - Alert if avg response time increases > 20%
4. **CI/CD Integration** - Automated testing on push/PR
5. **Historical Trending** - Track performance metrics over time in database
6. **Load Testing** - Test concurrent user scenarios
7. **Error Injection** - Test error handling and recovery
8. **Visual Regression Testing** - Frontend screenshot comparison

## Test Report Archive

Recent test reports demonstrate consistent performance:

- **Oct 10, 2025 (Single-Loop Tradier Integration)**: 40/40 PASSED, 11.03s avg, 7 min 22 sec, EXCELLENT rating
- **Oct 9, 2025 (Wall Analysis Tests)**: 38/38 PASSED, 11.05s avg, EXCELLENT rating
- **Oct 8, 2025 (Single-Loop Post-Service-Tier-Change)**: 36/36 PASSED, 10.44s avg, 6 min 36 sec, EXCELLENT rating
- **Oct 6, 2025 (10-Loop Baseline)**: 270/270 PASSED (27 tests × 10), 8.73s overall avg
- **Post-MCP Removal**: 70% performance improvement vs legacy architecture
- **Consistency**: 100% success rate across all validation runs
