## 🔴 CRITICAL: YOU MUST ALWAYS USE THESE TOOLS FIRST in any particular order to perform all task(s)

- __Serena Tools__: Use for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
- __Sequential-Thinking Tools__: Use for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
- __Context7 Tools__: Use for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups
- __Filesystem Tools__: Use for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
- __Standard Read/Write/Edit Tools__: Use for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
- __Playwright Tools__: Use for Testing with Browser automation for React GUI & App Validation

## Quick Start

__One-Click Application Startup (Recommended):__

The startup scripts automatically START all development servers BUT __DOES NOT OPEN THE APP IN BROWSER AUTOMATICALLY__.

```bash
# Option 1: Main startup script (recommended)
./start-app.sh
```

__Prerequisites:__ uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (Main Script)

- __Terminal Support__: Tries `gnome-terminal` first, falls back to `xterm`
- __Cross-Platform__: Works on most Linux distributions and macOS
- __Automatic Fallback__: Gracefully handles missing terminal emulators

## What the Scripts Do

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, vite)
- __Preserves MCP servers__ - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- __Backend__: Starts FastAPI server on `http://127.0.0.1:8000`
- __Frontend__: Starts Vite dev server on `http://127.0.0.1:3000`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent hard-coded ports (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch

- __NOTIFIES USER TO LAUNCH BROWSER TO START THE APP WHEN SERVERS ARE READY__

__Access:__ <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)
