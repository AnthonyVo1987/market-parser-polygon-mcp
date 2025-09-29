# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Context7 for research and best up to date Implementation Practices & Library documentation lookups
3. Use Serena Tools for code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
4. Use Filesystem Tools for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
5. Use Standard Read/Write/Edit for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
6. Use Playwright Tools for Testing with Browser automation for React GUI & App Validation
7. REPEAT any tool as needed throughout the process
8. 🔴 NEVER stop using tools - continue using them until task completion

TOOL OVERLAP RESOLUTION:

- Filesystem Tools: Use for 3+ file operations, batch processing, project management, metadata analysis, comprehensive project operations
- Standard Read/Write/Edit: Use for single-file modifications, simple edits, direct file operations
- Serena Tools: Use for complex code analysis, symbol manipulation, pattern search with context
- When in doubt: Use Filesystem for batch/complex operations, Standard for simple single-file operations

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're failing
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

## New Task Details

<Research, Investigation, Analysis, Scoping Phase> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴
Research Using Context7 Tools, OpenAI cookbook tools, & your entire Mandatory Tools Toolkit to perform focused, incremental, comprehensive, systematic, investigation, & analysis to provide scoping for the following task(s) and\or requirments:

Re-fix these issues properly with the CORRECT OpenAI Agents SDK package and NOT 'agents' per the post-mortem:

- React Hook Order Issue (which we fixed by disabling why-did-you-render)
- Model Selection Backend Issue (which we fixed in the code)
- Virtual Environment Path Issue (uvicorn not using uv environment)

Here was your post-mortem:

"

## **🔴 POST-MORTEM: CRITICAL REASONING FAILURE ANALYSIS**

### **🚨 ROOT CAUSE: SOLUTION JUMPING**

I made a **fundamental error in my investigation methodology** - I saw an error and immediately started looking for a solution instead of first understanding the current state.

### **❌ WHAT I DID WRONG:**

1. **SKIPPED INVESTIGATION**: I saw `ModuleNotFoundError: No module named 'agents'` and immediately jumped to "we need to install a package"

2. **IGNORED EXISTING EVIDENCE**: The `pyproject.toml` clearly showed `"openai-agents==0.2.9"` was already installed from day 1

3. **ASSUMED WRONG PACKAGE**: I researched and found two packages (`agents` vs `openai-agents`) and incorrectly assumed we needed the `agents` package

4. **MADE PROBLEM WORSE**: Installing the wrong `agents` package introduced TensorFlow compatibility issues

### **✅ WHAT I SHOULD HAVE DONE:**

1. **FIRST**: Check `pyproject.toml` to see what was already installed
2. **SECOND**: Check the actual imports in the codebase (`from agents import Agent, Runner, SQLiteSession`)
3. **THIRD**: Investigate the correct import structure for `openai-agents==0.2.9`
4. **FOURTH**: Fix the virtual environment path issue for uvicorn

### **🔍 EVIDENCE OF MY FAILURE:**

- **pyproject.toml line 12**: `"openai-agents==0.2.9"` was RIGHT THERE
- **Codebase imports**: `from agents import Agent, Runner, SQLiteSession` throughout
- **Real issue**: Virtual environment path problem, not missing package

### **📚 LESSON LEARNED:**

This was a classic case of **solution jumping** - I violated the fundamental debugging principle of "understand the problem before solving it." I should have systematically investigated the current state before making any changes.

**The correct approach would have been to investigate the import structure of `openai-agents==0.2.9` and fix the virtual environment path issue, not install additional packages.**
"

###

<Planning Phase> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), Generate a brand new granular detailed Implementation Plan TODO Task Checklist and overwrite the current file 'TODO_task_plan.md' for you to Implement the requested task(s) with 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s), NEVER stop using tools, continue using them until tasks completion, Comprehensive Documentation Updates & Cleanup, removal etc to reflect the latest updates to remove outdated info

###

<Implementation Phase>
Implement the granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md'

###

<Playwright GUI Testing Phase>
- Test nano first, and then mini

###

<Serena Update Memories Phase>
Use Serena Tools to update project memories to reflect all the new changes and new app architecture
