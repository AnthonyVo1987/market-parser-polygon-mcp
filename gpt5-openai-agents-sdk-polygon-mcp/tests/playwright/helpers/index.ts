/**
 * Playwright Test Helpers - Main Export Index
 * 
 * Centralized exports for all Playwright CLI test utilities
 * Provides comprehensive testing infrastructure for financial data responses
 * 
 * @fileoverview Main export file for Playwright test helper utilities
 */

// Polling utilities - 30-second polling with 120s timeout
export {
  pollForResponse,
  pollForElement,
  pollForTextContent,
  pollForAnyCondition,
  classifyPerformance,
  PerformanceClassification,
  DEFAULT_POLLING_CONFIG,
  type PollingResult,
  type PollingConfig
} from './polling';

// Port detection utilities - Dynamic port discovery and health checks
export {
  findFrontendServer,
  verifyBackendServer,
  getSystemServerStatus,
  waitForServerReady,
  autoNavigateToFrontend,
  validateSystemReadiness,
  getTestBaseUrl,
  isPortInUse,
  DEFAULT_PORT_CONFIG,
  type ServerStatus,
  type PortDetectionConfig
} from './port-detection';

// Test execution helpers - Browser session management and message handling
export {
  BrowserSessionManager,
  sendMessageAndWaitForResponse,
  sendMessage,
  waitForPageReady,
  validatePageStructure,
  clearChatInterface,
  takeTimestampedScreenshot,
  executeTest,
  executeBatchTests,
  DEFAULT_SESSION_CONFIG,
  DEFAULT_INPUT_CONFIG,
  type TestExecutionResult,
  type BrowserSessionConfig,
  type MessageInputConfig
} from './test-helpers';

// Response validation utilities - Emoji indicators and content verification
export {
  validateFinancialResponse,
  validateKeyTakeawaysSection,
  validateEmojiIndicators,
  validateFinancialContent,
  validateTickerResponse,
  validateEmptyInputHandling,
  extractTickers,
  getValidationSummary,
  FINANCIAL_EMOJIS,
  COMMON_TICKERS,
  FINANCIAL_KEYWORDS,
  type ValidationResult,
  type TickerValidationConfig
} from './validation';

// Button interaction utilities - Financial analysis button testing
export {
  clickButtonAndWaitForResponse,
  inputTicker,
  clickButton,
  validateButtonState,
  detectProcessingState,
  executeMultiButtonTest,
  validateButtonAccessibility,
  generateButtonTestReport,
  ButtonType,
  BUTTON_SELECTORS,
  DEFAULT_BUTTON_STATE_CONFIG,
  type ButtonInteractionResult,
  type ButtonStateConfig
} from './button-helpers';

/**
 * Comprehensive test suite configuration
 * Combines all helper configurations for easy setup
 */
export const COMPREHENSIVE_TEST_CONFIG = {
  polling: {
    pollingIntervalMs: 30000,
    maxTimeoutMs: 120000,
    successThresholdMs: 45000,
  },
  portDetection: {
    frontendPortRange: { start: 3000, end: 3010 },
    backendPort: 8000,
    timeoutMs: 10000,
    healthCheckPath: '/',
    retryAttempts: 3,
    retryDelayMs: 2000,
  },
  browserSession: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    timeout: 120000,
    screenshotOnFailure: true,
    videoRecording: true,
    slowMo: 0,
  },
  messageInput: {
    inputSelector: 'textarea[placeholder*="message"], input[placeholder*="message"], textarea, .chat-input textarea, .message-input textarea',
    submitSelector: 'button[type="submit"], .send-button, button:has-text("Send"), [data-testid="send-button"]',
    inputMethod: 'type' as const,
    submitMethod: 'click' as const,
    clearBeforeInput: true,
    waitForFocus: true,
  },
  
  // Button interaction configuration
  buttonInteraction: {
    clickTimeout: 5000,          // 5-second timeout for button clicks
    stateValidationTimeout: 5000, // 5-second timeout for state validation
    processingDetectionDelay: 1000, // 1-second delay after click to detect processing
    multiButtonDelay: 3000,      // 3-second delay between multi-button tests
    accessibilityChecks: true,   // Enable accessibility validation
  },
  
  // Common test timeouts
  timeouts: {
    test: 120000,        // 120-second test timeout
    polling: 30000,      // 30-second polling interval
    navigation: 30000,   // 30-second navigation timeout
    element: 10000,      // 10-second element timeout
    button: 5000,        // 5-second button interaction timeout
  },
  
  // Performance thresholds
  performance: {
    success: 45000,      // < 45 seconds = SUCCESS
    slowPerformance: 120000, // 45-120 seconds = SLOW_PERFORMANCE
    timeout: 120000      // > 120 seconds = TIMEOUT
  },
  
  // Common test data
  testData: {
    validTickers: ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'SPY', 'GME'],
    testMessages: [
      'tell me about NVDA stock',
      'analyze AAPL performance',
      'what is MSFT doing today'
    ],
    emptyInputs: ['', '   ', '\n', '\t'],
    buttonTestTickers: ['NVDA', 'AAPL', 'GME'], // Tickers for button testing
    buttonCombinations: [
      ['STOCK_SNAPSHOT'],
      ['SUPPORT_RESISTANCE'], 
      ['TECHNICAL_ANALYSIS'],
      ['STOCK_SNAPSHOT', 'SUPPORT_RESISTANCE'],
      ['STOCK_SNAPSHOT', 'TECHNICAL_ANALYSIS'],
      ['SUPPORT_RESISTANCE', 'TECHNICAL_ANALYSIS']
    ]
  }
};

/**
 * Quick setup function for basic test suite
 * 
 * @param browser - Playwright browser instance
 * @returns Promise<{page: Page, sessionManager: BrowserSessionManager}> - Ready test environment
 */
export async function setupBasicTestSuite(browser: any) {
  // Import required classes and functions here to avoid circular dependencies
  const { BrowserSessionManager } = await import('./test-helpers');
  const { validateSystemReadiness } = await import('./port-detection');
  
  const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
  const page = await sessionManager.initializeSession(browser);
  
  // Validate system readiness
  const systemStatus = await validateSystemReadiness(COMPREHENSIVE_TEST_CONFIG.portDetection);
  if (!systemStatus.ready) {
    throw new Error(`System not ready: ${systemStatus.errors.join(', ')}`);
  }
  
  return { page, sessionManager };
}

/**
 * Complete test execution workflow
 * Combines all helpers for end-to-end test execution
 * 
 * @param browser - Playwright browser instance
 * @param testName - Name of the test
 * @param message - Message to send
 * @param expectedTicker - Expected ticker symbol (optional)
 * @returns Promise<{execution: TestExecutionResult, validation: ValidationResult}> - Complete test result
 */
export async function executeCompleteTest(
  browser: any,
  testName: string,
  message: string,
  expectedTicker?: string
) {
  // Import required functions
  const { sendMessageAndWaitForResponse } = await import('./test-helpers');
  const { validateFinancialResponse } = await import('./validation');
  
  // Setup test environment
  const { page, sessionManager } = await setupBasicTestSuite(browser);
  
  try {
    // Execute test with message
    const executionResult = await sendMessageAndWaitForResponse(page, message, testName);
    
    // Validate response if successful
    let validationResult: any;
    if (executionResult.success) {
      validationResult = await validateFinancialResponse(page, expectedTicker);
    } else {
      // Create empty validation result for failed tests
      validationResult = {
        isValid: false,
        hasKeyTakeaways: false,
        hasEmojiIndicators: false,
        hasFinancialContent: false,
        detectedEmojis: [],
        detectedTickers: [],
        detectedKeywords: [],
        contentLength: 0,
        validationErrors: ['Test execution failed'],
        responseContent: undefined
      };
    }
    
    return {
      execution: executionResult,
      validation: validationResult
    };
    
  } finally {
    // Clean up session
    await sessionManager.cleanup();
  }
}

/**
 * Batch test execution with comprehensive reporting
 * 
 * @param browser - Playwright browser instance
 * @param tests - Array of test configurations
 * @returns Promise<Array<{execution: TestExecutionResult, validation: ValidationResult}>> - All test results
 */
export async function executeBatchTestSuite(
  browser: any,
  tests: Array<{name: string, message: string, expectedTicker?: string}>
) {
  // Import required functions
  const { sendMessageAndWaitForResponse } = await import('./test-helpers');
  const { validateFinancialResponse } = await import('./validation');
  
  const { page, sessionManager } = await setupBasicTestSuite(browser);
  
  const results: Array<{execution: any, validation: any}> = [];
  
  try {
    for (const test of tests) {
      console.log(`[BATCH] Executing test: ${test.name}`);
      
      // Execute individual test
      const executionResult = await sendMessageAndWaitForResponse(page, test.message, test.name);
      
      // Validate response
      let validationResult: any;
      if (executionResult.success) {
        validationResult = await validateFinancialResponse(page, test.expectedTicker);
      } else {
        validationResult = {
          isValid: false,
          hasKeyTakeaways: false,
          hasEmojiIndicators: false,
          hasFinancialContent: false,
          detectedEmojis: [],
          detectedTickers: [],
          detectedKeywords: [],
          contentLength: 0,
          validationErrors: ['Test execution failed'],
          responseContent: undefined
        };
      }
      
      results.push({
        execution: executionResult,
        validation: validationResult
      });
      
      // Small delay between tests
      await page.waitForTimeout(2000);
    }
    
    return results;
    
  } finally {
    await sessionManager.cleanup();
  }
}

/**
 * Generate comprehensive test report
 * 
 * @param results - Array of test results
 * @returns Object with detailed test report
 */
export async function generateTestReport(
  results: Array<{execution: any, validation: any}>
) {
  const totalTests = results.length;
  const successfulExecutions = results.filter(r => r.execution.success).length;
  const validResponses = results.filter(r => r.validation.isValid).length;
  
  const executionSuccessRate = totalTests > 0 ? (successfulExecutions / totalTests) * 100 : 0;
  const validationSuccessRate = totalTests > 0 ? (validResponses / totalTests) * 100 : 0;
  
  // Performance classification breakdown
  const { PerformanceClassification } = await import('./polling');
  const performanceBreakdown = {
    success: results.filter(r => r.execution.classification === PerformanceClassification.SUCCESS).length,
    slowPerformance: results.filter(r => r.execution.classification === PerformanceClassification.SLOW_PERFORMANCE).length,
    timeout: results.filter(r => r.execution.classification === PerformanceClassification.TIMEOUT).length
  };
  
  // Average response time
  const responseTimes = results.map(r => r.execution.responseTime);
  const averageResponseTime = responseTimes.length > 0 
    ? responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length 
    : 0;
  
  // Validation summary (simplified for now)
  const validationSummary = {
    totalTests,
    validCount: validResponses,
    invalidCount: totalTests - validResponses,
    successRate: validationSuccessRate
  };
  
  return {
    overview: {
      totalTests,
      successfulExecutions,
      validResponses,
      executionSuccessRate,
      validationSuccessRate,
      averageResponseTime
    },
    performance: {
      breakdown: performanceBreakdown,
      averageResponseTime,
      responseTimes
    },
    validation: validationSummary,
    detailedResults: results
  };
}

/**
 * Export version and configuration info
 */
export const HELPERS_VERSION = '1.0.0';
export const HELPERS_CONFIG = {
  supportedFeatures: [
    '30-second polling methodology',
    '120-second test timeouts',
    'Dynamic port detection (3000-3003+)',
    'Backend health verification (port 8000)',
    'Single browser session management',
    'Financial emoji indicator validation',
    'KEY TAKEAWAYS section detection',
    'Ticker-specific response validation',
    'Performance classification (SUCCESS/SLOW_PERFORMANCE/TIMEOUT)',
    'Comprehensive test reporting',
    'Button interaction testing (Stock Snapshot, Support & Resistance, Technical Analysis)',
    'Button state validation (enabled/disabled/loading/pressed)',
    'Processing state detection',
    'Multi-button interaction testing',
    'Button accessibility validation',
    'Button UI consistency testing'
  ],
  requirements: {
    node: '>=18.0.0',
    playwright: '>=1.40.0',
    browsers: ['chromium'],
    ports: {
      frontend: '3000-3010',
      backend: '8000'
    },
    buttons: {
      types: ['STOCK_SNAPSHOT', 'SUPPORT_RESISTANCE', 'TECHNICAL_ANALYSIS'],
      emojis: ['📈', '🎯', '🔧'],
      maxInteractionTime: '5000ms'
    }
  }
};