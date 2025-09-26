# Suggested Commands for Market Parser Development

## 🚀 Application Startup Commands

### One-Click Startup (Recommended)

```bash
# Main startup script - automatically manages all servers
./start-app.sh

# Alternative XTerm version for better terminal compatibility
./start-app-xterm.sh

# npm script versions
npm run start:app
npm run start:app:xterm
```

### Manual Development Server Startup

```bash
# Start both backend and frontend
npm run dev

# Backend only (FastAPI with auto-reload)
npm run backend:dev

# Frontend only (Vite dev server)
npm run frontend:dev

# Backend CLI mode
npm run backend:cli
```

## 🔧 Code Quality Commands

### Linting and Formatting

```bash
# Run all linting (Python + TypeScript)
npm run lint

# Fix linting issues automatically
npm run lint:fix

# Python-specific linting
npm run lint:python

# TypeScript/JavaScript linting
npm run lint:js

# Format TypeScript/JavaScript code
npm run format

# Check formatting without fixing
npm run format:check

# TypeScript type checking
npm run type-check

# Run all checks (lint + format + type-check)
npm run check:all
```

### Python Code Quality

```bash
# Run PyLint
uv run pylint src/backend/ tests/

# Format with Black
uv run black src/backend/ tests/ --line-length 100

# Sort imports with isort
uv run isort src/backend/ tests/ --profile black --line-length 100

# Type checking with mypy
uv run mypy src/backend/
```

## 🏗️ Build Commands

### Frontend Builds

```bash
# Production build
npm run build

# Staging build
npm run build:staging

# Development build
npm run build:development

# Build all (frontend only)
npm run build:all
```

### Analysis and Optimization

```bash
# Bundle analysis
npm run analyze

# Visual bundle analyzer
npm run analyze:visualizer

# CSS optimization
npm run css:optimize

# CSS minification
npm run css:minify
```

## 🧪 Testing Commands

### Performance Testing

```bash
# Run all performance tests
npm run test:perf:all

# Development performance test
npm run test:perf:dev

# Staging performance test
npm run test:perf:staging

# Production performance test
npm run test:perf:prod
```

### Lighthouse Testing

```bash
# Run Lighthouse CI
npm run lighthouse

# Lighthouse with live server
npm run lighthouse:live-server

# Staging Lighthouse test
npm run lighthouse:live-server:staging
```

### PWA Testing

```bash
# Test PWA functionality
npm run test:pwa

# Staging PWA test
npm run test:pwa:staging

# Production PWA test
npm run test:pwa:production
```

## 📊 Performance Monitoring

### Performance Analysis

```bash
# React performance scan
npm run perf:scan

# Bundle analysis
npm run perf:bundle

# Lighthouse performance
npm run perf:lighthouse

# All performance tests
npm run perf:all
```

## 🌐 Serving and Deployment

### Local Serving

```bash
# Serve development build
npm run serve

# Serve staging build
npm run serve:staging

# Serve production build
npm run serve:production
```

### Cross-Device Testing

```bash
# Setup for cross-device testing
npm run cross-device:setup

# Staging cross-device testing
npm run cross-device:staging
```

## 🧹 Maintenance Commands

### Installation and Cleanup

```bash
# Install all dependencies
npm run install:all

# Install backend dependencies
npm run install:backend

# Clean build artifacts
npm run clean

# Clean cache
npm run clean:cache

# Clean and reinstall
npm run clean:install

# Full clean and reinstall
npm run clean:full

# Reset everything
npm run reset
```

## 🔍 Utility Commands

### Status and Health Checks

```bash
# Check application status
npm run status

# Health check
npm run health

# Backend health check
curl http://127.0.0.1:8000/health

# Frontend status
curl http://127.0.0.1:3000
```

### Development Utilities

```bash
# Live server help
npm run live-server:help

# Check running processes
ps aux | grep -E "(uvicorn|vite)"

# Check network connections
netstat -tlnp | grep -E ":(8000|3000)"

# Kill development servers
pkill -f "uvicorn src.backend.main:app"
pkill -f "vite.*--mode development"
```

## 🐍 Python-Specific Commands

### Package Management

```bash
# Install Python dependencies
uv install

# Install with dev dependencies
uv install --group dev

# Run Python scripts
uv run src/backend/main.py

# Run with specific Python version
uv run --python 3.11 src/backend/main.py
```

### Testing and Development

```bash
# Run Python tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/backend

# Run specific test file
uv run pytest tests/unit/test_api.py

# Run with verbose output
uv run pytest -v
```

## 🔧 System Commands (Linux)

### File Operations

```bash
# List files with details
ls -la

# Find files by pattern
find . -name "*.py" -type f

# Search in files
grep -r "pattern" src/

# Copy files
cp source destination

# Move/rename files
mv old_name new_name
```

### Process Management

```bash
# List processes
ps aux

# Kill processes by name
pkill -f "process_name"

# Kill processes by PID
kill -9 PID

# Check process status
ps aux | grep process_name
```

### Network Operations

```bash
# Check network connections
netstat -tlnp

# Test HTTP endpoints
curl -X GET http://127.0.0.1:8000/health

# Check if port is in use
lsof -i :8000

# Test connectivity
ping google.com
```

### Git Operations

```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "message"

# Push changes
git push

# Pull changes
git pull

# Check logs
git log --oneline

# Create branch
git checkout -b feature-branch
```

## 📋 Standardized Test Prompts

### Quick Response Test Prompts (Use These Only)

```bash
# Test prompts for consistent 30-60 second responses
# See tests/playwright/test_prompts.md for complete list

1. "Quick Response Needed with minimal tool calls: What is the current Market Status?"
2. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Single Stock Snapshot NVDA"
3. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Full Market Snapshot: SPY, QQQ, IWM"
4. "Quick Response Needed with minimal tool calls: Based on Market Status Date, what was the closing price of GME today?"
5. "Quick Response Needed with minimal tool calls: Based on Market Status Date, how is SOUN performance doing this week?"
6. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Top Market Movers Today for Gainers"
7. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Top Market Movers Today for Losers"
8. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Support & Resistance Levels NVDA"
9. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Technical Analysis SPY"
```

## 🎯 Best Practices

### Development Workflow

1. **Start development**: `./start-app.sh`
2. **Make changes** to code
3. **Run linting**: `npm run lint:fix`
4. **Test changes**: Use standardized test prompts
5. **Commit changes**: `git add . && git commit -m "message"`

### Code Quality Workflow

1. **Before committing**: `npm run check:all`
2. **Fix issues**: `npm run lint:fix`
3. **Verify types**: `npm run type-check`
4. **Test performance**: `npm run test:perf:dev`

### Testing Workflow

1. **Use standardized prompts** for consistent testing
2. **Test all environments**: dev, staging, production
3. **Monitor performance** with Lighthouse CI
4. **Verify PWA functionality** on different devices
