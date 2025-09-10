/**
 * TEST-B010: Multi-Button Interaction Test
 * 
 * Tests multiple button interactions in sequence with single ticker
 * Implements multi-button workflow testing and response validation
 * Part of continuous browser session protocol
 * 
 * @fileoverview Multi-button interaction CLI test with comprehensive validation
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  validateSystemReadiness,
  executeMultiButtonTest,
  clickButtonAndWaitForResponse,
  validateFinancialResponse,
  generateButtonTestReport,
  classifyPerformance,
  
  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  PerformanceClassification,
  ButtonType,
  
  // Browser session management
  BrowserSessionManager
} from './helpers/index';

/**
 * TEST-B010: Multi-Button Interaction Test Suite
 */
test.describe('TEST-B010: Multi-Button Interaction', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before multi-button testing', async () => {
    console.log('[TEST-B010] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B010] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B010] System validation completed');
    console.log(`[TEST-B010] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B010] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should execute all three button types in sequence with NVDA ticker', async ({ browser }) => {
    console.log('[TEST-B010] Starting multi-button interaction test execution...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session (part of continuous session)
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend with dynamic port detection
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B010] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000); // Allow interface to stabilize
      
      // Define test ticker and button sequence
      const testTicker = 'NVDA';
      const buttonSequence = [
        ButtonType.STOCK_SNAPSHOT,
        ButtonType.SUPPORT_RESISTANCE,
        ButtonType.TECHNICAL_ANALYSIS
      ];
      
      console.log(`[TEST-B010] Testing multi-button sequence with ticker: ${testTicker}`);
      console.log(`[TEST-B010] Button sequence: ${buttonSequence.join(' → ')}`);
      
      // Execute multi-button test
      const startTime = Date.now();
      const buttonResults = await executeMultiButtonTest(page, buttonSequence, testTicker);
      const totalResponseTime = Date.now() - startTime;
      
      console.log(`[TEST-B010] Multi-button interaction completed in ${totalResponseTime}ms`);
      
      // Validate all button interactions succeeded
      expect(buttonResults.length).toBe(3);
      
      // Check each button result
      buttonResults.forEach((result, index) => {
        const buttonType = buttonSequence[index];
        console.log(`[TEST-B010] Button ${index + 1} (${buttonType}): ${result.success ? 'SUCCESS' : 'FAILED'} (${result.responseTime}ms)`);
        
        expect(result.success).toBe(true);
        expect(result.buttonFound).toBe(true);
        expect(result.buttonClicked).toBe(true);
        expect(result.buttonType).toBe(buttonType);
        expect(result.responseTime).toBeGreaterThan(0);
        
        if (result.validationResult) {
          expect(result.validationResult.hasFinancialContent).toBe(true);
          expect(result.validationResult.detectedTickers).toContain('NVDA');
        }
      });
      
      // Generate comprehensive report
      const report = generateButtonTestReport(buttonResults);
      
      console.log(`[TEST-B010] Multi-button test report:`);
      console.log(`[TEST-B010] Total tests: ${report.summary.totalTests}`);
      console.log(`[TEST-B010] Successful: ${report.summary.successCount}`);
      console.log(`[TEST-B010] Buttons found: ${report.summary.buttonFoundCount}`);
      console.log(`[TEST-B010] Buttons clicked: ${report.summary.buttonClickedCount}`);
      console.log(`[TEST-B010] Average response time: ${Math.round(report.summary.averageResponseTime)}ms`);
      
      // Performance classification for overall test
      const averagePerformance = classifyPerformance(report.summary.averageResponseTime, COMPREHENSIVE_TEST_CONFIG.polling);
      console.log(`[TEST-B010] Overall performance classification: ${averagePerformance}`);
      
      // Validate report expectations
      expect(report.summary.totalTests).toBe(3);
      expect(report.summary.successCount).toBe(3);
      expect(report.summary.buttonFoundCount).toBe(3);
      expect(report.summary.buttonClickedCount).toBe(3);
      expect(report.summary.averageResponseTime).toBeGreaterThan(0);
      
      // Validate button type statistics
      expect(report.buttonTypes[ButtonType.STOCK_SNAPSHOT].tested).toBe(1);
      expect(report.buttonTypes[ButtonType.SUPPORT_RESISTANCE].tested).toBe(1);
      expect(report.buttonTypes[ButtonType.TECHNICAL_ANALYSIS].tested).toBe(1);
      
      console.log('[TEST-B010] ✅ Multi-button interaction test completed successfully');
      
    } catch (error) {
      console.log('[TEST-B010] ❌ Test execution failed:', error);
      throw error;
      
    } finally {
      // Session cleanup (will be part of continuous session in actual test runs)
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should execute two-button combinations with different tickers', async ({ browser }) => {
    console.log('[TEST-B010] Testing two-button combinations...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      // Test combinations from configuration
      const buttonCombinations = COMPREHENSIVE_TEST_CONFIG.testData.buttonCombinations;
      const twoButtonCombinations = buttonCombinations.filter(combo => combo.length === 2);
      
      console.log(`[TEST-B010] Testing ${twoButtonCombinations.length} two-button combinations`);
      
      for (let i = 0; i < twoButtonCombinations.length; i++) {
        const combination = twoButtonCombinations[i];
        const testTicker = ['AAPL', 'MSFT', 'GOOGL'][i % 3]; // Rotate tickers
        
        console.log(`[TEST-B010] --- Combination ${i + 1}: ${combination.join(' + ')} with ${testTicker} ---`);
        
        // Small delay between combinations
        if (i > 0) {
          await page.waitForTimeout(5000);
        }
        
        // Convert string array to ButtonType array
        const buttonTypes = combination.map(buttonStr => ButtonType[buttonStr as keyof typeof ButtonType]);
        
        const results = await executeMultiButtonTest(page, buttonTypes, testTicker);
        
        // Validate combination results
        expect(results.length).toBe(2);
        results.forEach(result => {
          expect(result.success).toBe(true);
          expect(result.buttonFound).toBe(true);
          expect(result.buttonClicked).toBe(true);
        });
        
        console.log(`[TEST-B010] Combination ${i + 1} completed: ${results.filter(r => r.success).length}/2 successful`);
      }
      
      console.log('[TEST-B010] ✅ Two-button combinations testing completed');
      
    } catch (error) {
      console.log('[TEST-B010] Two-button combinations failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate multi-button workflow with delays and state transitions', async ({ browser }) => {
    console.log('[TEST-B010] Validating multi-button workflow state transitions...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testTicker = 'SPY';
      
      // Test workflow: Input → Button 1 → Wait → Button 2 → Wait → Button 3
      console.log(`[TEST-B010] Testing workflow state transitions with ${testTicker}`);
      
      // Step 1: Stock Snapshot
      console.log('[TEST-B010] Step 1: Stock Snapshot');
      const result1 = await clickButtonAndWaitForResponse(
        page,
        ButtonType.STOCK_SNAPSHOT,
        testTicker,
        'Workflow-Step1'
      );
      
      expect(result1.success).toBe(true);
      console.log(`[TEST-B010] Step 1 completed: ${result1.responseTime}ms`);
      
      // Delay between steps
      await page.waitForTimeout(COMPREHENSIVE_TEST_CONFIG.buttonInteraction.multiButtonDelay);
      
      // Step 2: Support & Resistance (reuse same ticker input)
      console.log('[TEST-B010] Step 2: Support & Resistance');
      const result2 = await clickButtonAndWaitForResponse(
        page,
        ButtonType.SUPPORT_RESISTANCE,
        undefined, // Don't re-input ticker
        'Workflow-Step2'
      );
      
      expect(result2.success).toBe(true);
      console.log(`[TEST-B010] Step 2 completed: ${result2.responseTime}ms`);
      
      // Delay between steps
      await page.waitForTimeout(COMPREHENSIVE_TEST_CONFIG.buttonInteraction.multiButtonDelay);
      
      // Step 3: Technical Analysis (reuse same ticker input)
      console.log('[TEST-B010] Step 3: Technical Analysis');
      const result3 = await clickButtonAndWaitForResponse(
        page,
        ButtonType.TECHNICAL_ANALYSIS,
        undefined, // Don't re-input ticker
        'Workflow-Step3'
      );
      
      expect(result3.success).toBe(true);
      console.log(`[TEST-B010] Step 3 completed: ${result3.responseTime}ms`);
      
      // Validate workflow timing
      const totalWorkflowTime = result1.responseTime + result2.responseTime + result3.responseTime;
      console.log(`[TEST-B010] Total workflow time: ${totalWorkflowTime}ms`);
      
      // All steps should complete within overall test timeout
      expect(totalWorkflowTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      
      console.log('[TEST-B010] ✅ Multi-button workflow validation completed');
      
    } catch (error) {
      console.log('[TEST-B010] Workflow validation failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B010 development
 */
test.describe('TEST-B010: Development Utilities', () => {
  
  test('should validate TEST-B010 configuration', async () => {
    console.log('[TEST-B010] Validating multi-button test configuration...');
    
    // Validate multi-button delay configuration
    expect(COMPREHENSIVE_TEST_CONFIG.buttonInteraction.multiButtonDelay).toBe(3000);
    
    // Validate button combinations are defined
    const combinations = COMPREHENSIVE_TEST_CONFIG.testData.buttonCombinations;
    expect(combinations).toBeDefined();
    expect(combinations.length).toBeGreaterThan(0);
    
    // Validate single button combinations
    const singleButtonCombos = combinations.filter(combo => combo.length === 1);
    expect(singleButtonCombos.length).toBe(3); // Should have all 3 individual buttons
    
    // Validate two-button combinations
    const twoButtonCombos = combinations.filter(combo => combo.length === 2);
    expect(twoButtonCombos.length).toBe(3); // Should have 3 two-button combinations
    
    console.log('[TEST-B010] Configuration validation completed');
    console.log(`[TEST-B010] Multi-button delay: ${COMPREHENSIVE_TEST_CONFIG.buttonInteraction.multiButtonDelay}ms`);
    console.log(`[TEST-B010] Button combinations: ${combinations.length} total`);
  });
  
  test('should validate executeMultiButtonTest function', async () => {
    console.log('[TEST-B010] Validating executeMultiButtonTest function...');
    
    const { executeMultiButtonTest } = await import('./helpers/button-helpers');
    
    // Validate function is available
    expect(executeMultiButtonTest).toBeDefined();
    expect(typeof executeMultiButtonTest).toBe('function');
    
    console.log('[TEST-B010] executeMultiButtonTest function validation completed');
  });
  
});