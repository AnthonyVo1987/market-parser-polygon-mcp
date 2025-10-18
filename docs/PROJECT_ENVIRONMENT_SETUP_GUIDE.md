# 🚀 Project Environment Setup Guide for AI Agents

## 📋 Overview

This guide provides step-by-step instructions for AI agents to completely re-initialize the Market Parser Polygon MCP project environment when corruption occurs. This guide is based on successful re-initialization performed on September 29, 2025, and incorporates best practices for Python and Node.js environment management.

## 🎯 Success Criteria

- ✅ All 39/39 CLI regression tests pass (100% success rate)
- ✅ Python environment with 121 packages installed
- ✅ CLI starts without errors
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
│       ├── cli.py           # CLI interface (CORE BUSINESS LOGIC)
│       ├── gradio_app.py    # Gradio web UI (wraps CLI core)
│       ├── tools/           # AI agent tools
│       └── services/        # Service layer
├── docs/                    # Documentation
├── test-reports/            # Test output files
├── pyproject.toml           # Python dependencies
├── package.json             # npm scripts (backend tooling only)
├── uv.lock                  # Python lock file
└── test_cli_regression.sh   # 39-test validation suite
```

**Note**: src/frontend/ directory has been completely removed. Gradio is the only web interface.

## 🚨 Emergency Environment Reset Procedure

### Phase 1: Pre-Reset Verification

#### Step 1.1: Check Current Status
```bash
# Navigate to project root
cd /path/to/market-parser-polygon-mcp

# Verify current directory
pwd

# Check git status and branch
git status
git branch --show-current
git log --oneline -1
```

#### Step 1.2: Identify Corruption Symptoms
Look for these common corruption indicators:
- `ModuleNotFoundError` for core packages
- `ImportError` for project modules
- `npm ERR!` or `uv error` messages
- Missing virtual environment
- Broken symlinks in node_modules
- Package version conflicts

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
# Check uv version
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
+ polygon-api-client==1.15.4
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
from src.backend.cli import initialize_persistent_agent, process_query_with_footer
from src.backend.gradio_app import chat_with_agent
from src.backend.services.agent_service import create_agent
from src.backend.tools.polygon_tools import get_market_status_and_date_time
from src.backend.tools.tradier_tools import get_stock_quote
print('✅ Core project imports successful')
print('✅ All AI agent tools import correctly')
"
```

### Phase 4: Environment Validation

#### Step 4.1: Test CLI
```bash
# Test CLI can start
uv run src/backend/cli.py --help

# Quick test query (optional)
echo "market status" | uv run src/backend/cli.py
```

**Expected Output:**
```
✅ Agent initialized successfully
> market status
[Response with market status...]
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

### Issue 1: Python Import Errors
**Symptoms:** `ModuleNotFoundError: No module named 'agents'`
**Solution:**
```bash
# Ensure you're using the correct package
grep -r "openai-agents" pyproject.toml
# Should show: openai-agents==0.2.9

# Reinstall Python dependencies
rm -rf .venv
uv sync
```

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

## 📊 Success Validation Checklist

- [ ] Python virtual environment created (`.venv/` directory exists)
- [ ] 121 Python packages installed successfully
- [ ] Python imports working (`openai`, `agents`, `polygon`, `gradio`, project modules)
- [ ] **polygon-api-client** SDK installed and functional
- [ ] **gradio** package installed and functional
- [ ] CLI starts without errors
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

## 🔗 Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Project development rules and procedures
- [README.md](../README.md) - Project overview and quick start
- [package.json](../package.json) - npm scripts (backend tooling only)
- [pyproject.toml](../pyproject.toml) - Python dependencies and configuration
- [.serena/memories/testing_procedures.md](testing_procedures.md) - Comprehensive testing guide

---

**Last Updated:** October 17, 2025 (FastAPI & Startup Script Removal)
**Tested On:** Linux WSL2/Ubuntu with Python 3.12.3, uv 0.8.11
**Success Rate:** 100% (all tests passing consistently)
**Recent Validations:**
- Oct 17, 2025: 39/39 tests PASSED (Gradio-only architecture), 9.67s avg
- Oct 6, 2025: 270/270 tests PASSED (10-loop baseline), 8.73s overall avg
- Sep 29, 2025: 7/7 tests PASSED, environment fully operational

**Architecture:** Gradio-only (port 8000), persistent agent, direct APIs