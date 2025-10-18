#!/bin/bash

# Market Parser - One-Click Application Startup Script
# This script manages all dev servers and launches the application
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
GRADIO_HOST="127.0.0.1"
GRADIO_PORT="7860"
GRADIO_URL="http://${GRADIO_HOST}:${GRADIO_PORT}"
BACKEND_URL="http://${BACKEND_HOST}:${BACKEND_PORT}"

echo "🎯 Market Parser One-Click Startup"
echo "Backend:  ${BACKEND_URL}"
echo "Gradio:   ${GRADIO_URL}"
echo ""

# Step A: Kill existing dev servers (excluding MCP servers)
echo "🔄 Cleaning up existing dev servers..."
# Kill backend (uvicorn) - only target our specific main.py
pkill -f "uvicorn src.backend.main:app" 2>/dev/null
# Kill Gradio server
pkill -f "gradio_app.py" 2>/dev/null
# Wait for processes to terminate
sleep 2
echo "✅ Cleanup complete"

# Step B: Start servers in separate terminals or background
echo "🚀 Starting backend server..."

# Check if we can use terminal emulators (X display available)
if [ -n "$DISPLAY" ] && command -v gnome-terminal >/dev/null 2>&1; then
    gnome-terminal --title="Backend Server - Market Parser" -e bash -c "
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
elif [ -n "$DISPLAY" ] && command -v xterm >/dev/null 2>&1; then
    xterm -T "Backend Server - Market Parser" -e bash -c "
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
else
    # No X display available (WSL2 without X11 forwarding) - start in background
    echo "⚠️  No X display available - starting servers in background"
    echo "   Backend logs will be written to backend.log"
    nohup uv run uvicorn src.backend.main:app --host $BACKEND_HOST --port $BACKEND_PORT --reload > backend.log 2>&1 &
    BACKEND_PID=$!
    echo "   Backend PID: $BACKEND_PID"
fi

sleep 3  # Wait for backend to initialize

echo "🚀 Starting Gradio server..."
if [ -n "$DISPLAY" ] && command -v gnome-terminal >/dev/null 2>&1; then
    gnome-terminal --title="Gradio Server - Market Parser" -e bash -c "
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
elif [ -n "$DISPLAY" ] && command -v xterm >/dev/null 2>&1; then
    xterm -T "Gradio Server - Market Parser" -e bash -c "
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
else
    # No X display available (WSL2 without X11 forwarding) - start in background
    echo "   Gradio logs will be written to gradio.log"
    nohup uv run python src/backend/gradio_app.py > gradio.log 2>&1 &
    GRADIO_PID=$!
    echo "   Gradio PID: $GRADIO_PID"
fi

sleep 5  # Wait for Gradio to initialize

# Step C: Health check - verify servers are running
echo "✅ Verifying servers..."
MAX_RETRIES=10
RETRY_COUNT=0
BACKEND_READY=false
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

    if [ "$BACKEND_READY" = true ] && [ "$GRADIO_READY" = true ]; then
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 2
done

# Step D: Confirm servers are ready and provide manual launch instructions
if [ "$BACKEND_READY" = true ] && [ "$GRADIO_READY" = true ]; then
    echo ""
    echo "🎉 All servers are running successfully!"
    echo ""
    if [ -n "$DISPLAY" ]; then
        echo "⚠️  IMPORTANT: All servers are now running in separate terminal windows"
        echo "   • Backend Server: Running in one terminal window"
        echo "   • Gradio Server: Running in another terminal window"
        echo ""
        echo "🔴 CRITICAL: ALL servers MUST remain running for the app to work!"
        echo "   • Keep all terminal windows open at all times"
        echo "   • Do NOT close the terminal windows while using the app"
        echo "   • To stop servers: Close all terminal windows or use Ctrl+C in each"
    else
        echo "⚠️  IMPORTANT: All servers are now running in the background"
        echo "   • Backend Server: PID $BACKEND_PID (logs in backend.log)"
        echo "   • Gradio Server: PID $GRADIO_PID (logs in gradio.log)"
        echo ""
        echo "🔴 CRITICAL: ALL servers MUST remain running for the app to work!"
        echo "   • To stop servers: kill $BACKEND_PID $GRADIO_PID"
        echo "   • To view logs: tail -f backend.log gradio.log"
    fi
    echo ""
    echo "🌐 MANUAL BROWSER LAUNCH REQUIRED:"
    echo "   This script does NOT launch the actual application"
    echo "   You must manually open your browser and navigate to:"
    echo ""
    echo "   • Gradio UI: ${GRADIO_URL}"
    echo ""
    echo "📊 Server URLs:"
    echo "   • Backend API: ${BACKEND_URL}"
    echo "   • Gradio Frontend: ${GRADIO_URL}"
    echo ""
    echo "✅ Setup complete! Script exiting - servers will continue running in their terminals."
    echo ""
    cleanup_and_exit 0
else
    echo ""
    echo "❌ Failed to start all servers within timeout period."
    echo "Please check the terminal windows for error messages."
    echo ""
    echo "🔍 Troubleshooting:"
    if [ "$BACKEND_READY" = false ]; then
        echo "  • Backend: Check if port $BACKEND_PORT is available"
        echo "  • Backend: Verify Python dependencies are installed (uv install)"
        echo "  • Backend: Check .env file has required API keys"
    fi
    if [ "$GRADIO_READY" = false ]; then
        echo "  • Gradio: Check if port $GRADIO_PORT is available"
        echo "  • Gradio: Verify Python dependencies are installed (uv sync)"
        echo "  • Gradio: Check .env file has required API keys"
    fi
    echo ""
    cleanup_and_exit 1
fi