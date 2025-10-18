# Project Onboarding - Updated October 2025

**Last Updated:** 2025-10-18 (after dead code cleanup)
**Status:** COMPLETE - Comprehensive re-onboarding with latest architecture

---

## Project Purpose

**Market Parser** is a Python-based CLI and Gradio web interface for natural language financial queries. Users ask questions about stocks, options, technical analysis, and the system uses OpenAI GPT-5-nano with the OpenAI Agents SDK to analyze market data from Polygon.io and Tradier APIs.

**Architecture:** 100% Python full-stack (Gradio-only web UI, no React, no FastAPI)

---

## Technology Stack

### Core Technologies
- **Language:** Python 3.12.3
- **Package Manager:** uv 0.8.19
- **AI Framework:** OpenAI Agents SDK v0.2.9
- **AI Model:** GPT-5-nano (exclusive, 200K TPM)
- **Web UI:** Gradio 5.49.1+ (Python-based ChatInterface)

### Data Integration
- **Polygon.io:** Direct Python API (2 tools: market_status, ta_indicators)
- **Tradier:** Direct Python API (5 tools: quote, historical_prices, market_status, call_options, put_options)

### Development Tools
- **Linting:** pylint 3.0.0
- **Formatting:** black 23.12.0 (line length: 100)
- **Import Sorting:** isort 5.13.0 (black profile)
- **Type Checking:** mypy 1.7.0
- **Testing:** pytest 7.4.0

### Key Dependencies
```
openai-agents==0.2.9        # Agent orchestration
openai>=1.99.0,<1.100.0     # OpenAI API
pydantic                     # Data validation
gradio>=5.0.0                # Web UI
polygon-api-client>=1.14.0   # Polygon SDK
python-dotenv                # Environment config
rich                         # CLI formatting
aiofiles>=24.1.0             # Async file operations
python-lsp-server[all]>=1.13.1  # Language server
```

---

## Code Style & Conventions

### Python Style
- **Line Length:** 100 characters (Black standard)
- **Import Order:** Future → Stdlib → Third-party → First-party → Local (isort)
- **Type Hints:** Enabled for src/* (gradual adoption), disabled for tests
- **Docstrings:** Google-style docstrings expected
- **Naming:** snake_case for functions/variables, PascalCase for classes

### Code Organization
- **Directory Structure:** 
  - `src/backend/cli.py` - CLI core (single source of truth for business logic)
  - `src/backend/gradio_app.py` - Gradio wrapper (calls CLI core, no duplication)
  - `src/backend/tools/` - AI agent tools (polygon_tools.py, tradier_tools.py)
  - `src/backend/utils/` - Utility functions (response_utils, token_utils, datetime_utils)
  - `src/backend/services/` - Agent service initialization

### Design Patterns
- **Single Source of Truth:** CLI core owns all business logic
- **Wrapper Pattern:** Gradio imports and calls CLI functions directly
- **Persistent Agent:** ONE agent per lifecycle, reused for all messages
- **Tool Pattern:** AI tools are pure functions with clear contracts
- **No Code Duplication:** Gradio does NOT duplicate CLI logic

---

## Development Commands

### Start Applications
```bash
# CLI Interface (interactive terminal)
uv run src/backend/cli.py

# Gradio Web UI (browser-based, port 8000)
uv run python src/backend/gradio_app.py
# Access at http://127.0.0.1:8000
```

### Code Quality
```bash
# Linting (detect issues)
npm run lint                # Runs pylint on src/backend/ tests/

# Auto-fix (format + sort imports)
npm run lint:fix            # Runs black + isort on src/backend/ tests/

# Type checking (mypy)
uv run mypy src/backend/
```

### Testing
```bash
# Full CLI regression suite (39 comprehensive tests)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Expected: 39/39 COMPLETED with EXCELLENT performance (<10s avg)
# Results saved to: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log
```

### Maintenance
```bash
# Clean cache/builds
npm run clean              # Remove dist, test-results, node_modules
npm run clean:cache        # Remove cache files
npm run clean:install      # Clean + reinstall dependencies
npm run clean:full         # Full clean + reinstall

# Status check
npm run status             # Check Gradio health on port 8000
npm run health             # Same as status
```

### Git Operations
```bash
# View status
git status                 # Show changed files
git diff                   # Show changes

# Staging and committing (ATOMIC workflow)
git add -A                 # Stage ALL changes (only when ALL work done)
git commit -m "message"    # Commit immediately after staging
git push                   # Push immediately after commit

# Important: NEVER stage early. Only stage after ALL work complete.
# Reference: .serena/memories/git_commit_workflow.md
```

---

## Project Structure

```
market-parser-polygon-mcp/
├── src/
│   └── backend/
│       ├── cli.py                    # ⭐ CLI CORE (single source of truth)
│       ├── gradio_app.py             # ⭐ Gradio wrapper (imports CLI)
│       ├── config.py                 # Configuration management
│       ├── tools/
│       │   ├── tradier_tools.py      # 5 Tradier API tools
│       │   ├── polygon_tools.py      # 2 Polygon API tools
│       │   └── formatting_helpers.py # Response formatting
│       ├── utils/
│       │   ├── response_utils.py     # Response processing
│       │   ├── token_utils.py        # Token counting/caching
│       │   └── datetime_utils.py     # Date/time utilities
│       └── services/
│           └── agent_service.py      # Agent initialization
├── config/
│   └── app.config.json               # Non-sensitive settings
├── tests/                            # Test files
├── docs/                             # Documentation
├── .serena/                          # Serena onboarding files
│   └── memories/                     # Project knowledge base
├── test-reports/                     # Test execution reports
├── pyproject.toml                    # Python dependencies
├── package.json                      # npm/dev scripts
├── test_cli_regression.sh            # 39-test regression suite
└── CLAUDE.md                         # This guidance file
```

---

## Entry Points

### CLI Entry Point
- **File:** `src/backend/cli.py`
- **Main Function:** `cli_async()` (runs main loop)
- **Key Functions:** 
  - `initialize_persistent_agent()` - Create one agent per session
  - `process_query_with_footer()` - Process query and return with metrics
  - `_format_performance_footer()` - Format performance metrics

### Gradio Entry Point
- **File:** `src/backend/gradio_app.py`
- **Main Function:** ChatInterface setup
- **Wrapper Function:** `chat_with_agent(message, history)` - Calls CLI core
- **Access:** `http://127.0.0.1:8000`

---

## Key Features & Design

### Persistent Agent Architecture
- **One agent per lifecycle** (not per message)
- **System prompt cached** after first message (50% token savings)
- **Proper memory** maintained across entire session
- **CLI or Gradio** both use same agent architecture

### Performance Metrics
- **Tracked metrics:** Response time, tokens used, token type (input/output/cached)
- **Displayed to user:** In footer of every response
- **Format:** Plain text (works everywhere - CLI, Gradio, logs)

### Available Tools (7 total)
**Tradier (5 tools - PRIMARY):**
- get_stock_quote
- get_historical_prices
- get_market_status
- get_call_options_chain
- get_put_options_chain

**Polygon (2 tools - FALLBACK):**
- get_market_status_and_date_time
- get_ta_indicators

---

## Testing Strategy

### CLI Regression Suite (39 tests)
- **Location:** `test_cli_regression.sh`
- **Scope:** SPY (17 tests) + NVDA (17 tests) + Multi-ticker (5 tests)
- **Mode:** Single persistent session (all 39 tests in one CLI session)
- **Execution:** `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
- **Duration:** ~395 seconds (6.5 minutes)
- **Pass Criteria:** 39/39 COMPLETED with EXCELLENT performance (<10s avg)

### Two-Phase Testing Requirement
- **Phase 1:** Generate responses (automated by script)
- **Phase 2:** Verify responses with grep (manual verification required)

---

## Recent Architecture Changes (Oct 2025)

### React Retirement (Oct 17, 2025)
- ✅ Deleted entire React frontend (src/frontend/)
- ✅ Removed all TypeScript/JavaScript code
- ✅ Port 3000 removed (React web server)
- ✅ Result: Gradio is NOW the ONLY web interface

### FastAPI Removal (Oct 17, 2025)
- ✅ Deleted FastAPI backend (src/backend/main.py)
- ✅ Removed uvicorn dependencies
- ✅ Removed CORS middleware
- ✅ Result: Gradio runs standalone on port 8000

### Dead Code Cleanup (Oct 18, 2025)
- ✅ Deleted src/backend/__init__.py (dead imports)
- ✅ Deleted 6 obsolete config files (React/TypeScript tooling)
- ✅ Deleted .github/workflows/lighthouse-ci.yml (React CI)
- ✅ Cleaned all __pycache__/ orphaned bytecode
- ✅ Updated .pre-commit-config.yaml (removed ESLint)
- ✅ Updated documentation (React/FastAPI references)
- ✅ Result: Clean, simple Python-only architecture

---

## Migration Summary

**From (Oct 16, 2025):**
- React 18.2 (Port 3000) + FastAPI (Port 8000) + Gradio (Port 7860) = 3 servers
- ~25,000 lines of React/TypeScript code
- Complex multi-server orchestration

**To (Oct 18, 2025):**
- Gradio only (Port 8000) = 1 server
- ~0 lines of frontend code (all Python)
- Simple single-process architecture

**Benefits:**
- 60% faster startup time
- 30% less memory usage
- 50% token savings via prompt caching
- Simplified deployment and maintenance
- Zero code duplication (CLI is single source of truth)

---

## Important Guidelines

### Do's ✅
- Use Sequential-Thinking for complex tasks
- Use Serena tools for code analysis
- Use Black/isort for formatting
- Run test suite before committing
- Create atomic commits (all work at once)
- Update documentation when changing architecture

### Don'ts ❌
- Don't duplicate code between CLI and Gradio
- Don't stage files early during development
- Don't skip test execution
- Don't commit without documentation updates
- Don't modify git config or use --force
- Don't skip Phase 2 testing verification

---

## Relevant Memory Files

- `git_commit_workflow.md` - Atomic commit workflow
- `code_style_conventions.md` - Code style guidelines
- `testing_procedures.md` - Testing and validation procedures
- `tech_stack.md` - Detailed technology stack
- `dead_code_cleanup_completion_oct_2025.md` - Latest cleanup details
- `ai_agent_instructions_oct_2025.md` - Agent system details

---

**Last Onboarded:** 2025-10-18 (after dead code cleanup)
**Status:** ✅ Current with latest architecture
**Next Review:** When major architecture changes occur
