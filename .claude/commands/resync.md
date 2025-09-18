# Resync Slash Command

Resync new Claude Code Chat instance with latest project state, docs, & memory files

**Prototyping Focus:** All tasks enforce prototyping principles - no over-engineering, no enterprise-grade solutions, no testing/CI/CD during prototype phase.

## How to Use

1. **Run this command**: `/resync`

## What This Command Does

When you invoke `/resync`, I will:

1. Read the follow project docs ONE AT A TIME and acknowledge project state, last completed task(s), operating rules, & MCP Tools PRIMARY use FIRST & then Default Tools as Secondary Fallback, to provide context and background for future task(s):

- ~/CLAUDE.md
- ~/README.md

2. Acknowledge and provide :

- High level summary of current status of the project
- Last Completed Task Summary from CLAUDE.md
- Primary MCP Tools Usage & Secondary Fallback Tools Usage
- Playwright MCP Tools are the ONLY method to test - see `/tests/playwright/mcp_test_script_basic.md`

---
