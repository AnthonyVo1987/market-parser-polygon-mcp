# Resync Slash Command

Resync new Claude Code Chat instance with latest project state, docs, & memory files

**Prototyping Focus:** All tasks enforce prototyping principles - no over-engineering, no enterprise-grade solutions, no testing/CI/CD during prototype phase.

## How to Use

1. **Run this command**: `/resync`

## What This Command Does

When you invoke `/resync`, I will:

1. Read the follow project docs ONE AT A TIME and acknowledge project state, last completed task(s), operating rules, & MCP Tool PRIMARY use FIRST, to provide context and background for future task(s)

- CLAUDE.md
- LAST_TASK_SUMMARY.md
- MCP_TOOL_USAGE_GUIDE.md

2. Acknowledge and provide high level summary of current understanding of the project

---
