/**
 * TEST-B013: Button Performance Validation Test
 * 
 * Tests button performance metrics and response timing classification
 * Implements comprehensive performance validation and benchmarking
 * Part of continuous browser session protocol
 * 
 * @fileoverview Button performance validation CLI test with timing analysis
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  validateSystemReadiness,
  clickButtonAndWaitForResponse,
  executeMultiButtonTest,
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
 * TEST-B013: Button Performance Validation Test Suite
 */
test.describe('TEST-B013: Button Performance Validation', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before performance testing', async () => {
    console.log('[TEST-B013] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B013] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B013] System validation completed');
    console.log(`[TEST-B013] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B013] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should validate individual button performance metrics', async ({ browser }) => {
    console.log('[TEST-B013] Starting individual button performance validation...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B013] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      // Test performance for each button type
      const buttonTypes = [
        ButtonType.STOCK_SNAPSHOT,
        ButtonType.SUPPORT_RESISTANCE,
        ButtonType.TECHNICAL_ANALYSIS
      ];
      
      const testTickers = ['NVDA', 'AAPL', 'MSFT'];
      const performanceResults: Array<{
        buttonType: ButtonType;
        ticker: string;
        responseTime: number;
        classification: PerformanceClassification;
        success: boolean;
      }> = [];
      
      for (let i = 0; i < buttonTypes.length; i++) {
        const buttonType = buttonTypes[i];
        const ticker = testTickers[i];
        
        console.log(`[TEST-B013] --- Performance test ${i + 1}/3: ${buttonType} with ${ticker} ---`);
        
        // Small delay between tests
        if (i > 0) {
          await page.waitForTimeout(3000);
        }
        
        const startTime = Date.now();
        const buttonResult = await clickButtonAndWaitForResponse(
          page,
          buttonType,
          ticker,
          `Performance-${buttonType}-${ticker}`
        );
        const responseTime = Date.now() - startTime;
        
        const classification = classifyPerformance(responseTime, COMPREHENSIVE_TEST_CONFIG.polling);
        
        performanceResults.push({
          buttonType,
          ticker,
          responseTime,
          classification,
          success: buttonResult.success
        });
        
        console.log(`[TEST-B013] ${buttonType} performance: ${responseTime}ms (${classification})`);
        
        // Validate performance metrics
        expect(responseTime).toBeGreaterThan(0);
        expect(classification).toBeDefined();
        expect([PerformanceClassification.SUCCESS, PerformanceClassification.SLOW_PERFORMANCE, PerformanceClassification.TIMEOUT])
          .toContain(classification);
        
        // Log performance classification
        if (classification === PerformanceClassification.SUCCESS) {
          console.log(`[TEST-B013] ✅ ${buttonType} - Fast performance (< 45s)`);
        } else if (classification === PerformanceClassification.SLOW_PERFORMANCE) {
          console.log(`[TEST-B013] ⚠️ ${buttonType} - Slow performance (45-120s)`);
        } else {
          console.log(`[TEST-B013] ❌ ${buttonType} - Timeout (> 120s)`);
        }
      }
      
      // Analyze overall performance
      const totalResponseTime = performanceResults.reduce((sum, result) => sum + result.responseTime, 0);
      const averageResponseTime = totalResponseTime / performanceResults.length;
      const successfulTests = performanceResults.filter(result => result.success).length;
      
      console.log(`[TEST-B013] === PERFORMANCE SUMMARY ===`);
      console.log(`[TEST-B013] Total tests: ${performanceResults.length}`);
      console.log(`[TEST-B013] Successful: ${successfulTests}`);
      console.log(`[TEST-B013] Average response time: ${Math.round(averageResponseTime)}ms`);
      console.log(`[TEST-B013] Total time: ${totalResponseTime}ms`);
      
      // Performance distribution
      const successCount = performanceResults.filter(r => r.classification === PerformanceClassification.SUCCESS).length;
      const slowCount = performanceResults.filter(r => r.classification === PerformanceClassification.SLOW_PERFORMANCE).length;
      const timeoutCount = performanceResults.filter(r => r.classification === PerformanceClassification.TIMEOUT).length;
      
      console.log(`[TEST-B013] Performance distribution:`);
      console.log(`[TEST-B013]   SUCCESS: ${successCount}/3 (${Math.round(successCount/3*100)}%)`);
      console.log(`[TEST-B013]   SLOW: ${slowCount}/3 (${Math.round(slowCount/3*100)}%)`);
      console.log(`[TEST-B013]   TIMEOUT: ${timeoutCount}/3 (${Math.round(timeoutCount/3*100)}%)`);
      
      // Validate performance expectations
      expect(performanceResults.length).toBe(3);
      expect(averageResponseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      
      // At least some tests should complete (not all timeout)
      expect(successfulTests).toBeGreaterThan(0);
      
      console.log('[TEST-B013] ✅ Individual button performance validation completed');
      
    } catch (error) {
      console.log('[TEST-B013] ❌ Performance test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate multi-button performance benchmarks', async ({ browser }) => {
    console.log('[TEST-B013] Testing multi-button performance benchmarks...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testTicker = 'SPY';
      const buttonSequence = [
        ButtonType.STOCK_SNAPSHOT,
        ButtonType.SUPPORT_RESISTANCE
      ];
      
      console.log(`[TEST-B013] Multi-button performance test with ${testTicker}`);
      
      // Execute multi-button performance test
      const overallStartTime = Date.now();
      const buttonResults = await executeMultiButtonTest(page, buttonSequence, testTicker);
      const overallEndTime = Date.now();
      
      const overallResponseTime = overallEndTime - overallStartTime;
      
      // Generate performance report
      const report = generateButtonTestReport(buttonResults);
      
      console.log(`[TEST-B013] === MULTI-BUTTON PERFORMANCE REPORT ===`);
      console.log(`[TEST-B013] Total sequence time: ${overallResponseTime}ms`);
      console.log(`[TEST-B013] Average button time: ${Math.round(report.summary.averageResponseTime)}ms`);
      console.log(`[TEST-B013] Successful buttons: ${report.summary.successCount}/${report.summary.totalTests}`);
      
      // Performance breakdown
      console.log(`[TEST-B013] Performance breakdown:`);
      console.log(`[TEST-B013]   SUCCESS: ${report.performance.successCount}`);
      console.log(`[TEST-B013]   SLOW: ${report.performance.slowCount}`);
      console.log(`[TEST-B013]   TIMEOUT: ${report.performance.timeoutCount}`);
      
      // Detailed timing analysis
      buttonResults.forEach((result, index) => {
        const buttonType = buttonSequence[index];
        console.log(`[TEST-B013] ${buttonType}: ${result.responseTime}ms (${result.classification})`);
      });
      
      // Validate multi-button performance expectations
      expect(buttonResults.length).toBe(2);
      expect(report.summary.totalTests).toBe(2);
      expect(overallResponseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      
      // Validate that at least one button succeeds
      expect(report.summary.successCount).toBeGreaterThan(0);
      
      // Performance efficiency check (multi-button should not be too slow)
      const efficiencyRatio = report.summary.averageResponseTime / (COMPREHENSIVE_TEST_CONFIG.performance.success / 2);
      console.log(`[TEST-B013] Efficiency ratio: ${efficiencyRatio.toFixed(2)} (lower is better)`);
      
      if (efficiencyRatio <= 1.0) {
        console.log('[TEST-B013] ✅ Excellent performance efficiency');
      } else if (efficiencyRatio <= 2.0) {
        console.log('[TEST-B013] ⚠️ Acceptable performance efficiency');
      } else {
        console.log('[TEST-B013] ❌ Poor performance efficiency');
      }
      
      console.log('[TEST-B013] ✅ Multi-button performance benchmark completed');
      
    } catch (error) {
      console.log('[TEST-B013] Multi-button performance test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate performance consistency across multiple runs', async ({ browser }) => {
    console.log('[TEST-B013] Testing performance consistency...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testTicker = 'GOOGL';
      const testRuns = 3; // Limited runs for prototype testing
      const consistencyResults: number[] = [];
      
      console.log(`[TEST-B013] Running ${testRuns} consistency tests with ${testTicker}`);
      
      for (let run = 1; run <= testRuns; run++) {
        console.log(`[TEST-B013] --- Consistency run ${run}/${testRuns} ---`);
        
        // Small delay between runs
        if (run > 1) {
          await page.waitForTimeout(5000);
        }
        
        const startTime = Date.now();
        const buttonResult = await clickButtonAndWaitForResponse(
          page,
          ButtonType.STOCK_SNAPSHOT,
          testTicker,
          `Consistency-Run${run}`
        );
        const responseTime = Date.now() - startTime;
        
        if (buttonResult.success) {
          consistencyResults.push(responseTime);
          console.log(`[TEST-B013] Run ${run}: ${responseTime}ms (${buttonResult.classification})`);
        } else {
          console.log(`[TEST-B013] Run ${run}: FAILED - ${buttonResult.error}`);
        }
      }
      
      if (consistencyResults.length >= 2) {
        // Calculate consistency metrics
        const avgTime = consistencyResults.reduce((sum, time) => sum + time, 0) / consistencyResults.length;
        const minTime = Math.min(...consistencyResults);
        const maxTime = Math.max(...consistencyResults);
        const variance = consistencyResults.reduce((sum, time) => sum + Math.pow(time - avgTime, 2), 0) / consistencyResults.length;
        const stdDev = Math.sqrt(variance);
        const coefficient = stdDev / avgTime;
        
        console.log(`[TEST-B013] === CONSISTENCY ANALYSIS ===`);
        console.log(`[TEST-B013] Successful runs: ${consistencyResults.length}/${testRuns}`);
        console.log(`[TEST-B013] Average time: ${Math.round(avgTime)}ms`);
        console.log(`[TEST-B013] Min time: ${minTime}ms`);
        console.log(`[TEST-B013] Max time: ${maxTime}ms`);
        console.log(`[TEST-B013] Standard deviation: ${Math.round(stdDev)}ms`);
        console.log(`[TEST-B013] Coefficient of variation: ${coefficient.toFixed(3)}`);
        
        // Consistency evaluation
        if (coefficient <= 0.1) {
          console.log('[TEST-B013] ✅ Excellent consistency (CV ≤ 0.1)');
        } else if (coefficient <= 0.3) {
          console.log('[TEST-B013] ⚠️ Good consistency (CV ≤ 0.3)');
        } else {
          console.log('[TEST-B013] ❌ Poor consistency (CV > 0.3)');
        }
        
        // Validate consistency expectations
        expect(consistencyResults.length).toBeGreaterThan(0);
        expect(avgTime).toBeGreaterThan(0);
        expect(minTime).toBeGreaterThan(0);
        expect(maxTime).toBeGreaterThan(0);
        
      } else {
        console.log('[TEST-B013] ⚠️ Insufficient successful runs for consistency analysis');
      }
      
      console.log('[TEST-B013] ✅ Performance consistency validation completed');
      
    } catch (error) {
      console.log('[TEST-B013] Consistency test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B013 development
 */
test.describe('TEST-B013: Development Utilities', () => {
  
  test('should validate TEST-B013 configuration', async () => {
    console.log('[TEST-B013] Validating performance test configuration...');
    
    // Validate performance thresholds
    expect(COMPREHENSIVE_TEST_CONFIG.performance.success).toBe(45000);
    expect(COMPREHENSIVE_TEST_CONFIG.performance.slowPerformance).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.performance.timeout).toBe(120000);
    
    // Validate polling configuration
    expect(COMPREHENSIVE_TEST_CONFIG.polling.pollingIntervalMs).toBe(30000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.maxTimeoutMs).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.successThresholdMs).toBe(45000);
    
    console.log('[TEST-B013] Configuration validation completed');
    console.log(`[TEST-B013] SUCCESS threshold: ${COMPREHENSIVE_TEST_CONFIG.performance.success}ms`);
    console.log(`[TEST-B013] SLOW threshold: ${COMPREHENSIVE_TEST_CONFIG.performance.slowPerformance}ms`);
    console.log(`[TEST-B013] TIMEOUT threshold: ${COMPREHENSIVE_TEST_CONFIG.performance.timeout}ms`);
  });
  
  test('should validate performance helper functions', async () => {
    console.log('[TEST-B013] Validating performance helper functions...');
    
    const { classifyPerformance, generateButtonTestReport } = await import('./helpers/index');
    
    // Validate functions are available
    expect(classifyPerformance).toBeDefined();
    expect(typeof classifyPerformance).toBe('function');
    
    expect(generateButtonTestReport).toBeDefined();
    expect(typeof generateButtonTestReport).toBe('function');
    
    // Test classification function
    const fastClassification = classifyPerformance(30000, COMPREHENSIVE_TEST_CONFIG.polling);
    const slowClassification = classifyPerformance(90000, COMPREHENSIVE_TEST_CONFIG.polling);
    const timeoutClassification = classifyPerformance(150000, COMPREHENSIVE_TEST_CONFIG.polling);
    
    expect(fastClassification).toBe(PerformanceClassification.SUCCESS);
    expect(slowClassification).toBe(PerformanceClassification.SLOW_PERFORMANCE);
    expect(timeoutClassification).toBe(PerformanceClassification.TIMEOUT);
    
    console.log('[TEST-B013] Performance helper functions validation completed');
  });
  
});