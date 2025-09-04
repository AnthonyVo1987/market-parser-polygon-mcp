# New Task Slash Command

Execute complex development tasks using AI Team orchestration with the tech-lead-orchestrator.

## How to Use

1. **Edit task details** in `new_task_details.md`
2. **Run this command**: `/new_task`
3. **Follow the orchestrated plan** as specialists complete each task

## What This Command Does

When you invoke `/new_task`, I will:

1. **Read your task details** from `new_task_details.md`
2. **Invoke @agent-tech-lead-orchestrator** to analyze the task and create a specialist assignment plan
3. **Execute the plan** using the exact agents recommended by the tech-lead
4. **Ensure MCP tool compliance** for all specialists
5. **Create actual deliverables** (not just summaries)

## Command Execution

I'll read the task details from new_task_details.md and use @agent-tech-lead-orchestrator to analyze the requirements and assign the appropriate specialists from the available AI Team:

**Available Specialists (per CLAUDE.md):**

| Task Category | Agent | Responsibilities | Notes |
|---------------|-------|------------------|-------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, merges. Security-aware reviews, quality assurance for both Python and React code | Required for all development work |
| **Python Backend Development** | `@backend-developer` | Python/Pydantic AI development, FSM management, dual-mode processing, MCP server integration, backend API design | Primary architect for Python application logic |
| **React Frontend Architecture** | `@react-component-architect` | React component design, Next.js 14+ architecture, modern React patterns, component library integration | Leads React frontend development and component architecture |
| **API Design & Integration** | `@api-architect` | Backend-Frontend API contracts, RESTful API design, response schema design, integration patterns | Ensures clean data flow between Python backend and React frontend |
| **Documentation & Architecture** | `@documentation-specialist` | Architecture documentation, user guides, API documentation, component documentation, migration planning | Maintains comprehensive project documentation |
| **Deep Analysis & Planning** | `@code-archaeologist` | Complex architectural decisions, system analysis, migration strategy, technical debt assessment | On-demand for major architectural changes and system analysis |

**MCP Tool Requirements:**
All specialists MUST use:

- `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` for research
- `mcp__filesystem__*` tools for all file operations

---

## Execution Protocol

I'll read the task from new_task_details.md, then use @agent-tech-lead-orchestrator to get proper agent assignments and execute the plan with those exact specialists, ensuring all MCP tools are used and actual deliverables are created. Upon task completion, I will execute the mandatory post-task actions outlined below.

---

## 🚨 MANDATORY POST-TASK ACTIONS

After completing the primary task execution, the following 4-step procedure MUST be executed to ensure production readiness and quality assurance:

### Step 1: Review/Fix Loop
- Specialist performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle until achieving PASSING code review status

### Step 2: Task Summary & CLAUDE.md Update
- Generate comprehensive task completion summary
- Update CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

### Step 3: Atomic Git Commit & Push
- Run `git status` to review all staged and unstaged changes
- Create single atomic commit containing ALL changes: code files, documentation updates, and task summary
- Push commit to GitHub repository using provided personal access token
- **CRITICAL**: Must push to complete the workflow - commit without push is incomplete

### Step 4: Final Verification
- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly committed and pushed

**Key Requirements:**
- Single atomic commit prevents code vs documentation separation
- All changes (code + docs + summary) must be committed together
- Task summary generation occurs BEFORE git commit to ensure inclusion
- Automated workflow ensures consistency and completeness
