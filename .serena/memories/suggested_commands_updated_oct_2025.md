# Suggested Commands - Updated October 2025

**Note:** Reflect current Gradio-only architecture (React retired, FastAPI removed)

---

## 🚀 Quick Start

### Start CLI (Interactive Terminal)
```bash
uv run src/backend/cli.py
# Type: "Tesla stock analysis"
# Result: Financial analysis with metrics
```

### Start Gradio Web UI (Browser-based)
```bash
uv run python src/backend/gradio_app.py
# Access: http://127.0.0.1:8000
```

---

## 🛠️ Code Quality Commands

### View Linting Issues
```bash
npm run lint
# Runs: uv run pylint src/backend/ tests/
```

### Auto-fix Code (Black + isort)
```bash
npm run lint:fix
# Runs: 
#   uv run black src/backend/ tests/ --line-length 100
#   uv run isort src/backend/ tests/ --profile black --line-length 100
```

### Type Check (mypy)
```bash
uv run mypy src/backend/
# Verify type annotations
```

---

## 🧪 Testing Commands

### Run Full CLI Regression Suite (39 tests)
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
# Expected: 39/39 COMPLETED in ~395 seconds
# Result: Test report in test-reports/
```

### Run Python Tests (pytest)
```bash
uv run pytest tests/ -v
# Run unit tests
```

---

## 🧹 Maintenance Commands

### Clean Build Artifacts & Cache
```bash
npm run clean
# Removes: dist, test-results, node_modules

npm run clean:cache
# Removes: cache files only

npm run clean:full
# clean + reinstall dependencies
```

### Check Service Health
```bash
npm run status
# Verify Gradio running on port 8000

npm run health
# Same as status
```

---

## 📊 Development Workflow Commands

### Check Git Status
```bash
git status
# View all changed/untracked files
```

### Review Changes Before Commit
```bash
git diff
# View all changes
```

### Stage ALL Changes (Atomic Commit)
```bash
git add -A
# Stage ALL changes ONLY after ALL work complete
# WARNING: Never stage early during development!
```

### Commit Changes
```bash
git commit -m "$(cat <<'EOF'
[TAG] Descriptive message

- Change 1
- Change 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Push to Remote
```bash
git push
# Push immediately after commit
```

---

## 🔍 Code Exploration Commands

### Search for Pattern
```bash
grep -r "search_term" src/backend/
# Basic pattern search

grep -r -i "case-insensitive" src/backend/
# Case-insensitive search
```

### Find Python Files
```bash
find src/backend -name "*.py" -type f
# List all Python files
```

### Count Lines of Code
```bash
find src/backend -name "*.py" -type f -exec wc -l {} +
# Lines per file
```

---

## 📈 Performance & Monitoring

### Check Response Times
```bash
# From test report
grep "Response Time" test-reports/test_cli_regression_loop1_*.log
# Should show: ~9.5s average (EXCELLENT)
```

### Verify Test Pass Rate
```bash
# From test report
grep "COMPLETED" test-reports/test_cli_regression_loop1_*.log | wc -l
# Should show: 40 (39 tests + 1 summary line)
```

### Monitor Port 8000
```bash
curl http://127.0.0.1:8000
# Test Gradio availability

netstat -tlnp | grep 8000
# Check port binding
```

---

## 🔄 Development Cycle

### Typical Development Flow
```bash
# 1. Make code changes
# 2. Test code quality
npm run lint:fix

# 3. Run full test suite
chmod +x test_cli_regression.sh && ./test_cli_regression.sh

# 4. Review changes
git diff
git status

# 5. Stage ALL changes (only when ALL work complete)
git add -A

# 6. Verify staging
git status

# 7. Commit immediately
git commit -m "message"

# 8. Push immediately
git push
```

---

## 🚫 Commands NOT to Use

### ❌ Don't Use
```bash
# DON'T: Early staging during development
git add src/backend/cli.py  # Bad!

# DON'T: Delayed staging
git add -A
# ... more work ...
git commit  # Changed files won't be included!

# DON'T: Force push
git push --force  # Never on shared branches

# DON'T: Skip hooks
git commit --no-verify  # Skip pre-commit hooks

# DON'T: Modify git config
git config user.email "someone@example.com"  # Don't do this
```

---

## 📚 Serena Tool Commands

### Get Project Symbols Overview
```bash
# Via Serena tools (more efficient than grep)
# Use mcp__serena__get_symbols_overview
# Returns: function/class definitions in a file
```

### Search for Code Patterns
```bash
# Via Serena tools
# Use mcp__serena__search_for_pattern
# Finds: regex patterns in files (faster than grep)
```

### Find References
```bash
# Via Serena tools
# Use mcp__serena__find_referencing_symbols
# Finds: where a symbol is used
```

---

## 💾 Backup & Recovery

### Restore Deleted File
```bash
git checkout HEAD -- path/to/file.py
# Restore from git history
```

### Undo Staging
```bash
git reset HEAD
# Unstage all changes
```

### Revert Last Commit
```bash
git revert HEAD
# Create new commit that undoes previous
```

---

## 📋 Task Completion Checklist

When completing a task:
- [ ] Code changes made
- [ ] Test suite runs (39/39)
- [ ] Code quality checked (npm run lint:fix)
- [ ] Documentation updated
- [ ] Changes reviewed (git diff)
- [ ] All changes staged (git add -A)
- [ ] Commit created with proper message
- [ ] Pushed to remote (git push)

---

**Last Updated:** October 18, 2025
**Architecture:** Gradio-only Python full-stack
**Test Suite:** 39-test CLI regression
**Performance Target:** <10s average response time
