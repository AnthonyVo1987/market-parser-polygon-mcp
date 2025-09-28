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

3. Confirm: 🔴 CRITICAL: YOU MUST ALWAYS USE THESE TOOLS FIRST in any particular order to perform all task(s)

- **Serena Tools**: Use for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
- **Sequential-Thinking Tools**: Use for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
- **Context7 Tools**: Use for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups
- **Filesystem Tools**: Use for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
- **Standard Read/Write/Edit Tools**: Use for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
- **Playwright Tools**: Use for Testing with Browser automation for React GUI & App Validation

4. DO NOT PERFORM ANY NEW TASKS YET OR READ ANY OTHER FILES OR DOCS OTHER THAN CLAUDE.md for resync

---
