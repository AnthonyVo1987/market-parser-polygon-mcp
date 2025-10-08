# AI Agent Instructions - Post-Tool-Removal (October 2025)

## Current State (Post-OHLC-Fix - Oct 7, 2025 Evening)

**AI Agent**: OpenAI Agents SDK v0.2.9
**Model**: GPT-5-Nano (EXCLUSIVE)
**Total Tools**: 11 (1 Finnhub + 10 Polygon Direct API)
**Architecture**: Direct Python API integration (no MCP)
**Multi-Ticker Pattern**: Parallel get_stock_quote() calls via OpenAI Agents SDK
**Latest Fixes**: OHLC display requirements + Support/Resistance redundant call prevention

## System Prompt Location

`src/backend/services/agent_service.py` → `get_enhanced_agent_instructions()` function

## Key Features of Current Instructions

### 1. Tool Count and Architecture
- Lists exactly **11 SUPPORTED TOOLS**
- All tools use **Direct Python APIs** (no MCP)
- Clear categorization: Finnhub (1) + Polygon (10)
- **Parallel get_stock_quote() calls** for multiple tickers
- **OHLC display requirements** (RULE #5 - Oct 7 evening)
- **Chat history analysis** with Support/Resistance fix (RULE #9 - Oct 7 evening)

### 2. Direct API Tool Descriptions

**Finnhub (1 tool):**
- `get_stock_quote(symbol: str)` - Real-time stock quotes from Finnhub
  - Supports parallel calls for multiple tickers

**Polygon Direct API (10 tools):**

**Market Data:**
1. `get_market_status_and_date_time()` - Market status and current datetime
2. `get_options_quote_single(ticker: str)` - Single option contract quote

**OHLC Data:**
3. `get_OHLC_bars_custom_date_range(ticker, multiplier, timespan, from_date, to_date)` - OHLC bars for date range
4. `get_OHLC_bars_specific_date(ticker, date)` - OHLC bars for specific date
5. `get_OHLC_bars_previous_close(ticker)` - Previous close OHLC

**Technical Analysis:**
6. `get_ta_sma(ticker, timestamp, timespan, adjusted, window, series_type, order, limit)` - SMA indicator
7. `get_ta_ema(ticker, timestamp, timespan, adjusted, window, series_type, order, limit)` - EMA indicator
8. `get_ta_rsi(ticker, timestamp, timespan, adjusted, window, series_type, order, limit)` - RSI indicator
9. `get_ta_macd(ticker, timestamp, timespan, adjusted, short_window, long_window, signal_window, series_type, order, limit)` - MACD indicator

**Removed (Oct 7, 2025 afternoon):**
- ~~`get_stock_quote_multi(symbols: str)`~~ - Replaced by parallel get_stock_quote() calls

### 3. Critical Rules for Tool Usage (UPDATED Oct 7, 2025 Evening)

**RULE #1: Single Ticker Selection**
- Single ticker → ALWAYS use `get_stock_quote(ticker='SYMBOL')`
- Examples: "NVDA price", "GME closing price", "TSLA snapshot"
- Uses Finnhub API for real-time quote data

**RULE #2: Multiple Tickers = PARALLEL get_stock_quote() CALLS**
- Multiple tickers → Make PARALLEL calls to `get_stock_quote()`
- Max 3 parallel calls per batch (rate limiting protection)
- Examples: "SPY, QQQ, IWM prices", "NVDA and AMD"
- ✅ ALWAYS make PARALLEL calls: get_stock_quote(ticker='SYM1'), get_stock_quote(ticker='SYM2'), get_stock_quote(ticker='SYM3')
- 📊 Uses Finnhub API (fast, low overhead)
- ✅ OpenAI Agents SDK executes tool calls in PARALLEL automatically
- 🔴 CRITICAL: Each get_stock_quote call is INDEPENDENT - make them ALL at once

**RULE #3: Options Selection**
- Options contracts → use `get_options_quote_single()`
- Always show strike prices and expiration dates clearly
- Uses Polygon.io Direct API

**RULE #4: Market Status & Date/Time**
- Market status queries → use `get_market_status_and_date_time()`
- Returns market status, exchange statuses, server datetime

**RULE #5: OHLC Data with Display Requirements** ⭐ UPDATED Oct 7 Evening
- Historical OHLC prices → use get_OHLC_bars_* tools
- Date validation required (weekends/holidays/future dates)
- **CRITICAL DISPLAY REQUIREMENTS FOR OHLC BARS:**
  - **For custom date range**: MUST show start open, end close, $ and % change, period high/low, trading days
  - **For specific date**: MUST show Date, Open, High, Low, Close, Volume
  - ❌ NEVER just say "data retrieved" without actual numbers
  - ❌ NEVER say "If you'd like, I can show the data" - show it immediately
  - ✅ Example GOOD: "SPY Q1 2025: Started 1/2/25 at $580.50, ended 3/31/25 at $612.30 (+$31.80, +5.48%), High: $615.25, Low: $575.10, 60 days"
  - ❌ Example BAD: "SPY daily OHLC bars retrieved for Q1 2025" [USELESS!]

**RULE #6: Work with Available Data**
- ALWAYS use whatever data is returned, even if less than expected
- NEVER fail or refuse because got less data than requested

**RULE #7: Market Closed = Still Provide Data**
- 🔴 CRITICAL: Market being CLOSED is NOT a reason to refuse
- ALWAYS provide last available price when market closed
- Use fallback sequence: get_stock_quote → get_OHLC_bars_previous_close

**RULE #8: Technical Analysis - Check Chat History First**
- Minimum TA requirements: RSI-14, MACD, SMA 20/50/200, EMA 20/50/200
- FIRST: Check chat history for existing TA data
- IF all minimum TA data already retrieved → NO NEW TOOL CALLS
- Provide actual ANALYSIS (trends, momentum, volatility, patterns)
- NOT just raw numbers

**RULE #9: Chat History Analysis - Avoid Redundant Calls** ⭐ UPDATED Oct 7 Evening
- CRITICAL: Analyze conversation history for existing data BEFORE making tool calls
- **NEW Scenario 5 - Support & Resistance Levels:**
  - Previous: Already retrieved SPY price, SMA 20/50/200, EMA 20/50/200, RSI-14, MACD
  - Current: User asks "Support & Resistance Levels: SPY"
  - **CORRECT**: Use existing data, NO new tool calls
  - **REASONING**: Support/Resistance derived from existing price, SMA/EMA levels
  - ❌ WRONG: Making NEW calls for SMA/EMA/RSI/MACD when already retrieved
- Transparency: State "No tool calls needed - using existing data from previous queries"

### 4. Decision Tree (UPDATED Oct 7, 2025)

**Stock Quote Decision Tree:**
```
Step 0: Analyze chat history for existing data
Step 1: Count ticker symbols in request  
Step 2:
   - If count = 1 ticker → USE get_stock_quote(ticker='SYMBOL')
   - If count = 2-3 tickers → USE PARALLEL get_stock_quote() calls (max 3)
   - If count > 3 tickers → BATCH into groups of 3
Step 3: Execute tool calls (batched if needed)
Step 4: Generate response with existing + new data
```

### 5. Response Format Requirements

**Structured Output:**
```
KEY TAKEAWAYS / Bullet points with data
• Bullet point 1 with clear sentiment/direction
• Bullet point 2 with key metrics
• Bullet point 3 with actionable insight

DETAILED ANALYSIS (if applicable)
[Comprehensive analysis with clear directional indicators]

TOOLS USED
• tool_name(parameters) - Reasoning for selection
OR
• No tool calls needed - using existing data from previous queries
```

## Historical Context

### Evolution of Instructions

**Phase 1** (Pre-MCP Removal):
- 18 tools (7 MCP + 11 Direct API)
- Mixed MCP/Direct API patterns

**Phase 2** (Post-MCP Removal - Oct 2025):
- 12 tools (0 MCP + 12 Direct API)
- 70% performance improvement

**Phase 3** (Post-get_stock_quote_multi Removal - Oct 7 Afternoon):
- 11 tools (1 Finnhub + 10 Polygon Direct API)
- Parallel get_stock_quote() pattern
- Removed 139-line wrapper

**Phase 4** (Post-OHLC-Fix - Oct 7 Evening): ⭐ LATEST
- 11 tools (unchanged)
- Added OHLC display requirements to RULE #5
- Enhanced RULE #9 with Scenario 5 (Support/Resistance)
- New 35-test suite (test_cli_regression.sh)

### Latest Fixes (Oct 7, 2025 Evening)

**1. OHLC Display Requirements (RULE #5)**
- **Problem**: AI Agent just said "data retrieved" without showing actual prices
- **Fix**: Added "CRITICAL DISPLAY REQUIREMENTS FOR OHLC BARS" section
- **Result**: Test 15 (SPY OHLC Q1) now shows start: 589.39, end: 559.39, change: -4.31%, high: 613.23, low: 549.83, 60 days ✅

**2. Support & Resistance Redundant Calls (RULE #9)**
- **Problem**: AI Agent was calling get_ta_sma/ema/rsi/macd AGAIN for Support & Resistance even when all data already retrieved
- **Fix**: Added Scenario 5 to RULE #9 explicitly telling AI to use existing data
- **Result**: Test 12 reduced from 5.491s to 3.900s (29% faster) ✅

**3. New Test Suite (test_cli_regression.sh)**
- **Expansion**: 35 comprehensive tests (vs previous 27)
- **Coverage**: SPY sequence (15), NVDA sequence (15), Multi-ticker WDC/AMD/INTC (5)
- **Validation**: Parallel calls, chat history analysis, OHLC display

## Testing Validation

### Latest Test Results (Oct 7, 2025 Evening - Post-OHLC-Fix):
- **Total**: 35/35 tests (100%)
- **Average**: 11.62s per query
- **Range**: 2.188s - 31.599s
- **Performance**: EXCELLENT
- **Test 12 (Support & Resistance)**: 3.900s (vs previous 5.491s) - redundant call fix verified ✅
- **Test 15 (SPY OHLC Q1)**: Shows actual data (not just "data retrieved") ✅
- **Test 30 (NVDA OHLC Q1)**: Shows actual data ✅
- **Test 35 (Multi OHLC Q1)**: Shows actual data for all 3 tickers ✅
- **Chat History Reuse**: Test 32 correctly used existing data ✅
- **Parallel Calls**: Tests 31, 33, 34 correctly made parallel calls ✅
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-07_20-30.log`

### Previous Test Results (Oct 7 Afternoon - Post-Tool-Removal):
- **Total**: 27/27 tests (100%)
- **Average**: 7.31s per query
- **Range**: 4.848s - 11.580s

### Previous 10-Run Baseline (Oct 2025):
- **Total**: 270/270 tests (100%)
- **Average**: 6.10s per query
- **Improvement**: 70% faster than legacy MCP

## Tool Usage Examples (UPDATED Oct 7, 2025 Evening)

### OHLC Display Examples (NEW)

**Correct Response (Custom Date Range):**
```
• SPY daily bars (2025-01-02 to 2025-03-31)
   • Start open (2025-01-02): 589.39
   • End close (2025-03-31): 559.39
   • Change: -25.25 (-4.31%)
   • Period High: 613.23
   • Period Low: 549.83
   • Trading days: 60

Tools Used:
• get_OHLC_bars_custom_date_range(ticker='SPY', from_date='2025-01-02', to_date='2025-03-31', timespan='day', multiplier=1, limit=50000)
```

**Incorrect Response (NEVER DO THIS):**
```
❌ "SPY daily OHLC bars retrieved for 2025-01-02 to 2025-03-31 (60 trading days)"
❌ "Data provided as daily Open, High, Low, Close, Volume (above 2 decimals)"
❌ "If you'd like, I can export the full dataset as CSV"
```

### Support & Resistance with Chat History (NEW)

**Scenario: User already got SPY price, SMA 20/50/200, EMA 20/50/200, RSI, MACD**

**Correct Response:**
```
• Support levels: SPY around 663.09 (SMA20), 649.75 (SMA50), 602.06 (SMA200)
• Resistance levels: around 672.68 (last period high), ~672.99 intraday high

Current price: 669.12 (near resistance zone)

Tools Used: No tool calls needed - using existing data from previous queries (SMA/price levels)
```

**Incorrect Response (NEVER DO THIS):**
```
❌ Making NEW calls: get_ta_sma(...), get_ta_ema(...), get_ta_rsi(...), get_ta_macd(...)
❌ "Fetching SMA and EMA data for support/resistance analysis..."
```

## Performance Metrics

### Response Times (Latest - Oct 7 Evening):
- **Average**: 11.62s (EXCELLENT)
- **Range**: 2.188s - 31.599s
- **Support & Resistance**: 3.900s (29% faster than before fix)
- **Success Rate**: 100% (35/35 tests)

### Response Times (Oct 7 Afternoon):
- **Average**: 7.31s (EXCELLENT)
- **Range**: 4.848s - 11.580s

### Response Times (Post-MCP Removal):
- **Average**: 6.10s (EXCELLENT)
- **Improvement**: 70% faster than legacy MCP

## Files Involved

**Primary File:**
- `src/backend/services/agent_service.py`
  - `get_enhanced_agent_instructions()` - System prompt with ALL RULES
  - `get_optimized_model_settings()` - Model config
  - `create_agent()` - Agent initialization with 11 tools

**Tool Definitions:**
- `src/backend/tools/polygon_tools.py` - 10 Polygon Direct API tools
- `src/backend/tools/finnhub_tools.py` - 1 Finnhub tool

**Testing:**
- `test_cli_regression.sh` - NEW 35-test suite (Oct 7 evening)
- `CLI_test_regression.sh` - Legacy 27-test suite (deprecated)
- `test-reports/` - Test results

## Maintenance Notes

### When to Update Instructions

**Required Updates:**
- Adding new tools
- Fixing tool selection errors
- Fixing response quality issues (like OHLC display)
- Performance optimizations

### Testing After Changes

**Mandatory:**
```bash
# Run new 35-test suite
./test_cli_regression.sh

# Verify results
# - 35/35 tests PASSED
# - Average < 15s
# - Performance: EXCELLENT
# - All responses showing actual data (not just "data retrieved")
```

### Documentation Updates

After modifying agent instructions:
1. Update this memory file
2. Update `CLAUDE.md` Last Completed Task
3. Run test suite and include results
4. Update `project_architecture.md` if architecture changes

## Recent Fixes History (Oct 7, 2025)

### Morning: get_stock_quote_multi Removal

**Rationale:** Unnecessary 139-line wrapper, SDK handles parallel execution natively
**Changes:** Removed tool, updated RULE #2, tool count 12→11
**Results:** 27/27 tests PASSED, 7.31s average

### Evening: OHLC Display + Support/Resistance Fixes

**Problem 1: OHLC Useless Responses**
- AI said "data retrieved" without actual prices/ranges/changes
- Users got no useful information

**Fix 1: RULE #5 Display Requirements**
- Added "CRITICAL DISPLAY REQUIREMENTS FOR OHLC BARS" section
- Explicit requirements for custom date range and specific date queries
- Good vs bad response examples

**Problem 2: Support/Resistance Redundant Calls**
- AI called get_ta_sma/ema/rsi/macd AGAIN even when all data already existed
- Wasted time and API calls

**Fix 2: RULE #9 Scenario 5**
- Added explicit scenario for Support & Resistance
- Tells AI to use existing price, SMA/EMA data instead of making new calls

**Results:**
- 35/35 tests PASSED ✅
- OHLC responses now show actual data (start, end, change, high, low, days)
- Support & Resistance 29% faster (5.491s → 3.900s)
- Chat history analysis working correctly

## Future Enhancements

Potential improvements:
1. **Adaptive tool selection** - Learn from user patterns
2. **Caching layer** - Cache common queries
3. **Multi-modal support** - Chart generation
4. **Sentiment analysis tools** - Dedicated sentiment APIs
5. **Real-time streaming** - WebSocket support
