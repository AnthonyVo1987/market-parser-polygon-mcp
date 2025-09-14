# Root Command Reference Guide

This guide provides comprehensive documentation for all available commands in the Market Parser project. All commands can now be executed from the project root directory.

## Quick Start Commands

### 🚀 Essential Development Commands
```bash
# Start both backend and frontend in development mode
npm run dev
npm start            # Alias for npm run dev

# Check project status
npm run status       # Shows backend/frontend health status
npm run health       # Alias for npm run status

# Install all dependencies
npm run install:all  # Installs both backend and frontend dependencies

# Clean and reset everything
npm run reset        # Full clean, install, and start development
```

## 🔧 Development Commands

### Combined Development
```bash
npm run dev              # Backend (uvicorn) + Frontend (vite) with concurrently
npm run start            # Alias for npm run dev
npm run dev:full         # Backend (python server) + Frontend (vite)
npm run dev:frontend     # Frontend only
npm run dev:backend      # Backend only
```

### Backend Development
```bash
npm run backend:dev      # Start FastAPI with uvicorn and hot reload
npm run backend:server   # Start built-in Python server with settings
npm run backend:cli      # Start CLI interface for manual testing
npm run backend:install  # Install Python dependencies with uv
```

### Frontend Development
```bash
npm run frontend:install       # Install Node.js dependencies
npm run frontend:dev           # Development server (default mode)
npm run frontend:dev:staging   # Development server (staging config)
npm run frontend:dev:production # Development server (production config)
npm run frontend:preview       # Preview built application
```

## 🏗️ Build & Analysis Commands

### Building
```bash
npm run build                    # Production build (alias for frontend:build)
npm run build:all               # Build all components (currently frontend only)
npm run build:dev               # Development build
npm run build:staging           # Staging build
npm run frontend:build          # Production build
npm run frontend:build:staging  # Staging build
npm run frontend:build:development # Development build
```

### Bundle Analysis
```bash
npm run analyze                 # Bundle analysis for production
npm run analyze:visualizer      # Visual bundle analyzer with charts
npm run analyze:staging         # Bundle analysis for staging
npm run analyze:development     # Bundle analysis for development
```

## 🧹 Code Quality Commands

### Linting & Formatting
```bash
npm run lint             # Run ESLint on TypeScript/React code
npm run lint:js          # Explicit JavaScript/TypeScript linting
npm run lint:fix         # Auto-fix ESLint issues where possible
npm run format           # Format code with Prettier
npm run format:js        # Explicit JavaScript/TypeScript formatting
npm run format:check     # Check code formatting without making changes
npm run type-check       # TypeScript type checking without emit
npm run check:all        # Run all quality checks (lint + format + type-check)
```

### Quality Check Summary
- `npm run check:all` runs: lint → format:check → type-check
- Use `npm run lint:fix` and `npm run format` to auto-fix issues
- `npm run type-check` validates TypeScript without building

## 🧪 Testing Commands

### Playwright Testing
```bash
npm run test                    # Run all Playwright tests (default)
npm run test:playwright         # Run Playwright tests in headless mode
npm run test:playwright:headed  # Run tests with browser UI visible
npm run test:playwright:debug   # Run tests with debugging capabilities
npm run test:playwright:ui      # Run tests with interactive UI mode
```

### PWA Testing
```bash
npm run test:pwa            # Test Progressive Web App functionality
npm run test:pwa:staging    # Test PWA with staging configuration
npm run test:pwa:production # Test PWA with production configuration
```

### Test Locations
- **Playwright Tests**: `/tests/playwright/` - Contains B001-B016 test suite
- **Test Results**: Stored in `test-results/` directory
- **Test Reports**: Generated in HTML format for detailed analysis

## ⚡ Performance & Lighthouse

### Performance Analysis
```bash
npm run lighthouse                    # Full Lighthouse audit
npm run lighthouse:collect           # Collect performance metrics only
npm run lighthouse:assert            # Assert performance thresholds
npm run lighthouse:upload            # Upload results to LHCI server
npm run lighthouse:live-server       # Production build + Lighthouse instructions
npm run lighthouse:live-server:staging # Staging build + Lighthouse instructions
```

### Lighthouse Workflow
1. Run `npm run lighthouse:live-server` to build and get setup instructions
2. Start Live Server from VS Code (as instructed)
3. Lighthouse will test performance, PWA features, and accessibility

## 🌐 Serving & Deployment

### Local Serving
```bash
npm run serve            # Build development + serve instructions
npm run serve:staging    # Build staging + serve instructions
npm run serve:production # Build production + serve instructions
```

### Cross-Device Testing
```bash
npm run cross-device:setup    # Production build + network access instructions
npm run cross-device:staging  # Staging build + network access instructions
npm run live-server:help      # Detailed Live Server configuration help
```

### Serving Workflow
1. Commands build the appropriate version and provide instructions
2. Use VS Code Live Server extension to serve built files
3. Different configurations available for development (5500), staging (5501), production (5502)
4. Network access configured for mobile device testing

## 🔧 Installation & Maintenance

### Installation
```bash
npm run install:all      # Install root + frontend dependencies
npm run install:backend  # Install Python dependencies only
npm run install:frontend # Install Node.js dependencies only
```

### Cleaning
```bash
npm run clean            # Remove node_modules, frontend/node_modules, dist, test-results
npm run clean:cache      # Remove various cache directories
npm run clean:install    # Clean + install all dependencies
npm run clean:full       # Clean + clean cache + install all dependencies
```

### Maintenance Workflow
- `npm run clean:full` for complete reset when having issues
- `npm run reset` for quick clean + install + start development
- Dependencies are automatically managed through `postinstall` hook

## 🛠️ Utility Commands

### Status & Health Monitoring
```bash
npm run status  # Check backend (8000) and frontend (3000) health
npm run health  # Alias for npm run status
npm run reset   # Clean + install + start development (full reset)
```

### Status Output Example
```
=== Backend Status ===
{"status":"healthy","message":"Financial Analysis API is running","timestamp":"...","version":"1.0.0"}
=== Frontend Status ===
Frontend running on http://localhost:3000
```

## 📁 Command Categories Summary

| Category | Commands | Purpose |
|----------|----------|---------|
| **Development** | `dev`, `start`, `dev:*` | Local development servers |
| **Backend** | `backend:*` | Python FastAPI and CLI operations |
| **Frontend** | `frontend:*` | React/Vite operations |
| **Quality** | `lint*`, `format*`, `type-check`, `check:all` | Code quality and standards |
| **Build** | `build*`, `analyze*` | Production builds and analysis |
| **Testing** | `test*`, `lighthouse*` | Automated testing and performance |
| **Serving** | `serve*`, `cross-device*` | Local serving and deployment |
| **Maintenance** | `install:*`, `clean*`, `reset` | Project maintenance |
| **Utility** | `status`, `health` | System monitoring |

## 🌟 Most Commonly Used Commands

### Daily Development Workflow
```bash
# Start development
npm run dev

# Check code quality
npm run check:all

# Fix code issues
npm run lint:fix
npm run format

# Run tests
npm run test

# Check system status
npm run status
```

### Deployment Preparation
```bash
# Clean install and build
npm run clean:install
npm run build

# Performance analysis
npm run analyze
npm run lighthouse

# Cross-device testing
npm run cross-device:setup
```

## 🚨 Command Proxy Strategy

All commands use the `cd directory && command` strategy to maintain:

- **Root-Level Access**: All commands work from project root
- **No Directory Navigation**: Developers never need to `cd` into subdirectories
- **Consistent Interface**: Same command patterns across all tools
- **Environment Isolation**: Each command runs in appropriate directory context

## 🔍 Troubleshooting Commands

### Common Issues & Solutions
```bash
# Dependency issues
npm run clean:full

# Port conflicts
npm run status  # Check what's running
npm run reset   # Clean restart

# Build issues
npm run clean && npm run build

# Test failures
npm run test:playwright:debug  # Debug specific test issues
```

### Environment Verification
```bash
# Check all systems
npm run status && npm run check:all

# Verify installations
npm run install:all
```

This command reference provides complete documentation for the root-level command proxy system, enabling efficient development workflows without directory navigation requirements.