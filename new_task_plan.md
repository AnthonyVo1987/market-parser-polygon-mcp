# Task Plan: Standardized Test Prompts Documentation Update

## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop

using tools - continue using them until tasks completion!!!! 🔴

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout
the entire task execution. This is NOT a one-time checklist - you must
continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation
  at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation,
   Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Context7 for research and best up to date Implementation Practices
   & Library documentation lookups
3. Use Serena Tools for code analysis, symbol manipulation, pattern search
   with context, and memory management for complex financial algorithm
   development and refactoring; Use standard Read/Write/Edit for simple file
   content modifications
4. Use Filesystem Tools for Batch File operations (3+), file discovery,
   configuration management, metadata analysis, project organization, project
   structure analysis, and documentation generation for comprehensive project
   management; Use standard Read/Write/Edit for single-file content
   modifications
5. Use Standard Read/Write/Edit for single-file content modifications,
   simple edits, and direct file operations; use Serena/Filesystem for
   complex analysis, batch operations, and project management
6. Use Playwright Tools for Testing with Browser automation for React GUI
   & App Validation
7. 🔴 REPEAT any tool as needed throughout the process
8. 🔴 NEVER stop using tools - continue using them until task completion

TOOL OVERLAP RESOLUTION:

- Filesystem Tools: Use for 3+ file operations, batch processing, project
  management, metadata analysis, comprehensive project operations
- Standard Read/Write/Edit: Use for single-file modifications, simple
  edits, direct file operations
- Serena Tools: Use for complex code analysis, symbol manipulation,
  pattern search with context
- When in doubt: Use Filesystem for batch/complex operations, Standard
  for simple single-file operations

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're
  failing
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch
  operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

REMEMBER: The tool list is your toolkit - use every tool as often as
needed, in any order, throughout the entire task execution. Choose the
right tool for the right operation

###

## New Task Details

Perform research and scope out some more independent CLI\GUI Performance Optmizations.  No New Docs needed yet for the scoping:

## Scope Task 1. Use Toolkit to scope out removing all appended "Footer Data" & Footer Code from AI Response from both CLI & UI

- Current code is appeneding footer data to every AI Response that should be removed to improve response times: AI Model Name, Timestamp, Response Time
- Need to also completely remove the code that would try and detect and append AI Model name to responses.  We still want to keep AI Model Selector feature, so be careful not to remove core business critical functionality
- Need to also completely remove the code that would try and detect and calculate response times from BOTH the CLI & GUI code. The response time will be re-implemented at a later date for a better implementation
- Need to also completely remove the code that would generate timestamp

## Scope Task 2. Use Toolkit to scope out Completely removing the BUTTON PROMPT STOCK TICKER Input Validation code.  Input validation will be re-implemented better in the future TBD, but for now, we can remove it.  We will NOT perform any BUTTON PROMPT STOCK TICKER Input Validation at the moment, but for now just set a max number of characters of 5 characters MAX for the input, which should cover most ticker names.  All of the Button Prompts should now be active and available to click no matter what is input in the BUTTON PROMPT STOCK TICKER Input.  Input Validation wil now be handled implicitly from the AI Agent Response.  Valid tickers will have AI Agent correctly respond, and the for invalid tickers, the AI Agent will already respond that the ticker is Invalid and\or Not Found

## Scope Task 3. Use Toolkit to scope out Completely removing the GUI Response Times code and component display since we will NOT calculate response times currently and will just rely on the the new integrated performance monitoring tools for response time performance analysis
