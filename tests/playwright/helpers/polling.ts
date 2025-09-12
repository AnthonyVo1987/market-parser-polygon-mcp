/**
 * Polling Utilities for Playwright CLI Tests
 * 
 * Implements 30-second polling methodology with 120-second test limits
 * Provides early completion detection and timeout handling
 * 
 * @fileoverview Core polling utilities for financial data response detection
 */

import { Page, Locator } from '@playwright/test';

/**
 * Performance classification based on response timing
 */
export enum PerformanceClassification {
  SUCCESS = 'SUCCESS',           // < 45 seconds
  SLOW_PERFORMANCE = 'SLOW_PERFORMANCE', // 45-120 seconds  
  TIMEOUT = 'TIMEOUT'            // > 120 seconds
}

/**
 * Result interface for polling operations
 */
export interface PollingResult {
  success: boolean;
  responseTime: number;
  classification: PerformanceClassification;
  responseContent?: string;
  error?: string;
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
 * Poll for financial data response with 30-second intervals
 * 
 * @param page - Playwright page instance
 * @param config - Polling configuration
 * @returns Promise<PollingResult> - Result with timing and classification
 */
export async function pollForResponse(
  page: Page, 
  config: PollingConfig = DEFAULT_POLLING_CONFIG
): Promise<PollingResult> {
  const startTime = Date.now();
  const endTime = startTime + config.maxTimeoutMs;
  
  console.log(`[POLLING] Starting 30-second polling for financial response (max ${config.maxTimeoutMs}ms)`);
  
  let pollCount = 0;
  
  while (Date.now() < endTime) {
    pollCount++;
    const currentTime = Date.now();
    const elapsedTime = currentTime - startTime;
    
    console.log(`[POLLING] Poll #${pollCount} at ${elapsedTime}ms - Checking for response...`);
    
    try {
      // Check for response indicators
      const responseDetected = await detectFinancialResponse(page, config);
      
      if (responseDetected.found) {
        const responseTime = Date.now() - startTime;
        const classification = classifyPerformance(responseTime, config);
        
        console.log(`[POLLING] SUCCESS: Response detected after ${responseTime}ms (${classification})`);
        
        return {
          success: true,
          responseTime,
          classification,
          responseContent: responseDetected.content
        };
      }
      
      // Check if we have time for another full polling cycle
      const timeRemaining = endTime - Date.now();
      if (timeRemaining < config.pollingIntervalMs) {
        console.log(`[POLLING] Insufficient time remaining (${timeRemaining}ms) for next poll cycle`);
        break;
      }
      
      // Wait for next polling interval
      console.log(`[POLLING] No response yet, waiting ${config.pollingIntervalMs}ms for next poll...`);
      await page.waitForTimeout(config.pollingIntervalMs);
      
    } catch (error) {
      console.log(`[POLLING] Error during poll #${pollCount}:`, error);
      // Continue polling despite errors - might be temporary
    }
  }
  
  // Timeout reached
  const finalTime = Date.now() - startTime;
  console.log(`[POLLING] TIMEOUT: No response after ${finalTime}ms (${pollCount} polls)`);
  
  return {
    success: false,
    responseTime: finalTime,
    classification: PerformanceClassification.TIMEOUT,
    error: `Timeout after ${finalTime}ms with ${pollCount} polling attempts`
  };
}

/**
 * Detect financial response content on the page
 * 
 * @param page - Playwright page instance  
 * @param config - Polling configuration
 * @returns Promise<{found: boolean, content?: string}> - Detection result
 */
async function detectFinancialResponse(
  page: Page, 
  config: PollingConfig
): Promise<{found: boolean, content?: string}> {
  
  // Primary detection: Look for "🎯 KEY TAKEAWAYS" section
  const keyTakeawaysSelector = 'text=🎯 KEY TAKEAWAYS';
  const keyTakeawaysElement = page.locator(keyTakeawaysSelector);
  
  try {
    // Check if KEY TAKEAWAYS section is visible
    const keyTakeawaysVisible = await keyTakeawaysElement.isVisible({ timeout: 1000 });
    
    if (keyTakeawaysVisible) {
      console.log(`[POLLING] Detected 🎯 KEY TAKEAWAYS section`);
      
      // Get the content of the response
      const responseContent = await page.textContent('body') || '';
      
      // Validate it contains financial indicators
      if (containsFinancialIndicators(responseContent)) {
        return { found: true, content: responseContent };
      }
    }
  } catch (error) {
    // Element not found yet, continue checking
  }
  
  // Secondary detection: Look for financial emoji indicators
  const emojiIndicators = ['📈', '📉', '💰', '💸', '🏢', '📊'];
  
  for (const emoji of emojiIndicators) {
    try {
      const emojiElement = page.locator(`text=${emoji}`);
      const emojiVisible = await emojiElement.isVisible({ timeout: 1000 });
      
      if (emojiVisible) {
        console.log(`[POLLING] Detected financial emoji: ${emoji}`);
        const responseContent = await page.textContent('body') || '';
        
        if (containsFinancialIndicators(responseContent)) {
          return { found: true, content: responseContent };
        }
      }
    } catch (error) {
      // Continue checking other indicators
    }
  }
  
  // Tertiary detection: Custom element selector if provided
  if (config.elementSelector) {
    try {
      const customElement = page.locator(config.elementSelector);
      const customVisible = await customElement.isVisible({ timeout: 1000 });
      
      if (customVisible) {
        console.log(`[POLLING] Detected custom element: ${config.elementSelector}`);
        const elementContent = await customElement.textContent() || '';
        
        // Apply content matcher if provided
        if (config.contentMatcher) {
          if (config.contentMatcher.test(elementContent)) {
            return { found: true, content: elementContent };
          }
        } else {
          return { found: true, content: elementContent };
        }
      }
    } catch (error) {
      // Custom element not found yet
    }
  }
  
  return { found: false };
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