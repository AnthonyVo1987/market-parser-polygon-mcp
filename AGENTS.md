# AI Agent Instructions

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

## STANDARDIZED TEST PROMPTS

**CRITICAL:** All testing MUST use these standardized prompts to ensure
consistent, quick responses (30-60 seconds) and avoid false failures from
complex prompts.

### Quick Response Test Prompts (Use These Only)

1. **"Quick Response Needed with minimal tool calls: What is the current
   Market Status?"**
2. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Single Stock Snapshot NVDA"**
3. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Full Market Snapshot: SPY, QQQ, IWM"**
4. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, what was the closing price of GME today?"**
5. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, how is SOUN performance doing this week?"**
6. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Top Market Movers Today for Gainers"**
7. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Top Market Movers Today for Losers"**
8. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Support & Resistance Levels NVDA"**
9. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Technical Analysis SPY"**

**MANDATORY RULES:**

- ✅ Use ONLY these prompts for testing
- ✅ Copy prompts EXACTLY as written
- ✅ Expected response time: 30-60 seconds
- ❌ DO NOT create custom prompts
- ❌ DO NOT modify these prompts
- ❌ DO NOT use complex, open-ended queries

**📋 COMPLETE PROMPT REFERENCE:** For the full standardized test prompts
documentation, see `tests/playwright/test_prompts.md`

## Quick Start

**One-Click Application Startup (Recommended):**

The startup scripts automatically START all development servers BUT **DOES
NOT OPEN THE APP IN BROWSER AUTOMATICALLY**.

```bash
# Option 1: Main startup script (recommended)
./start-app.sh
```

**Prerequisites:** uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (Main Script)

- **Terminal Support**: Tries `gnome-terminal` first, falls back to
  `xterm`
- **Cross-Platform**: Works on most Linux distributions and macOS
- **Automatic Fallback**: Gracefully handles missing terminal
  emulators

## What the Scripts Do

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, vite)
- **Preserves MCP servers** - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- **Backend**: Starts FastAPI server on `http://127.0.0.1:8000`
- **Frontend**: Starts Vite dev server on `http://127.0.0.1:3000`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent hard-coded ports (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch

- **NOTIFIES USER TO LAUNCH BROWSER TO START THE APP WHEN SERVERS ARE READY**

**Access:** <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)
