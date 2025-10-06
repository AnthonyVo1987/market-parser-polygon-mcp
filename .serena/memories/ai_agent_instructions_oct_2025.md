# AI Agent Instructions - Post-MCP Removal (October 2025)

## Current State (Post-MCP Removal)

**AI Agent**: OpenAI Agents SDK v0.2.9
**Model**: GPT-5-Nano (EXCLUSIVE)
**Total Tools**: 12 (1 Finnhub + 11 Polygon Direct API)
**Architecture**: Direct Python API integration (no MCP)

## System Prompt Location

`src/backend/services/agent_service.py` → `get_enhanced_agent_instructions()` function

## Key Features of Current Instructions

### 1. Tool Count and Architecture
- Lists exactly **12 SUPPORTED TOOLS**
- All tools use **Direct Python APIs** (no MCP)
- Clear categorization: Finnhub (1) + Polygon (11)

### 2. Direct API Tool Descriptions

**Finnhub (1 tool):**
- `get_stock_quote(symbol: str)` - Real-time stock quotes from Finnhub

**Polygon Direct API (11 tools):**

**Market Data:**
1. `get_market_status_and_date_time()` - Market status and current datetime
2. `get_stock_quote_multi(symbols: str)` - Multiple stock quotes (comma-separated)
3. `get_options_quote_single(ticker: str)` - Single option contract quote

**OHLC Data:**
4. `get_OHLC_bars_custom_date_range(ticker, multiplier, timespan, from_date, to_date)` - OHLC bars for date range
5. `get_OHLC_bars_specific_date(ticker, date)` - OHLC bars for specific date
6. `get_OHLC_bars_previous_close(ticker)` - Previous close OHLC

**Technical Analysis:**
7. `get_ta_sma(ticker, timestamp, timespan, adjusted, window, series_type, order, limit)` - SMA indicator
8. `get_ta_ema(ticker, timestamp, timespan, adjusted, window, series_type, order, limit)` - EMA indicator
9. `get_ta_rsi(ticker, timestamp, timespan, adjusted, window, series_type, order, limit)` - RSI indicator
10. `get_ta_macd(ticker, timestamp, timespan, adjusted, short_window, long_window, signal_window, series_type, order, limit)` - MACD indicator

### 3. Critical Rules for Tool Usage

**RULE #1: Market Data Selection**
- Single ticker → use `get_stock_quote` or `get_stock_quote_multi`
- Multiple tickers → use `get_stock_quote_multi` (comma-separated)
- Options → use `get_options_quote_single`

**RULE #2: Always Include Required Parameters**
- All TA tools require: `ticker`, `timestamp`, `timespan`
- OHLC tools require: `ticker`, date parameters
- No parameter should be omitted

**RULE #3: Work with Available Data**
- ALWAYS use whatever data is returned, even if less than expected
- If request 2 weeks but get 1 week → PROCEED with 1 week
- NEVER fail or refuse because got less data than requested
- Example: Weekly change needs AT LEAST 1 week, not exactly 2

**RULE #4: Market Closed = Still Provide Data**
- 🔴 CRITICAL: Market being CLOSED is NOT a reason to refuse
- ALWAYS provide last available price when market is closed
- Use snapshot tools - they return last trade price even when closed
- If snapshot fails, fallback to OHLC tools
- NEVER respond with "unavailable" or ask user to retry
- Format: "SPY: 669.21 (Note: Market closed; last traded price)"

**RULE #5: Quick Response Enforcement**
- All user prompts include "Quick Response Needed with minimal tool calls"
- Use MINIMUM tool calls necessary
- Prefer single tool call over multiple
- Don't over-engineer responses

**RULE #6: Tool Call Transparency**
- At END of EVERY response, list each tool call with reasoning
- Format: `tool_name(parameters)` - Reasoning for selection
- Helps users understand which tools were used and why

### 4. Response Format Requirements

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

### 5. Optimized Model Settings

**Configuration** (from `get_optimized_model_settings()`):
```python
{
    "model": "gpt-5-nano",
    "max_tokens": 16384,
    "temperature": 0.1,  # Deterministic responses
    "parallel_tool_calls": True,  # Faster execution
    "rate_limits": {
        "max_requests_per_minute": 30,
        "max_tokens_per_minute": 200000  # GPT-5-Nano specific
    }
}
```

**Rationale:**
- **Low temperature (0.1)**: Consistent, deterministic financial analysis
- **Parallel tool calls**: Faster when multiple tools needed
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

### Key Improvements (October 2025)

**1. Tool Selection Accuracy**
- Fixed confusion between single/multi ticker tools
- Clear decision tree for tool selection
- Explicit parameter requirements

**2. Error Handling**
- No longer refuses when market closed
- Works with partial data
- Better fallback strategies

**3. Performance Optimization**
- Quick response enforcement
- Minimal tool calls requirement
- Parallel tool execution

**4. User Experience**
- Structured output format
- Clear sentiment indicators
- Tool transparency section

## Testing Validation

### 3x Sanity Check Results (Oct 2025):
- **Run 1**: 7/7 tests (100%), 17.78s avg
- **Run 2**: 7/7 tests (100%), 18.10s avg
- **Run 3**: 7/7 tests (100%), 15.49s avg

### 10-Run Baseline Results (Oct 2025):
- **Total**: 270/270 tests (100%)
- **Average**: 6.10s per query
- **Std Dev**: 0.80s (highly consistent)
- **Performance**: 70% faster than legacy MCP

## Tool Usage Examples

### Correct Tool Selection

**Market Status:**
```python
get_market_status_and_date_time()
# Returns: market status, date, time
```

**Single Stock Quote:**
```python
get_stock_quote(symbol="NVDA")
# OR
get_stock_quote_multi(symbols="NVDA")
```

**Multiple Stock Quotes:**
```python
get_stock_quote_multi(symbols="SPY,QQQ,IWM")
# Note: Comma-separated string
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
• get_stock_quote_multi(symbols="SPY") - Retrieved last trade price
```

**Incorrect Response (NEVER DO THIS):**
```
❌ "SPY price unavailable (market closed). Please try again when market opens."
❌ "I cannot provide current price as the market is closed."
❌ "Data not available; market is currently closed."
```

## Performance Metrics

### Response Times (Post-MCP Removal):
- **Average**: 6.10s (EXCELLENT)
- **Range**: 5.25s - 7.57s
- **Improvement**: 70% faster than legacy MCP (20s avg)

### Success Rates:
- **Test Pass Rate**: 100% (270/270 in 10-run baseline)
- **Tool Selection Accuracy**: 100%
- **Response Quality**: Consistent structured output

## Files Involved

**Primary File:**
- `src/backend/services/agent_service.py`
  - `get_enhanced_agent_instructions()` - System prompt
  - `get_optimized_model_settings()` - Model config
  - `create_agent()` - Agent initialization

**Tool Definitions:**
- `src/backend/tools/polygon_tools.py` - 11 Polygon Direct API tools
- `src/backend/tools/finnhub_tools.py` - 1 Finnhub tool

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
./CLI_test_regression.sh 3

# Verify consistency across runs
```

### Documentation Updates

After modifying agent instructions:
1. Update this memory file
2. Update `CLAUDE.md` Last Completed Task
3. Run test suite and include results
4. Update `project_architecture.md` if tool count changes

## Future Enhancements

Potential improvements:
1. **Adaptive tool selection** - Learn from user patterns
2. **Caching layer** - Cache common queries (e.g., market status)
3. **Error recovery** - Automatic fallback strategies
4. **Multi-modal support** - Add chart generation tools
5. **Sentiment analysis tools** - Dedicated sentiment APIs
6. **Real-time streaming** - WebSocket support for live data
