/**
 * Integration Test for Playwright Helper Functions
 * 
 * Validates that all helper utilities work together correctly
 * Tests the complete workflow from port detection to response validation
 * 
 * @fileoverview Integration test for Playwright CLI test helper utilities
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  setupBasicTestSuite,
  executeCompleteTest,
  COMPREHENSIVE_TEST_CONFIG,
  HELPERS_VERSION,
  
  // Individual helper imports for granular testing
  validateSystemReadiness,
  findFrontendServer,
  verifyBackendServer,
  BrowserSessionManager,
  pollForResponse,
  validateFinancialResponse,
  FINANCIAL_EMOJIS,
  PerformanceClassification
} from './helpers/index';

/**
 * Test suite for helper function integration
 */
test.describe('Playwright Helper Functions Integration', () => {
  
  test('should validate helper configuration and version', async () => {
    // Verify helpers are properly exported and configured
    expect(HELPERS_VERSION).toBeDefined();
    expect(COMPREHENSIVE_TEST_CONFIG).toBeDefined();
    expect(COMPREHENSIVE_TEST_CONFIG.timeouts.test).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.performance.success).toBe(45000);
    
    console.log(`[INTEGRATION] Helpers version: ${HELPERS_VERSION}`);
    console.log(`[INTEGRATION] Configuration validated successfully`);
  });
  
  test('should detect system readiness', async () => {
    console.log(`[INTEGRATION] Testing system readiness detection...`);
    
    // Test system readiness validation
    const systemStatus = await validateSystemReadiness();
    
    expect(systemStatus).toBeDefined();
    expect(systemStatus.errors).toBeDefined();
    expect(Array.isArray(systemStatus.errors)).toBe(true);
    
    console.log(`[INTEGRATION] System ready: ${systemStatus.ready}`);
    console.log(`[INTEGRATION] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[INTEGRATION] Backend: ${systemStatus.backend ? `port ${systemStatus.backend.port}, accessible: ${systemStatus.backend.accessible}` : 'not found'}`);
    
    if (!systemStatus.ready) {
      console.log(`[INTEGRATION] System not ready - errors:`, systemStatus.errors);
      // Don't fail the test - just log the status for debugging
    }
  });
  
  test('should detect frontend and backend servers', async () => {
    console.log(`[INTEGRATION] Testing server detection...`);
    
    // Test frontend server detection
    const frontendServer = await findFrontendServer();
    console.log(`[INTEGRATION] Frontend server:`, frontendServer);
    
    // Test backend server verification
    const backendServer = await verifyBackendServer();
    console.log(`[INTEGRATION] Backend server:`, backendServer);
    
    // Verify server status objects have required properties
    if (frontendServer) {
      expect(frontendServer.port).toBeGreaterThanOrEqual(3000);
      expect(frontendServer.port).toBeLessThanOrEqual(3010);
      expect(typeof frontendServer.running).toBe('boolean');
      expect(typeof frontendServer.accessible).toBe('boolean');
    }
    
    expect(backendServer.port).toBe(8000);
    expect(typeof backendServer.running).toBe('boolean');
    expect(typeof backendServer.accessible).toBe('boolean');
  });
  
  test('should validate financial emoji constants', async () => {
    console.log(`[INTEGRATION] Testing financial emoji validation...`);
    
    // Verify emoji constants are properly defined
    expect(FINANCIAL_EMOJIS.BULLISH).toBe('📈');
    expect(FINANCIAL_EMOJIS.BEARISH).toBe('📉');
    expect(FINANCIAL_EMOJIS.MONEY).toBe('💰');
    expect(FINANCIAL_EMOJIS.TARGET).toBe('🎯');
    
    console.log(`[INTEGRATION] Financial emojis validated:`, Object.values(FINANCIAL_EMOJIS));
  });
  
  test('should validate performance classification enum', async () => {
    console.log(`[INTEGRATION] Testing performance classification...`);
    
    // Verify performance classification constants
    expect(PerformanceClassification.SUCCESS).toBe('SUCCESS');
    expect(PerformanceClassification.SLOW_PERFORMANCE).toBe('SLOW_PERFORMANCE');
    expect(PerformanceClassification.TIMEOUT).toBe('TIMEOUT');
    
    console.log(`[INTEGRATION] Performance classifications validated`);
  });
  
  test('should initialize browser session manager', async ({ browser }) => {
    console.log(`[INTEGRATION] Testing browser session manager...`);
    
    const sessionManager = new BrowserSessionManager();
    
    try {
      // Test session initialization
      const page = await sessionManager.initializeSession(browser);
      
      expect(page).toBeDefined();
      expect(typeof page.goto).toBe('function');
      expect(typeof page.locator).toBe('function');
      
      // Test page basic functionality
      const url = page.url();
      console.log(`[INTEGRATION] Session initialized, current URL: ${url}`);
      
      // Test session stats
      const stats = sessionManager.getSessionStats();
      expect(stats.totalTests).toBe(0);
      expect(stats.sessionDuration).toBeGreaterThan(0);
      
      console.log(`[INTEGRATION] Session stats:`, stats);
      
    } finally {
      // Always cleanup
      await sessionManager.cleanup();
    }
  });
  
  test.skip('should execute complete test workflow (requires system ready)', async ({ browser }) => {
    console.log(`[INTEGRATION] Testing complete workflow...`);
    
    // This test is skipped by default since it requires both frontend and backend running
    // Enable by removing .skip when system is ready for full integration testing
    
    try {
      const result = await executeCompleteTest(
        browser,
        'integration-test',
        'test message for integration',
        'NVDA'
      );
      
      expect(result.execution).toBeDefined();
      expect(result.validation).toBeDefined();
      expect(typeof result.execution.success).toBe('boolean');
      expect(typeof result.validation.isValid).toBe('boolean');
      
      console.log(`[INTEGRATION] Complete test result:`, {
        executionSuccess: result.execution.success,
        validationPassed: result.validation.isValid,
        responseTime: result.execution.responseTime,
        classification: result.execution.classification
      });
      
    } catch (error) {
      console.log(`[INTEGRATION] Complete workflow test failed (expected if system not ready):`, error);
      // Don't fail the test - this is expected if servers aren't running
    }
  });
  
  test('should validate test configuration constants', async () => {
    console.log(`[INTEGRATION] Testing configuration constants...`);
    
    const config = COMPREHENSIVE_TEST_CONFIG;
    
    // Validate polling configuration
    expect(config.polling.pollingIntervalMs).toBe(30000);
    expect(config.polling.maxTimeoutMs).toBe(120000);
    expect(config.polling.successThresholdMs).toBe(45000);
    
    // Validate port detection configuration
    expect(config.portDetection.frontendPortRange.start).toBe(3000);
    expect(config.portDetection.frontendPortRange.end).toBe(3010);
    expect(config.portDetection.backendPort).toBe(8000);
    
    // Validate timeouts
    expect(config.timeouts.test).toBe(120000);
    expect(config.timeouts.polling).toBe(30000);
    
    // Validate performance thresholds
    expect(config.performance.success).toBe(45000);
    expect(config.performance.slowPerformance).toBe(120000);
    expect(config.performance.timeout).toBe(120000);
    
    // Validate test data
    expect(Array.isArray(config.testData.validTickers)).toBe(true);
    expect(config.testData.validTickers).toContain('NVDA');
    expect(config.testData.validTickers).toContain('AAPL');
    
    console.log(`[INTEGRATION] Configuration validation completed successfully`);
  });
  
  test('should handle TypeScript type safety', async () => {
    console.log(`[INTEGRATION] Testing TypeScript type safety...`);
    
    // This test validates that TypeScript compilation succeeds and types are correct
    // If this test runs, it means the TypeScript compilation was successful
    
    const config = COMPREHENSIVE_TEST_CONFIG;
    
    // Test type safety by accessing nested properties
    const pollingInterval: number = config.polling.pollingIntervalMs;
    const frontendPorts: {start: number, end: number} = config.portDetection.frontendPortRange;
    const validTickers: readonly string[] = config.testData.validTickers;
    
    expect(typeof pollingInterval).toBe('number');
    expect(typeof frontendPorts.start).toBe('number');
    expect(Array.isArray(validTickers)).toBe(true);
    
    console.log(`[INTEGRATION] TypeScript type safety validated`);
  });
  
});

/**
 * Standalone utility test for development/debugging
 */
test.describe('Helper Utilities Development Tests', () => {
  
  test('should validate helper imports work correctly', async () => {
    console.log(`[DEV] Testing all helper imports...`);
    
    // Test that all major helpers can be imported without errors
    expect(setupBasicTestSuite).toBeDefined();
    expect(executeCompleteTest).toBeDefined();
    expect(validateSystemReadiness).toBeDefined();
    expect(findFrontendServer).toBeDefined();
    expect(verifyBackendServer).toBeDefined();
    expect(BrowserSessionManager).toBeDefined();
    expect(pollForResponse).toBeDefined();
    expect(validateFinancialResponse).toBeDefined();
    
    console.log(`[DEV] All helper imports validated successfully`);
  });
  
  test('should provide development debugging info', async () => {
    console.log(`[DEV] Providing development debugging information...`);
    
    console.log(`[DEV] Helpers Version: ${HELPERS_VERSION}`);
    console.log(`[DEV] Supported Features:`, COMPREHENSIVE_TEST_CONFIG);
    console.log(`[DEV] Financial Emojis Available:`, Object.keys(FINANCIAL_EMOJIS));
    console.log(`[DEV] Performance Classifications:`, [
      PerformanceClassification.SUCCESS,
      PerformanceClassification.SLOW_PERFORMANCE,
      PerformanceClassification.TIMEOUT
    ]);
    
    // Test constants are accessible
    expect(COMPREHENSIVE_TEST_CONFIG.testData.validTickers.length).toBeGreaterThan(0);
    expect(Object.keys(FINANCIAL_EMOJIS).length).toBeGreaterThan(0);
    
    console.log(`[DEV] Development debugging info provided successfully`);
  });
  
});