# Project Onboarding - Latest October 2025

## Project Purpose

**Market Parser** is a Python CLI and Gradio web application for natural language financial analysis.

- **Primary Use**: Ask questions about stocks, options, technical analysis, and market data
- **Data Sources**: Polygon.io API (market data), Tradier API (options data), OpenAI GPT-5-nano (natural language processing)
- **AI Engine**: OpenAI Agents SDK v0.2.9 with custom Polygon/Tradier tools
- **Deployment**: AWS AppRunner (port 8000), also runs locally

## Latest Architecture (October 18, 2025)

### Entry Points (LATEST - Just Refactored)

**Standard Python Entry Point (NEW):**
```bash
uv run main.py  # Standard Python convention, recommended
```
- File: `src/main.py` (created October 18, 2025)
- Calls: `backend.cli.main()`
- Status: ✅ WORKING

**Console Scripts (NEW):**
```bash
uv run market-parser            # CLI interface
uv run market-parser-gradio     # Gradio web UI
```
- Defined in: `pyproject.toml` [project.scripts]
- Status: ✅ BOTH WORKING
- Note: May require `uv sync` for console script discovery

**Legacy Entry Points (Still Supported):**
```bash
uv run src/backend/cli.py                    # Direct CLI
uv run python -m backend.cli                 # Module execution
uv run python src/backend/gradio_app.py      # Direct Gradio
```

### Project Structure (Latest)

```
market-parser-polygon-mcp/
├── src/
│   ├── main.py                          # ⭐ NEW: Standard Python entry point
│   └── backend/
│       ├── __init__.py                  # ⭐ NEW: Backend package init
│       ├── cli.py                       # CLI interface + business logic
│       ├── gradio_app.py                # Gradio web UI (PWA + Hot Reload)
│       ├── config.py                    # Configuration
│       ├── tools/                       # AI agent tools
│       │   ├── polygon_tools.py         # Polygon.io API tools
│       │   ├── tradier_tools.py         # Tradier API tools
│       │   ├── formatting_helpers.py    # Formatting utilities
│       │   ├── error_utils.py           # Error response standardization
│       │   ├── validation_utils.py      # Input validation
│       │   └── api_utils.py             # API utilities
│       ├── services/
│       │   └── agent_service.py         # Agent initialization
│       └── utils/
│           ├── response_utils.py        # Response formatting
│           ├── datetime_utils.py        # Datetime utilities
│           └── token_utils.py           # Token counting
├── pyproject.toml                       # ⭐ UPDATED: Added [project.scripts]
├── CLAUDE.md                            # Project documentation (UPDATED)
├── test_cli_regression.sh               # 39-test regression suite
└── ...
```

## Tech Stack

### Core Dependencies
- **Python:** 3.10+ (with UV for package management)
- **AI Framework:** OpenAI Agents SDK v0.2.9
- **Web Framework:** Gradio 5.49.1+
- **Financial APIs:** Polygon Python Client, Tradier REST API
- **Data Processing:** Pandas, NumPy (implicit via Polygon/Tradier)

### Development Tools
- **Package Manager:** UV 0.8.19+
- **Linting:** Pylint, Black, isort
- **Type Checking:** mypy
- **Testing:** pytest (39-test regression suite)
- **Version Control:** Git (AWS CodeCommit)

### Deployment
- **Cloud:** AWS AppRunner (port 8000)
- **Container:** Docker (Dockerfile included)
- **CI/CD:** GitHub Actions

## Code Style & Conventions

### Python Style
- **Standard:** PEP 8
- **Line Length:** 88 (Black default)
- **Type Hints:** Comprehensive (all functions)
- **Docstrings:** Google/NumPy style, comprehensive
- **Naming:** snake_case for functions/variables, PascalCase for classes

### Import Organization
- **Pattern:** Relative imports within backend package
- **Order:** Standard library, third-party, local imports
- **Grouping:** Organized in clear sections

### Error Handling
- **Pattern:** DRY principle with centralized error_utils.py
- **Response Format:** JSON standardized via `create_error_response()`
- **Validation:** Centralized in validation_utils.py

### Documentation
- **Entry Points:** Well-documented in CLAUDE.md
- **Functions:** Comprehensive docstrings with examples
- **Architecture:** Documented in .serena/memories/ files

## Latest Gradio Features

### Progressive Web App (PWA)
- **Status:** ✅ ENABLED (pwa=True in gradio_app.py)
- **Benefit:** Users can install app on desktop/mobile
- **Installation:** Chrome/Edge browser install icon
- **Experience:** Standalone window, native-like app

### Hot Reload (Development)
- **Command:** `uv run gradio src/backend/gradio_app.py`
- **Feature:** Auto-reload on file save
- **Performance:** 2x-10x less CPU than standard auto-reload
- **Use Case:** Faster development iteration

### Production Mode (No Hot Reload)
- **Command:** `uv run python src/backend/gradio_app.py`
- **Port:** 8000 (localhost) or 0.0.0.0 (AWS AppRunner)
- **Features:** PWA still enabled

## Development Commands

### Entry Points
```bash
# Standard Python entry point (recommended)
uv run main.py

# Console scripts
uv run market-parser              # CLI
uv run market-parser-gradio       # Gradio

# Legacy methods
uv run src/backend/cli.py         # Direct CLI
uv run python -m backend.cli      # Module
```

### Gradio Development
```bash
# Hot reload mode (recommended for development)
uv run gradio src/backend/gradio_app.py

# Production mode (no hot reload)
uv run python src/backend/gradio_app.py
```

### Testing
```bash
# Run 39-test CLI regression suite
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

### Code Quality
```bash
# Linting
npm run lint              # Check with pylint
npm run lint:fix          # Auto-fix with black + isort

# Type checking
npm run type-check        # mypy

# Format
npm run format            # Format code

# Run all checks
npm run check:all         # All quality checks
```

### Code Management
```bash
# Commit work (atomic workflow)
git status                 # Review changes
git add -A                 # Stage all
git commit -m "message"    # Atomic commit
git push                   # Push to remote
```

## Testing (39 Tests)

### Test Categories
1. **Market Status** (1 test) - Check market open/closed status
2. **Single Ticker OHLC** (16 tests) - Price history for different tickers
3. **Multi-Ticker OHLC** (5 tests) - Compare multiple stocks
4. **Technical Analysis** (6 tests) - RSI, MACD, SMA, EMA indicators
5. **Options Chains** (8 tests) - Call/put options for various expiration dates
6. **Support/Resistance** (3 tests) - Key price levels

### Test Execution
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

### Test Results (Latest - Oct 18, 2025)
- **Total Tests:** 39/39 COMPLETED (100%)
- **Pass Rate:** 39/39 PASSED (100%)
- **Errors:** 0
- **Average Time:** 8.87s/test
- **Duration:** ~5-6 minutes total

## Recent Changes (October 18, 2025)

### Phase 1: Entry Point Setup
- ✅ Created `src/backend/__init__.py`
- ✅ Created `src/main.py`
- ✅ Added `main()` function to cli.py

### Phase 2: PyProject Scripts
- ✅ Added `[project.scripts]` to pyproject.toml
- ✅ Defined `market-parser` console script
- ✅ Defined `market-parser-gradio` console script

### Phase 3: Gradio Features
- ✅ Added `main()` function to gradio_app.py
- ✅ Enabled PWA with `pwa=True`
- ✅ Updated startup messages for PWA/hot reload

### Phase 4: Documentation
- ✅ Updated CLAUDE.md (entry points, Gradio features)
- ✅ Updated tech_stack_oct_2025.md
- ✅ Updated project_architecture.md
- ✅ Updated react_retirement_completion_oct_2025.md

### Phase 5: Testing
- ✅ 39/39 tests PASSED
- ✅ 0 errors found
- ✅ All entry points tested

### Phase 6: Git Commits
- ✅ Commit 469b7f6: Feature implementation
- ✅ Commit 560ba7b: Documentation update

## Important Guidelines

### Code Quality
1. **No breaking changes** - All changes are 100% backward compatible
2. **Comprehensive testing** - Must run 39-test suite before commits
3. **Standards compliance** - Full PEP 8 and Python best practices
4. **Documentation** - Update CLAUDE.md when adding features

### Development Workflow
1. **Use entry points** - Prefer `uv run main.py` over direct execution
2. **Use hot reload** - For Gradio development, use `uv run gradio ...`
3. **Run tests** - Always run 39-test suite after changes
4. **Atomic commits** - Stage all, commit all, push immediately

### Tool Usage
- **Serena Tools:** For code analysis, symbol manipulation
- **Sequential-Thinking:** For systematic planning
- **Bash:** For testing and git operations
- **Standard Read/Write/Edit:** For file operations

## Key Contacts & Resources

### Project Files
- **Main docs:** CLAUDE.md
- **Tech stack:** .serena/memories/tech_stack_oct_2025.md
- **Architecture:** .serena/memories/project_architecture.md
- **Code cleanup:** .serena/memories/code_cleanup_refactoring_oct_2025.md

### Git Status
- **Current branch:** react_retirement
- **Main branch:** master
- **Recent commits:** 469b7f6 (feature), 560ba7b (docs)

### APIs
- **Polygon.io:** Financial market data, technical indicators
- **Tradier:** Real-time market status, options chains
- **OpenAI:** GPT-5-nano for natural language processing

## Next Steps for Development

1. **Use new entry points:**
   - `uv run main.py` for CLI
   - `uv run market-parser` for console script
   - `uv run gradio src/backend/gradio_app.py` for hot reload development

2. **Run tests after changes:**
   - Always execute 39-test regression suite
   - Check for 0 errors in Phase 2 verification

3. **Update documentation:**
   - Add to CLAUDE.md Last Completed Task section
   - Update relevant .serena/memories/ files
   - Keep architecture documentation current

4. **Follow atomic commit workflow:**
   - Complete all work first
   - Stage all files at once
   - Commit and push immediately

---

**Last Updated:** October 18, 2025
**Project Status:** ✅ HEALTHY
**Test Status:** ✅ 39/39 PASSING
**Architecture:** ✅ OPTIMIZED (Latest refactoring complete)
