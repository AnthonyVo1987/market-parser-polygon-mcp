/**
 * TEST-B016: Button Integration Test
 * 
 * Tests complete button integration with backend services and end-to-end workflows
 * Implements comprehensive integration validation and full system testing
 * Part of continuous browser session protocol
 * 
 * @fileoverview Button integration CLI test with full system validation
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  validateSystemReadiness,
  executeCompleteTest,
  clickButtonAndWaitForResponse,
  executeMultiButtonTest,
  generateButtonTestReport,
  generateTestReport,
  validateFinancialResponse,
  
  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  PerformanceClassification,
  ButtonType,
  
  // Browser session management
  BrowserSessionManager
} from './helpers/index';

/**
 * TEST-B016: Button Integration Test Suite
 */
test.describe('TEST-B016: Button Integration', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before integration testing', async () => {
    console.log('[TEST-B016] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B016] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B016] System validation completed');
    console.log(`[TEST-B016] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B016] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should execute complete end-to-end button workflow integration', async ({ browser }) => {
    console.log('[TEST-B016] Starting complete end-to-end button integration test...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B016] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      // Define comprehensive test scenarios
      const integrationScenarios = [
        {
          name: 'Stock Analysis Workflow',
          ticker: 'NVDA',
          buttons: [ButtonType.STOCK_SNAPSHOT, ButtonType.SUPPORT_RESISTANCE, ButtonType.TECHNICAL_ANALYSIS],
          description: 'Complete stock analysis using all three button types'
        },
        {
          name: 'Quick Snapshot Check',
          ticker: 'AAPL', 
          buttons: [ButtonType.STOCK_SNAPSHOT],
          description: 'Single button snapshot for quick analysis'
        },
        {
          name: 'Technical Focus',
          ticker: 'MSFT',
          buttons: [ButtonType.SUPPORT_RESISTANCE, ButtonType.TECHNICAL_ANALYSIS],
          description: 'Technical analysis focused workflow'
        }
      ];
      
      const allResults: any[] = [];
      
      for (let i = 0; i < integrationScenarios.length; i++) {
        const scenario = integrationScenarios[i];
        
        console.log(`[TEST-B016] === SCENARIO ${i + 1}/3: ${scenario.name} ===`);
        console.log(`[TEST-B016] Ticker: ${scenario.ticker}, Buttons: ${scenario.buttons.length}`);
        console.log(`[TEST-B016] Description: ${scenario.description}`);
        
        // Small delay between scenarios
        if (i > 0) {
          await page.waitForTimeout(5000);
        }
        
        // Execute multi-button test for this scenario
        const scenarioStartTime = Date.now();
        const buttonResults = await executeMultiButtonTest(page, scenario.buttons, scenario.ticker);
        const scenarioEndTime = Date.now();
        
        const scenarioTime = scenarioEndTime - scenarioStartTime;
        
        // Validate scenario results
        const successfulButtons = buttonResults.filter(result => result.success);
        const scenarioSuccess = successfulButtons.length === scenario.buttons.length;
        
        console.log(`[TEST-B016] Scenario ${i + 1} completed in ${scenarioTime}ms`);
        console.log(`[TEST-B016] Successful buttons: ${successfulButtons.length}/${scenario.buttons.length}`);
        console.log(`[TEST-B016] Scenario success: ${scenarioSuccess ? 'SUCCESS' : 'PARTIAL/FAILED'}`);
        
        // Detailed validation for successful buttons
        successfulButtons.forEach((result, buttonIndex) => {
          const buttonType = scenario.buttons[buttonIndex];
          console.log(`[TEST-B016]   ${buttonType}: ${result.responseTime}ms (${result.classification})`);
          
          if (result.validationResult) {
            const validation = result.validationResult;
            console.log(`[TEST-B016]     Valid: ${validation.isValid}, Tickers: ${validation.detectedTickers.join(', ')}`);
            console.log(`[TEST-B016]     Emojis: ${validation.detectedEmojis.length}, Content: ${validation.contentLength} chars`);
          }
        });
        
        // Add scenario result to overall results
        allResults.push(...buttonResults.map(result => ({
          ...result,
          scenario: scenario.name,
          ticker: scenario.ticker
        })));
        
        // Validate scenario expectations
        expect(buttonResults.length).toBe(scenario.buttons.length);
        expect(successfulButtons.length).toBeGreaterThan(0); // At least one button should succeed
        expect(scenarioTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      }
      
      // Generate comprehensive integration report
      console.log(`[TEST-B016] === INTEGRATION SUMMARY ===`);
      
      const integrationReport = generateButtonTestReport(allResults);
      
      console.log(`[TEST-B016] Total button interactions: ${integrationReport.summary.totalTests}`);
      console.log(`[TEST-B016] Successful interactions: ${integrationReport.summary.successCount}`);
      console.log(`[TEST-B016] Success rate: ${Math.round(integrationReport.summary.successCount / integrationReport.summary.totalTests * 100)}%`);
      console.log(`[TEST-B016] Average response time: ${Math.round(integrationReport.summary.averageResponseTime)}ms`);
      
      // Performance distribution
      console.log(`[TEST-B016] Performance distribution:`);
      console.log(`[TEST-B016]   SUCCESS: ${integrationReport.performance.successCount}`);
      console.log(`[TEST-B016]   SLOW: ${integrationReport.performance.slowCount}`);
      console.log(`[TEST-B016]   TIMEOUT: ${integrationReport.performance.timeoutCount}`);
      
      // Button type analysis
      console.log(`[TEST-B016] Button type performance:`);
      Object.entries(integrationReport.buttonTypes).forEach(([buttonType, stats]) => {
        const successRate = stats.tested > 0 ? Math.round(stats.successful / stats.tested * 100) : 0;
        console.log(`[TEST-B016]   ${buttonType}: ${stats.successful}/${stats.tested} (${successRate}%), avg: ${Math.round(stats.averageTime)}ms`);
      });
      
      // Validate integration expectations
      expect(integrationReport.summary.totalTests).toBeGreaterThan(0);
      expect(integrationReport.summary.successCount).toBeGreaterThan(0);
      expect(integrationReport.summary.averageResponseTime).toBeGreaterThan(0);
      
      // At least 50% success rate for integration test
      const integrationSuccessRate = integrationReport.summary.successCount / integrationReport.summary.totalTests;
      expect(integrationSuccessRate).toBeGreaterThan(0.5);
      
      if (integrationSuccessRate >= 0.8) {
        console.log('[TEST-B016] ✅ Excellent integration performance (≥80% success)');
      } else if (integrationSuccessRate >= 0.6) {
        console.log('[TEST-B016] ⚠️ Good integration performance (≥60% success)');
      } else {
        console.log('[TEST-B016] ❌ Poor integration performance (<60% success)');
      }
      
      console.log('[TEST-B016] ✅ Complete end-to-end button integration test completed');
      
    } catch (error) {
      console.log('[TEST-B016] ❌ Integration test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate backend integration and data consistency', async ({ browser }) => {
    console.log('[TEST-B016] Testing backend integration and data consistency...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      // Test data consistency across multiple button interactions with same ticker
      const testTicker = 'SPY';
      console.log(`[TEST-B016] Testing data consistency with ${testTicker}`);
      
      const consistencyResults: Array<{
        buttonType: ButtonType;
        detectedTickers: string[];
        contentLength: number;
        hasFinancialContent: boolean;
        responseTime: number;
      }> = [];
      
      // Execute each button type with same ticker
      const buttonTypes = [
        ButtonType.STOCK_SNAPSHOT,
        ButtonType.SUPPORT_RESISTANCE,
        ButtonType.TECHNICAL_ANALYSIS
      ];
      
      for (const buttonType of buttonTypes) {
        console.log(`[TEST-B016] Testing data consistency: ${buttonType} with ${testTicker}`);
        
        const result = await clickButtonAndWaitForResponse(
          page,
          buttonType,
          testTicker,
          `DataConsistency-${buttonType}`
        );
        
        if (result.success && result.validationResult) {
          const validation = result.validationResult;
          
          consistencyResults.push({
            buttonType,
            detectedTickers: validation.detectedTickers,
            contentLength: validation.contentLength,
            hasFinancialContent: validation.hasFinancialContent,
            responseTime: result.responseTime
          });
          
          console.log(`[TEST-B016] ${buttonType} data: ${validation.detectedTickers.length} tickers, ${validation.contentLength} chars`);
          
        } else {
          console.log(`[TEST-B016] ⚠️ ${buttonType} failed - cannot validate data consistency`);
        }
        
        // Delay between tests
        await page.waitForTimeout(3000);
      }
      
      // Analyze data consistency
      if (consistencyResults.length >= 2) {
        console.log(`[TEST-B016] === DATA CONSISTENCY ANALYSIS ===`);
        
        // Check if all responses mention the test ticker
        const allHaveTestTicker = consistencyResults.every(result => 
          result.detectedTickers.includes(testTicker.toUpperCase())
        );
        
        console.log(`[TEST-B016] All responses contain ${testTicker}: ${allHaveTestTicker ? 'YES' : 'NO'}`);
        
        // Check content length consistency (financial responses should have reasonable content)
        const contentLengths = consistencyResults.map(result => result.contentLength);
        const avgContentLength = contentLengths.reduce((sum, len) => sum + len, 0) / contentLengths.length;
        const minContentLength = Math.min(...contentLengths);
        const maxContentLength = Math.max(...contentLengths);
        
        console.log(`[TEST-B016] Content lengths: avg ${Math.round(avgContentLength)}, range ${minContentLength}-${maxContentLength}`);
        
        // All should have financial content
        const allHaveFinancialContent = consistencyResults.every(result => result.hasFinancialContent);
        console.log(`[TEST-B016] All have financial content: ${allHaveFinancialContent ? 'YES' : 'NO'}`);
        
        // Response time consistency
        const responseTimes = consistencyResults.map(result => result.responseTime);
        const avgResponseTime = responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length;
        
        console.log(`[TEST-B016] Average response time: ${Math.round(avgResponseTime)}ms`);
        
        // Validate data consistency expectations
        expect(allHaveTestTicker).toBe(true);
        expect(allHaveFinancialContent).toBe(true);
        expect(minContentLength).toBeGreaterThan(50); // Reasonable minimum content
        expect(avgResponseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
        
        if (allHaveTestTicker && allHaveFinancialContent) {
          console.log('[TEST-B016] ✅ Data consistency validated');
        } else {
          console.log('[TEST-B016] ❌ Data consistency issues detected');
        }
        
      } else {
        console.log('[TEST-B016] ⚠️ Insufficient successful responses for data consistency analysis');
      }
      
      console.log('[TEST-B016] ✅ Backend integration and data consistency testing completed');
      
    } catch (error) {
      console.log('[TEST-B016] Backend integration test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate complete system integration with error recovery', async ({ browser }) => {
    console.log('[TEST-B016] Testing complete system integration with error recovery...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      // Test mixed valid and invalid scenarios for robustness
      const robustnessTests = [
        { ticker: 'NVDA', buttonType: ButtonType.STOCK_SNAPSHOT, expected: 'success' },
        { ticker: 'INVALID123', buttonType: ButtonType.STOCK_SNAPSHOT, expected: 'handled_error' },
        { ticker: 'AAPL', buttonType: ButtonType.SUPPORT_RESISTANCE, expected: 'success' },
        { ticker: '', buttonType: ButtonType.TECHNICAL_ANALYSIS, expected: 'input_validation' },
        { ticker: 'GOOGL', buttonType: ButtonType.TECHNICAL_ANALYSIS, expected: 'success' }
      ];
      
      console.log(`[TEST-B016] Running ${robustnessTests.length} robustness tests...`);
      
      const robustnessResults: Array<{
        test: any;
        actualResult: 'success' | 'error' | 'validation_error';
        responseTime: number;
        matchesExpectation: boolean;
      }> = [];
      
      for (let i = 0; i < robustnessTests.length; i++) {
        const testCase = robustnessTests[i];
        
        console.log(`[TEST-B016] --- Robustness test ${i + 1}: ${testCase.ticker || 'empty'} with ${testCase.buttonType} ---`);
        
        // Small delay between tests
        if (i > 0) {
          await page.waitForTimeout(2000);
        }
        
        const startTime = Date.now();
        const result = await clickButtonAndWaitForResponse(
          page,
          testCase.buttonType,
          testCase.ticker,
          `Robustness-Test${i + 1}`
        );
        const responseTime = Date.now() - startTime;
        
        // Classify actual result
        let actualResult: 'success' | 'error' | 'validation_error';
        
        if (result.success) {
          actualResult = 'success';
        } else if (result.error?.toLowerCase().includes('input') || result.error?.toLowerCase().includes('validation')) {
          actualResult = 'validation_error';
        } else {
          actualResult = 'error';
        }
        
        // Check if result matches expectation
        const matchesExpectation = 
          (testCase.expected === 'success' && actualResult === 'success') ||
          (testCase.expected === 'handled_error' && (actualResult === 'error' || actualResult === 'success')) ||
          (testCase.expected === 'input_validation' && (actualResult === 'validation_error' || actualResult === 'error'));
        
        robustnessResults.push({
          test: testCase,
          actualResult,
          responseTime,
          matchesExpectation
        });
        
        console.log(`[TEST-B016] Test ${i + 1} result: ${actualResult} (expected: ${testCase.expected}) - ${matchesExpectation ? 'MATCH' : 'MISMATCH'}`);
        console.log(`[TEST-B016] Response time: ${responseTime}ms`);
        
        if (result.error) {
          console.log(`[TEST-B016] Error details: ${result.error}`);
        }
      }
      
      // Analyze robustness results
      console.log(`[TEST-B016] === ROBUSTNESS ANALYSIS ===`);
      
      const totalTests = robustnessResults.length;
      const matchingTests = robustnessResults.filter(result => result.matchesExpectation).length;
      const robustnessScore = (matchingTests / totalTests) * 100;
      
      console.log(`[TEST-B016] Robustness score: ${robustnessScore.toFixed(1)}% (${matchingTests}/${totalTests})`);
      
      // Response time analysis
      const avgResponseTime = robustnessResults.reduce((sum, result) => sum + result.responseTime, 0) / totalTests;
      console.log(`[TEST-B016] Average response time: ${Math.round(avgResponseTime)}ms`);
      
      // Error handling analysis
      const errorTests = robustnessResults.filter(result => result.test.expected !== 'success');
      const errorHandlingSuccess = errorTests.filter(result => result.matchesExpectation).length;
      const errorHandlingRate = errorTests.length > 0 ? (errorHandlingSuccess / errorTests.length) * 100 : 100;
      
      console.log(`[TEST-B016] Error handling success rate: ${errorHandlingRate.toFixed(1)}% (${errorHandlingSuccess}/${errorTests.length})`);
      
      // Validate robustness expectations
      expect(totalTests).toBe(5);
      expect(robustnessScore).toBeGreaterThan(60); // At least 60% should match expectations
      expect(avgResponseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      
      if (robustnessScore >= 80) {
        console.log('[TEST-B016] ✅ Excellent system robustness');
      } else if (robustnessScore >= 60) {
        console.log('[TEST-B016] ⚠️ Good system robustness');
      } else {
        console.log('[TEST-B016] ❌ Poor system robustness');
      }
      
      console.log('[TEST-B016] ✅ Complete system integration with error recovery testing completed');
      
    } catch (error) {
      console.log('[TEST-B016] System integration test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B016 development
 */
test.describe('TEST-B016: Development Utilities', () => {
  
  test('should validate TEST-B016 configuration', async () => {
    console.log('[TEST-B016] Validating integration test configuration...');
    
    // Validate integration test expectations
    expect(COMPREHENSIVE_TEST_CONFIG.timeouts.test).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.buttonInteraction.multiButtonDelay).toBe(3000);
    
    // Validate test data for integration scenarios
    const buttonTestTickers = COMPREHENSIVE_TEST_CONFIG.testData.buttonTestTickers;
    expect(buttonTestTickers).toContain('NVDA');
    expect(buttonTestTickers).toContain('AAPL');
    expect(buttonTestTickers).toContain('GME');
    
    console.log('[TEST-B016] Configuration validation completed');
    console.log(`[TEST-B016] Test timeout: ${COMPREHENSIVE_TEST_CONFIG.timeouts.test}ms`);
    console.log(`[TEST-B016] Multi-button delay: ${COMPREHENSIVE_TEST_CONFIG.buttonInteraction.multiButtonDelay}ms`);
  });
  
  test('should validate integration helper functions', async () => {
    console.log('[TEST-B016] Validating integration helper functions...');
    
    const { 
      executeCompleteTest, 
      generateButtonTestReport, 
      generateTestReport 
    } = await import('./helpers/index');
    
    // Validate functions are available
    expect(executeCompleteTest).toBeDefined();
    expect(typeof executeCompleteTest).toBe('function');
    
    expect(generateButtonTestReport).toBeDefined();
    expect(typeof generateButtonTestReport).toBe('function');
    
    expect(generateTestReport).toBeDefined();
    expect(typeof generateTestReport).toBe('function');
    
    console.log('[TEST-B016] Integration helper functions validation completed');
  });
  
});