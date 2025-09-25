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

- Investigate and fix all of the follow bugs reported by user testing of latest CLI-GUI Optmizations

1. Chat input not cleared after sending a chat

2. AI Agent not correctly using real world time and date. Incorrectly thinks "now, this week, yesterday, today etc" refers to the date of its knowledge training data cutoff, and incorrectly uses data, prices from outdated time period.  Need to enforce that for Financial Analysis, AI Agents are NOT ALLOWED TO USE KNOWLEDGE DATA TRAINING CUTOFF BECAUSE Financial Analysis alwasy requires up to date data. For example, requesting for "How did NVDA performance do last week?" and/or "What was closing price of NVDA today?", the AI Agent would incorrectly use dates and prices from back in it's knowledcge data cutoff from ~2024 to respond, BUT obviously this makes no sense because the current year is 2025!  SO the response gives completely inocrrect prices and data because AI Agent is confused between "now, this week, yesterday, today etc" and thinks that means the data of it's knowledge data cutoff dates

3. AI Agent incorrectly thinks it does not have tools to retreive real time prices\data and\or data "now".  AI Agents should use "Snapshot Tools", for anything related to realtime and\or now data\prices.  A 15 minutes quote\data delay is sufficient to meet "Real-time now data".  AI Agents already have ALL the tools needed from the Polygon MCP Server to always give real-time \ now prices\data.  AI Agents should NEVER respond with saying it does NOT have the tools to retreive real-time-data \ quotes because AI Agents DO have all the tools needed.
