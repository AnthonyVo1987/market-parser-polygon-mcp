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

## Task 1. Read & Understand prompting guide docs/openAI_GPT-5_prompting_guide.md to then CONSOLIDATE AND STANDARDIZW ALL Outputs & Output Formats for ALL Prompts

A. DATA FIRST

- Data should be formatted in Bullet point format with 2 Decimal Points Max
- Provide Data in "Cleaned Up Raw Format" to provide user no frills data and numbers first, and then verbal analaysis later

- Example: Stock Snapshot\Quote Tools would return to AI Agent raw Responses like this:

// AI Agent receives Raw Formatted Responses from Stock Snapshot\Quote Tools
{
  "ticker": {
    "ticker": "NVDA",
    "todaysChangePerc": 0.37401819517432494,
    "todaysChange": 0.6619000000000028,
    "updated": 1758820926750610200,
    "day": {
      "o": 174.48,
      "h": 180.26,
      "l": 173.125,
      "c": 177.64,
      "v": 120671347,
      "vw": 177.3213
    },
    "min": {
      "av": 120663293,
      "t": 1758820860000,
      "n": 4103,
      "o": 177.85,
      "h": 177.8599,
      "l": 177.61,
      "c": 177.623864,
      "v": 447886,
      "vw": 177.7376
    },
    "prevDay": {
      "o": 179.77,
      "h": 179.78,
      "l": 175.4,
      "c": 176.97,
      "v": 143564116,
      "vw": 177.4531
    }
  },
  "status": "OK",
  "request_id": "a37466e0d0e8ace2739f3e27577f6f9e"
}

- So response should be cleaned up a bit and formatted better to convert the raw JSON Responses to Data should be formatted in Bullet point format with 2 Decimal Points, AND converting the truncated repsonse attributes to actual user friendly words\terms:

// AI Agent receives Raw Formatted Responses from Stock Snapshot\Quote Tools

- Ticker
- Today's Change %
- Today's Change $
...

Day

- VWAP
- Open
- Low
...

Minute Data

- VWAP
- Open
- Low
...

Previous Day

- VWAP
- Open
- Low
...

- Do not need   "status": "OK",  "request_id": "a37466e0d0e8ace2739f3e27577f6f9e"

##

B. DETAILED ANALYSIS

- Provide Maximum of 3 KEY TAKEAWAYS\INSIGHTS in Numbered\bullet point format
- No actionable recommendations
- Focus on the data only

###

## Task 2. AnalysisIntent.SNAPSHOT Prompt Changes

- Fix the prompt because it needs to focus on providing STOCK and\or OPTIONS SNAPSHOTS, and NOT generic market snapshots.  AI Agent should use the relevant STOCK\OPTIONS Snapshots tools since snapshot tools provide real-time data
- Remove redundant ANALYSIS: Current price data, volume, and key performance metrics.
- Follow the new output formatting changes from Task 1, so new output is now:

A. DATA FIRST (from Task 1)

B. DETAILED ANALYSIS (from Task 1)

- Provide Maximum of 3 KEY TAKEAWAYS\INSIGHTS in Numbered\bullet point format
- No actionable recommendations
- Focus on the data only

## Task 3. AnalysisIntent.SUPPORT_RESISTANCE Prompt Changes

- Follow the new output formatting changes from Task 1, so new output is now:

A. DATA FIRST (from Task 1)

B. DETAILED ANALYSIS (from Task 1)

- Provide Maximum of 3 KEY TAKEAWAYS\INSIGHTS in Numbered\bullet point format
- No actionable recommendations
- Focus on the data only

## Task 4. AnalysisIntent.TECHNICAL Prompt Changes

Provide Only the following Technial Analysis now:

- RSI-14
- MACD (All)
- EMA 20/50/200 (3 different timing windows Day)
- SMA 20/50/200 Day (3 different timing windows Day)

- Follow the new output formatting changes from Task 1, so new output is now:

A. DATA FIRST (from Task 1)

B. DETAILED ANALYSIS (from Task 1)

- Provide Maximum of 3 KEY TAKEAWAYS\INSIGHTS in Numbered\bullet point format
- No actionable recommendations
- Focus on the data only

## Task 5. AnalysisIntent.General Prompt Changes

- Follow the new output formatting changes from Task 1, so new output is now:

A. DATA FIRST (from Task 1)

B. DETAILED ANALYSIS (from Task 1)

- Provide Maximum of 3 KEY TAKEAWAYS\INSIGHTS in Numbered\bullet point format
- No actionable recommendations
- Focus on the data only

## Task 6: Validate fixes by testing the CLI with some test prompts ONE AT A TIME to capture the footer data: uv run src/backend/main.py

Test Prompt 1: "Current Market Status"
Test Prompt 2: "Single Stock Snapshot NVDA"
Test Prompt 3: "NVDA Support & Resistance Levels

## Task 7: Use Serena Tools to update memories
