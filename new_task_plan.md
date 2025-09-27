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

## AI Agent Task: Phase 5 Testing & Validation for Shared Persistent Agent Implementation

You are tasked with performing **Phase 5: Testing & Validation** for the Shared Persistent Agent Implementation. This involves comprehensive testing of the shared persistent agent architecture across functionality, performance, and integration testing.

**CRITICAL REQUIREMENTS:**

- Complete ALL Phase 5 tasks as specified in the implementation plan
- Use the 3 test prompts as an ADDITIONAL validation layer
- Generate comprehensive test reports for each task
- Use ALL mandatory tools throughout the process

## **Task 5.1: Functionality Testing**

**5.1.1** Test CLI session persistence
**5.1.2** Test GUI session management  
**5.1.3** Test agent caching functionality
**5.1.4** Test conversation memory across messages

**Test Scenarios:**

- CLI Session Persistence: Start CLI session, send "Current Market Status", then "What about NVDA?", verify message 2 references message 1 context
- GUI Session Management: Start GUI session, send multiple messages, verify conversation memory works
- Agent Caching: Send multiple similar requests, verify agent creation time decreases, verify cache hit rate increases

## **Task 5.2: Performance Testing**

**5.2.1** Measure response time improvements (target: 4-20s faster per session)
**5.2.2** Test memory usage with caching
**5.2.3** Test performance under load
**5.2.4** Validate conversation memory functionality

**Performance Test with 7 Prompts:**

```text
"Current Market Status"
"Single Stock Snapshot NVDA" 
"Full Market Snapshot: SPY, QQQ, IWM"
"GME closing price today"
"SOUN performance this week"
"NVDA Support & Resistance Levels"
"SPY Technical Analysis"
```

## **Task 5.3: Integration Testing**

**5.3.1** Test dead code removal doesn't break functionality
**5.3.2** Test session persistence integration
**5.3.3** Test agent caching integration
**5.3.4** Test MCP server optimization

## **ADDITIONAL VALIDATION: 3 Test Prompts in Same Session**

**CRITICAL:** As an additional validation layer, test these 3 prompts in the SAME CLI session sequentially with 120s timeout per prompt:

1. **Test Prompt 1:** `Current Market Status`
2. **Test Prompt 2:** `Single Stock Snapshot NVDA`  
3. **Test Prompt 3:** `Full Market Snapshot: SPY, QQQ, IWM`

**Expected Performance Improvements:**

- First prompt: ~30-60s (agent creation + MCP server setup)
- Second prompt: ~20-40s (cached agent reuse)
- Third prompt: ~20-40s (cached agent reuse)
- **Target:** 4-20s faster per session (10-40% improvement)

**DELIVERABLES:**

1. Functionality test results for all 5.1 tasks
2. Performance test results with timing data for all 5.2 tasks
3. Integration test results for all 5.3 tasks
4. Additional validation report for the 3 test prompts
5. Comprehensive .md test report summarizing all results

**MANDATORY TOOL USAGE:**
Use ALL available tools throughout the testing process:

- Sequential-Thinking for test planning and analysis
- Terminal commands for CLI/GUI execution
- File operations for report generation
- Serena tools for code analysis and validation
- Context7 for research if issues arise
- Performance monitoring tools for metrics collection

Execute Phase 5 testing systematically and provide comprehensive validation results for the shared persistent agent implementation.
