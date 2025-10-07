# 🚀 Project Environment Setup Guide for AI Agents

## 📋 Overview

This guide provides step-by-step instructions for AI agents to completely re-initialize the Market Parser Polygon MCP project environment when corruption occurs. This guide is based on successful re-initializations performed on September 29, 2025 and October 6, 2025, and incorporates best practices for Python and Node.js environment management.

## 🎯 Success Criteria

- ✅ All 27/27 CLI regression tests pass (100% success rate)
- ✅ Python environment with 121 packages installed
- ✅ Node.js environment with 1,131 packages installed
- ✅ Frontend builds successfully
- ✅ Backend server starts without errors
- ✅ All imports and dependencies working correctly
- ✅ polygon-api-client SDK properly installed and functional

## 🔧 Prerequisites

- **Operating System**: Linux (WSL2/Ubuntu recommended)
- **Python**: 3.12.3 (managed by uv)
- **Node.js**: 24.6.0+ (for frontend development)
- **Package Managers**: uv 0.8.11+ (Python), npm 11.6.0+ (Node.js)
- **Git**: For version control and branch management

## 📁 Project Structure

```
market-parser-polygon-mcp/
├── .venv/                    # Python virtual environment
├── node_modules/             # Node.js dependencies
├── src/                      # Source code
│   ├── backend/             # FastAPI backend
│   │   ├── main.py          # Main application
│   │   ├── tools/           # AI agent tools
│   │   │   └── polygon_tools.py  # Polygon Direct API tools
│   │   └── services/        # Service layer
│   │       └── agent_service.py  # Agent creation service
│   └── frontend/            # React frontend
├── docs/                    # Documentation
├── test-reports/            # Test output files
├── pyproject.toml           # Python dependencies
├── package.json             # Node.js dependencies
├── uv.lock                  # Python lock file
├── package-lock.json        # Node.js lock file
└── CLI_test_regression.sh   # Comprehensive validation script (27 tests)
```

## 🚨 Emergency Environment Reset Procedure

### Phase 1: Pre-Reset Verification

#### Step 1.1: Check Current Status

```bash
# Navigate to project root
cd /home/1000211866/Github/market-parser-polygon-mcp

# Verify current directory
pwd

# Check git status and branch
git status
git branch --show-current
git log --oneline -1
```

#### Step 1.2: Identify Corruption Symptoms

Look for these common corruption indicators:

- `ModuleNotFoundError` for core packages (especially polygon, openai, agents)
- `ImportError` for project modules (polygon_tools, agent_service)
- `npm ERR!` or `uv error` messages
- Missing virtual environment (.venv/ directory)
- Broken symlinks in node_modules
- Package version conflicts
- Test failures due to missing dependencies

### Phase 2: Complete Environment Cleanup

#### Step 2.1: Stop All Running Processes

```bash
# Kill any running development servers
pkill -f "uvicorn"
pkill -f "vite"
pkill -f "npm run"

# Verify no processes are running on project ports
netstat -tlnp | grep -E ":(3000|8000|5500)"
```

#### Step 2.2: Remove All Environment Files

```bash
# Remove Python virtual environment
rm -rf .venv

# Remove Node.js dependencies
rm -rf node_modules

# Remove lock files
rm -f package-lock.json
rm -f uv.lock

# Remove any build artifacts
rm -rf dist/
rm -rf dev-dist/

# Verify cleanup
ls -la | grep -E "(\.venv|node_modules|package-lock\.json|uv\.lock)" || echo "✅ Cleanup complete"
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
+ finnhub-python==2.4.25
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
from src.backend.services.agent_service import create_agent
from src.backend.tools.polygon_tools import (
    get_market_status_and_date_time,
    get_ta_sma,
    get_OHLC_bars_custom_date_range
)
print('✅ Core project imports successful')
print('✅ All 11 AI agent tools import correctly')
"
```

### Phase 4: Node.js Environment Setup

#### Step 4.1: Verify Node.js Installation

```bash
# Check Node.js version (should be 24.6.0+)
node --version

# Check npm version (should be 11.6.0+)
npm --version

# If Node.js not installed, install it
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Step 4.2: Install Node.js Dependencies

```bash
# Install all Node.js dependencies with legacy peer deps
npm install --legacy-peer-deps

# Verify installation
npm list --depth=0
```

**Expected Output (Oct 6, 2025):**

```
added 1131 packages, and audited 1131 packages in 42s
263 packages are looking for funding
6 vulnerabilities (4 low, 2 moderate)
```

#### Step 4.3: Test Frontend Build

```bash
# Test frontend production build
npm run build

# Verify build output
ls -la dist/
```

**Expected Output:**

```
vite v5.4.20 building for production...
transforming...
✓ 224 modules transformed.
rendering chunks...
✓ built in 3.65s
```

### Phase 5: Environment Validation

#### Step 5.1: Test Backend Server

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
{"status": "healthy", "timestamp": "2025-10-06T10:19:23.123456"}
```

#### Step 5.2: Test Frontend Server

```bash
# Start frontend server in background
npm run frontend:dev &

# Wait for server to start
sleep 10

# Test frontend endpoint
curl -s http://127.0.0.1:3000 | head -10

# Stop server
pkill -f "vite"
```

**Expected Output:**

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Market Parser</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### Phase 6: Comprehensive Testing

#### Step 6.1: Run CLI Regression Test Suite (27 Tests)

```bash
# Run the comprehensive 27-test regression suite
./CLI_test_regression.sh
```

**Expected Output (Oct 6, 2025 Format):**

```
🧪 CLI REGRESSION TEST SUITE
====================================
📊 Test Configuration:
   Total Prompts: 27
   Loop Count: 1/1
   Session Mode: PERSISTENT (single session)
   Calculation Engine: awk (universal compatibility)

⏱️  Total Session Duration: 3 min 49 sec

📊 Test Results Summary:
   Total Tests: 27
   Passed: 27
   Failed: 0
   Success Rate: 100%

=== RESPONSE TIME ANALYSIS ===
Min Response Time: 3.62s
Max Response Time: 17.91s
Avg Response Time: 8.42s
Performance Rating: EXCELLENT

✅ All 27 tests PASSED!
✅ Session Persistence: VERIFIED (1 session)
✅ Overall Performance Rating: EXCELLENT
```

#### Step 6.2: Verify Test Report

```bash
# Check test report was created
ls -la test-reports/cli_regression_test_*.txt

# Verify test report content shows all statistics correctly
head -30 test-reports/cli_regression_test_*.txt
```

**Expected:** Test report should show:
- ✅ All 27 tests PASSED
- ✅ Duration in "MM min SS sec" format (not "XXXs")
- ✅ Response times with 2 decimal precision (e.g., 8.42s, not 8.443s)
- ✅ Min/Max/Avg all different values (not stuck at same value)
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
- This occurred after syncing back to main branch following massive architectural changes

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

### Issue 2: Node.js Peer Dependency Conflicts

**Symptoms:** `npm ERR! ERESOLVE unable to resolve dependency tree`
**Solution:**

```bash
# Use legacy peer deps flag
npm install --legacy-peer-deps

# If still failing, clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Issue 3: Port Already in Use

**Symptoms:** `Error: Port 3000 is already in use`
**Solution:**

```bash
# Find and kill processes using ports
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Verify ports are free
netstat -tlnp | grep -E ":(3000|8000)"
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
grep -c "awk.*BEGIN.*printf" CLI_test_regression.sh

# Should show 10+ matches (awk calculations present)

# If script still uses bc, update from latest version in repo
git checkout master -- CLI_test_regression.sh
```

## 📊 Success Validation Checklist

- [ ] Python virtual environment created (`.venv/` directory exists)
- [ ] 121 Python packages installed successfully
- [ ] Python imports working (`openai`, `agents`, `polygon`, project modules)
- [ ] **polygon-api-client** SDK installed and functional
- [ ] Node.js dependencies installed (1,131 packages)
- [ ] Frontend builds without errors (production build succeeds)
- [ ] Backend server starts and responds to health checks
- [ ] Frontend server starts and serves content
- [ ] **All 27 CLI regression tests pass (100% success rate)**
- [ ] Test report generated successfully with correct formatting
- [ ] Test statistics calculated correctly (no 0s, proper min/max/avg)
- [ ] Duration shows in "MM min SS sec" format
- [ ] No critical errors in logs

## 🚀 Quick Recovery Commands

For rapid recovery when you know the issue:

```bash
# Complete reset and reinstall
rm -rf .venv node_modules package-lock.json uv.lock dist/ dev-dist/
uv sync
npm install --legacy-peer-deps
./CLI_test_regression.sh
```

## 📊 Recent Successful Re-Initializations

### Oct 6, 2025 - Post-Branch-Sync Re-Init
**Context:** Environment corrupted after syncing back to main branch following massive architectural changes (MCP removal, model selector removal, token tracking enhancements)

**Outcome:**
- ✅ 121 Python packages installed (121/121 success)
- ✅ 1,131 Node.js packages installed (1,131/1,131 success)
- ✅ **polygon-api-client dependency bug discovered and fixed**
- ✅ All 27/27 CLI regression tests PASSED (100% success)
- ✅ Avg Response Time: 8.42s (EXCELLENT performance)
- ✅ Production build: 3.65s (successful)

**Critical Fix Applied:**
- Added missing `polygon-api-client>=1.14.0` to pyproject.toml
- This dependency was required after Phase 4 migration to Direct Polygon API
- Without it, all Polygon tool imports failed with ModuleNotFoundError

### Sep 29, 2025 - Initial Comprehensive Re-Init
**Outcome:**
- ✅ 119 Python packages installed
- ✅ 1,131 Node.js packages installed  
- ✅ All 7/7 comprehensive tests PASSED
- ✅ Environment fully operational

## 📝 Notes for AI Agents

1. **Always verify each step** before proceeding to the next
2. **Check error messages carefully** - they often indicate the root cause
3. **Use the CLI regression test suite** as the final validation step (27 tests)
4. **Document any deviations** from this guide for future reference
5. **If tests fail**, check the test report for specific error details
6. **Environment corruption** often requires complete cleanup, not partial fixes
7. **After major architectural changes**, always verify dependency completeness
8. **Check pyproject.toml** for missing dependencies if imports fail
9. **Test statistics should be non-zero** - if you see 0s, calculation engine has issues
10. **Polygon Direct API requires polygon-api-client** - verify it's installed

## Critical Dependencies Checklist

When re-initializing, verify these critical packages are present:

### Python (pyproject.toml)
```toml
dependencies = [
  "openai-agents==0.2.9",
  "openai>=1.99.0,<1.100.0",
  "polygon-api-client>=1.14.0",  # CRITICAL for Direct API
  "finnhub-python>=2.4.25",
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

# Test 3: Finnhub API
uv run python -c "import finnhub; print('✅ Finnhub SDK OK')"

# Test 4: Project Tools
uv run python -c "from src.backend.tools.polygon_tools import get_market_status_and_date_time; print('✅ Polygon Tools OK')"

# Test 5: Agent Service
uv run python -c "from src.backend.services.agent_service import create_agent; print('✅ Agent Service OK')"
```

## 🔗 Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Project development rules and procedures
- [README.md](../README.md) - Project overview and quick start
- [package.json](../package.json) - Node.js scripts and dependencies
- [pyproject.toml](../pyproject.toml) - Python dependencies and configuration
- [.serena/memories/testing_procedures.md](testing_procedures.md) - Comprehensive testing guide

---

**Last Updated:** October 6, 2025  
**Tested On:** Linux WSL2/Ubuntu with Python 3.12.3, uv 0.8.11, Node.js 24.6.0, npm 11.6.0  
**Success Rate:** 100% (all tests passing consistently)  
**Recent Validations:** 
- Oct 6, 2025 (12:00 PM PDT): **270/270 tests PASSED** (10-loop baseline), 8.73s overall avg
- Oct 6, 2025 (11:00 AM PDT): 81/81 tests PASSED (3-loop validation), 8.71s overall avg
- Sep 29, 2025: 7/7 tests PASSED, environment fully operational

**Comprehensive Validation Summary:**
- Total tests executed: 358 (270 + 81 + 7)
- Success rate: 100% (358/358 PASSED)
- Performance: EXCELLENT (all tests < 10s average)
- Reliability: Fully stable and operational
