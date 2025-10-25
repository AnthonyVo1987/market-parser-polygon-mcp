# AI Agent Instructions - Post-Tool-Removal (October 2025)

## Agent Persistence & Initialization (October 2025)

### Architecture: ONE Persistent Agent Per Lifecycle

**Problem Solved**: Application was creating a NEW OpenAI agent for EVERY user message, wasting tokens and preventing prompt caching.

**Current Architecture** (CORRECT ✅):
- Create ONE persistent agent per lifecycle (startup)
- Agent reused for ALL messages in session
- System prompt cached after first message (50% token savings)
- Agent maintains context across entire session

**OLD Architecture** (INCORRECT ❌):
- Created NEW agent for EVERY message
- System prompt sent with EVERY message (2000+ tokens wasted)
- No prompt caching benefits
- No agent memory across messages

### Implementation Pattern: CLI = Core, GUI = Wrapper

**Following commit b866f0a principle:**

```
Backend/CLI owns core business logic
         ↓
Frontend/GUI calls CLI functions
         ↓
  No code duplication
```

### Core Functions (src/backend/cli.py)

**1. initialize_persistent_agent()** - Single Source of Truth
- Creates agent ONCE at startup
- Both CLI and GUI call this function
- Returns configured Agent instance

**2. process_query()** - Core Business Logic
- Processes queries using persistent agent
- Both CLI and GUI call this function
- Takes persistent agent as parameter

### CLI Mode
- Creates agent ONCE at startup via `initialize_persistent_agent()`
- Reuses same agent for all user inputs
- Calls `process_query()` for each message

### GUI Mode (FastAPI)
- FastAPI lifespan creates agent ONCE at startup via `initialize_persistent_agent()`
- Stores agent in global shared resources
- Dependency injection provides agent to endpoints
- Chat endpoint calls `process_query()` for each message

### Key Benefits

**1. Token Efficiency (50% Savings)**:
- System prompt cached after first message
- Subsequent messages use cached prompt
- 50% reduction in input tokens

**2. Reduced Overhead**:
- Agent creation cost paid ONCE at startup
- Faster response times
- Less CPU usage

**3. Proper Agent Memory**:
- Same agent maintains context across entire session
- Better conversation flow
- Proper chat history

**4. Best Practices Compliance**:
- Follows OpenAI Agents SDK best practices
- Matches real-world AI agent usage patterns
- Enables prompt caching optimizations

### Files Involved

**Core Business Logic**:
- `src/backend/cli.py` - Shared functions, CLI mode implementation
- `src/backend/services/agent_service.py` - Agent creation logic

**GUI Integration**:
- `src/backend/main.py` - FastAPI lifespan with agent initialization
- `src/backend/routers/chat.py` - Chat endpoint using shared functions
- `src/backend/dependencies.py` - Dependency injection for shared resources

### Test Validation

- 38/38 tests PASSED (100% success rate)
- Average: 11.05s (EXCELLENT rating)
- Session persistence: VERIFIED across all tests
- All 38 tests run in SINGLE CLI session with SINGLE agent
- Test Report: `test-reports/test_cli_regression_loop1_2025-10-09_20-33.log`

---

## Current State (Post-OHLC-Fix - Oct 7, 2025 Evening)

**AI Agent**: OpenAI Agents SDK v0.2.9
**Model**: GPT-5-Nano (EXCLUSIVE)
**Total Tools**: 11 (1 Finnhub + 10 Polygon Direct API)
**Architecture**: Direct Python API integration (no MCP)
**Multi-Ticker Pattern**: Parallel get_stock_quote() calls via OpenAI Agents SDK
**Agent Persistence**: ONE agent per lifecycle, reused for all messages (Oct 2025)
**Latest Fixes**: OHLC display requirements + Support/Resistance redundant call prevention

## System Prompt Location

`src/backend/services/agent_service.py` → `get_enhanced_agent_instructions()` function

## Key Features of Current Instructions

### 1. Tool Count and Architecture
- Lists exactly **13 SUPPORTED TOOLS** ⭐ UPDATED Oct 25, 2025
- All tools use **Direct Python APIs** (no MCP)
- Clear categorization: Finnhub (1) + Polygon (9) + Tradier (3)
- **Parallel get_stock_quote() calls** for multiple tickers
- **OHLC display requirements** (RULE #6 - Oct 7 evening)
- **Chat history analysis** as RULE #1 (CRITICAL - Oct 25)
- **Persistent agent** (ONE agent per lifecycle, reused for all messages)

### 2. Direct API Tool Descriptions

**Finnhub (1 tool):**
- `get_stock_quote(symbol: str)` - Real-time stock quotes from Finnhub
  - Supports parallel calls for multiple tickers

**Polygon Direct API (9 tools):**

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

**Tradier API (3 tools):** ⭐ NEW Oct 25, 2025

**Options Chains:**
10. `get_options_chain_both(ticker, current_price, expiration_date)` - Both call and put options chains (RECOMMENDED)
    - Returns 20 strikes for each chain (10 above + 10 below current price)
    - Single API call, efficient and comprehensive
    - Identical strike prices for both call and put chains
    - Sorted descending (highest strike first)
    - Use for comprehensive options analysis

11. `get_call_options_chain(ticker, current_price, expiration_date)` - Call options chain only
    - Returns 20 strikes centered around current price
    - Use when user explicitly requests ONLY call options
    - Sorted descending

12. `get_put_options_chain(ticker, current_price, expiration_date)` - Put options chain only
    - Returns 20 strikes centered around current price
    - Use when user explicitly requests ONLY put options
    - Sorted descending

**Removed (Oct 7, 2025 afternoon):**
- ~~`get_stock_quote_multi(symbols: str)`~~ - Replaced by parallel get_stock_quote() calls

### 3. Critical Rules for Tool Usage (UPDATED Oct 25, 2025 - Restructured)

**RULE #1: 🔴 ANALYZE CHAT HISTORY BEFORE MAKING TOOL CALLS - AVOID REDUNDANT CALLS** ⭐ CRITICAL
- **MANDATORY**: Analyze conversation history for existing data BEFORE making ANY tool calls
- **Purpose**: Prevent redundant API calls, improve response time, reduce costs
- **Process**:
  1. Review chat history for previously retrieved data
  2. Check if current request can be answered with existing data
  3. Only make NEW tool calls if data is missing or outdated
  4. State "No tool calls needed - using existing data from previous queries" when reusing data

**Key Scenarios:**

**Scenario 1 - Technical Analysis After Price Retrieval:**
- Previous: Retrieved SPY price, SMA 20/50/200, EMA 20/50/200, RSI-14, MACD
- Current: User asks "Perform technical analysis: SPY"
- ✅ **CORRECT**: Use existing data, NO new tool calls
- ❌ **WRONG**: Making NEW calls for SMA/EMA/RSI/MACD when already retrieved

**Scenario 2 - Support & Resistance Levels:**
- Previous: Already retrieved SPY price, SMA 20/50/200, EMA 20/50/200, RSI-14, MACD
- Current: User asks "Support & Resistance Levels: SPY"
- ✅ **CORRECT**: Use existing data, NO new tool calls
- **REASONING**: Support/Resistance derived from existing price, SMA/EMA levels
- ❌ **WRONG**: Making NEW calls for SMA/EMA/RSI/MACD when already retrieved

**Scenario 3 - Options Analysis After Options Chain Retrieval:**
- Previous: Retrieved SPY call and put options chains
- Current: User asks "Analyze options chain and find call/put walls: SPY"
- ✅ **CORRECT**: Use existing options data, NO new tool calls
- ❌ **WRONG**: Re-fetching options chains when already retrieved

**Scenario 4 - Multi-Step Analysis:**
- Previous: Retrieved WDC, AMD, SOUN prices and TA indicators
- Current: User asks "Compare technical analysis: WDC, AMD, SOUN"
- ✅ **CORRECT**: Use existing data for all three tickers, NO new tool calls
- ❌ **WRONG**: Re-fetching any data that was already retrieved

**Transparency Requirements:**
- Always state when reusing data: "No tool calls needed - using existing data from previous queries"
- Be explicit about which data is being reused
- Only make new calls when truly necessary

**RULE #2: Single Ticker Selection**
- Single ticker → ALWAYS use `get_stock_quote(ticker='SYMBOL')`
- Examples: "NVDA price", "GME closing price", "TSLA snapshot"
- Uses Finnhub API for real-time quote data

**RULE #3: Multiple Tickers = PARALLEL get_stock_quote() CALLS**
- Multiple tickers → Make PARALLEL calls to `get_stock_quote()`
- Max 3 parallel calls per batch (rate limiting protection)
- Examples: "SPY, QQQ, IWM prices", "NVDA and AMD"
- ✅ ALWAYS make PARALLEL calls: get_stock_quote(ticker='SYM1'), get_stock_quote(ticker='SYM2'), get_stock_quote(ticker='SYM3')
- 📊 Uses Finnhub API (fast, low overhead)
- ✅ OpenAI Agents SDK executes tool calls in PARALLEL automatically
- 🔴 CRITICAL: Each get_stock_quote call is INDEPENDENT - make them ALL at once

**RULE #4: Options Chain Selection** ⭐ UPDATED Oct 25, 2025

**For BOTH Call AND Put Options Chains (RECOMMENDED - DEFAULT):**
- ✅ **FIRST CHOICE**: Use `get_options_chain_both(ticker, current_price, expiration_date)`
- Returns BOTH call and put options chains in ONE response
- Single API call, more efficient than separate calls
- Shows 20 strikes for each chain (10 above + 10 below current price)
- Identical strike prices for both call and put chains
- **Use when**: User asks for "both", "call and put", "options chain", or is ambiguous
- Examples:
  - "Show me call and put options for SPY" → get_options_chain_both()
  - "Get the full options chain for NVDA" → get_options_chain_both()
  - "I need options for AAPL" → get_options_chain_both() (default to comprehensive)

**For ONLY Call Options OR ONLY Put Options (SPECIFIC):**
- Call options only → use `get_call_options_chain(ticker, current_price, expiration_date)`
- Put options only → use `get_put_options_chain(ticker, current_price, expiration_date)`
- Shows 20 strikes centered around current price (10 above + 10 below)
- **Use when**: User explicitly requests ONLY calls or ONLY puts
- Examples:
  - "Show me ONLY call options for SPY" → get_call_options_chain()
  - "Get PUT options for NVDA" → get_put_options_chain()

**For Single Option Contracts:**
- Single option quote → use `get_options_quote_single()`
- Uses Polygon.io Direct API
- **Use when**: User asks for a specific option contract with strike and expiration

**Decision Tree:**
```
User Query → Analyze Intent → Select Tool

"call and put options" → BOTH chains → get_options_chain_both()
"full options chain" → BOTH chains → get_options_chain_both()
"options for [ticker]" → Ambiguous → get_options_chain_both() (default)
"call options only" → Calls only → get_call_options_chain()
"put options only" → Puts only → get_put_options_chain()
"[ticker] SPY250131C00680000" → Single contract → get_options_quote_single()
```

**Performance Note:**
- get_options_chain_both() makes ONE API call (vs two separate calls)
- ~50% faster response time for full options analysis
- Recommended as default choice for comprehensive options data

**RULE #5: Market Status & Date/Time**
- Market status queries → use `get_market_status_and_date_time()`
- Returns market status, exchange statuses, server datetime

**RULE #6: OHLC Data with Display Requirements** ⭐ UPDATED Oct 7 Evening
- Historical OHLC prices → use get_OHLC_bars_* tools
- Date validation required (weekends/holidays/future dates)
- **CRITICAL DISPLAY REQUIREMENTS FOR OHLC BARS:**
  - **For custom date range**: MUST show start open, end close, $ and % change, period high/low, trading days
  - **For specific date**: MUST show Date, Open, High, Low, Close, Volume
  - ❌ NEVER just say "data retrieved" without actual numbers
  - ❌ NEVER say "If you'd like, I can show the data" - show it immediately
  - ✅ Example GOOD: "SPY Q1 2025: Started 1/2/25 at $580.50, ended 3/31/25 at $612.30 (+$31.80, +5.48%), High: $615.25, Low: $575.10, 60 days"
  - ❌ Example BAD: "SPY daily OHLC bars retrieved for Q1 2025" [USELESS!]

**RULE #7: Work with Available Data**
- ALWAYS use whatever data is returned, even if less than expected
- NEVER fail or refuse because got less data than requested

**RULE #8: Market Closed = Still Provide Data**
- 🔴 CRITICAL: Market being CLOSED is NOT a reason to refuse
- ALWAYS provide last available price when market closed
- Use fallback sequence: get_stock_quote → get_OHLC_bars_previous_close

**RULE #9: Technical Analysis - Check Chat History First**
- Minimum TA requirements: RSI-14, MACD, SMA 20/50/200, EMA 20/50/200
- FIRST: Check chat history for existing TA data
- IF all minimum TA data already retrieved → NO NEW TOOL CALLS
- Provide actual ANALYSIS (trends, momentum, volatility, patterns)
- NOT just raw numbers

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

**Phase 5** (Persistent Agent Architecture - Oct 2025): ⭐ CURRENT
- 11 tools (unchanged)
- ONE persistent agent per lifecycle (not per message)
- CLI = Single Source of Truth, GUI = Wrapper
- 50% token savings via prompt caching

### Latest Fixes (Oct 2025 - Persistent Agent)

**1. Agent Lifecycle Management:**
- **Problem**: App was creating NEW agent for EVERY message
- **Fix**: Create ONE persistent agent at startup, reuse for all messages
- **Architecture**: CLI owns agent initialization, GUI imports CLI functions
- **Result**: 50% token savings via prompt caching, proper agent memory

**2. OHLC Display Requirements (RULE #5):**
- **Problem**: AI Agent just said "data retrieved" without showing actual prices
- **Fix**: Added "CRITICAL DISPLAY REQUIREMENTS FOR OHLC BARS" section
- **Result**: Test 15 (SPY OHLC Q1) now shows start: 589.39, end: 559.39, change: -4.31%, high: 613.23, low: 549.83, 60 days ✅

**3. Support & Resistance Redundant Calls (RULE #9):**
- **Problem**: AI Agent was calling get_ta_sma/ema/rsi/macd AGAIN for Support & Resistance even when all data already retrieved
- **Fix**: Added Scenario 5 to RULE #9 explicitly telling AI to use existing data
- **Result**: Test 12 reduced from 5.491s to 3.900s (29% faster) ✅

**4. New Test Suite (test_cli_regression.sh):**
- **Expansion**: 38 comprehensive tests (vs previous 35)
- **Coverage**: SPY sequence (16), NVDA sequence (16), Multi-ticker WDC/AMD/GME (6)
- **Validation**: Parallel calls, chat history analysis, OHLC display, agent persistence

## Testing Validation

### Latest Test Results (Oct 2025 - Persistent Agent):
- **Total**: 38/38 tests (100%)
- **Average**: 11.05s per query
- **Range**: 2.188s - 31.599s
- **Performance**: EXCELLENT
- **Agent**: Single persistent agent for all 38 tests ✅
- **Prompt Caching**: System prompt cached after first message (50% token savings) ✅
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-09_20-33.log`

### Previous Test Results (Oct 7 Evening - Post-OHLC-Fix):
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

### Previous Test Results (Oct 7 Afternoon - Post-Tool-Removal):
- **Total**: 27/27 tests (100%)
- **Average**: 7.31s per query
- **Range**: 4.848s - 11.580s

### Previous 10-Run Baseline (Oct 2025):
- **Total**: 270/270 tests (100%)
- **Average**: 6.10s per query
- **Improvement**: 70% faster than legacy MCP

## Tool Usage Examples (UPDATED Oct 2025)

### Agent Persistence Examples (NEW)

**Correct Architecture (Persistent Agent ✅):**
```
# CLI Mode
cli_session = SQLiteSession("cli_session")
analysis_agent = initialize_persistent_agent()  # Create ONCE
await _run_cli_loop(cli_session, analysis_agent)  # Reuse for all messages

# GUI Mode (FastAPI Lifespan)
async def lifespan(fastapi_app: FastAPI):
    shared_agent = initialize_persistent_agent()  # Create ONCE
    set_shared_resources(shared_session, shared_agent)  # Store globally
    yield  # App runs, agent reused for all HTTP requests

# Chat Endpoint
shared_agent = get_agent()  # Get persistent agent
result = await process_query(shared_agent, shared_session, user_input)  # Reuse agent
```

**Incorrect Architecture (Agent Per Message ❌):**
```
# DON'T DO THIS - Creates agent for EVERY message
for user_input in messages:
    agent = create_agent()  # ❌ NEW agent each time
    result = await Runner.run(agent, user_input)  # ❌ No prompt caching
```

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

### Response Times (Latest - Oct 2025 with Persistent Agent):
- **Average**: 11.05s (EXCELLENT)
- **Range**: 2.188s - 31.599s
- **Agent**: Single persistent agent (no creation overhead)
- **Token Savings**: 50% via prompt caching
- **Success Rate**: 100% (38/38 tests)

### Response Times (Oct 7 Evening):
- **Average**: 11.62s (EXCELLENT)
- **Range**: 2.188s - 31.599s
- **Support & Resistance**: 3.900s (29% faster than before fix)

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

**Agent Persistence:**
- `src/backend/cli.py`
  - `initialize_persistent_agent()` - Single source of truth for agent creation
  - `process_query()` - Single source of truth for query processing
- `src/backend/main.py`
  - `lifespan()` - Creates persistent agent at FastAPI startup
- `src/backend/routers/chat.py`
  - `chat_endpoint()` - Uses persistent agent via dependency injection
- `src/backend/dependencies.py`
  - `set_shared_resources()` - Stores persistent agent
  - `get_agent()` - Returns persistent agent

**Tool Definitions:**
- `src/backend/tools/polygon_tools.py` - 10 Polygon Direct API tools
- `src/backend/tools/finnhub_tools.py` - 1 Finnhub tool

**Testing:**
- `test_cli_regression.sh` - 38-test suite (Oct 2025)
- `test-reports/` - Test results

## Maintenance Notes

### When to Update Instructions

**Required Updates:**
- Adding new tools
- Fixing tool selection errors
- Fixing response quality issues (like OHLC display)
- Performance optimizations
- Architecture changes (like persistent agent)

### Testing After Changes

**Mandatory:**
```bash
# Run 38-test suite
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Verify results
# - 38/38 tests PASSED
# - Average < 15s
# - Performance: EXCELLENT
# - All responses showing actual data (not just "data retrieved")
# - Agent persistence verified (single agent for all tests)
```

### Documentation Updates

After modifying agent instructions:
1. Update this memory file
2. Update `CLAUDE.md` Last Completed Task
3. Run test suite and include results
4. Update `project_architecture.md` if architecture changes
5. Update `tech_stack.md` if agent persistence changes

## Recent Fixes History (Oct 2025)

### Persistent Agent Architecture Implementation

**Rationale:** App was creating NEW agent for EVERY message, wasting tokens
**Changes:**
- Create ONE persistent agent at startup
- CLI owns agent initialization (initialize_persistent_agent function)
- CLI owns query processing (process_query function)
- GUI imports and calls CLI functions (no duplication)
- Agent reused for ALL messages in session
**Results:**
- 38/38 tests PASSED
- 50% token savings via prompt caching
- Proper agent memory across session
- Zero code duplication (CLI = core, GUI = wrapper)

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