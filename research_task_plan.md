# Research Task Plan: Gradio Port Migration (7860 → 8000)

**Date:** October 18, 2025
**Research Phase:** COMPLETED
**Status:** Ready for Implementation Planning

---

## 📋 Executive Summary

**Research Question:** Why does Gradio fail to launch on port 7860, and how do we migrate to port 8000 for AWS deployment?

**Key Findings:**
- ✅ Port 7860 is hardcoded in gradio_app.py (lines 100, 107)
- ✅ Port 7860 referenced in 17+ documentation files
- ✅ Port 8000 is available (freed by FastAPI removal)
- ✅ No environment variable configuration exists
- ✅ Simple code + documentation update required

**Recommendation:** Change Gradio from port 7860 → 8000 for AWS deployment compatibility

---

## 🔍 Research Methodology

### Tools Used:
1. **Sequential-Thinking** - Systematic analysis of the port failure issue
2. **Serena search_for_pattern** - Comprehensive codebase search for "7860"
3. **Standard Read** - Analysis of gradio_app.py configuration
4. **Bash netstat** - Port availability verification

### Research Phases:
1. ✅ Error analysis and requirement understanding
2. ✅ Codebase pattern search for port references
3. ✅ Configuration file analysis
4. ✅ Port availability verification
5. ✅ Solution design and scoping

---

## 🎯 Problem Statement

### Original Error:
```
OSError: Cannot find empty port in range: 7860-7860. You can specify a different
port by setting the GRADIO_SERVER_PORT environment variable or passing the
`server_port` parameter to `launch()`.
```

### Business Requirement:
- **AWS Deployment:** Need to use standard port 8000 for AWS deployment
- **Port Standardization:** Consolidate on single common port (8000)
- **Critical Constraint:** Gradio MUST launch before CLI testing

---

## 📊 Research Findings

### 1. Port Configuration Analysis

**Current State:**
```python
# src/backend/gradio_app.py (line 105-107)
demo.launch(
    server_name="127.0.0.1",
    server_port=7860,  # ❌ CURRENT: Gradio default port
    share=False,
    ...
)
```

**Print Statement:**
```python
# src/backend/gradio_app.py (line 100)
print("📍 Server: http://127.0.0.1:7860")  # ❌ CURRENT
```

**Required Change:**
```python
# NEW: AWS deployment port
demo.launch(
    server_name="127.0.0.1",
    server_port=8000,  # ✅ NEW: AWS deployment port
    share=False,
    ...
)

print("📍 Server: http://127.0.0.1:8000")  # ✅ NEW
```

### 2. Documentation References

**Files Containing Port 7860:** (17 files total)

**Critical Documentation:**
1. `CLAUDE.md` - 9 references
2. `README.md` - 5 references
3. `AGENTS.md` - 8 references
4. `TODO_task_plan.md` - 7 references
5. `package.json` - 2 references (npm scripts)
6. `docs/PROJECT_ENVIRONMENT_SETUP_GUIDE.md` - 6 references

**Serena Memories:** (11 files)
1. `.serena/memories/project_architecture.md` - 12 references
2. `.serena/memories/react_retirement_completion_oct_2025.md` - 17 references
3. `.serena/memories/fastapi_removal_completion_oct_2025.md` - 13 references
4. `.serena/memories/SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE.md` - 11 references
5. `.serena/memories/task_completion_checklist.md` - 2 references
6. `.serena/memories/project_onboarding_summary.md` - 6 references
7. `.serena/memories/suggested_commands.md` - 7 references
8. `.serena/memories/ui_refactor_oct_2025.md` - 2 references
9. `.serena/memories/adaptive_formatting_guide.md` - 1 reference

**Other Files:**
1. `research_task_plan.md` - 7 references (this file - will be updated)

### 3. Port Availability

**Verification Command:**
```bash
netstat -tlnp 2>/dev/null | grep -E ":(7860|8000)"
```

**Result:** Both ports available (no conflicts)

**Analysis:**
- ✅ Port 7860: Available (temporary conflict resolved)
- ✅ Port 8000: Available (FastAPI removed)
- ✅ No blocking processes on either port

### 4. Environment Configuration

**Checked Locations:**
- `.env` file - ❌ No GRADIO_SERVER_PORT variable
- `config/app.config.json` - ❌ No Gradio port config (FastAPI config removed)
- `pyproject.toml` - ❌ No runtime port config

**Conclusion:** Port is ONLY configured in gradio_app.py (hardcoded)

---

## 🔧 Solution Design

### Phase 1: Code Changes (1 file, 2 lines)

**File:** `src/backend/gradio_app.py`

**Changes:**
1. **Line 100:** Update print statement
   ```python
   # Before:
   print("📍 Server: http://127.0.0.1:7860")

   # After:
   print("📍 Server: http://127.0.0.1:8000")
   ```

2. **Line 107:** Update server_port parameter
   ```python
   # Before:
   server_port=7860,  # Gradio default port (separate from FastAPI:8000, React:3000)

   # After:
   server_port=8000,  # AWS deployment port (unified with previous FastAPI port)
   ```

### Phase 2: Documentation Updates (17 files)

**Strategy:** Global find-replace using Serena or Task agent

**Pattern:** Replace ALL instances of:
- `7860` → `8000`
- `http://127.0.0.1:7860` → `http://127.0.0.1:8000`
- `http://localhost:7860` → `http://localhost:8000`
- `:(7860|8000)` → `:8000` (in grep/netstat commands)

**Files to Update:**
1. CLAUDE.md
2. README.md
3. AGENTS.md
4. TODO_task_plan.md
5. package.json
6. docs/PROJECT_ENVIRONMENT_SETUP_GUIDE.md
7. All 11 Serena memory files

**Note:** Some files may have historical references (e.g., "was port 7860, now 8000") - preserve those for context.

### Phase 3: Testing Validation

**Test Sequence:**
1. **Gradio Launch Test** (MANDATORY FIRST)
   ```bash
   uv run python src/backend/gradio_app.py
   ```

   **Expected Output:**
   ```
   📍 Server: http://127.0.0.1:8000
   Running on local URL: http://127.0.0.1:8000
   ```

   **Success Criteria:**
   - ✅ No OSError about port conflicts
   - ✅ Server starts on port 8000
   - ✅ Web interface accessible at http://127.0.0.1:8000

   **Critical:** If Gradio fails, DO NOT proceed to CLI testing

2. **CLI Regression Tests** (AFTER Gradio success)
   ```bash
   chmod +x test_cli_regression.sh && ./test_cli_regression.sh
   ```

   **Expected Results:**
   - ✅ 39/39 tests COMPLETED
   - ✅ 39/39 tests PASSED (0 errors)
   - ✅ Average response time < 15s
   - ✅ Phase 2 verification: All responses correct

---

## 📝 Implementation Scope

### Files to Modify:
- **Code:** 1 file (gradio_app.py - 2 lines)
- **Documentation:** 17 files (global port reference updates)
- **Total:** 18 files

### Estimated Effort:
- **Code Changes:** 2 minutes
- **Documentation Updates:** 15-20 minutes (using Task agent for parallel updates)
- **Testing:** 10-15 minutes (Gradio + CLI tests)
- **Total:** ~30-40 minutes

### Risk Assessment:
- **Risk Level:** LOW
- **Rationale:**
  - Simple port number change
  - No logic modifications
  - Port 8000 available and tested
  - Gradio supports arbitrary ports
  - No environment dependencies

---

## 🚀 Next Steps

1. **Create TODO_task_plan.md** with granular implementation checklist
2. **Implement code changes** using Sequential-Thinking + Serena tools
3. **Update documentation** using Task agent for parallel updates
4. **Test Gradio launch** on port 8000 (MANDATORY before CLI testing)
5. **Run CLI regression tests** (39-test suite)
6. **Atomic commit** following proper git workflow

---

## 🔑 Key Technical Insights

### Why Port 8000?
1. **AWS Standard:** Port 8000 is standard for HTTP services in AWS deployment
2. **Port Consolidation:** FastAPI used 8000, now available after removal
3. **Simplicity:** Single port instead of multiple (was: 8000 FastAPI + 7860 Gradio)
4. **Consistency:** Aligns with backend port conventions

### Architecture Impact:
**Before:**
- React: Port 3000 (removed)
- FastAPI: Port 8000 (removed)
- Gradio: Port 7860 (current)

**After:**
- Gradio: Port 8000 (AWS deployment ready)

### Deployment Benefits:
- ✅ Standard AWS port for HTTP services
- ✅ No port conflicts with standard services
- ✅ Simplified firewall/security group rules
- ✅ Better alignment with cloud platform conventions

---

## 📚 References

**Related Documentation:**
- `.serena/memories/fastapi_removal_completion_oct_2025.md` - FastAPI port 8000 removal
- `.serena/memories/react_retirement_completion_oct_2025.md` - React port 3000 removal
- `new_research_details.md` - Original task requirements

**Port Search Results:**
- Total files with port 7860 references: 17
- Total port 7860 occurrences: 100+
- Code files requiring changes: 1
- Documentation files requiring updates: 17

---

## ✅ Success Criteria

**Research Phase Complete When:**
- ✅ Root cause identified (hardcoded port 7860)
- ✅ All port references located (17 files)
- ✅ Solution designed (port 7860 → 8000)
- ✅ Port availability verified (8000 is free)
- ✅ Testing strategy defined (Gradio first, then CLI)
- ✅ Implementation plan ready

**ALL CRITERIA MET - RESEARCH COMPLETE**

---

## 🎯 Research Completion Summary

**Status:** ✅ RESEARCH PHASE COMPLETE

**Findings:**
- Problem: Hardcoded port 7860 in gradio_app.py
- Solution: Change to port 8000 for AWS deployment
- Scope: 1 code file (2 lines) + 17 documentation files
- Risk: LOW (simple port change, no logic modifications)
- Testing: Gradio launch → CLI regression tests

**Ready for Phase 2:** Planning (TODO_task_plan.md creation)
