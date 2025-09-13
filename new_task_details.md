# New Task Details

## Task Description

[MIGRATION] Fix Remaining Gaps & Tasks to Fully Close Migration

# Migration Audit & Implementation Plan

Based on my comprehensive review of the migration documentation and codebase audit, here's the complete assessment and action plan:

What the Documentation Claims vs Reality:

* **Documentation Claims:** 100% complete (all 10 phases done)
* **Actual Codebase State:** CONFIRMED - Migration IS complete with proper structure

**Verified Achievements:**

* ✅ Phase 1-2: Branch setup and documentation prep - **COMPLETE**
* ✅ Phase 3-4: Legacy files removed (`chat_ui.py`, `market_parser_demo.py`, `stock_data_fsm/`) - **CONFIRMED**
* ✅ Phase 5-6: System migrated to root (`/src/`, `/frontend/`) - **CONFIRMED** ✅ Phase 7: Dependencies fixed (OpenAI v1.99.9, openai-agents v0.2.8) - **CONFIRMED**
* ✅ Phase 8: Documentation updated - **MOSTLY COMPLETE**
* ✅ Phase 9: Tests migrated to `/tests/` - **CONFIRMED**
* ✅ Phase 10: Legacy directory removed (`gpt5-openai-agents-sdk-polygon-mcp/ doesn't exist`) - **CONFIRMED**

---

## Research Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

* Research & Analyze task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last

## Planning Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

* IF RESEARCH FROM Tasks were NOT performed, this is a VIOLATION and task must be restarted from the beginning
* Based on the research task(s), generate fully detailed, granular, implementation plan task breakdown todo checklist to complete all the requested task(s)

## Remaining Gaps & Tasks to Fully Close Migration (HIGH PRIORITY)

**1. Clean Up Legacy References**

* **Issue:** Multiple files still reference old "gpt5-openai-agents-sdk-polygon-mcp" paths
* **Files to Update:**
  * `package.json` - scripts still point to old paths
  * `frontend/LIVE_SERVER_DOCUMENTATION_TEMPLATES.md` - Multiple old path references
  * `.github/workflows/lighthouse-ci.yml` - CI/CD references old paths

**2. Update Root package.json Scripts**

* **Current:** Scripts reference `gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI`
* **Fix:** Update to reference `/frontend/` instead

**3. Remove Legacy Test Files from Root**

* **Files to Move/Remove:**
  * `test_dual_stock_prompts.py`
  * `test_real_mode_simple.py`
  * `test_real_root_cause_fixes.py`
  * `test_unified_conversational.py`

## DETAILED IMPLEMENTATION PLAN

**Task 1: Update `package.json` Scripts**

* // Update these scripts to use new paths:
  * `"port:js": "cd frontend && npm run lint"`
  * `"format:js": "cd frontend && npm run format"`
  * `"lint:fix": "npm run format:python && cd frontend && npm run lint:fix"`

**Task 2: Update Frontend Documentation**

* Replace all references to `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/` with `/frontend/`
* Update `LIVE_SERVER_DOCUMENTATION_TEMPLATES.md`

**Task 3: Update GitHub Actions**

* Update `.github/workflows/lighthouse-ci.yml` to reference `/frontend/` instead of old paths

**Task 4: Clean Up Root Directory**

* Move test files to `/tests/` or remove if obsolete

**Task 5: Final Validation**

* Run `uv run src/main.py` to test CLI
* Run `cd frontend && npm run dev` to test frontend
* Verify all documentation is accurate

**Task 6: Create Final Migration Commit**

* Stage all updates
* Create atomic commit with message documenting migration completion
* Update `docs/ENHANCED_10_PHASE_MIGRATION_ORCHESTRATION_PLAN.md`
* Update `CLAUDE.md` and `LAST_TASK_SUMMARY.md`

## Implementation Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

* Based on all the research & newly generated implementation plan task breakdown, perform the requested todo checklist task(s)

## Testing Task(s) - SPECIALISTS(s) to use Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

## Final Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to perform Final 4 Tasks

Final Task 1: Review/Fix Loop

* SPECIALISTS performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
* Uses `mcp__filesystem__*` tools for all file operations and examination
* Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
* Continue review/fix cycle WITH LINT until achieving PASSING code review status

Final Task 2: Task Summary Updates for LAST_TASK_SUMMARY.md & CLAUDE.md

* Generate detailed task completion summary & OVERWRITE the doc "LAST_TASK_SUMMARY.md"
* Based on detailed task completion summary, generate high level task completion summary 20 lines MAX for updating CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
* Include all deliverables, changes made, and completion status
* This ensures task summary is included in the atomic commit

Final Task 3: Atomic Git Commit & Push

* Run `git status` to review all staged and unstaged changes
* Create single atomic git commit containing ALL changes: code files, CLAUDE.md, LAST_TASK_SUMMARY.md, documentation updates, test reports, task summary etc
* the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever
* git Push commit to repository using provided personal access token
* **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Final Task 4: Final Verification

* Run final `git status` to confirm successful commit and push
* Verify working tree is clean and branch is up-to-date with remote
* Confirm all changes are properly git committed and git pushed

**Key Requirements:**

## Requirements

## Expected Outcome*

*SINGLE ATOMIC COMMIT OF ALL FILES AND DOC CHANGES - DO NOT COMMIT MORE THAN 1x for the same Phases.  DO NOT COMMIT UNLESS ALL FILES AND DOC CHANGES ARE FINALIZED AND READY TO BE COMMITTED*

## Additional Context

* Read 'docs/ENHANCED_10_PHASE_MIGRATION_ORCHESTRATION_PLAN.md' for more context & background if needed
* Read 'PHASE_7_10_MIGRATION_STATUS_REPORT.md' for more context & background if needed
