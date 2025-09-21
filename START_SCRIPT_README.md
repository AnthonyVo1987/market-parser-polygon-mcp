# One-Click Startup Scripts

The Market Parser project provides one-click startup scripts that automatically manage development servers.

## Quick Start

__One-Click Application Startup (Recommended):__

The startup scripts automatically START all development servers BUT __DOES NOT OPEN THE APP IN BROWSER AUTOMATICALLY__.

```bash
# Option 1: Main startup script (recommended)
./start-app.sh

# Option 2: XTerm version for better terminal compatibility
./start-app-xterm.sh

# Option 3: Use npm scripts
npm run start:app          # Main script
npm run start:app:xterm    # XTerm version
```

__Prerequisites:__ uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (Main Script)

- __Terminal Support__: Tries `gnome-terminal` first, falls back to `xterm`
- __Cross-Platform__: Works on most Linux distributions and macOS
- __Automatic Fallback__: Gracefully handles missing terminal emulators

### start-app-xterm.sh (XTerm Version)

- __XTerm Focused__: Specifically designed for xterm users
- __Window Positioning__: Places backend and frontend terminals side-by-side
- __Font Configuration__: Uses readable DejaVu Sans Mono font
- __Enhanced Display__: Better window titles and layout

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

- __NOTIFIES USER TO LAUNCH BROWSER TO START THE APP__

__Access:__ <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

## Script Variants

### start-app.sh (Main Script)

- __Terminal Support__: Tries `gnome-terminal` first, falls back to `xterm`
- __Cross-Platform__: Works on most Linux distributions and macOS
- __Automatic Fallback__: Gracefully handles missing terminal emulators

### start-app-xterm.sh (XTerm Version)

- __XTerm Focused__: Specifically designed for xterm users
- __Window Positioning__: Places backend and frontend terminals side-by-side
- __Font Configuration__: Uses readable DejaVu Sans Mono font
- __Enhanced Display__: Better window titles and layout

## Configuration

The scripts use __centralized configuration__ from `config/app.config.json` for consistency:

```bash
# Configuration is loaded from config/app.config.json
# Backend: 127.0.0.1:8000
# Frontend: 127.0.0.1:3000
```

This ensures:

- ✅ No port conflicts or dynamic allocation issues
- ✅ Consistent development environment
- ✅ Cloud deployment compatibility
- ✅ Easy troubleshooting
- ✅ Single source of truth for configuration

## Requirements

### System Requirements

- __Terminal Emulator__: `gnome-terminal` or `xterm` (automatically detected)
- __HTTP Client__: `curl` (for health checks)
- __Browser__: Any modern browser with `xdg-open`, `open`, or `start` support

### Development Dependencies

- __Python__: uv package manager with dependencies installed
- __Node.js__: Version 18.0.0+ with npm dependencies installed
- __Environment__: `.env` file with required API keys

## Error Handling

The scripts provide comprehensive error handling:

### Port Conflicts

```
❌ Failed to start all servers within timeout period.
🔍 Troubleshooting:
  • Backend: Check if port 8000 is available
  • Frontend: Check if port 3000 is available
```

### Missing Dependencies

```
❌ No suitable terminal emulator found (gnome-terminal or xterm)
Please install gnome-terminal or xterm to use this script
```

### Server Startup Issues

```
🔍 Troubleshooting:
  • Backend: Verify Python dependencies are installed (uv install)
  • Backend: Check .env file has required API keys
  • Frontend: Verify Node.js dependencies are installed (npm install)
  • Frontend: Check if Node.js >= 18.0.0 is installed
```

## Manual Cleanup

If you need to manually stop servers:

```bash
# Kill backend server
pkill -f "uvicorn src.backend.main:app"

# Kill frontend server
pkill -f "npm run frontend:dev"
pkill -f "vite.*--mode development"

# Or close the terminal windows directly
```

## Troubleshooting

### Script Won't Run

```bash
# Make sure scripts are executable
chmod +x start-app.sh start-app-xterm.sh

# Check script syntax
bash -n start-app.sh
```

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

```
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
```
