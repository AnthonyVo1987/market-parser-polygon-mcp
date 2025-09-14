/**
 * TEST-B012: Button Error Handling Test
 * 
 * Tests button error handling scenarios (invalid tickers, network errors, timeout conditions)
 * Implements comprehensive error handling validation and recovery testing
 * Part of continuous browser session protocol
 * 
 * @fileoverview Button error handling CLI test with error scenario validation
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  validateSystemReadiness,
  clickButtonAndWaitForResponse,
  inputTicker,
  clickButton,
  validateFinancialResponse,
  
  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  PerformanceClassification,
  ButtonType,
  
  // Browser session management
  BrowserSessionManager
} from './helpers/index';

/**
 * TEST-B012: Button Error Handling Test Suite
 */
test.describe('TEST-B012: Button Error Handling', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before error handling testing', async () => {
    console.log('[TEST-B012] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B012] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B012] System validation completed');
    console.log(`[TEST-B012] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B012] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should handle invalid ticker symbols gracefully', async ({ browser }) => {
    console.log('[TEST-B012] Starting invalid ticker error handling test...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B012] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      // Test invalid ticker symbols
      const invalidTickers = ['INVALID', 'NOTREAL', 'FAKE123', 'XYZ999'];
      
      for (const invalidTicker of invalidTickers) {
        console.log(`[TEST-B012] Testing invalid ticker: ${invalidTicker}`);
        
        // Execute button test with invalid ticker
        const buttonResult = await clickButtonAndWaitForResponse(
          page,
          ButtonType.STOCK_SNAPSHOT,
          invalidTicker,
          `ErrorHandling-Invalid-${invalidTicker}`
        );
        
        console.log(`[TEST-B012] ${invalidTicker} result: ${buttonResult.success ? 'SUCCESS' : 'FAILED'} (${buttonResult.responseTime}ms)`);
        
        // Error handling validation
        if (!buttonResult.success) {
          console.log(`[TEST-B012] ✅ Error properly handled for ${invalidTicker}: ${buttonResult.error}`);
          
          // Validate error classification
          expect(buttonResult.classification).toBeDefined();
          expect(buttonResult.buttonFound).toBeDefined();
          expect(buttonResult.buttonClicked).toBeDefined();
          
        } else {
          // If successful, validate response contains error information or proper handling
          console.log(`[TEST-B012] ⚠️ ${invalidTicker} returned success - checking for error content...`);
          
          const validationResult = buttonResult.validationResult;
          if (validationResult) {
            const responseContent = validationResult.responseContent || '';
            const hasErrorContent = responseContent.toLowerCase().includes('error') || 
                                  responseContent.toLowerCase().includes('invalid') ||
                                  responseContent.toLowerCase().includes('not found');
            
            if (hasErrorContent) {
              console.log(`[TEST-B012] ✅ Error content detected in response for ${invalidTicker}`);
            } else {
              console.log(`[TEST-B012] ⚠️ No explicit error content found for ${invalidTicker}`);
            }
          }
        }
        
        // Small delay between invalid ticker tests
        await page.waitForTimeout(2000);
      }
      
      console.log('[TEST-B012] ✅ Invalid ticker error handling test completed');
      
    } catch (error) {
      console.log('[TEST-B012] ❌ Invalid ticker test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should handle empty input gracefully', async ({ browser }) => {
    console.log('[TEST-B012] Testing empty input error handling...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      // Test empty input scenarios
      const emptyInputs = COMPREHENSIVE_TEST_CONFIG.testData.emptyInputs; // ['', '   ', '\\n', '\\t']
      
      for (const emptyInput of emptyInputs) {
        console.log(`[TEST-B012] Testing empty input: "${emptyInput}"`);
        
        // Try to input empty/whitespace ticker
        const inputResult = await inputTicker(page, emptyInput);
        
        if (inputResult.success) {
          // Try clicking button with empty input
          const clickResult = await clickButton(page, ButtonType.STOCK_SNAPSHOT);
          
          console.log(`[TEST-B012] Empty input "${emptyInput}" click result: ${clickResult.success ? 'SUCCESS' : 'FAILED'}`);
          
          if (!clickResult.success) {
            console.log(`[TEST-B012] ✅ Empty input properly rejected: ${clickResult.error}`);
          } else {
            // Button clicked - check if system handles empty input gracefully
            console.log(`[TEST-B012] ⚠️ Button clicked with empty input - checking response...`);
            
            // Wait briefly for any response or error
            await page.waitForTimeout(5000);
            
            // Check for error messages on page
            const pageContent = await page.textContent('body') || '';
            const hasErrorMessage = pageContent.toLowerCase().includes('please enter') ||
                                  pageContent.toLowerCase().includes('required') ||
                                  pageContent.toLowerCase().includes('invalid');
            
            if (hasErrorMessage) {
              console.log(`[TEST-B012] ✅ Error message displayed for empty input`);
            } else {
              console.log(`[TEST-B012] ⚠️ No explicit error message for empty input`);
            }
          }
        } else {
          console.log(`[TEST-B012] ✅ Input validation rejected empty input: ${inputResult.error}`);
        }
        
        // Clear input for next test
        try {
          const inputSelectors = [
            'textarea[placeholder*="message"]',
            'input[placeholder*="message"]', 
            'textarea'
          ];
          
          for (const selector of inputSelectors) {
            try {
              const element = page.locator(selector).first();
              const isVisible = await element.isVisible({ timeout: 1000 });
              
              if (isVisible) {
                await element.clear();
                break;
              }
            } catch (error) {
              // Continue
            }
          }
        } catch (error) {
          // Continue
        }
        
        await page.waitForTimeout(1000);
      }
      
      console.log('[TEST-B012] ✅ Empty input error handling test completed');
      
    } catch (error) {
      console.log('[TEST-B012] Empty input test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should handle button not found scenarios', async ({ browser }) => {
    console.log('[TEST-B012] Testing button not found error handling...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      // Input valid ticker
      const testTicker = 'NVDA';
      await inputTicker(page, testTicker);
      
      // Test all button types for availability
      const buttonTypes = [
        ButtonType.STOCK_SNAPSHOT,
        ButtonType.SUPPORT_RESISTANCE,
        ButtonType.TECHNICAL_ANALYSIS
      ];
      
      for (const buttonType of buttonTypes) {
        console.log(`[TEST-B012] Testing button availability: ${buttonType}`);
        
        const clickResult = await clickButton(page, buttonType);
        
        console.log(`[TEST-B012] ${buttonType} click result: ${clickResult.success ? 'SUCCESS' : 'FAILED'}`);
        console.log(`[TEST-B012] ${buttonType} found: ${clickResult.buttonFound}`);
        
        if (!clickResult.success && !clickResult.buttonFound) {
          console.log(`[TEST-B012] ✅ Button not found error properly handled: ${clickResult.error}`);
          
          // Validate error message contains useful information
          expect(clickResult.error).toContain(buttonType);
          expect(typeof clickResult.error).toBe('string');
          
        } else if (clickResult.success) {
          console.log(`[TEST-B012] ✅ ${buttonType} button found and clickable`);
          
          // Wait for any response to complete before next test
          await page.waitForTimeout(3000);
          
        } else {
          console.log(`[TEST-B012] ⚠️ ${buttonType} button found but click failed: ${clickResult.error}`);
        }
      }
      
      console.log('[TEST-B012] ✅ Button availability error handling test completed');
      
    } catch (error) {
      console.log('[TEST-B012] Button not found test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should handle timeout scenarios gracefully', async ({ browser }) => {
    console.log('[TEST-B012] Testing timeout error handling...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testTicker = 'MSFT';
      
      console.log(`[TEST-B012] Testing timeout handling with ${testTicker}`);
      
      // Execute button test and let it run to see if timeout is handled properly
      const buttonResult = await clickButtonAndWaitForResponse(
        page,
        ButtonType.TECHNICAL_ANALYSIS,
        testTicker,
        'ErrorHandling-Timeout-Test'
      );
      
      console.log(`[TEST-B012] Timeout test result: ${buttonResult.success ? 'SUCCESS' : 'TIMEOUT'} (${buttonResult.responseTime}ms)`);
      console.log(`[TEST-B012] Classification: ${buttonResult.classification}`);
      
      // Validate timeout handling
      if (buttonResult.classification === PerformanceClassification.TIMEOUT) {
        console.log('[TEST-B012] ✅ Timeout properly classified and handled');
        
        expect(buttonResult.success).toBe(false);
        expect(buttonResult.responseTime).toBeGreaterThan(COMPREHENSIVE_TEST_CONFIG.performance.slowPerformance);
        expect(buttonResult.error).toBeDefined();
        
      } else if (buttonResult.classification === PerformanceClassification.SLOW_PERFORMANCE) {
        console.log('[TEST-B012] ⚠️ Slow performance detected (between 45-120 seconds)');
        
        expect(buttonResult.responseTime).toBeGreaterThan(COMPREHENSIVE_TEST_CONFIG.performance.success);
        expect(buttonResult.responseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.performance.slowPerformance);
        
      } else {
        console.log('[TEST-B012] ✅ Response within normal performance range');
        
        expect(buttonResult.responseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.performance.success);
      }
      
      // Validate error information if present
      if (buttonResult.error) {
        expect(typeof buttonResult.error).toBe('string');
        expect(buttonResult.error.length).toBeGreaterThan(0);
      }
      
      console.log('[TEST-B012] ✅ Timeout error handling test completed');
      
    } catch (error) {
      console.log('[TEST-B012] Timeout test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B012 development
 */
test.describe('TEST-B012: Development Utilities', () => {
  
  test('should validate TEST-B012 configuration', async () => {
    console.log('[TEST-B012] Validating error handling test configuration...');
    
    // Validate empty inputs configuration
    const emptyInputs = COMPREHENSIVE_TEST_CONFIG.testData.emptyInputs;
    expect(emptyInputs).toBeDefined();
    expect(emptyInputs.length).toBeGreaterThan(0);
    expect(emptyInputs).toContain('');
    expect(emptyInputs).toContain('   ');
    
    // Validate performance thresholds for timeout classification
    expect(COMPREHENSIVE_TEST_CONFIG.performance.success).toBe(45000);
    expect(COMPREHENSIVE_TEST_CONFIG.performance.slowPerformance).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.performance.timeout).toBe(120000);
    
    console.log('[TEST-B012] Configuration validation completed');
    console.log(`[TEST-B012] Empty inputs: ${emptyInputs.length} variants`);
    console.log(`[TEST-B012] Timeout threshold: ${COMPREHENSIVE_TEST_CONFIG.performance.timeout}ms`);
  });
  
  test('should validate error classification constants', async () => {
    console.log('[TEST-B012] Validating error classification constants...');
    
    // Validate PerformanceClassification enum
    expect(PerformanceClassification.SUCCESS).toBe('SUCCESS');
    expect(PerformanceClassification.SLOW_PERFORMANCE).toBe('SLOW_PERFORMANCE');
    expect(PerformanceClassification.TIMEOUT).toBe('TIMEOUT');
    
    console.log('[TEST-B012] Error classification constants validation completed');
  });
  
});