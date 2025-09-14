# Comprehensive Migration Execution Plan
## Consolidation: Current Structure → src/backend/ + src/frontend/

**Target Architecture:**
```
├── src/
│   ├── backend/          # Python FastAPI + CLI code
│   └── frontend/         # React + Vite code
├── tests/
│   ├── e2e/             # Playwright tests
│   └── unit/            # Unit tests (future)
├── docs/                # All documentation
├── package.json         # Consolidated root config
├── vite.config.ts       # Consolidated Vite config
└── tsconfig.json        # Consolidated TypeScript config
```

---

## ⚠️ CRITICAL SUCCESS FACTORS

1. **Atomic Execution**: Each phase must complete fully before starting the next
2. **Zero Downtime**: System remains recoverable at every step
3. **Import Dependencies**: Phase 6 (Import Updates) is CRITICAL - system broken without it
4. **Validation Checkpoints**: Must validate functionality after Phases 2, 5, 6, and 7
5. **Single Browser Session**: All testing must use same browser instance throughout

---

## 📋 PHASE 1: Pre-Migration Preparation (5 minutes)

**Responsibility:** `@code-archaeologist` (Current specialist)

**Objective:** Create safety checkpoints and validate current functionality

### Step 1.1: Create Migration Branch and Backup
```bash
# Create dedicated migration branch
git checkout -b migration-consolidation

# Create comprehensive backup
git stash push -u -m "pre-migration-backup-$(date +%Y%m%d-%H%M%S)"

# Create rollback checkpoint
git tag pre-migration-checkpoint
```

### Step 1.2: Document Current Working State
```bash
# Test CLI functionality
uv run src/main.py --help

# Test FastAPI server (in background)
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 5
curl http://localhost:8000/health
kill $SERVER_PID

# Test React frontend build
cd frontend
npm run build
cd ..

# Document current ports and processes
echo "Current setup validated at $(date)" > migration-validation.log
```

### Step 1.3: Risk Mitigation Setup
```bash
# Ensure no uncommitted changes
git status --porcelain

# Document current environment
cp .env .env.backup
ls -la > file-structure-before.txt
```

**Validation Checkpoint 1:** All three interfaces (CLI, FastAPI, React) function correctly

**Rollback Procedure:**
```bash
git reset --hard pre-migration-checkpoint
git stash pop
```

---

## 📋 PHASE 2: Backend Migration (10 minutes)

**Responsibility:** `@backend-developer`

**Objective:** Move all Python backend code to src/backend/ structure

### Step 2.1: Create Backend Structure
```bash
mkdir -p src/backend
```

### Step 2.2: Move Core Backend Files (Preserve Git History)
```bash
# Move main Python backend modules
git mv src/main.py src/backend/main.py
git mv src/response_manager.py src/backend/response_manager.py
git mv src/response_parser.py src/backend/response_parser.py
git mv src/prompt_templates.py src/backend/prompt_templates.py
git mv src/performance_monitor.py src/backend/performance_monitor.py
git mv src/security_utils.py src/backend/security_utils.py

# Move root Python entry points
git mv market_parser_demo.py src/backend/market_parser_demo.py
git mv chat_ui.py src/backend/chat_ui.py

# Move FSM directory structure
git mv stock_data_fsm src/backend/stock_data_fsm
```

### Step 2.3: Create Backend Package Structure
```bash
# Create __init__.py files for proper Python packaging
touch src/__init__.py
touch src/backend/__init__.py
touch src/backend/stock_data_fsm/__init__.py
```

**⚠️ CRITICAL WARNING:** After this step, Python imports will be broken until Phase 6 is completed. Do not test functionality until import paths are updated.

**Validation Checkpoint 2:**
```bash
# Verify file moves were successful
ls -la src/backend/
ls -la src/backend/stock_data_fsm/
```

---

## 📋 PHASE 3: Frontend Migration (10 minutes)

**Responsibility:** `@react-component-architect`

**Objective:** Move all React frontend code to src/frontend/ structure

### Step 3.1: Create Frontend Structure
```bash
mkdir -p src/frontend
```

### Step 3.2: Move React Source Code (Preserve Git History)
```bash
# Move core React application
git mv frontend/src src/frontend/src
git mv frontend/public src/frontend/public
git mv frontend/index.html src/frontend/index.html

# Move build outputs (preserve for reference)
git mv frontend/dev-dist src/frontend/dev-dist
git mv frontend/dist src/frontend/dist
```

### Step 3.3: Move Frontend Configs (For Consolidation)
```bash
# Move configs with .bak extension (will be consolidated in Phase 5)
git mv frontend/package.json src/frontend/package.json.bak
git mv frontend/vite.config.ts src/frontend/vite.config.ts.bak
git mv frontend/tsconfig.json src/frontend/tsconfig.json.bak
git mv frontend/tsconfig.node.json src/frontend/tsconfig.node.json.bak
git mv frontend/.eslintrc.js src/frontend/.eslintrc.js.bak

# Backup node_modules for reference
if [ -d "frontend/node_modules" ]; then
  mv frontend/node_modules src/frontend/node_modules.bak
fi
```

**Validation Checkpoint 3:**
```bash
# Verify frontend source moved correctly
ls -la src/frontend/src/
ls -la src/frontend/public/
```

---

## 📋 PHASE 4: Test and Documentation Reorganization (10 minutes)

**Responsibility:** `@code-archaeologist` (maintains test infrastructure)

**Objective:** Consolidate all tests and documentation into organized structure

### Step 4.1: Create Test Structure
```bash
mkdir -p tests/e2e
mkdir -p tests/unit
mkdir -p docs/migration
```

### Step 4.2: Move Playwright Tests (High Risk - Complex Paths)
```bash
# Move Playwright test suite (preserve complex config dependencies)
if [ -d "gpt5-openai-agents-sdk-polygon-mcp/tests/playwright" ]; then
  git mv gpt5-openai-agents-sdk-polygon-mcp/tests/playwright tests/e2e/playwright
fi

# Move test documentation
if [ -d "gpt5-openai-agents-sdk-polygon-mcp/docs" ]; then
  git mv gpt5-openai-agents-sdk-polygon-mcp/docs tests/e2e/docs
fi

# Move Playwright config and results
if [ -f "playwright.config.ts" ]; then
  git mv playwright.config.ts tests/e2e/playwright.config.ts
fi

if [ -d "tests/test-results" ]; then
  git mv tests/test-results tests/e2e/test-results
fi

if [ -d "playwright-report" ]; then
  git mv playwright-report tests/e2e/playwright-report
fi
```

### Step 4.3: Move Migration Documentation
```bash
# Consolidate migration docs
if [ -d "gpt5-openai-agents-sdk-polygon-mcp/docs/deprecated" ]; then
  git mv gpt5-openai-agents-sdk-polygon-mcp/docs/deprecated docs/migration/deprecated
fi
```

### Step 4.4: Clean Up Empty Directories
```bash
# Remove empty directories (only if empty)
rmdir gpt5-openai-agents-sdk-polygon-mcp/tests/playwright 2>/dev/null || true
rmdir gpt5-openai-agents-sdk-polygon-mcp/tests 2>/dev/null || true
rmdir gpt5-openai-agents-sdk-polygon-mcp/docs 2>/dev/null || true
rmdir gpt5-openai-agents-sdk-polygon-mcp 2>/dev/null || true
rmdir frontend 2>/dev/null || true
```

**Validation Checkpoint 4:**
```bash
# Verify test structure
ls -la tests/e2e/
ls -la tests/e2e/playwright/
```

---

## 📋 PHASE 5: Configuration Consolidation (15 minutes)

**Responsibility:** `@api-architect` (coordinates frontend-backend integration)

**Objective:** Create consolidated configs that work with new structure

### Step 5.1: Consolidate package.json (CRITICAL)

Create root package.json merging both existing package.json files:

```json
{
  "name": "market-parser-polygon-mcp",
  "version": "1.0.0",
  "type": "module",
  "workspaces": [
    "src/frontend"
  ],
  "scripts": {
    "dev": "npm run dev -w src/frontend",
    "build": "npm run build -w src/frontend",
    "preview": "npm run preview -w src/frontend",
    "test": "cd tests/e2e && npx playwright test",
    "test:headed": "cd tests/e2e && npx playwright test --headed",
    "backend:dev": "uv run uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload",
    "backend:cli": "uv run src/backend/main.py",
    "install:frontend": "npm install -w src/frontend"
  },
  "devDependencies": {
    "@playwright/test": "^1.49.1"
  }
}
```

### Step 5.2: Create Frontend Workspace package.json

Create src/frontend/package.json:

```json
{
  "name": "frontend-openai",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite --config ../../vite.config.ts",
    "build": "vite build --config ../../vite.config.ts",
    "preview": "vite preview --config ../../vite.config.ts",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-markdown": "^9.0.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@typescript-eslint/eslint-plugin": "^7.2.0",
    "@typescript-eslint/parser": "^7.2.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.57.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.6",
    "typescript": "^5.2.2",
    "vite": "^5.2.0"
  }
}
```

### Step 5.3: Create Consolidated vite.config.ts (Root Level)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  root: 'src/frontend',
  build: {
    outDir: '../../dist',
    emptyOutDir: true
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

### Step 5.4: Update Playwright Configuration

Update tests/e2e/playwright.config.ts:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './playwright',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'cd ../../ && uv run uvicorn src.backend.main:app --host 0.0.0.0 --port 8000',
    url: 'http://localhost:8000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Step 5.5: Create Consolidated TypeScript Configuration

Create root tsconfig.json:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/frontend/src/*"],
      "@/backend/*": ["src/backend/*"]
    }
  },
  "include": [
    "src/frontend/src",
    "tests/e2e/playwright"
  ],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**Validation Checkpoint 5:** Configuration files created and paths updated.

---

## 📋 PHASE 6: Import Path Updates (15 minutes)

**Responsibility:** `@backend-developer` + `@react-component-architect` (parallel execution)

**Objective:** Fix all broken imports to restore system functionality

### Step 6.1: Backend Import Updates (`@backend-developer`)

Update Python imports in all backend files:

**src/backend/main.py:**
```python
# OLD imports:
from src.response_manager import ResponseManager, ProcessingMode
from src.response_parser import ResponseParser
from src.prompt_templates import PromptTemplateManager
# NEW imports:
from src.backend.response_manager import ResponseManager, ProcessingMode
from src.backend.response_parser import ResponseParser
from src.backend.prompt_templates import PromptTemplateManager
```

**src/backend/response_manager.py:**
```python
# Update relative imports:
from src.backend.response_parser import ResponseParser
from src.backend.security_utils import validate_input, sanitize_data
```

**All other backend files:** Update imports to use `src.backend.` prefix

### Step 6.2: Update Command References

**Root package.json scripts (already updated in Phase 5):**
- `"backend:dev": "uv run uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload"`
- `"backend:cli": "uv run src/backend/main.py"`

### Step 6.3: Update Documentation and Config References

**CLAUDE.md updates:**
```bash
# Update all command examples:
# OLD: uv run src/main.py
# NEW: uv run src/backend/main.py

# OLD: uvicorn src.main:app
# NEW: uvicorn src.backend.main:app
```

**Validation Checkpoint 6 (CRITICAL):**
```bash
# Test backend functionality restored
uv run src/backend/main.py --help
uv run uvicorn src.backend.main:app --host 0.0.0.0 --port 8001 &
sleep 5
curl http://localhost:8001/health
```

---

## 📋 PHASE 7: Final Validation and Cleanup (10 minutes)

**Responsibility:** `@code-reviewer` (validates all changes)

**Objective:** Comprehensive system validation and cleanup

### Step 7.1: Backend Validation
```bash
# Test CLI interface
echo "Testing CLI..."
uv run src/backend/main.py

# Test FastAPI server
echo "Testing FastAPI server..."
uv run uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 10
curl http://localhost:8000/health
kill $SERVER_PID
```

### Step 7.2: Frontend Validation
```bash
# Install frontend dependencies
npm install

# Test frontend build
npm run build

# Test frontend dev server
npm run dev &
FRONTEND_PID=$!
sleep 10
curl http://localhost:3000/
kill $FRONTEND_PID
```

### Step 7.3: E2E Test Validation
```bash
# Test Playwright configuration
cd tests/e2e
npx playwright test --list

# Run one simple test to verify setup
npx playwright test test-b001-market-status.spec.ts --headed
```

### Step 7.4: Final Cleanup
```bash
# Remove backup files if everything works
rm -f src/frontend/*.bak
rm -rf src/frontend/node_modules.bak

# Update git status
git add .
git status
```

### Step 7.5: Documentation Updates

Update CLAUDE.md with new structure:

```markdown
## 🚀 Quick Start - Complete Command Sequence (Virgin State to Running)

### Step 2: Backend Setup (Required First)
```bash
# Start FastAPI backend server
npm run backend:dev

# OR Start CLI interface
npm run backend:cli
```

### Step 4: GUI Setup - Vite Development Server
```bash
# Install and start frontend
npm install
npm run dev
```
```

**Final Validation Checkpoint:**
- [ ] CLI works: `npm run backend:cli`
- [ ] FastAPI works: `npm run backend:dev` + `curl http://localhost:8000/health`
- [ ] React works: `npm run dev` + browser loads http://localhost:3000/
- [ ] Tests work: `npm run test --list` shows all tests
- [ ] Build works: `npm run build` succeeds

---

## 🚨 RISK MITIGATION AND ROLLBACK PROCEDURES

### Phase-by-Phase Rollback

**Phases 1-4 (File Moves):**
```bash
git reset --hard pre-migration-checkpoint
git stash pop
```

**Phase 5-6 (Config/Import Issues):**
```bash
# Restore from backup and retry specific phase
git checkout pre-migration-checkpoint -- package.json vite.config.ts
git stash pop
```

**Phase 7 (Validation Failures):**
- Fix specific issues identified in validation
- Don't rollback unless fundamental architectural problems

### Emergency Recovery Commands
```bash
# Complete rollback to pre-migration state
git tag emergency-rollback-$(date +%Y%m%d-%H%M%S)
git reset --hard pre-migration-checkpoint
git clean -fd
git stash pop
```

### Common Issue Resolution

**"Import Error" Issues:**
- Check Phase 6 import path updates were applied correctly
- Verify `src/__init__.py` and `src/backend/__init__.py` exist
- Check PYTHONPATH includes project root

**"Command Not Found" Issues:**
- Check package.json scripts use correct paths
- Verify npm workspace configuration
- Check that uvicorn command points to `src.backend.main:app`

**"Build Failed" Issues:**
- Check vite.config.ts points to correct src/frontend paths
- Verify tsconfig.json includes correct paths
- Check all frontend dependencies installed

---

## 📝 SPECIALIST TASK ASSIGNMENTS

### @backend-developer Tasks (Phase 2 + 6.1)
- **Duration:** 25 minutes
- **Phase 2:** Execute all Python file moves to src/backend/
- **Phase 6.1:** Fix all Python import paths
- **Dependencies:** Must wait for Phase 5 completion before testing
- **Validation:** Backend CLI and FastAPI server must work after Phase 6

### @react-component-architect Tasks (Phase 3 + 6.2)
- **Duration:** 20 minutes
- **Phase 3:** Execute all React file moves to src/frontend/
- **Phase 6.2:** Verify frontend build works with new configs
- **Dependencies:** Must wait for Phase 5 completion before testing
- **Validation:** React dev server must work after Phase 6

### @api-architect Tasks (Phase 5)
- **Duration:** 15 minutes
- **Phase 5:** Create all consolidated configurations
- **Critical:** This phase enables subsequent phases to work
- **Dependencies:** Must complete Phases 2-4 first
- **Validation:** Configurations must be syntactically correct

### @code-reviewer Tasks (Phase 7)
- **Duration:** 10 minutes
- **Phase 7:** Final validation and approval
- **Validation:** All three interfaces (CLI, FastAPI, React) must work
- **Authority:** Can require fixes or approve for commit

### @code-archaeologist Tasks (Phases 1, 4)
- **Duration:** 15 minutes
- **Phase 1:** Pre-migration setup and safety checkpoints
- **Phase 4:** Test infrastructure reorganization
- **Coordination:** Oversee overall migration process

---

## ⏱️ ESTIMATED TIMELINE

**Total Duration:** 90 minutes (1.5 hours)

- **Phase 1:** 5 minutes (Pre-migration preparation)
- **Phase 2:** 10 minutes (Backend migration)
- **Phase 3:** 10 minutes (Frontend migration)
- **Phase 4:** 10 minutes (Test reorganization)
- **Phase 5:** 15 minutes (Configuration consolidation)
- **Phase 6:** 15 minutes (Import path updates)
- **Phase 7:** 10 minutes (Final validation)
- **Buffer:** 15 minutes (Issue resolution)

**Parallel Execution Opportunities:**
- Phases 2 and 3 can run in parallel (backend-developer + react-component-architect)
- Phase 6.1 and 6.2 can run in parallel (backend + frontend import fixes)

---

## ✅ SUCCESS CRITERIA

**Migration is complete and successful when:**

1. **✅ Backend Functionality:** CLI and FastAPI server work with `src.backend.` imports
2. **✅ Frontend Functionality:** React dev server and build work from new structure
3. **✅ Test Integration:** Playwright tests can run from `tests/e2e/` location
4. **✅ Clean Structure:** All files organized in target `src/backend/` + `src/frontend/` structure
5. **✅ Documentation Updated:** CLAUDE.md reflects new command patterns
6. **✅ Single Atomic Commit:** All changes committed together with migration summary

**Atomic Commit Message Template:**
```
feat: Consolidate project structure into src/backend/ and src/frontend/

- Move Python backend code to src/backend/ with updated imports
- Move React frontend code to src/frontend/ with workspace config
- Consolidate package.json, vite.config.ts, and tsconfig.json at root
- Reorganize Playwright tests to tests/e2e/ structure
- Update all import paths and command references
- Preserve git history for all file moves

Backend: CLI + FastAPI working with src.backend.* imports
Frontend: React dev server working with consolidated Vite config
Tests: Playwright working from tests/e2e/ structure
Docs: CLAUDE.md updated with new command patterns

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```