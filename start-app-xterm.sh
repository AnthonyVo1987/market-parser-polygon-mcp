#!/bin/bash

# Market Parser - One-Click Application Startup Script (XTerm Version)
# This script manages all dev servers and launches the application using xterm

# Configuration (hard-coded for consistency)
BACKEND_HOST="127.0.0.1"
BACKEND_PORT="8000"
FRONTEND_HOST="127.0.0.1"
FRONTEND_PORT="3000"
FRONTEND_URL="http://${FRONTEND_HOST}:${FRONTEND_PORT}"
BACKEND_URL="http://${BACKEND_HOST}:${BACKEND_PORT}"

echo "🎯 Market Parser One-Click Startup (XTerm Version)"
echo "Backend:  ${BACKEND_URL}"
echo "Frontend: ${FRONTEND_URL}"
echo ""

# Check if xterm is available
if ! command -v xterm >/dev/null 2>&1; then
    echo "❌ xterm is not installed. Please install xterm:"
    echo "   Ubuntu/Debian: sudo apt-get install xterm"
    echo "   CentOS/RHEL: sudo yum install xterm"
    echo "   macOS: Install via Homebrew: brew install xterm"
    echo ""
    echo "Alternatively, use the main startup script: ./start-app.sh"
    exit 1
fi

# Step A: Kill existing dev servers (excluding MCP servers)
echo "🔄 Cleaning up existing dev servers..."
# Kill backend (uvicorn) - only target our specific main.py
pkill -f "uvicorn src.backend.main:app" 2>/dev/null
# Kill frontend (vite) - be careful not to kill other vite processes
pkill -f "vite.*--mode development" 2>/dev/null
pkill -f "npm run frontend:dev" 2>/dev/null
# Wait for processes to terminate
sleep 2
echo "✅ Cleanup complete"

# Step B: Start servers in separate xterm windows
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

# Step C: Health check - verify servers are running
echo "✅ Verifying servers..."
MAX_RETRIES=10
RETRY_COUNT=0
BACKEND_READY=false
FRONTEND_READY=false

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

    if [ "$BACKEND_READY" = true ] && [ "$FRONTEND_READY" = true ]; then
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 2
done

# Step D: Confirm servers are ready and provide manual launch instructions
if [ "$BACKEND_READY" = true ] && [ "$FRONTEND_READY" = true ]; then
    echo ""
    echo "🎉 All servers are running successfully!"
    echo ""
    echo "⚠️  IMPORTANT: Both servers are now running in separate xterm windows"
    echo "   • Backend Server: Running in left xterm window"
    echo "   • Frontend Server: Running in right xterm window"
    echo ""
    echo "🔴 CRITICAL: BOTH servers MUST remain running for the app to work!"
    echo "   • Keep both xterm windows open at all times"
    echo "   • Do NOT close the xterm windows while using the app"
    echo "   • To stop servers: Close both xterm windows or use Ctrl+C in each"
    echo ""
    echo "🌐 MANUAL BROWSER LAUNCH REQUIRED:"
    echo "   This script does NOT launch the actual application"
    echo "   You must manually open your browser and navigate to:"
    echo "   ${FRONTEND_URL}"
    echo ""
    echo "📊 Server URLs:"
    echo "   • Backend API: ${BACKEND_URL}"
    echo "   • Frontend UI: ${FRONTEND_URL}"
    echo ""
    echo "🎨 XTerm Features:"
    echo "  • Positioned windows side by side for easy monitoring"
    echo "  • Readable font (DejaVu Sans Mono, size 12)"
    echo "  • Proper window titles for identification"
    echo ""
    echo "✅ Setup complete! Script exiting - servers will continue running in their xterm windows."
    echo ""
    exit 0
else
    echo ""
    echo "❌ Failed to start all servers within timeout period."
    echo "Please check the xterm windows for error messages."
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
    echo ""
    exit 1
fi