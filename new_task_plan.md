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

---

**PROMPT FOR AI AGENT:**

```
Use ALL your Mandatory Toolkit Tools to systematically implement Phase 0: Dead Code Cleanup from docs/implementation_plans/shared_persistent_agent_implementation_plan.md.

CRITICAL REQUIREMENTS:
- Read the implementation plan document first to understand the exact requirements
- Follow the Phase 0 tasks in exact order (0.1.1 through 0.1.6)
- Use comprehensive verification tools to ensure no code is removed that's actually being used
- Test after each removal to ensure functionality remains intact

PHASE 0 TASKS TO IMPLEMENT:
1. Remove `guardrail_agent` (line 617) - never used
2. Remove `finance_analysis_agent` (line 631) - never used  
3. Remove `finance_guardrail()` function (lines 639-646) - exported but never called
4. Remove entire `optimized_agent_instructions.py` file - never used
5. Remove unused imports and dependencies
6. Update `src/backend/__init__.py` to remove `finance_guardrail` import/export
7. Verify no broken references after cleanup

VALIDATION REQUIREMENTS:
- Run linting to ensure no broken imports
- Run tests to verify functionality remains intact
- Check for any remaining references to removed code
- Verify no circular import dependencies
- Confirm all test cases pass
- Check for any runtime errors in both CLI and GUI
- Validate that removed code doesn't affect existing functionality

MANDATORY TOOL USAGE:
- Use sequential thinking for task analysis and planning
- Use code analysis tools to verify each removal is safe
- Use search tools to find all references before removing
- Use testing tools to validate after each change
- Use git tools to track changes
- Continue using tools throughout the entire process

SUCCESS CRITERIA:
- All dead code removed without breaking functionality
- No broken imports or references
- All tests pass
- Clean, maintainable codebase ready for Phase 5 & 6
- Single atomic commit with all changes

Execute this implementation systematically and verify each step before proceeding to the next.
```

---

This prompt provides clear instructions for implementing Phase 0 with comprehensive verification and testing requirements.
