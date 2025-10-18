#!/bin/bash

# Market Parser - One-Click Application Startup Script (WSL2/XTerm Compatible)
# This script manages all dev servers and launches the application using tmux (WSL2) or xterm (X11)
# Features: 30-second timeout fallback to prevent hanging

# Set up timeout mechanism (30 seconds)
TIMEOUT_DURATION=30
SCRIPT_PID=$$
TIMEOUT_PID=""

# Function to cleanup and exit
cleanup_and_exit() {
    local exit_code=${1:-0}
    # Kill timeout process if it exists
    if [ -n "$TIMEOUT_PID" ]; then
        kill $TIMEOUT_PID 2>/dev/null
    fi
    exit $exit_code
}

# Set up timeout process
(
    sleep $TIMEOUT_DURATION
    echo ""
    echo "⏰ TIMEOUT: Script exceeded ${TIMEOUT_DURATION}s - forcing exit"
    echo "   This is a safety mechanism to prevent hanging"
    kill $SCRIPT_PID 2>/dev/null
) &
TIMEOUT_PID=$!

# Trap signals to cleanup
trap 'cleanup_and_exit 1' INT TERM

# Configuration (hard-coded for consistency)
BACKEND_HOST="127.0.0.1"
BACKEND_PORT="8000"
FRONTEND_HOST="127.0.0.1"
FRONTEND_PORT="3000"
GRADIO_HOST="127.0.0.1"
GRADIO_PORT="7860"
FRONTEND_URL="http://${FRONTEND_HOST}:${FRONTEND_PORT}"
GRADIO_URL="http://${GRADIO_HOST}:${GRADIO_PORT}"
BACKEND_URL="http://${BACKEND_HOST}:${BACKEND_PORT}"

echo "🎯 Market Parser One-Click Startup (WSL2/XTerm Compatible)"
echo "Backend:  ${BACKEND_URL}"
echo "Frontend: ${FRONTEND_URL}"
echo "Gradio:   ${GRADIO_URL} ⭐ NEW"
echo ""

# Check environment and available terminal emulators
USE_TMUX=false
USE_XTERM=false

# Check if we're in WSL2 or similar environment without X11 display
if [ -z "$DISPLAY" ]; then
    echo "🔍 WSL2/Headless environment detected (no DISPLAY set)"
    if command -v tmux >/dev/null 2>&1; then
        USE_TMUX=true
        echo "✅ Using tmux for session management"
    else
        echo "❌ tmux is not installed. Please install tmux:"
        echo "   Ubuntu/Debian: sudo apt-get install tmux"
        echo "   CentOS/RHEL: sudo yum install tmux"
        echo "   macOS: Install via Homebrew: brew install tmux"
        exit 1
    fi
else
    # We have X11 display, check for xterm
    if command -v xterm >/dev/null 2>&1; then
        USE_XTERM=true
        echo "✅ Using xterm for window management"
    else
        echo "❌ xterm is not installed. Please install xterm:"
        echo "   Ubuntu/Debian: sudo apt-get install xterm"
        echo "   CentOS/RHEL: sudo yum install xterm"
        echo "   macOS: Install via Homebrew: brew install xterm"
        echo ""
        echo "Alternatively, use the main startup script: chmod +x start-app.sh && ./start-app.sh"
        exit 1
    fi
fi

# Step A: Kill existing dev servers (excluding MCP servers)
echo "🔄 Cleaning up existing dev servers..."
# Kill backend (uvicorn) - only target our specific main.py
pkill -f "uvicorn src.backend.main:app" 2>/dev/null
# Kill frontend (vite) - be careful not to kill other vite processes
pkill -f "vite.*--mode development" 2>/dev/null
pkill -f "npm run frontend:dev" 2>/dev/null
# Kill Gradio server
pkill -f "gradio_app.py" 2>/dev/null
# Wait for processes to terminate
sleep 2
echo "✅ Cleanup complete"

# Step B: Start servers in separate sessions
if [ "$USE_TMUX" = true ]; then
    # Clean up any existing tmux sessions
    tmux kill-session -t "market-parser-backend" 2>/dev/null
    tmux kill-session -t "market-parser-frontend" 2>/dev/null
    tmux kill-session -t "market-parser-gradio" 2>/dev/null
    
    echo "🚀 Starting backend server in tmux session..."
    tmux new-session -d -s "market-parser-backend" -c "$(pwd)" "
        echo '🔧 Starting FastAPI backend server...'
        echo 'Host: $BACKEND_HOST'
        echo 'Port: $BACKEND_PORT'
        echo 'Session: market-parser-backend'
        echo ''
        uv run uvicorn src.backend.main:app --host $BACKEND_HOST --port $BACKEND_PORT --reload
    "
    
    sleep 3  # Wait for backend to initialize
    
    echo "🚀 Starting frontend server in tmux session..."
    tmux new-session -d -s "market-parser-frontend" -c "$(pwd)" "
        echo '🔧 Starting Vite frontend server...'
        echo 'Host: $FRONTEND_HOST'
        echo 'Port: $FRONTEND_PORT'
        echo 'Session: market-parser-frontend'
        echo ''
        npm run frontend:dev
    "
    
    sleep 5  # Wait for frontend to initialize

    echo "🚀 Starting Gradio server in tmux session..."
    tmux new-session -d -s "market-parser-gradio" -c "$(pwd)" "
        echo '🎨 Starting Gradio frontend server...'
        echo 'Host: $GRADIO_HOST'
        echo 'Port: $GRADIO_PORT'
        echo 'Session: market-parser-gradio'
        echo ''
        uv run python src/backend/gradio_app.py
    "

    sleep 5  # Wait for Gradio to initialize

elif [ "$USE_XTERM" = true ]; then
    echo "🚀 Starting backend server in xterm..."
    xterm -T "Backend Server - Market Parser" -fa 'DejaVu Sans Mono' -fs 12 -geometry 120x40+0+0 -e bash -c "
        echo '🔧 Starting FastAPI backend server...'
        echo 'Host: $BACKEND_HOST'
        echo 'Port: $BACKEND_PORT'
        echo ''
        uv run uvicorn src.backend.main:app --host $BACKEND_HOST --port $BACKEND_PORT --reload
        echo ''
        echo '⚠️ Backend server stopped. Press Enter to close terminal.'
        read
    " &
    BACKEND_PID=$!
    
    sleep 3  # Wait for backend to initialize
    
    echo "🚀 Starting frontend server in xterm..."
    xterm -T "Frontend Server - Market Parser" -fa 'DejaVu Sans Mono' -fs 12 -geometry 120x40+600+0 -e bash -c "
        echo '🔧 Starting Vite frontend server...'
        echo 'Host: $FRONTEND_HOST'
        echo 'Port: $FRONTEND_PORT'
        echo ''
        npm run frontend:dev
        echo ''
        echo '⚠️ Frontend server stopped. Press Enter to close terminal.'
        read
    " &
    FRONTEND_PID=$!
    
    sleep 5  # Wait for frontend to initialize

    echo "🚀 Starting Gradio server in xterm..."
    xterm -T "Gradio Frontend (Port 7860) - Market Parser" -fa 'DejaVu Sans Mono' -fs 12 -geometry 120x40+1200+0 -e bash -c "
        echo '🎨 Starting Gradio frontend server...'
        echo 'Host: $GRADIO_HOST'
        echo 'Port: $GRADIO_PORT'
        echo ''
        uv run python src/backend/gradio_app.py
        echo ''
        echo '⚠️ Gradio server stopped. Press Enter to close terminal.'
        read
    " &
    GRADIO_PID=$!

    sleep 5  # Wait for Gradio to initialize
fi

# Step C: Health check - verify servers are running
echo "✅ Verifying servers..."
MAX_RETRIES=10
RETRY_COUNT=0
BACKEND_READY=false
FRONTEND_READY=false
GRADIO_READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    # Check backend
    if curl -s "${BACKEND_URL}/health" > /dev/null 2>&1; then
        if [ "$BACKEND_READY" = false ]; then
            echo "✓ Backend server is running at ${BACKEND_URL}"
        fi
        BACKEND_READY=true
    else
        echo "⏳ Waiting for backend server... (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)"
        BACKEND_READY=false
    fi

    # Check frontend
    if curl -s "${FRONTEND_URL}" > /dev/null 2>&1; then
        if [ "$FRONTEND_READY" = false ]; then
            echo "✓ Frontend server is running at ${FRONTEND_URL}"
        fi
        FRONTEND_READY=true
    else
        echo "⏳ Waiting for frontend server... (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)"
        FRONTEND_READY=false
    fi

    # Check Gradio
    if curl -s "${GRADIO_URL}" > /dev/null 2>&1; then
        if [ "$GRADIO_READY" = false ]; then
            echo "✓ Gradio server is running at ${GRADIO_URL}"
        fi
        GRADIO_READY=true
    else
        echo "⏳ Waiting for Gradio server... (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)"
        GRADIO_READY=false
    fi

    if [ "$BACKEND_READY" = true ] && [ "$FRONTEND_READY" = true ] && [ "$GRADIO_READY" = true ]; then
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 2
done

# Step D: Confirm servers are ready and provide manual launch instructions
if [ "$BACKEND_READY" = true ] && [ "$FRONTEND_READY" = true ] && [ "$GRADIO_READY" = true ]; then
    echo ""
    echo "🎉 All servers are running successfully!"
    echo ""
    
    if [ "$USE_TMUX" = true ]; then
        echo "⚠️  IMPORTANT: All servers are now running in separate tmux sessions"
        echo "   • Backend Server: Running in tmux session 'market-parser-backend'"
        echo "   • Frontend Server: Running in tmux session 'market-parser-frontend'"
        echo "   • Gradio Server: Running in tmux session 'market-parser-gradio' ⭐ NEW"
        echo ""
        echo "🔴 CRITICAL: ALL servers MUST remain running for the app to work!"
        echo "   • Keep all tmux sessions running at all times"
        echo "   • Do NOT kill the tmux sessions while using the app"
        echo "   • To stop servers: Use 'tmux kill-session -t session-name' or Ctrl+C in each session"
        echo ""
        echo "📱 TMUX SESSION ACCESS:"
        echo "   • View backend logs: tmux attach-session -t market-parser-backend"
        echo "   • View frontend logs: tmux attach-session -t market-parser-frontend"
        echo "   • View Gradio logs: tmux attach-session -t market-parser-gradio ⭐ NEW"
        echo "   • List all sessions: tmux list-sessions"
        echo "   • Detach from session: Ctrl+B, then D"
        echo ""
    elif [ "$USE_XTERM" = true ]; then
        echo "⚠️  IMPORTANT: All servers are now running in separate xterm windows"
        echo "   • Backend Server: Running in left xterm window (Port 8000)"
        echo "   • Frontend Server: Running in middle xterm window (Port 3000)"
        echo "   • Gradio Server: Running in right xterm window (Port 7860) ⭐ NEW"
        echo ""
        echo "🔴 CRITICAL: ALL servers MUST remain running for the app to work!"
        echo "   • Keep all xterm windows open at all times"
        echo "   • Do NOT close the xterm windows while using the app"
        echo "   • To stop servers: Close all xterm windows or use Ctrl+C in each"
        echo ""
        echo "🎨 XTerm Features:"
        echo "  • Three windows: Backend (left), React (middle), Gradio (right)"
        echo "  • Readable font (DejaVu Sans Mono, size 12)"
        echo "  • Proper window titles for identification"
        echo ""
    fi
    
    echo "🌐 MANUAL BROWSER LAUNCH REQUIRED:"
    echo "   This script does NOT launch the actual application"
    echo "   You must manually open your browser and navigate to ONE of:"
    echo ""
    echo "   • React GUI: ${FRONTEND_URL}"
    echo "   • Gradio GUI: ${GRADIO_URL} ⭐ NEW"
    echo ""
    echo "📊 All Server URLs:"
    echo "   • Backend API: ${BACKEND_URL}"
    echo "   • React Frontend: ${FRONTEND_URL}"
    echo "   • Gradio Frontend: ${GRADIO_URL} ⭐ NEW"
    echo ""
    
    if [ "$USE_TMUX" = true ]; then
        echo "✅ Setup complete! Script exiting - servers will continue running in their tmux sessions."
    else
        echo "✅ Setup complete! Script exiting - servers will continue running in their xterm windows."
    fi
    echo ""
    cleanup_and_exit 0
else
    echo ""
    echo "❌ Failed to start all servers within timeout period."
    if [ "$USE_TMUX" = true ]; then
        echo "Please check the tmux sessions for error messages:"
        echo "  • Backend: tmux attach-session -t market-parser-backend"
        echo "  • Frontend: tmux attach-session -t market-parser-frontend"
        echo "  • Gradio: tmux attach-session -t market-parser-gradio"
    else
        echo "Please check the xterm windows for error messages."
    fi
    echo ""
    echo "🔍 Troubleshooting:"
    if [ "$BACKEND_READY" = false ]; then
        echo "  • Backend: Check if port $BACKEND_PORT is available"
        echo "  • Backend: Verify Python dependencies are installed (uv install)"
        echo "  • Backend: Check .env file has required API keys"
    fi
    if [ "$FRONTEND_READY" = false ]; then
        echo "  • Frontend: Check if port $FRONTEND_PORT is available"
        echo "  • Frontend: Verify Node.js dependencies are installed (npm install)"
        echo "  • Frontend: Check if Node.js >= 18.0.0 is installed"
    fi
    if [ "$GRADIO_READY" = false ]; then
        echo "  • Gradio: Check if port $GRADIO_PORT is available"
        echo "  • Gradio: Verify Python dependencies are installed (uv sync)"
        echo "  • Gradio: Check .env file has required API keys"
    fi
    echo ""
    cleanup_and_exit 1
fi