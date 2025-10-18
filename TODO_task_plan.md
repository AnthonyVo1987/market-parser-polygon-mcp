# Dead Code Cleanup Implementation Plan - TODO Task Checklist

**Generated:** 2025-10-18
**Based On:** research_task_plan.md (comprehensive codebase audit)
**Status:** Ready for Implementation (Phase 3)
**Task:** Remove all dead code and legacy implementations after React/FastAPI retirement

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE THROUGHOUT IMPLEMENTATION

**YOU MUST systematically use Sequential-Thinking & Serena tools throughout the ENTIRE implementation:**

- **Sequential-Thinking**: Use at START of each phase for systematic approach and complex reasoning
- **Serena Tools**: Use for code analysis, pattern searches, and verification
- **Standard Tools**: Use for file operations (Read, Edit, Write) and bash commands
- **NEVER STOP** using advanced tools unless specific action only supported by Standard Tools

---

## Implementation Phases Overview

| Phase | Description | Tasks | Priority | Tools |
|-------|-------------|-------|----------|-------|
| **0** | Pre-Implementation Setup | 3 tasks | ⭐⭐⭐ CRITICAL | Bash, Sequential-Thinking |
| **1** | Dead Python Code Cleanup | 2 tasks | ⭐ HIGH | Serena, Bash |
| **2** | Orphaned Bytecode Cleanup | 2 tasks | ⭐ HIGH | Bash |
| **3** | Obsolete Config Files Cleanup | 2 tasks | ⭐⭐ MEDIUM | Bash |
| **4** | Obsolete CI Workflow Cleanup | 2 tasks | ⭐⭐ MEDIUM | Bash |
| **5** | Pre-Commit Hook Update | 4 tasks | ⭐⭐ MEDIUM | Read, Edit, Serena |
| **6** | Documentation Updates | 4 tasks | ⭐⭐⭐ LOW | Serena, Read, Edit |
| **7** | **MANDATORY Testing & Validation** | 6 tasks | ⭐⭐⭐ CRITICAL | Bash, Grep |
| **8** | Atomic Git Commit | 6 tasks | ⭐⭐⭐ CRITICAL | Bash |

**Total Tasks:** 31 tasks across 9 phases

---

## ⚠️ CRITICAL PRE-REQUISITES

### Before Starting ANY Implementation:

1. ✅ Ensure you are on the correct git branch (`react_retirement` or create new branch)
2. ✅ Verify working directory is clean (`git status`)
3. ✅ Read research_task_plan.md to understand all findings
4. ✅ Use Sequential-Thinking to plan approach for each phase
5. ✅ **NEVER stage files early** - only stage AFTER all work complete

---

## PHASE 0: Pre-Implementation Setup

### 🎯 **START with Sequential-Thinking for Pre-Implementation Analysis**

**MANDATORY:** Use Sequential-Thinking to:
- Analyze the overall task scope and dependencies
- Plan the execution order and risk mitigation
- Understand the testing strategy
- Confirm understanding of atomic commit workflow

### ✅ **Task 0.1: Run Baseline Test Suite**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Establish baseline that all tests pass BEFORE making any changes

**Commands:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Expected Result:**
- 39/39 tests COMPLETED
- Test report generated: `test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log`
- Save report path for later comparison

**Verification:**
```bash
# Check test completion
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
# Should output: 39
```

**❌ STOP IF:** Any tests fail - investigate and fix before proceeding

---

### ✅ **Task 0.2: Git Status Snapshot**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Verify clean working directory before making changes

**Commands:**
```bash
git status
```

**Expected Result:**
- Working tree clean OR only expected uncommitted changes
- Correct branch (`react_retirement` or new cleanup branch)

**Verification:**
- No unexpected modified files
- No unexpected untracked files

**❌ STOP IF:** Unexpected changes detected - commit or stash before proceeding

---

### ✅ **Task 0.3: Review Research Findings**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Read, Sequential-Thinking

**Purpose:** Understand all dead code identified in research phase

**Commands:**
```bash
# Read the research plan
cat research_task_plan.md | less
```

**Expected Result:**
- Understand 7 categories of dead code
- Understand 8 files to delete (372 lines)
- Understand 2+ files to update
- Understand all __pycache__/ directories to clean

**Verification:**
- Can explain what each file deletion accomplishes
- Can explain why each file is safe to delete

---

## PHASE 1: Dead Python Code Cleanup

### 🎯 **START with Sequential-Thinking for Python Code Cleanup Analysis**

**MANDATORY:** Use Sequential-Thinking to:
- Analyze the __init__.py file structure and imports
- Plan the verification strategy to ensure no active imports
- Understand the risk mitigation for deleting this file

### ✅ **Task 1.1: Verify __init__.py Has No Active Imports**

**Priority:** ⭐ HIGH
**Status:** [ ] Not Started
**Tool:** Serena `search_for_pattern`, Grep

**Purpose:** Confirm no code imports from src/backend/__init__.py

**Commands:**
```bash
# Search for imports using Serena
# Use pattern: "from backend import|from src.backend import|import backend"

# Fallback with grep if needed
grep -r "from backend import" src/
grep -r "from src.backend import" src/
grep -r "import backend" src/
```

**Expected Result:**
- **ZERO** imports found (file is not imported anywhere)
- Search returns empty results

**Verification:**
- No matches found in any .py files
- Safe to delete __init__.py

**❌ STOP IF:** Active imports found - investigate and refactor before deletion

---

### ✅ **Task 1.2: Delete src/backend/__init__.py**

**Priority:** ⭐ HIGH
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Remove dead Python file with obsolete imports

**Commands:**
```bash
rm src/backend/__init__.py
```

**Expected Result:**
- File deleted successfully
- 89 lines of dead code removed

**Verification:**
```bash
ls src/backend/__init__.py
# Should error: No such file or directory
```

**Impact:** Zero functional impact (file not imported)

---

## PHASE 2: Orphaned Bytecode Cleanup

### 🎯 **START with Sequential-Thinking for Bytecode Cleanup Analysis**

**MANDATORY:** Use Sequential-Thinking to:
- Understand why __pycache__ directories exist
- Plan the cleanup strategy for all orphaned bytecode
- Verify the cleanup is comprehensive

### ✅ **Task 2.1: List All __pycache__ Directories**

**Priority:** ⭐ HIGH
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Document all __pycache__ locations before cleanup

**Commands:**
```bash
find . -type d -name "__pycache__" | grep -v node_modules | grep -v .venv
```

**Expected Result:**
- List of all __pycache__/ directories in src/backend/
- Count for commit message documentation

**Verification:**
- Minimum 4 directories found (backend, tools, utils, services)

---

### ✅ **Task 2.2: Delete All __pycache__ Directories**

**Priority:** ⭐ HIGH
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Remove all orphaned bytecode files

**Commands:**
```bash
find . -type d -name "__pycache__" -not -path "./node_modules/*" -not -path "./.venv/*" -exec rm -rf {} +
```

**Expected Result:**
- All __pycache__/ directories deleted
- All orphaned .pyc files removed (api_models, dependencies, main, finnhub_tools)

**Verification:**
```bash
find . -type d -name "__pycache__"
# Should return empty or only node_modules/.venv
```

**Impact:** Negligible disk space recovered, cleaner repository

---

## PHASE 3: Obsolete Config Files Cleanup

### 🎯 **START with Sequential-Thinking for Config Files Analysis**

**MANDATORY:** Use Sequential-Thinking to:
- Understand purpose of each config file being deleted
- Verify no tooling dependencies on these files
- Plan verification strategy post-deletion

### ✅ **Task 3.1: Verify Config Files Exist**

**Priority:** ⭐⭐ MEDIUM
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Confirm all 6 obsolete config files are present

**Commands:**
```bash
ls -la tsconfig.node.json vite-env.d.ts postcss.config.js .prettierrc.cjs lighthouserc.js lighthouserc.cjs
```

**Expected Result:**
- All 6 files found
- Total size ~5KB

**Verification:**
- Each file exists
- Files are in root directory

---

### ✅ **Task 3.2: Delete 6 Obsolete Config Files**

**Priority:** ⭐⭐ MEDIUM
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Remove React/TypeScript tooling configuration files

**Commands:**
```bash
rm tsconfig.node.json vite-env.d.ts postcss.config.js .prettierrc.cjs lighthouserc.js lighthouserc.cjs
```

**Expected Result:**
- 6 files deleted successfully
- ~253 lines of config removed

**Verification:**
```bash
ls -la tsconfig.node.json vite-env.d.ts postcss.config.js .prettierrc.cjs lighthouserc.js lighthouserc.cjs 2>&1 | grep "No such file"
# Should show "No such file or directory" for all 6
```

**Impact:** Zero tooling impact (React removed, Python uses Black)

---

## PHASE 4: Obsolete CI Workflow Cleanup

### 🎯 **START with Sequential-Thinking for CI Workflow Analysis**

**MANDATORY:** Use Sequential-Thinking to:
- Understand the lighthouse-ci.yml workflow purpose
- Verify workflow is disabled and safe to delete
- Plan verification that no other workflows depend on it

### ✅ **Task 4.1: Verify Workflow File Exists**

**Priority:** ⭐⭐ MEDIUM
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Confirm obsolete CI workflow is present

**Commands:**
```bash
ls -la .github/workflows/lighthouse-ci.yml
```

**Expected Result:**
- File found (119 lines)
- References deleted frontend/ directory

**Verification:**
```bash
cat .github/workflows/lighthouse-ci.yml | grep -c "if: false"
# Should output: 2 (workflow is disabled)
```

---

### ✅ **Task 4.2: Delete Lighthouse CI Workflow**

**Priority:** ⭐⭐ MEDIUM
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Remove React frontend CI workflow

**Commands:**
```bash
rm .github/workflows/lighthouse-ci.yml
```

**Expected Result:**
- File deleted successfully
- 119 lines of CI config removed

**Verification:**
```bash
ls -la .github/workflows/
# Should NOT show lighthouse-ci.yml
```

**Impact:** Zero CI impact (workflow was disabled, React removed)

---

## PHASE 5: Pre-Commit Hook Update

### 🎯 **START with Sequential-Thinking for Pre-Commit Hook Analysis**

**MANDATORY:** Use Sequential-Thinking to:
- Understand current pre-commit hook structure
- Plan precise edit to remove ESLint section only
- Verify Python hooks remain intact

### ✅ **Task 5.1: Read Current .pre-commit-config.yaml**

**Priority:** ⭐⭐ MEDIUM
**Status:** [ ] Not Started
**Tool:** Read

**Purpose:** Understand current pre-commit configuration

**Commands:**
```bash
# Use Read tool to view file
```

**Expected Result:**
- File has 3 sections:
  - Python formatting/linting (lines 1-22) ✅ KEEP
  - JavaScript/TypeScript linting (lines 23-36) ❌ REMOVE
  - General file formatting (lines 38-47) ✅ KEEP

**Verification:**
- Identify exact line numbers of ESLint section
- Confirm section matches research findings

---

### ✅ **Task 5.2: Identify ESLint Section**

**Priority:** ⭐⭐ MEDIUM
**Status:** [ ] Not Started
**Tool:** Serena `search_for_pattern`

**Purpose:** Locate ESLint/TypeScript hook section

**Commands:**
```bash
# Use Serena search_for_pattern with "mirrors-eslint"
```

**Expected Result:**
- Pattern found at lines 23-36
- Section includes ESLint, TypeScript, React dependencies

**Verification:**
- Line numbers match research findings (23-36)
- Section starts with "mirrors-eslint"

---

### ✅ **Task 5.3: Remove ESLint/TypeScript Section**

**Priority:** ⭐⭐ MEDIUM
**Status:** [ ] Not Started
**Tool:** Edit

**Purpose:** Remove obsolete JavaScript/TypeScript linting hook

**Commands:**
```bash
# Use Edit tool to remove lines 23-36
# old_string: entire ESLint section (14 lines)
# new_string: empty (delete section)
```

**Expected Result:**
- Lines 23-36 removed
- File reduced from 47 lines to 33 lines
- Python and general hooks remain intact

**Verification:**
```bash
# Verify ESLint section removed
grep -q "mirrors-eslint" .pre-commit-config.yaml
# Should return 1 (not found)

# Verify Python hooks still present
grep -q "psf/black" .pre-commit-config.yaml
# Should return 0 (found)
```

---

### ✅ **Task 5.4: Verify Updated YAML Is Valid**

**Priority:** ⭐⭐ MEDIUM
**Status:** [ ] Not Started
**Tool:** Read, Bash

**Purpose:** Ensure .pre-commit-config.yaml is still valid YAML

**Commands:**
```bash
# Read updated file
# Use Read tool

# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.pre-commit-config.yaml'))"
```

**Expected Result:**
- File reads correctly
- YAML syntax is valid
- Only Python and general hooks present

**Verification:**
- No YAML syntax errors
- File structure intact

---

## PHASE 6: Documentation Updates

### 🎯 **START with Sequential-Thinking for Documentation Analysis**

**MANDATORY:** Use Sequential-Thinking to:
- Analyze scope of documentation updates needed
- Plan which files to update vs. mark as historical
- Prioritize most impactful documentation changes

### ✅ **Task 6.1: Update DEPLOYMENT-QUICKSTART.md**

**Priority:** ⭐⭐⭐ LOW
**Status:** [ ] Not Started
**Tool:** Serena `search_for_pattern`, Read, Edit

**Purpose:** Remove React frontend deployment references

**Commands:**
```bash
# Use Serena search_for_pattern to find "React" or "frontend"
# Use Read to view file
# Use Edit to update/remove React sections
```

**Expected Result:**
- React deployment steps removed
- Focus on Gradio-only deployment
- Updated to reflect current architecture

**Verification:**
```bash
grep -i "react\|frontend" DEPLOYMENT-QUICKSTART.md
# Should return zero or minimal historical references
```

---

### ✅ **Task 6.2: Update .claude/commands/new_task.md**

**Priority:** ⭐⭐⭐ LOW
**Status:** [ ] Not Started
**Tool:** Serena `search_for_pattern`, Read, Edit

**Purpose:** Remove @react-component-architect agent references

**Commands:**
```bash
# Use Serena search_for_pattern to find "react-component-architect"
# Use Read to view file
# Use Edit to remove React agent rows from tables
```

**Expected Result:**
- @react-component-architect references removed
- Agent table updated
- Focus on backend and Python agents

**Verification:**
```bash
grep -i "react-component-architect" .claude/commands/new_task.md
# Should return zero results
```

---

### ✅ **Task 6.3: Update .claude/commands/code_review_commit.md**

**Priority:** ⭐⭐⭐ LOW
**Status:** [ ] Not Started
**Tool:** Serena `search_for_pattern`, Read, Edit

**Purpose:** Remove TypeScript interface validation references

**Commands:**
```bash
# Use Serena search_for_pattern to find "TypeScript"
# Use Read to view file
# Use Edit to remove TypeScript validation steps
```

**Expected Result:**
- TypeScript validation step removed
- Focus on Python code review only

**Verification:**
```bash
grep -i "typescript" .claude/commands/code_review_commit.md
# Should return zero results
```

---

### ✅ **Task 6.4: Quick Audit of Other Documentation**

**Priority:** ⭐⭐⭐ LOW
**Status:** [ ] Not Started
**Tool:** Serena `search_for_pattern`, Bash

**Purpose:** Identify other docs that may need updates

**Commands:**
```bash
# Search all .md files for React/TypeScript references
grep -r -i "react\|typescript" *.md docs/ .serena/memories/ | grep -v "historical\|HISTORICAL\|retired" | head -20
```

**Expected Result:**
- List of files with potential outdated references
- Most should be marked as historical already

**Action:**
- Update critical references
- Mark appropriate files as historical
- Low priority - can be addressed in future commits

---

## PHASE 7: 🔴 MANDATORY Testing & Validation

### ⚠️ CRITICAL CHECKPOINT - DO NOT SKIP ⚠️

**CRITICAL:** You MUST run tests and perform Phase 2 verification BEFORE claiming completion

### 🎯 **START with Sequential-Thinking for Testing Strategy**

**MANDATORY:** Use Sequential-Thinking to:
- Plan comprehensive testing approach
- Understand Phase 2 mandatory verification requirements
- Plan evidence collection for all checkpoint questions

---

### ✅ **Task 7.1: Python Import Verification**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Verify critical modules import successfully after __init__.py deletion

**Commands:**
```bash
uv run python -c "import src.backend.cli; print('✅ CLI imports OK')"
uv run python -c "import src.backend.gradio_app; print('✅ Gradio imports OK')"
uv run python -c "from src.backend.tools import polygon_tools; print('✅ Tools import OK')"
```

**Expected Result:**
- All 3 imports succeed
- Each prints "✅ ... imports OK"
- No ImportError exceptions

**❌ STOP IF:** Any import fails - restore __init__.py and investigate

---

### ✅ **Task 7.2: Pylint Import Error Check**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Verify no import errors detected by pylint

**Commands:**
```bash
uv run pylint src/backend/ --disable=all --enable=import-error
```

**Expected Result:**
- **Score: 10.00/10**
- **No import errors detected**

**Verification:**
```bash
# Should show:
# Your code has been rated at 10.00/10
```

**❌ STOP IF:** Import errors detected - fix before proceeding

---

### ✅ **Task 7.3: Post-Cleanup Full Test Suite (Phase 1)**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Run full CLI regression suite - generate all 39 responses

**Commands:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Expected Result:**
- **39/39 tests COMPLETED** (responses generated)
- Test report generated: `test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log`
- **NOTE:** "39/39 COMPLETED" means responses received, NOT verified correct

**Verification:**
```bash
# Check completion count
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
# Should output: 39
```

**⚠️ IMPORTANT:** Phase 1 does NOT verify correctness - only completion

---

### ✅ **Task 7.4: 🔴 MANDATORY Phase 2 Verification (Error Detection)**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash (Grep)

**Purpose:** MANDATORY grep-based verification of test responses for errors

**🔴 REQUIRED: You MUST run these 3 grep commands and SHOW output:**

**Command 1: Find All Errors/Failures**
```bash
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log
```

**Command 2: Count 'Data Unavailable' Errors**
```bash
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log
```

**Command 3: Count Completed Tests**
```bash
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Expected Result:**
- **Command 1:** Either no output (0 errors) OR list of errors with line numbers
- **Command 2:** Count of "data unavailable" errors (ideally 0)
- **Command 3:** Should output 39 (all tests completed)

**🔴 MANDATORY: Document Results:**

If errors found, create evidence table:

| Test # | Test Name | Line # | Error Message | Tool Call (if visible) |
|--------|-----------|--------|---------------|------------------------|
| X | Test_Name | 123 | error message | tool_call(...) |

**If NO errors:** Explicitly state "✅ 0 failures found - all grep commands returned zero errors"

**❌ CANNOT PROCEED** without running all 3 grep commands and showing output

---

### ✅ **Task 7.5: Phase 2 Checkpoint Questions (MANDATORY)**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Evidence from Task 7.4

**Purpose:** Answer ALL checkpoint questions with evidence

**🔴 REQUIRED: Answer ALL 5 questions with evidence:**

1. ✅ **Did you RUN the 3 mandatory grep commands in Task 7.4?**
   - **Answer:** [YES/NO]
   - **Evidence:** [Paste grep outputs]

2. ✅ **Did you DOCUMENT all failures found (or confirm 0 failures)?**
   - **Answer:** [YES/NO]
   - **Evidence:** [Provide failure table OR "0 failures found"]

3. ✅ **Failure count from `grep -c "data unavailable"`:**
   - **Answer:** [X failures]
   - **Evidence:** [Show grep -c output]

4. ✅ **Tests that generated responses (COMPLETED):**
   - **Answer:** [X/39 COMPLETED]
   - **Evidence:** [Show grep -c "COMPLETED" output]

5. ✅ **Tests that PASSED verification (no errors):**
   - **Answer:** [X/39 PASSED]
   - **Evidence:** [39 minus failure count from Q3]

**🔴 CANNOT MARK TASK COMPLETE WITHOUT:**
- Running and showing grep outputs
- Documenting failures with evidence (or confirming 0 failures)
- Answering all 5 checkpoint questions with evidence

---

### ✅ **Task 7.6: Gradio Startup Verification**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Verify Gradio server starts successfully on port 8000

**Commands:**
```bash
# Start Gradio in background with timeout
timeout 10s uv run python src/backend/gradio_app.py 2>&1 | tee /tmp/gradio_startup.log &
GRADIO_PID=$!

# Wait for startup
sleep 5

# Check if running on port 8000
curl -s http://127.0.0.1:8000 > /dev/null && echo "✅ Gradio running on port 8000" || echo "❌ Gradio not accessible"

# Kill background process
kill $GRADIO_PID 2>/dev/null
```

**Expected Result:**
- "✅ Gradio running on port 8000"
- No startup errors in logs

**Verification:**
```bash
cat /tmp/gradio_startup.log | grep -i error
# Should return zero errors
```

**❌ STOP IF:** Gradio fails to start - investigate errors

---

## PHASE 8: 🔴 Atomic Git Commit Workflow

### ⚠️ CRITICAL: PROPER ATOMIC COMMIT WORKFLOW ⚠️

**DO NOT STAGE FILES EARLY - Stage ONLY immediately before commit**

### 🎯 **START with Sequential-Thinking for Commit Strategy**

**MANDATORY:** Use Sequential-Thinking to:
- Review all changes made during implementation
- Verify ALL work is complete (code, tests, docs)
- Plan atomic commit message structure
- Confirm understanding of proper staging workflow

---

### ✅ **Task 8.1: 🔴 CRITICAL - WAIT - Do NOT Stage Yet**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** None (Checkpoint)

**Purpose:** Ensure ALL work complete before staging

**🔴 VERIFY ALL OF THE FOLLOWING BEFORE PROCEEDING:**

- ✅ All code deletions complete (8 files)
- ✅ All bytecode cleanup complete (__pycache__)
- ✅ All config deletions complete (6 files)
- ✅ All CI workflow deletions complete (1 file)
- ✅ Pre-commit hook updated (ESLint removed)
- ✅ Documentation updated (React/TypeScript references)
- ✅ All tests PASS (Phase 1 + Phase 2 verification complete)
- ✅ Test report generated and saved
- ✅ All 5 checkpoint questions answered with evidence

**⚠️ DO NOT RUN `git add` YET**

**❌ STOP IF:** Any item above is NOT complete

---

### ✅ **Task 8.2: Final Review**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Review ALL changes before staging

**Commands:**
```bash
# Review all changed/deleted files
git status

# Review all changes
git diff
```

**Expected Result:**
- **Deleted files (8):**
  - src/backend/__init__.py
  - tsconfig.node.json
  - vite-env.d.ts
  - postcss.config.js
  - .prettierrc.cjs
  - lighthouserc.js
  - lighthouserc.cjs
  - .github/workflows/lighthouse-ci.yml

- **Modified files (2+):**
  - .pre-commit-config.yaml (ESLint section removed)
  - DEPLOYMENT-*.md (React references updated)
  - .claude/commands/*.md (React agents removed)

- **Untracked files:**
  - test-reports/test_cli_regression_loop1_*.log (NEW test report)

**Verification:**
- All changes look correct
- No unexpected modifications
- Ready to stage

---

### ✅ **Task 8.3: Stage Everything AT ONCE**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Stage ALL changes in ONE command

**Commands:**
```bash
git add -A
```

**⚠️ THIS IS THE FIRST TIME RUNNING `git add`**
**⚠️ ALL changes must be staged together**

**Expected Result:**
- All deletions staged
- All modifications staged
- All new files staged (test reports)

**Verification:**
```bash
git status
# Should show all changes as "Changes to be committed"
```

---

### ✅ **Task 8.4: Verify Staging Immediately**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Confirm ALL files staged, NOTHING unstaged

**Commands:**
```bash
git status
```

**Expected Result:**
- **"Changes to be committed:"** section lists ALL changes
- **"Changes not staged for commit:"** section is EMPTY
- **"Untracked files:"** section is EMPTY (or only temp files)

**Verification:**
- Count of staged files matches expectations (~10-15 files)
- No unstaged changes

**❌ STOP IF:** Any files unstaged - run `git add [missing-file]`

---

### ✅ **Task 8.5: Commit Immediately (Within 60 Seconds)**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash (Heredoc)

**Purpose:** Create atomic commit with comprehensive message

**Commands:**
```bash
git commit -m "$(cat <<'EOF'
[CLEANUP] Remove dead code after React/FastAPI retirement

**Summary:** Comprehensive cleanup of legacy code after migrating to Gradio-only Python full-stack architecture

**Code Deletions:**
- Deleted src/backend/__init__.py (89 lines - imports deleted modules)
- Cleaned all __pycache__/ directories (orphaned bytecode: api_models, dependencies, main, finnhub_tools)

**Config Deletions:**
- Deleted 6 obsolete React/TypeScript config files (253 lines):
  - tsconfig.node.json (TypeScript config)
  - vite-env.d.ts (Vite TypeScript definitions)
  - postcss.config.js (PostCSS for React CSS)
  - .prettierrc.cjs (Prettier for React)
  - lighthouserc.js (Lighthouse CI)
  - lighthouserc.cjs (Lighthouse CI duplicate)

**CI/CD Deletions:**
- Deleted .github/workflows/lighthouse-ci.yml (119 lines - React frontend CI workflow)

**Configuration Updates:**
- Updated .pre-commit-config.yaml (removed ESLint/TypeScript hook - 14 lines)

**Documentation Updates:**
- Updated DEPLOYMENT-QUICKSTART.md (removed React deployment references)
- Updated .claude/commands/new_task.md (removed @react-component-architect)
- Updated .claude/commands/code_review_commit.md (removed TypeScript validation)
- Other documentation cleanups

**Testing & Verification:**
- ✅ Test Suite: 39/39 PASS (100%)
- ✅ Phase 2 Verification: X/39 PASS (grep-based error detection)
- ✅ Python Imports: All modules import successfully
- ✅ Pylint: No import errors (10.00/10)
- ✅ Gradio: Starts successfully on port 8000
- Test Report: test-reports/test_cli_regression_loop1_YYYY-MM-DD_HH-MM.log

**Impact:**
- Files Deleted: 8 files (372 lines of dead code)
- Directories Cleaned: All __pycache__/ (4+ directories)
- Functional Impact: Zero (all dead code, no active dependencies)
- Code Quality: Improved (cleaner codebase, reduced confusion)

**Risk Assessment:** LOW (comprehensive testing, all changes are deletions)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**⚠️ CRITICAL:** Update placeholders in commit message:
- Replace `X/39 PASS` with actual pass count from Phase 2 verification
- Replace `YYYY-MM-DD_HH-MM` with actual test report timestamp

**Expected Result:**
- Commit created successfully
- Comprehensive commit message with all details

**Verification:**
```bash
git log -1 --stat
# Should show commit with all changes
```

---

### ✅ **Task 8.6: Push Immediately**

**Priority:** ⭐⭐⭐ CRITICAL
**Status:** [ ] Not Started
**Tool:** Bash

**Purpose:** Push commit to remote repository

**Commands:**
```bash
git push
```

**Expected Result:**
- Commit pushed successfully to `origin/react_retirement` (or current branch)
- Remote updated

**Verification:**
```bash
git status
# Should show: Your branch is up to date with 'origin/...'
```

**✅ IMPLEMENTATION COMPLETE** when push succeeds

---

## Success Criteria

### ✅ All Tasks Complete When:

1. ✅ All 8 files deleted (372 lines)
2. ✅ All __pycache__/ directories cleaned
3. ✅ Pre-commit config updated (ESLint removed)
4. ✅ Documentation updated (React/TypeScript references)
5. ✅ **Phase 1 Tests:** 39/39 COMPLETED (responses generated)
6. ✅ **Phase 2 Verification:** All 3 grep commands run and documented
7. ✅ **Checkpoint Questions:** All 5 questions answered with evidence
8. ✅ **Test Pass Count:** X/39 PASS (documented with evidence)
9. ✅ Python imports verified (no errors)
10. ✅ Pylint clean (10.00/10)
11. ✅ Gradio starts successfully
12. ✅ Atomic commit created and pushed

---

## Risk Mitigation

### Rollback Strategy (If Needed)

If any critical issues arise:

```bash
# Restore deleted files from git
git checkout HEAD -- src/backend/__init__.py
git checkout HEAD -- tsconfig.node.json vite-env.d.ts postcss.config.js .prettierrc.cjs lighthouserc.js lighthouserc.cjs
git checkout HEAD -- .github/workflows/lighthouse-ci.yml

# Restore pre-commit config
git checkout HEAD -- .pre-commit-config.yaml

# Clean staged changes
git reset HEAD
```

---

## Notes for Implementation

### Tool Usage Patterns:

- **Sequential-Thinking:** Start of each phase for systematic approach
- **Serena Tools:** Code analysis, pattern searches, verification
- **Standard Read:** Inspect files before editing
- **Standard Edit:** Precise file modifications
- **Bash:** File operations, testing, git commands

### Common Pitfalls to Avoid:

1. ❌ Staging files early during development
2. ❌ Skipping Phase 2 verification
3. ❌ Not answering all 5 checkpoint questions
4. ❌ Claiming tests "PASS" without grep verification
5. ❌ Committing without test reports
6. ❌ Delay between staging and committing

### Remember:

- **"39/39 COMPLETED" ≠ "39/39 PASSED"**
- Only Phase 2 verification proves correctness
- Must run all 3 grep commands and show output
- Must answer all 5 checkpoint questions with evidence
- Must document failures OR confirm 0 failures

---

**Implementation Plan Complete**
**Status:** Ready for Phase 3 (Implementation)
**Next Step:** Begin with Task 0.1 (Pre-Implementation Setup)

---

*Generated by: Claude Code (Sonnet 4.5) using Sequential-Thinking*
*Based on: research_task_plan.md (comprehensive audit findings)*
*Date: 2025-10-18*
*Total Tasks: 31 tasks across 9 phases*
*Estimated Time: 2-3 hours*
