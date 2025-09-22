## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s)

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis
2. Use Context7 for research and best practices
3. Use Serena Tools for code analysis and manipulation
4. Use Filesystem Tools for batch operations and project management
5. Use Standard Read/Write/Edit for file modifications
6. Use Playwright Tools for testing and validation
7. REPEAT any tool as needed throughout the process
8. NEVER stop using tools - continue using them until task completion

SPECIFIC TOOL USAGE GUIDELINES:

**Serena Tools**: USE AS OFTEN AS NEEDED for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications

**Sequential-Thinking Tools**: USE AS OFTEN AS NEEDED for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)

**Context7 Tools**: USE AS OFTEN AS NEEDED for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups

**Filesystem Tools**: USE AS OFTEN AS NEEDED for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications

**Standard Read/Write/Edit Tools**: USE AS OFTEN AS NEEDED for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management

**Playwright Tools**: USE AS OFTEN AS NEEDED for Testing with Browser automation for React GUI & App Validation

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

###

## Task Details: CORRECTED Tool Usage Review: Phase 1, 2, & 3

- Because of incorrect tool usage, You need to perform another CORRECTED Code Review WITH PROPER TOOL USE for Phase 1, 2, & 3 from docs/implementation_plans/UI_Performance_Optimization_Implementation_Plan.md
- Perform the Code Review Task, Summary Task, Atomic Git Commit & Push Task, & Final Verification Task

# Code Review Task

- Use the tools AS OFTEN AS NEEDED & IN ANY ORDER AS NEEDED: Sequential-Thinking, Serena Tools, FileSystem Tools, Context7 Tools for Researching Robust most update to date best, robust, modern practices, latest documentation, latest framework(s) to perform the task(s): perform comprehensive code review of JUST THE CHANGED FILES\DOCS ONLY - DO NOT REVIEW FILES\DOCS THAT HAVE NOTHING TO DO WITH RECENT CHANGES
- Use standard Read/Write/Edit tools for single-file operations
- Continue review/fix loop until achieving PASSING code review status
- PROCEED TO REMAINING Summary Task, Atomic Git Commit & Push Task, & Final Verification Task

# Summary Task

- Create token & context efficient git commit message of all the changes to prepare for the final commit task(s)
- Update CLAUDE.md "Last Completed Task Summary" section with the VERBATIM COPY of the token & context efficient git commit message between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- This ensures that the git commit message is cached for token & context efficient in order to update CLAUDE.md with, preventing the need to waste tokens by having to regenerate similiar task completion summaries

# Atomic Git Commit & Push Task

**MANDATORY PRE-COMMIT CHECKLIST (CRITICAL FOR SUCCESS):**

1. Run `git status` to identify ALL modified files
2. Run `git add .` to stage ALL changes (never commit without staging all)
3. Run `git status` again to verify ALL files are staged
4. Verify specialist work inclusion: ALL frontend, backend, test, and config changes MUST be staged
5. Only then execute `git commit` with comprehensive message

**AGENT PROCESS REQUIREMENTS:**

- Code reviewer MUST verify all specialist work is staged before commit
- NEVER commit without comprehensive staging verification
- Implement explicit git status checks at each phase
- Failure to include all modified files is a CRITICAL VIOLATION

**Commit Requirements:**

- Create single atomic git commit containing ALL : CLAUDE.md, code files, documentation changes, 1x test report if it exist, NO TEST OUTPUT RESULTS\DATA\SCREENSHOTS\VIDEOS ETC
- **CRITICAL**: DO NOT INCLUDE & COMMIT testing artifacts & testing outputs
- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever

- ## 🚨 MANDATORY: DOUBLE CHECK THAT CLAUDE.MD HAS NO MORE CHANGES AND THAT YOU WILL COMMIT CLAUDE.MD ATOMICALY

- ## 🚨 MANDATORY: YOU ARE NOT ALLOWED TO PERFORM 2 SEPARATE COMMITS WITH A SEPARATE CLAUDE.MD COMMIT

- git commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

# Final Verification Task

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly git committed and git pushed
- NO LINGERING UNCOMMITTED CLAUDE.MD
- CLAUDE.MD COMMIT ALONG WITH THE REST OF FILES
