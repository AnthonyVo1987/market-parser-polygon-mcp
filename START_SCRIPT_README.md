# One-Click Startup Scripts

The Market Parser project provides one-click startup scripts that automatically manage development servers and launch the application.

## Quick Start

```bash
# Option 1: Use npm script (recommended)
npm run start:app

# Option 2: Run script directly
./start-app.sh

# Option 3: Use xterm version for better terminal compatibility
npm run start:app:xterm
# or
./start-app-xterm.sh
```

## What the Scripts Do

### 🔄 Server Cleanup
- Kills existing development servers (uvicorn, vite)
- **Preserves MCP servers** - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup
- **Backend**: Starts FastAPI server on `http://127.0.0.1:8000`
- **Frontend**: Starts Vite dev server on `http://127.0.0.1:3000`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent ports from centralized configuration (no dynamic allocation)

### ✅ Health Verification
- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch
- **Automatically opens the application in your default browser** after server confirmation
- Supports multiple browser opening methods (xdg-open, open, start)
- Cross-platform compatibility (Linux, macOS, Windows/WSL)
- Shows helpful success message with URLs
- **True one-click experience** - no manual browser navigation required

## Script Variants

### start-app.sh (Main Script)
- **Terminal Support**: Tries `gnome-terminal` first, falls back to `xterm`
- **Cross-Platform**: Works on most Linux distributions and macOS
- **Automatic Fallback**: Gracefully handles missing terminal emulators

### start-app-xterm.sh (XTerm Version)
- **XTerm Focused**: Specifically designed for xterm users
- **Window Positioning**: Places backend and frontend terminals side-by-side
- **Font Configuration**: Uses readable DejaVu Sans Mono font
- **Enhanced Display**: Better window titles and layout

## Configuration

The scripts use **centralized configuration** from `config/app.config.json` for consistency:

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
- **Terminal Emulator**: `gnome-terminal` or `xterm` (automatically detected)
- **HTTP Client**: `curl` (for health checks)
- **Browser**: Any modern browser with `xdg-open`, `open`, or `start` support

### Development Dependencies
- **Python**: uv package manager with dependencies installed
- **Node.js**: Version 18.0.0+ with npm dependencies installed
- **Environment**: `.env` file with required API keys

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
- Script will show manual navigation instructions if automatic browser launch fails
- Check if `xdg-open`, `open`, or `start` commands are available on your system

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
🌐 Opening application in browser...

✨ Application started successfully!
📊 Backend API: http://127.0.0.1:8000
🌐 Frontend UI: http://127.0.0.1:3000

💡 Tip: Keep both terminal windows open to see server logs
🛑 To stop servers: Close both terminal windows or use Ctrl+C in each
```

## Integration with Development Workflow

The startup scripts integrate seamlessly with existing npm commands:

```bash
# Start everything with one command
npm run start:app

# Check server status
npm run health

# Reset everything (clean + start)
npm run reset
```

This provides a true **one-click development experience** that eliminates the complexity of managing multiple servers and processes manually.