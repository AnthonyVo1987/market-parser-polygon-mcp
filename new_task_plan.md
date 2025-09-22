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

###

## Task Details

## 🚀 COMPREHENSIVE UI TEST EXECUTION PROMPT

**CRITICAL: MANDATORY TOOL USAGE to perform all task(s)**

You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

**TOOL USAGE REQUIREMENTS:**

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

**MANDATORY TOOL USAGE PATTERNS:**

1. START with Sequential-Thinking for task analysis
2. Use Context7 for research and best practices
3. Use Serena Tools for code analysis and manipulation
4. Use Filesystem Tools for batch operations and project management
5. Use Standard Read/Write/Edit for file modifications
6. Use Playwright Tools for testing and validation
7. REPEAT any tool as needed throughout the process
8. NEVER stop using tools - continue using them until task completion

**SPECIFIC TOOL USAGE GUIDELINES:**

**Sequential-Thinking Tools**: USE AS OFTEN AS NEEDED for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)

**Playwright Tools**: USE AS OFTEN AS NEEDED for Testing with Browser automation for React GUI & App Validation

**Filesystem Tools**: USE AS OFTEN AS NEEDED for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management

**Standard Read/Write/Edit Tools**: USE AS OFTEN AS NEEDED for single-file content modifications, simple edits, and direct file operations

**Serena Tools**: USE AS OFTEN AS NEEDED for Advanced code analysis, symbol manipulation, pattern search with context, and memory management

**Context7 Tools**: USE AS OFTEN AS NEEDED for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups

---

## **TASK EXECUTION REQUIREMENTS**

### **Phase 1: Test Plan Execution (Steps 1-11)**

Execute the EXACT test plan from `docs/implementation_plans/UI_Enhanced_Playwright_Test_Plan_2025.md` with NO DEVIATIONS:

1. **Kill All Existing Servers** - `pkill -f "uvicorn\|vite\|npm"`
2. **Start Fresh Servers** - `./start-app.sh`
3. **Wait for Servers** - `sleep 15`
4. **Verify Servers** - `curl -s http://127.0.0.1:8000/health && curl -s http://127.0.0.1:3000 | head -3`
5. **Navigate to Frontend** - `mcp_playwright-backup_playwright_navigate` with `{"url": "http://127.0.0.1:3000"}`
6. **Verify Enhanced UI Layout** - `mcp_playwright-backup_playwright_get_visible_text`
7. **Test Mobile Sidebar Toggle** - `mcp_playwright-backup_playwright_click` with `{"selector": "[data-testid='mobile-sidebar-toggle']"}`
8. **Verify Performance Indicator** - `mcp_playwright-backup_playwright_get_visible_text`
9. **Test Analysis Buttons Container** - `mcp_playwright-backup_playwright_get_visible_text`
10. **Verify Enhanced Input Field** - `mcp_playwright-backup_playwright_get_visible_text`
11. **Check Bottom Control Panel** - `mcp_playwright-backup_playwright_get_visible_text`

### **Phase 2: Enhanced UI Test 1 - Modern Layout Validation (Steps 12-21)**

Execute ALL test steps with proper 30-second polling intervals:

- Fill Enhanced Input Field with test query
- Press Enter to submit
- Wait 30 seconds for response
- Verify response contains "KEY TAKEAWAYS" section
- Test all UI elements systematically
- Document results for each step

### **Phase 3: Mobile UI Test (Steps 22-31)**

Execute ALL mobile-specific test steps:

- Test mobile sidebar functionality
- Verify responsive design elements
- Test touch interactions
- Document mobile-specific results

### **Phase 4: Analysis Functionality Test (Steps 32-41)**

Execute ALL analysis button tests:

- Test Stock Snapshot functionality
- Test Support/Resistance analysis
- Test Technical Analysis features
- Document analysis results

### **Phase 5: Performance Metrics Test (Steps 42-51)**

Execute ALL performance-related tests:

- Verify performance indicator display
- Test response time tracking
- Test message count display
- Test real-time status updates
- Document performance results

### **Phase 6: Export Functionality Test (Steps 52-61)**

Execute ALL export-related tests:

- Test export button functionality
- Test recent message buttons
- Test debug panel information
- Document export results

---

## **TEST REPORT GENERATION REQUIREMENTS**

### **After ALL Tests Complete:**

1. **Generate Comprehensive Test Report** with:
   - Status of EACH test case (PASS/FAIL)
   - Detailed results for each test step
   - Screenshots of any failures
   - Performance metrics captured
   - Error messages and debugging information
   - Complete coverage analysis

2. **Create Test Report File** as `test-reports/UI_Enhanced_Test_Report_$(date +%Y-%m-%d_%H-%M).md`

3. **Include in Report**:
   - Test execution summary
   - Individual test case results
   - Performance data
   - Error analysis
   - Recommendations for fixes

---

## **FINAL TASKS REQUIREMENTS**

### **Summary Task:**

- Create token & context efficient git commit message
- Update CLAUDE.md "Last Completed Task Summary" section with VERBATIM COPY of commit message between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers

### **Atomic Git Commit & Push Task:**

**MANDATORY PRE-COMMIT CHECKLIST:**

1. Run `git status` to identify ALL modified files
2. Run `git add .` to stage ALL changes
3. Run `git status` again to verify ALL files are staged
4. Verify ALL frontend, backend, test, and config changes are staged
5. Execute `git commit` with comprehensive message
6. Execute `git push` to complete workflow

**Commit Requirements:**

- Single atomic commit containing ALL changes
- Include CLAUDE.md, test report, documentation changes
- NO testing artifacts, screenshots, or videos
- NO lingering uncommitted files

### **Final Verification Task:**

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date
- Confirm all changes are properly committed and pushed

---

## **CRITICAL SUCCESS CRITERIA**

- **100% Test Coverage**: ALL test cases must be executed
- **No Deviations**: Follow test plan exactly as written
- **Complete Documentation**: Detailed report for each test case
- **No Fixes**: Report issues but do not attempt to fix them
- **Clean Git History**: Single atomic commit with all changes
- **Comprehensive Reporting**: Full test results with status and details

**REMEMBER**: Use tools continuously throughout the entire process. This is a comprehensive testing and reporting workflow that requires extensive tool usage from start to finish.

**Execute this prompt to perform the complete UI test execution, generate detailed test reports, and complete all final tasks with proper git commit and push.**
