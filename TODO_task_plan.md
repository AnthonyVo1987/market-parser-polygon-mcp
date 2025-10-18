# TODO Task Plan: Gradio Port Migration (7860 → 8000)

**Date:** October 18, 2025
**Status:** Implementation Ready
**Based on:** research_task_plan.md

---

## 🎯 Mission

Migrate Gradio web interface from port 7860 to port 8000 for AWS deployment compatibility.

**Scope:** 1 code file (2 lines) + 17 documentation files

---

## 📋 Task Checklist Overview

- [ ] **Phase 0:** Pre-Implementation Verification (3 tasks)
- [ ] **Phase 1:** Code Changes (2 tasks)
- [ ] **Phase 2:** Documentation Updates (17 tasks)
- [ ] **Phase 3:** Testing & Validation (6 tasks) 🔴 MANDATORY
- [ ] **Phase 4:** Final Verification (3 tasks)
- [ ] **Phase 5:** Atomic Commit & Push (6 tasks)

**Total Tasks:** 37

---

## 🚨 MANDATORY TOOL USAGE

**YOU MUST use Sequential-Thinking and Serena tools throughout ALL phases:**

- ✅ **Sequential-Thinking:** Use for planning, analysis, and complex reasoning at EVERY phase
- ✅ **Serena Tools:** Use for code analysis, symbol searches, and pattern matching
- ✅ **Task Agent:** Use for parallel documentation updates
- ✅ **Standard Tools:** Use for file operations and git commands

**VIOLATION = TASK FAILURE**

---

## Phase 0: Pre-Implementation Verification

### 0.1: Verify Port Availability

**Commands:**
```bash
netstat -tlnp 2>/dev/null | grep -E ":(7860|8000)" || echo "✅ Ports available"
```

**Expected Output:**
```
✅ Ports available
```

**Checkpoint:** Both ports 7860 and 8000 must be free

---

### 0.2: Create Backup Tag

**Command:**
```bash
git tag -a backup-before-port-migration -m "Backup before Gradio port 7860→8000 migration"
```

**Verification:**
```bash
git tag -l | grep backup-before-port-migration
```

**Expected Output:**
```
backup-before-port-migration
```

**Checkpoint:** Backup tag created successfully

---

### 0.3: Verify Git Clean State

**Command:**
```bash
git status --short
```

**Expected Output:**
```
M TODO_task_plan.md
?? research_task_plan.md
```

**Checkpoint:** Only expected files (task plans) should be modified/untracked

---

## Phase 1: Code Changes (gradio_app.py)

### 1.1: Update Print Statement (Line 100)

**Tool:** Edit

**File:** `src/backend/gradio_app.py`

**Change:**
```python
# OLD:
print("📍 Server: http://127.0.0.1:7860")

# NEW:
print("📍 Server: http://127.0.0.1:8000")
```

**Verification:**
```bash
grep "Server: http://127.0.0.1:8000" src/backend/gradio_app.py
```

**Expected Output:**
```python
print("📍 Server: http://127.0.0.1:8000")
```

**Checkpoint:** Print statement updated to show port 8000

---

### 1.2: Update server_port Parameter (Line 107)

**Tool:** Edit

**File:** `src/backend/gradio_app.py`

**Change:**
```python
# OLD:
server_port=7860,  # Gradio default port (separate from FastAPI:8000, React:3000)

# NEW:
server_port=8000,  # AWS deployment port (unified with previous FastAPI port)
```

**Verification:**
```bash
grep "server_port=8000" src/backend/gradio_app.py
```

**Expected Output:**
```python
server_port=8000,  # AWS deployment port (unified with previous FastAPI port)
```

**Checkpoint:** server_port parameter updated to 8000

---

## Phase 2: Documentation Updates (17 files)

**Strategy:** Use Task agent for parallel updates to maximize speed

### 2.1: Update CLAUDE.md (9 references)

**Pattern:** Replace all instances of:
- `7860` → `8000`
- `http://127.0.0.1:7860` → `http://127.0.0.1:8000`
- `http://localhost:7860` → `http://localhost:8000`

**Preserve:** Historical references (e.g., "was 7860, now 8000")

---

### 2.2: Update README.md (5 references)

**Same pattern as CLAUDE.md**

---

### 2.3: Update AGENTS.md (8 references)

**Same pattern as CLAUDE.md**

---

### 2.4: Update package.json (2 references - npm scripts)

**Lines to update:**
```json
// OLD:
"status": "echo '=== Gradio UI Status ===' && (curl -s http://localhost:7860 > /dev/null && echo 'Gradio UI running on http://localhost:7860' || echo 'Gradio UI not running')",

// NEW:
"status": "echo '=== Gradio UI Status ===' && (curl -s http://localhost:8000 > /dev/null && echo 'Gradio UI running on http://localhost:8000' || echo 'Gradio UI not running')",
```

---

### 2.5: Update docs/PROJECT_ENVIRONMENT_SETUP_GUIDE.md (6 references)

**Same pattern as CLAUDE.md**

---

### 2.6-2.16: Update Serena Memory Files (11 files)

**Files:**
1. `.serena/memories/project_architecture.md` (12 references)
2. `.serena/memories/react_retirement_completion_oct_2025.md` (17 references)
3. `.serena/memories/fastapi_removal_completion_oct_2025.md` (13 references)
4. `.serena/memories/SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE.md` (11 references)
5. `.serena/memories/task_completion_checklist.md` (2 references)
6. `.serena/memories/project_onboarding_summary.md` (6 references)
7. `.serena/memories/suggested_commands.md` (7 references)
8. `.serena/memories/ui_refactor_oct_2025.md` (2 references)
9. `.serena/memories/adaptive_formatting_guide.md` (1 reference)

**Pattern:** Same as CLAUDE.md (replace all port references)

**Note:** Create new Serena memory: `port_migration_to_8000_oct_2025.md` documenting this change

---

### 2.17: Verification - All Documentation Updated

**Command:**
```bash
grep -r "7860" --include="*.md" --include="*.json" src/ docs/ *.md .serena/memories/ package.json 2>/dev/null | wc -l
```

**Expected Output:**
```
0
```

**Checkpoint:** All port 7860 references updated to 8000 (except in historical context)

---

## Phase 3: Testing & Validation 🔴 MANDATORY

### 3.1: 🔴 CRITICAL - Test Gradio Launch (MUST PASS FIRST)

**Command:**
```bash
timeout 30 uv run python src/backend/gradio_app.py &
sleep 5
curl -s http://127.0.0.1:8000 | head -5
pkill -f "gradio_app.py"
```

**Expected Output:**
```
🚀 Initializing Market Parser Gradio Interface...
✅ Agent initialized successfully

============================================================
🎨 Market Parser Gradio Interface
============================================================
📍 Server: http://127.0.0.1:8000
📖 Docs: See research_task_plan.md for details
🔄 Hot Reload: Use 'gradio src/backend/gradio_app.py'
============================================================

Running on local URL: http://127.0.0.1:8000
```

**Success Criteria:**
- ✅ No OSError about port conflicts
- ✅ Server starts on port 8000 (NOT 7860)
- ✅ Web interface accessible at http://127.0.0.1:8000
- ✅ Curl returns HTML content

**🔴 BLOCKING CHECKPOINT:**
- **IF GRADIO FAILS:** STOP HERE - DO NOT proceed to CLI testing
- **IF GRADIO PASSES:** Continue to CLI testing

---

### 3.2: Run CLI Regression Tests (ONLY if Gradio passed)

**Command:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Expected Output:**
```
✅ CLI session completed
⏱️  Total Session Duration: 6 min 8 sec

📊 Test Results Analysis
========================
Total Tests: 39
✅ Completed: 39
❌ Incomplete: 0
Generation Rate: 100%
Average Response Time: 9.41s
📈 Overall Performance Rating: EXCELLENT
```

**Checkpoint:** 39/39 tests generate responses

---

### 3.3: Phase 2a - Error Detection (MANDATORY Grep Commands)

**Command 1:**
```bash
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log | tail -20
```

**Expected Output:** (empty or no critical errors)

**Command 2:**
```bash
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log
```

**Expected Output:**
```
0
```

**Command 3:**
```bash
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Expected Output:**
```
40
```

**Checkpoint:** Show grep output as evidence

---

### 3.4: Phase 2b - Document Failures (if any found)

**IF errors found in Phase 2a:**
- Create failure table with test number, line number, error message
- Document root cause
- Fix and re-test

**IF no errors:**
- Confirm: "✅ 0 failures found"

**Checkpoint:** Either show failure table OR confirm 0 failures

---

### 3.5: Phase 2c - Verify Response Correctness

**For tests without errors, verify:**
1. ✅ Response addresses the prompt query
2. ✅ Correct ticker symbols used
3. ✅ Appropriate tool calls made
4. ✅ Data formatting correct
5. ✅ No hallucinated data
6. ✅ Response complete (not truncated)

**Checkpoint:** Manual verification of sample responses

---

### 3.6: Phase 2d - Final Test Verification

**Answer ALL checkpoint questions:**

1. Did you RUN the 3 mandatory grep commands? **YES/NO + show output**
2. Did you DOCUMENT failures OR confirm 0 failures? **YES/NO + evidence**
3. Failure count from grep -c "data unavailable": **X failures**
4. Tests that generated responses: **X/39 COMPLETED**
5. Tests that PASSED verification: **X/39 PASSED**

**Checkpoint:** All 5 questions answered with evidence

**🔴 ENFORCEMENT:**
- Cannot proceed to Phase 4 without Phase 2d evidence
- Cannot claim task complete without test results
- Test failures must be fixed and re-tested

---

## Phase 4: Final Verification

### 4.1: Grep for Remaining Port 7860 References

**Command:**
```bash
grep -r "7860" --include="*.py" --include="*.md" --include="*.json" src/ docs/ *.md .serena/memories/ package.json 2>/dev/null || echo "✅ No remaining references"
```

**Expected Output:**
```
✅ No remaining references
```

**Note:** Exclude historical references in memory files (acceptable)

**Checkpoint:** No active code/config references to port 7860

---

### 4.2: Verify Gradio Accessible on Port 8000

**Command:**
```bash
curl -s http://127.0.0.1:8000 | grep -i "gradio\|market" | head -3
```

**Expected Output:** HTML content with Gradio/Market Parser references

**Checkpoint:** Web interface responding on port 8000

---

### 4.3: Review All Modified Files

**Command:**
```bash
git status --short
```

**Expected Files:**
- M src/backend/gradio_app.py
- M CLAUDE.md
- M README.md
- M AGENTS.md
- M package.json
- M docs/PROJECT_ENVIRONMENT_SETUP_GUIDE.md
- M .serena/memories/*.md (11 files)
- A .serena/memories/port_migration_to_8000_oct_2025.md
- M TODO_task_plan.md
- M research_task_plan.md
- A test-reports/test_cli_regression_loop1_*.log

**Checkpoint:** All expected files present, no unexpected changes

---

## Phase 5: Atomic Commit & Push

### 5.1: Complete ALL Work FIRST (DO NOT stage yet)

**Checklist:**
- ✅ Code changes complete (gradio_app.py)
- ✅ Documentation updates complete (17 files)
- ✅ Tests run and passed (39/39)
- ✅ Test reports generated
- ✅ Task plans updated
- ✅ New Serena memory created

**⚠️ DO NOT RUN `git add` YET**

**Checkpoint:** ALL work is 100% complete

---

### 5.2: Verify Everything Complete

**Commands:**
```bash
git status  # Review ALL changed/new files
git diff src/backend/gradio_app.py | head -20  # Verify code changes
```

**Checkpoint:** Review output, ensure everything is ready

---

### 5.3: Stage Everything at Once

**Command:**
```bash
git add -A  # Stage ALL files in ONE command
```

**⚠️ This is the FIRST time running `git add`**

**Checkpoint:** All files staged in single operation

---

### 5.4: Verify Staging Immediately

**Command:**
```bash
git status --short
```

**Expected:** All files should show "M" or "A" in first column, NOTHING unstaged

**Checkpoint:** All files staged, nothing left unstaged

---

### 5.5: Commit Immediately (within 60 seconds)

**Command:**
```bash
git commit -m "$(cat <<'EOF'
[PORT] Migrate Gradio from port 7860 to 8000 for AWS deployment

**Problem:** Gradio configured for port 7860, need port 8000 for AWS deployment
**Requirement:** Use standard port 8000 for AWS cloud deployment compatibility

**Solution:** Update Gradio port configuration from 7860 → 8000

**Code Changes:**
- src/backend/gradio_app.py (lines 100, 107):
  - Print statement: http://127.0.0.1:7860 → http://127.0.0.1:8000
  - server_port: 7860 → 8000
  - Updated comment: "AWS deployment port (unified with previous FastAPI port)"

**Documentation Updates (17 files):**
- CLAUDE.md, README.md, AGENTS.md
- package.json (npm status script)
- docs/PROJECT_ENVIRONMENT_SETUP_GUIDE.md
- All 11 Serena memory files
- Created: .serena/memories/port_migration_to_8000_oct_2025.md

**Testing Results:**
✅ Gradio Launch Test: PASSED
- Server starts on http://127.0.0.1:8000
- No port conflicts
- Web interface accessible

✅ CLI Regression Tests: 39/39 PASSED (100%)
- Tests completed: 39/39 COMPLETED
- Average response time: 9.41s (EXCELLENT)
- Phase 2 verification: 0 errors found
- Test report: test-reports/test_cli_regression_loop1_*.log

**Success Metrics:**
- ✅ Port migration: 100% SUCCESS
- ✅ Code changes: 1 file, 2 lines
- ✅ Documentation updates: 17 files
- ✅ Gradio launch: WORKING on port 8000
- ✅ CLI tests: 39/39 PASSED (100%)
- ✅ Zero errors: 0 data unavailable errors

**AWS Deployment Ready:**
- Port 8000 configured for cloud deployment
- Unified port strategy (no longer split across 7860/8000)
- Standard HTTP service port for AWS

**Files Changed:**
- Code: 1 file (gradio_app.py)
- Documentation: 17 files
- Serena Memories: 11 updated + 1 new
- Test Reports: 1 new
- Total: 30 files

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Checkpoint:** Commit created with comprehensive message

---

### 5.6: Push Immediately

**Command:**
```bash
git push
```

**Expected Output:**
```
To https://github.com/AnthonyVo1987/market-parser-polygon-mcp.git
   xxxxxxx..yyyyyyy  react_retirement -> react_retirement
```

**Checkpoint:** Changes pushed to remote successfully

---

## ✅ Task Completion Checklist

**ALL of the following MUST be checked:**

- [ ] Phase 0: Pre-verification complete (ports available, backup tag, git clean)
- [ ] Phase 1: Code changes complete (gradio_app.py updated)
- [ ] Phase 2: Documentation updated (17 files)
- [ ] Phase 3: Gradio launch test PASSED on port 8000
- [ ] Phase 3: CLI regression tests PASSED (39/39)
- [ ] Phase 3: Phase 2 grep verification complete (0 errors)
- [ ] Phase 4: Final verification complete (no remaining 7860 references)
- [ ] Phase 5: Atomic commit created and pushed
- [ ] Test report generated and saved
- [ ] All evidence shown to user

**🔴 TASK IS NOT COMPLETE UNTIL ALL BOXES CHECKED**

---

## 📊 Success Criteria

**Code:**
- ✅ gradio_app.py lines 100 & 107 updated
- ✅ Port 8000 configured correctly
- ✅ No syntax errors

**Documentation:**
- ✅ All 17 files updated
- ✅ All port 7860 references changed to 8000
- ✅ New Serena memory created

**Testing:**
- ✅ Gradio launches on port 8000 without errors
- ✅ 39/39 CLI tests PASS
- ✅ 0 data unavailable errors
- ✅ Phase 2 verification complete

**Commit:**
- ✅ All changes staged together
- ✅ Comprehensive commit message
- ✅ Pushed to remote

---

## 🎯 Final Summary

**Task:** Migrate Gradio port 7860 → 8000
**Scope:** 1 code file + 17 documentation files
**Status:** Implementation Ready
**Next:** Execute all phases systematically using Sequential-Thinking + Serena tools

**🔴 REMEMBER:**
- Use Sequential-Thinking at EVERY phase
- Test Gradio BEFORE CLI testing
- Show Phase 2 verification evidence
- Follow atomic commit workflow exactly
