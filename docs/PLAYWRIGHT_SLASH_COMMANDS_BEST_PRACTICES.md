# Playwright Slash Commands Best Practices Guide

**Comprehensive Best Practices from Context7 Research and Implementation Experience**

---

## Overview

This guide compiles best practices from comprehensive research including Claude Code documentation, Playwright automation standards, and established testing methodologies. These recommendations ensure robust, maintainable, and reliable implementation of `/test_cli_full` and `/test_mcp_full` commands.

---

## 1. Command Design Best Practices

### Single Responsibility Principle

**✅ DO:**
```markdown
# Each command has one clear purpose
/test_cli_full    # Execute complete B001-B016 tests via CLI
/test_mcp_full    # Execute complete B001-B016 tests via MCP
```

**❌ DON'T:**
```markdown
# Avoid multi-purpose commands
/test_all_methods # Ambiguous - could mean CLI, MCP, or both
```

### Self-Documenting Commands

**✅ DO:**
```yaml
---
description: Execute complete B001-B016 Playwright CLI test suite with performance analysis
argument-hint: [test-filter-pattern]
---
```

**❌ DON'T:**
```yaml
---
description: Run tests
---
```

### Consistent Naming Conventions

**✅ DO:**
- Use hyphenated names: `test-cli-full.md`
- Descriptive and specific: `test-mcp-full.md`
- Follow project conventions

**❌ DON'T:**
- Abbreviations: `test-c-f.md`
- Spaces: `test cli full.md`
- Inconsistent patterns

---

## 2. YAML Frontmatter Best Practices

### Minimal Tool Permissions

**✅ DO - CLI Method:**
```yaml
---
allowed-tools: Bash(cd:*), Bash(npx:*), Bash(curl:*), TodoWrite, Write
description: Execute complete B001-B016 Playwright CLI test suite
argument-hint: [test-filter-pattern]
---
```

**✅ DO - MCP Method:**
```yaml
---
allowed-tools: mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_type, mcp__playwright__browser_click, mcp__playwright__browser_wait_for, mcp__playwright__browser_evaluate, TodoWrite, Write
description: Execute complete B001-B016 Playwright MCP browser automation suite
argument-hint: [test-filter-pattern]
---
```

**❌ DON'T:**
```yaml
---
allowed-tools: Bash(*), Write(*), Read(*)  # Too permissive
---
```

### Descriptive Argument Hints

**✅ DO:**
```yaml
argument-hint: [test-filter-pattern]
# or
argument-hint: [B001-B003 | priority-tests | all]
```

**❌ DON'T:**
```yaml
argument-hint: [args]  # Not descriptive
```

---

## 3. Environment Validation Best Practices

### Comprehensive Pre-flight Checks

**✅ DO:**
```markdown
## Environment Status Check
- Backend Status: !`curl -f http://localhost:8000/health || echo "❌ Backend not ready"`
- Frontend Status: !`curl -f http://localhost:3000/ || curl -f http://localhost:3001/ || curl -f http://localhost:3002/ || echo "❌ Frontend not ready"`
- Test Files Count: !`cd /path/to/tests && ls test-b*.spec.ts | wc -l`
- Playwright Installation: !`npx playwright --version || echo "❌ Playwright not installed"`
```

**❌ DON'T:**
```markdown
## Quick Check
- Backend: !`curl localhost:8000`  # No error handling
```

### Progressive Validation Strategy

**✅ DO:**
1. **Infrastructure Health**: Server status checks
2. **Environment Setup**: Test files and dependencies
3. **Tool Availability**: Required tools and permissions
4. **Session Readiness**: Browser and session preparation

**❌ DON'T:**
- Skip validation steps
- Assume infrastructure is ready
- Proceed without confirming prerequisites

---

## 4. Test Execution Best Practices

### CLI Method Best Practices

**✅ DO:**
```bash
# Enhanced CLI pattern with required configuration
npx playwright test --timeout=120000 --workers=1 test-b001-market-status.spec.ts
```

**Key Points:**
- Always use `--timeout=120000` (120-second universal timeout)
- Always use `--workers=1` (single browser session requirement)
- Include descriptive error messages for failures
- Capture and report actual execution times

**❌ DON'T:**
```bash
npx playwright test  # Missing required configuration
npx playwright test --workers=4  # Breaks single session requirement
```

### MCP Method Best Practices

**✅ DO:**
```json
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "Expected Response Pattern",
    "time": 10
  }
}
```

**Key Points:**
- Always use 10-second polling intervals (configuration requirement)
- Maintain single browser session throughout all tests
- Use descriptive element selectors
- Implement proper error recovery

**❌ DON'T:**
```json
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "time": 30  # Wrong interval - should be 10
  }
}
```

---

## 5. Progress Tracking Best Practices

### TodoWrite Integration Patterns

**✅ DO:**
```javascript
// Create comprehensive todo list
const todoList = [
  {
    "content": "Execute B001: Market Status Check",
    "status": "pending",
    "activeForm": "Executing B001: Market Status Check"
  },
  // ... Continue for all B001-B016 tests
];

// Update progress systematically
await markInProgress("B001");
await executeTest("B001");
await markCompleted("B001");
```

**❌ DON'T:**
```javascript
// Skip progress tracking
executeAllTests();  // No tracking

// Batch update without individual tracking
markAllCompleted();  // Violates integrity protocols
```

### Testing Integrity Protocol

**✅ DO:**
1. **Create todo list BEFORE starting tests**
2. **Mark in_progress BEFORE executing each test**
3. **Mark completed ONLY after successful execution**
4. **Never claim completion without actual execution**

**❌ DON'T:**
1. Generate completion reports before finishing tests
2. Mark tests complete without execution
3. Ignore todo list status when reporting

---

## 6. Performance Measurement Best Practices

### Accurate Timing Collection

**✅ DO:**
```javascript
const startTime = Date.now();
await executeTest(testId);
const duration = (Date.now() - startTime) / 1000;
const classification = classifyPerformance(duration);

recordResult({
  testId,
  duration,
  classification,
  actualTiming: true
});
```

**❌ DON'T:**
```javascript
// Estimate or fabricate timing data
const estimatedDuration = 45; // Don't estimate
recordResult({ duration: estimatedDuration });
```

### Performance Classification Standards

**✅ DO:**
```javascript
function classifyPerformance(duration) {
  if (duration <= 30) return "😊"; // Good
  if (duration <= 60) return "😐"; // OK  
  if (duration <= 119) return "😴"; // Slow
  return "❌"; // Timeout (≥120s)
}
```

**Key Points:**
- Use exact thresholds (30s, 60s, 119s)
- Account for method-specific expectations
- CLI: More 😊😐 expected
- MCP: More 😐😴 expected (normal)

---

## 7. Error Handling Best Practices

### Graceful Degradation

**✅ DO:**
```javascript
try {
  await executeTest(testId);
  markCompleted(testId);
} catch (error) {
  if (error.type === 'TIMEOUT') {
    recordTimeout(testId);
    continueWithNextTest();
  } else if (error.type === 'INFRASTRUCTURE') {
    attemptRecovery();
    retryTest(testId);
  } else {
    recordError(testId, error);
    proceedWithRemainingTests();
  }
}
```

**❌ DON'T:**
```javascript
try {
  await executeTest(testId);
} catch (error) {
  throw error; // Terminates entire test suite
}
```

### Error Classification and Recovery

**✅ DO:**
1. **Infrastructure Errors**: Attempt recovery, retry
2. **Test Execution Errors**: Skip test, continue suite
3. **Timeout Errors**: Record as timeout, continue
4. **Session Errors**: Restart session if needed

**❌ DON'T:**
- Let single test failure stop entire suite
- Ignore error context for recovery decisions
- Fail to document error conditions in reports

---

## 8. Report Generation Best Practices

### Standardized Report Structure

**✅ DO:**
```markdown
# [Method] Playwright Test Execution Report B001-B016

**Report Date:** [Date]
**Test Coverage:** [16/16 Tests Completed]
**Method:** [CLI/MCP Automation]
**Overall Success Rate:** [X]%

## Executive Summary
- Clear summary of results and key findings
- Performance distribution analysis
- Infrastructure status summary

## Detailed Test Results
[Individual test results with timing and validation]

## Performance Analysis
[Actual performance metrics and analysis]

## Infrastructure Assessment
[System component status and stability]

## Quality Metrics
[Completion rates, error analysis, recommendations]
```

**❌ DON'T:**
```markdown
# Test Report
Tests run. All passed.
```

### Performance Data Presentation

**✅ DO:**
```markdown
#### B001: Market Status Check ✅ PASS 😊 (28s)
- **Result:** PASS - Response received within 120s timeout
- **Performance:** Good 😊 (28 seconds - optimal performance)
- **Validation:** Market data retrieval functionality confirmed
- **Response Format:** Proper emoji-enhanced financial analysis received
- **Method Notes:** CLI method inherently faster than MCP (expected)
```

**❌ DON'T:**
```markdown
B001: PASS (fast)
```

---

## 9. Security and Permissions Best Practices

### Principle of Least Privilege

**✅ DO:**
- Request only necessary tool permissions
- Use specific permission patterns: `Bash(npx:*)` not `Bash(*)`
- Document why each permission is needed
- Regular review and cleanup of permissions

**❌ DON'T:**
- Request broad permissions "just in case"
- Use wildcard permissions unnecessarily
- Skip permission documentation

### Data Protection

**✅ DO:**
```javascript
// Sanitize sensitive data in reports
function sanitizeErrorMessage(error) {
  return error.message
    .replace(/api_key=[^&\s]+/g, 'api_key=***')
    .replace(/password=[^&\s]+/g, 'password=***');
}
```

**❌ DON'T:**
- Include API keys or credentials in reports
- Log sensitive user data
- Expose internal system details unnecessarily

---

## 10. Integration Best Practices

### Claude Code Integration

**✅ DO:**
- Follow established Claude Code patterns
- Use standard frontmatter configuration
- Implement proper argument handling with `$ARGUMENTS`
- Include dynamic environment validation with `!` prefix

**❌ DON'T:**
- Deviate from established patterns without justification
- Skip argument validation
- Hard-code environment assumptions

### Tool Integration Patterns

**✅ DO:**
```javascript
// Abstract tool usage for maintainability
class ToolManager {
  async executeBashCommand(cmd, description) {
    return await this.invokeTool('Bash', {
      command: cmd,
      description: description
    });
  }
  
  async updateTodoList(updates) {
    return await this.invokeTool('TodoWrite', {
      todos: updates
    });
  }
}
```

**❌ DON'T:**
- Directly call tools without abstraction
- Skip error handling for tool calls
- Ignore tool-specific best practices

---

## 11. Maintenance and Evolution Best Practices

### Documentation Standards

**✅ DO:**
- Keep documentation current with implementation
- Include examples and troubleshooting guides
- Document known limitations and workarounds
- Provide clear upgrade/migration paths

**❌ DON'T:**
- Leave documentation outdated
- Skip inline comments for complex logic
- Assume implementation is self-explanatory

### Version Management

**✅ DO:**
```markdown
## Version History
- v1.0: Initial CLI and MCP command implementation
- v1.1: Enhanced error handling and recovery
- v1.2: Improved performance measurement accuracy
```

**❌ DON'T:**
- Change behavior without version tracking
- Skip backward compatibility considerations
- Ignore impact on existing workflows

### Testing and Validation

**✅ DO:**
- Test commands in isolation and integration
- Validate against all supported scenarios
- Include edge case testing
- Regular regression testing

**❌ DON'T:**
- Deploy without thorough testing
- Skip edge case validation
- Assume previous testing covers new changes

---

## 12. Performance Optimization Best Practices

### Method-Specific Optimizations

**CLI Optimizations:**
```javascript
// CLI-specific optimizations
const cliConfig = {
  timeout: 120000,    // 120-second timeout
  workers: 1,         // Single session requirement
  reporter: 'line',   // Fast line reporter
  retries: 0          // No automatic retries
};
```

**MCP Optimizations:**
```javascript
// MCP-specific optimizations
const mcpConfig = {
  pollingInterval: 10,    // Required 10-second intervals
  sessionReuse: true,     // Maintain single session
  earlyExit: true,        // Exit early on success
  elementWaiting: true    // Use proper element waiting
};
```

### Resource Management

**✅ DO:**
- Monitor memory usage during long test runs
- Clean up temporary files after execution
- Release browser resources properly
- Implement proper session cleanup

**❌ DON'T:**
- Let resources accumulate during execution
- Skip cleanup procedures
- Ignore memory leaks or resource issues

---

## 13. User Experience Best Practices

### Clear User Communication

**✅ DO:**
```markdown
## Task: Complete CLI Test Execution

Execute the complete B001-B016 Playwright test suite using CLI methodology with enhanced configuration and comprehensive reporting.

**Expected Duration:** 10-15 minutes for complete suite
**Progress Tracking:** Todo list will show real-time progress
**Report Location:** Generated in docs/ directory with timestamp
```

**❌ DON'T:**
```markdown
Run tests.
```

### Helpful Error Messages

**✅ DO:**
```markdown
❌ **Backend Server Not Ready**

The FastAPI backend server is not responding at http://localhost:8000/health

**Quick Fix:**
1. Start the backend: `cd gpt5-openai-agents-sdk-polygon-mcp && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`
2. Wait for "Application startup complete" message
3. Retry the command

**Alternative Ports:** If port 8000 is busy, check .env file for FASTAPI_PORT configuration
```

**❌ DON'T:**
```markdown
Backend error. Fix and retry.
```

---

## 14. Quality Assurance Best Practices

### Comprehensive Testing

**✅ DO:**
1. **Unit Testing**: Test individual components in isolation
2. **Integration Testing**: Test command execution end-to-end
3. **Performance Testing**: Validate timing accuracy and classifications
4. **Error Testing**: Test error conditions and recovery
5. **Regression Testing**: Ensure changes don't break existing functionality

### Code Review Standards

**✅ DO:**
- Review command templates for completeness
- Validate tool permissions and security
- Check error handling coverage
- Verify performance measurement accuracy
- Test with different environment configurations

**❌ DON'T:**
- Skip review for "simple" changes
- Assume testing covers all edge cases
- Ignore performance implications

---

## Conclusion

These best practices, derived from comprehensive research of Claude Code documentation, Playwright automation standards, and testing methodologies, provide a solid foundation for implementing robust and reliable Playwright testing slash commands.

Key principles to remember:

1. **Reliability First**: Robust error handling and recovery
2. **Transparency**: Accurate reporting and progress tracking
3. **Consistency**: Standardized patterns and conventions
4. **Security**: Minimal permissions and data protection
5. **Maintainability**: Clear documentation and version management
6. **User Experience**: Clear communication and helpful guidance

Following these practices ensures the `/test_cli_full` and `/test_mcp_full` commands will be valuable, reliable tools that integrate seamlessly with the Market Parser project's high-quality standards.