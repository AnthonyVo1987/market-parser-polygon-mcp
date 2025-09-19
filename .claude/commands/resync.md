# Resync Slash Command

Resync new Claude Code Chat instance with latest project state, docs, & memory files

**Prototyping Focus:** All tasks enforce prototyping principles - no over-engineering, no enterprise-grade solutions, no testing/CI/CD during prototype phase.

## How to Use

1. **Run this command**: `/resync`

## What This Command Does

When you invoke `/resync`, I will:

1. MANDATORY TOOL USAGE VERIFICATION: Confirm you understand and WILL use the MCP Tools PRIMARY approach for all tasks in this project.
2. Read the project documentation to acknowledge project state, last completed task(s), operating rules, & MCP Tools PRIMARY use FIRST & then Default Tools as
Secondary Fallback:
• ~/CLAUDE.md (if exists)
• ~/README.md (if exists)

3. VERBATIM RECITATION REQUIREMENT: You MUST recite the exact "MANDATORY Tools Usage Guidance for all Task(s)" section from CLAUDE.md word-for-word, then
explicitly confirm you WILL follow and use each tool category as specified

4. Acknowledge and provide:
• High level summary of current status of the project
• Last Completed Task Summary from CLAUDE.md
• Primary MCP Tools Usage & Secondary Fallback Tools Usage
• Playwright MCP Tools are the ONLY method to test

5. Confirm you are ready to assist with tasks using the established tool protocols and project constraints.

---

Expected Outcome:

• ~/CLAUDE.md: Read & AI Agent will follow it
• ~/README.md: Read & AI Agent will follow it
• High level summary of current status of the project
• Last Completed Task Summary from CLAUDE.md
• AI Agent will recite and WILL FOLLOW and USE tools verbatim

By forcing the AI Agent to verbatim recite and follow Tools usage from CLAUDE.md, we make sure the Agent actually reads and absorbs the entire Tools Usage
Guide section instead of just glossing over it.
The key addition is Step 3 which requires:

1. Verbatim recitation of the exact tool usage guidance
2. Explicit confirmation of WILL follow and use each tool
3. Absorption verification through word-for-word repetition

This ensures the AI Agent doesn't just acknowledge the tools but actually internalizes and commits to using them properly
---
