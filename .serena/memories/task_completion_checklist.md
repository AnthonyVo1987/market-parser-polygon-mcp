# Task Completion Checklist

## 🔴 CRITICAL: Testing is MANDATORY - Not Optional

**Before ANY task can be considered complete:**

1. ✅ Code must be implemented
2. ✅ Tests must be EXECUTED (not just created)
3. ✅ Test results must be SHOWN (100% pass rate)
4. ✅ Test report path must be provided
5. ❌ NO test execution = Task INCOMPLETE

**Rule:** Code without test execution = Code NOT implemented

---

## Pre-Commit Code Quality Checks

### 1. Linting (Required - Must Pass)

```bash
npm run lint                  # Run all linting checks
```

**Requirements:**

- ✅ Python: 10.00/10 pylint score (zero errors)
- ✅ JavaScript/TypeScript: 0 errors (4 acceptable warnings currently)
- ❌ Do NOT commit if linting fails

### 2. Type Checking (Required)

```bash
npm run type-check            # TypeScript type validation
```

**Requirements:**

- ✅ No TypeScript compilation errors
- ✅ All type definitions properly declared

### 3. Code Formatting (Required)

```bash
npm run format:check          # Verify Prettier formatting
```

**If formatting issues found:**

```bash
npm run lint:fix              # Auto-fix Python + JS/TS
npm run format                # Apply Prettier formatting
```

### 4. Build Validation (Recommended)

```bash
npm run build                 # Production build test
```

**Requirements:**

- ✅ Build completes without errors
- ✅ No bundle size regressions
- ⚠️ Monitor build time (should be ~3-6s)

## 🔴 Testing Requirements (MANDATORY - DO NOT SKIP)

### 5. Run Comprehensive Tests (REQUIRED FOR TASK COMPLETION)

**🔴 CRITICAL: You MUST execute tests and show results - not just create test files**

```bash
# Run the appropriate test suite based on task
./CLI_test_regression.sh   # For tasks with 16 tests
# OR
./test_7_prompts_comprehensive.sh          # For tasks with 7 tests
```

**Expected Results (MUST VERIFY):**

- ✅ All X/X tests must PASS (100% success rate)
- ✅ Response times: 13-35s average (varies with real API calls)
- ✅ Test report generated in test-reports/
- ✅ Session persistence verified (single session for all tests)
- ✅ Performance metrics shown (min/max/avg response times)
- ⚠️ Varying response times confirm real API calls (not mocked)

**ENFORCEMENT:**

- ❌ Task is NOT complete without test execution
- ❌ Creating test file ≠ Running test file
- ❌ Updating test suite ≠ Executing test suite
- ✅ Must RUN tests and SHOW results to user
- ✅ Must verify 100% pass rate
- ✅ Must provide test report file path

### 6. Verify Test Reports

```bash
ls -la test-reports/comprehensive_7_prompts_test_*.txt
```

**Check for:**

- Test completion timestamp
- All tests marked as PASS
- Performance ratings (GOOD/EXCELLENT)
- No error messages in output

## Server Health Checks

### 7. Backend Health Verification

```bash
# Start backend
npm run backend:dev

# In another terminal, check health
curl http://127.0.0.1:8000/health
```

**Expected Response:**

```json
{"status": "healthy", "timestamp": "2025-XX-XXTXX:XX:XX.XXXXXX"}
```

### 8. Frontend Build & Serve

```bash
npm run build
npm run serve
```

**Verify:**

- ✅ Frontend builds successfully
- ✅ Application loads at <http://127.0.0.1:3000>
- ✅ No console errors in browser DevTools

## Documentation Updates

### 9. Update CLAUDE.md (If Applicable)

If task involves significant changes, update:

```markdown
## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
[TYPE] Brief description

- Bullet point of changes
- Additional modifications
- Breaking changes if any

BREAKING CHANGE: Description (if applicable)
<!-- LAST_COMPLETED_TASK_END -->
```

### 10. Update Memory Files (For Major Changes)

If task introduces new patterns, architecture changes, or commands:

- Update relevant Serena memory files
- Add new memory files if needed
- Keep memories concise and actionable

## Git Commit Process

### 11. Stage Changes

```bash
git status                    # Review changed files
git add .                     # Stage all changes
# OR
git add <specific_files>      # Stage specific files only
```

### 12. Verify Staged Changes

```bash
git diff --cached             # Review what will be committed
```

### 13. Create Commit

```bash
git commit -m "$(cat <<'EOF'
[TYPE] Brief description

- Detailed change 1
- Detailed change 2
- Additional modifications

BREAKING CHANGE: Description (if applicable)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Commit Types:**

- `[feat]`: New feature
- `[fix]`: Bug fix
- `[refactor]`: Code refactoring
- `[test]`: Test changes
- `[docs]`: Documentation
- `[chore]`: Maintenance
- `[RE-INIT]`: Environment re-initialization
- `[SERENA]`: Serena-related changes

### 14. Push Changes (When Ready)

```bash
git push                      # Push to remote
```

## Performance Validation

### 15. Run Performance Checks (Optional but Recommended)

```bash
npm run lighthouse            # Lighthouse CI audit
npm run perf:bundle           # Bundle size analysis
```

**Performance Targets:**

- First Contentful Paint: ~256ms
- Core Web Vitals: 85%+ improvement
- Memory Heap: ~13.8MB
- Bundle size: Monitor for regressions

## Environment Validation

### 16. Verify Environment Integrity

```bash
# Check Python environment
uv run python -c "import openai; from agents import Agent; print('✅ Python OK')"

# Check Node.js dependencies
npm list --depth=0 | head -10

# Verify servers can start
./start-app.sh
```

## Final Checklist Summary

Before considering a task complete, verify:

- [ ] All linting checks pass (Python 10/10, JS/TS 0 errors)
- [ ] TypeScript type checking passes
- [ ] Code properly formatted (Black, isort, Prettier)
- [ ] Production build succeeds
- [ ] All 7 comprehensive tests pass
- [ ] Backend health endpoint responds correctly
- [ ] Frontend loads without errors
- [ ] CLAUDE.md updated if needed
- [ ] Memory files updated for significant changes
- [ ] Git commit created with proper format
- [ ] Changes pushed to remote (if ready)

## Common Issues & Solutions

### Issue: Linting Fails

**Solution:**

```bash
npm run lint:fix              # Auto-fix most issues
# Manually fix remaining issues
npm run lint                  # Re-verify
```

### Issue: Tests Fail

**Solution:**

1. Check backend is running: `curl http://127.0.0.1:8000/health`
2. Verify API keys in `.env`
3. Check test output for specific errors
4. Review test-reports/ for detailed logs

### Issue: Build Fails

**Solution:**

```bash
npm run clean:full            # Deep clean
uv sync                       # Reinstall Python deps
npm install --legacy-peer-deps # Reinstall Node deps
npm run build                 # Retry build
```

### Issue: Port Already in Use

**Solution:**

```bash
pkill -f "uvicorn"            # Kill backend
pkill -f "vite"               # Kill frontend
lsof -ti:8000 | xargs kill -9 # Force kill port 8000
lsof -ti:3000 | xargs kill -9 # Force kill port 3000
```

## Project-Specific Requirements

### GPT-5-Nano Only Policy

- ✅ Verify no GPT-5-Mini references introduced
- ✅ All AI calls use GPT-5-Nano model
- ⚠️ Breaking change if model policy modified

### API Key Security

- ❌ NEVER commit `.env` file
- ❌ NEVER hardcode API keys
- ✅ Always use environment variables
- ✅ Verify `.env.example` is updated if new keys added

### Startup Script Compatibility

- ✅ Verify scripts work in both X11 and WSL2/headless environments
- ✅ Scripts must exit cleanly (30s timeout mechanism)
- ✅ Health checks must complete successfully

## Continuous Integration Notes

When CI/CD is implemented:

- All checklist items should be automated in CI pipeline
- Failing checks should block merges
- Performance budgets should be enforced
- Security scans should run on dependencies
