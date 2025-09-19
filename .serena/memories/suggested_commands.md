# Essential Development Commands

## Application Startup (One-Click)
```bash
./start-app.sh                # Main startup script (recommended)
./start-app-xterm.sh          # XTerm version
npm run start:app             # Main script via npm
npm run start:app:xterm       # XTerm version via npm
```

## Development Commands
```bash
npm run dev                   # Start both backend and frontend
npm run backend:dev           # Backend only (FastAPI on port 8000)
npm run frontend:dev          # Frontend only (Vite on port 3000)
npm run backend:cli           # CLI interface
```

## Code Quality
```bash
npm run lint                  # All linting (Python + JS/TS)
npm run lint:python           # Python linting only
npm run lint:js              # JavaScript/TypeScript only
npm run lint:fix             # Auto-fix all issues
npm run format               # Format JS/TS code
npm run type-check           # TypeScript type checking
```

## Build & Serve
```bash
npm run build                # Production build
npm run serve                # Development build + Live Server instructions
npm run serve:production     # Production build + Live Server instructions
```

## Health & Status
```bash
npm run status               # Check backend/frontend health
curl http://localhost:8000/health    # Backend health endpoint
curl http://localhost:3000           # Frontend availability
```

## Installation & Maintenance
```bash
uv install                   # Install Python dependencies
npm install                  # Install Node.js dependencies
npm run clean                # Remove node_modules and dist
npm run reset                # Clean + reinstall + start dev
```

## System Utilities (Linux)
```bash
ls -la                       # List files with details
cd /path/to/directory        # Change directory
grep -r "pattern" .          # Search for patterns
find . -name "*.py"          # Find files by pattern
ps aux | grep uvicorn        # Check running processes
kill -9 <PID>               # Kill process by PID
```