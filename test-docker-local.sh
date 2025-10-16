#!/bin/bash
# Test Docker build locally before deploying

set -e

echo "🔨 Building Docker image..."
docker build -t market-parser-test .

echo ""
echo "✅ Build successful!"
echo ""
echo "🚀 Starting container..."
echo "   Access at: http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

docker run -p 8000:8000 \
    -e POLYGON_API_KEY="${POLYGON_API_KEY}" \
    -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
    -e TRADIER_API_KEY="${TRADIER_API_KEY}" \
    -e FINNHUB_API_KEY="${FINNHUB_API_KEY}" \
    market-parser-test
