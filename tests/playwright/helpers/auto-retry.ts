/**
 * Auto-Retry Detection Module for Playwright Tests
 *
 * Implements two-phase intelligent detection to replace 30-second polling:
 * Phase 1: Detect ANY AI response completion (loading states, response containers)
 * Phase 2: Validate response content against test-specific criteria
 *
 * @fileoverview Core auto-retry utilities for eliminating polling overhead
 */

import { Page, Locator, expect } from '@playwright/test';

/**
 * Auto-retry detection result interface
 */
export interface AutoRetryResult {
  success: boolean;
  responseTime: number;
  responseContent?: string;
  phase1Time: number;  // Time to detect ANY response
  phase2Time: number;  // Time to validate content
  error?: string;
  validationResult?: ValidationResult;
}

/**
 * Validation result for Phase 2 content checking
 */
export interface ValidationResult {
  isValid: boolean;
  hasFinancialContent: boolean;
  hasEmojiIndicators: boolean;
  contentLength: number;
  detectedEmojis: string[];
  detectedTickers: string[];
  errorDetails?: string;
}

/**
 * Configuration for auto-retry detection
 */
export interface AutoRetryConfig {
  maxTimeoutMs: number;           // Maximum total timeout (default: 120000ms)
  phase1Methods: DetectionMethod[]; // Methods to try for Phase 1 detection
  expectTimeout?: number;         // Custom expect timeout (default: uses maxTimeoutMs)
  enablePhase2Validation: boolean; // Whether to run Phase 2 validation
}

/**
 * Detection methods for Phase 1 (ANY response detection)
 */
export enum DetectionMethod {
  LOADING_HIDDEN = 'loading_hidden',          // Wait for loading indicator to disappear
  RESPONSE_VISIBLE = 'response_visible',      // Wait for response container to appear
  MESSAGE_COUNT = 'message_count',            // Wait for message count to increase
  COMPLETION_TEXT = 'completion_text',        // Wait for completion indicator text
  NO_LOADING_CLASS = 'no_loading_class'       // Wait for loading class to be removed
}

/**
 * Default auto-retry configuration
 */
export const DEFAULT_AUTO_RETRY_CONFIG: AutoRetryConfig = {
  maxTimeoutMs: 120000,  // 120-second maximum timeout
  phase1Methods: [
    DetectionMethod.LOADING_HIDDEN,
    DetectionMethod.RESPONSE_VISIBLE,
    DetectionMethod.MESSAGE_COUNT
  ],
  enablePhase2Validation: true
};

/**
 * Main auto-retry function: Two-phase intelligent detection
 *
 * @param page - Playwright page instance
 * @param config - Auto-retry configuration
 * @returns Promise<AutoRetryResult> - Detection and validation results
 */
export async function detectResponseWithAutoRetry(
  page: Page,
  config: AutoRetryConfig = DEFAULT_AUTO_RETRY_CONFIG
): Promise<AutoRetryResult> {

  const startTime = Date.now();
  console.log(`[AUTO-RETRY] Starting two-phase detection (max ${config.maxTimeoutMs}ms)`);

  try {
    // Phase 1: Detect ANY response completion
    const phase1Start = Date.now();
    const responseDetected = await executePhase1Detection(page, config);
    const phase1Time = Date.now() - phase1Start;

    if (!responseDetected.success) {
      return {
        success: false,
        responseTime: Date.now() - startTime,
        phase1Time,
        phase2Time: 0,
        error: responseDetected.error
      };
    }

    console.log(`[AUTO-RETRY] Phase 1 SUCCESS: Response detected in ${phase1Time}ms`);

    // Phase 2: Validate response content (if enabled)
    let validationResult: ValidationResult | undefined;
    let phase2Time = 0;

    if (config.enablePhase2Validation) {
      const phase2Start = Date.now();
      validationResult = await executePhase2Validation(page);
      phase2Time = Date.now() - phase2Start;

      console.log(`[AUTO-RETRY] Phase 2 completed in ${phase2Time}ms - Valid: ${validationResult.isValid}`);
    }

    const totalTime = Date.now() - startTime;

    return {
      success: true,
      responseTime: totalTime,
      phase1Time,
      phase2Time,
      responseContent: responseDetected.content,
      validationResult
    };

  } catch (error) {
    const totalTime = Date.now() - startTime;
    console.log(`[AUTO-RETRY] ERROR: ${error}`);

    return {
      success: false,
      responseTime: totalTime,
      phase1Time: 0,
      phase2Time: 0,
      error: String(error)
    };
  }
}

/**
 * Phase 1: Detect ANY response completion using multiple methods
 */
async function executePhase1Detection(
  page: Page,
  config: AutoRetryConfig
): Promise<{success: boolean, content?: string, error?: string}> {

  const timeout = config.expectTimeout || config.maxTimeoutMs;
  console.log(`[AUTO-RETRY] Phase 1: Trying ${config.phase1Methods.length} detection methods`);

  // Try each detection method
  for (const method of config.phase1Methods) {
    try {
      console.log(`[AUTO-RETRY] Trying detection method: ${method}`);

      switch (method) {
        case DetectionMethod.LOADING_HIDDEN:
          await tryLoadingHiddenDetection(page, timeout);
          break;

        case DetectionMethod.RESPONSE_VISIBLE:
          await tryResponseVisibleDetection(page, timeout);
          break;

        case DetectionMethod.MESSAGE_COUNT:
          await tryMessageCountDetection(page, timeout);
          break;

        case DetectionMethod.COMPLETION_TEXT:
          await tryCompletionTextDetection(page, timeout);
          break;

        case DetectionMethod.NO_LOADING_CLASS:
          await tryNoLoadingClassDetection(page, timeout);
          break;
      }

      // If we reach here, the method succeeded
      console.log(`[AUTO-RETRY] Detection method ${method} succeeded`);

      // Get response content for Phase 2
      const content = await page.textContent('body') || '';
      return { success: true, content };

    } catch (error) {
      console.log(`[AUTO-RETRY] Detection method ${method} failed: ${error}`);
      // Continue to next method
    }
  }

  // All methods failed
  return {
    success: false,
    error: `All ${config.phase1Methods.length} detection methods failed within ${timeout}ms`
  };
}

/**
 * Phase 2: Validate response content for financial data quality
 */
async function executePhase2Validation(page: Page): Promise<ValidationResult> {
  console.log(`[AUTO-RETRY] Phase 2: Validating response content`);

  try {
    // Get the latest response content
    const responseContent = await getLatestResponseContent(page);

    if (!responseContent || responseContent.length === 0) {
      return {
        isValid: false,
        hasFinancialContent: false,
        hasEmojiIndicators: false,
        contentLength: 0,
        detectedEmojis: [],
        detectedTickers: [],
        errorDetails: 'No response content found'
      };
    }

    // Financial content detection
    const hasFinancialContent = detectFinancialContent(responseContent);

    // Emoji indicators detection
    const detectedEmojis = detectFinancialEmojis(responseContent);
    const hasEmojiIndicators = detectedEmojis.length > 0;

    // Ticker detection
    const detectedTickers = detectTickers(responseContent);

    // Overall validation
    const isValid = hasFinancialContent && hasEmojiIndicators && responseContent.length > 50;

    return {
      isValid,
      hasFinancialContent,
      hasEmojiIndicators,
      contentLength: responseContent.length,
      detectedEmojis,
      detectedTickers
    };

  } catch (error) {
    return {
      isValid: false,
      hasFinancialContent: false,
      hasEmojiIndicators: false,
      contentLength: 0,
      detectedEmojis: [],
      detectedTickers: [],
      errorDetails: String(error)
    };
  }
}

/**
 * Detection Method: Wait for loading indicator to disappear
 */
async function tryLoadingHiddenDetection(page: Page, timeout: number): Promise<void> {
  const loadingSelectors = [
    '[data-testid="loading"]',
    '.loading',
    '.loading-spinner',
    '.loader',
    'text=Loading...',
    'text=Thinking...',
    '[aria-label*="loading" i]'
  ];

  for (const selector of loadingSelectors) {
    try {
      const element = page.locator(selector);
      const isVisible = await element.isVisible({ timeout: 1000 });

      if (isVisible) {
        console.log(`[AUTO-RETRY] Found loading indicator: ${selector}, waiting for it to disappear`);
        await expect(element).toBeHidden({ timeout });
        return; // Success
      }
    } catch (error) {
      // Try next selector
    }
  }

  throw new Error('No loading indicators found to monitor');
}

/**
 * Detection Method: Wait for response container to appear
 */
async function tryResponseVisibleDetection(page: Page, timeout: number): Promise<void> {
  const responseSelectors = [
    '.chat-message:last-child',
    '.message:last-child',
    '.ai-response',
    '.response-content',
    '[data-testid="ai-response"]',
    '.chat-response'
  ];

  for (const selector of responseSelectors) {
    try {
      const element = page.locator(selector);
      await expect(element).toBeVisible({ timeout });

      // Additional check: ensure it has meaningful content
      const content = await element.textContent();
      if (content && content.trim().length > 10) {
        console.log(`[AUTO-RETRY] Response container visible with content: ${selector}`);
        return; // Success
      }
    } catch (error) {
      // Try next selector
    }
  }

  throw new Error('No response containers became visible with content');
}

/**
 * Detection Method: Wait for message count to increase
 */
async function tryMessageCountDetection(page: Page, timeout: number): Promise<void> {
  const messageSelectors = [
    '.chat-message',
    '.message',
    '[data-testid*="message"]'
  ];

  for (const selector of messageSelectors) {
    try {
      const messages = page.locator(selector);
      const initialCount = await messages.count();

      console.log(`[AUTO-RETRY] Initial message count (${selector}): ${initialCount}`);

      // Wait for count to increase by at least 1
      await expect(messages).toHaveCount(initialCount + 1, { timeout });

      console.log(`[AUTO-RETRY] Message count increased to: ${initialCount + 1}`);
      return; // Success

    } catch (error) {
      // Try next selector
    }
  }

  throw new Error('No message count increases detected');
}

/**
 * Detection Method: Wait for completion indicator text
 */
async function tryCompletionTextDetection(page: Page, timeout: number): Promise<void> {
  const completionTexts = [
    'Generated with Claude Code',
    'DISCLAIMER',
    '🎯 KEY TAKEAWAYS',
    'Analysis complete'
  ];

  for (const text of completionTexts) {
    try {
      const element = page.locator(`text=${text}`);
      await expect(element).toBeVisible({ timeout });

      console.log(`[AUTO-RETRY] Completion text detected: ${text}`);
      return; // Success

    } catch (error) {
      // Try next text
    }
  }

  throw new Error('No completion indicator texts found');
}

/**
 * Detection Method: Wait for loading class to be removed
 */
async function tryNoLoadingClassDetection(page: Page, timeout: number): Promise<void> {
  const bodyElement = page.locator('body');

  try {
    // Check if body has loading class
    const hasLoadingClass = await bodyElement.evaluate(el =>
      el.classList.contains('loading') ||
      el.classList.contains('is-loading') ||
      el.classList.contains('app-loading')
    );

    if (hasLoadingClass) {
      console.log(`[AUTO-RETRY] Body has loading class, waiting for removal`);

      await page.waitForFunction(
        () => {
          const body = document.querySelector('body');
          return body && !body.classList.contains('loading') &&
                 !body.classList.contains('is-loading') &&
                 !body.classList.contains('app-loading');
        },
        { timeout }
      );

      return; // Success
    }
  } catch (error) {
    // Method not applicable or failed
  }

  throw new Error('No loading classes found on body element');
}

/**
 * Get the latest response content from the page
 */
async function getLatestResponseContent(page: Page): Promise<string> {
  const selectors = [
    '.chat-message:last-child',
    '.message:last-child',
    '.ai-response',
    '.response-content'
  ];

  for (const selector of selectors) {
    try {
      const element = page.locator(selector);
      const content = await element.textContent();

      if (content && content.trim().length > 0) {
        return content.trim();
      }
    } catch (error) {
      // Try next selector
    }
  }

  // Fallback: get body content
  return await page.textContent('body') || '';
}

/**
 * Detect financial content in response text
 */
function detectFinancialContent(content: string): boolean {
  const financialKeywords = [
    'stock', 'price', 'volume', 'market', 'trading', 'exchange',
    'bullish', 'bearish', 'buy', 'sell', 'analysis', 'earnings',
    'revenue', 'profit', 'loss', 'investment', 'portfolio',
    'NVDA', 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'SPY', 'QQQ', 'GME'
  ];

  const contentLower = content.toLowerCase();
  const matchCount = financialKeywords.filter(keyword =>
    contentLower.includes(keyword)
  ).length;

  // Must contain at least 2 financial keywords
  return matchCount >= 2;
}

/**
 * Detect financial emoji indicators
 */
function detectFinancialEmojis(content: string): string[] {
  const financialEmojis = ['📈', '📉', '💰', '💸', '🏢', '📊', '🎯', '💲', '🔢'];

  return financialEmojis.filter(emoji => content.includes(emoji));
}

/**
 * Detect stock tickers in content
 */
function detectTickers(content: string): string[] {
  const tickerRegex = /\b[A-Z]{1,5}\b/g;
  const matches = content.match(tickerRegex) || [];

  // Filter to likely tickers (2-5 characters, common patterns)
  const likelyTickers = matches.filter(match =>
    match.length >= 2 &&
    match.length <= 5 &&
    !['THE', 'AND', 'FOR', 'ARE', 'YOU', 'NOT', 'BUT', 'CAN', 'HAS', 'WAS'].includes(match)
  );

  // Remove duplicates
  return [...new Set(likelyTickers)];
}

/**
 * Utility: Create custom auto-retry config for specific tests
 */
export function createTestSpecificConfig(
  testType: 'market-status' | 'ticker-analysis' | 'button-template',
  maxTimeout: number = 120000
): AutoRetryConfig {

  const baseConfig = { ...DEFAULT_AUTO_RETRY_CONFIG, maxTimeoutMs: maxTimeout };

  switch (testType) {
    case 'market-status':
      return {
        ...baseConfig,
        phase1Methods: [DetectionMethod.LOADING_HIDDEN, DetectionMethod.MESSAGE_COUNT]
      };

    case 'ticker-analysis':
      return {
        ...baseConfig,
        phase1Methods: [DetectionMethod.RESPONSE_VISIBLE, DetectionMethod.COMPLETION_TEXT]
      };

    case 'button-template':
      return {
        ...baseConfig,
        phase1Methods: [DetectionMethod.MESSAGE_COUNT, DetectionMethod.RESPONSE_VISIBLE]
      };

    default:
      return baseConfig;
  }
}