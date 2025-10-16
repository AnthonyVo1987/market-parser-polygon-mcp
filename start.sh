#!/bin/bash
# Production startup script for App Runner

# Start FastAPI with production settings
exec uvicorn src.backend.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 2 \
  --timeout-keep-alive 120 \
  --no-access-log
