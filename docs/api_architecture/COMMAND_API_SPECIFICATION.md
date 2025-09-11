# Playwright Slash Commands API Specification

**Comprehensive Command API Architecture for `/test_cli_full` and `/test_mcp_full` Implementation**

---

## Executive Summary

This document defines the complete API specification for implementing two Playwright testing slash commands within the Claude Code environment. The specification ensures compliance with established patterns while providing robust testing capabilities for the B001-B016 test suite.

---

## 1. Command Structure Specifications

### File Organization API

```
.claude/
└── commands/
    ├── test-cli-full.md
    └── test-mcp-full.md
```

**Naming Convention Standards:**
- Hyphenated filenames for consistency with Claude Code patterns
- Descriptive names indicating method and scope
- `.md` extension for markdown-based command definitions

### YAML Frontmatter API Specification

#### CLI Command Frontmatter
```yaml
---
allowed-tools: Bash(cd:*), Bash(npx:*), Bash(curl:*), Bash(ls:*), TodoWrite, Write
description: Execute complete B001-B016 Playwright CLI test suite with performance analysis
argument-hint: [test-filter-pattern]
---
```

#### MCP Command Frontmatter
```yaml
---
allowed-tools: mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_type, mcp__playwright__browser_click, mcp__playwright__browser_wait_for, mcp__playwright__browser_evaluate, mcp__playwright__browser_press_key, TodoWrite, Write
description: Execute complete B001-B016 Playwright MCP browser automation suite
argument-hint: [test-filter-pattern]
---
```

---

## 2. Tool Permission Matrix API

### Permission Classification System

| Permission Category | CLI Method | MCP Method | Justification |
|-------------------|------------|------------|---------------|
| **File System Navigation** | `Bash(cd:*)` | ❌ Not Required | CLI needs directory navigation for test execution |
| **Process Execution** | `Bash(npx:*)` | ❌ Not Required | CLI requires Playwright CLI execution |
| **Network Validation** | `Bash(curl:*)` | ❌ Not Required | Health checks for environment validation |
| **File Listing** | `Bash(ls:*)` | ❌ Not Required | Test file validation and counting |
| **Browser Navigation** | ❌ Not Required | `mcp__playwright__browser_navigate` | MCP session initialization |
| **Browser Snapshot** | ❌ Not Required | `mcp__playwright__browser_snapshot` | State capture and validation |
| **Browser Interaction** | ❌ Not Required | `mcp__playwright__browser_type`, `mcp__playwright__browser_click`, `mcp__playwright__browser_press_key` | Test execution interactions |
| **Response Detection** | ❌ Not Required | `mcp__playwright__browser_wait_for` | Response polling with 10s intervals |
| **State Validation** | ❌ Not Required | `mcp__playwright__browser_evaluate` | Result extraction and validation |
| **Progress Tracking** | `TodoWrite` | `TodoWrite` | 16-item B001-B016 progress tracking |
| **Report Generation** | `Write` | `Write` | Standardized test report creation |

### Security Constraints API

```typescript
interface SecurityConstraints {
  toolRestrictions: {
    noBashWildcard: boolean;           // No Bash(*) permissions
    restrictedToSpecific: boolean;     // Only specific tool patterns allowed
    readOnlyTestFiles: boolean;        // Read-only access to test files
    writeOnlyReports: boolean;         // Write access limited to report directory
  };
  
  dataProtection: {
    noSensitiveData: boolean;          // No sensitive data in reports
    sanitizedErrors: boolean;          // Sanitized error messages
    tempFileCleanup: boolean;          // Temporary file cleanup
  };
  
  executionLimits: {
    maxExecutionTime: number;          // 30 minutes maximum
    singleProcess: boolean;            // Single process per command
    resourceMonitoring: boolean;       // Resource usage monitoring
  };
}
```

---

## 3. Command Interface API

### Argument Handling Specification

```typescript
interface CommandArguments {
  testFilterPattern?: string;          // Optional test filter (B001-B003, priority-tests, all)
  
  // Supported patterns:
  // "B001-B003"      - Range selection
  // "priority-tests" - Priority test subset
  // "all"           - Complete B001-B016 suite (default)
  // undefined       - Execute all tests
}
```

### Environment Validation API

```typescript
interface EnvironmentValidation {
  // Dynamic validation using ! prefix in markdown
  backendHealth: {
    command: "curl -f http://localhost:8000/health || echo '❌ Backend not ready'";
    expected: string;                  // "ok" response or error message
    required: true;
  };
  
  frontendDetection: {
    command: "curl -f http://localhost:3000/ || curl -f http://localhost:3001/ || curl -f http://localhost:3002/ || echo '❌ Frontend not ready'";
    ports: number[];                   // [3000, 3001, 3002, ...] auto-detection
    required: true;
  };
  
  testFileValidation: {
    command: "cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp/tests/playwright && ls test-b*.spec.ts | wc -l";
    expected: 16;                      // Must find all 16 B001-B016 test files
    required: true;
  };
  
  playwrightInstallation: {
    command: "npx playwright --version || echo '❌ Playwright not installed'";
    expected: string;                  // Version string or error message
    required: true;
  };
}
```

### Command Template API Structure

```typescript
interface CommandTemplate {
  frontmatter: YAMLFrontmatter;        // Tool permissions and metadata
  environmentCheck: EnvironmentValidation; // Dynamic validation section
  taskDefinition: {
    title: string;                     // Clear task description
    requirements: string[];            // Bullet-pointed requirements
    focusArea: string;                 // $ARGUMENTS integration
    instructions: string[];            // Step-by-step execution plan
  };
}
```

---

## 4. Parameter Handling API

### CLI Method Parameters

```typescript
interface CLIParameters {
  timeout: 120000;                     // 120-second universal timeout (milliseconds)
  workers: 1;                          // Single worker for session continuity
  reporter: 'line';                    // Fast line reporter for performance
  retries: 0;                          // No automatic retries
  
  // Command construction:
  buildCommand(testFile: string): string {
    return `npx playwright test --timeout=${this.timeout} --workers=${this.workers} --reporter=${this.reporter} ${testFile}`;
  }
}
```

### MCP Method Parameters

```typescript
interface MCPParameters {
  sessionManagement: {
    singleSession: true;               // Maintain single browser session
    sessionValidation: boolean;        // Validate session continuity
    browserReuse: true;                // Reuse browser instance
  };
  
  pollingConfiguration: {
    interval: 10;                      // 10-second polling intervals (required)
    maxAttempts: 12;                   // 120s total timeout (12 * 10s)
    earlyExit: true;                   // Exit early on successful response
  };
  
  responseDetection: {
    expectedPatterns: string[];        // Expected response patterns
    timeoutHandling: 'graceful';       // Graceful timeout degradation
    validationRequired: boolean;       // Response validation required
  };
}
```

---

## 5. Integration Hooks API

### Claude Code Integration Points

```typescript
interface ClaudeCodeIntegration {
  commandParser: {
    yamlFrontmatterValidation: boolean; // YAML validation on command load
    toolPermissionValidation: boolean;  // Permission validation before execution
    argumentParsing: boolean;           // $ARGUMENTS variable integration
  };
  
  executionEnvironment: {
    environmentValidation: boolean;     // Pre-flight environment checks
    dynamicValidation: boolean;         // ! prefix command execution
    errorHandling: boolean;            // Structured error handling
  };
  
  reportingIntegration: {
    standardizedOutput: boolean;        // Consistent report formats
    timestampGeneration: boolean;       // Automatic timestamp generation
    fileNaming: boolean;               // Standardized file naming
  };
}
```

### MCP Tool Integration Hooks

```typescript
interface MCPToolIntegration {
  browserAutomation: {
    navigationHook: 'mcp__playwright__browser_navigate';
    snapshotHook: 'mcp__playwright__browser_snapshot';
    interactionHooks: [
      'mcp__playwright__browser_type',
      'mcp__playwright__browser_click', 
      'mcp__playwright__browser_press_key'
    ];
    waitingHook: 'mcp__playwright__browser_wait_for';
    evaluationHook: 'mcp__playwright__browser_evaluate';
  };
  
  progressTracking: {
    todoWriteHook: 'TodoWrite';         // Progress tracking integration
    stateTransitions: ['pending', 'in_progress', 'completed'];
    integrityValidation: boolean;       // Prevent false completion reporting
  };
  
  reportGeneration: {
    writeHook: 'Write';                // Report file generation
    templateSystem: boolean;           // Standardized report templates
    performanceIntegration: boolean;   // Performance data integration
  };
}
```

---

## 6. Error Handling API Specification

### Error Classification System

```typescript
enum ErrorType {
  INFRASTRUCTURE = 'infrastructure',
  TEST_EXECUTION = 'test_execution', 
  SESSION_MANAGEMENT = 'session_management',
  TIMEOUT = 'timeout',
  VALIDATION = 'validation'
}

interface ErrorHandler {
  classifyError(error: Error): ErrorType;
  handleInfrastructureError(error: Error, context: ExecutionContext): RecoveryAction;
  handleTestExecutionError(error: Error, context: ExecutionContext): RecoveryAction;
  handleSessionError(error: Error, context: ExecutionContext): RecoveryAction;
  handleTimeoutError(error: Error, context: ExecutionContext): RecoveryAction;
  handleValidationError(error: Error, context: ExecutionContext): RecoveryAction;
}

interface RecoveryAction {
  action: 'retry' | 'skip' | 'restart_session' | 'graceful_exit';
  maxRetries?: number;
  backoffStrategy?: 'linear' | 'exponential';
  continueExecution: boolean;
}
```

### Error Recovery Workflows

```typescript
interface ErrorRecoveryWorkflow {
  infrastructureErrors: {
    detection: 'curl_health_check_failure';
    recovery: ['retry_with_backoff', 'graceful_exit'];
    maxAttempts: 3;
    backoffDelay: [5, 10, 20]; // seconds
  };
  
  testExecutionErrors: {
    detection: 'test_timeout_or_failure';
    recovery: ['skip_test', 'continue_suite'];
    logging: 'detailed_error_capture';
    reporting: 'include_in_final_report';
  };
  
  sessionManagementErrors: {
    detection: 'browser_session_lost';
    recovery: ['restart_session', 'retry_current_test'];
    sessionValidation: 'verify_continuity';
    fallback: 'graceful_degradation';
  };
}
```

---

This comprehensive Command API Specification provides the complete foundation for implementing robust, maintainable, and secure Playwright testing slash commands that seamlessly integrate with the Claude Code environment while adhering to all established architectural patterns and constraints.