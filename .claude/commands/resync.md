# Resync Slash Command

Resync new AI Agent Chat instance with latest project state, docs, & memory files

**Prototyping Focus:** All tasks enforce prototyping principles - no over-engineering, no enterprise-grade solutions, no testing/CI/CD during prototype phase.

## How to Use

1. **Run this command**: `/resync`

## What This Command Does

When you invoke `/resync`, I will:

1. Read the project documentation to acknowledge project state, last completed task(s), operating rules, & MCP Tools PRIMARY use FIRST & then Default Tools as
Secondary Fallback:
• ~/CLAUDE.md (if exists)
• ~/README.md (if exists)

3. Acknowledge and provide:
• High level summary of current status of the project
• Last Completed Task Summary from CLAUDE.md
• Primary MCP Tools Usage & Secondary Fallback Tools Usage
• Playwright MCP Tools are the ONLY method to test

4. Confirm you are ready to assist with tasks using the established tool protocols and project constraints

---
