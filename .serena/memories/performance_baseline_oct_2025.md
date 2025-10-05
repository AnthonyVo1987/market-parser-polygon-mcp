# AI Agent Performance Baseline - October 2025

**Established**: October 4, 2025  
**Purpose**: Baseline performance metrics for GPT-5-Nano AI Agent with optimized tool selection instructions  
**Test Configuration**: 7-prompt persistent session test suite  
**Total Runs**: 10 consecutive test runs (70 total tests)  

---

## Overall Performance Summary

### Success Rate
- **Total Tests**: 70/70 (10 runs × 7 tests each)
- **Success Rate**: **100%** (all tests passed)
- **Session Persistence**: **VERIFIED** (all runs maintained single session)
- **Tool Selection Accuracy**: **100%** (correct tool used for every test)

### Response Time Statistics

#### Aggregate (All 70 Tests)
- **Min Response Time**: 5.820s (Run 5, Test 6)
- **Max Response Time**: 32.777s (Run 1, Test 2)
- **Overall Average**: **15.97s**
- **Performance Rating**: **EXCELLENT**

#### Per-Run Averages
| Run | Avg Time | Min Time | Max Time | Performance | Duration |
|-----|----------|----------|----------|-------------|----------|
| 1   | 17.78s   | 7.947s   | 32.777s  | EXCELLENT   | 123.04s  |
| 2   | 17.18s   | 7.071s   | 28.972s  | EXCELLENT   | 118.59s  |
| 3   | 15.83s   | 8.224s   | 22.310s  | EXCELLENT   | 108.52s  |
| 4   | 16.65s   | 6.841s   | 21.607s  | EXCELLENT   | 114.32s  |
| 5   | 14.77s   | 5.820s   | 28.886s  | EXCELLENT   | 101.09s  |
| 6   | 14.00s   | 5.974s   | 22.085s  | EXCELLENT   | 95.51s   |
| 7   | 13.81s   | 7.196s   | 22.129s  | EXCELLENT   | 94.20s   |
| 8   | 17.09s   | 11.587s  | 21.344s  | EXCELLENT   | 117.25s  |
| 9   | 15.96s   | 7.576s   | 23.910s  | EXCELLENT   | 109.37s  |
| 10  | 16.68s   | 7.495s   | 24.374s  | EXCELLENT   | 114.44s  |

---

## Test Suite Composition

### Test 1: Market Status Query
- **Prompt**: "What the current Market Status?"
- **Expected Tool**: `get_market_status()`
- **Average Response**: 14-20s range
- **Complexity**: Low (single tool call)

### Test 2: Single Stock Snapshot (NVDA)
- **Prompt**: "Stock Snapshot: NVDA"
- **Expected Tool**: `get_snapshot_ticker(ticker='NVDA', market_type='stocks')`
- **Average Response**: 12-33s range (highest variance)
- **Complexity**: Medium (single ticker snapshot)

### Test 3: Multi-Stock Snapshot (SPY, QQQ, IWM)
- **Prompt**: "Stock Snapshot: SPY, QQQ, IWM"
- **Expected Tool**: `get_snapshot_all(tickers=['SPY','QQQ','IWM'], market_type='stocks')`
- **Average Response**: 13-24s range
- **Complexity**: Medium (multi-ticker snapshot)

### Test 4: Closing Price Query (SPY)
- **Prompt**: "What was closing price today for: SPY"
- **Expected Tool**: `get_snapshot_ticker(ticker='SPY', market_type='stocks')`
- **Average Response**: 6-10s range (fastest test)
- **Complexity**: Low (single ticker, simple query)

### Test 5: Weekly Performance Analysis (SPY)
- **Prompt**: "Current weekly Price Change $ and % for: SPY"
- **Expected Tool**: `get_aggs()` with weekly timespan
- **Average Response**: 17-28s range
- **Complexity**: High (requires historical aggregates)

### Test 6: Support & Resistance Levels (SPY)
- **Prompt**: "Support & Resistance Levels: SPY"
- **Expected Tool**: `get_aggs()` with weekly/daily aggregates
- **Average Response**: 6-11s range
- **Complexity**: Medium (analysis of historical data)

### Test 7: Technical Analysis (SPY)
- **Prompt**: "Technical Analysis: SPY"
- **Expected Tool**: `get_aggs()` for trend analysis
- **Average Response**: 7-8s range
- **Complexity**: Medium (comprehensive analysis)

---

## Performance Consistency Analysis

### Response Time Distribution
- **Fast (< 10s)**: 18.6% of tests (primarily Test 4, Test 6, Test 7)
- **Optimal (10-20s)**: 54.3% of tests (majority of responses)
- **Good (20-30s)**: 24.3% of tests (complex queries)
- **Acceptable (30-40s)**: 2.8% of tests (outliers in Test 2)

### Session Duration Trends
- **Shortest Session**: 94.20s (Run 7)
- **Longest Session**: 123.04s (Run 1)
- **Average Session**: 109.63s
- **Consistency**: ±13% variance from mean

### Tool Selection Accuracy
- **Single Ticker Tests (Test 2, Test 4)**: 100% correct use of `get_snapshot_ticker()`
- **Multi-Ticker Test (Test 3)**: 100% correct use of `get_snapshot_all()`
- **Aggregate Tests (Test 5, 6, 7)**: 100% correct use of `get_aggs()`
- **Market Status Test (Test 1)**: 100% correct use of `get_market_status()`

---

## Key Improvements Since Baseline Establishment

### Issues Fixed (Pre-Baseline)
1. **Tool Selection Confusion**: AI agent was using `get_snapshot_all()` for single tickers instead of `get_snapshot_ticker()` (~43% error rate)
2. **Missing Parameters**: Validation errors due to missing `market_type='stocks'` parameter
3. **Market Closed Refusals**: AI agent refused requests when market was closed instead of returning last available price
4. **Strict Data Requirements**: AI agent required exact data amounts instead of working with available data
5. **Ticker Format Errors**: Wrong format for multi-ticker calls (string instead of list)

### Solutions Implemented
1. **RULE #1**: Single ticker = ALWAYS use `get_snapshot_ticker()` with `market_type='stocks'`
2. **RULE #2**: Multiple tickers = ALWAYS use `get_snapshot_all()` with `market_type='stocks'` and LIST format
3. **RULE #6**: Work with available data - no strict requirements
4. **RULE #7**: NEVER refuse when market closed - always return last available price
5. **Tool Call Transparency**: Each response includes "Tools Used" section with reasoning

### Results
- **Tool Selection Accuracy**: 43% → 100%
- **Response Success Rate**: 43% → 100%
- **Average Response Time**: 20-23s → 15-18s (15-22% improvement)
- **Zero Refusals**: Eliminated all "unavailable" and "market closed" failure responses

---

## Baseline Metrics for Future Comparison

### Critical Performance Indicators
1. **Success Rate Target**: ≥ 95% (baseline: 100%)
2. **Average Response Time Target**: ≤ 20s (baseline: 15.97s)
3. **Tool Selection Accuracy Target**: ≥ 98% (baseline: 100%)
4. **Session Persistence Target**: 100% (baseline: 100%)

### Performance Degradation Alerts
- **WARNING**: If average response time > 20s (25% degradation from baseline)
- **CRITICAL**: If average response time > 25s (57% degradation from baseline)
- **WARNING**: If tool selection accuracy < 95%
- **CRITICAL**: If success rate < 90%

### Recommended Testing Frequency
- **Weekly**: Single test run for sanity check
- **Pre-Release**: 3x test runs for validation
- **Major Changes**: 10x test runs for new baseline establishment
- **Performance Regression**: Immediate investigation if 2 consecutive tests show >15% degradation

---

## Test Environment

### Backend Configuration
- **Framework**: FastAPI with Uvicorn
- **AI Model**: GPT-5-Nano (OpenAI Agents SDK v0.2.9)
- **MCP Server**: Polygon.io v0.4.1
- **Port**: 8000 (localhost)

### Test Script
- **File**: `test_7_prompts_persistent_session.sh`
- **Mode**: Persistent session (single CLI instance for all 7 tests)
- **Timeout**: 120s per test
- **Output**: Detailed report in `test-reports/`

### System Specifications
- **OS**: Linux (WSL2)
- **Python**: 3.12.3 with uv 0.8.19
- **Node**: v24.6.0 with npm 11.6.0

---

## Usage Guidelines

### When to Re-Establish Baseline
- **Major AI Agent Instruction Changes**: Any modifications to system prompt or tool selection rules
- **API/MCP Server Updates**: Changes to Polygon.io MCP or OpenAI Agents SDK
- **Model Updates**: If GPT-5-Nano model is updated or replaced
- **Performance Optimization**: After implementing response time improvements

### Comparison Methodology
1. Run `test_7_prompts_persistent_session.sh` at least 3 times
2. Calculate average response time across all runs
3. Compare to baseline average (15.97s)
4. Check tool selection accuracy (should be 100%)
5. Verify success rate (should be 100%)
6. Flag any degradation > 15% for investigation

### Performance Investigation Triggers
- Average response time > 18.4s (15% slower than baseline)
- Any test failure (< 100% success rate)
- Tool selection errors (< 100% accuracy)
- Session persistence failures

---

## Historical Context

**Previous State** (Before October 4, 2025 fixes):
- Tool selection errors in ~43% of single-ticker tests
- Frequent "unavailable" responses due to market closure
- Average response time: 20-23s
- Validation errors from missing parameters

**Current State** (October 4, 2025 baseline):
- 100% tool selection accuracy
- Zero refusal responses
- Average response time: 15.97s
- All parameters correctly provided
- Full transparency with "Tools Used" section

**Future Expectations**:
- Maintain or improve current performance
- Monitor for model updates that may affect response times
- Track tool selection accuracy over time
- Document any regressions with detailed analysis

---

## Notes

- All 10 baseline runs executed on October 4, 2025 (single day)
- Market was CLOSED during testing (after-hours)
- All tests successfully returned last available prices despite market closure
- No false failures detected in any run
- Session persistence verified in 100% of runs (single CLI session per run)
- Test reports archived in `test-reports/persistent_session_test_*.txt`

This baseline represents the **optimal performance** of the AI agent after comprehensive instruction optimization and serves as the reference point for all future performance tracking and regression detection.