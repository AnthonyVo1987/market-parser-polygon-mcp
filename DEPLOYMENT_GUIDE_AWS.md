# Market Parser – AWS Deployment Guide

This guide scopes options and provides a recommended path to deploy the app as a production web service on AWS.

## Current Stack
- Python agent using Pydantic AI (OpenAI Responses API)
- MCP Polygon server (currently launched via `uvx` in CLI)
- CLI and Gradio GUI (optional)
- Session-based chat with token/cost tracking

## Deployment Options

### 1) Python-only service (Recommended initial path)
- Containerize a FastAPI (ASGI) backend that:
  - Starts the Polygon MCP server once at startup
  - Exposes chat endpoints (REST and/or WS/SSE for streaming)
  - Tracks per-message and session token/cost
  - Optionally serves the Gradio GUI at `/gui` (internal/demo)
- Where to run:
  - AWS App Runner (simplest to operate)
  - Or ECS Fargate (more control)
- Pros: Minimal rewrite; reuse the agent/MCP; good observability via CloudWatch
- Cons: If you keep Gradio only, UX is less customizable than a React frontend

### 2) Python backend + React (Next.js) frontend
- FastAPI backend as above
- Next.js chat UI (streaming), deployed to AWS Amplify Hosting or S3+CloudFront
- Pros: Best UX and future flexibility
- Cons: Additional work: new frontend, streaming protocol, auth, CI/CD for 2 apps

### 3) Gradio-only container
- Keep `chat_ui.py` as the primary UI and containerize
- Pros: Fastest to ship
- Cons: Less enterprise polish and customization

### Not recommended for MCP
- Serverless (Lambda/API Gateway): MCP requires a long-lived server; cold starts + per-request spawn are fragile/slow
- EKS (Kubernetes): powerful but overkill initially; prefer App Runner/ECS first

---

## Recommended Architecture (Phase 1)

1) Build a Python container (FastAPI)
- Startup: launch MCP Polygon server once and keep running
- Endpoints:
  - `POST /chat` – single-turn chat (returns full response when done)
  - `GET /healthz` – health probe
  - (Optional) `GET /stream` – SSE or WebSocket streaming of assistant output
- Optionally mount Gradio UI at `/gui`

2) AWS App Runner Deployment
- Connect to ECR or GitHub
- Configure environment variables/secrets
- Monitor logs in CloudWatch

3) Secrets & Config
- OPENAI_API_KEY and POLYGON_API_KEY via AWS Secrets Manager → injected as environment variables
- Pricing vars for cost estimation via env:
  - Per 1M tokens: `OPENAI_GPT5_NANO_INPUT_PRICE_PER_1M`, `OPENAI_GPT5_NANO_OUTPUT_PRICE_PER_1M`
  - Or per token: `OPENAI_GPT5_NANO_INPUT_PRICE_PER_TOKEN`, `OPENAI_GPT5_NANO_OUTPUT_PRICE_PER_TOKEN`

---

## Dockerization Notes

- Replace `uvx` for MCP in containers by installing the Polygon MCP server directly during image build.
  - Example (in Dockerfile build step):
    - `pip install "git+https://github.com/polygon-io/mcp_polygon@v0.4.0"`
  - Update your MCP startup code from:
    - `command="uvx" ... args=["--from", "git+https://...", "mcp_polygon"]`
  - To:
    - `command="mcp_polygon"` with no args (or appropriate CLI args if needed)

Minimal Dockerfile outline (example):

```Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . /app

# Install system deps if needed
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "git+https://github.com/polygon-io/mcp_polygon@v0.4.0" \
    && pip install --no-cache-dir -r <(python - <<'PY'
from pathlib import Path
import tomllib
cfg = tomllib.loads(Path('pyproject.toml').read_text())
print('\n'.join(cfg['project']['dependencies']))
PY
)

# Install web server
RUN pip install --no-cache-dir uvicorn fastapi

EXPOSE 8080
# CMD: replace with your ASGI app entrypoint (e.g., app.main:app)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## FastAPI Service (Implementation Hints)

- App lifecycle
  - On startup event: launch MCP server via `MCPServerStdio(...)` and keep the toolset open
  - Store a single Agent instance (thread-safe usage) or create per-request if needed
- Endpoints
  - `POST /chat` request body: `{ "message": string, "session_id": string }`
  - Return: `{ "output": string, "usage": { ... }, "tools_used": [ ... ] }`
  - Maintain per-session totals in memory first; move to Redis (ElastiCache) for horizontal scaling
- Logging
  - Log model name, usage (tokens), tool calls, duration, request id
  - Send to stdout; App Runner/ECS ship logs to CloudWatch automatically

---

## AWS App Runner – Quick Steps

1) Build & push image to ECR (or connect repo directly)
2) Create App Runner service
   - Image source: ECR (or GitHub)
   - Runtime: Container
   - Port: 8080
   - Env vars: `OPENAI_API_KEY`, `POLYGON_API_KEY`, pricing vars
   - Health check: `/healthz`
3) Observe logs in CloudWatch; validate `/healthz` and `/chat`

---

## ECS Fargate – Quick Steps (Alternative)

- Create ECR repo and push image
- Task Definition with required env vars
- Service on Fargate (public/private as needed)
- ALB for HTTP routing + health checks
- CloudWatch logs via FireLens (default AWS logs driver works too)

---

## CI/CD (GitHub Actions → ECR → App Runner)

High-level workflow:
- On push to `master`:
  - Build Docker image
  - Push to ECR
  - Update App Runner service to latest image

Secrets needed in GitHub Actions: AWS credentials, AWS account/region, ECR repo name.

---

## Local Testing

- CLI: `uv run market_parser_demo.py`
- GUI: `uv run chat_ui.py` → open `http://127.0.0.1:7860`
- FastAPI (once implemented): `uvicorn app:app --host 0.0.0.0 --port 8080`

Ensure `.env` at project root with keys/pricing, or set env vars before launching.

---

## Security & Cost Notes
- Use AWS Secrets Manager/Parameter Store; avoid hardcoding keys in Docker images
- Restrict outbound network if desired (VPC endpoints, egress controls)
- Consider rate limiting to prevent abuse
- Monitor token usage/costs; add budgets/alerts in AWS

---

## Phase 2 (Frontend UX)
- Add a Next.js chat UI with streaming
- Deployed via Amplify Hosting or S3+CloudFront
- Keep FastAPI backend; reuse endpoints

---

## Summary
- Start with a Python-only container (FastAPI) on App Runner for a quick, reliable deployment
- Keep MCP running within the container; migrate away from `uvx` at runtime
- Add React UI later as needed
