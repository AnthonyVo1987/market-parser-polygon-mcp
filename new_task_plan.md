Here's the comprehensive prompt for an AI Agent to perform the requested task:

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s)

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis
2. Use Context7 for research and best practices
3. Use Serena Tools for code analysis and manipulation
4. Use Filesystem Tools for batch operations and project management
5. Use Standard Read/Write/Edit for file modifications
6. Use Playwright Tools for testing and validation
7. REPEAT any tool as needed throughout the process
8. NEVER stop using tools - continue using them until task completion

SPECIFIC TOOL USAGE GUIDELINES:

**Serena Tools**: USE AS OFTEN AS NEEDED for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications

**Sequential-Thinking Tools**: USE AS OFTEN AS NEEDED for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)

**Context7 Tools**: USE AS OFTEN AS NEEDED for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups

**Filesystem Tools**: USE AS OFTEN AS NEEDED for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications

**Standard Read/Write/Edit Tools**: USE AS OFTEN AS NEEDED for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management

**Playwright Tools**: USE AS OFTEN AS NEEDED for Testing with Browser automation for React GUI & App Validation

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

---

## **TASK: Comprehensive UI Performance Optimization Implementation Audit & Verification**

### **Primary Objective**

Perform a comprehensive code review and audit to verify that the entire PRE-IMPLEMENTATION TASKS & PHASE 1: REMOVE ALL HIGH IMPACT EFFECTS has been completely implemented from `docs/implementation_plans/UI_Performance_Optimization_Implementation_Plan.md` STEP BY STEP.

### **Context**

- We previously implemented all UI Performance Optimizations up to Phase 3 on a different development environment/PC
- Current environment was NOT used for implementation, so development tools may not be fully configured
- Need to verify environment parity and ensure all tasks are properly completed
- This is a SANITY CHECK to ensure the new dev environment is truly configured correctly

### **Task Requirements**

#### **1. Environment Setup Verification**

- Review `CLAUDE.md`, `START_SCRIPT_README.md`, & `start-app.sh` for proper script and commands
- Verify dev servers can start properly using the correct commands
- Use Playwright tools to navigate to the app page for testing if needed
- Ensure all development tools are properly installed and configured

#### **2. Comprehensive Implementation Audit**

- Systematically review `docs/implementation_plans/UI_Performance_Optimization_Implementation_Plan.md`
- Go through PRE-IMPLEMENTATION TASKS step by step
- Go through PHASE 1: REMOVE ALL HIGH IMPACT EFFECTS step by step
- Mark each completed task with ✅ green checkmarks

#### **3. Task Execution Strategy**

**For NON-CODING Tasks:**

- PERFORM the task to ensure dev environment can replicate it
- Example: If task is to capture baseline performance data, then perform it
- Verify the environment can execute the required commands/measurements

**For CODING Tasks:**

- DO NOT RE-IMPLEMENT the code
- Only review & audit the code to verify completion
- Check that the implementation matches the requirements
- Verify code quality and correctness

#### **4. Verification Process**

- Use Sequential-Thinking to plan the audit approach
- Use Serena Tools for comprehensive code analysis
- Use Filesystem Tools for batch file operations and project management
- Use Context7 Tools for best practices research
- Use Playwright Tools for browser-based testing and validation
- Use Standard Read/Write/Edit for single-file modifications

#### **5. Success Criteria**

- All PRE-IMPLEMENTATION TASKS verified as completed ✅
- All PHASE 1 tasks verified as completed ✅
- Development environment fully functional and tested
- All performance measurement tools operational
- Baseline data captured and documented
- Environment parity confirmed with previous implementation

#### **6. Deliverables**

- Comprehensive audit report with ✅ checkmarks for each completed task
- Verification that all non-coding tasks can be executed in current environment
- Confirmation that all coding tasks are properly implemented
- Documentation of any missing or incomplete implementations
- Final confirmation that environment is ready for Post-Implementation Tasks

### **Critical Notes**

- This is an AUDIT and VERIFICATION task, not a re-implementation task
- Focus on ensuring the current environment can replicate all functionality
- Verify that all performance measurement capabilities are working
- Confirm that the development setup matches the previous implementation
- Only implement missing non-coding tasks (like running performance tests)
- Do NOT re-implement existing code - only verify it exists and is correct

**Remember: Use ALL available tools continuously throughout the entire process. This is a comprehensive audit that requires thorough investigation, analysis, and verification using every tool in your toolkit.**
