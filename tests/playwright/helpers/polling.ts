/**
 * Auto-Retry Response Detection for Playwright CLI Tests
 *
 * Implements intelligent two-phase detection to replace 30-second polling:
 * Phase 1: Detect ANY response completion, Phase 2: Validate content
 * Provides immediate detection and timeout handling
 *
 * @fileoverview Auto-retry utilities for financial data response detection
 */

import { Page, Locator } from '@playwright/test';
import {
  detectResponseWithAutoRetry,
  AutoRetryResult,
  AutoRetryConfig,
  createTestSpecificConfig,
  DEFAULT_AUTO_RETRY_CONFIG
} from './auto-retry';
import { validateResponseByTestName, TestValidationResult } from './response-validators';

/**
 * Performance classification based on response timing
 */
export enum PerformanceClassification {
  SUCCESS = 'SUCCESS',           // < 45 seconds
  SLOW_PERFORMANCE = 'SLOW_PERFORMANCE', // 45-120 seconds  
  TIMEOUT = 'TIMEOUT'            // > 120 seconds
}

/**
 * Result interface for auto-retry operations (enhanced from polling)
 */
export interface PollingResult {
  success: boolean;
  responseTime: number;
  classification: PerformanceClassification;
  responseContent?: string;
  error?: string;
  // Enhanced auto-retry specific fields
  phase1Time?: number;
  phase2Time?: number;
  validationResult?: TestValidationResult;
  detectionMethod?: string;
}

/**
 * Configuration for polling operations
 */
export interface PollingConfig {
  pollingIntervalMs: number;    // Default: 30000ms (30 seconds)
  maxTimeoutMs: number;         // Default: 120000ms (120 seconds)
  successThresholdMs: number;   // Default: 45000ms (45 seconds)
  elementSelector?: string;     // Optional specific element to monitor
  contentMatcher?: RegExp;      // Optional content validation pattern
}

/**
 * Default polling configuration following test specifications
 */
export const DEFAULT_POLLING_CONFIG: PollingConfig = {
  pollingIntervalMs: 30000,     // 30-second polling intervals
  maxTimeoutMs: 120000,         // 120-second maximum timeout
  successThresholdMs: 45000,    // 45-second success threshold
};

/**
 * Auto-retry response detection to replace 30-second polling
 *
 * @param page - Playwright page instance
 * @param config - Polling configuration (converted to auto-retry)
 * @param testName - Optional test name for specific validation
 * @returns Promise<PollingResult> - Result with timing and classification
 */
export async function pollForResponse(
  page: Page,
  config: PollingConfig = DEFAULT_POLLING_CONFIG,
  testName?: string
): Promise<PollingResult> {

  console.log(`[AUTO-RETRY] Starting intelligent detection (max ${config.maxTimeoutMs}ms)`);
  console.log(`[AUTO-RETRY] Test: ${testName || 'generic'}`);

  // Convert legacy polling config to auto-retry config
  const autoRetryConfig: AutoRetryConfig = {
    maxTimeoutMs: config.maxTimeoutMs,
    phase1Methods: testName ?
      createTestSpecificConfig(getTestType(testName), config.maxTimeoutMs).phase1Methods :
      DEFAULT_AUTO_RETRY_CONFIG.phase1Methods,
    enablePhase2Validation: true
  };

  try {
    // Execute two-phase auto-retry detection
    const autoRetryResult = await detectResponseWithAutoRetry(page, autoRetryConfig);

    let validationResult: TestValidationResult | undefined;

    // If we have test name and response content, validate specifically
    if (testName && autoRetryResult.responseContent && autoRetryResult.success) {
      validationResult = validateResponseByTestName(testName, autoRetryResult.responseContent);
      console.log(`[AUTO-RETRY] Validation: ${validationResult.status} for ${testName}`);

      if (validationResult.status === 'FAIL') {
        console.log(`[AUTO-RETRY] Validation FAILED: ${validationResult.failureReasons.join(', ')}`);
      }
    }

    // Classify performance using existing logic
    const classification = classifyPerformance(autoRetryResult.responseTime, config);

    console.log(`[AUTO-RETRY] ${autoRetryResult.success ? 'SUCCESS' : 'FAILED'}: ` +
               `Total: ${autoRetryResult.responseTime}ms, ` +
               `Phase1: ${autoRetryResult.phase1Time}ms, ` +
               `Phase2: ${autoRetryResult.phase2Time}ms (${classification})`);

    return {
      success: autoRetryResult.success && (validationResult?.status !== 'FAIL'),
      responseTime: autoRetryResult.responseTime,
      classification,
      responseContent: autoRetryResult.responseContent,
      error: autoRetryResult.error,
      phase1Time: autoRetryResult.phase1Time,
      phase2Time: autoRetryResult.phase2Time,
      validationResult,
      detectionMethod: 'auto-retry-two-phase'
    };

  } catch (error) {
    const errorTime = Date.now();
    console.log(`[AUTO-RETRY] EXCEPTION: ${error}`);

    return {
      success: false,
      responseTime: config.maxTimeoutMs,
      classification: PerformanceClassification.TIMEOUT,
      error: String(error),
      detectionMethod: 'auto-retry-two-phase'
    };
  }
}

/**
 * Helper function to determine test type for auto-retry configuration
 */
function getTestType(testName: string): 'market-status' | 'ticker-analysis' | 'button-template' {
  const upperName = testName.toUpperCase();

  if (upperName.includes('B001') || upperName.includes('MARKET-STATUS')) {
    return 'market-status';
  }

  if (upperName.includes('B002') || upperName.includes('B003') ||
      upperName.includes('B004') || upperName.includes('B005') ||
      upperName.includes('NVDA') || upperName.includes('SPY') ||
      upperName.includes('GME') || upperName.includes('TICKER')) {
    return 'ticker-analysis';
  }

  if (upperName.includes('B007') || upperName.includes('B008') ||
      upperName.includes('B009') || upperName.includes('BUTTON') ||
      upperName.includes('SNAPSHOT') || upperName.includes('SUPPORT') ||
      upperName.includes('TECHNICAL')) {
    return 'button-template';
  }

  return 'ticker-analysis'; // Default fallback
}

/**
 * DEPRECATED: Legacy detection function - kept for compatibility
 * Use auto-retry detection instead
 */
async function detectFinancialResponse(
  page: Page,
  config: PollingConfig
): Promise<{found: boolean, content?: string}> {
  console.log(`[DEPRECATED] detectFinancialResponse called - use auto-retry instead`);

  // Fallback to simple content check
  try {
    const responseContent = await page.textContent('body') || '';
    const hasFinancialContent = containsFinancialIndicators(responseContent);

    return {
      found: hasFinancialContent && responseContent.length > 50,
      content: responseContent
    };
  } catch (error) {
    return { found: false };
  }
}

/**
 * Check if content contains financial indicators
 * 
 * @param content - Text content to validate
 * @returns boolean - True if financial indicators found
 */
function containsFinancialIndicators(content: string): boolean {
  const financialKeywords = [
    'stock', 'price', 'volume', 'market cap', 'trading',
    'NVDA', 'AAPL', 'MSFT', 'GOOGL', 'TSLA', // Common tickers
    'bullish', 'bearish', 'buy', 'sell',
    'earnings', 'revenue', 'profit', 'loss',
    'analysis', 'recommendation'
  ];
  
  const contentLower = content.toLowerCase();
  
  // Must contain at least 2 financial keywords to be valid
  const matchCount = financialKeywords.filter(keyword => 
    contentLower.includes(keyword)
  ).length;
  
  return matchCount >= 2;
}

/**
 * Classify performance based on response timing
 * 
 * @param responseTime - Time in milliseconds
 * @param config - Polling configuration  
 * @returns PerformanceClassification - Performance category
 */
export function classifyPerformance(
  responseTime: number, 
  config: PollingConfig = DEFAULT_POLLING_CONFIG
): PerformanceClassification {
  
  if (responseTime <= config.successThresholdMs) {
    return PerformanceClassification.SUCCESS;
  } else if (responseTime <= config.maxTimeoutMs) {
    return PerformanceClassification.SLOW_PERFORMANCE;
  } else {
    return PerformanceClassification.TIMEOUT;
  }
}

/**
 * Poll for specific element visibility with early detection
 * 
 * @param page - Playwright page instance
 * @param selector - Element selector to monitor
 * @param config - Polling configuration
 * @returns Promise<PollingResult> - Result with timing and classification
 */
export async function pollForElement(
  page: Page,
  selector: string,
  config: PollingConfig = DEFAULT_POLLING_CONFIG
): Promise<PollingResult> {
  
  const elementConfig = {
    ...config,
    elementSelector: selector
  };
  
  return pollForResponse(page, elementConfig);
}

/**
 * Poll for text content matching a pattern
 * 
 * @param page - Playwright page instance
 * @param pattern - RegExp pattern to match
 * @param config - Polling configuration
 * @returns Promise<PollingResult> - Result with timing and classification
 */
export async function pollForTextContent(
  page: Page,
  pattern: RegExp,
  config: PollingConfig = DEFAULT_POLLING_CONFIG
): Promise<PollingResult> {
  
  const textConfig = {
    ...config,
    contentMatcher: pattern
  };
  
  return pollForResponse(page, textConfig);
}

/**
 * Utility function to wait for any of multiple conditions
 * 
 * @param page - Playwright page instance
 * @param conditions - Array of polling configurations to check
 * @returns Promise<PollingResult> - Result from first successful condition
 */
export async function pollForAnyCondition(
  page: Page,
  conditions: Array<Partial<PollingConfig>>
): Promise<PollingResult> {
  
  const promises = conditions.map(condition => 
    pollForResponse(page, { ...DEFAULT_POLLING_CONFIG, ...condition })
  );
  
  try {
    const result = await Promise.race(promises);
    return result;
  } catch (error) {
    return {
      success: false,
      responseTime: DEFAULT_POLLING_CONFIG.maxTimeoutMs,
      classification: PerformanceClassification.TIMEOUT,
      error: `All conditions failed: ${error}`
    };
  }
}