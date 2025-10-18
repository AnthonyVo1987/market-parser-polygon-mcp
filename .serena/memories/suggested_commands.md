# Suggested Commands

## Application Startup

### Gradio Web UI (Recommended)
```bash
# Start Gradio interface on port 7860
uv run python src/backend/gradio_app.py

# Access: http://127.0.0.1:7860
```

### CLI Interface
```bash
# Interactive CLI (no web GUI)
uv run src/backend/main.py
# or
npm run backend:cli
```

### Backend Server Only
```bash
# Backend only (for API access)
npm run backend:dev
# or
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload

# Access API docs: http://127.0.0.1:8000/docs
```

## Testing

### CLI Regression Testing
```bash
# Single test loop (39 tests)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Multiple test loops (e.g., 10 loops)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh 10
```

**Test Coverage:**
- 39 standardized test prompts per loop
- Single persistent CLI session
- Response time tracking
- 100% success rate expected
- Average response time: ~9.67s

### Test Report Location
```bash
# Test reports saved to
ls -la test-reports/
```

## Code Quality

### Linting
```bash
# Python linting
npm run lint:python
uv run pylint src/backend/ tests/

# Python linting + auto-fix
npm run lint:fix
uv run black src/backend/ tests/ --line-length 100
uv run isort src/backend/ tests/ --profile black --line-length 100
```

## Maintenance

### Installation
```bash
# Install backend dependencies
npm run install:backend
uv install
```

### Cleanup
```bash
# Remove cache
npm run clean:cache
rm -rf .cache node_modules/.cache

# Full cleanup
npm run clean
rm -rf node_modules dist test-results
```

### Health Check
```bash
# Check server status
npm run status
npm run health

# Manual backend health check
curl http://localhost:8000/health

# Manual Gradio UI check
curl http://localhost:7860
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

## Debugging

### Backend Debugging
```bash
# Run with verbose logging
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload --log-level debug
```

### Gradio UI Debugging
```bash
# Run with debug mode
uv run python src/backend/gradio_app.py --debug
```

### Process Management
```bash
# Find running processes
ps aux | grep uvicorn
ps aux | grep gradio

# Kill processes
pkill -f uvicorn
pkill -f gradio_app

# Check port usage
netstat -tlnp | grep :8000
netstat -tlnp | grep :7860
lsof -i :8000
lsof -i :7860
```

## Quick Reference

### Most Used Commands
```bash
# Start Gradio UI
uv run python src/backend/gradio_app.py

# Run CLI regression tests
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# Lint and fix all issues
npm run lint:fix

# Check server health
npm run status
```

### Development Workflow
```bash
# 1. Start Gradio web interface
uv run python src/backend/gradio_app.py

# 2. Make code changes
# ... edit files ...

# 3. Run quality checks
npm run lint:fix

# 4. Test changes
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# 5. Commit (proper atomic workflow - see git_commit_workflow.md)
git status
git diff
git add -A  # ONLY after ALL work complete
git commit -m "message"
git push
```

## Notes

- **React frontend removed**: React has been completely retired (Oct 17, 2025)
- **Gradio only**: Gradio (port 7860) is the ONLY web interface
- **No frontend build commands**: No npm run build, frontend:dev, type-check, etc.
- **Port 3000 removed**: Only ports 8000 (backend) and 7860 (Gradio) are active
