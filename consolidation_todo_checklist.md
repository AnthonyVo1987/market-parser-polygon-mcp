# 🔴 CRITICAL: Prompt Consolidation TODO Checklist

## Task 2: Granular Detailed TODO Task Checklist for Prompt Consolidation

**Objective:** Consolidate all AI Chat Prompts to use only a single common System Prompt & Agent instructions from `src/backend/main.py`, removing the dynamic prompt manager system completely.

---

## Phase 1: Remove Dynamic Prompt Manager System

### 1.0 Investigation: Direct Prompts System Analysis

- [ ] **1.0.1** ✅ COMPLETED: Investigate if `src/backend/direct_prompts.py` is dead code
- [ ] **1.0.2** ✅ COMPLETED: Verify no frontend analysis buttons exist (only CSS remnants)
- [ ] **1.0.3** ✅ COMPLETED: Confirm DirectPromptManager usage in main.py is legacy
- [ ] **1.0.4** ✅ COMPLETED: Determine that entire direct prompts system can be removed

### 1.1 Remove Dynamic Prompt Manager Files

- [ ] **1.1.1** Delete `src/backend/dynamic_prompt_manager.py`
- [ ] **1.1.2** Delete `src/backend/dynamic_prompt_integration.py`
- [ ] **1.1.3** Delete `src/backend/dynamic_prompts.py`
- [ ] **1.1.4** Delete `src/backend/secure_prompt_manager.py`
- [ ] **1.1.5** Delete `src/backend/advanced_prompting_features.py`
- [ ] **1.1.6** Delete `src/backend/security_features.py` (if exists)

### 1.2 Remove Dynamic Prompt Test Files

- [ ] **1.2.1** Delete `tests/test_dynamic_prompting_system.py`
- [ ] **1.2.2** Delete `test_template.py`

### 1.3 Remove Dynamic Prompt Documentation

- [ ] **1.3.1** Delete `docs/dynamic_prompting_system_usage.md`
- [ ] **1.3.2** Delete `docs/dynamic_prompting_system_user_guide.md`
- [ ] **1.3.3** Delete `docs/dynamic_prompting_system_developer_guide.md`
- [ ] **1.3.4** Delete `docs/dynamic_prompting_system_api_reference.md`
- [ ] **1.3.5** Delete `docs/dynamic_prompting_system_troubleshooting.md`
- [ ] **1.3.6** Delete `docs/dynamic_prompting_system_migration_guide.md`
- [ ] **1.3.7** Delete `docs/dynamic_prompting_usage_guide.md`

### 1.4 Remove Dynamic Prompt Implementation Plans

- [ ] **1.4.1** Delete `docs/implementation_plans/dynamic_adaptive_prompting_system_implementation_plan.md`
- [ ] **1.4.2** Delete `docs/implementation_plans/dynamic_adaptive_prompting_system_scoping.md`
- [ ] **1.4.3** Delete `docs/implementation_plans/prompt_consolidation_implementation_plan.md`
- [ ] **1.4.4** Delete `docs/implementation_plans/direct_prompt_migration_implementation_plan.md`

### 1.5 Remove Dynamic Prompt Configuration Files

- [ ] **1.5.1** Delete `config/staging.yaml`
- [ ] **1.5.2** Delete `config/monitoring.yaml`
- [ ] **1.5.3** Delete `config/deployment.yaml`

### 1.6 Remove Dynamic Prompt Memory Files

- [ ] **1.6.1** Delete `.serena/memories/dynamic_adaptive_prompting_system_architecture.md`
- [ ] **1.6.2** Delete `.serena/memories/dynamic_adaptive_prompting_system_implementation.md`
- [ ] **1.6.3** Delete `.serena/memories/dynamic_prompting_integration_guide.md`

---

## Phase 2: Consolidate Prompts into main.py

### 2.1 Update main.py get_enhanced_agent_instructions Function

- [ ] **2.1.1** Remove dynamic prompt import from `get_enhanced_agent_instructions()`
- [ ] **2.1.2** Replace dynamic prompt logic with static prompt from fallback
- [ ] **2.1.3** Remove try/except ImportError block for dynamic_prompt_integration
- [ ] **2.1.4** Ensure function returns consistent prompt for both CLI and GUI

### 2.2 Consolidate DirectPromptManager into main.py

- [ ] **2.2.1** Move `AnalysisIntent` enum from `direct_prompts.py` to `main.py`
- [ ] **2.2.2** Move `DirectPromptManager` class from `direct_prompts.py` to `main.py`
- [ ] **2.2.3** Update all imports in `main.py` to use local classes
- [ ] **2.2.4** Remove import of `DirectPromptManager` from `direct_prompts.py`

### 2.3 Update API Models

- [ ] **2.3.1** Update `src/backend/api_models.py` to import `AnalysisIntent` from `main.py`
- [ ] **2.3.2** Update try/except import pattern in `api_models.py`

---

## Phase 3: Remove Direct Prompts File

### 3.1 Remove direct_prompts.py

- [ ] **3.1.1** Delete `src/backend/direct_prompts.py`
- [ ] **3.1.2** Verify no remaining imports or references to this file

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
- [ ] **5.1.3** Search for "DynamicPromptManager" references
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
- [ ] **6.2.3** Verify button analysis still works with consolidated system
- [ ] **6.2.4** Test that both CLI and GUI use identical prompts

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
- GUI chat uses same prompts as CLI

✅ **No Dynamic Prompt System**

- All dynamic prompt files removed
- No dynamic prompt manager references
- Simplified architecture

✅ **No "Data first, Detailed Analysis" Enforcement**

- Updated prompts in `main.py` remove this requirement
- Responses no longer enforce this format

✅ **No Unused Dead Code**

- All dynamic prompt system files removed
- No references to removed system
- Clean, maintainable codebase

---

## Critical Success Criteria

1. **Single Source of Truth**: All prompts come from `main.py` only
2. **No Dynamic System**: Complete removal of dynamic prompt manager
3. **GUI = CLI**: GUI uses identical prompts to CLI
4. **No Dead Code**: All unused files and references removed
5. **Functional**: Both CLI and GUI work with consolidated system
6. **Clean**: No broken imports or references remain

---

## Risk Mitigation

- **Backup**: Create backup before starting
- **Incremental**: Complete each phase before moving to next
- **Testing**: Test after each major change
- **Rollback**: Keep ability to rollback if issues arise

---

**Total Estimated Tasks: 67 individual tasks across 6 phases**
**Estimated Time: 4-6 hours for experienced developer**
**Risk Level: Medium (extensive file removal and code changes)**
