# Resync Slash Command

Resync new AI Agent Chat instance with latest project state, docs, & memory files

**Prototyping Focus:** All tasks enforce prototyping principles - no over-engineering, no enterprise-grade solutions, no testing/CI/CD during prototype phase.

## How to Use

1. **Run this command**: `/resync`

## What This Command Does

When you invoke `/resync`, I will:

1. Carefuly read and ingest ONLY 'CLAUDE.md' to understand Project Development Rules & Operating Procedures.

2. After ingesting CLAUDE.md, Acknowledge and provide:
• High level summary of current status of the project
• High level summary of Last Completed Task Summary from CLAUDE.md

3. Get Serena Initial Instructions to understand optimal Serena Tools usage:
   - **Primary Method (Preferred)**: Use `mcp__serena__initial_instructions` tool
   - **Fallback Method**: If tool fails, use `mcp__serena__read_memory` with memory name: `serena_initial_instructions`

4. DO NOT PERFORM ANY NEW TASKS YET OR READ ANY OTHER FILES OR DOCS OTHER THAN CLAUDE.md for resync

---
