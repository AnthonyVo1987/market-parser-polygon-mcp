# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

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
7. REPEAT any tool as needed throughout the process
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

## New Task Details

## Task 1. In our Codebase, Investigate, Research, and Plan out the complete removal and retirement of any Legacy logging that the app added.  For performance optimizations, we will rely on JUST the default console\logs being generated from web console and dev server logs.  If we need to add addtional console messages and\or logs, we will add on a case by case basis.  Even with the complete removal of any additional logging, there are STILL default console\logs in web browsers and dev servers, so let's try NOT to add any extra overhed by adding extra debug info

- src/backend/utils/logger.py, src/frontend/utils/logger.ts, src/frontend/hooks/useDebugLog.ts are examples of some of the legacy logging code that you need to check if we can remove and there could be other files too
- Expected Outcome: No addtional Debug, production, Staging verbose, detailed console\logs etc.  We will debug JUST as is with no app specific logging and rely on built in logs and traces from our frameworks.

## Task 2. Based on the Investigation, Research, & Analysis from previous task(s), Generate a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to implement task 1

## Task 3. Implement the granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md'

## Task 4. Review projects Lint\ESLint\Pylint commands and config, and run full Lint\ESLint\PyLint and fix all issues

## Task 5. Perform some quick testing of CLI version (uv run src/backend/main.py), fix any issues

## Task 6. Perform some quick testing of GUI version using Playwright Tools, fix any issues

## Task 7. Use Serena to update memories
