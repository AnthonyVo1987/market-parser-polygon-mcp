# Tech Stack

## Core Technologies

### Backend Framework

- **FastAPI** (v0.115.5): Modern async web framework
- **Python** (3.12.3): Programming language
- **Uvicorn**: ASGI server for FastAPI

### AI/ML Integration

- **OpenAI Agents SDK** (v0.2.9): Agent framework for GPT-5
- **GPT-5-Nano**: AI model for financial analysis (ONLY model allowed - NO GPT-5-Mini, NO model selection)
- **Reasoning effort**: Low (optimized for speed)

### Financial Data APIs

**Finnhub (1 tool):**

- Single ticker quotes via `get_stock_quote`

**Polygon.io Direct API (11 tools):**

1. `get_market_status_and_date_time` - Market status and datetime
2. `get_stock_quote_multi` - Multi-ticker quotes
3. `get_options_quote_single` - Options contracts with Greeks
4. `get_OHLC_bars_custom_date_range` - Custom date range OHLC bars
5. `get_OHLC_bars_specific_date` - Specific date OHLC bars
6. `get_OHLC_bars_previous_close` - Previous trading day OHLC
7. `get_ta_sma` - Simple Moving Average
8. `get_ta_ema` - Exponential Moving Average
9. `get_ta_rsi` - Relative Strength Index
10. `get_ta_macd` - MACD Indicator
11. (Additional tool if needed)

**Total**: 12 tools (1 Finnhub + 11 Polygon Direct API)

### Database

- **SQLite**: Session storage via OpenAI Agents SDK
- **Session management**: Conversation memory persistence

### Frontend

- **React** (18.2.0): UI framework
- **TypeScript** (5.5.3): Type-safe JavaScript
- **Vite** (5.2.13): Build tool and dev server
- **TailwindCSS** (3.4.4): Utility-first CSS

### Code Quality

- **Pylint** (3.3.3): Python linting (10.00/10 score maintained)
- **ESLint** (9.17.0): JavaScript/TypeScript linting
- **Black** (24.10.0): Python code formatting
- **isort** (5.13.2): Python import sorting
- **Prettier** (3.4.2): JS/TS code formatting
- **markdownlint-cli2**: Markdown linting

### Testing

- **CLI_test_regression.sh**: Single source of truth for CLI testing with loop automation
  - **Loop Support**: Automated loop testing (1-10 iterations, default: 1)
    - Usage: `./CLI_test_regression.sh [LOOP_COUNT]`
    - Examples: `./CLI_test_regression.sh` (1 loop), `./CLI_test_regression.sh 3` (3 loops)
  - **27 tests per loop** (16 original + 11 SPY TA indicator tests)
    - Market data queries (7 tests)
    - TA indicators (4 original tests)
    - OHLC/options queries (5 tests)
    - SPY TA variants (11 tests): MACD, SMA/EMA (5/10/20/50/200)
  - **Persistent session**: All 27 tests in single CLI session per loop
  - **Aggregate statistics**: Min/max/avg response times across all loops
  - **Individual reports**: Separate test report generated per loop iteration
  - **100% pass rate required** before commit
- **Performance metrics**: Response time tracking (target: <30s average)
- **Health checks**: Backend `/health` endpoint validation
- **Legacy scripts removed**: test_7_prompts_persistent_session.sh, CLI_test_regression.sh

### Development Tools

- **uv** (0.8.19): Python package manager
- **npm** (11.6.0): Node.js package manager
- **Node.js** (v24.6.0): JavaScript runtime

## Architecture Patterns

### Token Usage Tracking

**Backend (Python):**

- **Function**: `extract_token_usage_from_context_wrapper()` in `src/backend/utils/token_utils.py`
- **Returns**: Dictionary with `total_tokens`, `input_tokens`, `output_tokens`
- **Compatibility**: Supports both OpenAI naming conventions (input/output and prompt/completion)
- **Legacy function**: `extract_token_count_from_context_wrapper()` (deprecated, kept for compatibility)

**API Response:**

- **ResponseMetadata fields**:
  - `tokenCount`: Total tokens (deprecated, use inputTokens + outputTokens)
  - `inputTokens`: Prompt/input tokens
  - `outputTokens`: Completion/output tokens
- **Format**: All fields use camelCase aliases for frontend compatibility

**Frontend (TypeScript):**

- **Interfaces**: `MessageMetadata` and `ResponseMetadata` in `src/frontend/types/chat_OpenAI.ts`
- **Display**: Shows "Input: X | Output: Y | Total: Z" format
- **Backward compatibility**: Falls back to `tokenCount` if input/output not available

### Tool Architecture

- **Direct API pattern**: All tools use direct Polygon Python Library calls
- **@function_tool decorator**: Consistent tool definition pattern
- **Comprehensive docstrings**: Detailed tool documentation
- **Structured JSON responses**: Consistent response format

### Agent Configuration

- **Model**: GPT-5-Nano only (NO GPT-5-Mini, NO model selection)
- **Reasoning**: Low effort (optimized for speed)
- **Verbosity**: Low (concise responses)
- **Max tokens**: 128,000
- **Service tier**: Flex
- **Usage tracking**: Enabled via `include_usage=True`

### Session Management

- **Persistent sessions**: CLI and web sessions stored separately
- **SQLite backend**: Local session storage
- **Automatic cleanup**: Session cleanup on exit

## Performance Metrics

### Latest Test Results (Oct 5, 2025)

**27-Test Suite (Model Selector Removal + Token/Performance Fixes):**

- **Total Tests**: 27/27 PASSED ✅
- **Success Rate**: 100%
- **Average Response Time**: 7.34s ⭐ EXCELLENT
- **Response Time Range**: 4.11s - 17.14s
- **Session Mode**: PERSISTENT (all tests in single session)
- **Test Report**: `test-reports/cli_regression_test_loop1_20251005_181607.txt`

**Changes Validated:**

1. ✅ AI Model Selector completely removed (backend + frontend)
2. ✅ Token display showing Input/Output/Total separately
3. ✅ Performance indicators (FCP, LCP, CLS) displaying correctly

### Post-MCP Removal Baseline (Oct 5, 2025)

**10-Run Statistical Analysis (160 total tests):**

- **Min Average**: 5.25s
- **Max Average**: 7.57s
- **Overall Average**: 6.10s ⭐ EXCELLENT
- **Median**: 5.92s
- **Std Deviation**: 0.80s (highly consistent)
- **Success Rate**: 100% (160/160 tests PASSED)

**Performance Improvement:**

- **Legacy (with MCP)**: ~20s average
- **Current (Direct API)**: 6.10s average
- **🚀 Improvement**: 70% faster (removed MCP overhead)

**Performance Ratings:**

- **Exceptional**: <6s average
- **Excellent**: 6-10s average ✅ CURRENT
- **Good**: 10-30s average
- **Acceptable**: 30-90s average

**Test Environment:**

- 16-test persistent session suite
- Direct Polygon Python API (no MCP)
- CLI-only testing (no GUI interference)
- GPT-5-Nano model with low reasoning effort

### Build Performance

- **Production build**: ~3-6s
- **Dev server startup**: <2s
- **Hot reload**: <500ms

### UI Performance Monitoring

**Performance Metrics Tracking:**

- **FCP** (First Contentful Paint): Web Vitals metric
- **LCP** (Largest Contentful Paint): Web Vitals metric
- **CLS** (Cumulative Layout Shift): Web Vitals metric
- **Implementation**: `usePerformanceMonitoring()` hook in `src/frontend/utils/performance.tsx`
- **Fix (Oct 5, 2025)**: Metrics initialize as `undefined` instead of `0` for proper "Calculating..." display

## Configuration Management

### Environment Variables (.env)

- `POLYGON_API_KEY`: Polygon.io API key
- `OPENAI_API_KEY`: OpenAI API key
- `DEFAULT_MODEL`: gpt-5-nano (ONLY allowed value)

### Config Files

- `app.config.json`: Non-sensitive application settings
- `pyproject.toml`: Python project configuration
- `package.json`: Node.js dependencies and scripts
- `.eslintrc.cjs`: ESLint configuration
- `.prettierrc`: Prettier configuration

## Deployment

### Ports

- **Backend**: 8000 (FastAPI/Uvicorn)
- **Frontend Dev**: 3000 (Vite)
- **Frontend Prod**: 5500 (served via npm)

### Startup Scripts

- `start-app.sh`: Main startup script (30s timeout, works in WSL2 and X11)
- `start-app-xterm.sh`: XTerm variant (X11 environments)

### Health Checks

- **Backend**: `GET /health` → `{"status": "healthy", "timestamp": "..."}`
- **Frontend**: Served content verification
- **Retry logic**: 10 attempts with 2s intervals

## Migration History

### Infrastructure Cleanup (Oct 5, 2025)

**AI Model Selector Removal:**

- **Backend**: Removed `src/backend/routers/models.py` (entire file)
- **Backend**: Removed model selection classes from `src/backend/api_models.py`:
  - `CustomModel`, `AIModelId`, `AIModel`, `ModelListResponse`, `ModelSelectionRequest`, `ModelSelectionResponse`
- **Backend**: Kept `ResponseMetadata` (used by chat endpoint)
- **Backend**: Removed `/api/v1/models` router registration from `src/backend/main.py`
- **Frontend**: Removed `src/frontend/types/ai_models.ts` (entire file)
- **Frontend**: Removed model selection imports and commented code from `ChatInterface_OpenAI.tsx`
- **Rationale**: Only GPT-5-Nano is allowed, no model selection needed

**Token Display Enhancement:**

- **Backend**: Added `extract_token_usage_from_context_wrapper()` function
- **Backend**: Updated `ResponseMetadata` with `inputTokens` and `outputTokens` fields
- **Frontend**: Updated `MessageMetadata` and `ResponseMetadata` interfaces with new fields
- **Frontend**: Updated `ChatMessage_OpenAI.tsx` to display "Input: X | Output: Y | Total: Z" format
- **Backward compatibility**: Kept `tokenCount` field as deprecated fallback

**Performance Indicators Fix:**

- **Issue**: FCP, LCP, CLS stuck on "Calculating..." because metrics initialized to `0`
- **Fix**: Changed initialization from `0` to `undefined` in `usePerformanceMonitoring()` hook
- **Result**: UI properly distinguishes between "not measured yet" (undefined) and actual values

### Tool Evolution

1. **Phase 1**: Initial 10 tools (7 Polygon MCP + 1 Finnhub + 2 Polygon Direct)
2. **Phase 2**: Added TA indicators (10 → 14 tools)
3. **Phase 3**: Migration to direct API (14 → 18 tools, 6 MCP + 12 Direct)
4. **Phase 4**: MCP removal (18 → 12 tools, all Direct API) ⭐ CURRENT

### Breaking Changes

- **Oct 5, 2025**: Removed Polygon MCP server and all MCP tools
- All queries now use direct Polygon Python API
- Agent creation simplified: no MCP server parameter
- Performance improved: no MCP overhead

## Development Workflow

### Code Quality Checklist

1. **Linting**: `npm run lint` (Python 10/10, JS/TS 0 errors)
2. **Type checking**: `npm run type-check`
3. **Formatting**: `npm run format:check` or `npm run lint:fix`
4. **Build**: `npm run build`
5. **Testing**: `./CLI_test_regression.sh [LOOP_COUNT]` (27/27 PASS required per loop)

### Git Workflow

- **Atomic commits**: All changes in single commit
- **Descriptive messages**: Clear commit message with context
- **Co-authoring**: Claude credited in commits
- **Breaking changes**: Clearly marked in commit message

## Key Principles

1. **GPT-5-Nano Only**: NO GPT-5-Mini allowed, NO model selection
2. **Direct API**: All tools use Polygon Python Library directly (no MCP)
3. **Code Quality**: 10.00/10 Pylint score mandatory
4. **Testing Required**: 100% test pass rate before commit
5. **Performance**: <30s average response time target
6. **Token Transparency**: Display input/output/total tokens separately
7. **UI Performance**: Monitor FCP, LCP, CLS metrics for optimal UX
