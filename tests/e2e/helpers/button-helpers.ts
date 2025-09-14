/**
 * Button Interaction Helpers for Playwright CLI Tests
 * 
 * Implements button-specific test functionality for Stock Snapshot, Support & Resistance, and Technical Analysis
 * Provides button interaction methods, state validation, and processing detection
 * 
 * @fileoverview Button testing utilities for financial analysis button interactions
 */

import { Page, Locator } from '@playwright/test';
import { pollForResponse, PollingResult, PerformanceClassification, DEFAULT_POLLING_CONFIG } from './polling';
import { validateFinancialResponse, ValidationResult } from './validation';

/**
 * Button type enumeration for financial analysis buttons
 */
export enum ButtonType {
  STOCK_SNAPSHOT = 'STOCK_SNAPSHOT',         // 📈 Stock Snapshot button
  SUPPORT_RESISTANCE = 'SUPPORT_RESISTANCE', // 🎯 Support & Resistance button  
  TECHNICAL_ANALYSIS = 'TECHNICAL_ANALYSIS'  // 🔧 Technical Analysis button
}

/**
 * Button selector configuration for different button types
 */
export const BUTTON_SELECTORS = {
  [ButtonType.STOCK_SNAPSHOT]: [
    '#button-snapshot-label',
    'button:has-text("📊")',
    'button:has-text("Snapshot Analysis")', 
    '.analysis-button:has-text("Snapshot")',
    'button:has-text("📈")',
    'button:has-text("Stock Snapshot")', 
    '[data-testid="stock-snapshot-button"]',
    '.stock-snapshot-btn'
  ],
  [ButtonType.SUPPORT_RESISTANCE]: [
    '#button-support_resistance-label',
    'button:has-text("🎯")',
    'button:has-text("Support Resistance Analysis")',
    '.analysis-button:has-text("Support")',
    'button:has-text("Support & Resistance")',
    '[data-testid="support-resistance-button"]', 
    '.support-resistance-btn'
  ],
  [ButtonType.TECHNICAL_ANALYSIS]: [
    '#button-technical_analysis-label',
    'button:has-text("🔧")',
    'button:has-text("Technical Analysis")',
    '.analysis-button:has-text("Technical")',
    '[data-testid="technical-analysis-button"]',
    '.technical-analysis-btn'
  ]
} as const;

/**
 * Button interaction result interface
 */
export interface ButtonInteractionResult {
  success: boolean;
  buttonType: ButtonType;
  responseTime: number;
  classification: PerformanceClassification;
  buttonFound: boolean;
  buttonClicked: boolean;
  validationResult?: ValidationResult;
  error?: string;
  screenshot?: string;
}

/**
 * Button state validation configuration
 */
export interface ButtonStateConfig {
  expectedStates: Array<'enabled' | 'disabled' | 'loading' | 'pressed'>;
  waitForStateChange: boolean;
  maxStateWaitMs: number;
}

/**
 * Default button state configuration
 */
export const DEFAULT_BUTTON_STATE_CONFIG: ButtonStateConfig = {
  expectedStates: ['enabled'],
  waitForStateChange: false,
  maxStateWaitMs: 5000
};

/**
 * Click button and wait for financial response
 * 
 * @param page - Playwright page instance
 * @param buttonType - Type of button to click
 * @param ticker - Optional ticker symbol for input
 * @param testName - Test name for logging
 * @returns Promise<ButtonInteractionResult> - Complete button interaction result
 */
export async function clickButtonAndWaitForResponse(
  page: Page,
  buttonType: ButtonType,
  ticker?: string,
  testName: string = 'ButtonTest'
): Promise<ButtonInteractionResult> {
  
  console.log(`[BUTTON-HELPER] Starting button interaction: ${buttonType}${ticker ? ` for ${ticker}` : ''}`);
  
  const startTime = Date.now();
  
  try {
    // Step 1: Input ticker if provided
    if (ticker) {
      const inputResult = await inputTicker(page, ticker);
      if (!inputResult.success) {
        return {
          success: false,
          buttonType,
          responseTime: Date.now() - startTime,
          classification: PerformanceClassification.TIMEOUT,
          buttonFound: false,
          buttonClicked: false,
          error: `Failed to input ticker: ${inputResult.error}`
        };
      }
    }
    
    // Step 2: Find and click the button
    const clickResult = await clickButton(page, buttonType);
    if (!clickResult.success) {
      return {
        success: false,
        buttonType,
        responseTime: Date.now() - startTime,
        classification: PerformanceClassification.TIMEOUT,
        buttonFound: clickResult.buttonFound,
        buttonClicked: false,
        error: clickResult.error
      };
    }
    
    // Step 3: Wait for response with polling
    console.log(`[BUTTON-HELPER] Button clicked, waiting for response...`);
    const pollingResult = await pollForResponse(page);
    
    // Step 4: Validate response if successful
    let validationResult: ValidationResult | undefined;
    if (pollingResult.success) {
      validationResult = await validateFinancialResponse(page, ticker);
    }
    
    const result: ButtonInteractionResult = {
      success: pollingResult.success,
      buttonType,
      responseTime: pollingResult.responseTime,
      classification: pollingResult.classification,
      buttonFound: clickResult.buttonFound,
      buttonClicked: clickResult.success,
      validationResult,
      error: pollingResult.error
    };
    
    console.log(`[BUTTON-HELPER] Button interaction completed: ${buttonType} - ${result.classification} (${result.responseTime}ms)`);
    
    return result;
    
  } catch (error) {
    const responseTime = Date.now() - startTime;
    
    console.log(`[BUTTON-HELPER] Button interaction failed: ${buttonType} - Error: ${error}`);
    
    return {
      success: false,
      buttonType,
      responseTime,
      classification: PerformanceClassification.TIMEOUT,
      buttonFound: false,
      buttonClicked: false,
      error: String(error)
    };
  }
}

/**
 * Input ticker symbol into the input field
 * 
 * @param page - Playwright page instance  
 * @param ticker - Ticker symbol to input
 * @returns Promise<{success: boolean, error?: string}> - Input operation result
 */
export async function inputTicker(
  page: Page,
  ticker: string
): Promise<{success: boolean, error?: string}> {
  
  console.log(`[BUTTON-HELPER] Inputting ticker: ${ticker}`);
  
  try {
    // Input field selectors (same as used in existing test helpers)
    const inputSelectors = [
      'textarea[placeholder*="message"]',
      'input[placeholder*="message"]', 
      'textarea',
      '.chat-input textarea',
      '.message-input textarea',
      'input[type="text"]'
    ];
    
    let inputElement: Locator | null = null;
    
    // Find available input field
    for (const selector of inputSelectors) {
      try {
        const element = page.locator(selector).first();
        const isVisible = await element.isVisible({ timeout: 2000 });
        
        if (isVisible) {
          inputElement = element;
          console.log(`[BUTTON-HELPER] Found input field: ${selector}`);
          break;
        }
      } catch (error) {
        // Continue to next selector
      }
    }
    
    if (!inputElement) {
      return { success: false, error: 'No input field found' };
    }
    
    // Clear and input ticker
    await inputElement.focus();
    await inputElement.clear();
    await inputElement.type(ticker);
    
    // Verify input was entered
    const inputValue = await inputElement.inputValue();
    if (inputValue !== ticker) {
      return { success: false, error: `Input verification failed. Expected: ${ticker}, Got: ${inputValue}` };
    }
    
    console.log(`[BUTTON-HELPER] Ticker input successful: ${ticker}`);
    return { success: true };
    
  } catch (error) {
    console.log(`[BUTTON-HELPER] Ticker input failed:`, error);
    return { success: false, error: String(error) };
  }
}

/**
 * Click specific button type
 * 
 * @param page - Playwright page instance
 * @param buttonType - Type of button to click
 * @returns Promise<{success: boolean, buttonFound: boolean, error?: string}> - Click operation result
 */
export async function clickButton(
  page: Page,
  buttonType: ButtonType
): Promise<{success: boolean, buttonFound: boolean, error?: string}> {
  
  console.log(`[BUTTON-HELPER] Clicking button: ${buttonType}`);
  
  try {
    const selectors = BUTTON_SELECTORS[buttonType];
    let buttonElement: Locator | null = null;
    
    // Find the button using available selectors
    for (const selector of selectors) {
      try {
        const element = page.locator(selector).first();
        const isVisible = await element.isVisible({ timeout: 3000 });
        
        if (isVisible) {
          buttonElement = element;
          console.log(`[BUTTON-HELPER] Found button using selector: ${selector}`);
          break;
        }
      } catch (error) {
        // Continue to next selector
      }
    }
    
    if (!buttonElement) {
      console.log(`[BUTTON-HELPER] Button not found: ${buttonType}`);
      return { 
        success: false, 
        buttonFound: false, 
        error: `Button not found: ${buttonType}. Tried selectors: ${selectors.join(', ')}` 
      };
    }
    
    // Check if button is enabled
    const isEnabled = await buttonElement.isEnabled();
    if (!isEnabled) {
      return { 
        success: false, 
        buttonFound: true, 
        error: `Button is disabled: ${buttonType}` 
      };
    }
    
    // Click the button
    await buttonElement.click();
    
    // Brief wait for UI to respond to click
    await page.waitForTimeout(1000);
    
    console.log(`[BUTTON-HELPER] Button clicked successfully: ${buttonType}`);
    return { success: true, buttonFound: true };
    
  } catch (error) {
    console.log(`[BUTTON-HELPER] Button click failed:`, error);
    return { 
      success: false, 
      buttonFound: false, 
      error: String(error) 
    };
  }
}

/**
 * Validate button states (enabled, disabled, loading, etc.)
 * 
 * @param page - Playwright page instance
 * @param buttonType - Type of button to validate
 * @param config - Button state validation configuration
 * @returns Promise<{valid: boolean, actualStates: string[], error?: string}> - State validation result
 */
export async function validateButtonState(
  page: Page,
  buttonType: ButtonType,
  config: ButtonStateConfig = DEFAULT_BUTTON_STATE_CONFIG
): Promise<{valid: boolean, actualStates: string[], error?: string}> {
  
  console.log(`[BUTTON-HELPER] Validating button state: ${buttonType}`);
  
  try {
    const selectors = BUTTON_SELECTORS[buttonType];
    let buttonElement: Locator | null = null;
    
    // Find the button
    for (const selector of selectors) {
      try {
        const element = page.locator(selector).first();
        const isVisible = await element.isVisible({ timeout: 2000 });
        
        if (isVisible) {
          buttonElement = element;
          break;
        }
      } catch (error) {
        // Continue
      }
    }
    
    if (!buttonElement) {
      return { 
        valid: false, 
        actualStates: [], 
        error: `Button not found: ${buttonType}` 
      };
    }
    
    // Check various button states
    const actualStates: string[] = [];
    
    // Check enabled/disabled
    const isEnabled = await buttonElement.isEnabled();
    actualStates.push(isEnabled ? 'enabled' : 'disabled');
    
    // Check for loading indicators
    const hasLoadingClass = await buttonElement.getAttribute('class')
      .then(className => className?.includes('loading') || className?.includes('spinner') || false)
      .catch(() => false);
    
    const hasLoadingAttribute = await buttonElement.getAttribute('aria-busy')
      .then(ariaBusy => ariaBusy === 'true')
      .catch(() => false);
    
    if (hasLoadingClass || hasLoadingAttribute) {
      actualStates.push('loading');
    }
    
    // Check for pressed state
    const isPressed = await buttonElement.getAttribute('aria-pressed')
      .then(ariaPressed => ariaPressed === 'true')
      .catch(() => false);
    
    if (isPressed) {
      actualStates.push('pressed');
    }
    
    // Wait for state change if configured
    if (config.waitForStateChange) {
      console.log(`[BUTTON-HELPER] Waiting for state change (${config.maxStateWaitMs}ms)...`);
      await page.waitForTimeout(config.maxStateWaitMs);
      
      // Re-check states after waiting
      // (This is simplified - could implement more sophisticated state change detection)
    }
    
    // Validate expected states
    const hasAllExpectedStates = config.expectedStates.every(expectedState => 
      actualStates.includes(expectedState)
    );
    
    console.log(`[BUTTON-HELPER] Button state validation: ${hasAllExpectedStates ? 'VALID' : 'INVALID'}`);
    console.log(`[BUTTON-HELPER] Expected states: ${config.expectedStates.join(', ')}`);
    console.log(`[BUTTON-HELPER] Actual states: ${actualStates.join(', ')}`);
    
    return {
      valid: hasAllExpectedStates,
      actualStates,
      error: hasAllExpectedStates ? undefined : `Expected states ${config.expectedStates.join(', ')}, got ${actualStates.join(', ')}`
    };
    
  } catch (error) {
    console.log(`[BUTTON-HELPER] Button state validation failed:`, error);
    return { 
      valid: false, 
      actualStates: [], 
      error: String(error) 
    };
  }
}

/**
 * Detect processing state after button click
 * 
 * @param page - Playwright page instance
 * @returns Promise<{isProcessing: boolean, processingIndicators: string[]}> - Processing state result
 */
export async function detectProcessingState(
  page: Page
): Promise<{isProcessing: boolean, processingIndicators: string[]}> {
  
  console.log(`[BUTTON-HELPER] Detecting processing state...`);
  
  const processingIndicators: string[] = [];
  
  try {
    // Check for loading indicators
    const loadingSelectors = [
      '.loading',
      '.spinner',
      '.processing',
      '[aria-busy="true"]',
      'text=Loading',
      'text=Processing',
      'text=Analyzing'
    ];
    
    for (const selector of loadingSelectors) {
      try {
        const element = page.locator(selector);
        const isVisible = await element.isVisible({ timeout: 1000 });
        
        if (isVisible) {
          processingIndicators.push(selector);
        }
      } catch (error) {
        // Continue checking
      }
    }
    
    // Check for disabled buttons (indicating processing)
    const buttonSelectors = [
      'button[disabled]',
      'button[aria-disabled="true"]'
    ];
    
    for (const selector of buttonSelectors) {
      try {
        const elements = page.locator(selector);
        const count = await elements.count();
        
        if (count > 0) {
          processingIndicators.push(`${selector} (${count} disabled buttons)`);
        }
      } catch (error) {
        // Continue checking
      }
    }
    
    const isProcessing = processingIndicators.length > 0;
    
    console.log(`[BUTTON-HELPER] Processing state: ${isProcessing ? 'PROCESSING' : 'IDLE'}`);
    if (isProcessing) {
      console.log(`[BUTTON-HELPER] Processing indicators: ${processingIndicators.join(', ')}`);
    }
    
    return { isProcessing, processingIndicators };
    
  } catch (error) {
    console.log(`[BUTTON-HELPER] Processing state detection failed:`, error);
    return { isProcessing: false, processingIndicators: [] };
  }
}

/**
 * Execute multi-button interaction test
 * 
 * @param page - Playwright page instance
 * @param buttons - Array of button types to test in sequence
 * @param ticker - Ticker symbol for input
 * @returns Promise<ButtonInteractionResult[]> - Results for each button interaction
 */
export async function executeMultiButtonTest(
  page: Page,
  buttons: ButtonType[],
  ticker: string
): Promise<ButtonInteractionResult[]> {
  
  console.log(`[BUTTON-HELPER] Executing multi-button test with ${buttons.length} buttons for ${ticker}`);
  
  const results: ButtonInteractionResult[] = [];
  
  for (let i = 0; i < buttons.length; i++) {
    const buttonType = buttons[i];
    
    console.log(`[BUTTON-HELPER] --- Button ${i + 1}/${buttons.length}: ${buttonType} ---`);
    
    // Small delay between button tests
    if (i > 0) {
      await page.waitForTimeout(3000);
    }
    
    const result = await clickButtonAndWaitForResponse(
      page, 
      buttonType, 
      ticker, 
      `MultiButton-${buttonType}-${i + 1}`
    );
    
    results.push(result);
    
    // Log intermediate result
    console.log(`[BUTTON-HELPER] Button ${i + 1} result: ${result.success ? 'SUCCESS' : 'FAILED'} (${result.responseTime}ms)`);
  }
  
  console.log(`[BUTTON-HELPER] Multi-button test completed: ${results.filter(r => r.success).length}/${results.length} successful`);
  
  return results;
}

/**
 * Validate button accessibility features
 * 
 * @param page - Playwright page instance
 * @param buttonType - Type of button to validate
 * @returns Promise<{accessible: boolean, issues: string[]}> - Accessibility validation result
 */
export async function validateButtonAccessibility(
  page: Page,
  buttonType: ButtonType
): Promise<{accessible: boolean, issues: string[]}> {
  
  console.log(`[BUTTON-HELPER] Validating button accessibility: ${buttonType}`);
  
  const issues: string[] = [];
  
  try {
    const selectors = BUTTON_SELECTORS[buttonType];
    let buttonElement: Locator | null = null;
    
    // Find the button
    for (const selector of selectors) {
      try {
        const element = page.locator(selector).first();
        const isVisible = await element.isVisible({ timeout: 2000 });
        
        if (isVisible) {
          buttonElement = element;
          break;
        }
      } catch (error) {
        // Continue
      }
    }
    
    if (!buttonElement) {
      issues.push('Button not found for accessibility testing');
      return { accessible: false, issues };
    }
    
    // Check for aria-label or accessible text
    const ariaLabel = await buttonElement.getAttribute('aria-label');
    const textContent = await buttonElement.textContent();
    const title = await buttonElement.getAttribute('title');
    
    const hasAccessibleText = !!(ariaLabel || textContent?.trim() || title);
    if (!hasAccessibleText) {
      issues.push('Button lacks accessible text (aria-label, text content, or title)');
    }
    
    // Check for role attribute
    const role = await buttonElement.getAttribute('role');
    if (!role && !(await buttonElement.evaluate(el => el.tagName.toLowerCase() === 'button'))) {
      issues.push('Non-button element lacks role="button" attribute');
    }
    
    // Check if button is keyboard accessible
    const tabIndex = await buttonElement.getAttribute('tabindex');
    if (tabIndex === '-1') {
      issues.push('Button is not keyboard accessible (tabindex="-1")');
    }
    
    // Check for focus visibility
    await buttonElement.focus();
    const hasOutline = await buttonElement.evaluate(el => {
      const style = window.getComputedStyle(el);
      return style.outline !== 'none' && style.outline !== '0px' && style.outline !== '';
    });
    
    if (!hasOutline) {
      // This is a warning, not necessarily an error
      console.log(`[BUTTON-HELPER] Warning: Button may lack visible focus indicator`);
    }
    
    const accessible = issues.length === 0;
    
    console.log(`[BUTTON-HELPER] Accessibility validation: ${accessible ? 'ACCESSIBLE' : 'ISSUES FOUND'}`);
    if (!accessible) {
      console.log(`[BUTTON-HELPER] Accessibility issues: ${issues.join(', ')}`);
    }
    
    return { accessible, issues };
    
  } catch (error) {
    console.log(`[BUTTON-HELPER] Accessibility validation failed:`, error);
    issues.push(`Accessibility validation error: ${error}`);
    return { accessible: false, issues };
  }
}

/**
 * Generate button test report from multiple results
 * 
 * @param results - Array of button interaction results  
 * @returns Object with comprehensive button test report
 */
export function generateButtonTestReport(results: ButtonInteractionResult[]): {
  summary: {
    totalTests: number;
    successCount: number;
    buttonFoundCount: number;
    buttonClickedCount: number;
    averageResponseTime: number;
  };
  performance: {
    successCount: number;
    slowCount: number;
    timeoutCount: number;
  };
  buttonTypes: {
    [key: string]: {
      tested: number;
      successful: number;
      averageTime: number;
    };
  };
  detailedResults: ButtonInteractionResult[];
} {
  
  const totalTests = results.length;
  const successCount = results.filter(r => r.success).length;
  const buttonFoundCount = results.filter(r => r.buttonFound).length;
  const buttonClickedCount = results.filter(r => r.buttonClicked).length;
  
  const responseTimes = results.map(r => r.responseTime);
  const averageResponseTime = responseTimes.length > 0 
    ? responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length 
    : 0;
  
  // Performance breakdown
  const performance = {
    successCount: results.filter(r => r.classification === PerformanceClassification.SUCCESS).length,
    slowCount: results.filter(r => r.classification === PerformanceClassification.SLOW_PERFORMANCE).length,
    timeoutCount: results.filter(r => r.classification === PerformanceClassification.TIMEOUT).length
  };
  
  // Button type statistics
  const buttonTypes: {[key: string]: {tested: number; successful: number; averageTime: number}} = {};
  
  for (const buttonType of Object.values(ButtonType)) {
    const typeResults = results.filter(r => r.buttonType === buttonType);
    const typeSuccessful = typeResults.filter(r => r.success);
    const typeTimes = typeResults.map(r => r.responseTime);
    
    buttonTypes[buttonType] = {
      tested: typeResults.length,
      successful: typeSuccessful.length,
      averageTime: typeTimes.length > 0 ? typeTimes.reduce((sum, time) => sum + time, 0) / typeTimes.length : 0
    };
  }
  
  return {
    summary: {
      totalTests,
      successCount,
      buttonFoundCount,
      buttonClickedCount,
      averageResponseTime
    },
    performance,
    buttonTypes,
    detailedResults: results
  };
}