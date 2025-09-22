## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion!!!! 🔴

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
7. 🔴 REPEAT any tool as needed throughout the process
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

###

## New Task Details

Update docs/implementation_plans/direct_prompt_migration_implementation_plan.md Phase 3 & Testing Phase details

- Modify the test plan to have a distinct Testing & Validation Phase that will ONLY PERFORM THE TESTING AND VALIDATION.  ANY CODE, FILE, DOC, CONFIG type change DOES NOT BELONG IN Testing & Validation Phase.  ANY file changes means it belongs as part of the development\implementation Phase. In this case, that last Phase for Implementation is Phase 3, so Phase 3 needs to wrap up ALL file changes before procdeeding to Testing & Validation Phase.  See details below on how I want it updated:

- Here are all the tasks that can remain in Phase 3 since they are still development\implementation tasks.  Even though it is NOT code that is being changed, it still counts as implementation:

### **PHASE 3: INTEGRATION & TESTING**

#### **Task 3.1: Update Package Dependencies**

- [ ] **3.1.1** Remove unused frontend dependencies from `package.json`
- [ ] **3.1.2** Remove unused backend dependencies from `pyproject.toml`
- [ ] **3.1.3** Update dependency versions if needed

#### **Task 3.2: Update Configuration**

- [ ] **3.2.1** Update environment variables
- [ ] **3.2.2** Update configuration files
- [ ] **3.2.3** Update documentation

#### **Task 3.4: Documentation Updates**

- [ ] **3.4.1** Update README.md
- [ ] **3.4.2** Update API documentation
- [ ] **3.4.3** Update code comments
- [ ] **3.4.4** Update deployment documentation

- Here are all the previous Phase 3 tasks that MUST BE MIGRATED HAVE IT'S OWN distinct Testing & Validation Phase. You can see how none of these tasks have nothing to do with implementation and purely testing

#### **Task 3.3: Testing**

- [ ] **3.3.1** Test all API endpoints
- [ ] **3.3.2** Test frontend functionality
- [ ] **3.3.3** Test CLI functionality
- [ ] **3.3.4** Test error handling
- [ ] **3.3.5** Test performance improvements
