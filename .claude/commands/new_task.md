# New Task Slash Command

Execute complex development tasks using AI Team orchestration with the @agent-tech-lead-orchestrator.

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