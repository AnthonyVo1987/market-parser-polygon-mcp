# New Task Slash Command

Execute complex development tasks using AI Team orchestration with the tech-lead-orchestrator.

## How to Use

1. **Edit task details** in `/home/anthony/Github/market-parser-polygon-mcp/new_task_details.md`
2. **Run this command**: `/new_task`
3. **Follow the orchestrated plan** as specialists complete each task

## What This Command Does

When you invoke `/new_task`, I will:

1. **Read your task details** from `new_task_details.md`
2. **Invoke @tech-lead-orchestrator** to analyze the task and create a specialist assignment plan
3. **Execute the plan** using the exact agents recommended by the tech-lead
4. **Ensure MCP tool compliance** for all specialists
5. **Create actual deliverables** (not just summaries)

## Command Execution

I'll read the task details from new_task_details.md and use @tech-lead-orchestrator to analyze the requirements and assign the appropriate specialists from the available AI Team:

**Available Specialists (per CLAUDE.md):**
- @code-reviewer - MANDATORY for all features, PRs, merges
- @performance-optimizer - Cost reduction, speed improvement  
- @backend-developer - Python/Pydantic AI development
- @frontend-developer - Gradio interface development
- @api-architect - MCP server optimization
- @documentation-specialist - Architecture docs, user guides
- @code-archaeologist - Complex architectural decisions

**MCP Tool Requirements:**
All specialists MUST use:
- `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` for research
- `mcp__filesystem__*` tools for all file operations

---

## Execution Protocol

I'll read the task from new_task_details.md, then use @tech-lead-orchestrator to get proper agent assignments and execute the plan with those exact specialists, ensuring all MCP tools are used and actual deliverables are created.