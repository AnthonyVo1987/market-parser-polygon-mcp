# Technology Stack

## Core Technologies

### Backend
- **Framework**: FastAPI (latest)
- **Python Version**: 3.12.3
- **Package Manager**: uv 0.8.19
- **AI Integration**: OpenAI Agents SDK v0.2.9
- **AI Model**: GPT-5-Nano (EXCLUSIVE - no model selection)
- **Service Tier**: "default" (optimized for prototyping, better performance than "flex")
- **API Libraries**:
  - `openai-agents==0.2.9` (OpenAI Agents SDK)
  - `openai>=1.99.0,<1.100.0` (OpenAI Python SDK)
  - `finnhub-python>=2.4.25` (Finnhub Direct API)
  - `polygon-api-client>=1.14.0` (Polygon Python SDK)
  - Direct Polygon Python API integration (no MCP)

### Frontend
- **Framework**: React 18.2+
- **Build Tool**: Vite 5.2+
- **Language**: TypeScript
- **Node Version**: v24.6.0
- **Package Manager**: npm 11.6.0
- **UI Features**:
  - React Markdown for formatting
  - React Scan for performance monitoring
  - PWA support with vite-plugin-pwa

### Data Sources
- **Polygon.io**: Direct Python API integration (12 tools, updated Oct 9, 2025 - options chain bugs fixed)
- **Finnhub**: Custom Python API integration (1 tool)
- **Total AI Agent Tools**: 12 (updated Oct 8, 2025 - added 2 options chain tools)

### Development Tools
- **Python Linting**: pylint, black, isort, mypy
- **JS/TS Linting**: ESLint, Prettier, TypeScript compiler
- **Testing**: CLI regression test suite (test_cli_regression.sh - 36 tests)
- **Performance**: Lighthouse CI, React Scan
- **Version Control**: Git

## AI Agent Architecture

### OpenAI Agents SDK v0.2.9
- **Primary Model**: GPT-5-Nano (200K TPM rate limit)
- **Service Tier**: "default" (changed from "flex" Oct 8, 2025)
- **Integration Pattern**: Direct API tools (no MCP)
- **Performance**: 70% faster than legacy MCP architecture
- **Token Tracking**: Dual naming convention support (input_tokens/prompt_tokens)
- **Parallel Execution**: Native parallel tool execution for multiple ticker queries

#### Service Tier Configuration (Updated Oct 8, 2025)
- **Current Setting**: `service_tier: "default"` (in agent_service.py:344)
- **Previous Setting**: `service_tier: "flex"`
- **Change Reason**: Prototyping phase requires better performance; "flex" tier was causing compute resources rate limiting
- **Impact**: Improved response consistency and throughput for development testing
- **Configuration Location**: `src/backend/services/agent_service.py:344`
- **Validation**: 36/36 tests PASSED with 16.28s avg (EXCELLENT rating)

#### OpenAI Prompt Caching (October 2025)
- **Status**: Fully Integrated
- **API Version**: Responses API (OpenAI Agents SDK v0.2.9)
- **Automatic Activation**: Prompts >1024 tokens cached automatically
- **Cache Hit Detection**: `input_tokens_details.cached_tokens` field
- **Cost Savings**: 50% on cached input tokens, up to 80% latency reduction
- **Implementation**:
  - `token_utils.py`: Extracts cached tokens from SDK usage object
  - `response_utils.py`: CLI display with cache hit information
  - `chat.py`: API includes cachedInputTokens/cachedOutputTokens
  - Frontend: TypeScript types and React component display
- **Cache Optimization**: Agent instructions cached (sent with every message)

### Direct API Tools (12 Total - Updated Oct 9, 2025)

**Finnhub Custom API (1 tool):**
- `get_stock_quote` - Real-time stock quotes from Finnhub (supports parallel calls for multiple tickers)

**Polygon Direct API (11 tools - Updated Oct 9, 2025 - Bug Fixes):**

**Market Data (1 tool):**
- `get_market_status_and_date_time` - Market status and current datetime

**OHLC Bars (3 tools):**
- `get_OHLC_bars_custom_date_range` - OHLC bars for custom date range
- `get_OHLC_bars_specific_date` - OHLC bars for specific date
- `get_OHLC_bars_previous_close` - Previous close OHLC bars

**Technical Analysis (4 tools):**
- `get_ta_sma` - Simple Moving Average (SMA)
- `get_ta_ema` - Exponential Moving Average (EMA)
- `get_ta_rsi` - Relative Strength Index (RSI)
- `get_ta_macd` - Moving Average Convergence Divergence (MACD)

**Options Chain (2 tools - Updated Oct 9, 2025 - Critical Bug Fixes):**
- `get_call_options_chain` - Fetch EXACTLY 10 call option strikes above current price (ascending order)
- `get_put_options_chain` - Fetch EXACTLY 10 put option strikes below current price (descending order)

**REMOVED Oct 8, 2025:**
- `get_options_quote_single` - Single option quote (removed - inefficient, replaced with full options chain tools)

### Options Chain Tools (Updated Oct 9, 2025 - Bug Fixes)

**Purpose**: Fetch options chains with strike prices, Greeks, IV, volume, and open interest

**Implementation**:
- **Location**: `src/backend/tools/polygon_tools.py`
- **API**: Polygon.io `list_snapshot_options_chain` endpoint
- **Response Format**: JSON with strike prices as keys ($XXX.XX)
- **Data Fields**: price (option price), delta, gamma, theta, vega, implied_volatility, volume, open_interest
- **Decimal Precision**: All values rounded to 2 decimals with None-safe handling
- **10-Strike Limit**: Enforced via `list()[:10]` slice (fixed Oct 9, 2025)

**Critical Bug Fixes (Oct 9, 2025)**:
1. **10-Strike Limit Enforcement**: 
   - **Bug**: Tools were returning 174 total strikes (flooding messages)
   - **Root Cause**: For loop iterated through ALL API results without enforcing limit
   - **Fix**: Changed from `for option in client.list_snapshot_options_chain(...): options_chain.append(option)` to `options_chain = list(client.list_snapshot_options_chain(...))[:10]`
   - **Impact**: Reduced from 174 strikes to exactly 40 strikes total (10 per chain x 4 tests)

2. **None-Safe Rounding**:
   - **Bug**: `round(value, 2)` failed when API returned None values
   - **Error**: "type NoneType doesn't define __round__ method"
   - **Fix**: Added defensive None checks: `round(value if value is not None else 0.0, 2)`
   - **Impact**: No more NoneType errors, graceful handling of incomplete API data

3. **Field Naming Clarity**:
   - **Change**: Renamed "close" to "price" for clarity
   - **Reason**: Make it obvious to AI Agent that this is the option price
   - **Impact**: Improved readability and understanding

**Call Options Chain** (`get_call_options_chain`):
- **Purpose**: Fetch EXACTLY 10 strike prices ABOVE current price
- **Parameters**:
  - ticker (str): Stock ticker symbol
  - current_price (float): Current underlying stock price
  - expiration_date (str): YYYY-MM-DD format
- **API Parameters**: strike_price.gte, contract_type="call", order="asc", limit=10
- **Sort**: Ascending (lowest to highest strikes)
- **Limit Enforcement**: `list()[:10]` slice guarantees exactly 10 strikes

**Put Options Chain** (`get_put_options_chain`):
- **Purpose**: Fetch EXACTLY 10 strike prices BELOW current price
- **Parameters**:
  - ticker (str): Stock ticker symbol
  - current_price (float): Current underlying stock price
  - expiration_date (str): YYYY-MM-DD format
- **API Parameters**: strike_price.lte, contract_type="put", order="desc", limit=10
- **Sort**: Descending (highest to lowest strikes)
- **Limit Enforcement**: `list()[:10]` slice guarantees exactly 10 strikes

**Agent Instructions**: RULE #9 (lines 234-263)
- Workflow: Identify call/put → Get current_price if needed → Parse expiration_date → Call tool
- Date Handling: "this Friday" → Calculate date, "Oct 10" → Convert to YYYY-MM-DD
- Common Mistakes: Not fetching current_price first, incorrect date format, wrong tool selection

### TA Tool Enforcement (Updated Oct 8, 2025)

**CRITICAL AGENT INSTRUCTION RULES:**
- AI Agent **MUST FETCH** each requested TA indicator via dedicated tool calls
- AI Agent **CANNOT APPROXIMATE** or calculate TA values from OHLC data
- **Data Reuse Policy**: Only allowed if EXACT same indicator with EXACT same parameters was previously fetched
- **Examples of VIOLATIONS**:
  - ❌ "I pulled SMA-50 and SMA-200; SMA-20 value is approximated from latest 20-day window data"
  - ❌ Having 20 days of OHLC data and calculating SMA-20 manually
  - ❌ Using "approximated", "calculated", "derived", or "estimated" for TA indicators

**Enforcement Location**: `src/backend/services/agent_service.py` - RULE #7
**Validation**: Test 10 (SPY SMA) and Test 23 (NVDA SMA) verified all 3 tool calls made (no approximation)

### Migration History
- **Phase 4 Complete** (Oct 2025): ALL MCP tools migrated to Direct API
- **MCP Server**: Completely removed
- **Performance Gain**: 70% faster (removed MCP server overhead)
- **Architecture**: Direct Python API integration replaces MCP entirely
- **Phase 5 Complete** (Oct 2025): Removed get_stock_quote_multi wrapper, now using parallel get_stock_quote calls
- **Phase 6 Complete** (Oct 8, 2025): Removed get_options_quote_single, reduced tool count to 10
- **Phase 7 Complete** (Oct 8, 2025): Added get_call_options_chain and get_put_options_chain, increased tool count to 12
- **Phase 8 Complete** (Oct 9, 2025): Fixed critical options chain bugs (10-strike limit, None-safe rounding, field naming)

## Development Environment

### System Requirements
- **OS**: Linux (WSL2 on Windows supported)
- **Python**: 3.12.3 via uv
- **Node.js**: 18.0.0+ (currently v24.6.0)
- **npm**: 9.0.0+ (currently 11.6.0)

### Environment Variables (.env)
- `POLYGON_API_KEY` - Polygon.io API key
- `OPENAI_API_KEY` - OpenAI API key
- `FINNHUB_API_KEY` - Finnhub API key

### Configuration Files
- **Centralized Config**: `config/app.config.json` (non-sensitive settings)
- **Environment**: `.env` (API keys only)
- **Python**: `pyproject.toml`, `.pylintrc`
- **TypeScript**: `tsconfig.json`, `.eslintrc.cjs`, `.prettierrc.cjs`
- **Build**: `vite.config.ts`, `postcss.config.js`

## Testing Infrastructure (Updated Oct 9, 2025)

### CLI Regression Test Suite
- **Script**: `test_cli_regression.sh`
- **Total Tests**: 36 tests
- **Test Organization**: Ticker-based sequences
  - SPY Test Sequence: Tests 1-15 (15 tests - includes 2 options tests)
  - NVDA Test Sequence: Tests 16-30 (15 tests - includes 2 options tests)
  - Multi-Ticker Test Sequence: Tests 31-36 (6 tests - WDC, AMD, GME)
- **Log Output**: Project tmp/ folder (fixed Oct 9, 2025 - was using system /tmp)
- **Dynamic Dates**: Queries use relative dates (no hardcoded dates requiring updates)
- **Session Persistence**: All tests run in single CLI session
- **Calculation Engine**: awk-based (universal compatibility, no bc dependency)
- **Output Format**: 2 decimal precision, human-readable duration (MM min SS sec)

### Test Script Path Fix (Oct 9, 2025)
- **Bug**: Test script outputting logs to system /tmp instead of project tmp/
- **Violation**: Writing files outside project scope
- **Fix**: Changed `/tmp/` to `./tmp/` with `mkdir -p tmp`
- **Impact**: All test artifacts now properly contained within project directory

### Test Results (Oct 9, 2025 - Post Bug Fixes)
- **Total**: 36/36 PASSED (100%)
- **Avg Response Time**: 9.91s (EXCELLENT)
- **Duration**: 5 min 59 sec
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-09_11-05.log`
- **Performance Rating**: EXCELLENT (< 30s threshold)
- **Options Chain Verification**: Exactly 10 strikes per chain (SPY Call/Put, NVDA Call/Put)
- **Strike Count**: 40 total strikes (10 x 4 tests) - down from 174 before fix

### Test Execution Requirements
- **Mandatory**: Before all commits, after agent service changes, before PRs
- **Recommended**: After changing prompts, during optimization work
- **Validation**: 3-loop runs for comprehensive validation, 10-loop for baselines
- **Evidence**: Test reports must be included in commits

## Performance Metrics

### Current Performance (Oct 9, 2025 - Post Bug Fixes)
- **Average Response Time**: 9.91s (EXCELLENT rating)
- **Success Rate**: 100% (36/36 tests passed)
- **Performance Range**: 2.435s - 26.112s
- **Test Suite**: 36 tests (SPY 15 + NVDA 15 + Multi 6)
- **Session Duration**: 5 min 59 sec
- **Consistency**: High (all tests completed successfully)
- **Options Chain**: Exactly 10 strikes per chain (bug fixed)

### Optimization Features
- **Direct API**: No MCP server overhead
- **Parallel Tool Execution**: Multiple get_stock_quote calls executed concurrently
- **Token Tracking**: Real-time input/output token monitoring
- **Response Timing**: FastAPI middleware for precise measurement
- **Quick Response**: Minimal tool calls enforcement for speed
- **Service Tier**: "default" for better prototyping performance
- **TA Tool Enforcement**: Prevents unnecessary approximation, ensures data accuracy
- **10-Strike Limit**: Prevents message flooding, ensures concise responses

## Recent Updates (Oct 9, 2025)

### Options Chain Bug Fixes (Critical)
- **Files Modified**:
  - `src/backend/tools/polygon_tools.py`: Fixed 10-strike limit enforcement, None-safe rounding, field naming
  - `test_cli_regression.sh`: Fixed log output paths from /tmp to ./tmp
- **Bug #1**: 10-Strike Limit Not Enforced
  - **Evidence**: 174 total strikes found in logs (should be 40)
  - **Fix**: Changed for loop to `list()[:10]` slice
  - **Validation**: Now shows exactly 10 strikes per chain
- **Bug #2**: NoneType Round Error
  - **Error**: "type NoneType doesn't define __round__ method"
  - **Fix**: Added None checks: `round(value if value is not None else 0.0, 2)`
  - **Validation**: No more NoneType errors
- **Bug #3**: Test Script Path Violation
  - **Violation**: Logs written to system /tmp instead of project tmp/
  - **Fix**: Changed paths to ./tmp with mkdir -p tmp
  - **Validation**: Logs now in project folder
- **Enhancement**: Field Naming
  - **Change**: Renamed "close" to "price" for clarity
  - **Reason**: Make option price obvious to AI Agent
  - **Validation**: Tests show "price" field correctly
- **Test Results**: 36/36 PASSED, 9.91s avg (EXCELLENT rating)
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-09_11-05.log`

### Documentation Updates
- **Serena Memories**: Updated tech_stack.md with bug fix details and validation
- **Test Reports**: Generated comprehensive test report with evidence