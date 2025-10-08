# One-Click Startup Scripts

The Market Parser project provides one-click startup scripts that
automatically manage development servers.

## Quick Start

__One-Click Application Startup (Recommended):__

The startup scripts automatically START all development servers BUT
__DOES NOT OPEN THE APP IN BROWSER AUTOMATICALLY__.

```textbash
# Option 1: XTerm startup script (RECOMMENDED - WORKING)
./start-app-xterm.sh

# Option 2: Main startup script (NOW WORKING - FIXED)
./start-app.sh  # ✅ WORKING: Script now exits cleanly with timeout

# Option 3: Use npm scripts
npm run start:app:xterm    # XTerm version (RECOMMENDED)
npm run start:app          # Main script (NOW WORKING)
```text

__Prerequisites:__ uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (NOW WORKING - FIXED)

- __Status__: ✅ WORKING - Script now exits cleanly with timeout mechanism
- __Features__: 30-second timeout fallback to prevent hanging
- __Environment Support__: Works in both X11 and WSL2/headless environments
- __Background Mode__: Uses background processes in WSL2, terminal windows in X11
- __Logging__: Writes server logs to backend.log and frontend.log in WSL2 mode

### start-app-xterm.sh (RECOMMENDED - WORKING)

- __WSL2/XTerm Compatible__: Automatically detects environment and uses appropriate terminal
- __WSL2 Support__: Uses tmux sessions when X11 display is not available
- __XTerm Support__: Uses xterm windows when X11 display is available
- __Window Positioning__: Places backend and frontend terminals side-by-side (xterm) or separate sessions (tmux)
- __Font Configuration__: Uses readable DejaVu Sans Mono font (xterm mode)
- __Enhanced Display__: Better window titles and layout
- __Status__: ✅ FULLY TESTED - Both startup scripts working correctly

## What the Scripts Do

### ⏰ Timeout Mechanism

Both scripts now include a **30-second timeout fallback** to prevent hanging:

- **Normal Operation**: Scripts typically complete in 10-15 seconds
- **Safety Net**: 30-second timeout ensures scripts never hang indefinitely
- **AI Agent Friendly**: Prevents AI agents from getting stuck waiting for script completion
- **Graceful Exit**: Scripts exit cleanly after server verification or timeout

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

- __NOTIFIES USER TO LAUNCH BROWSER TO START THE APP__

__Access:__ <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

## Configuration

The scripts use __centralized configuration__ from `config/app.config.json` for consistency:

```textbash
# Configuration is loaded from config/app.config.json
# Backend: 127.0.0.1:8000
# Frontend: 127.0.0.1:3000
```text

This ensures:

- ✅ No port conflicts or dynamic allocation issues
- ✅ Consistent development environment
- ✅ Cloud deployment compatibility
- ✅ Easy troubleshooting
- ✅ Single source of truth for configuration

## Requirements

### System Requirements

- __Terminal Emulator__: `xterm` (for X11 environments) or `tmux` (for WSL2/headless environments)
- __Environment Detection__: Automatically detects WSL2/headless vs X11 environments
- __HTTP Client__: `curl` (for health checks)
- __Browser__: Any modern browser with `xdg-open`, `open`, or `start` support

### Development Dependencies

- __Python__: uv package manager with dependencies installed
- __Node.js__: Version 18.0.0+ with npm dependencies installed
- __Environment__: `.env` file with required API keys

## Error Handling

The scripts provide comprehensive error handling:

### Port Conflicts

```text
❌ Failed to start all servers within timeout period.
🔍 Troubleshooting:
  • Backend: Check if port 8000 is available
  • Frontend: Check if port 3000 is available
```text

### Missing Dependencies

```text
❌ No suitable terminal emulator found
WSL2/Headless: Please install tmux (sudo apt-get install tmux)
X11 Environment: Please install xterm (sudo apt-get install xterm)
```text

### Server Startup Issues

```text
🔍 Troubleshooting:
  • Backend: Verify Python dependencies are installed (uv install)
  • Backend: Check .env file has required API keys
  • Frontend: Verify Node.js dependencies are installed (npm install)
  • Frontend: Check if Node.js >= 18.0.0 is installed
```text

## Manual Cleanup

If you need to manually stop servers:

```textbash
# Kill backend server
pkill -f "uvicorn src.backend.main:app"

# Kill frontend server
pkill -f "npm run frontend:dev"
pkill -f "vite.*--mode development"

# For tmux sessions (WSL2)
tmux kill-session -t market-parser-backend
tmux kill-session -t market-parser-frontend

# For xterm windows (X11)
# Or close the terminal windows directly
```text

## WSL2/Tmux Usage

When running in WSL2 or headless environments, the script uses tmux sessions:

### Accessing Tmux Sessions

```textbash
# View backend server logs
tmux attach-session -t market-parser-backend

# View frontend server logs  
tmux attach-session -t market-parser-frontend

# List all sessions
tmux list-sessions

# Detach from current session (while inside tmux)
Ctrl+B, then D
```text

### Tmux Session Management

- Sessions run in the background and persist even if you close your terminal
- Use `tmux attach-session -t session-name` to reconnect to a session
- Use `tmux kill-session -t session-name` to stop a specific session
- Both servers must remain running for the application to work

## Troubleshooting

### Script Won't Run

```textbash
# Make sure scripts are executable
chmod +x start-app.sh start-app-xterm.sh

# Check script syntax
bash -n start-app.sh
```text

### Servers Start But Health Checks Fail

1. Check if ports 8000/3000 are accessible
2. Verify `.env` file has required API keys
3. Check terminal windows for specific error messages
4. Test manual server startup to identify issues

### Browser Won't Open Automatically

- The application will still be accessible at `http://127.0.0.1:3000`
- Script will show manual navigation for browser launch

## Success Output

When everything works correctly, you'll see:

```text
🎯 Market Parser One-Click Startup
Backend:  http://127.0.0.1:8000
Frontend: http://127.0.0.1:3000

🔄 Cleaning up existing dev servers...
✅ Cleanup complete
🚀 Starting backend server...
🚀 Starting frontend server...
✅ Verifying servers...
✓ Backend server is running at http://127.0.0.1:8000
✓ Frontend server is running at http://127.0.0.1:3000

🎉 All servers are running successfully!

📊 Backend API: http://127.0.0.1:8000
🌐 Frontend UI: http://127.0.0.1:3000

💡 Tip: Keep both terminal windows open to see server logs
🛑 To stop servers: Close both terminal windows or use Ctrl+C in each
```text
