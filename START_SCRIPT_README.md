# One-Click Startup Script

The Market Parser project provides a one-click startup script that
automatically manages both backend and Gradio servers.

## Quick Start

__One-Click Application Startup (Recommended):__

The startup script automatically starts all development servers.

```bash
# Start backend + Gradio UI
chmod +x start-gradio.sh && ./start-gradio.sh
```

__Prerequisites:__ uv, API keys in .env

## Script Features

### start-gradio.sh

- __Status__: ✅ WORKING - Starts backend and Gradio servers
- __Environment Support__: Works in both X11 and WSL2/headless environments
- __Logging__: Server logs displayed in separate terminal windows
- __Health Checks__: Verifies both servers are running before completion

## What the Scripts Do

### ⏰ Timeout Mechanism

Both scripts now include a **30-second timeout fallback** to prevent hanging:

- **Normal Operation**: Scripts typically complete in 10-15 seconds
- **Safety Net**: 30-second timeout ensures scripts never hang indefinitely
- **AI Agent Friendly**: Prevents AI agents from getting stuck waiting for script completion
- **Graceful Exit**: Scripts exit cleanly after server verification or timeout

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, gradio)
- __Preserves MCP servers__ - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- __Backend__: Starts FastAPI server on `http://127.0.0.1:8000`
- __Gradio UI__: Starts Gradio ChatInterface on `http://127.0.0.1:7860`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent hard-coded ports (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies Gradio interface responds

### 🌐 Browser Access

- __NOTIFIES USER TO OPEN BROWSER WHEN SERVERS ARE READY__

__Access:__ <http://127.0.0.1:7860> (Gradio UI) or <http://127.0.0.1:8000> (API docs)

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
- __Environment__: `.env` file with required API keys

## Error Handling

The scripts provide comprehensive error handling:

### Port Conflicts

```text
❌ Failed to start all servers within timeout period.
🔍 Troubleshooting:
  • Backend: Check if port 8000 is available
  • Gradio UI: Check if port 7860 is available
```

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
  • Gradio UI: Verify Gradio dependencies are installed (uv install)
```

## Manual Cleanup

If you need to manually stop servers:

```bash
# Kill backend server
pkill -f "uvicorn src.backend.main:app"

# Kill Gradio server
pkill -f "gradio"
pkill -f "python.*gradio_ui.py"

# Or close the terminal windows directly
```

## Server Logs

When running the startup script, both servers display logs in separate terminal windows:

- Backend server logs show API requests and responses
- Gradio UI logs show chat interactions and performance metrics
- Both servers must remain running for the application to work

## Troubleshooting

### Script Won't Run

```bash
# Make sure script is executable
chmod +x start-gradio.sh

# Check script syntax
bash -n start-gradio.sh
```

### Servers Start But Health Checks Fail

1. Check if ports 8000/7860 are accessible
2. Verify `.env` file has required API keys
3. Check terminal windows for specific error messages
4. Test manual server startup to identify issues

### Accessing the Application

- Gradio UI: `http://127.0.0.1:7860`
- Backend API: `http://127.0.0.1:8000`

## Success Output

When everything works correctly, you'll see:

```text
🎯 Market Parser Gradio Startup
Backend:  http://127.0.0.1:8000
Gradio UI: http://127.0.0.1:7860

🔄 Cleaning up existing dev servers...
✅ Cleanup complete
🚀 Starting backend server...
🚀 Starting Gradio UI...
✅ Verifying servers...
✓ Backend server is running at http://127.0.0.1:8000
✓ Gradio UI is running at http://127.0.0.1:7860

🎉 All servers are running successfully!

📊 Backend API: http://127.0.0.1:8000
🌐 Gradio UI: http://127.0.0.1:7860

💡 Tip: Keep both terminal windows open to see server logs
🛑 To stop servers: Close both terminal windows or use Ctrl+C in each
```
