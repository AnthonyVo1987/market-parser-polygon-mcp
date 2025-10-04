# 🚀 Project Environment Setup Guide for AI Agents

## 📋 Overview

This guide provides step-by-step instructions for AI agents to completely re-initialize the Market Parser Polygon MCP project environment when corruption occurs. This guide is based on successful re-initialization performed on September 29, 2025, and incorporates best practices for Python and Node.js environment management.

## 🎯 Success Criteria

- ✅ All 7/7 comprehensive CLI tests pass
- ✅ Python environment with 119 packages installed
- ✅ Node.js environment with 1131 packages installed
- ✅ Frontend builds successfully
- ✅ Backend server starts without errors
- ✅ All imports and dependencies working correctly

## 🔧 Prerequisites

- **Operating System**: Linux (WSL2/Ubuntu recommended)
- **Python**: 3.11.13 (managed by uv)
- **Node.js**: 18+ (for frontend development)
- **Package Managers**: uv (Python), npm (Node.js)
- **Git**: For version control and branch management

## 📁 Project Structure

```
market-parser-polygon-mcp/
├── .venv/                    # Python virtual environment
├── node_modules/             # Node.js dependencies
├── src/                      # Source code
│   ├── backend/             # FastAPI backend
│   └── frontend/            # React frontend
├── docs/                    # Documentation
├── test-reports/            # Test output files
├── pyproject.toml           # Python dependencies
├── package.json             # Node.js dependencies
├── uv.lock                  # Python lock file
├── package-lock.json        # Node.js lock file
└── test_7_prompts_comprehensive.sh  # Validation script
```

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
# Check uv version
uv --version

# If uv not installed, install it
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

#### Step 3.2: Install Python Dependencies

```bash
# Install all Python dependencies
uv sync

# Verify installation
uv run python -c "import openai; from agents import Agent, Runner, SQLiteSession; print('✅ Python imports working')"
```

**Expected Output:**

```
Using CPython 3.11.13
Creating virtual environment at: .venv
Resolved 125 packages in 552ms
Installed 119 packages in 195ms
+ aiofiles==24.1.0
+ openai==1.99.9
+ openai-agents==0.2.9
... (additional packages)
✅ Python imports working
```

#### Step 3.3: Verify Python Environment

```bash
# Check virtual environment
ls -la .venv/

# Test critical imports
uv run python -c "
import sys
print(f'Python version: {sys.version}')
print(f'Python path: {sys.executable}')

# Test core project imports
from src.backend.main import app
from src.backend.services.agent_service import create_agent
print('✅ Core project imports successful')
"
```

### Phase 4: Node.js Environment Setup

#### Step 4.1: Verify Node.js Installation

```bash
# Check Node.js version
node --version

# Check npm version
npm --version

# If Node.js not installed, install it
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Step 4.2: Install Node.js Dependencies

```bash
# Install all Node.js dependencies with legacy peer deps
npm install --legacy-peer-deps

# Verify installation
npm list --depth=0
```

**Expected Output:**

```
added 1130 packages, and audited 1131 packages in 49s
263 packages are looking for funding
6 vulnerabilities (4 low, 2 moderate)
```

#### Step 4.3: Test Frontend Build

```bash
# Test frontend build
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
✓ built in 5.31s
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
{"status": "healthy", "timestamp": "2025-09-29T10:19:23.123456"}
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

#### Step 6.1: Run 7-Prompt Comprehensive Test

```bash
# Run the comprehensive test suite
./test_7_prompts_comprehensive.sh
```

**Expected Output:**

```
🧪 Comprehensive 7 Test Prompts Validation
=========================================
📊 Test Results Summary:
   Test 1: Test_1_Market_Status_Query - PASS
   Test 2: Test_2_Single_Stock_Snapshot_NVDA - PASS
   Test 3: Test_3_Full_Market_Snapshot_SPY_QQQ_IWM - PASS
   Test 4: Test_4_Closing_Price_Query_GME - PASS
   Test 5: Test_5_Performance_Analysis_SOUN - PASS
   Test 6: Test_6_Support_Resistance_NVDA - PASS
   Test 7: Test_7_Technical_Analysis_SPY - PASS

📊 Response Time Analysis:
   Min Response Time: 23.944s
   Max Response Time: 23.944s
   Avg Response Time: 0s
   Successful Tests: 7/7

📈 Overall Performance Rating: GOOD
🎉 All 7 tests passed!
✅ Comprehensive Validation: SUCCESS
```

#### Step 6.2: Verify Test Report

```bash
# Check test report was created
ls -la test-reports/comprehensive_7_prompts_test_*.txt

# Verify test report content
head -20 test-reports/comprehensive_7_prompts_test_*.txt
```

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
- [ ] 119 Python packages installed successfully
- [ ] Python imports working (`openai`, `agents`, project modules)
- [ ] Node.js dependencies installed (1131 packages)
- [ ] Frontend builds without errors
- [ ] Backend server starts and responds to health checks
- [ ] Frontend server starts and serves content
- [ ] All 7 comprehensive tests pass
- [ ] Test report generated successfully
- [ ] No critical errors in logs

## 🚀 Quick Recovery Commands

For rapid recovery when you know the issue:

```bash
# Complete reset and reinstall
rm -rf .venv node_modules package-lock.json uv.lock dist/ dev-dist/
uv sync
npm install --legacy-peer-deps
./test_7_prompts_comprehensive.sh
```

## 📝 Notes for AI Agents

1. **Always verify each step** before proceeding to the next
2. **Check error messages carefully** - they often indicate the root cause
3. **Use the comprehensive test** as the final validation step
4. **Document any deviations** from this guide for future reference
5. **If tests fail**, check the test report for specific error details
6. **Environment corruption** often requires complete cleanup, not partial fixes

## 🔗 Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Project development rules and procedures
- [README.md](../README.md) - Project overview and quick start
- [package.json](../package.json) - Node.js scripts and dependencies
- [pyproject.toml](../pyproject.toml) - Python dependencies and configuration

---

**Last Updated:** September 29, 2025  
**Tested On:** Linux WSL2/Ubuntu with Python 3.11.13 and Node.js 18+  
**Success Rate:** 100% (7/7 tests passing)
