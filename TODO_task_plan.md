# TODO Task Plan: Legacy Feature Cleanup Implementation

**Created**: 2025-10-06
**Task**: Remove 4 legacy deprecated features from entire codebase
**Research Document**: RESEARCH_FINDINGS_LEGACY_CLEANUP.md

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE THROUGHOUT ALL PHASES

**You MUST use ALL available tools AS OFTEN AS NEEDED throughout implementation:**

- ✅ Sequential-Thinking: For analysis, planning, and complex reasoning at EVERY phase
- ✅ Serena Tools: For code symbol manipulation, pattern search, and memory updates
- ✅ Standard Read/Write/Edit: For file modifications and verification
- ✅ NEVER stop using tools - continue until task completion

---

## Implementation Overview

**Total Tasks**: 4 legacy feature removals
**Files to Delete**: 1 (system.py)
**Files to Modify**: 5-7 (api_models, main, routers/__init__, performance.tsx, response_utils, docs)
**Docs to Update**: 3-4 (CLAUDE.md, AGENTS.md, api-integration-guide.md, README.md)
**Estimated Risk**: LOW
**Expected Performance Gain**: 1-2% CPU reduction

---

## PHASE 1: Backend Cleanup (Tasks 2 & 3)

### ✅ TASK 1.1: Delete system.py Router File

**Status**: ⏸️ PENDING

**Action**:
```bash
rm src/backend/routers/system.py
```

**Impact**:
- Removes /api/v1/system/status endpoint (Task 2)
- Removes prompt_templates_loaded=0 usage (Task 3 partial)

**Verification**: File no longer exists

**Tool Usage**: Standard Bash

---

### ✅ TASK 1.2: Update api_models.py - Remove 3 Classes + 1 Field

**Status**: ⏸️ PENDING

**Actions**:

1. **Remove docstring reference** (Line 5):
   - Find: "for the FastAPI endpoints that expose PromptTemplateManager functionality."
   - Replace with: "for the FastAPI endpoints."

2. **Remove SystemMetrics class** (Lines 64-70):
   - Entire class deletion including:
     - `api_version: str`
     - `prompt_templates_loaded: int`
     - `supported_analysis_types: List[str]`
     - `uptime_seconds: Optional[float]`

3. **Remove SystemStatusResponse class** (Lines 72-75):
   - Entire class deletion

**Verification**:
```bash
# Should return no results
grep -n "SystemMetrics\|SystemStatusResponse\|PromptTemplate" src/backend/api_models.py
```

**Tool Usage**: Serena find_symbol + delete_lines OR Standard Edit tool

---

### ✅ TASK 1.3: Update main.py - Remove Router Registration

**Status**: ⏸️ PENDING

**Actions**:

1. **Find router import**:
   - Search for: `from backend.routers import system_router` OR `system`

2. **Remove import line**:
   - Delete the import statement

3. **Remove router registration**:
   - Search for: `app.include_router(system_router`
   - Delete the registration line

**Verification**:
```bash
# Should return no results
grep -n "system_router\|system.router" src/backend/main.py
```

**Tool Usage**: Serena search_for_pattern + Standard Edit

---

### ✅ TASK 1.4: Update routers/__init__.py - Remove Export

**Status**: ⏸️ PENDING

**Actions**:

1. **Find system router export**:
   - Search for: `from .system import router as system_router`

2. **Remove export line**:
   - Delete the export statement

**Verification**:
```bash
# Should return no results
grep -n "system" src/backend/routers/__init__.py
```

**Tool Usage**: Standard Read + Edit

---

## PHASE 2: Frontend Cleanup (Task 1)

### ✅ TASK 2.1: Remove CSS Analysis Function from performance.tsx

**Status**: ⏸️ PENDING

**Actions**:

1. **Use Serena to find analyzeCSSPerformance function**:
   ```
   mcp__serena__find_symbol(name_path="analyzeCSSPerformance", relative_path="src/frontend/utils/performance.tsx")
   ```

2. **Locate exact line range** for function body

3. **Remove entire function** using Serena delete_symbol OR delete_lines

4. **Find all calls** to analyzeCSSPerformance:
   ```
   mcp__serena__find_referencing_symbols(name_path="analyzeCSSPerformance", relative_path="src/frontend/utils/performance.tsx")
   ```

5. **Remove function calls** from ChatInterface_OpenAI.tsx (if any)

**Verification**:
```bash
# Should return no results
grep -rn "analyzeCSSPerformance" src/frontend/
```

**Tool Usage**: Serena find_symbol + find_referencing_symbols + delete operations

---

## PHASE 3: CLI Cleanup (Task 4)

### ✅ TASK 3.1: Remove All Emojis from response_utils.py

**Status**: ⏸️ PENDING

**Actions**:

1. **Use Serena to get print_response function**:
   ```
   mcp__serena__find_symbol(name_path="print_response", relative_path="src/backend/utils/response_utils.py", include_body=true)
   ```

2. **Remove/update the following**:
   - Line 10: Change docstring from "with emoji support" → "for CLI output"
   - Line 11: Remove ✅ emoji from success message
   - Line 25: Remove comment "better emoji support"
   - Line 30: Remove 📊 emoji from "Performance Metrics"
   - Line 33: Remove ⏱️ emoji from "Response Time"
   - Line 50: Remove 🔢 emoji from "Tokens Used"
   - Line 56/58: Remove 🤖 emoji from "Model"
   - Line 64: Remove comment about emoji

3. **Clean replacements**:
   ```python
   # Before: "[bold green]✅ Query processed successfully![/bold green]"
   # After:  "[bold green]Query processed successfully![/bold green]"

   # Before: "[bold cyan]📊 Performance Metrics:[/bold cyan]"
   # After:  "[bold cyan]Performance Metrics:[/bold cyan]"

   # Before: "⏱️  Response Time:"
   # After:  "Response Time:"

   # Before: "🔢  Tokens Used:"
   # After:  "Tokens Used:"

   # Before: "🤖  Model:"
   # After:  "Model:"
   ```

**Verification**:
```bash
# Should return no emoji characters
grep -n "✅\|📊\|⏱️\|🔢\|🤖" src/backend/utils/response_utils.py
```

**Tool Usage**: Serena find_symbol + replace_symbol_body OR Standard Edit with regex

---

## PHASE 4: Documentation Cleanup

### ✅ TASK 4.1: Update CLAUDE.md - Remove prompt_templates.py Reference

**Status**: ⏸️ PENDING

**Actions**:

1. **Find reference** (Line 429):
   ```
   │   └── prompt_templates.py # Analysis templates
   ```

2. **Remove the line** from project structure

**Verification**:
```bash
grep -n "prompt_template" CLAUDE.md
# Should return 0 results
```

**Tool Usage**: Standard Read + Edit

---

### ✅ TASK 4.2: Update AGENTS.md - Remove prompt_templates.py Reference

**Status**: ⏸️ PENDING

**Actions**:

1. **Check if AGENTS.md has same reference** (likely same structure as CLAUDE.md)

2. **Remove line** if found

**Verification**:
```bash
grep -n "prompt_template" AGENTS.md
# Should return 0 results
```

**Tool Usage**: Standard Read + Edit

---

### ✅ TASK 4.3: Clean docs/api/api-integration-guide.md - Remove ALL PromptTemplate Docs

**Status**: ⏸️ PENDING

**Actions**:

1. **Find all PromptTemplate sections** (Lines 173-587+):
   - Section: "PromptTemplateManager Integration"
   - Section: "PromptTemplate API"
   - Section: "Frontend Template Integration"
   - Section: "Caching Implementation"
   - Section: "Mock API Responses"

2. **Remove entire sections** referencing:
   - PromptTemplateManager class
   - PromptTemplate schema
   - PromptTemplatesResponse
   - /api/v1/prompts/templates endpoint
   - Emoji field in template schema (lines 203, 819, 833)

3. **This is a LARGE documentation cleanup** - consider:
   - Option A: Delete entire file (if ALL content is about PromptTemplates)
   - Option B: Remove only PromptTemplate-related sections

**Verification**:
```bash
grep -n "PromptTemplate\|prompt_template\|emoji" docs/api/api-integration-guide.md
# Should return 0 results
```

**Tool Usage**: Standard Read + Edit (large-scale edits)

---

### ✅ TASK 4.4: Update README.md - Verify No References

**Status**: ⏸️ PENDING

**Actions**:

1. **Search for any references**:
   ```bash
   grep -n "prompt_template\|PromptTemplate\|emoji\|CSS analysis\|system/status" README.md
   ```

2. **Remove if found**, otherwise skip

**Verification**: No references found in README.md

**Tool Usage**: Standard Grep + Edit if needed

---

## PHASE 5: CLI Testing (MANDATORY)

### ✅ TASK 5.1: Run Comprehensive CLI Test Suite

**Status**: ⏸️ PENDING

**Actions**:

1. **Execute test suite**:
   ```bash
   ./CLI_test_regression.sh
   ```

2. **Verify results**:
   - ✅ All 27 tests PASS
   - ✅ 100% success rate
   - ✅ Response times within normal range (4-17 seconds)
   - ✅ No errors or failures

3. **If failures occur**:
   - Analyze failure logs
   - Fix issues
   - Re-run tests until 100% pass

4. **Generate test report**:
   - Test report saved in: `test-reports/cli_regression_test_loop*_YYYYMMDD_HHMMSS.txt`

**Success Criteria**:
- 27/27 tests PASS
- Test report generated
- Evidence shown to user

**Tool Usage**: Standard Bash

---

### ✅ TASK 5.2: Manual CLI Verification (Optional but Recommended)

**Status**: ⏸️ PENDING

**Actions**:

1. **Test CLI manually**:
   ```bash
   uv run src/backend/main.py
   ```

2. **Enter test query**: "Tesla stock analysis"

3. **Verify output**:
   - ✅ Response generated successfully
   - ✅ No emoji characters in output (Task 4 verification)
   - ✅ Performance metrics still displayed
   - ✅ No errors or warnings

**Tool Usage**: Standard Bash

---

### ✅ TASK 5.3: Manual Web UI Verification (Optional but Recommended)

**Status**: ⏸️ PENDING

**Actions**:

1. **Start application**:
   ```bash
   ./start-app-xterm.sh
   ```

2. **Open browser**: http://127.0.0.1:3000

3. **Test query**: "AAPL stock analysis"

4. **Verify UI**:
   - ✅ Query processes successfully
   - ✅ Performance metrics displayed
   - ✅ No CSS analysis overhead (1-2% CPU reduction)
   - ✅ No errors in console

**Tool Usage**: Standard Bash + Manual browser testing

---

## PHASE 6: Serena Memory Updates

### ✅ TASK 6.1: Update tech_stack.md Memory

**Status**: ⏸️ PENDING

**Actions**:

1. **Read current memory**:
   ```
   mcp__serena__read_memory(memory_file_name="tech_stack.md")
   ```

2. **Search for references** to:
   - PromptTemplateManager
   - SystemMetrics with prompt_templates_loaded
   - CSS performance analysis
   - Emoji support

3. **Update or remove** outdated sections

4. **Add cleanup notes**:
   ```markdown
   **Legacy Features Removed (Oct 2025)**:
   - CSS performance analysis (high overhead, minimal value)
   - /api/v1/system/status endpoint (unused)
   - Prompt Template system remnants (already deprecated)
   - Emoji in CLI responses (cosmetic feature)
   ```

**Tool Usage**: Serena read_memory + write_memory

---

### ✅ TASK 6.2: Update project_architecture.md Memory

**Status**: ⏸️ PENDING

**Actions**:

1. **Read current memory**:
   ```
   mcp__serena__read_memory(memory_file_name="project_architecture.md")
   ```

2. **Remove references** to:
   - system.py router
   - PromptTemplate system
   - CSS analysis function
   - Emoji functionality

3. **Update architecture diagrams** if they reference removed components

**Tool Usage**: Serena read_memory + write_memory

---

### ✅ TASK 6.3: Update code_style_conventions.md Memory (If Needed)

**Status**: ⏸️ PENDING

**Actions**:

1. **Check for references**:
   ```
   mcp__serena__read_memory(memory_file_name="code_style_conventions.md")
   ```

2. **Remove emoji guidelines** if present

**Tool Usage**: Serena read_memory + write_memory (if needed)

---

## PHASE 7: Update CLAUDE.md Last Completed Task

### ✅ TASK 7.1: Update Last Completed Task Section

**Status**: ⏸️ PENDING

**Actions**:

1. **Read CLAUDE.md** LAST_COMPLETED_TASK section

2. **Replace with new summary**:
   ```markdown
   [CLEANUP] Remove legacy deprecated features from entire codebase

   **Primary Changes:**

   1. **CSS Analysis Removal**: Removed high-overhead CSS performance analysis
   2. **System Status Endpoint Removal**: Deleted unused /api/v1/system/status endpoint
   3. **Prompt Template Cleanup**: Removed all remnants of deprecated PromptTemplate system
   4. **Emoji Removal**: Cleaned emoji characters from CLI responses

   **Backend Changes:**

   - **Deleted**: `src/backend/routers/system.py` (entire file - unused endpoint)
   - **api_models.py**: Removed SystemMetrics, SystemStatusResponse classes + prompt_templates_loaded field
   - **main.py**: Removed system_router registration
   - **routers/__init__.py**: Removed system_router export
   - **response_utils.py**: Removed all emoji characters from CLI output formatting

   **Frontend Changes:**

   - **performance.tsx**: Removed analyzeCSSPerformance() function (HIGH overhead - 1-2% CPU)

   **Documentation Changes:**

   - **CLAUDE.md**: Removed prompt_templates.py reference from project structure
   - **AGENTS.md**: Removed prompt_templates.py reference from project structure
   - **docs/api/api-integration-guide.md**: Removed extensive legacy PromptTemplate documentation

   **Test Results:**

   - **Total Tests**: 27/27 PASSED ✅
   - **Success Rate**: 100%
   - **Average Response Time**: [ACTUAL VALUE]s
   - **Test Report**: `cli_regression_test_loop*_YYYYMMDD_HHMMSS.txt`

   **Performance Improvements:**

   - ✅ CSS analysis overhead eliminated (1-2% CPU reduction)
   - ✅ Codebase simplified and more maintainable
   - ✅ Documentation now accurate and up-to-date

   **Files Changed:**

   - ❌ Deleted: `src/backend/routers/system.py`
   - ✅ Modified: `src/backend/api_models.py` (removed 3 classes)
   - ✅ Modified: `src/backend/main.py` (removed router registration)
   - ✅ Modified: `src/backend/routers/__init__.py` (removed export)
   - ✅ Modified: `src/backend/utils/response_utils.py` (emoji cleanup)
   - ✅ Modified: `src/frontend/utils/performance.tsx` (removed CSS analysis)
   - ✅ Modified: `CLAUDE.md` (updated structure)
   - ✅ Modified: `AGENTS.md` (updated structure)
   - ✅ Modified: `docs/api/api-integration-guide.md` (removed legacy docs)
   - ✅ Updated: `.serena/memories/tech_stack.md`
   - ✅ Updated: `.serena/memories/project_architecture.md`

   **Total**: 1 file deleted, 10 files modified, 2 Serena memories updated
   ```

**Tool Usage**: Standard Read + Edit

---

## PHASE 8: Final Git Commit (ATOMIC WORKFLOW)

### ✅ TASK 8.1: Verify All Work Complete

**Status**: ⏸️ PENDING

**Actions**:

1. **Review all changes**:
   ```bash
   git status
   git diff
   ```

2. **Checklist - Verify ALL complete**:
   - ✅ system.py deleted
   - ✅ api_models.py updated (3 classes removed)
   - ✅ main.py updated (router removed)
   - ✅ routers/__init__.py updated (export removed)
   - ✅ performance.tsx updated (CSS analysis removed)
   - ✅ response_utils.py updated (emojis removed)
   - ✅ CLAUDE.md updated (structure + last task)
   - ✅ AGENTS.md updated (structure)
   - ✅ docs/api/api-integration-guide.md updated (legacy docs removed)
   - ✅ Serena memories updated (tech_stack, project_architecture)
   - ✅ CLI tests run and passed (27/27)
   - ✅ Test report generated

3. **Ensure NOTHING is staged yet**:
   ```bash
   git status
   # Should show: "Changes not staged for commit"
   ```

**Tool Usage**: Standard Bash

---

### ✅ TASK 8.2: Stage Everything At Once

**Status**: ⏸️ PENDING

**Actions**:

1. **Stage ALL files in ONE command**:
   ```bash
   git add -A
   ```

2. **This is the FIRST time running git add**

3. **Verify staging immediately**:
   ```bash
   git status
   ```

4. **Should see**:
   - All modified files staged
   - Deleted system.py staged
   - Test report staged
   - Documentation updates staged
   - Serena memories staged
   - NOTHING unstaged

**Tool Usage**: Standard Bash

---

### ✅ TASK 8.3: Commit Immediately (Within 60 Seconds)

**Status**: ⏸️ PENDING

**Actions**:

```bash
git commit -m "$(cat <<'EOF'
[CLEANUP] Remove legacy deprecated features from entire codebase

**Primary Changes:**

1. **CSS Analysis Removal**: Removed high-overhead CSS performance analysis
2. **System Status Endpoint Removal**: Deleted unused /api/v1/system/status endpoint
3. **Prompt Template Cleanup**: Removed all remnants of deprecated PromptTemplate system
4. **Emoji Removal**: Cleaned emoji characters from CLI responses

**Backend Changes:**

- **Deleted**: src/backend/routers/system.py (entire file - unused endpoint)
- api_models.py: Removed SystemMetrics, SystemStatusResponse classes + prompt_templates_loaded field
- main.py: Removed system_router registration
- routers/__init__.py: Removed system_router export
- response_utils.py: Removed all emoji characters from CLI output formatting

**Frontend Changes:**

- performance.tsx: Removed analyzeCSSPerformance() function (HIGH overhead - 1-2% CPU)

**Documentation Changes:**

- CLAUDE.md: Removed prompt_templates.py reference + updated last completed task
- AGENTS.md: Removed prompt_templates.py reference
- docs/api/api-integration-guide.md: Removed extensive legacy PromptTemplate documentation

**Test Results:**

- Total Tests: 27/27 PASSED ✅
- Success Rate: 100%
- Average Response Time: [ACTUAL]s
- Test Report: cli_regression_test_loop*_YYYYMMDD_HHMMSS.txt

**Performance Improvements:**

- CSS analysis overhead eliminated (1-2% CPU reduction)
- Codebase simplified and more maintainable
- Documentation now accurate and up-to-date

**Files Changed:**

- ❌ Deleted: src/backend/routers/system.py
- ✅ Modified: src/backend/api_models.py (removed 3 classes)
- ✅ Modified: src/backend/main.py (removed router registration)
- ✅ Modified: src/backend/routers/__init__.py (removed export)
- ✅ Modified: src/backend/utils/response_utils.py (emoji cleanup)
- ✅ Modified: src/frontend/utils/performance.tsx (removed CSS analysis)
- ✅ Modified: CLAUDE.md (updated structure + last task)
- ✅ Modified: AGENTS.md (updated structure)
- ✅ Modified: docs/api/api-integration-guide.md (removed legacy docs)
- ✅ Updated: .serena/memories/tech_stack.md
- ✅ Updated: .serena/memories/project_architecture.md

**Total**: 1 file deleted, 10 files modified, 2 Serena memories updated

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Tool Usage**: Standard Bash

---

### ✅ TASK 8.4: Push Immediately

**Status**: ⏸️ PENDING

**Actions**:

```bash
git push
```

**Verification**: Commit successfully pushed to remote

**Tool Usage**: Standard Bash

---

## Task Completion Summary

**Total Phases**: 8
**Total Tasks**: 24
**Implementation Time**: 60-90 minutes estimated
**Testing Time**: 15-20 minutes
**Documentation Time**: 20-30 minutes
**Total**: 95-140 minutes

---

## Success Criteria Checklist

- ✅ All 4 legacy features completely removed
- ✅ Zero references in code, docs, or memories
- ✅ All tests passing (27/27 CLI tests)
- ✅ Web UI fully functional
- ✅ CLI fully functional (without emojis)
- ✅ 1-2% CPU performance improvement
- ✅ Cleaner, more maintainable codebase
- ✅ Documentation accurate and up-to-date
- ✅ Serena memories updated
- ✅ Atomic commit with all changes
- ✅ Changes pushed to remote

---

## Risk Mitigation

**If tests fail**:
1. Review error logs carefully
2. Identify which removal caused the issue
3. Fix the specific problem
4. Re-run tests until 100% pass
5. Do NOT proceed to commit until tests pass

**If web UI breaks**:
1. Check browser console for errors
2. Verify frontend changes didn't introduce regressions
3. Test with CSS analysis removal reverted
4. Fix and re-test

**If CLI breaks**:
1. Check for emoji removal causing formatting issues
2. Verify Rich library still working correctly
3. Test with emoji removal reverted
4. Fix and re-test

---

**Plan Created**: 2025-10-06
**Ready for Implementation**: ✅ YES
**Use Sequential-Thinking at each phase for systematic execution**
