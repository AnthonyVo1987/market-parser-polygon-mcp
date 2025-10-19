# Suggested Commands - Latest October 2025

## Entry Points (Latest - Just Added)

### CLI Interface

```bash
# Standard Python entry point (RECOMMENDED - just added Oct 18)
uv run main.py

# Console script (RECOMMENDED - just added Oct 18)
uv run market-parser

# Legacy methods (still supported)
uv run src/backend/cli.py
uv run python -m backend.cli
```

### Gradio Web Interface

```bash
# Development with hot reload (RECOMMENDED for dev - just added Oct 18)
uv run gradio src/backend/gradio_app.py

# Console script (just added Oct 18)
uv run market-parser-gradio

# Production mode (no hot reload)
uv run python src/backend/gradio_app.py
```

## Testing

```bash
# Run full 39-test CLI regression suite (recommended after any changes)
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# View latest test report
cat test-reports/test_cli_regression_loop1_*.log | tail -50

# Check for errors (Phase 2 verification)
grep -c "error\|unavailable" test-reports/test_cli_regression_loop1_*.log
```

## Code Quality

```bash
# Lint Python code
npm run lint

# Auto-fix with black + isort
npm run lint:fix

# Type checking with mypy
npm run type-check

# Format code
npm run format

# Run all checks
npm run check:all
```

## Git Workflow (Atomic)

```bash
# Check status (before staging anything)
git status

# Review changes
git diff

# Stage ALL files at once (ONLY do this when all work is complete)
git add -A

# Verify staging
git status

# Commit immediately
git commit -m "message"

# Push immediately
git push
```

## Development Utilities

```bash
# List project files and structure
ls -la src/backend/

# Find specific symbols in code
grep -r "main()" src/backend/

# Search for function definitions
grep -r "^def " src/backend/

# Count lines of code
find src/backend -name "*.py" -exec wc -l {} +

# Check Python version
python --version

# Check UV version
uv --version
```

## Serena Tools (Code Analysis)

```bash
# List directory structure
mcp__serena__list_dir

# Search for code patterns
mcp__serena__search_for_pattern

# Get symbol overview
mcp__serena__get_symbols_overview

# Find specific symbols
mcp__serena__find_symbol

# Write memory files
mcp__serena__write_memory
```

## One-Command Development Workflow

```bash
# 1. Make code changes
# 2. Run tests
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# 3. Check quality
npm run lint:fix && npm run type-check

# 4. Stage and commit
git add -A && git commit -m "message" && git push
```

## Debugging

```bash
# Test CLI entry point
uv run main.py

# Test console script
uv run market-parser

# Test Gradio with hot reload
timeout 10 uv run gradio src/backend/gradio_app.py

# Check imports
python -c "from backend.cli import main; print('CLI imports OK')"
python -c "from backend.gradio_app import main; print('Gradio imports OK')"
```

## Documentation

```bash
# View main project documentation
cat CLAUDE.md | head -100

# View tech stack
cat .serena/memories/tech_stack_oct_2025.md

# View project architecture
cat .serena/memories/project_architecture.md

# View task plan
cat TODO_task_plan.md
```

## Configuration & Environment

```bash
# Check .env variables
grep -E "API_KEY|POLYGON|TRADIER" .env

# Reload environment
source .env

# Check Python dependencies
uv pip list | grep -E "gradio|openai|polygon"
```

## Notes

- **Entry Points:** Recently refactored (Oct 18) - use new `uv run main.py`
- **Console Scripts:** Just enabled (Oct 18) - use `uv run market-parser`
- **Gradio Features:** PWA enabled + hot reload available
- **Tests:** Always run 39-test suite after changes
- **Commits:** Follow atomic workflow strictly
- **Hot Reload:** Use `gradio` command for faster development

---

**Last Updated:** October 18, 2025
**All commands tested and working:** ✅
