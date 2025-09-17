/**
 * Test Helpers for Playwright CLI Tests
 * 
 * Implements browser session management and message handling functionality
 * Supports single browser session protocol and performance timing
 * 
 * @fileoverview Core test utilities for browser session management and UI interactions
 */

import { Page, Browser, BrowserContext, expect } from '@playwright/test';
import { pollForResponse, PollingResult, PerformanceClassification } from './polling';
import { autoNavigateToFrontend, validateSystemReadiness, DEFAULT_PORT_CONFIG } from './port-detection';

/**
 * Test execution result interface
 */
export interface TestExecutionResult {
  success: boolean;
  responseTime: number;
  classification: PerformanceClassification;
  testName: string;
  input?: string;
  responseContent?: string;
  error?: string;
  screenshot?: string;
}

/**
 * Browser session configuration
 */
export interface BrowserSessionConfig {
  headless: boolean;
  viewport: { width: number; height: number };
  timeout: number;
  screenshotOnFailure: boolean;
  videoRecording: boolean;
  slowMo: number;
}

/**
 * Default browser session configuration
 */
export const DEFAULT_SESSION_CONFIG: BrowserSessionConfig = {
  headless: true, // Can be overridden for debugging
  viewport: { width: 1280, height: 720 },
  timeout: 120000, // 120-second timeout
  screenshotOnFailure: true,
  videoRecording: true,
  slowMo: 0, // No artificial delays for accurate performance measurement
};

/**
 * Message input configuration for testing
 */
export interface MessageInputConfig {
  inputSelector: string;
  submitSelector: string;
  inputMethod: 'type' | 'fill';
  submitMethod: 'click' | 'keyboard';
  clearBeforeInput: boolean;
  waitForFocus: boolean;
}

/**
 * Default message input configuration for React frontend
 */
export const DEFAULT_INPUT_CONFIG: MessageInputConfig = {
  inputSelector: 'textarea[placeholder*="message"], input[placeholder*="message"], textarea, .chat-input textarea, .message-input textarea',
  submitSelector: 'button[type="submit"], .send-button, button:has-text("Send"), [data-testid="send-button"]',
  inputMethod: 'type',
  submitMethod: 'click',
  clearBeforeInput: true,
  waitForFocus: true,
};

/**
 * Browser session manager for single session testing
 */
export class BrowserSessionManager {
  private browser: Browser | null = null;
  private context: BrowserContext | null = null;
  private page: Page | null = null;
  private sessionStartTime: number = 0;
  private testResults: TestExecutionResult[] = [];
  
  constructor(private config: BrowserSessionConfig = DEFAULT_SESSION_CONFIG) {}
  
  /**
   * Initialize browser session (called once per test suite)
   */
  async initializeSession(browser: Browser): Promise<Page> {
    console.log(`[SESSION] Initializing single browser session...`);
    
    this.browser = browser;
    this.sessionStartTime = Date.now();
    
    // Create browser context with configuration
    this.context = await this.browser.newContext({
      viewport: this.config.viewport,
      recordVideo: this.config.videoRecording ? { dir: 'test-results/videos/' } : undefined,
    });
    
    // Create single page for entire test session
    this.page = await this.context.newPage();
    
    // Set default timeout
    this.page.setDefaultTimeout(this.config.timeout);
    
    // Validate system readiness
    const systemStatus = await validateSystemReadiness();
    if (!systemStatus.ready) {
      throw new Error(`System not ready for testing: ${systemStatus.errors.join(', ')}`);
    }
    
    // Navigate to frontend
    await autoNavigateToFrontend(this.page);
    
    console.log(`[SESSION] Browser session initialized successfully`);
    return this.page;
  }
  
  /**
   * Get current page instance (must call initializeSession first)
   */
  getPage(): Page {
    if (!this.page) {
      throw new Error('Browser session not initialized. Call initializeSession first.');
    }
    return this.page;
  }
  
  /**
   * Add test result to session history
   */
  addTestResult(result: TestExecutionResult): void {
    this.testResults.push(result);
    console.log(`[SESSION] Test result added: ${result.testName} - ${result.classification} (${result.responseTime}ms)`);
  }
  
  /**
   * Get session statistics
   */
  getSessionStats(): {
    totalTests: number;
    successCount: number;
    slowCount: number;
    timeoutCount: number;
    sessionDuration: number;
    averageResponseTime: number;
  } {
    const totalTests = this.testResults.length;
    const successCount = this.testResults.filter(r => r.classification === PerformanceClassification.SUCCESS).length;
    const slowCount = this.testResults.filter(r => r.classification === PerformanceClassification.SLOW_PERFORMANCE).length;
    const timeoutCount = this.testResults.filter(r => r.classification === PerformanceClassification.TIMEOUT).length;
    const sessionDuration = Date.now() - this.sessionStartTime;
    const averageResponseTime = totalTests > 0 
      ? this.testResults.reduce((sum, r) => sum + r.responseTime, 0) / totalTests 
      : 0;
    
    return {
      totalTests,
      successCount,
      slowCount,
      timeoutCount,
      sessionDuration,
      averageResponseTime
    };
  }
  
  /**
   * Cleanup session (called once at end of test suite)
   */
  async cleanup(): Promise<void> {
    console.log(`[SESSION] Cleaning up browser session...`);
    
    const stats = this.getSessionStats();
    console.log(`[SESSION] Final stats:`, stats);
    
    if (this.context) {
      await this.context.close();
    }
    
    // Note: Browser is closed by Playwright automatically
    console.log(`[SESSION] Session cleanup complete`);
  }
}

/**
 * Send message and wait for response with auto-retry detection
 */
export async function sendMessageAndWaitForResponse(
  page: Page,
  message: string,
  testName: string,
  inputConfig: MessageInputConfig = DEFAULT_INPUT_CONFIG
): Promise<TestExecutionResult> {

  console.log(`[TEST-HELPER] Starting auto-retry test: ${testName}`);
  console.log(`[TEST-HELPER] Input message: "${message}"`);

  const startTime = Date.now();

  try {
    // Step 1: Send the message
    await sendMessage(page, message, inputConfig);

    // Step 2: Wait for response with auto-retry detection
    const pollingResult = await pollForResponse(page, undefined, testName);

    const result: TestExecutionResult = {
      success: pollingResult.success,
      responseTime: pollingResult.responseTime,
      classification: pollingResult.classification,
      testName,
      input: message,
      responseContent: pollingResult.responseContent,
      error: pollingResult.error
    };

    // Enhanced logging for auto-retry
    if (pollingResult.phase1Time && pollingResult.phase2Time) {
      console.log(`[TEST-HELPER] Auto-retry phases: Phase1=${pollingResult.phase1Time}ms, Phase2=${pollingResult.phase2Time}ms`);
    }

    if (pollingResult.validationResult) {
      console.log(`[TEST-HELPER] Content validation: ${pollingResult.validationResult.status}`);
      if (pollingResult.validationResult.status === 'FAIL') {
        console.log(`[TEST-HELPER] Validation failures: ${pollingResult.validationResult.failureReasons.join(', ')}`);
      }
    }

    console.log(`[TEST-HELPER] Test completed: ${testName} - ${result.classification} (${result.responseTime}ms)`);

    return result;

  } catch (error) {
    const responseTime = Date.now() - startTime;

    console.log(`[TEST-HELPER] Test failed: ${testName} - Error: ${error}`);

    // Take screenshot on failure if configured
    let screenshot: string | undefined;
    if (DEFAULT_SESSION_CONFIG.screenshotOnFailure) {
      try {
        const screenshotPath = `test-results/failure-${testName}-${Date.now()}.png`;
        await page.screenshot({
          path: screenshotPath,
          fullPage: true
        });
        screenshot = screenshotPath;
      } catch (screenshotError) {
        console.log(`[TEST-HELPER] Screenshot failed:`, screenshotError);
      }
    }

    return {
      success: false,
      responseTime,
      classification: PerformanceClassification.TIMEOUT,
      testName,
      input: message,
      error: String(error),
      screenshot
    };
  }
}

/**
 * Send message to chat interface
 */
export async function sendMessage(
  page: Page,
  message: string,
  config: MessageInputConfig = DEFAULT_INPUT_CONFIG
): Promise<void> {
  
  console.log(`[TEST-HELPER] Sending message: "${message}"`);
  
  // Find input field
  const inputElement = page.locator(config.inputSelector).first();
  
  // Wait for input to be visible and enabled
  await inputElement.waitFor({ state: 'visible', timeout: 10000 });
  
  // Focus on input if required
  if (config.waitForFocus) {
    await inputElement.focus();
  }
  
  // Clear existing content if required
  if (config.clearBeforeInput) {
    await inputElement.clear();
  }
  
  // Input the message
  if (config.inputMethod === 'type') {
    await inputElement.type(message);
  } else {
    await inputElement.fill(message);
  }
  
  // Submit the message
  if (config.submitMethod === 'click') {
    const submitButton = page.locator(config.submitSelector).first();
    await submitButton.waitFor({ state: 'visible', timeout: 5000 });
    await submitButton.click();
  } else {
    // Submit via keyboard (Enter key)
    await inputElement.press('Enter');
  }
  
  console.log(`[TEST-HELPER] Message sent successfully`);
}

/**
 * Wait for page to be in ready state
 */
export async function waitForPageReady(page: Page, timeout: number = 30000): Promise<void> {
  console.log(`[TEST-HELPER] Waiting for page ready state...`);
  
  try {
    // Wait for network to be idle
    await page.waitForLoadState('networkidle', { timeout });
    
    // Additional check for React app to be mounted
    await page.waitForFunction(
      () => {
        // Check if React app is mounted (look for common React indicators)
        return document.querySelector('[data-reactroot], #root > *, .App, .app, main, .container') !== null;
      },
      { timeout: 10000 }
    );
    
    console.log(`[TEST-HELPER] Page is ready`);
    
  } catch (error) {
    console.log(`[TEST-HELPER] Page ready check failed, continuing anyway:`, error);
    // Don't throw - page might still be functional
  }
}

/**
 * Validate page contains expected UI elements
 */
export async function validatePageStructure(page: Page): Promise<{valid: boolean, missingElements: string[]}> {
  console.log(`[TEST-HELPER] Validating page structure...`);
  
  const expectedElements = [
    'textarea, input[type="text"]', // Input field
    'button', // Some kind of button
    'body', // Basic page structure
  ];
  
  const missingElements: string[] = [];
  
  for (const selector of expectedElements) {
    try {
      const element = page.locator(selector).first();
      const isVisible = await element.isVisible({ timeout: 5000 });
      
      if (!isVisible) {
        missingElements.push(selector);
      }
    } catch (error) {
      missingElements.push(selector);
    }
  }
  
  const valid = missingElements.length === 0;
  
  console.log(`[TEST-HELPER] Page structure validation: ${valid ? 'VALID' : 'INVALID'}`);
  if (!valid) {
    console.log(`[TEST-HELPER] Missing elements:`, missingElements);
  }
  
  return { valid, missingElements };
}

/**
 * Clear chat history/interface
 */
export async function clearChatInterface(page: Page): Promise<void> {
  console.log(`[TEST-HELPER] Clearing chat interface...`);
  
  try {
    // Look for clear/reset button
    const clearSelectors = [
      'button:has-text("Clear")',
      'button:has-text("Reset")', 
      '[data-testid="clear-button"]',
      '.clear-chat',
      '.reset-chat'
    ];
    
    for (const selector of clearSelectors) {
      try {
        const clearButton = page.locator(selector);
        const isVisible = await clearButton.isVisible({ timeout: 2000 });
        
        if (isVisible) {
          await clearButton.click();
          console.log(`[TEST-HELPER] Chat cleared using: ${selector}`);
          return;
        }
      } catch (error) {
        // Continue to next selector
      }
    }
    
    // If no clear button found, try refreshing the page
    console.log(`[TEST-HELPER] No clear button found, refreshing page...`);
    await page.reload({ waitUntil: 'networkidle' });
    
  } catch (error) {
    console.log(`[TEST-HELPER] Clear chat interface failed:`, error);
    // Continue anyway - not critical for testing
  }
}

/**
 * Take screenshot with timestamp
 */
export async function takeTimestampedScreenshot(
  page: Page, 
  testName: string, 
  suffix: string = ''
): Promise<string> {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `test-results/screenshot-${testName}-${timestamp}${suffix ? '-' + suffix : ''}.png`;
  
  await page.screenshot({ 
    path: filename,
    fullPage: true 
  });
  
  console.log(`[TEST-HELPER] Screenshot saved: ${filename}`);
  return filename;
}

/**
 * Execute test with comprehensive error handling and reporting
 */
export async function executeTest(
  page: Page,
  testName: string,
  message: string,
  sessionManager?: BrowserSessionManager
): Promise<TestExecutionResult> {
  
  console.log(`[TEST-HELPER] === EXECUTING TEST: ${testName} ===`);
  
  // Take "before" screenshot
  await takeTimestampedScreenshot(page, testName, 'before');
  
  // Execute the test
  const result = await sendMessageAndWaitForResponse(page, message, testName);
  
  // Take "after" screenshot
  await takeTimestampedScreenshot(page, testName, 'after');
  
  // Add to session manager if provided
  if (sessionManager) {
    sessionManager.addTestResult(result);
  }
  
  console.log(`[TEST-HELPER] === TEST COMPLETED: ${testName} - ${result.success ? 'SUCCESS' : 'FAILED'} ===`);
  
  return result;
}

/**
 * Batch execute multiple tests in single browser session
 */
export async function executeBatchTests(
  page: Page,
  tests: Array<{name: string, message: string}>,
  sessionManager?: BrowserSessionManager
): Promise<TestExecutionResult[]> {
  
  console.log(`[TEST-HELPER] === BATCH EXECUTION: ${tests.length} tests ===`);
  
  const results: TestExecutionResult[] = [];
  
  for (let i = 0; i < tests.length; i++) {
    const test = tests[i];
    
    console.log(`[TEST-HELPER] --- Batch test ${i + 1}/${tests.length}: ${test.name} ---`);
    
    // Small delay between tests to ensure UI stability
    if (i > 0) {
      await page.waitForTimeout(2000);
    }
    
    const result = await executeTest(page, test.name, test.message, sessionManager);
    results.push(result);
    
    // Continue with next test regardless of individual test results
  }
  
  console.log(`[TEST-HELPER] === BATCH EXECUTION COMPLETED ===`);
  
  return results;
}