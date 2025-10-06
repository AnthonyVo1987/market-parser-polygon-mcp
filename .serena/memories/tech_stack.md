# Tech Stack

## Core Technologies

### Backend Framework
- **FastAPI** (v0.115.5): Modern async web framework
- **Python** (3.12.3): Programming language
- **Uvicorn**: ASGI server for FastAPI

### AI/ML Integration
- **OpenAI Agents SDK** (v0.2.9): Agent framework for GPT-5
- **GPT-5-Nano**: AI model for financial analysis (ONLY model allowed - NO GPT-5-Mini)
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
- **CLI_test_regression.sh**: Single source of truth for CLI testing (27 tests)
  - 16 original tests (market data, TA indicators, OHLC/options)
  - 11 new SPY TA indicator tests (MACD, SMA/EMA variants: 5/10/20/50/200)
  - Persistent session testing in single CLI session
  - 100% pass rate required before commit
- **Performance metrics**: Response time tracking (target: <30s average)
- **Health checks**: Backend `/health` endpoint validation
- **Legacy scripts removed**: test_7_prompts_persistent_session.sh, test_16_prompts_persistent_session.sh

### Development Tools
- **uv** (0.8.19): Python package manager
- **npm** (11.6.0): Node.js package manager
- **Node.js** (v24.6.0): JavaScript runtime

## Architecture Patterns

### Tool Architecture
- **Direct API pattern**: All tools use direct Polygon Python Library calls
- **@function_tool decorator**: Consistent tool definition pattern
- **Comprehensive docstrings**: Detailed tool documentation
- **Structured JSON responses**: Consistent response format

### Agent Configuration
- **Model**: GPT-5-Nano only (NO GPT-5-Mini)
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
5. **Testing**: `./CLI_test_regression.sh` (27/27 PASS required)

### Git Workflow
- **Atomic commits**: All changes in single commit
- **Descriptive messages**: Clear commit message with context
- **Co-authoring**: Claude credited in commits
- **Breaking changes**: Clearly marked in commit message

## Key Principles

1. **GPT-5-Nano Only**: NO GPT-5-Mini allowed
2. **Direct API**: All tools use Polygon Python Library directly (no MCP)
3. **Code Quality**: 10.00/10 Pylint score mandatory
4. **Testing Required**: 100% test pass rate before commit
5. **Performance**: <30s average response time target
