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
- **Testing**: CLI regression test suite (test_cli_regression.sh - 38 tests, updated Oct 9, 2025)
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

### CLI Visual Enhancements (Oct 9, 2025)

#### Markdown Table Formatting
- **Purpose**: Display options chain data in readable table format
- **Location**: RULE #9 in `src/backend/services/agent_service.py` (lines 253-263)
- **Implementation**: Pure prompt engineering (no code logic changes)
- **Table Structure**:
  - Header row: Strike, Price, Delta, Gamma, Theta, Vega, IV, Volume, Open Interest
  - Strike prices in first column with $ formatting
  - IV formatted as percentage (XX.XX%)
  - Volume/Open Interest with comma thousands separators
- **Example**: "📊 SPY Call Options Chain (Expiring 2025-10-10)" followed by Markdown table
- **Rendering**: Rich library displays tables with borders and alignment
- **Performance Overhead**: <10ms per response (0.1% of avg response time)

#### Emoji Response Formatting
- **Purpose**: Enhance visual clarity and engagement
- **Location**: After RULE #9 in `agent_service.py` (lines 275-285)
- **Implementation**: Pure prompt engineering (no code logic changes)
- **Emoji Categories**:
  - Financial: 📊 (charts/data), 📈 (bullish), 📉 (bearish), 💹 (financial data)
  - Status: ✅ (positive), ⚠️ (caution), 🔴 (critical), 🟢 (good/healthy)
- **Usage Guidelines**: 2-5 emojis per response, prioritize clarity over decoration
- **Examples**:
  - "📊 SPY Call Options Chain (Expiring 2025-10-10)"
  - "📈 Bullish momentum confirmed with RSI 67.5"
  - "⚠️ Approaching overbought territory (RSI > 70)"
- **Performance Overhead**: Negligible (<1ms per response)

#### Intelligent Response Formatting (Lists vs Tables)
- **Purpose**: Optimize formatting based on data complexity
- **Location**: After emoji formatting in `agent_service.py` (lines 287-324)
- **Implementation**: Pure prompt engineering (decision logic)

**When to Use Lists** (prioritize speed):
- Simple responses with 1-5 data points
- Single ticker price quotes
- Binary questions (market status)
- Single TA indicator results
- Quick summaries

**When to Use Tables** (prioritize readability):
- Complex responses with 6+ data points
- Multiple ticker comparisons (2+ tickers)
- OHLC bars with multiple dates
- Multiple TA indicators (SMA 20/50/200)
- Options chain data
- Multi-dimensional data

**Decision Logic**:
1. Count data dimensions: Single value = list, Multiple dimensions = table
2. Count items: 1-5 items = list, 6+ items = table
3. Assess complexity: Simple = list, Complex = table
4. Multi-ticker queries: Always use tables

**Table Format Requirements**:
- Markdown syntax with | separators
- Header row with column names
- Numerical value alignment
- Reasonable column widths

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

**Agent Instructions**: RULE #9 (lines 234-273)
- Workflow: Identify call/put → Get current_price if needed → Parse expiration_date → Call tool
- Date Handling: "this Friday" → Calculate date, "Oct 10" → Convert to YYYY-MM-DD
- Markdown Table Formatting: Display options chain as table for better readability
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
- **Phase 9 Complete** (Oct 9, 2025): CLI Visual Enhancements (Markdown tables, emojis, intelligent formatting)

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

## Testing Infrastructure (Updated Oct 9, 2025 - Visual Enhancements)

### CLI Regression Test Suite
- **Script**: `test_cli_regression.sh`
- **Total Tests**: 38 tests (updated Oct 9, 2025 - added 2 Wall analysis tests)
- **Test Organization**: Ticker-based sequences
  - SPY Test Sequence: Tests 1-16 (16 tests - includes 2 options + 1 wall analysis)
  - NVDA Test Sequence: Tests 17-32 (16 tests - includes 2 options + 1 wall analysis)
  - Multi-Ticker Test Sequence: Tests 33-38 (6 tests - WDC, AMD, GME)
- **Log Output**: Project tmp/ folder (fixed Oct 9, 2025 - was using system /tmp)
- **Dynamic Dates**: Queries use relative dates (no hardcoded dates requiring updates)
- **Session Persistence**: All tests run in single CLI session
- **Calculation Engine**: awk-based (universal compatibility, no bc dependency)
- **Output Format**: 2 decimal precision, human-readable duration (MM min SS sec)

### New Test Cases (Oct 9, 2025)
- **Test 16**: SPY Options Chain Wall Analysis - "Analyze the Options Chain Data for SPY and provide potential Call & Put Wall(s) Strike Prices"
- **Test 32**: NVDA Options Chain Wall Analysis - "Analyze the Options Chain Data for NVDA and provide potential Call & Put Wall(s) Strike Prices"
- **Purpose**: Validate AI Agent can identify support/resistance levels from options chain data
- **Expected Output**: Call walls (resistance), Put walls (support), strike prices with OI/volume data, implications

### Test Script Path Fix (Oct 9, 2025)
- **Bug**: Test script outputting logs to system /tmp instead of project tmp/
- **Violation**: Writing files outside project scope
- **Fix**: Changed `/tmp/` to `./tmp/` with `mkdir -p tmp`
- **Impact**: All test artifacts now properly contained within project directory

### Test Results (Oct 9, 2025 - CLI Visual Enhancements)

**Single Loop Validation (Initial)**:
- **Total**: 38/38 PASSED (100%)
- **Avg Response Time**: 10.57s (EXCELLENT)
- **Duration**: 6 min 44 sec
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-09_12-15.log`

**10-Loop Baseline (Performance Baseline Established)**:
- **Total Tests**: 380/380 PASSED (100%)
- **Avg Response Time**: 12.07s (EXCELLENT rating)
- **Duration**: 77 min 7 sec (1 hour 17 minutes)
- **Performance Range**: 3-49s typical (95% of responses)
- **Anomaly Rate**: 0.26% (1 outlier in 380 tests)
- **Baseline Report**: `test-reports/performance_baseline_10loop_2025-10-09.md`
- **Loop Reports**: `test-reports/test_cli_regression_loop*_2025-10-09_*.log`

**Visual Features Validated**:
- ✅ Markdown tables render correctly with alignment (40 tables across 10 loops)
- ✅ Emojis appear in responses (320+ emojis, 2-5 per response)
- ✅ Wall analysis provides meaningful strike identification (20 analyses)
- ✅ Intelligent formatting (lists for simple, tables for complex)

### Test Execution Requirements
- **Mandatory**: Before all commits, after agent service changes, before PRs
- **Recommended**: After changing prompts, during optimization work
- **Validation**: 3-loop runs for comprehensive validation, 10-loop for baselines
- **Evidence**: Test reports must be included in commits

## Performance Metrics

### Current Performance Baseline (Oct 9, 2025 - 10-Loop Baseline)
- **Baseline Average Response Time**: 12.07s (EXCELLENT rating)
- **Success Rate**: 100% (380/380 tests passed across 10 loops)
- **Performance Range**: 2.44s - 82.02s (typical: 3-49s for 95% of responses)
- **Test Suite**: 38 tests per loop (SPY 16 + NVDA 16 + Multi 6)
- **Average Session Duration**: 7 min 42 sec per loop
- **Consistency**: High (standard deviation ~0.88s across loop averages)
- **Options Chain**: Exactly 10 strikes per chain (bug fixed)
- **Visual Enhancements Overhead**: <10ms per response (negligible)
- **Anomaly Rate**: 0.26% (1 outlier in 380 tests - API rate limiting)
- **Baseline Report**: `test-reports/performance_baseline_10loop_2025-10-09.md`

### Optimization Features
- **Direct API**: No MCP server overhead
- **Parallel Tool Execution**: Multiple get_stock_quote calls executed concurrently
- **Token Tracking**: Real-time input/output token monitoring
- **Response Timing**: FastAPI middleware for precise measurement
- **Quick Response**: Minimal tool calls enforcement for speed
- **Service Tier**: "default" for better prototyping performance
- **TA Tool Enforcement**: Prevents unnecessary approximation, ensures data accuracy
- **10-Strike Limit**: Prevents message flooding, ensures concise responses
- **Intelligent Formatting**: Lists for speed (simple), tables for clarity (complex)

## Recent Updates (Oct 9, 2025 - CLI Visual Enhancements)

### CLI Visual Enhancements Implementation
- **Files Modified**:
  - `src/backend/services/agent_service.py`: Added Markdown table formatting (RULE #9), emoji formatting, intelligent response formatting
  - `test_cli_regression.sh`: Added 2 new Wall analysis test cases, updated test count 36→38
- **Enhancement #1**: Markdown Table Formatting (lines 253-263)
  - **Purpose**: Display options chain data in beautiful tables
  - **Implementation**: Pure prompt engineering (no code changes)
  - **Features**: Header row, strike $ formatting, IV %, comma separators
  - **Performance**: <10ms overhead per response
- **Enhancement #2**: Emoji Response Formatting (lines 275-285)
  - **Purpose**: Visual clarity and engagement
  - **Emojis**: 📊📈📉💹✅⚠️🟢🔴
  - **Usage**: 2-5 per response, sparingly applied
  - **Performance**: <1ms overhead per response
- **Enhancement #3**: Intelligent Response Formatting (lines 287-324)
  - **Purpose**: Optimize format based on complexity
  - **Lists**: Simple responses (1-5 items, single ticker, binary questions)
  - **Tables**: Complex responses (6+ items, multi-ticker, OHLC bars)
  - **Decision Logic**: Data dimensions, item count, complexity assessment
- **Enhancement #4**: Options Chain Wall Analysis Tests
  - **Test 16**: SPY Wall analysis (identifies call/put walls with strike prices)
  - **Test 32**: NVDA Wall analysis (identifies call/put walls with strike prices)
  - **Validation**: AI Agent reuses existing options chain data (no redundant calls)
- **Test Results**: 38/38 PASSED, 10.57s avg (EXCELLENT rating)
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-09_12-15.log`
- **Visual Verification**:
  - ✅ Markdown tables render with proper alignment and borders
  - ✅ Emojis enhance readability without overwhelming
  - ✅ Wall analysis provides actionable strike price identification
  - ✅ Intelligent formatting adapts to response complexity

### Documentation Updates
- **Serena Memories**: Updated tech_stack.md with CLI Visual Enhancements details
- **Test Reports**: Generated comprehensive test report with visual enhancement validation

## Frontend Code Duplication Elimination (Oct 9, 2025)

### Problem Solved
Eliminated **157 lines of duplicate formatting code** in frontend that was replicating backend markdown formatting logic.

### Solution Implemented
**File**: `src/frontend/components/ChatMessage_OpenAI.tsx`

**Changes Made**:
1. ✅ Deleted `createMarkdownComponents()` function (154 lines)
   - Removed custom components for: p, h1, h2, h3, ul, ol, li, strong, em, blockquote, code
   - All had inline styling that duplicated backend formatting decisions

2. ✅ Deleted `markdownComponents` useMemo declaration (2 lines)
   - Removed reference to deleted function

3. ✅ Updated Markdown component to use default rendering
   - Changed: `<Markdown components={markdownComponents}>` → `<Markdown>`
   - Now uses react-markdown's default components

4. ✅ Removed unused `ComponentPropsWithoutRef` import (1 line)
   - Cleanup: Import was only used in deleted custom components

**Total Code Reduction**: 157 lines deleted

### Architecture Change

**Before (Duplicate Code ❌)**:
```
Backend → Generates Markdown → CLI (Rich library renders with styling)
Backend → Generates Markdown → GUI (157 lines of custom React components render with styling)
                                     ↑ DUPLICATE FORMATTING LOGIC
```

**After (No Duplication ✅)**:
```
Backend → Generates Markdown → CLI (Rich library renders)
Backend → Generates Markdown → GUI (Default react-markdown renders)
                                     ↑ ZERO CUSTOM FORMATTING CODE
```

### Benefits

**1. Zero Code Duplication**:
- Backend owns all formatting (markdown generation)
- CLI renders markdown with Rich library
- GUI renders markdown with default react-markdown
- No duplicate presentation logic

**2. Simplified Maintenance**:
- Changes only needed in backend (markdown generation)
- Frontend automatically inherits changes
- No need to update 2 places for formatting changes

**3. Better Performance**:
- Default react-markdown rendering is lightweight
- No custom component overhead
- Faster initial load and rendering

**4. Cleaner Codebase**:
- Frontend: -157 lines of custom formatting code
- Simpler component structure
- Easier to understand and maintain

### Implementation Details

**Tools Used**:
- Sequential-Thinking: 11 thoughts total (4 planning, 4 implementation analysis, 3 verification)
- Standard Edit: TypeScript file modifications (correct tool for React/TypeScript)
- Standard Write: Memory file updates

**Test Results**:
- CLI Regression: 38/38 PASSED (100% success rate)
- Average Response Time: 11.14s (EXCELLENT - within 12.07s baseline)
- Frontend: User validated and approved GUI appearance
- No regression in backend or frontend functionality

**Markdown Format**:
- Backend: AI agent generates well-formatted markdown
- CLI: Rich library renders markdown in terminal (unchanged)
- GUI: react-markdown renders markdown in browser (simplified)
- Universal format: Same markdown content for both interfaces

### Impact Summary

**Frontend**:
- ✅ 157 lines deleted
- ✅ Simplified to pure presentation layer
- ✅ No custom formatting logic
- ✅ Markdown rendering with defaults

**Backend**:
- ✅ No changes required
- ✅ Already generates markdown correctly
- ✅ Single source of truth maintained

**CLI**:
- ✅ No changes required
- ✅ Rich rendering unchanged
- ✅ 100% test pass rate

**Maintenance**:
- ✅ Changes only in backend
- ✅ Frontend auto-inherits
- ✅ No duplicate code paths

**Test Report**: `test-reports/test_cli_regression_loop1_2025-10-09_16-57.log`