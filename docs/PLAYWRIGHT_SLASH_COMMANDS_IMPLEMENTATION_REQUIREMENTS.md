# Playwright Testing Slash Commands Implementation Requirements

**Comprehensive Research-Based Implementation Guide for `/test_cli_full` and `/test_mcp_full` Commands**

---

## Executive Summary

This document provides comprehensive implementation requirements for creating two new Claude Code slash commands that execute the complete B001-B016 Playwright test suite. The requirements are based on extensive research of:

- **Custom Slash Commands documentation** - Command structure and implementation patterns
- **Playwright Testing Master Plan** - Complete B001-B016 test specifications and methodologies
- **Context7 best practices research** - Claude Code patterns and Playwright automation standards

---

## 1. Implementation Requirements Matrix

### Command Specifications Comparison

| Aspect | `/test_cli_full` | `/test_mcp_full` |
|--------|------------------|------------------|
| **Purpose** | Execute B001-B016 tests via Playwright CLI | Execute B001-B016 tests via MCP browser automation |
| **File Location** | `.claude/commands/test-cli-full.md` | `.claude/commands/test-mcp-full.md` |
| **Primary Tools** | `Bash`, `TodoWrite`, `Write` | `mcp__playwright__browser_*`, `TodoWrite`, `Write` |
| **Execution Method** | `npx playwright test` commands | MCP browser automation tools |
| **Expected Performance** | Inherently faster (😊😐 majority) | Inherently slower (😐😴 expected) |
| **Session Protocol** | Single browser via `--workers=1` | Single browser session maintained |
| **Polling Method** | Internal Playwright 100ms polling | 10-second polling intervals |
| **Timeout Configuration** | `--timeout=120000` (120 seconds) | 120-second universal timeout |

### Required Tool Permissions

#### `/test_cli_full` Required Tools:
```yaml
allowed-tools: Bash(cd:*), Bash(npx:*), Bash(curl:*), Bash(ls:*), TodoWrite, Write
```

#### `/test_mcp_full` Required Tools:
```yaml
allowed-tools: mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_type, mcp__playwright__browser_click, mcp__playwright__browser_wait_for, mcp__playwright__browser_evaluate, mcp__playwright__browser_press_key, TodoWrite, Write
```

---

## 2. Technical Architecture Requirements

### Universal Requirements (Both Commands)

#### Environment Validation Protocol
- **Backend Health Check**: `curl -f http://localhost:8000/health`
- **Frontend Auto-Detection**: Support ports 3000, 3001, 3002, etc. (Vite auto-adjustment)
- **Test Files Verification**: Confirm all 16 B001-B016 .spec.ts files exist
- **Infrastructure Status**: Validate complete system readiness before execution

#### Performance Classification System
- **Good 😊**: ≤30 seconds (optimal performance)
- **OK 😐**: 31-60 seconds (acceptable performance)
- **Slow 😴**: 61-119 seconds (functional but slow)
- **TIMEOUT**: ≥120 seconds (automatic FAIL)

#### Testing Integrity Protocols
- **Todo List Management**: Create 16-item todo list tracking each B001-B016 test
- **Progress Tracking**: Mark tests as in_progress before execution, completed after success
- **Error Prevention**: No false completion reporting or fabricated results
- **Session Continuity**: Maintain single browser session throughout entire test sequence

### CLI-Specific Architecture (`/test_cli_full`)

#### Execution Pattern
```bash
# Enhanced CLI pattern with required configuration
npx playwright test --timeout=120000 --workers=1 test-b001-market-status.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b002-nvda-analysis.spec.ts
# ... continue for all B001-B016 tests
```

#### Performance Expectations
- **Target Distribution**: Majority Good 😊 and OK 😐 classifications
- **Polling Method**: Internal Playwright 100ms polling (correct, not a configuration error)
- **Average Execution**: ~48 seconds per test based on historical data

### MCP-Specific Architecture (`/test_mcp_full`)

#### Browser Session Protocol
```json
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {"url": "http://localhost:3000"}
}
```

#### Polling Configuration
```json
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {"text": "Expected Response Pattern", "time": 10}
}
```
**Critical**: 10-second intervals required (any other interval is configuration error)

#### Performance Expectations
- **Target Distribution**: More OK 😐 and Slow 😴 classifications (normal for MCP)
- **Session Maintenance**: Single browser instance throughout all tests
- **Response Detection**: 10-second polling until response or 120s timeout

---

## 3. Command Implementation Templates

### `/test_cli_full` Template

```markdown
---
allowed-tools: Bash(cd:*), Bash(npx:*), Bash(curl:*), Bash(ls:*), TodoWrite, Write
description: Execute complete B001-B016 Playwright CLI test suite with performance analysis
argument-hint: [test-filter-pattern]
---

## Environment Status Check
- Backend Status: !`curl -f http://localhost:8000/health || echo "❌ Backend not ready"`
- Frontend Status: !`curl -f http://localhost:3000/ || curl -f http://localhost:3001/ || curl -f http://localhost:3002/ || echo "❌ Frontend not ready"`
- Test Files Count: !`cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp/tests/playwright && ls test-b*.spec.ts | wc -l`

## Task: Complete CLI Test Execution

Execute the complete B001-B016 Playwright test suite using CLI methodology with enhanced configuration and comprehensive reporting.

**Testing Requirements:**
- Use `--timeout=120000 --workers=1` for all test executions
- Maintain single browser session protocol
- Track performance using 😊😐😴 classification system
- Generate `playwright_CLI_test_[timestamp].md` report
- Follow testing integrity protocols from master plan

**Focus Area:** $ARGUMENTS

**Instructions:**
1. Create todo list with 16 items for B001-B016 test tracking
2. Execute tests sequentially using enhanced CLI pattern
3. Record performance metrics for each test
4. Generate comprehensive test report with standardized format
5. Include infrastructure status and error analysis
```

### `/test_mcp_full` Template

```markdown
---
allowed-tools: mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_type, mcp__playwright__browser_click, mcp__playwright__browser_wait_for, mcp__playwright__browser_evaluate, mcp__playwright__browser_press_key, TodoWrite, Write
description: Execute complete B001-B016 Playwright MCP browser automation suite
argument-hint: [test-filter-pattern]
---

## Environment Status Check
Verify infrastructure readiness for MCP browser automation testing.

## Task: Complete MCP Browser Test Execution

Execute the complete B001-B016 Playwright test suite using MCP browser automation tools with single session protocol and 10-second polling methodology.

**Testing Requirements:**
- Maintain single browser session throughout all tests
- Use 10-second polling intervals (critical configuration requirement)
- Track performance using 😊😐😴 classification system
- Generate `playwright_MCP_test_[timestamp].md` report
- Follow MCP tool integration best practices

**Focus Area:** $ARGUMENTS

**Instructions:**
1. Create todo list with 16 items for B001-B016 test tracking
2. Initialize single browser session with mcp__playwright__browser_navigate
3. Execute tests using MCP browser tools with proper polling
4. Record performance metrics for each test
5. Generate comprehensive test report with standardized format
6. Include session continuity validation and error analysis
```

---

## 4. Report Generation Specifications

### Standard Report Structure

#### Report Naming Convention
- CLI: `playwright_CLI_test_[YY-MM-DD]_[HH-MM].md`
- MCP: `playwright_MCP_test_[YY-MM-DD]_[HH-MM].md`

#### Required Report Sections

**1. Executive Summary**
- Test coverage and completion rate
- Overall success rate and performance distribution
- Key achievements and findings
- Infrastructure status summary

**2. Performance Overview**
- Average response time across all tests
- Performance classification distribution (😊😐😴 counts)
- Method-specific performance notes
- Infrastructure stability metrics

**3. Detailed Test Results**
For each B001-B016 test:
```markdown
#### B001: Market Status Check ✅ PASS 😊 (28s)
- **Result:** PASS - Response received within 120s timeout
- **Performance:** Good 😊 (28 seconds - optimal performance)
- **Validation:** Market data retrieval functionality confirmed
- **Response Format:** Proper emoji-enhanced financial analysis received
- **Method Notes:** [CLI/MCP specific observations]
```

**4. Infrastructure Assessment**
```markdown
### System Components Status
✅ **FastAPI Backend:** Operational on port 8000
✅ **Vite Development Server:** Operational on port [auto-detected]
✅ **MCP Server Integration:** Polygon.io connectivity confirmed
✅ **OpenAI API Integration:** GPT-5-mini model responding correctly
✅ **Database/Session Management:** State persistence working
```

**5. Quality Metrics**
- Test completion rate calculation
- Performance distribution analysis
- Error recovery validation
- Infrastructure uptime percentage

---

## 5. Error Handling and Recovery Patterns

### Common Error Scenarios

#### Server Startup Issues
- **Backend Problems**: API key validation, port conflicts, uv installation
- **Frontend Issues**: Node.js version, npm dependencies, port auto-adjustment
- **CORS Problems**: Cross-origin configuration validation

#### Test Execution Issues
- **Browser Installation**: `npx playwright install chromium` requirement
- **Timeout Handling**: 120-second limit with graceful degradation
- **Session Breaks**: Single browser session maintenance validation
- **Performance Issues**: MCP timeout configuration adjustment

#### Recovery Procedures
```markdown
**Port Conflict Resolution:**
1. Detect actual frontend port: curl-based detection
2. Update test configuration accordingly
3. Validate connectivity before proceeding

**Infrastructure Recovery:**
1. Server health check validation
2. Automatic retry with backoff
3. Clear error messaging for user guidance
```

---

## 6. Integration Points and Dependencies

### TodoWrite Integration
- **Purpose**: Track progress through all 16 B001-B016 tests
- **Pattern**: Create todo list → Mark in_progress → Mark completed
- **Integrity**: Prevent false completion reporting

### Write Tool Integration
- **Purpose**: Generate standardized test reports
- **Pattern**: Collect metrics → Format report → Write to file
- **Standards**: Follow exact naming conventions and formatting templates

### MCP Tool Dependencies
- **Navigation**: `mcp__playwright__browser_navigate` for session initialization
- **Interaction**: Complete set of browser tools for test execution
- **Validation**: `mcp__playwright__browser_evaluate` for result verification

### Bash Tool Dependencies
- **Environment**: Health checks and validation commands
- **Execution**: Playwright CLI commands with proper configuration
- **Monitoring**: Infrastructure status throughout execution

---

## 7. Quality Assurance Requirements

### Testing Integrity Protocols
- **Mandatory**: No fabricated or false completion reports
- **Required**: Complete test execution before claiming success
- **Standard**: Honest documentation of failures and incomplete results
- **Process**: Multiple verification steps prevent false reporting

### Performance Measurement Standards
- **Accuracy**: Report actual timing data, not estimated values
- **Classification**: Proper use of 😊😐😴 performance categories
- **Method Awareness**: Account for inherent speed differences between CLI/MCP
- **Baseline Establishment**: Document performance baselines for optimization

### Infrastructure Validation Requirements
- **Pre-flight Checks**: Complete environment validation before execution
- **Continuous Monitoring**: Infrastructure status throughout testing
- **Error Recovery**: Graceful handling of infrastructure failures
- **Documentation**: Complete infrastructure status in all reports

---

## 8. Best Practice Recommendations

### Command Design Principles
1. **Single Purpose**: Each command has one clear, well-defined purpose
2. **Self-Documenting**: Clear descriptions and comprehensive error messages
3. **Robust Validation**: Extensive pre-flight checks and error handling
4. **Consistent Output**: Standardized reporting across both methodologies

### Implementation Best Practices
1. **Tool Permissions**: Minimal required permissions for security
2. **Error Handling**: Comprehensive error scenarios with clear recovery steps
3. **Performance Optimization**: Method-appropriate optimization strategies
4. **Documentation**: Detailed inline documentation and user guidance

### Integration Best Practices
1. **Modular Design**: Commands can be executed independently
2. **Standard Interfaces**: Consistent argument handling and output formats
3. **Quality Controls**: Multiple validation points prevent common errors
4. **Maintenance**: Clear patterns for updates and modifications

---

## 9. Implementation Checklist

### Pre-Implementation Requirements
- [ ] Verify `.claude/commands/` directory exists
- [ ] Confirm all required tools are available
- [ ] Validate test environment setup (B001-B016 files)
- [ ] Test infrastructure connectivity

### Command Creation Steps
- [ ] Create `test-cli-full.md` with complete template
- [ ] Create `test-mcp-full.md` with complete template
- [ ] Validate YAML frontmatter configuration
- [ ] Test argument handling and validation
- [ ] Verify tool permissions and execution

### Integration Validation
- [ ] Test TodoWrite integration for progress tracking
- [ ] Test Write tool integration for report generation
- [ ] Validate error handling and recovery procedures
- [ ] Confirm performance measurement accuracy

### Quality Assurance Testing
- [ ] Execute complete CLI test sequence
- [ ] Execute complete MCP test sequence
- [ ] Compare output quality and consistency
- [ ] Validate reporting accuracy and completeness

---

This comprehensive implementation guide provides all necessary specifications for creating robust, reliable Playwright testing slash commands that follow established best practices and maintain the highest quality standards established in the Market Parser project's testing protocols.