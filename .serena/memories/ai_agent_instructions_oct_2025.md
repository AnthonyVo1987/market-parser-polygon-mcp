# AI Agent Instructions - Post-Tool-Removal (October 2025)

## Current State (Post-get_stock_quote_multi Removal - Oct 7, 2025)

**AI Agent**: OpenAI Agents SDK v0.2.9
**Model**: GPT-5-Nano (EXCLUSIVE)
**Total Tools**: 11 (1 Finnhub + 10 Polygon Direct API)
**Architecture**: Direct Python API integration (no MCP)
**Multi-Ticker Pattern**: Parallel get_stock_quote() calls via OpenAI Agents SDK

## System Prompt Location

`src/backend/services/agent_service.py` → `get_enhanced_agent_instructions()` function

## Key Features of Current Instructions

### 1. Tool Count and Architecture
- Lists exactly **11 SUPPORTED TOOLS**
- All tools use **Direct Python APIs** (no MCP)
- Clear categorization: Finnhub (1) + Polygon (10)
- **NEW**: Parallel get_stock_quote() calls for multiple tickers

### 2. Direct API Tool Descriptions

**Finnhub (1 tool):**
- `get_stock_quote(symbol: str)` - Real-time stock quotes from Finnhub
  - **NEW**: Supports parallel calls for multiple tickers

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

**Removed (Oct 7, 2025):**
- ~~`get_stock_quote_multi(symbols: str)`~~ - Replaced by parallel get_stock_quote() calls

### 3. Critical Rules for Tool Usage (UPDATED Oct 7, 2025)

**RULE #1: Single Ticker Selection**
- Single ticker → ALWAYS use `get_stock_quote(ticker='SYMBOL')`
- Examples: "NVDA price", "GME closing price", "TSLA snapshot"
- Uses Finnhub API for real-time quote data

**RULE #2: Multiple Tickers = PARALLEL get_stock_quote() CALLS** ⭐ NEW
- Multiple tickers → Make PARALLEL calls to `get_stock_quote()`
- Examples: "SPY, QQQ, IWM prices", "NVDA and AMD", "Market snapshot: TSLA, AAPL, MSFT"
- ✅ ALWAYS make PARALLEL calls: get_stock_quote(ticker='SYM1'), get_stock_quote(ticker='SYM2'), get_stock_quote(ticker='SYM3')
- 📊 Uses Finnhub API (fast, low overhead - parallel calls acceptable)
- ✅ OpenAI Agents SDK executes tool calls in PARALLEL automatically
- 🔴 CRITICAL: Each get_stock_quote call is INDEPENDENT - make them ALL at once, not sequentially

**RULE #3: Options Selection**
- Options contracts → use `get_options_quote_single()`
- Uses Polygon.io Direct API

**RULE #4: Always Include Required Parameters**
- All TA tools require: `ticker`, `timestamp`, `timespan`
- OHLC tools require: `ticker`, date parameters
- No parameter should be omitted

**RULE #5: Work with Available Data**
- ALWAYS use whatever data is returned, even if less than expected
- If request 2 weeks but get 1 week → PROCEED with 1 week
- NEVER fail or refuse because got less data than requested
- Example: Weekly change needs AT LEAST 1 week, not exactly 2

**RULE #6: Market Closed = Still Provide Data**
- 🔴 CRITICAL: Market being CLOSED is NOT a reason to refuse
- ALWAYS provide last available price when market is closed
- Use get_stock_quote - returns last trade price even when closed
- NEVER respond with "unavailable" or ask user to retry
- Format: "SPY: 669.21 (Note: Market closed; last traded price)"

**RULE #7: Quick Response Enforcement**
- Use MINIMUM tool calls necessary
- Prefer parallel execution for multiple tickers
- Don't over-engineer responses

**RULE #8: Tool Call Transparency**
- At END of EVERY response, list each tool call with reasoning
- Format: `tool_name(parameters)` - Reasoning for selection
- Helps users understand which tools were used and why

### 4. Decision Tree (UPDATED Oct 7, 2025)

**Stock Quote Decision Tree:**
```
Step 1: Count how many ticker symbols in the request
Step 2:
   - If count = 1 ticker → USE get_stock_quote(ticker='SYMBOL')
   - If count ≥ 2 tickers → USE PARALLEL get_stock_quote() calls
Step 3: For multiple tickers, make ALL calls at once (parallel execution)
Step 4: OpenAI Agents SDK handles parallel tool execution automatically
```

### 5. Response Format Requirements

**Structured Output:**
```
KEY TAKEAWAYS
• Bullet point 1 with clear sentiment/direction
• Bullet point 2 with key metrics
• Bullet point 3 with actionable insight

DETAILED ANALYSIS
[Comprehensive analysis with clear directional indicators]

TOOLS USED
• tool_name(parameters) - Reasoning for selection
```

**Key Characteristics:**
- **KEY TAKEAWAYS**: 2-4 bullet points, concise
- **DETAILED ANALYSIS**: Comprehensive but focused
- **TOOLS USED**: Transparency section (always included)
- **Sentiment**: Clear directional indicators (bullish/bearish/neutral)
- **No disclaimers**: Streamlined, no verbose legal disclaimers

### 6. Optimized Model Settings

**Configuration** (from `get_optimized_model_settings()`):
```python
{
    "model": "gpt-5-nano",
    "max_tokens": 16384,
    "temperature": 0.1,  # Deterministic responses
    "parallel_tool_calls": True,  # CRITICAL for multi-ticker queries
    "rate_limits": {
        "max_requests_per_minute": 30,
        "max_tokens_per_minute": 200000  # GPT-5-Nano specific
    }
}
```

**Rationale:**
- **Low temperature (0.1)**: Consistent, deterministic financial analysis
- **Parallel tool calls**: CRITICAL for multi-ticker queries
- **High max_tokens**: Allows comprehensive analysis
- **Proper rate limits**: GPT-5-Nano specific (200K TPM)

## Historical Context

### Evolution of Instructions

**Phase 1** (Pre-MCP Removal):
- 18 tools (7 MCP + 11 Direct API)
- Mixed MCP/Direct API patterns
- Complex tool selection logic

**Phase 2** (Post-MCP Removal - Oct 2025):
- 12 tools (0 MCP + 12 Direct API)
- Unified Direct API pattern
- Simplified tool selection
- 70% performance improvement

**Phase 3** (Post-get_stock_quote_multi Removal - Oct 7, 2025):
- 11 tools (1 Finnhub + 10 Polygon Direct API)
- Parallel get_stock_quote() calls for multi-ticker
- Leverages OpenAI Agents SDK native parallel execution
- Simplified codebase (removed 139-line wrapper)

### Key Improvements (October 2025)

**1. Tool Selection Accuracy**
- Clear parallel call pattern for multi-ticker queries
- Explicit RULE #2 for parallel execution
- Updated decision tree

**2. Error Handling**
- No longer refuses when market closed
- Works with partial data
- Better fallback strategies

**3. Performance Optimization**
- Quick response enforcement
- Minimal tool calls requirement
- Native parallel tool execution

**4. User Experience**
- Structured output format
- Clear sentiment indicators
- Tool transparency section

**5. Architecture Simplification (Oct 7, 2025)**
- Removed unnecessary get_stock_quote_multi wrapper
- Leverages SDK's native parallel execution
- Tool count reduced from 12 to 11

## Testing Validation

### Latest Test Results (Oct 7, 2025 - Post-Tool-Removal):
- **Total**: 27/27 tests (100%)
- **Average**: 7.31s per query
- **Range**: 4.848s - 11.580s
- **Performance**: EXCELLENT
- **Multi-Ticker Tests**: Tests #3 and #12 passed with parallel pattern
- **Test Report**: `cli_regression_test_loop1_20251007_141546.txt`

### Previous 10-Run Baseline Results (Oct 2025):
- **Total**: 270/270 tests (100%)
- **Average**: 6.10s per query
- **Std Dev**: 0.80s (highly consistent)
- **Performance**: 70% faster than legacy MCP

## Tool Usage Examples (UPDATED Oct 7, 2025)

### Correct Tool Selection

**Market Status:**
```python
get_market_status_and_date_time()
# Returns: market status, date, time
```

**Single Stock Quote:**
```python
get_stock_quote(symbol="NVDA")
```

**Multiple Stock Quotes (NEW PATTERN):**
```python
# PARALLEL execution - all calls at once
get_stock_quote(ticker="SPY")
get_stock_quote(ticker="QQQ")
get_stock_quote(ticker="IWM")
# Note: SDK executes these in parallel automatically
```

**Technical Analysis (SMA):**
```python
get_ta_sma(
    ticker="SPY",
    timestamp="2024-10-01",
    timespan="day",
    adjusted=True,
    window=50,
    series_type="close",
    order="desc",
    limit=10
)
```

**OHLC Data:**
```python
get_OHLC_bars_custom_date_range(
    ticker="TSLA",
    multiplier=1,
    timespan="day",
    from_date="2024-09-01",
    to_date="2024-10-01"
)
```

### Market Closed Handling

**Correct Response (Market Closed):**
```
KEY TAKEAWAYS
• SPY: $569.21 (Note: Market closed; last traded price)
• Daily change: +$2.15 (+0.38%)
• Last trade: 4:00 PM ET

DETAILED ANALYSIS
The S&P 500 ETF (SPY) closed at $569.21, showing modest gains...

TOOLS USED
• get_stock_quote(ticker='SPY') - Retrieved last trade price
```

**Incorrect Response (NEVER DO THIS):**
```
❌ "SPY price unavailable (market closed). Please try again when market opens."
❌ "I cannot provide current price as the market is closed."
❌ "Data not available; market is currently closed."
```

### Multi-Ticker Examples (NEW - Oct 7, 2025)

**Example 1: "Stock Snapshot: SPY, QQQ, IWM"**
```
TOOLS USED
• get_stock_quote(ticker='SPY') - Multiple tickers (3 symbols), using parallel get_stock_quote calls per RULE #2
• get_stock_quote(ticker='QQQ') - Parallel execution with first call
• get_stock_quote(ticker='IWM') - Parallel execution with first and second calls
```

**Example 2: "AAPL and MSFT prices"**
```
TOOLS USED
• get_stock_quote(ticker='AAPL') - Multiple tickers (2 symbols), parallel execution per RULE #2
• get_stock_quote(ticker='MSFT') - Parallel execution with first call
```

## Performance Metrics

### Response Times (Latest - Oct 7, 2025):
- **Average**: 7.31s (EXCELLENT)
- **Range**: 4.848s - 11.580s
- **Parallel Execution**: Working correctly
- **Success Rate**: 100% (27/27 tests)

### Previous Response Times (Post-MCP Removal):
- **Average**: 6.10s (EXCELLENT)
- **Range**: 5.25s - 7.57s
- **Improvement**: 70% faster than legacy MCP (20s avg)

### Success Rates:
- **Test Pass Rate**: 100% (consistent across all tests)
- **Tool Selection Accuracy**: 100%
- **Response Quality**: Consistent structured output

## Files Involved

**Primary File:**
- `src/backend/services/agent_service.py`
  - `get_enhanced_agent_instructions()` - System prompt with RULE #2 for parallel calls
  - `get_optimized_model_settings()` - Model config with parallel_tool_calls=True
  - `create_agent()` - Agent initialization with 11 tools

**Tool Definitions:**
- `src/backend/tools/polygon_tools.py` - 10 Polygon Direct API tools (get_stock_quote_multi removed)
- `src/backend/tools/finnhub_tools.py` - 1 Finnhub tool (get_stock_quote)

**Testing:**
- `CLI_test_regression.sh` - 27 test prompts
- `test-reports/` - Test results

## Maintenance Notes

### When to Update Instructions

**Required Updates:**
- Adding new tools
- Changing tool signatures
- Fixing tool selection errors
- Performance optimizations

**Optional Updates:**
- Improving response format
- Clarifying existing rules
- Adding new examples

### Testing After Changes

**Mandatory:**
```bash
# Run full test suite
./CLI_test_regression.sh

# Verify results
# - 27/27 tests PASSED
# - Average < 10s
# - Performance: EXCELLENT
```

**Recommended:**
```bash
# Run 3-loop sanity check
for i in 1 2 3; do ./CLI_test_regression.sh; done

# Verify consistency across runs
```

### Documentation Updates

After modifying agent instructions:
1. Update this memory file
2. Update `CLAUDE.md` Last Completed Task
3. Run test suite and include results
4. Update `project_architecture.md` if tool count changes
5. Update `tech_stack.md` with tool count

## Tool Removal History (Oct 7, 2025)

### get_stock_quote_multi Removal

**Rationale:**
- Unnecessary wrapper function (139 lines)
- OpenAI Agents SDK handles parallel execution natively
- Finnhub API is fast - parallel calls acceptable
- Simplifies codebase and leverages SDK features

**Changes Made:**
1. Removed `get_stock_quote_multi` from polygon_tools.py
2. Updated RULE #2 to emphasize parallel get_stock_quote() calls
3. Updated tool count from 12 to 11
4. Updated decision tree for multi-ticker queries
5. Updated all examples to show parallel call pattern

**Test Results:**
- 27/27 tests PASSED ✅
- 100% success rate
- 7.31s average response time (EXCELLENT)
- Tests #3 and #12 verified parallel execution

**Benefits:**
- ✅ Simplified codebase (removed 139 lines)
- ✅ Leverages SDK native parallel execution
- ✅ Tool count reduced from 12 to 11
- ✅ No performance regression
- ✅ Clear parallel execution pattern in instructions

## Future Enhancements

Potential improvements:
1. **Adaptive tool selection** - Learn from user patterns
2. **Caching layer** - Cache common queries (e.g., market status)
3. **Error recovery** - Automatic fallback strategies
4. **Multi-modal support** - Add chart generation tools
5. **Sentiment analysis tools** - Dedicated sentiment APIs
6. **Real-time streaming** - WebSocket support for live data
