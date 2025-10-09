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
- **Polygon.io**: Direct Python API integration (9 tools, updated Oct 8, 2025)
- **Finnhub**: Custom Python API integration (1 tool)
- **Total AI Agent Tools**: 10 (reduced from 11, updated Oct 8, 2025)

### Development Tools
- **Python Linting**: pylint, black, isort, mypy
- **JS/TS Linting**: ESLint, Prettier, TypeScript compiler
- **Testing**: CLI regression test suite (test_cli_regression.sh - 32 tests, 100% pass rate)
- **Performance**: Lighthouse CI, React Scan
- **Version Control**: Git

## AI Agent Architecture

### OpenAI Agents SDK v0.2.9
- **Primary Model**: GPT-5-Nano (200K TPM rate limit)
- **Service Tier**: "default" (changed from "flex" Oct 8, 2025 - see below)
- **Integration Pattern**: Direct API tools (no MCP)
- **Performance**: 70% faster than legacy MCP architecture
- **Token Tracking**: Dual naming convention support (input_tokens/prompt_tokens)
- **Parallel Execution**: Native parallel tool execution for multiple ticker queries

#### Service Tier Configuration (Updated Oct 8, 2025)
- **Current Setting**: `service_tier: "default"` (in agent_service.py:367)
- **Previous Setting**: `service_tier: "flex"`
- **Change Reason**: Prototyping phase requires better performance; "flex" tier was causing compute resources rate limiting
- **Impact**: Improved response consistency and throughput for development testing
- **Configuration Location**: `src/backend/services/agent_service.py:367`
- **Validation**: 36/36 tests PASSED with 10.44s avg (EXCELLENT rating)

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

### Direct API Tools (10 Total - Updated Oct 8, 2025)

**Finnhub Custom API (1 tool):**
- `get_stock_quote` - Real-time stock quotes from Finnhub (supports parallel calls for multiple tickers)

**Polygon Direct API (9 tools - Updated Oct 8, 2025):**
- `get_market_status_and_date_time` - Market status and current datetime
- `get_OHLC_bars_custom_date_range` - OHLC bars for custom date range
- `get_OHLC_bars_specific_date` - OHLC bars for specific date
- `get_OHLC_bars_previous_close` - Previous close OHLC bars
- `get_ta_sma` - Simple Moving Average (SMA)
- `get_ta_ema` - Exponential Moving Average (EMA)
- `get_ta_rsi` - Relative Strength Index (RSI)
- `get_ta_macd` - Moving Average Convergence Divergence (MACD)

**REMOVED Oct 8, 2025:**
- `get_options_quote_single` - Single option quote (removed - inefficient, will be replaced with full options chain tool in future)

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

## Dependencies

### Backend Python (pyproject.toml)
```toml
dependencies = [
  "openai-agents==0.2.9",
  "pydantic",
  "rich",
  "python-dotenv",
  "openai>=1.99.0,<1.100.0",
  "fastapi",
  "uvicorn[standard]",
  "aiofiles>=24.1.0",
  "python-lsp-server[all]>=1.13.1",
  "openai-agents-mcp>=0.0.8",
  "finnhub-python>=2.4.25",
]

[dependency-groups]
dev = [
  "pylint>=3.0.0",
  "black>=23.12.0",
  "isort>=5.13.0",
  "mypy>=1.7.0",
  "pytest>=7.4.0",
]
```

### Frontend JavaScript (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-markdown": "^9.0.0",
    "react-scan": "^0.4.3",
    "use-debounce": "^10.0.6"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.2.0",
    "eslint": "^8.57.0",
    "prettier": "^3.0.0",
    "@lhci/cli": "^0.15.0"
  }
}
```

## Build & Deployment

### Ports
- **Backend**: 8000 (FastAPI server)
- **Frontend Dev**: 3000 (Vite dev server)
- **Frontend Prod**: 5500 (Live Server for production build)

### Build Process
- **Frontend**: `npm run build` - TypeScript compilation + Vite build
- **Backend**: No build required (Python interpreted)
- **Performance**: Lighthouse CI for performance testing

## Performance Metrics

### Current Performance (Oct 8, 2025 - Post-TA-Enforcement & Options-Removal)
- **Average Response Time**: 7.88s (EXCELLENT rating)
- **Success Rate**: 100% (32/32 tests passed)
- **Performance Range**: 3.861s - 15.317s
- **Test Suite**: 32 tests (SPY 13 + NVDA 13 + Multi 6)
- **Session Duration**: 4 min 15 sec
- **Consistency**: High (all tests completed successfully)

### Previous Performance (Post-Service-Tier-Change Oct 8, 2025)
- **Average Response Time**: 10.44s (EXCELLENT rating)
- **Success Rate**: 100% (36/36 tests passed)
- **Performance Range**: 2.188s - 31.599s
- **Test Suite**: 36 tests organized by ticker (SPY 15 + NVDA 15 + Multi 6)

### Optimization Features
- **Direct API**: No MCP server overhead
- **Parallel Tool Execution**: Multiple get_stock_quote calls executed concurrently
- **Token Tracking**: Real-time input/output token monitoring
- **Response Timing**: FastAPI middleware for precise measurement
- **Quick Response**: Minimal tool calls enforcement for speed
- **Service Tier**: "default" for better prototyping performance
- **TA Tool Enforcement**: Prevents unnecessary approximation, ensures data accuracy

## Testing Infrastructure (Updated Oct 8, 2025)

### CLI Regression Test Suite
- **Script**: `test_cli_regression.sh`
- **Total Tests**: 32 tests (reduced from 36 - removed 4 options tests)
- **Test Organization**: Ticker-based sequences
  - SPY Test Sequence: Tests 1-13 (13 tests)
  - NVDA Test Sequence: Tests 14-26 (13 tests)
  - Multi-Ticker Test Sequence: Tests 27-32 (6 tests - WDC, AMD, GME)
- **Dynamic Dates**: Queries use relative dates (no hardcoded dates requiring updates)
  - Example: "Stock Price on the previous week's Friday: $SPY"
  - Example: "Daily Stock Price bars Analysis from the last 2 trading weeks: $SPY"
- **Session Persistence**: All tests run in single CLI session
- **Calculation Engine**: awk-based (universal compatibility, no bc dependency)
- **Output Format**: 2 decimal precision, human-readable duration (MM min SS sec)

### Test Results (Oct 8, 2025 - TA Enforcement & Options Removal)
- **Total**: 32/32 PASSED (100%)
- **Avg Response Time**: 7.88s (EXCELLENT)
- **Duration**: 4 min 15 sec
- **Test Report**: `test-reports/test_cli_regression_loop1_2025-10-08_17-52.log`
- **Performance Rating**: EXCELLENT (< 30s threshold)
- **TA Verification**: All SMA/EMA tests verified - agent fetches ALL indicators (no approximation)

### Test Execution Requirements
- **Mandatory**: Before all commits, after agent service changes, before PRs
- **Recommended**: After changing prompts, during optimization work
- **Validation**: 3-loop runs for comprehensive validation, 10-loop for baselines
- **Evidence**: Test reports must be included in commits

## Legacy Feature Cleanup (Oct 2025)

**Context:** Removed 5 deprecated legacy features from entire codebase for improved performance and maintainability.

### Features Removed

**1. CSS Performance Analysis:**
- **Impact**: HIGH overhead (1-2% CPU continuous)
- **Location**: `src/frontend/utils/performance.tsx` (analyzeCSSPerformance function)
- **Reason**: Minimal value - scanned DOM 6× every 2s with querySelectorAll('*')
- **Benefit**: 1-2% CPU reduction, cleaner codebase

**2. /api/v1/system/status Endpoint:**
- **Impact**: Zero usage (unused endpoint)
- **Files Removed**: `src/backend/routers/system.py` (entire file)
- **Files Modified**: api_models.py (SystemMetrics, SystemStatusResponse classes), main.py, routers/__init__.py
- **Reason**: No frontend, tests, or docs referenced it
- **Benefit**: Simplified API surface, removed dead code

**3. Prompt Template System Remnants:**
- **Impact**: Already deprecated (system was previously removed)
- **Remnants Removed**:
  - api_models.py docstring reference to "PromptTemplateManager"
  - SystemMetrics.prompt_templates_loaded field (always 0)
  - docs/api/api-integration-guide.md (957 lines of outdated docs)
  - Project structure references in CLAUDE.md, AGENTS.md, README.md
- **Reason**: System was replaced by Direct Prompts, only documentation remained
- **Benefit**: Documentation now accurate, no misleading references

**4. Emoji in CLI Responses:**
- **Impact**: Cosmetic feature (CLI only)
- **Location**: `src/backend/utils/response_utils.py` (print_response function)
- **Emojis Removed**: ✅ (success), 📊 (metrics), ⏱️ (time), 🔢 (tokens), 🤖 (model)
- **Reason**: Purely visual, no functional value
- **Benefit**: Cleaner CLI output, simpler code

**5. get_stock_quote_multi Tool (Oct 2025):**
- **Impact**: Wrapper function removal
- **Location**: `src/backend/tools/polygon_tools.py` (139 lines removed)
- **Replacement**: Multiple parallel get_stock_quote() calls via OpenAI Agents SDK
- **Reason**: Unnecessary wrapper - SDK handles parallel execution natively
- **Benefit**: Simplified codebase, reduced tool count from 12 to 11, leverages native parallel execution

**6. get_options_quote_single Tool (Oct 8, 2025):**
- **Impact**: Complete tool removal (176 lines from polygon_tools.py)
- **Location**: `src/backend/tools/polygon_tools.py` (function deleted)
- **Agent Service**: Removed from imports, tools list, and instructions
- **Test Suite**: Removed 4 options test cases (2 SPY, 2 NVDA)
- **Reason**: Inefficient single-quote tool, will be replaced with full options chain fetcher in future
- **Benefit**: Tool count reduced from 11 to 10, test count from 36 to 32, cleaner codebase

### Performance Benefits
- **CPU Usage**: 1-2% reduction from CSS analysis removal
- **Code Quality**: Simpler, more maintainable codebase
- **Documentation**: Accurate and up-to-date
- **API Surface**: Cleaner with unused endpoint removed
- **Tool Count**: Reduced from 12 to 10 tools
- **Test Suite**: Reduced from 36 to 32 tests (removed deprecated options tests)
- **Architecture**: Leverages OpenAI Agents SDK native parallel execution

## Recent Updates (Oct 8, 2025)

### TA Tool Enforcement & Options Tool Removal
- **File**: `src/backend/services/agent_service.py`
- **Change 1**: Added comprehensive TA enforcement rules (RULE #7)
  - Agent MUST fetch all requested TA indicators via tool calls
  - Agent CANNOT approximate TA values from OHLC data
  - Explicit examples of violations and correct behavior
- **Change 2**: Removed get_options_quote_single tool
  - Deleted from imports and tools list
  - Removed RULE #3 about options
  - Updated tool count from 11 to 10
  - Renumbered subsequent rules
- **File**: `src/backend/tools/polygon_tools.py`
  - Completely removed get_options_quote_single function (176 lines)
  - Removed docstring references to options tool (3 locations)
- **File**: `test_cli_regression.sh`
  - Removed 4 options test cases (2 SPY, 2 NVDA)
  - Updated test count from 36 to 32
  - Updated all test numbering and comments
- **Validation**: 32/32 tests PASSED, 7.88s avg, EXCELLENT rating
- **TA Verification**: Tests 10 and 23 confirmed all SMA indicators fetched (no approximation)

### Service Tier Optimization
- **File**: `src/backend/services/agent_service.py:367`
- **Change**: `service_tier: "flex"` → `service_tier: "default"`
- **Reason**: Prototyping phase requires better performance; "flex" tier was causing compute resources rate limiting
- **Impact**: Improved response consistency and throughput
- **Validation**: 36/36 tests PASSED with 10.44s avg (EXCELLENT rating)

### Test Suite Restructuring
- **Previous**: 27 tests (mixed organization)
- **Updated**: 36 tests organized by ticker (SPY 15 + NVDA 15 + Multi 6)
- **Current**: 32 tests (SPY 13 + NVDA 13 + Multi 6)
- **Dynamic Dates**: Queries use relative dates instead of hardcoded dates
- **Sustainability**: No date updates required over time
- **Ticker Changes**: GME replaced INTC in multi-ticker sequence
- **Test Results**: 32/32 PASSED, 7.88s avg, EXCELLENT rating

### Documentation Updates
- **CLAUDE.md**: Updated Last Completed Task Summary with TA enforcement and options removal
- **README.md**: Updated all test count references from 36 to 32
- **Serena Memories**: Updated tech_stack.md with tool count and TA enforcement details
- **Test Reports**: `test-reports/test_cli_regression_loop1_2025-10-08_17-52.log`
