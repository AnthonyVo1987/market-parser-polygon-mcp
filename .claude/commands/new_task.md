# New Task Slash Command

Execute complex development tasks using AI Team orchestration with the @agent-tech-lead-orchestrator.

**Prototyping Focus:** All tasks enforce prototyping principles - no over-engineering, no enterprise-grade solutions, no testing/CI/CD during prototype phase.

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

## Available Specialists (per CLAUDE.md)

| Task Category | Agent | Responsibilities | Notes |
|---------------|-------|------------------|-------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, merges. Security-aware reviews, quality assurance for both Python and React code | Required for all development work |
| **Python Backend Development** | `@backend-developer` | Python/Pydantic AI development, FSM management, dual-mode processing, MCP server integration, backend API design | Primary architect for Python application logic |
| **React Frontend Architecture** | `@react-component-architect` | React component design, Next.js 14+ architecture, modern React patterns, component library integration | Leads React frontend development and component architecture |
| **API Design & Integration** | `@api-architect` | Backend-Frontend API contracts, RESTful API design, response schema design, integration patterns | Ensures clean data flow between Python backend and React frontend |
| **Documentation & Architecture** | `@documentation-specialist` | Architecture documentation, user guides, API documentation, component documentation, migration planning | Maintains comprehensive project documentation |
| **Deep Analysis & Planning** | `@code-archaeologist` | Complex architectural decisions, system analysis, migration strategy, technical debt assessment | On-demand for major architectural changes and system analysis |

## MCP Tool Requirements

MCP Tools are PRIMARY tools for ALL specialists. All specialists MUST use:

- `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` for research
- `mcp__filesystem__*` tools for all file operations
- `mcp__github__*` tools as primary method for repo operations

---

## Execution Protocol - Enhanced A-I Workflow

The `/new_task` command follows a systematic A-I process with tech-lead orchestration for ALL modes (Plan and Non-Plan).

### A-I Workflow Steps

**A. User Invokes `/new_task`**

- User provides task details via `/new_task` command
- Task details captured from `new_task_details.md` for analysis and planning

**B. Main Agent uses @agent-tech-lead-orchestrator (MANDATORY)**

- Required for BOTH Plan Mode and Non-Plan Mode
- Tech-lead reads, analyzes, and reviews task details in `new_task_details.md`
- Systematic evaluation of requirements and specialist assignment planning

**C. Plan Mode: Tech-Lead Orchestrated Planning**

- `@agent-tech-lead-orchestrator` generates comprehensive plan WITH Specialist Assignments
- Detailed task breakdown with specialist role allocations and dependencies

**D. Non-Plan Mode: Tech-Lead Orchestrated Planning**

- `@agent-tech-lead-orchestrator` generates streamlined plan WITH Specialist Assignments
- Focused task execution plan with efficient specialist coordination

**E. Specialist(s) Execute Plan**

- Specialists execute plan from `@agent-tech-lead-orchestrator` using exact assignments
- ALL specialists MUST use MCP tools as PRIMARY method (fallback to default tools if needed)
- Prototyping principles enforced: no over-engineering, functional delivery focus

**F. Review/Fix Loop - Final Task 1**

- Specialist performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking`
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__*` calls for documentation/best practices if needed
- Continue review/fix cycle WITH LINT until achieving PASSING status

**G. Task Summary & CLAUDE.md Update - Final Task 2**

- Generate comprehensive Last Completed Task Summary → overwrite `LAST_TASK_SUMMARY.md`
- Generate MAX 20-line high-level overview → update CLAUDE.md task summary section
- Include all deliverables, changes made, and completion status for atomic commit

**H. Atomic Git Commit & Push - Final Task 3**

- PRIMARY: Use `mcp__github__push_files` for atomic operations
- Single atomic commit containing ALL changes:
  - Code/file changes
  - Documentation updates  
  - CLAUDE.md updates
  - LAST_TASK_SUMMARY.md updates
- **CRITICAL**: Must push to complete workflow - commit without push is incomplete

**I. Final Verification - Final Task 4**

- Run final verification to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly committed and pushed to GitHub

### Prototyping Principles Enforcement

- **No over-engineering**: Keep solutions simple and functional
- **No enterprise-grade requirements**: Avoid production-ready complexity
- **No testing/CI/CD**: Skip test scripts, unit tests, and CI/CD pipelines
- **Functional delivery focus**: Make it work first, refine later if needed

### Quality Requirements

- Tech-lead orchestrator MANDATORY for both Plan and Non-Plan modes
- MCP tools as PRIMARY method for all specialist operations
- Atomic commit principle: ALL changes in single commit operation
- GitHub MCP tools for repo management over traditional git commands

---