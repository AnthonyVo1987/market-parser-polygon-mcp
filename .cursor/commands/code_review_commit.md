## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion!!!! 🔴

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

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
4. Use Filesystem Tools for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
5. Use Standard Read/Write/Edit for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
6. Use Playwright Tools for Testing with Browser automation for React GUI & App Validation
7. 🔴 REPEAT any tool as needed throughout the process
8. 🔴 NEVER stop using tools - continue using them until task completion

TOOL OVERLAP RESOLUTION:

- Filesystem Tools: Use for 3+ file operations, batch processing, project management, metadata analysis, comprehensive project operations
- Standard Read/Write/Edit: Use for single-file modifications, simple edits, direct file operations
- Serena Tools: Use for complex code analysis, symbol manipulation, pattern search with context
- When in doubt: Use Filesystem for batch/complex operations, Standard for simple single-file operations

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

REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

# 🚨 CRITICAL WORKFLOW - NUMBERED TODO CHECKLIST FOR AI AGENT

**MANDATORY: Follow steps in EXACT numerical order. Do NOT skip steps. Do NOT proceed to next step until current step is complete.**

## CODE REVIEW TASKS (Steps 1-15)

1. Run `git status` to identify ALL modified files in the repository
2. Use Sequential-Thinking to analyze the scope and nature of changes
3. Use Serena Tools to perform comprehensive code analysis of changed files ONLY
4. Use FileSystem Tools for batch file operations if 3+ files need changes
5. Use standard Read/Write/Edit tools for single-file modifications
6. Use Context7 Tools to research best practices for any new implementations
7. Review code quality, syntax, and logic in all changed files
8. Check for linting errors using read_lints tool on changed files
9. Fix any identified issues in the code
10. Verify all imports and dependencies are correct
11. Ensure TypeScript interfaces and types are properly defined
12. Validate API endpoints and data models are consistent
13. Check that all file paths and references are correct
14. Confirm no broken functionality or missing dependencies
15. **VERIFICATION**: All code review issues resolved - proceed to Summary Tasks

## SUMMARY TASKS (Steps 16-20)

16. Create a comprehensive, token-efficient git commit message describing ALL changes
17. **SAVE COMMIT MESSAGE TO CACHE** - Store this exact message for reuse
18. Update CLAUDE.md "Last Completed Task Summary" section with VERBATIM copy of commit message
19. Place commit message between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
20. **VERIFICATION**: CLAUDE.md updated with cached commit message - proceed to Staging Tasks

## STAGING TASKS (Steps 21-30)

21. Run `git status` to confirm all modified files are identified
22. Run `git add .` to stage ALL changes (including CLAUDE.md)
23. Run `git status` again to verify ALL files are staged
24. **🚨 MANDATORY CHECK**: Confirm CLAUDE.md appears in staged files list
25. **🚨 MANDATORY CHECK**: Verify CLAUDE.md contains the task summary in staged content
26. **🚨 MANDATORY CHECK**: Confirm ALL task-related files are staged (code, docs, config)
27. **🚨 MANDATORY CHECK**: Verify NO files remain unstaged
28. **🚨 MANDATORY CHECK**: Confirm working directory is clean except for staged files
29. **🚨 MANDATORY CHECK**: Verify commit message cache is ready for use
30. **VERIFICATION**: All files properly staged including CLAUDE.md - proceed to Commit Tasks

## COMMIT TASKS (Steps 31-35)

31. Execute `git commit` using the EXACT cached commit message from step 17
32. **🚨 CRITICAL**: Ensure commit includes CLAUDE.md with ALL other files in SINGLE commit
33. **🚨 CRITICAL**: Verify commit message matches the cached version exactly
34. Execute `git push` to push commit to remote repository
35. **VERIFICATION**: Commit and push successful - proceed to Final Verification Tasks

## FINAL VERIFICATION TASKS (Steps 36-45)

36. Run `git status` to confirm working tree is clean
37. Verify branch is up-to-date with remote repository
38. Confirm all changes are properly committed and pushed
39. **🚨 MANDATORY CHECK**: NO lingering uncommitted files
40. **🚨 MANDATORY CHECK**: CLAUDE.md was committed with all other files
41. **🚨 MANDATORY CHECK**: Single atomic commit was created (no separate commits)
42. If additional file changes detected after commit, run `git diff` to analyze
43. **If changes are COSMETIC ONLY**: Discard with `git restore` - DO NOT COMMIT
44. **If changes are FUNCTIONAL**: This indicates STAGING FAILURE - proceed to Recovery Tasks
45. **VERIFICATION**: All verification checks passed - workflow complete

## RECOVERY TASKS (Steps 46-50) - ONLY IF STAGING FAILURE DETECTED

46. Revert the bad commit: `git reset --hard HEAD~1`
47. Restart entire workflow from step 1 (Code Review Tasks)
48. Ensure ALL files (including CLAUDE.md) are properly staged in step 22
49. Create new single atomic commit with ALL files in step 31
50. **CRITICAL**: Never create separate commits - always single atomic commit

## 🚨 CRITICAL RULES - VIOLATION = RESTART ENTIRE WORKFLOW

- **SINGLE ATOMIC COMMIT RULE**: CLAUDE.md MUST be committed with ALL other files in the SAME commit
- **NO SEPARATE COMMITS**: Creating separate commits for CLAUDE.md or any file = VIOLATION
- **STAGING VERIFICATION**: ALL files must be staged before commit - no exceptions
- **COMMIT MESSAGE CACHE**: Use exact cached message - do not regenerate
- **WORKFLOW ORDER**: Follow numbered steps in exact sequence - no deviations
