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
4. **MUST USE Context7, Sequential-Thinking, Filesystem Tools as Primary Tools compliance** for all specialists
5. **Create actual deliverables** (not just summaries)

## Command Execution

I'll read the task details from new_task_details.md and use @agent-tech-lead-orchestrator to analyze the requirements and assign the appropriate specialists from the available AI Team:

## Available Specialists (per CLAUDE.md)

| **Task Category** | **Agent** | **Specific Responsibilities** |
|-------------------|-----------|------------------------------|
| **Agent System Development** | `backend-developer` | FastAPI + Pydantic AI + OpenAI Agents SDK, guardrail system, prompt templates |
| **Financial Query Processing** | `backend-developer` | MCP integration, Polygon.io data handling, agent orchestration |
| **React Components & UI** | `react-component-architect` | Modern React 18.2+ patterns, hooks, PWA features, financial dashboards |
| **API Design & Integration** | `api-architect` | REST endpoints, Polygon.io MCP server design, data contracts |
| **Performance & Optimization** | `performance-optimizer` | Real-time financial data processing, agent efficiency, response times |
| **Code Quality & Security** | `code-reviewer` | Security-aware reviews, financial data handling, maintainability |

## Primary Tool Requirements

Context7, Sequential-Thinking, Filesystem are PRIMARY tools for ALL specialists. All specialists MUST use:

- `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` for research
- `mcp__filesystem__*` tools for all file operations

---

## Execution Protocol

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

- `@agent-tech-lead-orchestrator` generates comprehensive plan WITH Specialist Assignments AND ENFORCE usage of Context7, Sequential-Thinking, Filesystem Tools for EACH Specialist
- Detailed task breakdown with specialist role allocations and dependencies

**D. Non-Plan Mode: Tech-Lead Orchestrated Planning**

- `@agent-tech-lead-orchestrator` generates streamlined plan WITH Specialist Assignments
- Focused task execution plan with efficient specialist coordination

**E. Specialist(s) Execute Plan**

- Specialists MUST USE Context7, Sequential-Thinking, Filesystem Tools as Primary Tools to execute plan from `@agent-tech-lead-orchestrator` using exact assignments
- ALL specialists MUST USE Context7, Sequential-Thinking, Filesystem Tools as Primary Tools
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

**MANDATORY PRE-COMMIT CHECKLIST (CRITICAL FOR SUCCESS):**
1. Run `git status` to identify ALL modified files
2. Run `git add .` to stage ALL changes (never commit without staging all)
3. Run `git status` again to verify ALL files are staged
4. Verify specialist work inclusion: ALL frontend, backend, test, and config changes MUST be staged
5. Only then execute `git commit` with comprehensive message

**AGENT PROCESS REQUIREMENTS:**
- Code reviewer MUST verify all specialist work is staged before commit
- NEVER commit without comprehensive staging verification
- Implement explicit git status checks at each phase
- Failure to include all modified files is a CRITICAL VIOLATION

- PRIMARY: Use `git` for atomic operations
- Single atomic commit containing ALL changes:
  - Code/file changes (ALL specialist deliverables)
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
- Context7, Sequential-Thinking, & Filesystem Tools as PRIMARY method for all specialist operations
- Atomic commit principle: ALL changes in single commit operation

---
