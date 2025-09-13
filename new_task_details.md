# New Task Details

## Task Description

[MIGRATION] Migrate,integrate, & refactor anything remaining to be Root-Level Project Accessible

- There could be lingering nested code that needs to be properly migrated to be Project Root Folder Level Access, such as the frontend folder React UI Code
- Nested frontend folder React UI Code also has redundant code, such as dupe package.lock etc
- End goal is that THE ENTIRE migrated project needs to have ALL commands. scripts, code, tests, dev servers mandated to be accessible and run from Project Root - No exceptions
- There could even be more code\scripts\commands that need additional folder level to run, so we need to make sure everything can be converted to have users run anything from top level
- I.E. Nested folders need user to know which commands. scripts, code, tests, dev servers can be run at root level vs requiring a folder change to a nested folder to run other commands. scripts, code, tests, dev servers.  This causes so much confusion for User and AI Coding Agents to run all commands. scripts, code, tests, dev servers because they are not sure which ones need to be run in which folder, so let's streamline and convert, integrate, & refactor the code to be Root level access for ease of use

## Research Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

- Research & Analyze task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last

## Planning Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

- IF RESEARCH FROM Tasks were NOT performed, this is a VIOLATION and task must be restarted from the beginning
- Based on the research task(s), generate fully detailed, granular, implementation plan task breakdown todo checklist to complete all the requested task(s)

## Implementation Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

- Based on all the research & newly generated implementation plan task breakdown, perform the requested todo checklist task(s)

- Update `docs/ENHANCED_10_PHASE_MIGRATION_ORCHESTRATION_PLAN.md` during the final task stages later to keep the docs upt to date

## Testing Task(s) - SPECIALISTS(s) to use Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

## Final Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to perform Final 4 Tasks

Final Task 1: Review/Fix Loop

- SPECIALISTS performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle WITH LINT until achieving PASSING code review status

Final Task 2: Task Summary Updates for LAST_TASK_SUMMARY.md & CLAUDE.md

- Generate detailed task completion summary & OVERWRITE the doc "LAST_TASK_SUMMARY.md"
- Based on detailed task completion summary, generate high level task completion summary 20 lines MAX for updating CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

Final Task 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic git commit containing ALL changes: code files, CLAUDE.md, LAST_TASK_SUMMARY.md, documentation updates, test reports, task summary etc
- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Final Task 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly git committed and git pushed

**Key Requirements:**

## Requirements

## Expected Outcome*

*SINGLE ATOMIC COMMIT OF ALL FILES AND DOC CHANGES - DO NOT COMMIT MORE THAN 1x for the same Phases.  DO NOT COMMIT UNLESS ALL FILES AND DOC CHANGES ARE FINALIZED AND READY TO BE COMMITTED*

## Additional Context

- Read 'docs/ENHANCED_10_PHASE_MIGRATION_ORCHESTRATION_PLAN.md' for more context & background if needed
- Read 'PHASE_7_10_MIGRATION_STATUS_REPORT.md' for more context & background if needed
