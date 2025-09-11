# Integration Interface Definitions

**Comprehensive Integration APIs for Playwright Slash Commands System Integration**

---

## Executive Summary

This document defines all integration interfaces required for seamless operation of the `/test_cli_full` and `/test_mcp_full` commands within the Market Parser ecosystem. These interfaces ensure consistent data flow, proper error handling, and maintainable system architecture.

---

## 1. TodoWrite Progress Tracking Integration

### TodoWrite API Interface

```typescript
interface TodoWriteIntegration {
  // Core TodoWrite interface for 16-test tracking
  createTestSuite(): TodoItem[];
  updateTestStatus(testId: string, status: TodoStatus): Promise<boolean>;
  validateCompletionIntegrity(): ValidationResult;
  getProgressSummary(): ProgressSummary;
}

interface TodoItem {
  content: string;           // "Execute B001: Market Status Check"
  status: TodoStatus;        // pending | in_progress | completed
  activeForm: string;        // "Executing B001: Market Status Check"
  testId: string;           // "B001", "B002", etc.
  timestamp?: Date;         // When status last changed
  metadata?: TestMetadata;  // Additional test context
}

enum TodoStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed'
}

interface TestMetadata {
  method: 'CLI' | 'MCP';
  duration?: number;        // Execution duration in seconds
  performance?: PerformanceClassification;
  errorDetails?: string;    // Error information if applicable
}
```

### TodoWrite State Management

```typescript
interface TodoWriteStateManager {
  // State transition validation
  validateStateTransition(
    currentState: TodoStatus, 
    newState: TodoStatus, 
    testContext: TestExecutionContext
  ): boolean;
  
  // Progress tracking utilities
  calculateCompletionRate(): number;
  getActiveTests(): TodoItem[];
  getPendingTests(): TodoItem[];
  getCompletedTests(): TodoItem[];
  
  // Testing integrity enforcement
  preventFalseCompletion(): boolean;
  requireActualExecution(testId: string): boolean;
  validateSequentialExecution(): boolean;
}

interface TestExecutionContext {
  testId: string;
  startTime: Date;
  method: 'CLI' | 'MCP';
  actualExecutionEvidence: ExecutionEvidence;
}

interface ExecutionEvidence {
  commandExecuted: string;
  outputReceived: string;
  timingData: TimingData;
  validationPassed: boolean;
}
```

### TodoWrite Integration Patterns

```typescript
// Standard 16-test suite initialization
const initializeTodoSuite = (): TodoItem[] => {
  const testSuite = [
    'B001: Market Status Check',
    'B002: NVDA Ticker Analysis', 
    'B003: Stock Data Retrieval',
    'B004: Price Information Query',
    'B005: Volume Analysis Request',
    'B006: Market Trends Inquiry',
    'B007: Financial Metrics Query',
    'B008: Sector Analysis Request',
    'B009: Performance Comparison',
    'B010: Risk Assessment Query',
    'B011: Portfolio Analysis Request',
    'B012: Investment Recommendation',
    'B013: Market Forecast Query',
    'B014: Technical Analysis Request',
    'B015: Earnings Data Inquiry',
    'B016: Economic Indicators Query'
  ];
  
  return testSuite.map((description, index) => ({
    content: `Execute ${description}`,
    status: TodoStatus.PENDING,
    activeForm: `Executing ${description}`,
    testId: `B${(index + 1).toString().padStart(3, '0')}`,
    timestamp: new Date()
  }));
};

// State transition enforcement
const enforceTestingIntegrity = async (
  testId: string, 
  newStatus: TodoStatus,
  executionEvidence: ExecutionEvidence
): Promise<boolean> => {
  // Prevent false completion reporting
  if (newStatus === TodoStatus.COMPLETED && !executionEvidence.validationPassed) {
    throw new IntegrityViolationError('Cannot mark completed without execution evidence');
  }
  
  // Require actual execution before completion
  if (newStatus === TodoStatus.COMPLETED && !executionEvidence.actualExecutionEvidence) {
    throw new IntegrityViolationError('Cannot mark completed without actual execution');
  }
  
  return true;
};
```

---

## 2. Report Generation Integration API

### Report Generation Interface

```typescript
interface ReportGenerationAPI {
  // Core report generation methods
  generateCLIReport(testResults: TestResult[], metadata: ReportMetadata): Promise<string>;
  generateMCPReport(testResults: TestResult[], metadata: ReportMetadata): Promise<string>;
  
  // Report formatting utilities
  formatExecutiveSummary(results: TestResult[]): string;
  formatDetailedResults(results: TestResult[]): string;
  formatPerformanceAnalysis(distribution: PerformanceDistribution): string;
  formatInfrastructureAssessment(infrastructure: InfrastructureStatus): string;
  formatQualityMetrics(metrics: QualityMetrics): string;
  
  // File operations
  saveReport(content: string, filename: string): Promise<boolean>;
  generateTimestamp(): string;
  validateReportContent(content: string): ValidationResult;
}

interface TestResult {
  testId: string;           // "B001", "B002", etc.
  description: string;      // "Market Status Check"
  status: TestStatus;       // PASS | FAIL | TIMEOUT
  duration: number;         // Execution time in seconds
  performance: PerformanceClassification; // 😊😐😴❌
  method: TestMethod;       // CLI | MCP
  details: TestDetails;
  timestamp: Date;
}

enum TestStatus {
  PASS = 'PASS',
  FAIL = 'FAIL', 
  TIMEOUT = 'TIMEOUT'
}

enum TestMethod {
  CLI = 'CLI',
  MCP = 'MCP'
}

interface TestDetails {
  commandExecuted?: string;   // CLI command or MCP action sequence
  responseReceived: boolean;
  responseContent?: string;   // Actual response content
  errorMessage?: string;      // Error details if applicable
  validationResult?: string;  // Response validation outcome
  infrastructureNotes?: string; // Method-specific observations
}
```

### Report Template System

```typescript
interface ReportTemplateSystem {
  // Template definitions
  getReportTemplate(method: TestMethod): ReportTemplate;
  applyTemplate(template: ReportTemplate, data: ReportData): string;
  validateTemplate(template: ReportTemplate): boolean;
  
  // Custom formatting
  formatTestResult(result: TestResult): string;
  formatPerformanceIndicator(classification: PerformanceClassification): string;
  formatTimestamp(date: Date): string;
  formatFilename(method: TestMethod, timestamp: string): string;
}

interface ReportTemplate {
  header: HeaderTemplate;
  executiveSummary: SummaryTemplate;
  performanceOverview: PerformanceTemplate;
  detailedResults: ResultsTemplate;
  infrastructureAssessment: InfrastructureTemplate;
  qualityMetrics: QualityTemplate;
  footer: FooterTemplate;
}

interface HeaderTemplate {
  title: string;
  reportDate: string;
  testCoverage: string;
  method: string;
  overallSuccessRate: string;
}

// Standard report naming convention
const generateReportFilename = (method: TestMethod): string => {
  const timestamp = new Date()
    .toISOString()
    .slice(0, 16)
    .replace('T', '_')
    .replace(/:/g, '-');
  
  return `playwright_${method}_test_${timestamp}.md`;
};
```

### Performance Data Integration

```typescript
interface PerformanceDataIntegration {
  // Performance classification logic
  classifyPerformance(duration: number): PerformanceClassification;
  
  // Performance distribution analysis
  analyzeDistribution(results: TestResult[]): PerformanceDistribution;
  
  // Method-specific performance context
  getMethodContext(method: TestMethod): PerformanceContext;
  
  // Performance insights generation
  generateInsights(distribution: PerformanceDistribution, method: TestMethod): PerformanceInsights;
}

enum PerformanceClassification {
  GOOD = '😊',      // ≤30 seconds
  OK = '😐',        // 31-60 seconds  
  SLOW = '😴',      // 61-119 seconds
  TIMEOUT = '❌'    // ≥120 seconds
}

interface PerformanceDistribution {
  good: number;     // Count of 😊 tests
  ok: number;       // Count of 😐 tests
  slow: number;     // Count of 😴 tests
  timeout: number;  // Count of ❌ tests
  total: number;    // Total test count
  averageDuration: number; // Average execution time
}

interface PerformanceContext {
  method: TestMethod;
  expectedDistribution: PerformanceDistribution; // Expected performance profile
  optimizations: string[];                       // Method-specific optimizations
  limitations: string[];                         // Known limitations
}

interface PerformanceInsights {
  summary: string;              // Overall performance assessment
  trends: string[];            // Performance trends observed
  recommendations: string[];   // Optimization recommendations
  methodSpecificNotes: string; // CLI vs MCP specific observations
}
```

---

## 3. Error Handling Integration API

### Error Classification and Recovery Interface

```typescript
interface ErrorHandlingIntegration {
  // Error classification
  classifyError(error: Error, context: ErrorContext): ErrorClassification;
  
  // Recovery strategies
  getRecoveryStrategy(classification: ErrorClassification): RecoveryStrategy;
  
  // Error recovery execution
  executeRecovery(strategy: RecoveryStrategy, context: ErrorContext): Promise<RecoveryResult>;
  
  // Error logging and reporting
  logError(error: Error, context: ErrorContext, recovery: RecoveryResult): void;
  includeInReport(error: Error, recovery: RecoveryResult): ErrorReportEntry;
}

interface ErrorContext {
  testId?: string;              // Which test was executing
  method: TestMethod;           // CLI or MCP method
  phase: ExecutionPhase;        // Which phase error occurred
  timestamp: Date;              // When error occurred
  environmentState: EnvironmentState; // System state at error time
}

enum ExecutionPhase {
  ENVIRONMENT_VALIDATION = 'environment_validation',
  TEST_INITIALIZATION = 'test_initialization',
  TEST_EXECUTION = 'test_execution',
  RESULT_VALIDATION = 'result_validation',
  REPORT_GENERATION = 'report_generation'
}

interface ErrorClassification {
  type: ErrorType;
  severity: ErrorSeverity;
  recoverable: boolean;
  category: ErrorCategory;
  description: string;
}

enum ErrorType {
  INFRASTRUCTURE = 'infrastructure',
  TEST_EXECUTION = 'test_execution',
  SESSION_MANAGEMENT = 'session_management', 
  TIMEOUT = 'timeout',
  VALIDATION = 'validation',
  CONFIGURATION = 'configuration'
}

enum ErrorSeverity {
  LOW = 'low',        // Continue execution
  MEDIUM = 'medium',  // Skip current test, continue suite
  HIGH = 'high',      // Attempt recovery, may fail
  CRITICAL = 'critical' // Graceful exit required
}

enum ErrorCategory {
  TRANSIENT = 'transient',     // Temporary issue, retry likely to succeed
  PERSISTENT = 'persistent',   // Consistent issue, retry unlikely to help
  ENVIRONMENTAL = 'environmental', // System/environment issue
  LOGICAL = 'logical'         // Logic or configuration issue
}
```

### Recovery Strategy Implementation

```typescript
interface RecoveryStrategy {
  action: RecoveryAction;
  maxRetries: number;
  backoffStrategy: BackoffStrategy;
  continueExecution: boolean;
  fallbackAction?: RecoveryAction;
}

enum RecoveryAction {
  RETRY = 'retry',
  SKIP_TEST = 'skip_test',
  RESTART_SESSION = 'restart_session',
  GRACEFUL_EXIT = 'graceful_exit',
  REINITIALIZE_ENVIRONMENT = 'reinitialize_environment'
}

interface BackoffStrategy {
  type: 'linear' | 'exponential' | 'fixed';
  baseDelay: number;        // Base delay in milliseconds
  maxDelay: number;         // Maximum delay in milliseconds
  multiplier?: number;      // For exponential backoff
}

interface RecoveryResult {
  success: boolean;
  attemptsUsed: number;
  totalRecoveryTime: number; // Time spent on recovery in milliseconds
  finalAction: RecoveryAction;
  continueExecution: boolean;
  errorDetails?: string;
}

// Standard error recovery workflows
const getStandardRecoveryStrategy = (classification: ErrorClassification): RecoveryStrategy => {
  switch (classification.type) {
    case ErrorType.INFRASTRUCTURE:
      return {
        action: RecoveryAction.RETRY,
        maxRetries: 3,
        backoffStrategy: {
          type: 'exponential',
          baseDelay: 5000,  // 5 seconds
          maxDelay: 30000,  // 30 seconds
          multiplier: 2
        },
        continueExecution: true,
        fallbackAction: RecoveryAction.GRACEFUL_EXIT
      };
      
    case ErrorType.TEST_EXECUTION:
      return {
        action: RecoveryAction.SKIP_TEST,
        maxRetries: 0,
        backoffStrategy: { type: 'fixed', baseDelay: 0, maxDelay: 0 },
        continueExecution: true
      };
      
    case ErrorType.SESSION_MANAGEMENT:
      return {
        action: RecoveryAction.RESTART_SESSION,
        maxRetries: 2,
        backoffStrategy: { type: 'linear', baseDelay: 10000, maxDelay: 10000 },
        continueExecution: true,
        fallbackAction: RecoveryAction.GRACEFUL_EXIT
      };
      
    default:
      return {
        action: RecoveryAction.GRACEFUL_EXIT,
        maxRetries: 0,
        backoffStrategy: { type: 'fixed', baseDelay: 0, maxDelay: 0 },
        continueExecution: false
      };
  }
};
```

---

## 4. MCP Tool Integration Interface

### MCP Browser Automation Integration

```typescript
interface MCPBrowserIntegration {
  // Session management
  initializeSession(url: string): Promise<SessionContext>;
  validateSession(context: SessionContext): Promise<boolean>;
  cleanupSession(context: SessionContext): Promise<void>;
  
  // Browser interactions
  navigateToUrl(url: string, context: SessionContext): Promise<NavigationResult>;
  captureSnapshot(context: SessionContext): Promise<SnapshotResult>;
  typeText(text: string, selector: string, context: SessionContext): Promise<InteractionResult>;
  clickElement(selector: string, context: SessionContext): Promise<InteractionResult>;
  pressKey(key: string, context: SessionContext): Promise<InteractionResult>;
  
  // Response detection and validation
  waitForResponse(pattern: string, timeout: number, context: SessionContext): Promise<ResponseResult>;
  evaluateContent(script: string, context: SessionContext): Promise<EvaluationResult>;
  extractResponseData(context: SessionContext): Promise<ExtractedData>;
}

interface SessionContext {
  sessionId: string;
  browserInstance: string;
  currentUrl: string;
  established: Date;
  lastActivity: Date;
  isValid: boolean;
}

interface NavigationResult {
  success: boolean;
  finalUrl: string;
  loadTime: number;
  errors?: string[];
}

interface SnapshotResult {
  success: boolean;
  snapshotData: string;      // Snapshot content or reference
  timestamp: Date;
  errors?: string[];
}

interface InteractionResult {
  success: boolean;
  action: string;            // Description of action performed
  duration: number;          // Time taken for interaction
  errors?: string[];
}

interface ResponseResult {
  success: boolean;
  responseDetected: boolean;
  detectionTime: number;     // Time until response detected
  responseContent?: string;
  timeoutReached: boolean;
  errors?: string[];
}

interface EvaluationResult {
  success: boolean;
  evaluationResult: any;     // Result of JavaScript evaluation
  executionTime: number;
  errors?: string[];
}

interface ExtractedData {
  responseText: string;
  responseFormat: 'json' | 'text' | 'html';
  extractedMetrics: ResponseMetrics;
  validationStatus: ValidationStatus;
}
```

### MCP Polling Configuration Interface

```typescript
interface MCPPollingIntegration {
  // Polling configuration management
  getPollingConfig(): PollingConfiguration;
  validatePollingConfig(config: PollingConfiguration): boolean;
  
  // Polling execution
  executePolling(pattern: string, config: PollingConfiguration): Promise<PollingResult>;
  
  // Early exit optimization
  checkEarlyExit(currentAttempt: number, result: any): boolean;
}

interface PollingConfiguration {
  interval: number;          // 10 seconds (required)
  maxAttempts: number;       // 12 attempts = 120s total
  earlyExit: boolean;        // Exit early on successful detection
  responsePattern: string;   // Pattern to detect in responses
  timeoutBehavior: 'graceful' | 'error';
}

interface PollingResult {
  success: boolean;
  totalAttempts: number;
  totalDuration: number;     // Total polling time
  responseDetected: boolean;
  finalResponse?: string;
  earlyExitUsed: boolean;
  errors?: string[];
}

// Standard 10-second polling implementation
const standardPollingConfig: PollingConfiguration = {
  interval: 10,              // 10 seconds (configuration requirement)
  maxAttempts: 12,           // 120 total seconds
  earlyExit: true,
  responsePattern: '',       // Set per test
  timeoutBehavior: 'graceful'
};
```

---

## 5. Performance Measurement Integration

### Performance Metrics Collection Interface

```typescript
interface PerformanceMetricsIntegration {
  // Timing measurement
  startTimer(testId: string): TimerContext;
  stopTimer(context: TimerContext): TimingResult;
  
  // Performance classification
  classifyPerformance(duration: number, method: TestMethod): PerformanceClassification;
  
  // Metrics aggregation
  aggregateMetrics(results: TestResult[]): PerformanceMetrics;
  
  // Method-specific analysis
  analyzeMethodPerformance(results: TestResult[], method: TestMethod): MethodPerformanceAnalysis;
}

interface TimerContext {
  testId: string;
  startTime: Date;
  method: TestMethod;
  timerActive: boolean;
}

interface TimingResult {
  testId: string;
  duration: number;          // Duration in seconds
  startTime: Date;
  endTime: Date;
  accuracy: TimingAccuracy;
}

enum TimingAccuracy {
  PRECISE = 'precise',       // Actual measured timing
  ESTIMATED = 'estimated',   // Estimated timing
  TIMEOUT = 'timeout'        // Timeout reached
}

interface PerformanceMetrics {
  totalTests: number;
  averageDuration: number;
  medianDuration: number;
  distribution: PerformanceDistribution;
  methodComparison?: MethodComparison;
}

interface MethodPerformanceAnalysis {
  method: TestMethod;
  expectedProfile: PerformanceProfile;
  actualProfile: PerformanceProfile;
  variance: PerformanceVariance;
  insights: string[];
}

interface PerformanceProfile {
  averageDuration: number;
  distributionExpected: PerformanceDistribution;
  optimizationFactors: string[];
}

interface PerformanceVariance {
  durationVariance: number;
  distributionDifference: PerformanceDistribution;
  significantDeviations: string[];
}
```

### Universal Timeout Integration

```typescript
interface TimeoutIntegration {
  // Universal timeout management
  setUniversalTimeout(seconds: number): void;
  getUniversalTimeout(): number;
  
  // Timeout enforcement
  enforceTimeout<T>(
    operation: () => Promise<T>,
    timeoutMs: number,
    context: TimeoutContext
  ): Promise<TimeoutResult<T>>;
  
  // Timeout classification
  classifyTimeout(duration: number): TimeoutClassification;
}

interface TimeoutContext {
  testId: string;
  method: TestMethod;
  operation: string;
  startTime: Date;
}

interface TimeoutResult<T> {
  success: boolean;
  result?: T;
  timedOut: boolean;
  duration: number;
  context: TimeoutContext;
}

enum TimeoutClassification {
  WITHIN_LIMIT = 'within_limit',
  APPROACHING_LIMIT = 'approaching_limit', // 80-119 seconds
  TIMEOUT_REACHED = 'timeout_reached'      // ≥120 seconds
}

// Universal 120-second timeout enforcement
const UNIVERSAL_TIMEOUT_SECONDS = 120;
const UNIVERSAL_TIMEOUT_MS = UNIVERSAL_TIMEOUT_SECONDS * 1000;

const enforceUniversalTimeout = async <T>(
  operation: () => Promise<T>,
  context: TimeoutContext
): Promise<TimeoutResult<T>> => {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => {
      reject(new Error(`Operation timed out after ${UNIVERSAL_TIMEOUT_SECONDS} seconds`));
    }, UNIVERSAL_TIMEOUT_MS);
  });
  
  try {
    const startTime = Date.now();
    const result = await Promise.race([operation(), timeoutPromise]);
    const duration = (Date.now() - startTime) / 1000;
    
    return {
      success: true,
      result,
      timedOut: false,
      duration,
      context
    };
  } catch (error) {
    const duration = (Date.now() - context.startTime.getTime()) / 1000;
    
    return {
      success: false,
      timedOut: duration >= UNIVERSAL_TIMEOUT_SECONDS,
      duration,
      context
    };
  }
};
```

---

## 6. Environment Validation Integration

### Infrastructure Health Check Interface

```typescript
interface InfrastructureValidationIntegration {
  // System health checks
  validateBackendHealth(): Promise<HealthCheckResult>;
  validateFrontendHealth(): Promise<HealthCheckResult>;
  validateTestEnvironment(): Promise<EnvironmentCheckResult>;
  
  // Comprehensive validation
  performFullValidation(): Promise<ValidationSummary>;
  
  // Auto-recovery capabilities
  attemptInfrastructureRecovery(issues: ValidationIssue[]): Promise<RecoveryResult>;
}

interface HealthCheckResult {
  service: string;           // 'backend' | 'frontend'
  healthy: boolean;
  responseTime: number;      // Response time in milliseconds
  endpoint: string;          // Tested endpoint
  details: HealthDetails;
  timestamp: Date;
}

interface HealthDetails {
  status?: string;           // Service-specific status
  version?: string;          // Service version if available
  port: number;              // Service port
  errors?: string[];         // Any error messages
}

interface EnvironmentCheckResult {
  component: string;         // Component being checked
  valid: boolean;
  expectedValue: any;        // What was expected
  actualValue: any;          // What was found
  checkType: EnvironmentCheckType;
  details?: string;
}

enum EnvironmentCheckType {
  FILE_COUNT = 'file_count',
  SERVICE_AVAILABILITY = 'service_availability',
  DEPENDENCY_INSTALLATION = 'dependency_installation',
  CONFIGURATION = 'configuration'
}

interface ValidationSummary {
  overallValid: boolean;
  componentResults: EnvironmentCheckResult[];
  healthResults: HealthCheckResult[];
  criticalIssues: ValidationIssue[];
  warnings: ValidationIssue[];
  validationTime: number;    // Total validation time in milliseconds
}

interface ValidationIssue {
  severity: 'critical' | 'warning' | 'info';
  component: string;
  description: string;
  suggestion: string;        // Suggested resolution
  recoverable: boolean;
}
```

### Dynamic Environment Detection

```typescript
interface DynamicEnvironmentDetection {
  // Port detection and management
  detectFrontendPort(): Promise<PortDetectionResult>;
  validatePortAccess(port: number): Promise<boolean>;
  
  // Service discovery
  discoverServices(): Promise<ServiceDiscoveryResult>;
  
  // Environment adaptation
  adaptToEnvironment(detection: EnvironmentDetection): Promise<AdaptationResult>;
}

interface PortDetectionResult {
  detectedPort: number | null;
  portsChecked: number[];
  responseTime: number;
  serviceInfo?: ServiceInfo;
}

interface ServiceInfo {
  name: string;
  version?: string;
  healthy: boolean;
  capabilities: string[];
}

interface ServiceDiscoveryResult {
  backend: ServiceInfo | null;
  frontend: ServiceInfo | null;
  additionalServices: ServiceInfo[];
  discoveryTime: number;
}

interface EnvironmentDetection {
  services: ServiceDiscoveryResult;
  ports: { [service: string]: number };
  configuration: EnvironmentConfiguration;
  capabilities: string[];
}

interface AdaptationResult {
  adapted: boolean;
  changes: ConfigurationChange[];
  newConfiguration: EnvironmentConfiguration;
  adaptationTime: number;
}

interface ConfigurationChange {
  component: string;
  property: string;
  oldValue: any;
  newValue: any;
  reason: string;
}
```

---

## 7. Quality Gate Integration Interface

### Quality Assurance Integration

```typescript
interface QualityGateIntegration {
  // Quality gate execution
  executeQualityGate(gate: QualityGate, context: QualityContext): Promise<QualityResult>;
  
  // Gate orchestration
  executeAllGates(context: QualityContext): Promise<QualityGateResults>;
  
  // Quality metrics
  calculateQualityMetrics(results: QualityGateResults): QualityMetrics;
  
  // Continuous validation
  enableContinuousValidation(interval: number): void;
  disableContinuousValidation(): void;
}

interface QualityGate {
  name: string;
  description: string;
  validator: (context: QualityContext) => Promise<QualityResult>;
  required: boolean;         // Is this gate mandatory?
  timeout: number;           // Gate execution timeout
  dependencies: string[];    // Other gates this depends on
}

interface QualityContext {
  testResults: TestResult[];
  todoList: TodoItem[];
  performanceMetrics: PerformanceMetrics;
  infrastructureStatus: InfrastructureStatus;
  executionMethod: TestMethod;
  timestamp: Date;
}

interface QualityResult {
  gateName: string;
  passed: boolean;
  score: number;             // 0-100 quality score
  details: QualityDetails;
  executionTime: number;
  timestamp: Date;
}

interface QualityDetails {
  checks: QualityCheck[];
  summary: string;
  recommendations: string[];
  criticalIssues: string[];
}

interface QualityCheck {
  name: string;
  passed: boolean;
  expected: any;
  actual: any;
  weight: number;            // Weight in overall score calculation
}

interface QualityGateResults {
  overallPassed: boolean;
  overallScore: number;
  gateResults: QualityResult[];
  executionTime: number;
  criticalFailures: string[];
}
```

### Testing Integrity Validation Interface

```typescript
interface TestingIntegrityIntegration {
  // Integrity validation methods
  validateTestingIntegrity(context: IntegrityContext): Promise<IntegrityResult>;
  
  // Specific integrity checks
  validateTodoListIntegrity(todoList: TodoItem[]): IntegrityCheckResult;
  validateExecutionIntegrity(testResults: TestResult[]): IntegrityCheckResult;
  validateReportIntegrity(reportContent: string, testResults: TestResult[]): IntegrityCheckResult;
  
  // Prevention mechanisms
  preventFalseCompletionReporting(): boolean;
  requireActualExecutionEvidence(): boolean;
  enforceSequentialValidation(): boolean;
}

interface IntegrityContext {
  todoList: TodoItem[];
  testResults: TestResult[];
  executionMethod: TestMethod;
  reportContent?: string;
  executionEvidence: ExecutionEvidence[];
}

interface IntegrityResult {
  integrityMaintained: boolean;
  violationsDetected: IntegrityViolation[];
  integrityScore: number;    // 0-100 integrity score
  recommendations: string[];
  enforcementActions: EnforcementAction[];
}

interface IntegrityViolation {
  type: ViolationType;
  severity: 'critical' | 'major' | 'minor';
  description: string;
  evidence: string;
  correctiveAction: string;
}

enum ViolationType {
  FALSE_COMPLETION = 'false_completion',
  MISSING_EVIDENCE = 'missing_evidence', 
  INCONSISTENT_DATA = 'inconsistent_data',
  PREMATURE_REPORTING = 'premature_reporting',
  FABRICATED_RESULTS = 'fabricated_results'
}

interface EnforcementAction {
  action: 'reject' | 'correct' | 'warn' | 'log';
  target: string;            // What to act upon
  description: string;       // What action will be taken
  automatic: boolean;        // Can be performed automatically?
}

interface IntegrityCheckResult {
  checkName: string;
  passed: boolean;
  issues: IntegrityViolation[];
  score: number;
  checkTime: number;
}
```

---

## 8. Claude Code Platform Integration

### Command System Integration Interface

```typescript
interface ClaudeCodeIntegration {
  // Command lifecycle management
  registerCommand(command: SlashCommand): Promise<boolean>;
  validateCommandStructure(command: SlashCommand): ValidationResult;
  
  // Execution coordination
  coordinateExecution(commandName: string, args: string[]): Promise<ExecutionResult>;
  
  // Tool integration
  validateToolPermissions(permissions: ToolPermission[]): PermissionResult;
  executeWithTools(toolSequence: ToolExecution[]): Promise<ToolExecutionResult>;
}

interface SlashCommand {
  name: string;              // Command name without leading slash
  filePath: string;          // Path to command definition file
  frontmatter: CommandFrontmatter;
  content: string;           // Command content body
  lastModified: Date;
}

interface CommandFrontmatter {
  allowedTools: string[];
  description: string;
  argumentHint: string;
  version?: string;
  author?: string;
  tags?: string[];
}

interface ToolPermission {
  tool: string;              // Tool name
  permissions: string[];     // Specific permissions granted
  justification: string;     // Why this permission is needed
}

interface ToolExecution {
  tool: string;
  action: string;
  parameters: Record<string, any>;
  timeout?: number;
  retryPolicy?: RetryPolicy;
}

interface ToolExecutionResult {
  success: boolean;
  results: ToolResult[];
  totalTime: number;
  errors?: ExecutionError[];
}

interface ToolResult {
  tool: string;
  action: string;
  success: boolean;
  result: any;
  executionTime: number;
  error?: string;
}
```

### Argument Processing Integration

```typescript
interface ArgumentProcessingIntegration {
  // Argument parsing and validation
  parseArguments(rawArgs: string, hint: string): ParsedArguments;
  validateArguments(args: ParsedArguments, command: SlashCommand): ArgumentValidation;
  
  // Context integration
  integrateWithContext(args: ParsedArguments, context: ExecutionContext): ContextualizedArguments;
  
  // Default handling
  applyDefaults(args: ParsedArguments, defaults: ArgumentDefaults): ParsedArguments;
}

interface ParsedArguments {
  raw: string;               // Original argument string
  parsed: Record<string, any>; // Parsed argument values
  recognized: boolean;       // Were arguments recognized?
  errors: string[];          // Parsing errors if any
}

interface ArgumentValidation {
  valid: boolean;
  validatedArgs: Record<string, any>;
  validationErrors: ValidationError[];
  suggestions: string[];     // Suggested corrections
}

interface ContextualizedArguments {
  arguments: Record<string, any>;
  context: ExecutionContext;
  environmentAdaptations: EnvironmentAdaptation[];
}

interface ArgumentDefaults {
  testFilter: string;        // Default test filter
  method: TestMethod;        // Default execution method
  timeout: number;           // Default timeout
  reportFormat: string;      // Default report format
}

interface EnvironmentAdaptation {
  property: string;
  adaptedValue: any;
  originalValue: any;
  reason: string;
}
```

---

This comprehensive Integration Interface Definitions document provides all necessary APIs and interfaces for seamless system integration, ensuring robust data flow, consistent error handling, and maintainable architecture across all components of the Playwright testing slash commands system.