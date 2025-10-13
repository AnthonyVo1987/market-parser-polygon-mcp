# Testing Procedures and Validation

## 🔴 CRITICAL: TWO-PHASE TESTING APPROACH (Updated Oct 12, 2025)

### Overview

**The test script can ONLY verify that responses were received. It CANNOT validate response correctness, tool calls, or data accuracy.**

All testing MUST follow the two-phase approach:

### Phase 1: Automated Response Generation

**What the Script Does:**
- Runs all 39 test prompts sequentially in ONE CLI session
- Measures response times
- Reports "X/39 COMPLETED" (responses received)
- Generates test report with full output

**What the Script Does NOT Do:**
- ❌ Validate response correctness
- ❌ Check tool calls
- ❌ Verify data accuracy
- ❌ Detect hallucinations
- ❌ Confirm proper formatting

**Script Limitation:** "39/39 COMPLETED" means "39 responses received" NOT "39 tests passed validation"

### Phase 2: Manual Response Verification (MANDATORY)

**AI Agent MUST verify each of the 39 responses against these criteria:**

1. ✅ **Response Addresses Prompt**: Response directly answers the question asked
2. ✅ **Correct Ticker Symbols**: Proper tickers used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
3. ✅ **Proper Tool Calls**: Polygon, Finnhub, or Tradier tools called appropriately
4. ✅ **Data Formatting**: OHLC data, tables, options chains formatted correctly
5. ✅ **No Hallucinations**: All data appears legitimate, no made-up numbers or dates
6. ✅ **Options Bid/Ask**: Options chains show Bid and Ask columns (NOT midpoint/average)
7. ✅ **TA Indicators**: Technical analysis includes proper metrics when requested
8. ✅ **Completeness**: Response not truncated, no unexpected errors

**Mandatory Checkpoint Question:**
"Did you verify the results of EACH test prompt to ensure the response was correct with proper tool calls and formatting?"

- **If NO**: You have NOT completed testing. Return to Phase 2.
- **If YES**: Testing is complete, proceed to documentation updates.

### Workflow Summary

```
1. Code Implementation ✅
2. Test Suite Update ✅
3. Phase 1: Execute test_cli_regression.sh ✅
4. Phase 1 Results: 39/39 COMPLETED ✅
5. Phase 2: Manually verify ALL 39 responses ✅ (MANDATORY)
6. Checkpoint: "Did you verify each response?" YES ✅
7. Documentation Updates ✅
8. Atomic Commit ✅
```

**CRITICAL:** Skipping Phase 2 = Testing INCOMPLETE = Task INVALID

---

## Primary Test Script

### CLI Regression Test Suite (RECOMMENDED)
**Script:** `test_cli_regression.sh`

**Purpose:** Tests all 39 standardized prompts (Updated Oct 12, 2025) in a SINGLE CLI session with two-phase validation.

**Features:**
- ✅ All 39 tests run sequentially in ONE session
- ✅ Accurate response time tracking with awk-based calculations
- ✅ Session persistence validation
- ✅ Comprehensive test reports with formatted output
- ✅ Performance classification
- ✅ Configurable loop count (1-10 runs)
- ✅ 2 decimal precision for all statistics
- ✅ Human-readable duration format (MM min SS sec)
- ✅ Two-phase validation workflow with Phase 2 instructions

**Usage:**
```bash
# Single test loop (39 tests) - Phase 1 only
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Multiple test loops (e.g., 3 loops for validation)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 3
```

**Test Coverage (39 tests total - Updated Oct 12, 2025):**

1. **SPY Test Sequence (Tests 1-16 - 16 tests)**:
   - Market Status
   - Current Price OHLC: $SPY
   - Yesterday's Price OHLC: $SPY
   - Last week's Performance OHLC: $SPY
   - Stock Price on previous week's Friday OHLC: $SPY
   - Stock Price Performance last 5 Trading Days OHLC: $SPY
   - Stock Price Performance past 2 Weeks OHLC: $SPY
   - Stock Price Performance past month: $SPY
   - Stock Price Performance past 3 months: $SPY
   - Get technical analysis indicator DATA only with NO ANALYSIS: $SPY
   - Support & Resistance Levels: $SPY
   - Perform technical analysis (Trends, Volatility, Momentum, Signals): $SPY
   - Get options expiration dates: $SPY
   - Get Call Options Chain Expiring this Friday: $SPY
   - Get Put Options Chain Expiring this Friday: $SPY
   - Analyze Options Chain Data & provide Call/Put Wall Strike Prices: $SPY

2. **NVDA Test Sequence (Tests 17-31 - 15 tests)**:
   - Current Price OHLC through Options Wall Analysis (no Market Status)
   - Same pattern as SPY but without initial Market Status prompt
   - All OHLC queries, TA, options expiration, options chains, wall analysis

3. **Multi-Ticker Test Sequence (Tests 32-39 - 8 tests)**:
   - Current Price OHLC: $WDC, $AMD, $SOUN
   - Yesterday's Price OHLC: $WDC, $AMD, $SOUN
   - Yesterday's Closing Price: $WDC, $AMD, $SOUN
   - Last week's Performance OHLC: $WDC, $AMD, $SOUN
   - Get TA indicator DATA only: $WDC, $AMD, $SOUN
   - Support & Resistance Levels: $WDC, $AMD, $SOUN
   - Perform TA (Trends, Volatility, Momentum, Signals): $WDC, $AMD, $SOUN
   - Get options expiration dates: $WDC, $AMD, $SOUN

**Note:** Multi-ticker sequence now uses $SOUN instead of $GME (Oct 12, 2025)

**Expected Performance (Oct 12, 2025 - 39 Test Suite):**
- **Total Tests**: 39 per loop
- **Average Response Time**: ~10-12s (EXCELLENT)
- **Phase 1 Duration**: ~7-8 minutes per loop
- **Phase 2 Duration**: ~60-90 minutes (manual verification)
- **Total Testing Time**: ~70-100 minutes per full validation cycle

**Performance Classification:**

| Category | Time Range | Rating |
|----------|-----------|--------|
| EXCELLENT | < 30s | ✅ Expected for most queries |
| GOOD | 30-45s | ✅ Acceptable for complex queries |
| ACCEPTABLE | 45-90s | ⚠️ May need optimization |
| SLOW | > 90s | ❌ Needs investigation |

---

## Test Script Output Changes (Oct 12, 2025)

### Old Terminology (Before Oct 12, 2025):
- ❌ "PASS/FAIL" - Misleading, suggested validation
- ❌ "100% pass rate" - False confidence
- ❌ "Tests passed" - Incorrect assumption

### New Terminology (After Oct 12, 2025):
- ✅ "COMPLETED/INCOMPLETE" - Neutral, factual
- ✅ "Generation rate" - Accurate description
- ✅ "Responses generated" - Clear meaning
- ✅ "Phase 1 Complete" - Explicit phase indication
- ✅ "Phase 2 Required" - Mandatory next step

### Script Output Example:
```
Phase 1 Results Summary (Responses Generated):
   Test 1: Test_1_SPY_Market_Status - COMPLETED
   Test 2: Test_2_SPY_Current_Price_OHLC - COMPLETED
   ...
   Test 39: Test_39_Multi_Options_Expiration_Dates_WDC_AMD_SOUN - COMPLETED

Total Tests: 39
Completed: 39
Incomplete: 0
Generation Rate: 100%

✅ Phase 1 Complete: All responses generated

🔴 PHASE 2 REQUIRED: Manual Verification Needed

Phase 2 Verification Checklist (for AI Agent):
For EACH of the 39 test responses, verify:
  1. ✅ Response directly addresses the prompt query
  2. ✅ Correct ticker symbols used
  3. ✅ Appropriate tool calls made
  4. ✅ Data formatting matches expected format
  5. ✅ No hallucinated data or made-up values
  6. ✅ Options chains show Bid/Ask columns
  7. ✅ Technical analysis includes proper indicators
  8. ✅ Response is complete (not truncated)

⚠️  MANDATORY CHECKPOINT QUESTION:
   "Did you verify the results of EACH test prompt to ensure
    the response was correct with proper tool calls and formatting?"
```

---

## Running Tests

### Phase 1: Execute Test Script

```bash
# Single loop (RECOMMENDED)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Multiple loops for validation
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 3
```

### Phase 2: Manual Verification

1. **Open test report:**
   ```bash
   cat test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log
   ```

2. **For each of 39 responses, verify 8 criteria**

3. **Document issues found** (if any)

4. **Answer checkpoint question:**
   - "Did you verify the results of EACH test prompt?"
   - Must answer YES before proceeding

5. **If issues found:**
   - Fix the issues
   - Re-run Phase 1
   - Re-perform Phase 2
   - Repeat until all responses correct

---

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
- ✅ After adding new API integrations

**Both phases MUST complete before claiming task complete.**

---

## Pre-Commit Checklist

See `task_completion_checklist.md` for full checklist. Testing requirements:

```bash
# Phase 1: Execute test script
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Phase 2: Manual verification
# - Review each of 39 responses in test report
# - Verify against 8-point criteria
# - Answer checkpoint question: YES
# - Document any issues found
# - Fix and re-test if needed

# Only proceed to commit after BOTH phases complete
```

**CRITICAL:** Both Phase 1 AND Phase 2 are MANDATORY before any commit.

---

## API Usage Considerations

**Note:** Each test run makes 39+ real API calls to:
- **Polygon.io**: Financial data (11 tools)
- **Finnhub**: Stock quotes (1 tool)
- **Tradier**: Options expiration dates (1 tool)
- **OpenAI**: GPT-5-Nano (AI agent with service_tier: "default")

**Cost Implications:**
- **Phase 1**: API costs for 39 queries
- **Phase 2**: No additional API costs (manual review)
- **OpenAI**: Tokens consumed (~800-1500 per test, ~30,000-60,000 per full run)

**Best Practice:**
- Run single-loop validation before commits (mandatory)
- Run 3-loop validation for significant changes
- Perform Phase 2 for each loop
- Monitor API usage and costs

---

## Test Suite Evolution

- **Oct 12, 2025**: 39 tests (SPY 16 + NVDA 15 + Multi 8) - Two-phase validation, OHLC terminology, $SOUN ticker
- **Oct 10, 2025**: 40 tests (SPY 17 + NVDA 17 + Multi 6) - Added Tradier expiration dates tests
- **Oct 9, 2025**: 38 tests (SPY 16 + NVDA 16 + Multi 6) - Added options chain wall analysis tests
- **Oct 8, 2025**: 36 tests (SPY 15 + NVDA 15 + Multi 6) - Service tier change to "default"

---

## Key Changes Summary (Oct 12, 2025)

1. **Test Count**: 40 → 39 tests
2. **Terminology**: "PASS/FAIL" → "COMPLETED/INCOMPLETE"
3. **Validation**: Single-phase → Two-phase approach
4. **Prompts**: More explicit OHLC terminology
5. **Tickers**: $GME → $SOUN in multi-ticker tests
6. **SPY Tests**: 17 → 16 (removed duplicate Market Status)
7. **NVDA Tests**: 17 → 15 (removed Market Status prompts)
8. **Multi Tests**: 6 → 8 (added more comprehensive coverage)
9. **Phase 2**: Added mandatory manual verification with 8-point criteria
10. **Checkpoint**: Added mandatory verification question

---

**For complete historical context, calculation details, troubleshooting, and performance benchmarks, see previous sections of this memory.**
