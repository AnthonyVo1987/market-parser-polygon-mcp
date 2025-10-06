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
./CLI_test_regression.sh   # For tasks with 27 tests (single persistent session)
```

**Expected Results (MUST VERIFY):**

- ✅ All 27/27 tests must PASS (100% success rate)
- ✅ Response times: 6-10s average (EXCELLENT performance)
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
ls -la test-reports/cli_regression_test_*.txt
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

## 🔴 CRITICAL: Proper Atomic Commit Workflow

**⚠️ MANDATORY: Stage ONLY Immediately Before Commit**

**See `.serena/memories/git_commit_workflow.md` for complete workflow documentation**

### The Fatal Mistake: Early Staging

**NEVER stage files early during development. Staging is the LAST step before committing.**

**What happens when you stage too early:**

1. ⏰ **Time T1**: You run `git add` (files staged)
   - Staging area = snapshot at T1
2. ⏰ **Time T2-T5**: You continue working
   - Update config files
   - Run tests (generates test reports)
   - Update documentation
3. ⏰ **Time T6**: You run `git commit`
   - **Only commits the T1 snapshot**
   - **All work after T1 is MISSING**

**Result: Incomplete, broken atomic commits** ❌

### Correct Atomic Commit Workflow (6 Phases)

**Follow this workflow EXACTLY:**

#### Phase 1: DO ALL WORK FIRST (DO NOT stage anything yet)

- ✅ Complete ALL code changes
- ✅ Run ALL tests and generate test reports
- ✅ Update ALL documentation (CLAUDE.md, tech_stack.md, etc.)
- ✅ Update ALL config files (.claude/settings.local.json, etc.)
- ✅ Update ALL Serena memories
- ✅ Update ALL task plans
- ⚠️ **DO NOT RUN `git add` YET**

#### Phase 2: VERIFY EVERYTHING IS COMPLETE

```bash
git status  # Review ALL changed/new files
git diff    # Review ALL changes
```

- Ensure ALL work is done
- Ensure ALL files are present

#### Phase 3: STAGE EVERYTHING AT ONCE

```bash
git add -A  # Stage ALL files in ONE command
```

- ⚠️ This is the FIRST time you run `git add`
- ⚠️ Stage ALL related files together

#### Phase 4: VERIFY STAGING IMMEDIATELY

```bash
git status  # Verify ALL files staged, NOTHING unstaged
```

- If anything is missing: `git add [missing-file]`

#### Phase 5: COMMIT IMMEDIATELY (within 60 seconds)

```bash
git commit -m "$(cat <<'EOF'
[TAG] Descriptive commit message

- Change 1
- Change 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### Phase 6: PUSH IMMEDIATELY

```bash
git push
```

### What Belongs in an Atomic Commit

**ALL of these must be included together:**

- ✅ Code changes (backend + frontend)
- ✅ Test reports (evidence of passing tests)
- ✅ Documentation updates (CLAUDE.md, README.md, etc.)
- ✅ Memory updates (.serena/memories/)
- ✅ Config changes (.claude/settings.local.json, etc.)
- ✅ Task plan updates (TODO_task_plan.md, etc.)

### ❌ NEVER DO THIS

- ❌ Stage files early during development
- ❌ Stage files "as you go"
- ❌ Run `git add` before ALL work is complete
- ❌ Delay between `git add` and `git commit`
- ❌ Commit without test reports
- ❌ Commit without documentation updates

**Enforcement:** Incomplete commits will be reverted and reworked.

**Commit Types:**

- `[FEAT]`: New feature
- `[FIX]`: Bug fix
- `[REFACTOR]`: Code refactoring
- `[TEST]`: Test changes
- `[DOCS]`: Documentation
- `[CHORE]`: Maintenance
- `[INFRASTRUCTURE]`: Infrastructure changes
- `[SERENA]`: Serena-related changes
- `[TESTING]`: Testing infrastructure changes

## Performance Validation

### 11. Run Performance Checks (Optional but Recommended)

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

### 12. Verify Environment Integrity

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
- [ ] All 27 comprehensive tests pass (100% success rate)
- [ ] Test report generated and path provided
- [ ] Backend health endpoint responds correctly
- [ ] Frontend loads without errors
- [ ] CLAUDE.md updated if needed
- [ ] Memory files updated for significant changes
- [ ] **ALL work complete BEFORE staging**
- [ ] Git commit created with proper atomic workflow
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

### Issue: Incomplete Atomic Commit

**Solution:**

1. DO NOT stage files early
2. Complete ALL work first (code, tests, docs, config)
3. Verify everything is done with `git status` and `git diff`
4. Stage everything at once with `git add -A`
5. Verify staging with `git status`
6. Commit immediately (within 60 seconds)
7. Push immediately

**See `.serena/memories/git_commit_workflow.md` for complete recovery procedures**

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
