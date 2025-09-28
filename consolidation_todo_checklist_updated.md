# 🔴 CRITICAL: Prompt Consolidation TODO Checklist - UPDATED

## Task 2: Granular Detailed TODO Task Checklist for Prompt Consolidation

**Objective:** Consolidate all AI Chat Prompts to use only a single common System Prompt & Agent instructions from `src/backend/main.py`, removing BOTH the dynamic prompt manager system AND the direct prompts system completely.

**CRITICAL DISCOVERY:** Both `dynamic_prompt_manager.py` AND `direct_prompts.py` are dead code that can be completely removed!

---

## Phase 1: Remove Dynamic Prompt Manager System

### 1.0 Investigation: Direct Prompts System Analysis

- [x] **1.0.1** ✅ COMPLETED: Investigate if `src/backend/direct_prompts.py` is dead code
- [x] **1.0.2** ✅ COMPLETED: Verify no frontend analysis buttons exist (only CSS remnants)
- [x] **1.0.3** ✅ COMPLETED: Confirm DirectPromptManager usage in main.py is legacy
- [x] **1.0.4** ✅ COMPLETED: Determine that entire direct prompts system can be removed

### 1.1 Remove Dynamic Prompt Manager Files

- [x] **1.1.1** ✅ COMPLETED: Delete `src/backend/dynamic_prompt_manager.py`
- [x] **1.1.2** ✅ COMPLETED: Delete `src/backend/dynamic_prompt_integration.py`
- [x] **1.1.3** ✅ COMPLETED: Delete `src/backend/dynamic_prompts.py`
- [x] **1.1.4** ✅ COMPLETED: Delete `src/backend/secure_prompt_manager.py`
- [x] **1.1.5** ✅ COMPLETED: Delete `src/backend/advanced_prompting_features.py`
- [x] **1.1.6** ✅ COMPLETED: Delete `src/backend/security_features.py`

### 1.2 Remove Dynamic Prompt Test Files

- [x] **1.2.1** ✅ COMPLETED: Delete `tests/test_dynamic_prompting_system.py`
- [x] **1.2.2** ✅ COMPLETED: Delete `test_template.py`

### 1.3 Remove Dynamic Prompt Documentation

- [x] **1.3.1** ✅ COMPLETED: Delete `docs/dynamic_prompting_system_usage.md`
- [x] **1.3.2** ✅ COMPLETED: Delete `docs/dynamic_prompting_system_user_guide.md`
- [x] **1.3.3** ✅ COMPLETED: Delete `docs/dynamic_prompting_system_developer_guide.md`
- [x] **1.3.4** ✅ COMPLETED: Delete `docs/dynamic_prompting_system_api_reference.md`
- [x] **1.3.5** ✅ COMPLETED: Delete `docs/dynamic_prompting_system_troubleshooting.md`
- [x] **1.3.6** ✅ COMPLETED: Delete `docs/dynamic_prompting_system_migration_guide.md`
- [x] **1.3.7** ✅ COMPLETED: Delete `docs/dynamic_prompting_usage_guide.md`

### 1.4 Remove Dynamic Prompt Implementation Plans

- [x] **1.4.1** ✅ COMPLETED: Delete `docs/implementation_plans/dynamic_adaptive_prompting_system_implementation_plan.md`
- [x] **1.4.2** ✅ COMPLETED: Delete `docs/implementation_plans/dynamic_adaptive_prompting_system_scoping.md`
- [x] **1.4.3** ✅ COMPLETED: Delete `docs/implementation_plans/prompt_consolidation_implementation_plan.md`
- [x] **1.4.4** ✅ COMPLETED: Delete `docs/implementation_plans/direct_prompt_migration_implementation_plan.md`

### 1.5 Remove Dynamic Prompt Configuration Files

- [x] **1.5.1** ✅ COMPLETED: Delete `config/staging.yaml`
- [x] **1.5.2** ✅ COMPLETED: Delete `config/monitoring.yaml`
- [x] **1.5.3** ✅ COMPLETED: Delete `config/deployment.yaml`

### 1.6 Remove Dynamic Prompt Memory Files

- [x] **1.6.1** ✅ COMPLETED: Delete `.serena/memories/dynamic_adaptive_prompting_system_architecture.md`
- [x] **1.6.2** ✅ COMPLETED: Delete `.serena/memories/dynamic_adaptive_prompting_system_implementation.md`
- [x] **1.6.3** ✅ COMPLETED: Delete `.serena/memories/dynamic_prompting_integration_guide.md`

---

## Phase 2: Remove Direct Prompts System (Dead Code)

### 2.1 Remove DirectPromptManager Usage from main.py

- [ ] **2.1.1** Remove `DirectPromptManager` import from `main.py` (lines 50, 69)
- [ ] **2.1.2** Remove `direct_prompt_manager = DirectPromptManager()` instantiation (line 931)
- [ ] **2.1.3** Remove all `direct_prompt_manager` usage in GUI chat endpoint (lines 1117-1122)
- [ ] **2.1.4** Remove all `direct_prompt_manager` usage in CLI (lines 1495-1499)
- [ ] **2.1.5** Simplify chat endpoint to use only `get_enhanced_agent_instructions()`

### 2.2 Update main.py get_enhanced_agent_instructions Function

- [x] **2.2.1** ✅ COMPLETED: Remove dynamic prompt import from `get_enhanced_agent_instructions()`
- [x] **2.2.2** ✅ COMPLETED: Replace dynamic prompt logic with static prompt from fallback
- [x] **2.2.3** ✅ COMPLETED: Remove try/except ImportError block for dynamic_prompt_integration
- [ ] **2.2.4** Ensure function returns consistent prompt for both CLI and GUI

### 2.3 Update API Models

- [ ] **2.3.1** Remove `AnalysisIntent` import from `src/backend/api_models.py`
- [ ] **2.3.2** Remove all `AnalysisIntent` usage from API models
- [ ] **2.3.3** Clean up any remaining references to analysis types

---

## Phase 3: Remove Direct Prompts File and Frontend CSS

### 3.1 Remove direct_prompts.py

- [ ] **3.1.1** Delete `src/backend/direct_prompts.py`
- [ ] **3.1.2** Verify no remaining imports or references to this file

### 3.2 Remove Frontend Analysis Button CSS

- [ ] **3.2.1** Remove analysis button CSS from `src/frontend/index.css`
- [ ] **3.2.2** Remove analysis button references from `src/frontend/utils/accessibility.ts`

---

## Phase 4: Update Documentation

### 4.1 Update Main Documentation

- [ ] **4.1.1** Update `README.md` to remove references to dynamic prompting system
- [ ] **4.1.2** Update `AGENTS.md` to reflect simplified prompt architecture
- [ ] **4.1.3** Update any other documentation files that reference dynamic prompting

### 4.2 Update Test Prompts Documentation

- [ ] **4.2.1** Update `tests/playwright/test_prompts.md` to reflect simplified system
- [ ] **4.2.2** Remove any references to dynamic prompt features

---

## Phase 5: Clean Up References

### 5.1 Search and Remove Dynamic Prompt References

- [ ] **5.1.1** Search entire codebase for "dynamic_prompt" references
- [ ] **5.1.2** Remove or update any remaining references
- [ ] **5.1.3** Search for "DirectPromptManager" references
- [ ] **5.1.4** Remove or update any remaining references

### 5.2 Clean Up Import Statements

- [ ] **5.2.1** Remove all imports of dynamic prompt modules
- [ ] **5.2.2** Update any remaining import statements
- [ ] **5.2.3** Verify no broken imports remain

---

## Phase 6: Verification and Testing

### 6.1 Code Verification

- [ ] **6.1.1** Run Python syntax check on all modified files
- [ ] **6.1.2** Verify no broken imports or references
- [ ] **6.1.3** Check that all functions and classes are properly defined

### 6.2 Functional Testing

- [ ] **6.2.1** Test CLI functionality with consolidated prompts
- [ ] **6.2.2** Test GUI functionality with consolidated prompts
- [ ] **6.2.3** Verify both CLI and GUI use identical prompts
- [ ] **6.2.4** Test that system works without any dynamic or direct prompt systems

### 6.3 Documentation Verification

- [ ] **6.3.1** Verify all documentation is updated and consistent
- [ ] **6.3.2** Check that no outdated references remain
- [ ] **6.3.3** Ensure README and other docs reflect new architecture

---

## Expected Outcomes

After completing this checklist:

✅ **Single Streamlined System Prompt & Agent Instructions**

- All prompts consolidated in `main.py`
- No dynamic or enhanced prompts anymore
- No direct prompts system anymore
- GUI chat uses same prompts as CLI

✅ **No Dynamic Prompt System**

- All dynamic prompt files removed
- No dynamic prompt manager references
- Simplified architecture

✅ **No Direct Prompts System**

- All direct prompt files removed
- No DirectPromptManager references
- No analysis button system
- No AnalysisIntent enum

✅ **No "Data first, Detailed Analysis" Enforcement**

- Updated prompts in `main.py` remove this requirement
- Responses no longer enforce this format

✅ **No Unused Dead Code**

- All dynamic prompt system files removed
- All direct prompt system files removed
- No references to removed systems
- Clean, maintainable codebase

---

## Critical Success Criteria

1. **Single Source of Truth**: All prompts come from `main.py` only
2. **No Dynamic System**: Complete removal of dynamic prompt manager
3. **No Direct System**: Complete removal of direct prompts system
4. **GUI = CLI**: GUI uses identical prompts to CLI
5. **No Dead Code**: All unused files and references removed
6. **Functional**: Both CLI and GUI work with consolidated system
7. **Clean**: No broken imports or references remain

---

## Risk Mitigation

- **Backup**: Create backup before starting
- **Incremental**: Complete each phase before moving to next
- **Testing**: Test after each major change
- **Rollback**: Keep ability to rollback if issues arise

---

**Total Estimated Tasks: 45 individual tasks across 6 phases**
**Estimated Time: 3-4 hours for experienced developer**
**Risk Level: Medium (extensive file removal and code changes)**
