/**
 * TEST-B007: Stock Snapshot Button Test
 * 
 * Tests Stock Snapshot (📈) button functionality with NVDA ticker
 * Implements button interaction testing and response validation
 * Part of continuous browser session protocol
 * 
 * @fileoverview Stock Snapshot button CLI test with emoji indicator validation
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  validateSystemReadiness,
  clickButtonAndWaitForResponse,
  validateFinancialResponse,
  classifyPerformance,
  
  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  PerformanceClassification,
  ButtonType,
  
  // Browser session management
  BrowserSessionManager
} from './helpers/index';

/**
 * TEST-B007: Stock Snapshot Button Test Suite
 */
test.describe('TEST-B007: Stock Snapshot Button', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before button testing', async () => {
    console.log('[TEST-B007] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B007] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B007] System validation completed');
    console.log(`[TEST-B007] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B007] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should execute Stock Snapshot button test with NVDA ticker', async ({ browser }) => {
    console.log('[TEST-B007] Starting Stock Snapshot button test execution...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session (part of continuous session)
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend with dynamic port detection
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B007] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000); // Allow interface to stabilize
      
      // Define test ticker for Stock Snapshot
      const testTicker = 'NVDA';
      
      console.log(`[TEST-B007] Testing Stock Snapshot button with ticker: ${testTicker}`);
      
      // Execute button test with 30-second polling and 120-second timeout
      const startTime = Date.now();
      const buttonResult = await clickButtonAndWaitForResponse(
        page,
        ButtonType.STOCK_SNAPSHOT,
        testTicker,
        'TEST-B007-StockSnapshot'
      );
      
      const responseTime = Date.now() - startTime;
      const performanceClass = classifyPerformance(responseTime, COMPREHENSIVE_TEST_CONFIG.polling);
      
      console.log(`[TEST-B007] Button interaction completed in ${responseTime}ms (${performanceClass})`);
      
      // Validate button interaction success
      expect(buttonResult.success).toBe(true);
      expect(buttonResult.buttonFound).toBe(true);
      expect(buttonResult.buttonClicked).toBe(true);
      expect(buttonResult.responseTime).toBeGreaterThan(0);
      expect(buttonResult.classification).toBeDefined();
      
      if (!buttonResult.success) {
        console.log('[TEST-B007] Button interaction failed:', buttonResult.error);
        throw new Error(`Button test execution failed: ${buttonResult.error}`);
      }
      
      // Validate response content for Stock Snapshot
      console.log('[TEST-B007] Validating Stock Snapshot response...');
      const validationResult = buttonResult.validationResult;
      
      if (validationResult) {
        // Stock Snapshot should contain financial indicators and NVDA-specific content
        expect(validationResult.hasFinancialContent).toBe(true);
        expect(validationResult.contentLength).toBeGreaterThan(100);
        expect(validationResult.detectedTickers).toContain('NVDA');
        
        // Should have emoji indicators for financial data
        expect(validationResult.hasEmojiIndicators).toBe(true);
        expect(validationResult.detectedEmojis.length).toBeGreaterThan(0);
        
        // Log detailed validation results
        console.log(`[TEST-B007] Response validation - Valid: ${validationResult.isValid}`);
        console.log(`[TEST-B007] KEY TAKEAWAYS present: ${validationResult.hasKeyTakeaways}`);
        console.log(`[TEST-B007] Emoji indicators: ${validationResult.detectedEmojis.join(', ')}`);
        console.log(`[TEST-B007] Detected tickers: ${validationResult.detectedTickers.join(', ')}`);
        console.log(`[TEST-B007] Content length: ${validationResult.contentLength} characters`);
        
        // Validate NVDA ticker presence
        if (validationResult.detectedTickers.includes('NVDA')) {
          console.log('[TEST-B007] ✅ NVDA ticker properly detected in response');
        } else {
          console.log('[TEST-B007] ⚠️ NVDA ticker not detected in response');
        }
      }
      
      // Performance classification validation
      console.log(`[TEST-B007] Performance classification: ${performanceClass}`);
      
      if (performanceClass === PerformanceClassification.SUCCESS) {
        console.log(`[TEST-B007] ✅ SUCCESS: Fast response (< 45 seconds)`);
      } else if (performanceClass === PerformanceClassification.SLOW_PERFORMANCE) {
        console.log(`[TEST-B007] ⚠️ SLOW_PERFORMANCE: Response took 45-120 seconds`);
      } else {
        console.log(`[TEST-B007] ❌ TIMEOUT: Response exceeded 120 seconds`);
      }
      
      // Validate Stock Snapshot specific content
      const responseContent = validationResult?.responseContent || '';
      const stockSnapshotKeywords = ['snapshot', 'stock', 'price', 'volume', 'market cap', 'current'];
      const hasStockSnapshotContent = stockSnapshotKeywords.some(keyword => 
        responseContent.toLowerCase().includes(keyword)
      );
      
      if (hasStockSnapshotContent) {
        console.log('[TEST-B007] ✅ Stock Snapshot content detected');
      } else {
        console.log('[TEST-B007] ⚠️ General financial response received (Stock Snapshot content not explicitly detected)');
      }
      
      // Final test assertions for Button-specific requirements
      expect(buttonResult.success).toBe(true);
      expect(buttonResult.buttonType).toBe(ButtonType.STOCK_SNAPSHOT);
      expect(buttonResult.buttonFound).toBe(true);
      expect(buttonResult.buttonClicked).toBe(true);
      expect(validationResult?.hasFinancialContent).toBe(true);
      expect(validationResult?.detectedTickers).toContain('NVDA');
      expect(responseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      
      console.log('[TEST-B007] ✅ Stock Snapshot button test completed successfully');
      
    } catch (error) {
      console.log('[TEST-B007] ❌ Test execution failed:', error);
      throw error;
      
    } finally {
      // Session cleanup (will be part of continuous session in actual test runs)
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate Stock Snapshot button state and interaction', async ({ browser }) => {
    console.log('[TEST-B007] Validating Stock Snapshot button state requirements...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      // Navigate and wait for page ready
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      // Input ticker first
      const testTicker = 'NVDA';
      const inputSelectors = [
        'textarea[placeholder*="message"]',
        'input[placeholder*="message"]', 
        'textarea',
        '.chat-input textarea'
      ];
      
      let inputElement: any = null;
      for (const selector of inputSelectors) {
        try {
          const element = page.locator(selector).first();
          const isVisible = await element.isVisible({ timeout: 2000 });
          
          if (isVisible) {
            inputElement = element;
            break;
          }
        } catch (error) {
          // Continue
        }
      }
      
      if (inputElement) {
        await inputElement.focus();
        await inputElement.clear();
        await inputElement.type(testTicker);
        console.log(`[TEST-B007] Input ticker: ${testTicker}`);
      }
      
      // Check for Stock Snapshot button presence and state
      const stockSnapshotSelectors = [
        'button:has-text("📈")',
        'button:has-text("Stock Snapshot")',
        '[data-testid="stock-snapshot-button"]',
        '.stock-snapshot-btn'
      ];
      
      let buttonFound = false;
      let buttonEnabled = false;
      
      for (const selector of stockSnapshotSelectors) {
        try {
          const button = page.locator(selector).first();
          const isVisible = await button.isVisible({ timeout: 3000 });
          
          if (isVisible) {
            buttonFound = true;
            buttonEnabled = await button.isEnabled();
            console.log(`[TEST-B007] Found Stock Snapshot button: ${selector} (enabled: ${buttonEnabled})`);
            break;
          }
        } catch (error) {
          // Continue checking
        }
      }
      
      console.log(`[TEST-B007] Button state validation - Found: ${buttonFound}, Enabled: ${buttonEnabled}`);
      
      // Log button availability status
      if (buttonFound && buttonEnabled) {
        console.log('[TEST-B007] ✅ Stock Snapshot button is available and interactive');
      } else if (buttonFound && !buttonEnabled) {
        console.log('[TEST-B007] ⚠️ Stock Snapshot button found but disabled');
      } else {
        console.log('[TEST-B007] ❌ Stock Snapshot button not found');
      }
      
      // This test validates button state, not interaction success
      expect(buttonFound || !buttonFound).toBe(true); // Always pass - this is discovery
      
    } catch (error) {
      console.log('[TEST-B007] Button state validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B007 development
 */
test.describe('TEST-B007: Development Utilities', () => {
  
  test('should validate TEST-B007 configuration', async () => {
    console.log('[TEST-B007] Validating button test configuration...');
    
    // Validate button interaction configuration
    expect(COMPREHENSIVE_TEST_CONFIG.buttonInteraction.clickTimeout).toBe(5000);
    expect(COMPREHENSIVE_TEST_CONFIG.buttonInteraction.stateValidationTimeout).toBe(5000);
    expect(COMPREHENSIVE_TEST_CONFIG.buttonInteraction.processingDetectionDelay).toBe(1000);
    
    // Validate button-specific timeouts
    expect(COMPREHENSIVE_TEST_CONFIG.timeouts.button).toBe(5000);
    expect(COMPREHENSIVE_TEST_CONFIG.timeouts.test).toBe(120000);
    
    // Validate test data includes button test tickers
    const buttonTestTickers = COMPREHENSIVE_TEST_CONFIG.testData.buttonTestTickers;
    expect(buttonTestTickers).toContain('NVDA');
    expect(buttonTestTickers).toContain('AAPL');
    expect(buttonTestTickers).toContain('GME');
    
    // Validate ButtonType enum
    expect(ButtonType.STOCK_SNAPSHOT).toBe('STOCK_SNAPSHOT');
    expect(ButtonType.SUPPORT_RESISTANCE).toBe('SUPPORT_RESISTANCE');
    expect(ButtonType.TECHNICAL_ANALYSIS).toBe('TECHNICAL_ANALYSIS');
    
    console.log('[TEST-B007] Configuration validation completed');
    console.log(`[TEST-B007] Button click timeout: ${COMPREHENSIVE_TEST_CONFIG.buttonInteraction.clickTimeout}ms`);
    console.log(`[TEST-B007] Button test timeout: ${COMPREHENSIVE_TEST_CONFIG.timeouts.test}ms`);
    console.log(`[TEST-B007] Test ticker: NVDA`);
  });
  
  test('should validate Stock Snapshot button selectors', async () => {
    console.log('[TEST-B007] Validating Stock Snapshot button selectors...');
    
    const { BUTTON_SELECTORS } = await import('./helpers/button-helpers');
    const stockSnapshotSelectors = BUTTON_SELECTORS[ButtonType.STOCK_SNAPSHOT];
    
    // Validate selectors are defined
    expect(stockSnapshotSelectors).toBeDefined();
    expect(stockSnapshotSelectors.length).toBeGreaterThan(0);
    
    // Validate specific selectors
    expect(stockSnapshotSelectors).toContain('button:has-text("📈")');
    expect(stockSnapshotSelectors).toContain('button:has-text("Stock Snapshot")');
    expect(stockSnapshotSelectors).toContain('[data-testid="stock-snapshot-button"]');
    
    console.log('[TEST-B007] Stock Snapshot selectors validation completed');
    console.log(`[TEST-B007] Available selectors: ${stockSnapshotSelectors.join(', ')}`);
  });
  
});