# Suggested Commands

## Application Startup

### One-Click Startup (Recommended)
```bash
# XTerm startup (RECOMMENDED - WORKING)
chmod +x start-app-xterm.sh && ./start-app-xterm.sh

# Main startup (NOW WORKING - FIXED with timeout)
chmod +x start-app.sh && ./start-app.sh

# Via npm scripts
npm run start:app:xterm    # XTerm version (recommended)
npm run start:app          # Main script (now working)
```

**What the scripts do:**
- Kill existing dev servers (uvicorn, vite)
- Start backend on http://127.0.0.1:8000
- Start frontend on http://127.0.0.1:3000
- Perform health checks
- Notify user to open browser (servers ready in 10-15s)
- **30-second timeout** prevents hanging

### Manual Server Startup
```bash
# Backend only
npm run backend:dev
# or
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload

# Frontend only
npm run frontend:dev
# or
vite --mode development

# Both servers (concurrently)
npm run dev
```

### CLI Interface
```bash
# Interactive CLI (no web GUI)
uv run src/backend/main.py
# or
npm run backend:cli
```

## Testing

### CLI Regression Testing
```bash
# Single test loop (27 tests)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Multiple test loops (e.g., 10 loops)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 10
```

**Test Coverage:**
- 27 standardized test prompts per loop
- Single persistent CLI session
- Response time tracking
- 100% success rate expected
- Average response time: ~6.10s

### Test Report Location
```bash
# Test reports saved to
ls -la test-reports/
```

## Code Quality

### Linting
```bash
# All linting (Python + JavaScript)
npm run lint

# Python linting only
npm run lint:python
uv run pylint src/backend/ tests/

# JavaScript/TypeScript linting only
npm run lint:js
eslint 'src/frontend/**/*.{ts,tsx}' --max-warnings 150
```

### Linting + Auto-Fix
```bash
# Fix all issues (Python + JavaScript)
npm run lint:fix

# Fix Python issues (black + isort)
npm run lint:fix:python
uv run black src/backend/ tests/ --line-length 100
uv run isort src/backend/ tests/ --profile black --line-length 100

# Fix JavaScript/TypeScript issues
npm run lint:fix:js
eslint 'src/frontend/**/*.{ts,tsx}' --fix
```

### Formatting
```bash
# Format JavaScript/TypeScript
npm run format
prettier --write 'src/frontend/**/*.{ts,tsx,js,jsx,json,css,md}'

# Check formatting
npm run format:check
prettier --check 'src/frontend/**/*.{ts,tsx,js,jsx,json,css,md}'
```

### Type Checking
```bash
# TypeScript type checking
npm run type-check
tsc --noEmit
```

### All Quality Checks
```bash
# Run all checks (lint + format + type-check)
npm run check:all
```

## Build Commands

### Production Build
```bash
# Build frontend for production
npm run build
# or
npm run frontend:build

# Build for specific environments
npm run frontend:build:development
npm run frontend:build:staging
npm run frontend:build:production
```

### Serve Production Build
```bash
# Development build + serve
npm run serve

# Staging build + serve
npm run serve:staging

# Production build + serve
npm run serve:production
```

**Note:** After running serve commands, open VS Code Command Palette (Ctrl+Shift+P) and run "Live Server: Open with Live Server"

## Performance Testing

### Lighthouse CI
```bash
# Build and prepare for Lighthouse testing
npm run lighthouse:live-server
npm run lighthouse:live-server:staging

# Run Lighthouse CI (after Live Server is running)
npx @lhci/cli@0.15.x autorun --config=lighthouserc.js
```

### Performance Monitoring
```bash
# React Scan (component re-renders)
npm run perf:scan

# Bundle analysis
npm run perf:bundle
source-map-explorer 'dist/assets/*.js'

# All performance checks
npm run perf:all
```

## Maintenance

### Installation
```bash
# Install all dependencies
npm run install:all
npm install

# Install backend dependencies only
npm run install:backend
uv install
```

### Cleanup
```bash
# Remove node_modules and dist
npm run clean
rm -rf node_modules dist test-results

# Remove cache
npm run clean:cache
rm -rf .cache node_modules/.cache

# Full cleanup + reinstall
npm run clean:install
npm run clean:full
```

### Health Check
```bash
# Check server status
npm run status
npm run health

# Manual backend health check
curl http://localhost:8000/health

# Manual frontend check
curl http://localhost:3000
```

## Development Utilities

### Git Workflow
```bash
# Check status
git status

# View changes
git diff

# Stage all changes (DO THIS LAST - see git_commit_workflow.md)
git add -A

# Commit (immediately after staging)
git commit -m "message"

# Push
git push
```

**CRITICAL:** See `.serena/memories/git_commit_workflow.md` for proper atomic commit workflow. Stage ONLY immediately before committing.

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
# or
vim .env
```

### Python Environment
```bash
# Check Python version
python3 --version

# Check uv version
uv --version

# Activate virtual environment (if needed)
source .venv/bin/activate
```

### Node Environment
```bash
# Check Node version
node --version

# Check npm version
npm --version
```

## Debugging

### Backend Debugging
```bash
# Run with verbose logging
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload --log-level debug
```

### Frontend Debugging
```bash
# Run with specific mode
vite --mode development
vite --mode staging
vite --mode production
```

### Process Management
```bash
# Find running processes
ps aux | grep uvicorn
ps aux | grep vite

# Kill processes (if startup scripts fail)
pkill -f uvicorn
pkill -f vite

# Check port usage
netstat -tlnp | grep :8000
netstat -tlnp | grep :3000
lsof -i :8000
lsof -i :3000
```

## Quick Reference

### Most Used Commands
```bash
# Start app (one-click)
chmod +x start-app-xterm.sh && ./start-app-xterm.sh

# Run CLI regression tests
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Lint and fix all issues
npm run lint:fix

# Type check
npm run type-check

# Build production
npm run build

# Check server health
npm run status
```

### Development Workflow
```bash
# 1. Start development servers
chmod +x start-app-xterm.sh && ./start-app-xterm.sh

# 2. Make code changes
# ... edit files ...

# 3. Run quality checks
npm run lint:fix
npm run type-check

# 4. Test changes
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# 5. Commit (proper atomic workflow - see git_commit_workflow.md)
git status
git diff
git add -A  # ONLY after ALL work complete
git commit -m "message"
git push
```
