/**
 * Response Validation Utilities for Playwright CLI Tests
 * 
 * Implements response validation with emoji indicators and content verification
 * Detects financial indicators, KEY TAKEAWAYS sections, and ticker-specific responses
 * 
 * @fileoverview Response validation and content analysis utilities for financial data
 */

import { Page, Locator } from '@playwright/test';

/**
 * Financial emoji indicators used in responses
 */
export const FINANCIAL_EMOJIS = {
  BULLISH: '📈',
  BEARISH: '📉',
  MONEY: '💰',
  MONEY_LOSS: '💸',
  BUILDING: '🏢',
  CHART: '📊',
  TARGET: '🎯',
  WARNING: '⚠️',
  CHECK: '✅',
  CROSS: '❌'
} as const;

/**
 * Validation result interface
 */
export interface ValidationResult {
  isValid: boolean;
  hasKeyTakeaways: boolean;
  hasEmojiIndicators: boolean;
  hasFinancialContent: boolean;
  detectedEmojis: string[];
  detectedTickers: string[];
  detectedKeywords: string[];
  contentLength: number;
  validationErrors: string[];
  responseContent?: string;
}

/**
 * Ticker-specific validation configuration
 */
export interface TickerValidationConfig {
  ticker: string;
  expectedKeywords: string[];
  requiredEmojis: string[];
  minContentLength: number;
  allowPartialMatch: boolean;
}

/**
 * Common stock tickers for validation
 */
export const COMMON_TICKERS = [
  'NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'AMD', 'INTC', 'SPY', 'GME'
] as const;

/**
 * Financial keywords for content validation
 */
export const FINANCIAL_KEYWORDS = [
  // Price and trading
  'price', 'stock', 'trading', 'volume', 'market cap', 'shares',
  'buy', 'sell', 'hold', 'bullish', 'bearish',
  
  // Financial metrics
  'earnings', 'revenue', 'profit', 'loss', 'eps', 'pe ratio',
  'dividend', 'yield', 'growth', 'valuation',
  
  // Market terms
  'analysis', 'recommendation', 'outlook', 'forecast',
  'resistance', 'support', 'trend', 'momentum',
  
  // Performance indicators
  'gain', 'decline', 'increase', 'decrease', 'up', 'down',
  'percentage', '%', 'basis points', 'volatility'
] as const;

/**
 * Validate financial response content
 * 
 * @param page - Playwright page instance
 * @param expectedTicker - Expected ticker symbol (optional)
 * @returns Promise<ValidationResult> - Comprehensive validation result
 */
export async function validateFinancialResponse(
  page: Page,
  expectedTicker?: string
): Promise<ValidationResult> {
  
  console.log(`[VALIDATION] Starting financial response validation${expectedTicker ? ` for ${expectedTicker}` : ''}`);
  
  // Get full page content
  const responseContent = await page.textContent('body') || '';
  const contentLength = responseContent.length;
  
  console.log(`[VALIDATION] Response content length: ${contentLength} characters`);
  
  const validationErrors: string[] = [];
  
  // Check for KEY TAKEAWAYS section
  const hasKeyTakeaways = await validateKeyTakeawaysSection(page);
  if (!hasKeyTakeaways) {
    validationErrors.push('Missing 🎯 KEY TAKEAWAYS section');
  }
  
  // Check for emoji indicators
  const { hasEmojis, detectedEmojis } = await validateEmojiIndicators(page, responseContent);
  if (!hasEmojis) {
    validationErrors.push('Missing financial emoji indicators');
  }
  
  // Check for financial content
  const { hasFinancialContent, detectedKeywords } = validateFinancialContent(responseContent);
  if (!hasFinancialContent) {
    validationErrors.push('Insufficient financial content detected');
  }
  
  // Check for ticker-specific content if ticker provided
  const detectedTickers = extractTickers(responseContent);
  if (expectedTicker && !detectedTickers.includes(expectedTicker.toUpperCase())) {
    validationErrors.push(`Expected ticker ${expectedTicker} not found in response`);
  }
  
  // Validate minimum content length
  if (contentLength < 100) {
    validationErrors.push(`Response too short: ${contentLength} characters (minimum 100)`);
  }
  
  const isValid = validationErrors.length === 0;
  
  const result: ValidationResult = {
    isValid,
    hasKeyTakeaways,
    hasEmojiIndicators: hasEmojis,
    hasFinancialContent,
    detectedEmojis,
    detectedTickers,
    detectedKeywords,
    contentLength,
    validationErrors,
    responseContent: contentLength > 0 ? responseContent : undefined
  };
  
  console.log(`[VALIDATION] Validation result: ${isValid ? 'VALID' : 'INVALID'}`);
  if (!isValid) {
    console.log(`[VALIDATION] Validation errors:`, validationErrors);
  }
  console.log(`[VALIDATION] Detected emojis:`, detectedEmojis);
  console.log(`[VALIDATION] Detected tickers:`, detectedTickers);
  console.log(`[VALIDATION] Detected keywords:`, detectedKeywords.slice(0, 10)); // First 10 for brevity
  
  return result;
}

/**
 * Validate KEY TAKEAWAYS section presence
 * 
 * @param page - Playwright page instance
 * @returns Promise<boolean> - True if KEY TAKEAWAYS section found
 */
export async function validateKeyTakeawaysSection(page: Page): Promise<boolean> {
  console.log(`[VALIDATION] Checking for 🎯 KEY TAKEAWAYS section...`);
  
  try {
    // Look for the exact KEY TAKEAWAYS text with target emoji
    const keyTakeawaysSelectors = [
      'text=🎯 KEY TAKEAWAYS',
      'text=KEY TAKEAWAYS',
      ':has-text("🎯 KEY TAKEAWAYS")',
      ':has-text("KEY TAKEAWAYS")'
    ];
    
    for (const selector of keyTakeawaysSelectors) {
      try {
        const element = page.locator(selector);
        const isVisible = await element.isVisible({ timeout: 2000 });
        
        if (isVisible) {
          console.log(`[VALIDATION] Found KEY TAKEAWAYS section using selector: ${selector}`);
          return true;
        }
      } catch (error) {
        // Continue to next selector
      }
    }
    
    console.log(`[VALIDATION] KEY TAKEAWAYS section not found`);
    return false;
    
  } catch (error) {
    console.log(`[VALIDATION] Error checking KEY TAKEAWAYS:`, error);
    return false;
  }
}

/**
 * Validate emoji indicators in response
 * 
 * @param page - Playwright page instance
 * @param content - Response content text
 * @returns Promise<{hasEmojis: boolean, detectedEmojis: string[]}> - Emoji validation result
 */
export async function validateEmojiIndicators(
  page: Page, 
  content: string
): Promise<{hasEmojis: boolean, detectedEmojis: string[]}> {
  
  console.log(`[VALIDATION] Checking for financial emoji indicators...`);
  
  const detectedEmojis: string[] = [];
  const allEmojis = Object.values(FINANCIAL_EMOJIS);
  
  // Check content for emojis
  for (const emoji of allEmojis) {
    if (content.includes(emoji)) {
      detectedEmojis.push(emoji);
    }
  }
  
  // Also check page elements for emoji visibility
  for (const emoji of allEmojis) {
    try {
      const emojiElement = page.locator(`text=${emoji}`);
      const isVisible = await emojiElement.isVisible({ timeout: 1000 });
      
      if (isVisible && !detectedEmojis.includes(emoji)) {
        detectedEmojis.push(emoji);
      }
    } catch (error) {
      // Continue checking other emojis
    }
  }
  
  const hasEmojis = detectedEmojis.length > 0;
  
  console.log(`[VALIDATION] Emoji check: ${hasEmojis ? 'FOUND' : 'NOT FOUND'} (${detectedEmojis.length} emojis)`);
  
  return { hasEmojis, detectedEmojis };
}

/**
 * Validate financial content keywords
 * 
 * @param content - Response content text
 * @returns {hasFinancialContent: boolean, detectedKeywords: string[]} - Financial content validation
 */
export function validateFinancialContent(content: string): {hasFinancialContent: boolean, detectedKeywords: string[]} {
  console.log(`[VALIDATION] Checking for financial content keywords...`);
  
  const contentLower = content.toLowerCase();
  const detectedKeywords: string[] = [];
  
  for (const keyword of FINANCIAL_KEYWORDS) {
    if (contentLower.includes(keyword.toLowerCase())) {
      detectedKeywords.push(keyword);
    }
  }
  
  // Require at least 3 financial keywords for valid financial content
  const hasFinancialContent = detectedKeywords.length >= 3;
  
  console.log(`[VALIDATION] Financial content: ${hasFinancialContent ? 'VALID' : 'INSUFFICIENT'} (${detectedKeywords.length} keywords)`);
  
  return { hasFinancialContent, detectedKeywords };
}

/**
 * Extract ticker symbols from content
 * 
 * @param content - Response content text
 * @returns string[] - Array of detected ticker symbols
 */
export function extractTickers(content: string): string[] {
  console.log(`[VALIDATION] Extracting ticker symbols...`);
  
  const detectedTickers: string[] = [];
  
  // Check for common tickers
  for (const ticker of COMMON_TICKERS) {
    const tickerRegex = new RegExp(`\\b${ticker}\\b`, 'gi');
    if (tickerRegex.test(content)) {
      if (!detectedTickers.includes(ticker)) {
        detectedTickers.push(ticker);
      }
    }
  }
  
  // Also look for ticker patterns (1-5 uppercase letters)
  const tickerPattern = /\b[A-Z]{1,5}\b/g;
  const matches = content.match(tickerPattern) || [];
  
  for (const match of matches) {
    if (match.length >= 2 && match.length <= 5 && !detectedTickers.includes(match)) {
      // Additional validation - check if it appears with financial context
      const contextRegex = new RegExp(`${match}\\s*(stock|price|trading|shares|corp|inc|ltd)`, 'gi');
      if (contextRegex.test(content)) {
        detectedTickers.push(match);
      }
    }
  }
  
  console.log(`[VALIDATION] Detected tickers:`, detectedTickers);
  
  return detectedTickers;
}

/**
 * Validate specific ticker response
 * 
 * @param page - Playwright page instance
 * @param config - Ticker validation configuration
 * @returns Promise<ValidationResult> - Ticker-specific validation result
 */
export async function validateTickerResponse(
  page: Page,
  config: TickerValidationConfig
): Promise<ValidationResult> {
  
  console.log(`[VALIDATION] Validating ticker-specific response for ${config.ticker}`);
  
  // Get base validation
  const baseValidation = await validateFinancialResponse(page, config.ticker);
  
  const additionalErrors: string[] = [];
  
  // Check for required keywords
  const foundKeywords = config.expectedKeywords.filter(keyword =>
    baseValidation.detectedKeywords.some(detected => 
      detected.toLowerCase().includes(keyword.toLowerCase())
    )
  );
  
  if (!config.allowPartialMatch && foundKeywords.length < config.expectedKeywords.length) {
    const missingKeywords = config.expectedKeywords.filter(keyword => 
      !foundKeywords.some(found => found.toLowerCase().includes(keyword.toLowerCase()))
    );
    additionalErrors.push(`Missing required keywords: ${missingKeywords.join(', ')}`);
  }
  
  // Check for required emojis
  const foundEmojis = config.requiredEmojis.filter(emoji =>
    baseValidation.detectedEmojis.includes(emoji)
  );
  
  if (foundEmojis.length < config.requiredEmojis.length) {
    const missingEmojis = config.requiredEmojis.filter(emoji => 
      !baseValidation.detectedEmojis.includes(emoji)
    );
    additionalErrors.push(`Missing required emojis: ${missingEmojis.join(', ')}`);
  }
  
  // Check minimum content length
  if (baseValidation.contentLength < config.minContentLength) {
    additionalErrors.push(`Content too short: ${baseValidation.contentLength} < ${config.minContentLength}`);
  }
  
  // Merge validation errors
  const allErrors = [...baseValidation.validationErrors, ...additionalErrors];
  
  const result: ValidationResult = {
    ...baseValidation,
    isValid: allErrors.length === 0,
    validationErrors: allErrors
  };
  
  console.log(`[VALIDATION] Ticker validation result for ${config.ticker}: ${result.isValid ? 'VALID' : 'INVALID'}`);
  
  return result;
}

/**
 * Validate empty input handling
 * 
 * @param page - Playwright page instance
 * @returns Promise<boolean> - True if empty input is properly handled
 */
export async function validateEmptyInputHandling(page: Page): Promise<boolean> {
  console.log(`[VALIDATION] Checking empty input handling...`);
  
  try {
    // Look for validation messages or disabled states
    const validationSelectors = [
      'text=Please enter a message',
      'text=Message cannot be empty',
      'text=Please enter some text',
      '[data-testid="error-message"]',
      '.error-message',
      '.validation-error'
    ];
    
    for (const selector of validationSelectors) {
      try {
        const element = page.locator(selector);
        const isVisible = await element.isVisible({ timeout: 2000 });
        
        if (isVisible) {
          console.log(`[VALIDATION] Found validation message: ${selector}`);
          return true;
        }
      } catch (error) {
        // Continue checking
      }
    }
    
    // Check if send button is disabled for empty input
    const sendButtonSelectors = [
      'button[type="submit"]',
      '.send-button',
      '[data-testid="send-button"]'
    ];
    
    for (const selector of sendButtonSelectors) {
      try {
        const button = page.locator(selector);
        const isDisabled = await button.isDisabled({ timeout: 2000 });
        
        if (isDisabled) {
          console.log(`[VALIDATION] Send button properly disabled for empty input`);
          return true;
        }
      } catch (error) {
        // Continue checking
      }
    }
    
    console.log(`[VALIDATION] Empty input handling validation failed - no proper validation detected`);
    return false;
    
  } catch (error) {
    console.log(`[VALIDATION] Error checking empty input handling:`, error);
    return false;
  }
}

/**
 * Get validation summary for multiple test results
 * 
 * @param results - Array of validation results
 * @returns Object with summary statistics
 */
export function getValidationSummary(results: ValidationResult[]): {
  totalTests: number;
  validCount: number;
  invalidCount: number;
  successRate: number;
  commonErrors: Array<{error: string, count: number}>;
  emojiStats: Array<{emoji: string, count: number}>;
  tickerStats: Array<{ticker: string, count: number}>;
} {
  
  const totalTests = results.length;
  const validCount = results.filter(r => r.isValid).length;
  const invalidCount = totalTests - validCount;
  const successRate = totalTests > 0 ? (validCount / totalTests) * 100 : 0;
  
  // Count common errors
  const errorCounts: {[key: string]: number} = {};
  results.forEach(result => {
    result.validationErrors.forEach(error => {
      errorCounts[error] = (errorCounts[error] || 0) + 1;
    });
  });
  
  const commonErrors = Object.entries(errorCounts)
    .map(([error, count]) => ({ error, count }))
    .sort((a, b) => b.count - a.count);
  
  // Count emoji usage
  const emojiCounts: {[key: string]: number} = {};
  results.forEach(result => {
    result.detectedEmojis.forEach(emoji => {
      emojiCounts[emoji] = (emojiCounts[emoji] || 0) + 1;
    });
  });
  
  const emojiStats = Object.entries(emojiCounts)
    .map(([emoji, count]) => ({ emoji, count }))
    .sort((a, b) => b.count - a.count);
  
  // Count ticker mentions
  const tickerCounts: {[key: string]: number} = {};
  results.forEach(result => {
    result.detectedTickers.forEach(ticker => {
      tickerCounts[ticker] = (tickerCounts[ticker] || 0) + 1;
    });
  });
  
  const tickerStats = Object.entries(tickerCounts)
    .map(([ticker, count]) => ({ ticker, count }))
    .sort((a, b) => b.count - a.count);
  
  return {
    totalTests,
    validCount,
    invalidCount,
    successRate,
    commonErrors,
    emojiStats,
    tickerStats
  };
}