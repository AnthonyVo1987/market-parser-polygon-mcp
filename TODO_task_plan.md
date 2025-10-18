# React Frontend Retirement - Implementation Task Plan

**Date:** October 17, 2025
**Branch:** react_retirement
**Research Reference:** research_task_plan.md
**Status:** Ready for Implementation

---

## Overview

This task plan provides a detailed, step-by-step implementation checklist for completely retiring the React frontend from the Market Parser codebase and migrating to a Gradio-only Python UI.

**Total Phases:** 9
**Estimated Duration:** 4-6 hours
**Complexity:** ⚠️ EXTREMELY COMPLEX

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE

**YOU MUST use advanced tools throughout ENTIRE implementation:**

- **Sequential-Thinking**: REQUIRED at START of every phase
- **Serena Tools**: For code analysis, symbol searches, pattern matching
- **Standard Tools**: For file operations when Serena doesn't support the operation
- **Continuous Usage**: Use tools repeatedly throughout each phase
- **Verification**: Use grep and Serena search after every phase

**SUCCESS PATTERN:**
✅ Sequential-Thinking at START of every phase
✅ Tools used multiple times per phase
✅ Verification after each major task
✅ Comprehensive testing before commit

---

## Phase 0: Pre-Implementation Verification

**Duration:** 10 minutes
**Objective:** Ensure prerequisites and create backups

### Task 0.1: Verify Git Branch ✅

**Already Complete:**
- ✅ Branch `react_retirement` created
- ✅ Branch pushed to remote

**Verification:**
```bash
git branch --show-current
# Expected: react_retirement

git status
# Expected: On branch react_retirement, clean working tree
```

---

### Task 0.2: Verify Gradio UI Working

**Objective:** Confirm Gradio is functional before deleting React

**Actions:**
```bash
# Start Gradio only
uv run python src/backend/gradio_app.py
```

**Manual Verification:**
1. ✅ Gradio starts without errors
2. ✅ Accessible at http://127.0.0.1:7860
3. ✅ Can send test query: "Market Status"
4. ✅ Receives proper response with footer

**Success Criteria:**
- Gradio UI fully functional
- Performance metrics footer visible
- Agent responds correctly

**If FAILED:** Do NOT proceed with React deletion

---

### Task 0.3: Verify CLI Working

**Objective:** Confirm CLI is functional (fallback interface)

**Actions:**
```bash
uv run src/backend/main.py
```

**Manual Verification:**
1. ✅ CLI starts without errors
2. ✅ Can send test query: "Market Status"
3. ✅ Receives proper response with footer

**Success Criteria:**
- CLI fully functional
- Performance metrics footer visible

---

### Task 0.4: Create Safety Backup (Optional)

**Objective:** Create archive branch for React code preservation

**Actions:**
```bash
# Optional: Create archive branch before deletion
git checkout -b react_frontend_archive
git push -u origin react_frontend_archive
git checkout react_retirement
```

**Rationale:** React code preserved in git history and dedicated archive branch

---

## Phase 1: Safe File & Directory Deletion

**Duration:** 30 minutes
**Objective:** Delete all React source code and build files
**Risk:** Low (no dependencies on these files)

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

---

### Task 1.1: Delete src/frontend/ Directory

**Objective:** Remove entire React source code directory

**Actions:**
```bash
# Verify directory exists first
ls -la src/frontend/

# Delete entire frontend directory
rm -rf src/frontend/

# Verify deletion
ls -la src/
# Expected: No 'frontend' directory
```

**Files Deleted:** ~30 files (components, utils, types, services, config, styles)

**Verification:**
```bash
# Should return empty
find . -type d -name "frontend" | grep -v node_modules

# Should return empty
find . -name "*.tsx" -o -name "*.jsx" | grep -v node_modules
```

**Success Criteria:**
- ✅ src/frontend/ directory completely removed
- ✅ No .tsx or .jsx files remain (except in node_modules)

---

### Task 1.2: Delete Build Output Directories

**Objective:** Remove Vite build artifacts

**Actions:**
```bash
# Delete production build
rm -rf dist/

# Delete development build
rm -rf dev-dist/

# Verify deletion
ls -la | grep dist
# Expected: No 'dist' or 'dev-dist' directories
```

**Verification:**
```bash
# Should return empty
ls -d */dist 2>/dev/null
```

**Success Criteria:**
- ✅ dist/ removed
- ✅ dev-dist/ removed

---

### Task 1.3: Delete public/ Directory

**Objective:** Remove React/PWA static assets

**Actions:**
```bash
# Verify contents first
ls -la public/

# Delete public directory
rm -rf public/

# Verify deletion
ls -la | grep public
# Expected: No 'public' directory
```

**Files Deleted:**
- pwa-icon.svg
- pwa-192x192.png
- pwa-512x512.png
- favicon.ico
- icon-generator.html

**Success Criteria:**
- ✅ public/ directory removed

---

### Task 1.4: Delete Vite Configuration Files

**Objective:** Remove Vite build configuration

**Actions:**
```bash
# Delete vite.config.ts
rm vite.config.ts

# Delete vite TypeScript definitions
rm vite-env.d.ts

# Verify deletion
ls -la | grep vite
# Expected: No vite files (except in node_modules)
```

**Verification:**
```bash
# Should return empty (except node_modules)
find . -name "*vite*" -type f | grep -v node_modules
```

**Success Criteria:**
- ✅ vite.config.ts deleted
- ✅ vite-env.d.ts deleted

---

### Task 1.5: Delete TypeScript Configuration

**Objective:** Remove TypeScript config (frontend-specific)

**Actions:**
```bash
# Verify it's React-specific first
grep -i "react" tsconfig.json
# Expected: Should show "jsx": "react-jsx"

# Delete tsconfig.json
rm tsconfig.json

# Verify deletion
ls -la | grep tsconfig.json
# Expected: Empty
```

**Note:** Backend doesn't use TypeScript, safe to delete

**Success Criteria:**
- ✅ tsconfig.json deleted

---

### Task 1.6: Delete React HTML Entry Point

**Objective:** Remove index.html (React entry point)

**Actions:**
```bash
# Verify it references React
grep "main.tsx" index.html
# Expected: Should show reference to /src/frontend/main.tsx

# Delete index.html
rm index.html

# Verify deletion
ls -la | grep index.html
# Expected: Empty
```

**Success Criteria:**
- ✅ index.html deleted

---

### Task 1.7: Delete ESLint React Configuration

**Objective:** Remove .eslintrc.cjs (heavily React-dependent)

**Actions:**
```bash
# Verify it's React-specific
grep -i "react" .eslintrc.cjs | wc -l
# Expected: 20+ React references

# Delete .eslintrc.cjs
rm .eslintrc.cjs

# Verify deletion
ls -la | grep eslintrc
# Expected: Empty
```

**Success Criteria:**
- ✅ .eslintrc.cjs deleted

---

### Task 1.8: Update .pre-commit-config.yaml

**Objective:** Remove eslint-plugin-react reference

**File:** .pre-commit-config.yaml

**Changes:**
- Line 34: Delete `- 'eslint-plugin-react'`

**Actions:**
```bash
# Use Edit tool to remove line 34
```

**Verification:**
```bash
grep "eslint-plugin-react" .pre-commit-config.yaml
# Expected: Empty
```

**Success Criteria:**
- ✅ eslint-plugin-react reference removed

---

### Task 1.9: Update .vscode/settings.json

**Objective:** Remove React language configurations

**File:** .vscode/settings.json

**Changes:**
- Line 20: Remove `"javascriptreact",`
- Line 22: Remove `"typescriptreact"`

**Verification:**
```bash
grep -i "react" .vscode/settings.json
# Expected: Empty
```

**Success Criteria:**
- ✅ React language configs removed

---

### 🔍 Phase 1 Verification

**Run after completing all Phase 1 tasks:**

```bash
# Verify no .tsx/.jsx files
find . -type f \( -name "*.tsx" -o -name "*.jsx" \) | grep -v node_modules
# Expected: Empty

# Verify no frontend directory
ls -la src/ | grep frontend
# Expected: Empty

# Verify no dist directories
ls -la | grep dist
# Expected: Empty (except node_modules)

# Verify no vite files
ls -la | grep vite
# Expected: Empty (except node_modules)

# Verify no index.html
ls -la | grep index.html
# Expected: Empty
```

**Success Criteria:**
- ✅ All source code deleted
- ✅ All build files deleted
- ✅ All config files updated
- ✅ No React files remain outside node_modules

---

## Phase 2: Package & Dependency Cleanup

**Duration:** 15 minutes
**Objective:** Remove React/Vite from package.json and regenerate lockfile
**Risk:** Low (careful removal prevents breaking backend)

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

---

### Task 2.1: Read Current package.json

**Objective:** Understand current dependencies before modification

**Actions:**
```bash
# Read package.json to confirm React dependencies
cat package.json | grep -A 5 "dependencies"
cat package.json | grep -A 20 "devDependencies"
```

**Document Current State:**
- Production deps with React: react, react-dom, react-markdown, react-scan
- Dev deps with React/Vite: @types/react, @types/react-dom, @vitejs/plugin-react, eslint-plugin-react*, vite

---

### Task 2.2: Remove Production Dependencies

**Objective:** Remove React runtime dependencies

**File:** package.json

**Remove these lines from "dependencies" section:**
```json
"react": "^18.2.0",
"react-dom": "^18.2.0",
"react-markdown": "^9.0.0",
"react-scan": "^0.4.3",
```

**Actions:**
1. Use Edit tool to remove each dependency
2. Ensure proper JSON formatting (no trailing commas)

**Verification:**
```bash
grep -i "react" package.json | grep -v "// Comment"
# Expected: Empty (no React dependencies)
```

---

### Task 2.3: Remove Dev Dependencies

**Objective:** Remove React/Vite development dependencies

**File:** package.json

**Remove these lines from "devDependencies" section:**
```json
"@types/react": "^18.2.66",
"@types/react-dom": "^18.2.22",
"@vitejs/plugin-react": "^4.2.1",
"eslint-plugin-react": "^7.33.0",
"eslint-plugin-react-hooks": "^4.6.0",
"eslint-plugin-react-refresh": "^0.4.6",
"vite": "^5.x.x",
```

**Note:** Keep TypeScript if needed (research required - likely not needed)

**Actions:**
1. Use Edit tool to remove each dev dependency
2. Check if TypeScript is used in backend
3. Remove vite completely

**Verification:**
```bash
grep -E "react|vite" package.json
# Expected: Empty (no React or Vite dependencies)
```

---

### Task 2.4: Remove NPM Scripts

**Objective:** Remove frontend-related scripts

**File:** package.json

**Remove/Update these scripts:**
```json
"frontend:dev": "vite --mode development",  // DELETE
"perf:scan": "react-scan http://localhost:3000",  // DELETE
"build": "tsc && vite build",  // DELETE or UPDATE if needed
"preview": "vite preview"  // DELETE
```

**Keep scripts:**
- Backend scripts (uvicorn, etc.)
- Testing scripts
- Linting scripts (if Python-only)

**Verification:**
```bash
grep -E "vite|react-scan|3000" package.json
# Expected: Empty
```

---

### Task 2.5: Regenerate package-lock.json

**Objective:** Update lockfile to reflect removed dependencies

**Actions:**
```bash
# Remove old lockfile
rm package-lock.json

# Regenerate with clean dependencies
npm install

# Verify no React/Vite packages installed
cat package-lock.json | grep -i "\"react\"" | wc -l
# Expected: 0 (or very few false positives like "contract")
```

**Verification:**
```bash
# Check node_modules size reduction
du -sh node_modules/
# Expected: Significantly smaller (~500MB reduction)

# Verify no React directories
ls node_modules/ | grep -i react
# Expected: Empty
```

**Success Criteria:**
- ✅ package.json cleaned
- ✅ package-lock.json regenerated
- ✅ node_modules cleaned (no React packages)
- ✅ npm install completes without errors

---

### 🔍 Phase 2 Verification

**Run after completing all Phase 2 tasks:**

```bash
# Verify package.json clean
grep -iE "react|vite" package.json
# Expected: Empty

# Verify no React in lockfile
grep "\"react\":" package-lock.json
# Expected: Empty (or only false positives)

# Verify npm install works
npm install
# Expected: Success, no errors

# Verify reduced dependency count
npm list --depth=0 | wc -l
# Expected: Significantly fewer packages
```

**Success Criteria:**
- ✅ No React dependencies in package.json
- ✅ No Vite dependencies in package.json
- ✅ package-lock.json regenerated successfully
- ✅ npm install completes without errors

---

## Phase 3: Backend Code Modifications

**Duration:** 20 minutes
**Objective:** Remove React static file serving and update CORS
**Risk:** Medium (must not break backend API)

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

---

### Task 3.1: Update src/backend/main.py - Remove StaticFiles Import

**Objective:** Remove unused import

**File:** src/backend/main.py
**Line:** 22

**Change:**
```python
# REMOVE this line:
from fastapi.staticfiles import StaticFiles
```

**Verification:**
```bash
grep "StaticFiles" src/backend/main.py
# Expected: Empty
```

---

### Task 3.2: Update src/backend/main.py - Remove CORS Configuration

**Objective:** Remove React frontend CORS origins

**File:** src/backend/main.py
**Lines:** 101-108

**Current Code:**
```python
if settings.cors_origins:
    cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

**Options:**

**Option A - Complete Removal (Recommended):**
- Delete entire CORS section (lines 101-108)
- Rationale: Gradio runs on same backend, no CORS needed

**Option B - Update to Empty Origins:**
```python
# Keep CORS middleware but with empty origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],  # Empty - no external origins
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

**Action:** Use Option A (complete removal) unless specific CORS needs identified

**Verification:**
```bash
grep -A 8 "cors_origins" src/backend/main.py
# Expected: Empty (if Option A) or shows empty origins (if Option B)
```

---

### Task 3.3: Update src/backend/main.py - Remove Static File Serving

**Objective:** Remove React build serving

**File:** src/backend/main.py
**Lines:** 126-128

**Remove this code:**
```python
static_dir = Path(__file__).parent.parent.parent / "dist"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
```

**Rationale:** No longer serving React static files from /dist

**Verification:**
```bash
grep -A 3 "static_dir" src/backend/main.py
# Expected: Empty

grep "StaticFiles" src/backend/main.py
# Expected: Empty
```

---

### Task 3.4: Test Backend Starts Without Errors

**Objective:** Verify backend modifications didn't break startup

**Actions:**
```bash
# Start backend
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000
```

**Manual Verification:**
1. ✅ Backend starts without import errors
2. ✅ No CORS errors in logs
3. ✅ API accessible at http://127.0.0.1:8000
4. ✅ Health check works: `curl http://127.0.0.1:8000/health`

**Success Criteria:**
- Backend starts successfully
- No errors in console
- API endpoints functional

**If FAILED:** Revert changes and debug before proceeding

---

### Task 3.5: Update config/app.config.json - Remove Frontend Section

**Objective:** Delete entire frontend configuration

**File:** config/app.config.json
**Lines:** 49-67

**Remove this entire section:**
```json
"frontend": {
  "server": {
    "host": "127.0.0.1",
    "port": 3000
  },
  "api": {
    "baseUrl": "/api"
  },
  "features": {
    "appEnv": "development",
    "pwa": true,
    "debugMode": true
  },
  "development": {
    "hmr": true,
    "sourceMap": true,
    "bundleAnalyzer": true
  }
}
```

**Note:** Ensure proper JSON formatting (no trailing comma after backend section)

**Verification:**
```bash
grep -i "frontend" config/app.config.json
# Expected: Empty

# Validate JSON syntax
python3 -c "import json; json.load(open('config/app.config.json'))"
# Expected: No errors
```

---

### Task 3.6: Update config/app.config.json - Update CORS Origins

**Objective:** Remove port 3000 CORS origins

**File:** config/app.config.json
**Lines:** 32-35

**Current:**
```json
"cors": {
  "origins": [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
  ]
}
```

**Change to:**
```json
"cors": {
  "origins": []
}
```

**Alternative:** Delete entire CORS section if not needed

**Verification:**
```bash
grep -A 5 "cors" config/app.config.json
# Expected: Empty origins array or no CORS section

# Validate JSON
python3 -c "import json; json.load(open('config/app.config.json'))"
# Expected: No errors
```

---

### 🔍 Phase 3 Verification

**Run after completing all Phase 3 tasks:**

```bash
# Verify no StaticFiles import
grep "StaticFiles" src/backend/main.py
# Expected: Empty

# Verify no static_dir references
grep "static_dir\|dist" src/backend/main.py
# Expected: Empty

# Verify config has no frontend section
grep -i "frontend" config/app.config.json
# Expected: Empty

# Verify config has empty CORS origins
grep -A 3 "cors" config/app.config.json
# Expected: Empty array or no CORS

# Test backend starts
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 &
sleep 3
curl http://127.0.0.1:8000/health
pkill -f uvicorn
# Expected: Health check passes
```

**Success Criteria:**
- ✅ Backend starts without errors
- ✅ No static file serving
- ✅ CORS updated/removed
- ✅ Config validated (proper JSON)
- ✅ API endpoints functional

---

## Phase 4: Startup Script Refactoring

**Duration:** 30 minutes
**Objective:** Remove all React/Vite references from startup scripts
**Risk:** Medium (scripts must work for backend + Gradio)

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

---

### Task 4.1: Refactor start-app.sh - Remove Frontend Variables

**Objective:** Delete FRONTEND_PORT variable

**File:** start-app.sh
**Line:** 39

**Remove:**
```bash
FRONTEND_PORT="3000"
```

**Verification:**
```bash
grep "FRONTEND_PORT" start-app.sh
# Expected: Empty
```

---

### Task 4.2: Refactor start-app.sh - Remove Frontend Cleanup

**Objective:** Remove vite process killing

**File:** start-app.sh
**Lines:** 56-58

**Remove:**
```bash
# Kill frontend (vite) - be careful not to kill other vite processes
pkill -f "vite.*--mode development" 2>/dev/null
pkill -f "npm run frontend:dev" 2>/dev/null
```

**Keep:** Backend and Gradio cleanup sections

**Verification:**
```bash
grep -i "vite\|frontend.*dev" start-app.sh
# Expected: Empty
```

---

### Task 4.3: Refactor start-app.sh - Remove Frontend Startup (Gnome-terminal)

**Objective:** Delete frontend startup in gnome-terminal mode

**File:** start-app.sh
**Lines:** 104-111

**Remove this entire section:**
```bash
echo "🚀 Starting frontend server..."
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "
        echo '🔧 Starting Vite frontend server...'
        echo 'Command: npm run frontend:dev'
        echo 'Port: 3000'
        echo '============================================'
        npm run frontend:dev
        # ...
    "
```

**Verification:**
```bash
grep -A 5 "Starting frontend server" start-app.sh
# Expected: Empty
```

---

### Task 4.4: Refactor start-app.sh - Remove Frontend Startup (Xterm)

**Objective:** Delete frontend startup in xterm fallback mode

**File:** start-app.sh
**Lines:** 119-123

**Remove this section:**
```bash
elif command -v xterm &> /dev/null; then
    xterm -T "Frontend (Port 3000)" -geometry 120x30+440+0 -e bash -c "
        echo '🔧 Starting Vite frontend server...'
        # ...
    " &
```

---

### Task 4.5: Refactor start-app.sh - Remove Frontend Startup (Fallback)

**Objective:** Delete frontend nohup background mode

**File:** start-app.sh
**Lines:** 131-132

**Remove:**
```bash
echo "   Frontend logs will be written to frontend.log"
nohup npm run frontend:dev > frontend.log 2>&1 &
```

---

### Task 4.6: Refactor start-app.sh - Update Sleep Timer

**Objective:** Reduce sleep time (no frontend to wait for)

**File:** start-app.sh
**Line:** 137

**Change:**
```bash
# OLD:
sleep 5  # Wait for frontend to initialize

# NEW:
sleep 3  # Wait for Gradio to initialize
```

---

### Task 4.7: Refactor start-app.sh - Remove Frontend Health Check

**Objective:** Delete port 3000 health check

**File:** start-app.sh
**Lines:** 194-201

**Remove this entire section:**
```bash
# Check frontend
FRONTEND_READY=false
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://127.0.0.1:$FRONTEND_PORT > /dev/null 2>&1; then
        FRONTEND_READY=true
        break
    fi
    echo "⏳ Waiting for frontend server... (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)"
    # ...
done
```

**Keep:** Backend and Gradio health checks

---

### Task 4.8: Refactor start-app.sh - Update Final Health Check Condition

**Objective:** Remove FRONTEND_READY from condition

**File:** start-app.sh
**Multiple locations**

**Change:**
```bash
# OLD:
if [ "$BACKEND_READY" = true ] && [ "$FRONTEND_READY" = true ] && [ "$GRADIO_READY" = true ]; then

# NEW:
if [ "$BACKEND_READY" = true ] && [ "$GRADIO_READY" = true ]; then
```

---

### Task 4.9: Refactor start-app.sh - Update Success Messages

**Objective:** Remove frontend server status messages

**File:** start-app.sh
**Lines:** 242, 247, etc.

**Remove all mentions of:**
- "Frontend Server: PID $FRONTEND_PID"
- "Frontend logs in frontend.log"
- References to port 3000

**Update URLs section to show only:**
- Backend: http://127.0.0.1:8000
- Gradio: http://127.0.0.1:7860

---

### Task 4.10: Refactor start-app-xterm.sh - Apply Same Changes

**Objective:** Apply all changes from start-app.sh to start-app-xterm.sh

**File:** start-app-xterm.sh

**Repeat tasks 4.1-4.9 for this file:**
- Remove FRONTEND_PORT variable (line 39)
- Remove vite cleanup (lines 89-91)
- Remove tmux frontend session (line 102)
- Remove frontend startup - tmux mode (lines 117-127)
- Remove frontend startup - xterm mode (lines 157-170)
- Remove frontend health check (lines 208-215)
- Update final condition (remove FRONTEND_READY)
- Update success messages (remove frontend references)
- Update tmux attach commands (remove frontend session)

**Additional xterm-specific:**
- Remove tmux session references to "market-parser-frontend"
- Update xterm window titles (remove "Frontend (Port 3000)")

---

### Task 4.11: Test start-app.sh

**Objective:** Verify script works with backend + Gradio only

**Actions:**
```bash
# Make executable
chmod +x start-app.sh

# Run script
./start-app.sh
```

**Manual Verification:**
1. ✅ Script starts without errors
2. ✅ Backend starts on port 8000
3. ✅ Gradio starts on port 7860
4. ✅ No errors about port 3000 or frontend
5. ✅ Health checks pass for backend and Gradio
6. ✅ Success message shows only 2 services (backend, Gradio)

**Test Cleanup:**
```bash
# Kill servers
pkill -f uvicorn
pkill -f "python.*gradio_app"
```

**Success Criteria:**
- Script executes successfully
- Both servers start
- No frontend references in output

---

### Task 4.12: Test start-app-xterm.sh

**Objective:** Verify xterm script works

**Actions:**
```bash
chmod +x start-app-xterm.sh
./start-app-xterm.sh
```

**Manual Verification:**
1. ✅ Script starts backend and Gradio in separate windows
2. ✅ No frontend/vite window
3. ✅ Health checks pass
4. ✅ Tmux sessions show only backend and Gradio (no frontend session)

**Test Cleanup:**
```bash
tmux kill-session -t market-parser-backend
tmux kill-session -t market-parser-gradio
# Or kill xterm windows manually
```

---

### 🔍 Phase 4 Verification

**Run after completing all Phase 4 tasks:**

```bash
# Verify no frontend variable references
grep -i "FRONTEND_PORT" start-app*.sh
# Expected: Empty

# Verify no vite references
grep -i "vite" start-app*.sh
# Expected: Empty

# Verify no port 3000 references
grep "3000" start-app*.sh
# Expected: Empty

# Verify no npm run frontend:dev
grep "frontend:dev" start-app*.sh
# Expected: Empty

# Verify final condition updated
grep "FRONTEND_READY" start-app*.sh
# Expected: Empty

# Test both scripts
./start-app.sh  # Should work
./start-app-xterm.sh  # Should work (if X11/tmux available)
```

**Success Criteria:**
- ✅ All frontend references removed from both scripts
- ✅ Scripts start backend + Gradio successfully
- ✅ Health checks work
- ✅ No errors or warnings about frontend/port 3000

---

## Phase 5: Documentation Updates

**Duration:** 90 minutes
**Objective:** Update all documentation to remove React references
**Risk:** Low (documentation only, no code impact)

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

**Strategy:** Update files in priority order (critical docs first)

---

### Task 5.1: Update CLAUDE.md (HIGH PRIORITY)

**Objective:** Remove all React references from main project guide

**File:** CLAUDE.md

**Sections to UPDATE:**

#### Section 1: Line 8 - Project Overview
**Change:**
```markdown
# OLD:
Market Parser is a Python CLI, React web application, and Gradio ChatInterface...

# NEW:
Market Parser is a Python CLI and Gradio ChatInterface...
```

#### Section 2: Lines 331-356 - Startup Scripts
**Remove:**
- Vite server references
- Port 3000 references
- React frontend health checks
- "React GUI: http://127.0.0.1:3000"

**Update to show only:**
- Backend (port 8000)
- Gradio (port 7860)

#### Section 3: Lines 372-383 - Features
**DELETE:**
- "React Web App" section
- "React Web Interface" subsection

**Keep:**
- Gradio ChatInterface section
- CLI Interface section

#### Section 4: Lines 411-415 - Architecture
**Change:**
```markdown
# OLD:
- **Frontend (React)**: React 18.2+ with Vite 5.2+ and TypeScript (port 3000)
- **Deployment**: Fixed ports (8000/3000/7860)

# NEW:
- **Deployment**: Fixed ports (8000/7860)
```

#### Section 5: Lines 441-442 - Project Structure
**Remove:**
```markdown
├── frontend/            # React frontend
│   ├── components/      # React components
```

#### Section 6: Lines 483-544 - Last Completed Task
**Update all instances:**
```markdown
# OLD: "CLI, React, and Gradio"
# NEW: "CLI and Gradio"

# OLD: "All interfaces (CLI, React, Gradio)"
# NEW: "All interfaces (CLI, Gradio)"
```

**Verification:**
```bash
grep -in "react\|3000\|vite" CLAUDE.md | grep -v "react_retirement\|research_task_plan"
# Expected: Empty (except historical task references)
```

**Estimated Changes:** ~30 references

---

### Task 5.2: Update README.md (HIGH PRIORITY)

**Objective:** Remove React from public-facing documentation

**File:** README.md

**Sections to UPDATE:**

#### Section 1: Line 3 - Description
**Change:**
```markdown
# OLD:
A Python CLI, React web application, and Gradio ChatInterface...

# NEW:
A Python CLI and Gradio ChatInterface...
```

#### Section 2: Line 56 - Prerequisites
**DELETE:**
```markdown
- **[Node.js 18+](https://nodejs.org/)** - For React frontend
```

#### Section 3: Lines 118-143 - Startup
**Remove:**
- Vite server startup info
- Port 3000 references
- React GUI URL

**Update to show only:**
- Backend startup
- Gradio startup
- CLI usage

#### Section 4: Lines 181-190 - Features
**DELETE:**
- "React Web App" section
- "React Web Interface" subsection

#### Section 5: Line 284 - Performance
**DELETE:**
```markdown
- **Bundle Optimization**: Vite build optimizations with tree shaking
```

#### Section 6: Lines 304-309 - Tech Stack
**Remove:**
```markdown
- **Frontend (React)**: React 18.2+ with Vite 5.2+ and TypeScript (port 3000)
```

**Change ports:**
```markdown
# OLD: (8000/3000/7860)
# NEW: (8000/7860)
```

#### Section 7: Lines 337-338 - Project Structure
**Remove:**
```markdown
├── frontend/            # React frontend
│   ├── components/      # React components
```

**Verification:**
```bash
grep -in "react\|node.js.*frontend\|3000\|vite" README.md
# Expected: Empty (except maybe historical references)
```

**Estimated Changes:** ~25 references

---

### Task 5.3: Update START_SCRIPT_README.md

**Objective:** Update startup script documentation

**File:** START_SCRIPT_README.md

**Changes:**
- Lines 60-239: Remove all React/Vite/port 3000 references
- Update server list to show only: Backend (8000), Gradio (7860)
- Update health check examples

**Verification:**
```bash
grep -i "react\|vite\|3000" START_SCRIPT_README.md
# Expected: Empty
```

**Estimated Changes:** ~15 references

---

### Task 5.4: Update AGENTS.md

**Objective:** Remove React from agents documentation

**File:** AGENTS.md
**Lines:** 8-329

**Changes:**
- Similar to CLAUDE.md updates
- Remove React application mentions
- Update URLs to exclude port 3000

**Verification:**
```bash
grep -i "react\|3000" AGENTS.md
# Expected: Empty
```

**Estimated Changes:** ~10 references

---

### Task 5.5: Update DEPLOYMENT.md

**Objective:** Remove React deployment references

**File:** DEPLOYMENT.md
**Line:** 9

**Change:**
```markdown
# OLD:
- **React frontend** - Built as static files, served by FastAPI

# NEW:
(Remove this line - only backend deployment now)
```

**Verification:**
```bash
grep -i "react\|frontend" DEPLOYMENT.md
# Expected: Empty or only backend references
```

**Estimated Changes:** ~5 references

---

### Task 5.6: Update DEPLOYMENT-SUMMARY.md

**Objective:** Major rewrite of deployment architecture

**File:** DEPLOYMENT-SUMMARY.md
**Lines:** 9-246

**Changes:**
- Remove: "Builds React frontend (Stage 1)"
- Remove: React static file serving documentation
- Remove: Node.js build stage
- Update: FastAPI serves API only (no static files)
- Remove: React production build references

**This file may need major restructuring - consider if it's still relevant.**

**Verification:**
```bash
grep -i "react\|vite\|3000" DEPLOYMENT-SUMMARY.md
# Expected: Empty
```

**Estimated Changes:** ~15 references

---

### Task 5.7: Update DEPLOYMENT-QUICKSTART.md

**Objective:** Remove React from deployment checklist

**File:** DEPLOYMENT-QUICKSTART.md
**Line:** 46

**Remove:**
```markdown
- ✅ React frontend (built static files)
```

**Verification:**
```bash
grep -i "react" DEPLOYMENT-QUICKSTART.md
# Expected: Empty
```

**Estimated Changes:** ~3 references

---

### Task 5.8: Update AWS-MCP-SERVERS-GUIDE.md

**Objective:** Remove React deployment reference

**File:** AWS-MCP-SERVERS-GUIDE.md
**Line:** 151

**Change:**
```markdown
# OLD:
- Query best practices for FastAPI + React deployment

# NEW:
- Query best practices for FastAPI + Gradio deployment
```

**Verification:**
```bash
grep -i "react" AWS-MCP-SERVERS-GUIDE.md
# Expected: Empty
```

**Estimated Changes:** ~2 references

---

### Task 5.9: Update docs/configuration-guide.md

**Objective:** Remove frontend configuration documentation

**File:** docs/configuration-guide.md
**Lines:** 53-340

**Changes:**
- Remove: Port 3000 CORS origin examples
- Remove: Frontend server configuration section
- Remove: Frontend port configuration

**Verification:**
```bash
grep -i "3000\|frontend" docs/configuration-guide.md
# Expected: Empty
```

**Estimated Changes:** ~8 references

---

### Task 5.10: Update docs/api/api-security-performance.md

**Objective:** Remove frontend development server references

**File:** docs/api/api-security-performance.md
**Lines:** 7-225

**Changes:**
- Line 7: Remove "Frontend Development: http://127.0.0.1:3000"
- Lines 223-225: Remove localhost:3000 CORS examples

**Verification:**
```bash
grep -i "3000\|frontend.*development" docs/api/api-security-performance.md
# Expected: Empty
```

**Estimated Changes:** ~5 references

---

### Task 5.11: Update docs/PROJECT_ENVIRONMENT_SETUP_GUIDE.md

**Objective:** Remove React setup and troubleshooting

**File:** docs/PROJECT_ENVIRONMENT_SETUP_GUIDE.md
**Lines:** 32-336

**Changes:**
- Remove: React frontend directory structure
- Remove: Vite build instructions
- Remove: Frontend curl test examples
- Remove: "Port 3000 is already in use" troubleshooting section

**Verification:**
```bash
grep -i "react\|vite\|3000" docs/PROJECT_ENVIRONMENT_SETUP_GUIDE.md
# Expected: Empty
```

**Estimated Changes:** ~12 references

---

### Task 5.12: Update docs/CLAUDE_CODE_SLASH_COMMANDS_GUIDE.md

**Objective:** Remove @react-component-architect agent references

**File:** docs/CLAUDE_CODE_SLASH_COMMANDS_GUIDE.md
**Lines:** 178-599

**Changes:**
- Remove: All @react-component-architect mentions
- Remove: React-specific MCP documentation references
- Remove: React component examples
- Update: Agent routing to exclude React frontend tasks

**Verification:**
```bash
grep -i "@react-component-architect\|react" docs/CLAUDE_CODE_SLASH_COMMANDS_GUIDE.md
# Expected: Empty
```

**Estimated Changes:** ~15 references

---

### Task 5.13: Update .claude/commands/new_task.md

**Objective:** Remove React from agent specializations

**File:** .claude/commands/new_task.md
**Line:** 33

**Remove this row:**
```markdown
| **React Components & UI** | `react-component-architect` | Modern React 18.2+ patterns, hooks, PWA features, financial dashboards |
```

**Verification:**
```bash
grep -i "react" .claude/commands/new_task.md
# Expected: Empty
```

**Estimated Changes:** ~3 references

---

### 🔍 Phase 5 Verification

**Run after completing all documentation updates:**

```bash
# Comprehensive grep for React references (exclude task plans and node_modules)
grep -r "react" --exclude-dir={node_modules,.git,test-reports} \
  --exclude="research_task_plan.md" \
  --exclude="TODO_task_plan.md" \
  --exclude="new_research_details.md" \
  . | grep -v "\.pyc\|package-lock.json"
# Expected: Very few or no false positives

# Check for port 3000 references
grep -r "3000" --exclude-dir={node_modules,.git,test-reports} \
  --exclude="research_task_plan.md" \
  --exclude="TODO_task_plan.md" \
  . | grep -v "\.pyc\|package-lock.json"
# Expected: Empty (except maybe git config or historical docs)

# Check for Vite references
grep -r "vite" --exclude-dir={node_modules,.git,test-reports} \
  --exclude="research_task_plan.md" \
  --exclude="TODO_task_plan.md" \
  . | grep -v "\.pyc\|package-lock.json"
# Expected: Empty
```

**Success Criteria:**
- ✅ CLAUDE.md updated (~30 changes)
- ✅ README.md updated (~25 changes)
- ✅ All 13 documentation files updated
- ✅ Grep verification shows no false positives
- ✅ All documentation references only Backend + Gradio

---

## Phase 6: Serena Memory Updates

**Duration:** 60 minutes
**Objective:** Update all Serena memory files to reflect Gradio-only architecture
**Risk:** Low (memory files only)

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

---

### Task 6.1: MAJOR REWRITE - project_architecture.md

**Objective:** Comprehensive rewrite of architecture documentation

**File:** .serena/memories/project_architecture.md

**Changes Required:**

#### 1. Overview Section (Line 5)
**Change:**
```markdown
# OLD:
Market Parser is a Python CLI, React web application, and Gradio ChatInterface...

# NEW:
Market Parser is a Python CLI and Gradio ChatInterface...
```

#### 2. Frontend Options Section
**DELETE ENTIRE SECTION:**
```markdown
### 1. React Web Application (Port 3000)
- Modern responsive interface with real-time chat
- Built with React 18.2+, Vite 5.2+, TypeScript
- Optimized performance (Core Web Vitals: 85%+ improvement)
- Uses FastAPI backend via HTTP requests
- **Simplified footer display** (no metadata extraction, displays complete response)
```

**REORDER:**
- Make Gradio #1
- Make CLI #2

#### 3. Performance Metrics Footer Section
**Update all instances:**
```markdown
# OLD: "CLI, React, and Gradio"
# NEW: "CLI and Gradio"
```

**DELETE:**
- React-specific implementation details
- React frontend footer component references

#### 4. System Architecture Diagram
**UPDATE ASCII diagram:**
- Remove: React GUI box
- Remove: Port 3000 references
- Update: Show only Backend (8000), Gradio (7860), CLI

#### 5. Backend Architecture Section
**UPDATE:**
- Remove: CORS configuration for port 3000
- Remove: Static file serving documentation
- Update: FastAPI serves API only (no static files)

**Estimated Changes:** Major rewrite, ~100+ lines affected

**Verification:**
```bash
grep -i "react\|3000\|vite" .serena/memories/project_architecture.md
# Expected: Empty
```

---

### Task 6.2: DELETE TYPESCRIPT SECTION - code_style_conventions.md

**Objective:** Remove entire React/TypeScript code style section

**File:** .serena/memories/code_style_conventions.md
**Lines:** 118-246

**DELETE ENTIRE SECTION:**
```markdown
## TypeScript/React Code Style

### Component Structure
[...130 lines of React/TypeScript conventions...]

### React Conventions
[...rules and patterns...]

**React Rules:**
- react/react-in-jsx-scope: off
- react/prop-types: off
- react-hooks/rules-of-hooks: error
[...etc...]
```

**Keep:**
- Python code style sections
- General conventions
- Backend-specific rules

**Verification:**
```bash
grep -i "react\|typescript.*react" .serena/memories/code_style_conventions.md
# Expected: Empty
```

**Estimated Changes:** ~130 lines deleted

---

### Task 6.3: Update suggested_commands.md

**Objective:** Remove React/Vite commands

**File:** .serena/memories/suggested_commands.md

**Changes:**

#### Lines 19-21: Startup Commands
**Remove:**
- "Kill existing dev servers (vite)"
- "Start frontend on http://127.0.0.1:3000"

#### Lines 36, 289-291: Vite Commands
**DELETE:**
```bash
vite --mode development
vite --mode staging
vite --mode production
```

#### Line 172: React Scan
**DELETE:**
```bash
# React Scan (component re-renders)
npm run perf:scan
```

#### Lines 221, 298-308: Port/Process Commands
**Remove:**
```bash
curl http://localhost:3000
ps aux | grep vite
pkill -f vite
netstat -tlnp | grep :3000
lsof -i :3000
```

**Keep:**
- Backend commands
- Python/uv commands
- CLI commands
- Gradio commands

**Verification:**
```bash
grep -i "vite\|react\|3000" .serena/memories/suggested_commands.md
# Expected: Empty
```

**Estimated Changes:** ~20 lines

---

### Task 6.4: Update task_completion_checklist.md

**Objective:** Update linting and health check sections

**File:** .serena/memories/task_completion_checklist.md

**Changes:**

#### Line 22: Linting Section
**Change:**
```markdown
# OLD:
# Lint TypeScript/React code
npm run lint

# NEW:
# Lint Python code only
pylint src/backend/
```

#### Line 160: Health Checks
**Remove:**
```bash
curl http://127.0.0.1:3000
```

**Keep only:**
```bash
curl http://127.0.0.1:8000/health  # Backend
curl http://127.0.0.1:7860         # Gradio
```

**Verification:**
```bash
grep -i "react\|typescript.*lint\|3000" .serena/memories/task_completion_checklist.md
# Expected: Empty
```

**Estimated Changes:** ~5 lines

---

### Task 6.5: REWRITE - project_onboarding_summary.md

**Objective:** Update project overview and tech stack

**File:** .serena/memories/project_onboarding_summary.md

**Changes:**

#### Line 5: Overview
**Change:**
```markdown
# OLD:
Market Parser is a Python CLI and React web application...

# NEW:
Market Parser is a Python CLI and Gradio ChatInterface...
```

#### Line 53: Architecture Pattern
**Remove:**
```markdown
- Backend generates markdown → CLI/GUI both render (no custom React components)
```

#### Lines 76-87: Frontend Stack
**DELETE ENTIRE SECTION:**
```markdown
- **Framework**: React 18.2+
- **Build Tool**: Vite 5.2+
- TypeScript
- UI: React Markdown (default rendering, no custom components)
- Performance: Lighthouse CI, React Scan
```

**REPLACE WITH:**
```markdown
**Frontend Stack:**
- **Framework**: Gradio 5.49.1+
- **Type**: Python ChatInterface
- **Rendering**: Built-in Gradio markdown
```

#### Lines 105-106: Directory Structure
**Remove:**
```markdown
│   └── frontend/            # React frontend
│       ├── components/      # React components (simplified markdown rendering)
```

#### Line 201: Code Style
**Remove:**
```markdown
- **React**: Functional components with hooks
```

#### Line 344: Development URLs
**Remove:**
```markdown
- **Frontend**: http://127.0.0.1:3000
```

**Update to:**
```markdown
- **Backend**: http://127.0.0.1:8000
- **Gradio**: http://127.0.0.1:7860
```

**Verification:**
```bash
grep -i "react\|vite\|3000" .serena/memories/project_onboarding_summary.md
# Expected: Empty
```

**Estimated Changes:** ~50 lines

---

### Task 6.6: Update SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE.md

**Objective:** Remove React setup instructions

**File:** .serena/memories/SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE.md

**Changes:**

#### Line 38: Directory Structure
**Remove:**
```markdown
│   └── frontend/            # React frontend
```

#### Lines 86-90: Process Management
**Remove:**
```bash
pkill -f "vite"
netstat -tlnp | grep -E ":(3000|8000|5500)"
```

**Update to:**
```bash
# Kill development servers
pkill -f "uvicorn"
pkill -f "gradio"
netstat -tlnp | grep -E ":(7860|8000)"
```

#### Lines 232-287: Frontend Setup
**DELETE ENTIRE SECTION:**
```markdown
### Frontend Build
vite v5.4.20 building for production...
[...vite build output...]
curl -s http://127.0.0.1:3000 | head -10
```

#### Lines 404-413: Troubleshooting
**DELETE:**
```markdown
**Symptoms:** `Error: Port 3000 is already in use`
**Solution:**
lsof -ti:3000 | xargs kill -9
```

**Verification:**
```bash
grep -i "react\|vite\|3000" .serena/memories/SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE.md
# Expected: Empty
```

**Estimated Changes:** ~60 lines

---

### Task 6.7: Update adaptive_formatting_guide.md

**Objective:** Update markdown rendering reference

**File:** .serena/memories/adaptive_formatting_guide.md
**Line:** 322

**Change:**
```markdown
# OLD:
- Tables render correctly in GUI (react-markdown)

# NEW:
- Tables render correctly in Gradio markdown rendering
```

**Verification:**
```bash
grep -i "react" .serena/memories/adaptive_formatting_guide.md
# Expected: Empty
```

**Estimated Changes:** ~2 lines

---

### Task 6.8: Update ui_refactor_oct_2025.md

**Objective:** Remove React DevTools reference

**File:** .serena/memories/ui_refactor_oct_2025.md
**Line:** 216

**Remove:**
```markdown
- Use React DevTools for component inspection
```

**Alternative:** Update to Gradio development tools if applicable

**Verification:**
```bash
grep -i "react" .serena/memories/ui_refactor_oct_2025.md
# Expected: Empty
```

**Estimated Changes:** ~3 lines

---

### 🔍 Phase 6 Verification

**Run after completing all Serena memory updates:**

```bash
# Verify no React references in memories
grep -ri "react" .serena/memories/ | grep -v "\.pkl\|cache"
# Expected: Empty

# Verify no port 3000 references
grep -r "3000" .serena/memories/ | grep -v "\.pkl\|cache"
# Expected: Empty

# Verify no Vite references
grep -ri "vite" .serena/memories/ | grep -v "\.pkl\|cache"
# Expected: Empty

# Read each memory file to verify accuracy
cat .serena/memories/project_architecture.md | head -50
cat .serena/memories/code_style_conventions.md | grep -A 5 "## Python"
# Manual review of first sections
```

**Success Criteria:**
- ✅ All 8 memory files updated
- ✅ project_architecture.md completely rewritten
- ✅ code_style_conventions.md TypeScript section deleted
- ✅ No React/Vite/port 3000 references remain
- ✅ All memories accurately reflect Gradio-only architecture

---

## Phase 7: Testing & Validation (MANDATORY)

**Duration:** 45 minutes
**Objective:** Comprehensive testing to validate all changes
**Risk:** Critical - must pass before proceeding

🔴 **CRITICAL: YOU MUST run tests BEFORE claiming completion**
🔴 **CRITICAL: Task is INCOMPLETE without test execution and results**

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

---

### Task 7.1: CLI Regression Test Suite (Phase 1)

**Objective:** Execute 39-test CLI regression suite

**Actions:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Expected Results:**
- ✅ Tests completed: 39/39 COMPLETED (100% generation rate)
- ✅ Average response time: < 12s (EXCELLENT rating)
- ✅ All tests generate responses
- ✅ Performance metrics footer appears in ALL responses

**Verification:**
- Test report generated in test-reports/
- No import errors
- No backend errors
- Session persistence verified

---

### Task 7.2: CLI Test Suite Phase 2a - ERROR DETECTION (MANDATORY)

🔴 **MANDATORY - YOU MUST RUN these grep commands and SHOW output**

**Command 1: Find all errors/failures**
```bash
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log
```

**Command 2: Count 'data unavailable' errors**
```bash
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log
```

**Command 3: Count completed tests**
```bash
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Required Output:** Paste ALL grep command outputs

---

### Task 7.3: CLI Test Suite Phase 2b - DOCUMENT FAILURES

**If Phase 2a grep commands found errors, create evidence-based failure table:**

| Test # | Test Name | Line # | Error Message | Tool Call (if visible) |
|--------|-----------|--------|---------------|------------------------|
| (Example) 3 | SPY_Yesterday_Price_OHLC | 157 | data unavailable | get_stock_price_history(...) |

**If NO errors found:** Confirm "0 failures found"

---

### Task 7.4: CLI Test Suite Phase 2c - VERIFY RESPONSE CORRECTNESS

**For tests without errors in Phase 2a, verify:**

1. ✅ Response directly addresses the prompt query
2. ✅ Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
3. ✅ Appropriate tool calls made (Polygon, Tradier)
4. ✅ Data formatting matches expected format (OHLC, tables, etc.)
5. ✅ No hallucinated data or made-up values
6. ✅ Options chains show Bid/Ask columns (NOT midpoint)
7. ✅ Technical analysis includes proper indicators
8. ✅ Response is complete (not truncated)
9. ✅ Performance metrics footer visible and correct

---

### Task 7.5: CLI Test Suite Phase 2d - CHECKPOINT QUESTIONS

**Answer ALL checkpoint questions with evidence:**

1. ✅ Did you RUN the 3 mandatory grep commands in Phase 2a? **YES/NO + SHOW OUTPUT**
2. ✅ Did you DOCUMENT all failures found (or confirm 0 failures)? **YES/NO + TABLE OR "0 failures"**
3. ✅ Failure count from grep -c "data unavailable": **X failures**
4. ✅ Tests that generated responses: **X/39 COMPLETED**
5. ✅ Tests that PASSED verification (no errors): **X/39 PASSED**

🔴 **CANNOT MARK TASK COMPLETE WITHOUT:**
- Running and showing grep outputs
- Documenting failures with evidence (or confirming 0 failures)
- Providing failure count
- Answering all 5 checkpoint questions with evidence

---

### Task 7.6: Manual Gradio UI Testing

**Objective:** Verify Gradio UI works correctly

**Actions:**
```bash
# Start Gradio
uv run python src/backend/gradio_app.py
```

**Manual Tests:**

1. ✅ **Basic Query Test**
   - Query: "Market Status"
   - Expected: Response with performance metrics footer

2. ✅ **Stock Price Test**
   - Query: "Tesla current stock price"
   - Expected: TSLA price with OHLC data + footer

3. ✅ **Options Chain Test**
   - Query: "SPY call options chain"
   - Expected: Options table with Bid/Ask + footer

4. ✅ **Multi-Ticker Test**
   - Query: "Current price for AMD, NVDA, WDC"
   - Expected: All 3 stocks with data + footer

5. ✅ **Footer Verification**
   - Verify footer shows: Response Time, Tokens Used, Model
   - Verify footer format matches CLI format

**Success Criteria:**
- All 5 manual tests pass
- No errors in Gradio console
- Performance metrics footer visible in all responses
- Footer format correct

---

### Task 7.7: Backend Health Check

**Objective:** Verify backend starts and responds correctly

**Actions:**
```bash
# Start backend
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 &

# Wait for startup
sleep 3

# Test health endpoint
curl http://127.0.0.1:8000/health

# Test API endpoint
curl -X POST http://127.0.0.1:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Market Status"}'

# Cleanup
pkill -f uvicorn
```

**Expected Results:**
- ✅ Health endpoint returns 200 OK
- ✅ Chat endpoint returns response with footer
- ✅ No CORS errors
- ✅ No static file serving errors

---

### Task 7.8: Startup Script Testing

**Objective:** Verify startup scripts work with backend + Gradio only

**Test start-app.sh:**
```bash
./start-app.sh
```

**Verify:**
1. ✅ Backend starts on port 8000
2. ✅ Gradio starts on port 7860
3. ✅ No errors about port 3000 or frontend
4. ✅ Health checks pass for both services
5. ✅ Success message shows 2 services only
6. ✅ Provided URLs work (backend API, Gradio UI)

**Cleanup:**
```bash
pkill -f uvicorn
pkill -f "python.*gradio"
```

**Test start-app-xterm.sh (if X11/tmux available):**
```bash
./start-app-xterm.sh
```

**Verify:**
1. ✅ Opens 2 windows (backend, Gradio) - NO frontend window
2. ✅ Both services start successfully
3. ✅ Health checks pass

**Success Criteria:**
- Both startup scripts work
- No frontend/vite references in output
- All services start correctly

---

### 🔍 Phase 7 Verification Summary

**Required Evidence Before Proceeding:**

**CLI Tests:**
- ✅ Test suite executed: 39/39 tests
- ✅ Grep commands run (3 commands with output shown)
- ✅ Failures documented (or 0 failures confirmed)
- ✅ Response verification completed
- ✅ Checkpoint questions answered with evidence
- ✅ Test report path provided

**Gradio Tests:**
- ✅ 5 manual tests passed
- ✅ Footer verified in all responses

**Backend Tests:**
- ✅ Health check passes
- ✅ API endpoint works
- ✅ No errors on startup

**Startup Scripts:**
- ✅ Both scripts tested and working

**Overall Success Criteria:**
- ✅ 100% CLI test pass rate (39/39)
- ✅ All Gradio manual tests pass
- ✅ Backend functional
- ✅ Startup scripts working
- ✅ Performance metrics footer visible everywhere

🔴 **IF ANY TESTS FAIL:** Fix issues and re-test before proceeding

---

## Phase 8: Final Verification & Cleanup

**Duration:** 20 minutes
**Objective:** Final grep audit and cleanup
**Risk:** Low (verification only)

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

---

### Task 8.1: Comprehensive Grep Verification

**Objective:** Find any remaining React/Vite/port 3000 references

**Command 1: Search for React**
```bash
grep -r "react" \
  --exclude-dir={node_modules,.git,test-reports,__pycache__} \
  --exclude="research_task_plan.md" \
  --exclude="TODO_task_plan.md" \
  --exclude="new_research_details.md" \
  --exclude="package-lock.json" \
  . | grep -v "\.pyc"
```

**Expected:** Empty (or only false positives like "contract", "interact")

---

**Command 2: Search for Port 3000**
```bash
grep -r "3000" \
  --exclude-dir={node_modules,.git,test-reports,__pycache__} \
  --exclude="research_task_plan.md" \
  --exclude="TODO_task_plan.md" \
  . | grep -v "\.pyc"
```

**Expected:** Empty (except maybe historical git references)

---

**Command 3: Search for Vite**
```bash
grep -r "vite" \
  --exclude-dir={node_modules,.git,test-reports,__pycache__} \
  --exclude="research_task_plan.md" \
  --exclude="TODO_task_plan.md" \
  . | grep -v "\.pyc"
```

**Expected:** Empty

---

**Command 4: Verify no .tsx/.jsx files**
```bash
find . -type f \( -name "*.tsx" -o -name "*.jsx" \) | grep -v node_modules
```

**Expected:** Empty

---

**Command 5: Verify no frontend directory**
```bash
ls -la src/ | grep frontend
```

**Expected:** Empty

---

**Command 6: Verify no dist directories**
```bash
ls -la | grep -E "^d.*dist"
```

**Expected:** Empty

---

**Success Criteria:**
- ✅ All grep searches return empty or acceptable false positives
- ✅ No React source files remain
- ✅ No build artifacts remain

**If any unexpected references found:** Update those files before proceeding

---

### Task 8.2: Clean Up Log Files

**Objective:** Remove any frontend.log or related files

**Actions:**
```bash
# Remove frontend log if exists
rm -f frontend.log

# Remove any other React-related logs
find . -name "*vite*.log" -o -name "*frontend*.log" | grep -v node_modules | xargs rm -f

# Verify
ls -la | grep -E "frontend|vite"
# Expected: Empty
```

---

### Task 8.3: Verify Git Status

**Objective:** Review all changes before commit

**Actions:**
```bash
# Check branch
git branch --show-current
# Expected: react_retirement

# See all changed files
git status

# Review changes
git diff --stat

# Count changed files
git status --short | wc -l
```

**Expected Changed Files:** ~60-70 files
- Deleted: ~40 files (src/frontend/, config files, build outputs)
- Modified: ~30 files (docs, memories, scripts, backend, package.json)

---

### 🔍 Phase 8 Final Checklist

**Before proceeding to commit, verify:**

- ✅ All grep searches clean (no unexpected React references)
- ✅ No .tsx/.jsx files remain
- ✅ No src/frontend/ directory
- ✅ No dist/ or dev-dist/ directories
- ✅ No vite config files
- ✅ No frontend log files
- ✅ Git status shows all expected changes
- ✅ All tests passed (Phase 7)
- ✅ Gradio UI working
- ✅ CLI working
- ✅ Backend API working
- ✅ Startup scripts working

🔴 **STOP:** Do NOT proceed to Phase 9 unless ALL checkboxes above are ✅

---

## Phase 9: Atomic Commit & Push

**Duration:** 10 minutes
**Objective:** Create comprehensive atomic commit
**Risk:** Low (commit only)

🔴 **CRITICAL: PROPER ATOMIC COMMIT WORKFLOW**

🔴 **MANDATORY:** Use Sequential-Thinking at START of this phase

---

### Task 9.1: Verify ALL Work Complete

**DO NOT stage anything yet - just verify**

**Checklist:**
- ✅ ALL code changes complete (src/frontend deleted, backend updated)
- ✅ ALL tests run and passed (39/39 CLI tests)
- ✅ ALL documentation updated (15 files)
- ✅ ALL Serena memories updated (8 files)
- ✅ ALL config files updated (package.json, app.config.json)
- ✅ ALL startup scripts updated (2 files)
- ✅ ALL task plans updated (this file, research plan)
- ✅ Test reports generated and verified

**Review Changes:**
```bash
git status
git diff --stat
```

**Expected Files:**
- Deleted: src/frontend/ directory, vite.config.ts, tsconfig.json, index.html, dist/, dev-dist/, public/, .eslintrc.cjs
- Modified: package.json, package-lock.json, src/backend/main.py, config/app.config.json, start-app*.sh, CLAUDE.md, README.md, ~40 other docs/memories
- New: test-reports/test_cli_regression_loop1_*.log (2 files)

---

### Task 9.2: Stage ALL Files at Once

**⚠️ This is the FIRST time you run `git add`**

**Actions:**
```bash
git add -A
```

**Immediately verify staging:**
```bash
git status
```

**Verify:**
- ✅ ALL changed files are staged (green)
- ✅ NO files remain unstaged (red)
- ✅ Deleted files shown as "deleted:"
- ✅ Modified files shown as "modified:"
- ✅ New test reports shown as "new file:"

**If anything missing:** `git add [missing-file]`

---

### Task 9.3: Create Atomic Commit (Within 60 seconds of staging)

**Objective:** Commit ALL changes together with comprehensive message

**Actions:**
```bash
git commit -m "$(cat <<'EOF'
[REACT-RETIREMENT] Complete React Frontend Removal - Gradio-Only Migration

Problem: React frontend added complexity and deployment overhead for
prototyping needs. Gradio provides simpler Python-only UI stack.

Objective: Complete removal of React frontend, migrating to Gradio-only
Python UI for simplified development and AWS deployment preparation.

Solution: Systematic retirement of React across 8 major categories with
comprehensive documentation and memory updates.

Code Changes (60+ files):

**1. Source Code Deletion (30 files):**
- Deleted: src/frontend/ directory (complete removal)
  - components/ (8 .tsx files)
  - services/, config/, types/, utils/, styles/
  - App.tsx, main.tsx, index.css, wdyr.ts
- Deleted: index.html (React entry point)
- Deleted: public/ directory (PWA icons)
- Deleted: dist/, dev-dist/ (build outputs)

**2. Build & Config Files (10 files):**
- Deleted: vite.config.ts, vite-env.d.ts
- Deleted: tsconfig.json (frontend TypeScript config)
- Deleted: .eslintrc.cjs (React ESLint config)
- Updated: .pre-commit-config.yaml (removed eslint-plugin-react)
- Updated: .vscode/settings.json (removed React language configs)

**3. Package Cleanup:**
- Removed 14 dependencies: react, react-dom, react-markdown, react-scan,
  @types/react, @types/react-dom, @vitejs/plugin-react, eslint-plugin-react,
  eslint-plugin-react-hooks, eslint-plugin-react-refresh, vite
- Removed npm scripts: frontend:dev, perf:scan, build, preview
- Regenerated: package-lock.json (removed ~100+ transitive dependencies)

**4. Backend Modifications:**
- src/backend/main.py:
  - Removed: StaticFiles import
  - Removed: CORS configuration for port 3000
  - Removed: Static file serving (lines 126-128)
- config/app.config.json:
  - Deleted: Entire "frontend" section (lines 49-67)
  - Updated: CORS origins (removed port 3000 origins)

**5. Startup Scripts (2 files, ~230 lines removed):**
- start-app.sh: Removed all React/Vite startup, health checks, port 3000
- start-app-xterm.sh: Removed all React/Vite startup, tmux frontend session
- Updated: Success messages to show Backend + Gradio only
- Updated: Health check conditions (removed FRONTEND_READY)

**6. Documentation Updates (15 files, ~150 references updated):**
- Main docs: CLAUDE.md, README.md, AGENTS.md
- Deployment: DEPLOYMENT.md, DEPLOYMENT-SUMMARY.md, DEPLOYMENT-QUICKSTART.md
- Guides: START_SCRIPT_README.md, configuration-guide.md, api-security-performance.md
- Setup: PROJECT_ENVIRONMENT_SETUP_GUIDE.md
- Commands: CLAUDE_CODE_SLASH_COMMANDS_GUIDE.md, new_task.md
- AWS: AWS-MCP-SERVERS-GUIDE.md
- Updated all: Port references (8000/3000/7860 → 8000/7860)
- Removed all: React Web App sections, Node.js prerequisites

**7. Serena Memory Updates (8 files, ~370 lines updated):**
- project_architecture.md: MAJOR REWRITE (removed React sections, updated diagrams)
- code_style_conventions.md: DELETED entire TypeScript/React section (~130 lines)
- suggested_commands.md: Removed all React/Vite commands (~20 lines)
- task_completion_checklist.md: Updated linting, health checks (~5 lines)
- project_onboarding_summary.md: Rewrote frontend stack section (~50 lines)
- SERNENA_PROJECT_ENVIRONMENT_SETUP_GUIDE.md: Removed React setup (~60 lines)
- adaptive_formatting_guide.md: Updated markdown rendering ref (~2 lines)
- ui_refactor_oct_2025.md: Removed React DevTools reference (~3 lines)

Test Results (MANDATORY CLI Regression Suite):

**Phase 1: Response Generation**
- ✅ Tests completed: 39/39 COMPLETED (100% generation rate)
- ✅ Average response time: X.XXs (EXCELLENT rating)
- ✅ Performance range: X.XXs - XX.XXs (all under 30s threshold)

**Phase 2a: Error Detection (Grep Evidence)**
Command 1: grep -i "error|unavailable|failed|invalid" test-reports/test_cli_regression_loop1_*.log
Result: [NO ERRORS or list specific errors]

Command 2: grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log
Result: 0 (ZERO errors)

Command 3: grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
Result: 40 (39 tests + 1 summary line)

**Phase 2b: Failures Documented**
- ✅ 0 failures found OR [provide failure table]

**Phase 2c: Response Verification**
- ✅ All responses address prompts correctly
- ✅ Proper tool calls made (Polygon, Tradier)
- ✅ Performance metrics footer visible in ALL responses
- ✅ Footer format correct (Response Time, Tokens, Model)

**Phase 2d: Checkpoint Questions (Evidence-Based)**
1. ✅ RAN 3 mandatory grep commands? YES - Output shown above
2. ✅ DOCUMENTED failures? YES - 0 failures confirmed
3. ✅ Failure count from grep -c "data unavailable": 0 failures
4. ✅ Tests that generated responses: 39/39 COMPLETED
5. ✅ Tests that PASSED verification: 39/39 PASSED

**Manual Testing Completed:**
- ✅ Gradio UI: 5 manual tests passed (Market Status, Stock Price, Options, Multi-Ticker, Footer)
- ✅ Backend: Health check passed, API endpoint functional
- ✅ CLI: Working correctly with footer
- ✅ Startup Scripts: Both scripts tested and working (Backend + Gradio only)

Success Metrics:
- ✅ Source code deletion: 100% SUCCESS (src/frontend/, all build files removed)
- ✅ Package cleanup: 100% SUCCESS (14 npm packages removed, lockfile regenerated)
- ✅ Backend updates: 100% SUCCESS (no static serving, CORS updated)
- ✅ Startup scripts: 100% SUCCESS (both scripts refactored, tested working)
- ✅ Documentation: 100% SUCCESS (15 files updated, all React references removed)
- ✅ Serena memories: 100% SUCCESS (8 files updated, architecture rewritten)
- ✅ Testing: 100% SUCCESS (39/39 CLI tests PASSED, Gradio validated)
- ✅ Grep verification: CLEAN (no unexpected React/Vite/port 3000 references)

Files Changed:
- Deleted: 40 files (src/frontend/, vite.config.ts, tsconfig.json, etc.)
- Modified: 30 files (docs, memories, backend, scripts, configs)
- New: 2 test reports (evidence of passing tests)
- Total: 72 files

Key Insights:
- Simplified architecture: Python-only stack reduces complexity
- Deployment ready: No Node.js/npm required for AWS deployment
- Gradio sufficient: Proven functional for all financial queries
- Zero duplication: Backend serves both CLI and Gradio
- Comprehensive cleanup: No React artifacts remain

Architecture Changes:
- Before: CLI + React (port 3000) + Gradio (port 7860) + Backend (port 8000)
- After: CLI + Gradio (port 7860) + Backend (port 8000)
- Reduction: 1 fewer service, 1 fewer port, ~500MB fewer dependencies

Test Report: test-reports/test_cli_regression_loop1_[timestamp].log
Research Plan: research_task_plan.md (15,700+ words)
Task Plan: TODO_task_plan.md (comprehensive checklist)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

### Task 9.4: Verify Commit Created

**Actions:**
```bash
# Verify commit
git log -1 --stat

# Verify no unstaged changes
git status
# Expected: "nothing to commit, working tree clean"
```

**Success Criteria:**
- ✅ Commit created with comprehensive message
- ✅ All files included in commit
- ✅ Working tree clean (no unstaged changes)

---

### Task 9.5: Push to Remote

**Actions:**
```bash
git push
```

**Expected:**
- Push successful to origin/react_retirement
- All changes uploaded

**Verification:**
```bash
git status
# Expected: "Your branch is up to date with 'origin/react_retirement'"
```

---

### 🎉 Task Complete!

**Final Verification:**

✅ **ALL PHASES COMPLETE:**
1. ✅ Phase 1: File & Directory Deletion
2. ✅ Phase 2: Package & Dependency Cleanup
3. ✅ Phase 3: Backend Code Modifications
4. ✅ Phase 4: Startup Script Refactoring
5. ✅ Phase 5: Documentation Updates
6. ✅ Phase 6: Serena Memory Updates
7. ✅ Phase 7: Testing & Validation (MANDATORY)
8. ✅ Phase 8: Final Verification & Cleanup
9. ✅ Phase 9: Atomic Commit & Push

✅ **SUCCESS CRITERIA MET:**
- ✅ 60+ files deleted/modified
- ✅ All React source code removed
- ✅ All documentation updated
- ✅ All Serena memories updated
- ✅ 39/39 CLI tests PASSED
- ✅ Gradio UI validated
- ✅ Backend functional
- ✅ Startup scripts working
- ✅ Comprehensive atomic commit
- ✅ Pushed to remote

**React Frontend Retirement: COMPLETE! 🎉**

---

## Appendix: Quick Reference

### Critical Commands

**Testing:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Verification Greps:**
```bash
grep -r "react" --exclude-dir={node_modules,.git,test-reports} .
grep -r "3000" --exclude-dir={node_modules,.git,test-reports} .
grep -r "vite" --exclude-dir={node_modules,.git,test-reports} .
```

**Startup:**
```bash
./start-app.sh  # Backend + Gradio
./start-app-xterm.sh  # Backend + Gradio (tmux/xterm mode)
```

**Manual Tests:**
```bash
# Gradio
uv run python src/backend/gradio_app.py

# CLI
uv run src/backend/main.py

# Backend
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000
```

---

## Time Estimates Summary

| Phase | Duration | Risk |
|-------|----------|------|
| Phase 0: Pre-Implementation | 10 min | Low |
| Phase 1: File Deletion | 30 min | Low |
| Phase 2: Package Cleanup | 15 min | Low |
| Phase 3: Backend Modifications | 20 min | Medium |
| Phase 4: Startup Scripts | 30 min | Medium |
| Phase 5: Documentation | 90 min | Low |
| Phase 6: Serena Memories | 60 min | Low |
| Phase 7: Testing (MANDATORY) | 45 min | Critical |
| Phase 8: Final Verification | 20 min | Low |
| Phase 9: Atomic Commit | 10 min | Low |
| **TOTAL** | **5.5 hours** | |

---

**END OF TODO TASK PLAN**

This comprehensive task plan provides systematic, granular implementation steps for complete React frontend retirement. Follow each phase sequentially, verify after each major task, and DO NOT skip the mandatory testing phase.
