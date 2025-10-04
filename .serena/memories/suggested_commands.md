# Suggested Development Commands

## Quick Start Commands

### One-Click Application Startup
```bash
./start-app-xterm.sh          # Recommended: XTerm startup (working)
./start-app.sh                # Main startup script (working with 30s timeout)
npm run start:app             # Alternative: npm wrapper for start-app.sh
```

**What these scripts do:**
- Kill existing dev servers (uvicorn, vite)
- Start backend on http://127.0.0.1:8000
- Start frontend on http://127.0.0.1:3000
- Perform health checks (10 retries, 2s intervals)
- Exit cleanly after verification or 30s timeout
- **Note:** Scripts do NOT auto-open browser - manually navigate to http://127.0.0.1:3000

## Backend Development

### Running Backend
```bash
npm run backend:dev           # Start FastAPI with hot reload (port 8000)
npm run backend:cli           # Run CLI interface directly
uv run src/backend/main.py    # Alternative: Direct Python execution
```

### Backend Installation
```bash
uv install                    # Install Python dependencies
npm run backend:install       # Alternative: npm wrapper
```

## Frontend Development

### Running Frontend
```bash
npm run frontend:dev          # Start Vite dev server (port 3000)
npm run dev                   # Start both backend + frontend concurrently
```

### Building Frontend
```bash
npm run build                 # Production build (optimized)
npm run build:staging         # Staging build
npm run build:dev             # Development build
```

## Code Quality Commands

### Linting
```bash
npm run lint                  # Run all linting (Python + JS/TS)
npm run lint:python           # Python only: pylint src/backend/ tests/
npm run lint:js               # JavaScript/TypeScript only: eslint
```

### Formatting
```bash
npm run lint:fix              # Auto-fix all (Python + JS)
npm run lint:fix:python       # Black + isort for Python
npm run lint:fix:js           # ESLint --fix for JS/TS
npm run format                # Prettier for JS/TS
```

### Type Checking
```bash
npm run type-check            # TypeScript type checking (tsc --noEmit)
npm run check:all             # Run lint + format check + type check
```

## Testing Commands

### Comprehensive Testing
```bash
./test_7_prompts_comprehensive.sh   # Run 7-prompt validation suite
```

**Expected Output:**
- All 7/7 tests should pass
- Response times: 19-46s (varies per real API calls)
- Test report generated in test-reports/

## Health & Status Checks

### Check Server Status
```bash
npm run status                # Check backend + frontend health
npm run health                # Alias for status
curl http://127.0.0.1:8000/health   # Direct backend health check
```

## Installation & Maintenance

### Clean & Reinstall
```bash
npm run clean                 # Remove node_modules and dist
npm run clean:install         # Clean + fresh install
npm run clean:full            # Deep clean (cache + install)
```

### Environment Setup
```bash
uv sync                       # Sync Python environment (recommended)
npm install --legacy-peer-deps # Install Node.js dependencies
```

## Git & Version Control

### Standard Git Operations
```bash
git status                    # Check working tree status
git add .                     # Stage all changes
git commit -m "message"       # Commit with message
git push                      # Push to remote
git pull                      # Pull from remote
```

## Linux System Utilities

### File Operations
```bash
ls -la                        # List files with details
cd <directory>                # Change directory
grep -r "pattern" .           # Search for pattern recursively
find . -name "*.py"           # Find files by name
tree -L 2                     # Show directory tree (2 levels)
```

### Process Management
```bash
ps aux | grep uvicorn         # Find uvicorn processes
pkill -f uvicorn              # Kill uvicorn processes
lsof -ti:8000                 # Find process using port 8000
netstat -tlnp | grep :3000    # Check port 3000 status
```

### Port Management
```bash
lsof -ti:3000 | xargs kill -9 # Kill process on port 3000
lsof -ti:8000 | xargs kill -9 # Kill process on port 8000
```

## Performance & Analysis

### Performance Testing
```bash
npm run lighthouse            # Run Lighthouse CI
npm run perf:bundle           # Bundle size analysis
npm run analyze               # Vite bundle analyzer
```

## Environment Requirements

- **Python**: 3.10+ (managed by uv)
- **Node.js**: 18.0.0+
- **npm**: 9.0.0+
- **uv**: Latest version for Python package management

## API Keys Required

Ensure `.env` file contains:
```
POLYGON_API_KEY=your_polygon_key
OPENAI_API_KEY=your_openai_key
```

## Port Configuration

- **Backend API**: http://127.0.0.1:8000
- **Frontend Dev**: http://127.0.0.1:3000
- **API Docs**: http://127.0.0.1:8000/docs (Swagger UI)

## Common Troubleshooting Commands

### Port Already in Use
```bash
pkill -f "uvicorn"            # Kill backend server
pkill -f "vite"               # Kill frontend server
lsof -ti:8000 | xargs kill -9 # Force kill port 8000
```

### Dependencies Issues
```bash
rm -rf .venv node_modules package-lock.json uv.lock
uv sync
npm install --legacy-peer-deps
```

### Verify Environment
```bash
python3 --version             # Check Python version
uv --version                  # Check uv version
node --version                # Check Node.js version
npm --version                 # Check npm version
```