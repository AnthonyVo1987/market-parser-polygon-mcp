# Multi-stage build for Market Parser App Runner deployment
# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig*.json ./
COPY vite.config.ts ./
COPY postcss.config.js ./
COPY index.html ./

# Copy config and source
COPY config/ ./config/
COPY src/frontend/ ./src/frontend/
COPY public/ ./public/

# Install dependencies and build
RUN npm ci --only=production
RUN npm run build

# Stage 2: Python backend with frontend static files
FROM python:3.10-slim

WORKDIR /app

# Install uv for Python package management
RUN pip install --no-cache-dir uv

# Copy Python dependencies
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy backend source
COPY src/backend/ ./src/backend/
COPY config/ ./config/

# Use production config
RUN cp config/app.config.production.json config/app.config.json

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/dist ./dist

# Expose port (App Runner will map this)
EXPOSE 8000

# Start script
COPY start.sh ./
RUN chmod +x start.sh

CMD ["./start.sh"]
