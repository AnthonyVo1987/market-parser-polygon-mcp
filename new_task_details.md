# New Task Details

## Task Description

[MIGRATION] Add Hard Coded Port Detection & Simplified App Start Scripts

Task 1. Add a new enhancement to remove ALL hard coded ports in .env and any envrionment variables, and instead, update code to only use hard coded IP and ports for all the Frontend & Backend Dev servers, and then update the rest of code accordingly to handle the new static IP & Ports for all Dev servers. This will help prevent the previous "dynamic port" config detetion we ran into and will simplify the code more. The expected outcome is that now whenever User, AI Agents, or Tests scripts try to start up all dev servers and to run the app, everything is consistent.  This prevents false trigger failures if an IP\Port happens to be in use, and a server got started with a different IP\Port, and then the Main app did not realize the different expected IP\Port, and so the app has a false trigger failure due to a simple server address config issue.  This prevent confusion for real failure vs setup\config issues.  It also makes no sense to have any hard coded IP\Port in a .env or environemnt variable because that will NOT help future task(s) that will want to deploy our app to AWS to the cloud, since deploying apps do NOT use environement variables like that.

Some example .env items to move:

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🖥️  FASTAPI SERVER CONFIGURATION

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# FastAPI Server Host (Optional)

# 🌍 Default: 0.0.0.0 (accepts connections from any IP)

# 🏠 Use 127.0.0.1 or localhost for local-only access

FASTAPI_HOST=0.0.0.0

# FastAPI Server Port (Optional)

# 🔌 Default: 8000

# ⚡ Change if port 8000 is already in use

FASTAPI_PORT=8000

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🌐 CORS & FRONTEND CONFIGURATION

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Additional CORS Origins (Optional)

# 🔗 Comma-separated list of allowed origins for CORS

# 🎯 Default origins already include localhost:3000, localhost:3001

# 🌍 Add production domains as needed

# CORS_ORIGINS=<http://localhost:3000,http://localhost:3001,https://your-domain.com>

Task 2. Based on the new static IP\Port code fixes from Task 1, generate new bash .sh script(s) to help automate and start our app easier in a single command for easier user use. Right now the app needs multiple bash commands to start multiple servers, FastAPI, CORS, VITE etc AND they all need to be kept running WHILE the app is running. So optmially, the single bash .sh command needs to perform the following:

A. Kill ONLY any running dev server(s) ( FastAPI, CORS, VITE etc).  Needs to focus on detecting and killing JUST the dev servers and NOT anything else, such as our EXCLUDING KILLING required Polygon MCP Servers, MCP Tools servers etc.  Confirm that ALL the app's dev servers only are killed before moving onto the next step.

B. Start all dev servers, ONE AT A TIME IN THEIR OWN SEPARATE BASH\TERMINAL window, and then verify they are all running and correct. If any issues, try and re--start servers again

C. Sanity check that ALL dev servers are running properly and STILL running, there should be at least 2x Dev servers, frontend & backend

D. If Sanity Check PASSES that ALL dev servers are running properly and STILL running, THEN the script can call the React GUI Local Browswer Address to run the GUI in the User's web browser

Expected outcome is running a single bash .sh script will have the entire GUI started up in the user's browser, running all the requred steps beforehand to be truly "one-click app start"

## Research Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

- Research & Analyze task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last

## Planning Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

- IF RESEARCH FROM Tasks were NOT performed, this is a VIOLATION and task must be restarted from the beginning
- Based on the research task(s), generate fully detailed, granular, implementation plan task breakdown todo checklist to complete all the requested task(s)

## Implementation Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the task(s)

- Based on all the research & newly generated implementation plan task breakdown, perform the requested todo checklist task(s)

## Final Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to perform Final 4 Tasks

Final Task 1: Review/Fix Loop

- SPECIALISTS performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle WITH LINT until achieving PASSING code review status

Final Task 2: Task Summary Updates for LAST_TASK_SUMMARY.md & CLAUDE.md

- Generate detailed task completion summary & OVERWRITE the doc "LAST_TASK_SUMMARY.md"
- Based on detailed task completion summary, generate high level task completion summary 20 lines MAX for updating CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

Final Task 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic git commit containing ALL changes: code files, CLAUDE.md, LAST_TASK_SUMMARY.md, documentation updates, test reports, task summary etc
- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Final Task 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly git committed and git pushed

**Key Requirements:**

## Requirements

## Expected Outcome*

## Additional Context
