/**
 * TEST-B006: Empty Message Test
 * 
 * Tests empty message input validation and UI behavior
 * Implements dynamic port detection and frontend validation testing
 * Part of continuous browser session protocol
 * 
 * @fileoverview Empty Message input validation test with UI state verification
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  validateSystemReadiness,
  waitForPageReady,
  validatePageStructure,
  validateEmptyInputHandling,
  
  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  
  // Browser session management
  BrowserSessionManager
} from './helpers/index';

/**
 * TEST-B006: Empty Message Test Suite
 */
test.describe('TEST-B006: Empty Message', () => {
  
  // Use shorter timeout for UI validation tests (no API calls expected)
  test.setTimeout(60000); // 60 seconds for UI-only tests
  
  test('should validate system readiness before testing', async () => {
    console.log('[TEST-B006] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B006] System not ready - errors:', systemStatus.errors);
      test.skip('System not ready for testing');
    }
    
    console.log('[TEST-B006] System validation completed');
    console.log(`[TEST-B006] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B006] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should validate empty message input handling', async ({ browser }) => {
    console.log('[TEST-B006] Starting empty message validation test...');
    
    const sessionManager = new BrowserSessionManager({
      ...COMPREHENSIVE_TEST_CONFIG.browserSession,
      timeout: 60000 // Shorter timeout for UI tests
    });
    let page: any;
    
    try {
      // Initialize browser session (part of continuous session)
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend with dynamic port detection
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B006] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready and validate structure
      await waitForPageReady(page);
      const pageStructure = await validatePageStructure(page);
      
      if (!pageStructure.valid) {
        console.log('[TEST-B006] Page structure invalid:', pageStructure.missingElements);
        throw new Error(`Page structure validation failed: ${pageStructure.missingElements.join(', ')}`);
      }
      
      console.log('[TEST-B006] Page structure validated successfully');
      
      // Find input and submit elements
      const inputSelectors = [
        'textarea[placeholder*="message"]',
        'input[placeholder*="message"]', 
        'textarea',
        '.chat-input textarea',
        '.message-input textarea',
        'input[type="text"]'
      ];
      
      const submitSelectors = [
        'button[type="submit"]',
        '.send-button',
        'button:has-text("Send")',
        '[data-testid="send-button"]',
        'button:has([data-icon="send"])',
        'button'
      ];
      
      let inputElement: any = null;
      let submitElement: any = null;
      
      // Find working input element
      for (const selector of inputSelectors) {
        try {
          const element = page.locator(selector).first();
          const isVisible = await element.isVisible({ timeout: 3000 });
          
          if (isVisible) {
            inputElement = element;
            console.log(`[TEST-B006] Found input element: ${selector}`);
            break;
          }
        } catch (error) {
          // Continue to next selector
        }
      }
      
      // Find working submit element
      for (const selector of submitSelectors) {
        try {
          const element = page.locator(selector).first();
          const isVisible = await element.isVisible({ timeout: 3000 });
          
          if (isVisible) {
            submitElement = element;
            console.log(`[TEST-B006] Found submit element: ${selector}`);
            break;
          }
        } catch (error) {
          // Continue to next selector
        }
      }
      
      // Validate elements found
      expect(inputElement).not.toBeNull();
      expect(submitElement).not.toBeNull();
      
      if (!inputElement || !submitElement) {
        throw new Error('Could not find required input or submit elements');
      }
      
      console.log('[TEST-B006] Required UI elements found and validated');
      
      // Test 1: Empty string input validation
      console.log('[TEST-B006] Testing empty string input...');
      
      await inputElement.clear();
      await inputElement.fill('');
      await page.waitForTimeout(1000); // Allow UI to react
      
      // Check if submit button is disabled for empty input
      const isSubmitDisabledEmpty = await submitElement.isDisabled({ timeout: 2000 }).catch(() => false);
      console.log(`[TEST-B006] Submit button disabled for empty input: ${isSubmitDisabledEmpty}`);
      
      // Test 2: Whitespace-only input validation
      console.log('[TEST-B006] Testing whitespace-only input...');
      
      await inputElement.clear();
      await inputElement.fill('   '); // Multiple spaces
      await page.waitForTimeout(1000); // Allow UI to react
      
      const isSubmitDisabledWhitespace = await submitElement.isDisabled({ timeout: 2000 }).catch(() => false);
      console.log(`[TEST-B006] Submit button disabled for whitespace: ${isSubmitDisabledWhitespace}`);
      
      // Test 3: Tab and newline only input validation
      console.log('[TEST-B006] Testing tab/newline-only input...');
      
      await inputElement.clear();
      await inputElement.fill('\t\n'); // Tab and newline
      await page.waitForTimeout(1000); // Allow UI to react
      
      const isSubmitDisabledSpecial = await submitElement.isDisabled({ timeout: 2000 }).catch(() => false);
      console.log(`[TEST-B006] Submit button disabled for tab/newline: ${isSubmitDisabledSpecial}`);
      
      // Test 4: Try clicking submit with empty input (if not disabled)
      console.log('[TEST-B006] Testing submit button click behavior with empty input...');
      
      await inputElement.clear();
      await inputElement.fill('');
      await page.waitForTimeout(1000);
      
      let clickSucceeded = true;
      let errorMessageAppeared = false;
      
      try {
        // Attempt to click submit button
        await submitElement.click({ timeout: 5000 });
        await page.waitForTimeout(2000); // Allow time for any validation messages
        
        // Check for validation error messages
        errorMessageAppeared = await validateEmptyInputHandling(page);
        
      } catch (error) {
        clickSucceeded = false;
        console.log(`[TEST-B006] Submit button click failed (expected): ${error}`);
      }
      
      console.log(`[TEST-B006] Submit click succeeded: ${clickSucceeded}`);
      console.log(`[TEST-B006] Validation message appeared: ${errorMessageAppeared}`);
      
      // Test 5: Validate proper input allows submission
      console.log('[TEST-B006] Testing valid input enables submission...');
      
      await inputElement.clear();
      await inputElement.fill('test message');
      await page.waitForTimeout(1000); // Allow UI to react
      
      const isSubmitEnabledValid = !(await submitElement.isDisabled({ timeout: 2000 }).catch(() => true));
      console.log(`[TEST-B006] Submit button enabled for valid input: ${isSubmitEnabledValid}`);
      
      // Validation Results Summary
      const validationResults = {
        emptyInputDisabled: isSubmitDisabledEmpty,
        whitespaceInputDisabled: isSubmitDisabledWhitespace,
        specialCharsDisabled: isSubmitDisabledSpecial,
        errorMessageOnClick: errorMessageAppeared,
        validInputEnabled: isSubmitEnabledValid
      };
      
      console.log('[TEST-B006] Empty input validation results:');
      Object.entries(validationResults).forEach(([key, value]) => {
        const status = value ? '✅' : '❌';
        console.log(`[TEST-B006]   ${status} ${key}: ${value}`);
      });
      
      // Assessment: Proper empty input handling
      const hasProperValidation = 
        isSubmitDisabledEmpty ||           // Button disabled for empty input, OR
        isSubmitDisabledWhitespace ||      // Button disabled for whitespace, OR  
        errorMessageAppeared;              // Error message appears on empty submit
      
      console.log(`[TEST-B006] Overall empty input validation: ${hasProperValidation ? '✅ PROPER' : '⚠️ NEEDS IMPROVEMENT'}`);
      
      // Test assertions
      expect(inputElement).not.toBeNull();
      expect(submitElement).not.toBeNull();
      expect(hasProperValidation).toBe(true); // Should have some form of empty input validation
      expect(isSubmitEnabledValid).toBe(true); // Should allow valid input
      
      console.log('[TEST-B006] ✅ Empty message validation test completed successfully');
      
    } catch (error) {
      console.log('[TEST-B006] ❌ Test execution failed:', error);
      throw error;
      
    } finally {
      // Session cleanup (will be part of continuous session in actual test runs)
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate input field behavior and accessibility', async ({ browser }) => {
    console.log('[TEST-B006] Validating input field behavior and accessibility...');
    
    const sessionManager = new BrowserSessionManager({
      ...COMPREHENSIVE_TEST_CONFIG.browserSession,
      timeout: 60000
    });
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await waitForPageReady(page);
      
      // Find input element
      const inputElement = page.locator('textarea, input[type="text"]').first();
      await inputElement.waitFor({ state: 'visible', timeout: 10000 });
      
      // Test input field properties
      console.log('[TEST-B006] Testing input field properties...');
      
      // Check if input is focusable
      await inputElement.focus();
      const isFocused = await inputElement.evaluate((el: any) => document.activeElement === el);
      console.log(`[TEST-B006] Input field focusable: ${isFocused}`);
      
      // Check placeholder text
      const placeholderText = await inputElement.getAttribute('placeholder') || '';
      console.log(`[TEST-B006] Placeholder text: "${placeholderText}"`);
      
      // Test typing behavior
      await inputElement.clear();
      await inputElement.type('Test typing behavior');
      const typedValue = await inputElement.inputValue();
      console.log(`[TEST-B006] Typed value: "${typedValue}"`);
      
      // Test clearing behavior
      await inputElement.clear();
      const clearedValue = await inputElement.inputValue();
      console.log(`[TEST-B006] Cleared value: "${clearedValue}"`);
      
      // Test accessibility attributes
      const ariaLabel = await inputElement.getAttribute('aria-label') || '';
      const ariaDescribedBy = await inputElement.getAttribute('aria-describedby') || '';
      const role = await inputElement.getAttribute('role') || '';
      
      console.log('[TEST-B006] Accessibility attributes:');
      console.log(`[TEST-B006]   aria-label: "${ariaLabel}"`);
      console.log(`[TEST-B006]   aria-describedby: "${ariaDescribedBy}"`);
      console.log(`[TEST-B006]   role: "${role}"`);
      
      // Basic accessibility validation
      const hasBasicAccessibility = 
        placeholderText.length > 0 ||      // Has placeholder text, OR
        ariaLabel.length > 0 ||            // Has aria-label, OR
        ariaDescribedBy.length > 0;        // Has aria-describedby
      
      console.log(`[TEST-B006] Basic accessibility present: ${hasBasicAccessibility}`);
      
      // Validation assertions
      expect(isFocused).toBe(true);
      expect(typedValue).toBe('Test typing behavior');
      expect(clearedValue).toBe('');
      
      console.log('[TEST-B006] ✅ Input field behavior validation completed');
      
    } catch (error) {
      console.log('[TEST-B006] Input field validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate submit button states and behavior', async ({ browser }) => {
    console.log('[TEST-B006] Validating submit button states and behavior...');
    
    const sessionManager = new BrowserSessionManager({
      ...COMPREHENSIVE_TEST_CONFIG.browserSession,
      timeout: 60000
    });
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await waitForPageReady(page);
      
      // Find input and submit elements
      const inputElement = page.locator('textarea, input[type="text"]').first();
      const submitElement = page.locator('button').first();
      
      await inputElement.waitFor({ state: 'visible', timeout: 10000 });
      await submitElement.waitFor({ state: 'visible', timeout: 10000 });
      
      console.log('[TEST-B006] Testing submit button states...');
      
      // Test button properties
      const buttonText = await submitElement.textContent() || '';
      const buttonType = await submitElement.getAttribute('type') || '';
      const buttonClass = await submitElement.getAttribute('class') || '';
      
      console.log(`[TEST-B006] Button text: "${buttonText}"`);
      console.log(`[TEST-B006] Button type: "${buttonType}"`);
      console.log(`[TEST-B006] Button class: "${buttonClass}"`);
      
      // Test button with empty input
      await inputElement.clear();
      await page.waitForTimeout(1000);
      
      const initialState = await submitElement.isEnabled();
      const initialDisabled = await submitElement.isDisabled().catch(() => false);
      
      console.log(`[TEST-B006] Initial button state - Enabled: ${initialState}, Disabled: ${initialDisabled}`);
      
      // Test button with valid input
      await inputElement.fill('valid test message');
      await page.waitForTimeout(1000);
      
      const validInputState = await submitElement.isEnabled();
      console.log(`[TEST-B006] Button state with valid input - Enabled: ${validInputState}`);
      
      // Test button visual states (if CSS classes change)
      const buttonClassWithEmpty = await submitElement.getAttribute('class') || '';
      await inputElement.fill('test');
      await page.waitForTimeout(1000);
      const buttonClassWithText = await submitElement.getAttribute('class') || '';
      
      const classesChanged = buttonClassWithEmpty !== buttonClassWithText;
      console.log(`[TEST-B006] Button CSS classes change with input: ${classesChanged}`);
      if (classesChanged) {
        console.log(`[TEST-B006]   Empty: "${buttonClassWithEmpty}"`);
        console.log(`[TEST-B006]   With text: "${buttonClassWithText}"`);
      }
      
      // Test button hover behavior (desktop)
      await submitElement.hover();
      await page.waitForTimeout(500);
      const buttonClassOnHover = await submitElement.getAttribute('class') || '';
      const hoverStateExists = buttonClassOnHover !== buttonClassWithText;
      
      console.log(`[TEST-B006] Button has hover state: ${hoverStateExists}`);
      
      // Button behavior validation summary
      const buttonBehavior = {
        hasText: buttonText.length > 0,
        respondsToInput: initialState !== validInputState || classesChanged,
        hasHoverState: hoverStateExists,
        isAccessible: buttonText.length > 0 || buttonClass.includes('button') || buttonType === 'submit'
      };
      
      console.log('[TEST-B006] Submit button behavior summary:');
      Object.entries(buttonBehavior).forEach(([key, value]) => {
        const status = value ? '✅' : '⚠️';
        console.log(`[TEST-B006]   ${status} ${key}: ${value}`);
      });
      
      // Validation assertions
      expect(buttonBehavior.hasText || buttonBehavior.isAccessible).toBe(true);
      
      console.log('[TEST-B006] ✅ Submit button behavior validation completed');
      
    } catch (error) {
      console.log('[TEST-B006] Submit button validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B006 development
 */
test.describe('TEST-B006: Development Utilities', () => {
  
  test('should validate TEST-B006 configuration', async () => {
    console.log('[TEST-B006] Validating test configuration...');
    
    // Validate empty input test data
    const emptyInputs = COMPREHENSIVE_TEST_CONFIG.testData.emptyInputs;
    expect(emptyInputs).toContain('');
    expect(emptyInputs).toContain('   ');
    expect(emptyInputs).toContain('\n');
    expect(emptyInputs).toContain('\t');
    
    console.log(`[TEST-B006] Empty input test data: ${JSON.stringify(emptyInputs)}`);
    
    // Validate input selectors
    const inputSelectors = COMPREHENSIVE_TEST_CONFIG.messageInput.inputSelector.split(',');
    expect(inputSelectors.length).toBeGreaterThan(0);
    console.log(`[TEST-B006] Input selectors: ${inputSelectors.join(', ')}`);
    
    // Validate submit selectors  
    const submitSelectors = COMPREHENSIVE_TEST_CONFIG.messageInput.submitSelector.split(',');
    expect(submitSelectors.length).toBeGreaterThan(0);
    console.log(`[TEST-B006] Submit selectors: ${submitSelectors.join(', ')}`);
    
    console.log('[TEST-B006] Configuration validation completed');
  });
  
  test('should validate empty input patterns', async () => {
    console.log('[TEST-B006] Testing empty input pattern recognition...');
    
    const testInputs = [
      { input: '', expected: true, description: 'empty string' },
      { input: '   ', expected: true, description: 'spaces only' },
      { input: '\t', expected: true, description: 'tab only' },
      { input: '\n', expected: true, description: 'newline only' },
      { input: '\t\n  ', expected: true, description: 'mixed whitespace' },
      { input: 'a', expected: false, description: 'single character' },
      { input: ' a ', expected: false, description: 'character with spaces' },
      { input: '123', expected: false, description: 'numbers' }
    ];
    
    testInputs.forEach(test => {
      const isEmpty = /^\s*$/.test(test.input);
      const matches = isEmpty === test.expected;
      const status = matches ? '✅' : '❌';
      
      console.log(`[TEST-B006] ${status} ${test.description}: "${test.input}" -> isEmpty: ${isEmpty} (expected: ${test.expected})`);
      expect(matches).toBe(true);
    });
    
    console.log('[TEST-B006] Empty input pattern validation completed');
  });
  
  test('should validate UI element detection patterns', async () => {
    console.log('[TEST-B006] Validating UI element detection patterns...');
    
    // Test CSS selector patterns for common UI elements
    const selectorPatterns = [
      { pattern: 'textarea[placeholder*="message"]', description: 'textarea with message placeholder' },
      { pattern: 'input[placeholder*="message"]', description: 'input with message placeholder' },
      { pattern: 'button[type="submit"]', description: 'submit button' },
      { pattern: 'button:has-text("Send")', description: 'button with Send text' },
      { pattern: '[data-testid="send-button"]', description: 'button with test ID' }
    ];
    
    selectorPatterns.forEach(({ pattern, description }) => {
      // Validate selector syntax (basic validation)
      const isValidSelector = /^[a-zA-Z0-9\[\]\=\*\"\:\-\(\)\.\_\s\,\>]+$/.test(pattern);
      const status = isValidSelector ? '✅' : '❌';
      
      console.log(`[TEST-B006] ${status} ${description}: ${pattern}`);
      expect(isValidSelector).toBe(true);
    });
    
    console.log('[TEST-B006] UI element detection patterns validation completed');
  });
  
});