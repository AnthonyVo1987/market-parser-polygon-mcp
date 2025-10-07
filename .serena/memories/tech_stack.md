# Technology Stack

## Core Technologies

### Backend
- **Framework**: FastAPI (latest)
- **Python Version**: 3.12.3
- **Package Manager**: uv 0.8.19
- **AI Integration**: OpenAI Agents SDK v0.2.9
- **AI Model**: GPT-5-Nano (EXCLUSIVE - no model selection)
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
- **Polygon.io**: Direct Python API integration (11 tools)
- **Finnhub**: Custom Python API integration (1 tool)
- **Total AI Agent Tools**: 12 (no MCP overhead)

### Development Tools
- **Python Linting**: pylint, black, isort, mypy
- **JS/TS Linting**: ESLint, Prettier, TypeScript compiler
- **Testing**: Playwright E2E, CLI regression tests
- **Performance**: Lighthouse CI, React Scan
- **Version Control**: Git

## AI Agent Architecture

### OpenAI Agents SDK v0.2.9
- **Primary Model**: GPT-5-Nano (200K TPM rate limit)
- **Integration Pattern**: Direct API tools (no MCP)
- **Performance**: 70% faster than legacy MCP architecture
- **Token Tracking**: Dual naming convention support (input_tokens/prompt_tokens)

### Direct API Tools (12 Total)

**Finnhub Custom API (1 tool):**
- `get_stock_quote` - Real-time stock quotes from Finnhub

**Polygon Direct API (11 tools):**
- `get_market_status_and_date_time` - Market status and current datetime
- `get_stock_quote_multi` - Multiple stock quotes (snapshot)
- `get_options_quote_single` - Single option quote
- `get_OHLC_bars_custom_date_range` - OHLC bars for custom date range
- `get_OHLC_bars_specific_date` - OHLC bars for specific date
- `get_OHLC_bars_previous_close` - Previous close OHLC bars
- `get_ta_sma` - Simple Moving Average (SMA)
- `get_ta_ema` - Exponential Moving Average (EMA)
- `get_ta_rsi` - Relative Strength Index (RSI)
- `get_ta_macd` - Moving Average Convergence Divergence (MACD)

### Migration History
- **Phase 4 Complete** (Oct 2025): ALL MCP tools migrated to Direct API
- **MCP Server**: Completely removed
- **Performance Gain**: 70% faster (removed MCP server overhead)
- **Architecture**: Direct Python API integration replaces MCP entirely

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

### Current Performance (Post-MCP Removal)
- **Average Response Time**: 6.10s (EXCELLENT rating)
- **Success Rate**: 100% (160/160 tests in 10-run baseline)
- **Performance Range**: 5.25s - 7.57s
- **Consistency**: 0.80s standard deviation
- **Improvement**: 70% faster than legacy MCP architecture

### Optimization Features
- **Direct API**: No MCP server overhead
- **Token Tracking**: Real-time input/output token monitoring
- **Response Timing**: FastAPI middleware for precise measurement
- **Quick Response**: Minimal tool calls enforcement for speed

## Legacy Feature Cleanup (Oct 2025)

**Context:** Removed 4 deprecated legacy features from entire codebase for improved performance and maintainability.

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

### Test Results (Post-Cleanup)

**CLI Regression Test Results:**
- **Total Tests**: 27/27 PASSED ✅
- **Success Rate**: 100%
- **Average Response Time**: 7.95s (EXCELLENT)
- **Response Range**: 3.004s - 24.614s
- **Test Report**: `cli_regression_test_loop1_20251006_211035.txt`

**Files Changed:**
- **Deleted**: 2 files (system.py, api-integration-guide.md)
- **Modified**: 10 files (api_models, main, routers/__init__, performance.tsx, response_utils, CLAUDE.md, AGENTS.md, README.md)
- **Total Impact**: Clean codebase, improved performance, accurate documentation

### Performance Benefits
- **CPU Usage**: 1-2% reduction from CSS analysis removal
- **Code Quality**: Simpler, more maintainable codebase
- **Documentation**: Accurate and up-to-date
- **API Surface**: Cleaner with unused endpoint removed
