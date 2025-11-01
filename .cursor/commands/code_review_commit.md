# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

🔴 CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Context7 for research and best up to date Implementation Practices & Library documentation lookups
3. Use Serena Tools for code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
4. REPEAT any tool as needed throughout the process
5. 🔴 NEVER stop using tools - continue using them until task completion

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're failing
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

# 🚨 CRITICAL WORKFLOW - NUMBERED TODO CHECKLIST FOR AI AGENT

**MANDATORY: Follow steps in EXACT numerical order. Do NOT skip steps. Do NOT proceed to next step until current step is complete.**

## **🚨 CRITICAL**: Use your Mandatory Toolkit for all tasks to Perform all: CODE REVIEW TASKS (Steps 1-10)

1. Run `git status` to identify ALL modified files in the repository
2. Based on ONLY the current modified files in the repo, perform comprehensive code review of the changes: reviewing full code and data execution path flow for any potential logic and\or integration issues, code quality, syntax, and logic in all changed files
3. Run the project's Lint\ESLInt\PYLint commands\config and check any linting errors using read_lints tool on changed files
4. Fix any identified issues in the code
5. Verify all imports and dependencies are correct
6. Ensure TypeScript interfaces and types are properly defined
7. Validate API endpoints and data models are consistent
8. Check that all file paths and references are correct
9. Confirm no broken functionality or missing dependencies
10. **VERIFICATION**: All code review issues resolved - proceed to Summary Tasks

## SUMMARY TASKS (Steps 11-15)

**🚨 CRITICAL**: Use your Mandatory Toolkit for all tasks to Perform all: Use your Mandatory Toolkit for all tasks to:
11. Create a comprehensive, token-efficient git commit message describing ALL changes
12. **SAVE COMMIT MESSAGE TO CACHE** - Store this exact message for reuse
13. Update CLAUDE.md "Last Completed Task Summary" section with VERBATIM copy of commit message
14. Place commit message between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
15. **VERIFICATION**: CLAUDE.md updated with cached commit message - proceed to Staging Tasks

## **🚨 CRITICAL**: Use your Mandatory Toolkit for all tasks to Perform all: STAGING TASKS (Steps 16-25)

16. Run `git status` to confirm all modified files are identified
17. Run `git add .` to stage ALL changes (including CLAUDE.md)
18. Run `git status` again to verify ALL files are staged
19. **🚨 MANDATORY CHECK**: Confirm CLAUDE.md appears in staged files list
20. **🚨 MANDATORY CHECK**: Verify CLAUDE.md contains the task summary in staged content
21. **🚨 MANDATORY CHECK**: Confirm ALL task-related files are staged (code, docs, config)
22. **🚨 MANDATORY CHECK**: Verify NO files remain unstaged
23. **🚨 MANDATORY CHECK**: Confirm working directory is clean except for staged files
24. **🚨 MANDATORY CHECK**: Verify commit message cache is ready for use
25. **VERIFICATION**: All files properly staged including CLAUDE.md - proceed to Commit Tasks

## COMMIT TASKS (Steps 26-30)

26. Execute `git commit` using the EXACT cached commit message from step 12
27. **🚨 CRITICAL**: Ensure commit includes CLAUDE.md with ALL other files in SINGLE commit
28. **🚨 CRITICAL**: Verify commit message matches the cached version exactly
29. Execute `git push` to push commit to remote repository
30. **VERIFICATION**: Commit and push successful - proceed to Final Verification Tasks

## FINAL VERIFICATION TASKS (Steps 31-40)

31. Run `git status` to confirm working tree is clean
32. Verify branch is up-to-date with remote repository
33. Confirm all changes are properly committed and pushed
34. **🚨 MANDATORY CHECK**: NO lingering uncommitted files
35. **🚨 MANDATORY CHECK**: CLAUDE.md was committed with all other files
36. **🚨 MANDATORY CHECK**: Single atomic commit was created (no separate commits)
37. If additional file changes detected after commit, run `git diff` to analyze
38. **If changes are COSMETIC ONLY**: Discard with `git restore` - DO NOT COMMIT
39. **If changes are FUNCTIONAL**: This indicates STAGING FAILURE - proceed to Recovery Tasks
40. **VERIFICATION**: All verification checks passed - workflow complete

## RECOVERY TASKS (Steps 41-45) - ONLY IF STAGING FAILURE DETECTED

41. Revert the bad commit: `git reset --hard HEAD~1`
42. Restart entire workflow from step 1 (Code Review Tasks)
43. Ensure ALL files (including CLAUDE.md) are properly staged in step 17
44. Create new single atomic commit with ALL files in step 26
45. **CRITICAL**: Never create separate commits - always single atomic commit

## 🚨 CRITICAL RULES - VIOLATION = RESTART ENTIRE WORKFLOW

- **SINGLE ATOMIC COMMIT RULE**: CLAUDE.md MUST be committed with ALL other files in the SAME commit
- **NO SEPARATE COMMITS**: Creating separate commits for CLAUDE.md or any file = VIOLATION
- **STAGING VERIFICATION**: ALL files must be staged before commit - no exceptions
- **COMMIT MESSAGE CACHE**: Use exact cached message - do not regenerate
- **WORKFLOW ORDER**: Follow numbered steps in exact sequence - no deviations
