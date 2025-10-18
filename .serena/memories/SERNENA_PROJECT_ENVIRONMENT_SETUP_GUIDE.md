# 🚀 Project Environment Setup Guide for AI Agents

## 📋 Overview

This guide provides step-by-step instructions for AI agents to completely re-initialize the Market Parser project environment when corruption occurs. This guide is based on successful re-initializations performed on September 29, 2025 and October 6, 2025, and incorporates best practices for Python environment management.

**Update (Oct 17, 2025)**: React frontend completely retired. Gradio (port 8000) is now the ONLY web interface.

## 🎯 Success Criteria

- ✅ All 39/39 CLI regression tests pass (100% success rate)
- ✅ Python environment with 121 packages installed
- ✅ Backend server starts without errors
- ✅ Gradio UI starts successfully (port 8000)
- ✅ All imports and dependencies working correctly
- ✅ polygon-api-client SDK properly installed and functional

## 🔧 Prerequisites

- **Operating System**: Linux (WSL2/Ubuntu recommended)
- **Python**: 3.12.3 (managed by uv)
- **Package Manager**: uv 0.8.11+ (Python)
- **Git**: For version control and branch management
- **No Node.js required**: Gradio is Python-based (package.json used for backend tooling only)

## 📁 Project Structure

```
market-parser-polygon-mcp/
├── .venv/                    # Python virtual environment
├── src/                      # Source code
│   └── backend/             # All application code
│       ├── main.py          # Main application
│       ├── cli.py           # CLI interface (CORE BUSINESS LOGIC)
│       ├── gradio_app.py    # Gradio web UI (wraps CLI core)
│       ├── tools/           # AI agent tools
│       │   ├── polygon_tools.py  # Polygon Direct API tools
│       │   └── tradier_tools.py  # Tradier Direct API tools
│       └── services/        # Service layer
│           └── agent_service.py  # Agent creation service
├── docs/                    # Documentation
├── test-reports/            # Test output files
├── pyproject.toml           # Python dependencies
├── package.json             # npm scripts (backend tooling only)
├── uv.lock                  # Python lock file
└── test_cli_regression.sh   # Comprehensive validation script (39 tests)
```

**Note**: src/frontend/ directory has been completely removed. Gradio is the only web interface.

## 🚨 Emergency Environment Reset Procedure

### Phase 1: Pre-Reset Verification

#### Step 1.1: Check Current Status

```bash
# Navigate to project root
cd /home/anthony/Github/market-parser-polygon-mcp

# Verify current directory
pwd

# Check git status and branch
git status
git branch --show-current
git log --oneline -1
```

#### Step 1.2: Identify Corruption Symptoms

Look for these common corruption indicators:

- `ModuleNotFoundError` for core packages (especially polygon, openai, agents, gradio)
- `ImportError` for project modules (polygon_tools, tradier_tools, agent_service)
- `uv error` messages
- Missing virtual environment (.venv/ directory)
- Package version conflicts
- Test failures due to missing dependencies

### Phase 2: Complete Environment Cleanup

#### Step 2.1: Stop All Running Processes

```bash
# Kill any running development servers
pkill -f "uvicorn"
pkill -f "gradio"
pkill -f "python.*gradio_app"

# Verify no processes are running on project ports
netstat -tlnp | grep -E ":(8000|8000|5500)"
```

#### Step 2.2: Remove All Environment Files

```bash
# Remove Python virtual environment
rm -rf .venv

# Remove lock files
rm -f uv.lock

# Remove any build artifacts
rm -rf dist/
rm -rf dev-dist/

# Verify cleanup
ls -la | grep -E "(\\.venv|uv\\.lock)" || echo "✅ Cleanup complete"
```

### Phase 3: Python Environment Setup

#### Step 3.1: Verify uv Installation

```bash
# Check uv version (should be 0.8.11+)
uv --version

# If uv not installed, install it
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

#### Step 3.2: Install Python Dependencies

```bash
# Install all Python dependencies from pyproject.toml
uv sync

# Verify critical package installations
uv run python -c "
import openai
from agents import Agent, Runner, SQLiteSession
from polygon import RESTClient
import gradio as gr
print('✅ Python imports working')
"
```

**Expected Output (Oct 6, 2025):**

```
Using CPython 3.12.3
Creating virtual environment at: .venv
Resolved 125 packages in 234ms
Installed 121 packages in 8.05s
+ aiofiles==24.1.0
+ gradio==5.0.0+
+ openai==1.99.9
+ openai-agents==0.2.9
+ openai-agents-mcp==0.0.8
+ polygon-api-client==1.15.4
+ python-lsp-server==1.13.1
... (additional packages)
✅ Python imports working
```

#### Step 3.3: Verify Python Environment

```bash
# Check virtual environment
ls -la .venv/

# Test critical project imports
uv run python -c "
import sys
print(f'Python version: {sys.version}')
print(f'Python path: {sys.executable}')

# Test core project imports
from src.backend.main import app
from src.backend.cli import initialize_persistent_agent, process_query_with_footer
from src.backend.gradio_app import chat_with_agent
from src.backend.services.agent_service import create_agent
from src.backend.tools.polygon_tools import get_market_status_and_date_time, get_ta_indicators
from src.backend.tools.tradier_tools import get_stock_quote, get_historical_prices
print('✅ Core project imports successful')
print('✅ All AI agent tools import correctly')
"
```

### Phase 4: Environment Validation

#### Step 4.1: Test Backend Server

```bash
# Start backend server in background
npm run backend:dev &

# Wait for server to start
sleep 10

# Test health endpoint
curl -s http://127.0.0.1:8000/health

# Stop server
pkill -f "uvicorn"
```

**Expected Output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000
{"status": "healthy", "timestamp": "2025-10-17T10:19:23.123456"}
```

#### Step 4.2: Test Gradio UI

```bash
# Start Gradio UI in background
uv run python src/backend/gradio_app.py &

# Wait for Gradio to start
sleep 10

# Test Gradio endpoint
curl -s http://127.0.0.1:8000 | head -10

# Stop Gradio
pkill -f "gradio_app"
```

**Expected Output:**

```
🚀 Initializing Market Parser Gradio Interface...
✅ Agent initialized successfully
Running on local URL:  http://127.0.0.1:8000
```

### Phase 5: Comprehensive Testing

#### Step 5.1: Run CLI Regression Test Suite (39 Tests)

```bash
# Run the comprehensive 39-test regression suite
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Expected Output (Oct 17, 2025 Format):**

```
🧪 CLI REGRESSION TEST SUITE
====================================
📊 Test Configuration:
   Total Prompts: 39
   Loop Count: 1/1
   Session Mode: PERSISTENT (single session)

⏱️  Total Session Duration: 6 min 18 sec

📊 Test Results Summary:
   Total Tests: 39
   Passed: 39
   Failed: 0
   Success Rate: 100%

=== RESPONSE TIME ANALYSIS ===
Min Response Time: 3.62s
Max Response Time: 17.91s
Avg Response Time: 9.67s
Performance Rating: EXCELLENT

✅ All 39 tests PASSED!
✅ Session Persistence: VERIFIED (1 session)
✅ Overall Performance Rating: EXCELLENT
```

#### Step 5.2: Verify Test Report

```bash
# Check test report was created
ls -la test-reports/test_cli_regression_loop1_*.log

# Verify test report content
head -30 test-reports/test_cli_regression_loop1_*.log
```

**Expected:** Test report should show:
- ✅ All 39 tests PASSED
- ✅ Duration in "MM min SS sec" format
- ✅ Response times with 2 decimal precision (e.g., 9.67s)
- ✅ Min/Max/Avg all different values
- ✅ No "0s" or "0.00s" for Duration or Avg Response Time

## 🔍 Troubleshooting Common Issues

### Issue 1: Python Import Error - Missing polygon Module

**Symptoms:** 
```
ModuleNotFoundError: No module named 'polygon'
  File ".../polygon_tools.py", line 11, in <module>
    from polygon import RESTClient
```

**Root Cause (Oct 6, 2025):**
- After architectural migration to Direct Polygon API, code imports `from polygon import RESTClient`
- `pyproject.toml` was missing `polygon-api-client` dependency

**Solution:**
```bash
# Verify polygon-api-client is in pyproject.toml dependencies
grep "polygon-api-client" pyproject.toml

# If missing, add it to pyproject.toml:
# polygon-api-client>=1.14.0

# Then reinstall dependencies
uv sync

# Verify installation
uv run python -c "from polygon import RESTClient; print('✅ Polygon SDK working')"
```

**Validation:** Re-run test suite to confirm all imports working

### Issue 2: Gradio Import Error

**Symptoms:** `ModuleNotFoundError: No module named 'gradio'`

**Solution:**
```bash
# Verify gradio is in pyproject.toml
grep "gradio" pyproject.toml

# Reinstall dependencies
uv sync

# Verify installation
uv run python -c "import gradio as gr; print('✅ Gradio working')"
```

### Issue 3: Port Already in Use

**Symptoms:** `Error: Port 8000 is already in use` or `Error: Port 8000 is already in use`

**Solution:**

```bash
# Find and kill processes using ports
lsof -ti:8000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Verify ports are free
netstat -tlnp | grep -E ":(8000|8000)"
```

### Issue 4: Virtual Environment Path Issues

**Symptoms:** `uvicorn not using uv environment`

**Solution:**

```bash
# Use npm scripts instead of direct uvicorn
npm run backend:dev

# Or ensure uv environment is activated
source .venv/bin/activate
uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Issue 5: Test Script Shows Incorrect Statistics

**Symptoms (Fixed Oct 6, 2025):**
- Total Session Duration: 0s
- Avg Response Time: 0s
- Min/Max Response Time stuck at same value

**Root Cause:** Script used `bc` (bash calculator) which was not installed

**Solution:** ✅ **FIXED** - Script now uses `awk` for all calculations (universally available)

**If you see this issue:**
```bash
# Verify script has been updated
grep -c "awk.*BEGIN.*printf" test_cli_regression.sh

# Should show 10+ matches (awk calculations present)

# If script still uses bc, update from latest version in repo
git checkout master -- test_cli_regression.sh
```

## 📊 Success Validation Checklist

- [ ] Python virtual environment created (`.venv/` directory exists)
- [ ] 121 Python packages installed successfully
- [ ] Python imports working (`openai`, `agents`, `polygon`, `gradio`, project modules)
- [ ] **polygon-api-client** SDK installed and functional
- [ ] **gradio** package installed and functional
- [ ] Backend server starts and responds to health checks
- [ ] Gradio UI starts successfully (port 8000)
- [ ] **All 39 CLI regression tests pass (100% success rate)**
- [ ] Test report generated successfully with correct formatting
- [ ] Test statistics calculated correctly (no 0s, proper min/max/avg)
- [ ] Duration shows in "MM min SS sec" format
- [ ] No critical errors in logs

## 🚀 Quick Recovery Commands

For rapid recovery when you know the issue:

```bash
# Complete reset and reinstall
rm -rf .venv uv.lock dist/ dev-dist/
uv sync
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

## 📊 Recent Successful Re-Initializations

### Oct 17, 2025 - Post-React-Retirement Re-Init
**Context:** Environment update after React frontend retirement

**Outcome:**
- ✅ 121 Python packages installed
- ✅ Gradio UI working on port 8000
- ✅ All 39/39 CLI regression tests PASSED
- ✅ Avg Response Time: 9.67s (EXCELLENT performance)
- ✅ No React dependencies needed

### Oct 6, 2025 - Post-Branch-Sync Re-Init
**Context:** Environment corrupted after syncing back to main branch following massive architectural changes (MCP removal, model selector removal)

**Outcome:**
- ✅ 121 Python packages installed (121/121 success)
- ✅ **polygon-api-client dependency bug discovered and fixed**
- ✅ All 27/27 CLI regression tests PASSED (100% success)
- ✅ Avg Response Time: 8.42s (EXCELLENT performance)

**Critical Fix Applied:**
- Added missing `polygon-api-client>=1.14.0` to pyproject.toml
- This dependency was required after Phase 4 migration to Direct Polygon API

### Sep 29, 2025 - Initial Comprehensive Re-Init
**Outcome:**
- ✅ 119 Python packages installed
- ✅ All 7/7 comprehensive tests PASSED
- ✅ Environment fully operational

## 📝 Notes for AI Agents

1. **Always verify each step** before proceeding to the next
2. **Check error messages carefully** - they often indicate the root cause
3. **Use the CLI regression test suite** as the final validation step (39 tests)
4. **Document any deviations** from this guide for future reference
5. **If tests fail**, check the test report for specific error details
6. **Environment corruption** often requires complete cleanup, not partial fixes
7. **After major architectural changes**, always verify dependency completeness
8. **Check pyproject.toml** for missing dependencies if imports fail
9. **Test statistics should be non-zero** - if you see 0s, calculation engine has issues
10. **Polygon Direct API requires polygon-api-client** - verify it's installed
11. **Gradio requires gradio package** - verify it's installed
12. **No React/Node.js needed** - Gradio is Python-based

## Critical Dependencies Checklist

When re-initializing, verify these critical packages are present:

### Python (pyproject.toml)
```toml
dependencies = [
  "openai-agents==0.2.9",
  "openai>=1.99.0,<1.100.0",
  "polygon-api-client>=1.14.0",  # CRITICAL for Direct API
  "gradio>=5.0.0",                # CRITICAL for web UI
  "fastapi",
  "uvicorn[standard]",
  "pydantic",
  "rich",
  "python-dotenv",
  "aiofiles>=24.1.0",
  "python-lsp-server[all]>=1.13.1",
  "openai-agents-mcp>=0.0.8",
]
```

### Critical Import Tests
```bash
# Test 1: OpenAI Agents SDK
uv run python -c "from agents import Agent, Runner; print('✅ Agents SDK OK')"

# Test 2: Polygon Direct API
uv run python -c "from polygon import RESTClient; print('✅ Polygon SDK OK')"

# Test 3: Gradio UI
uv run python -c "import gradio as gr; print('✅ Gradio OK')"

# Test 4: Project Tools
uv run python -c "from src.backend.tools.polygon_tools import get_market_status_and_date_time; print('✅ Polygon Tools OK')"

# Test 5: Project Tools
uv run python -c "from src.backend.tools.tradier_tools import get_stock_quote; print('✅ Tradier Tools OK')"

# Test 6: Gradio App
uv run python -c "from src.backend.gradio_app import chat_with_agent; print('✅ Gradio App OK')"

# Test 7: Agent Service
uv run python -c "from src.backend.services.agent_service import create_agent; print('✅ Agent Service OK')"
```

## 🔗 Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Project development rules and procedures
- [README.md](../README.md) - Project overview and quick start
- [package.json](../package.json) - npm scripts (backend tooling only)
- [pyproject.toml](../pyproject.toml) - Python dependencies and configuration
- [.serena/memories/testing_procedures.md](testing_procedures.md) - Comprehensive testing guide

---

**Last Updated:** October 17, 2025 (React Frontend Retirement)
**Tested On:** Linux WSL2/Ubuntu with Python 3.12.3, uv 0.8.11
**Success Rate:** 100% (all tests passing consistently)
**Recent Validations:** 
- Oct 17, 2025: 39/39 tests PASSED (Gradio-only frontend), 9.67s avg
- Oct 6, 2025: 270/270 tests PASSED (10-loop baseline), 8.73s overall avg
- Sep 29, 2025: 7/7 tests PASSED, environment fully operational

**Architecture:** Gradio-only frontend (port 8000), persistent agent, direct APIs
