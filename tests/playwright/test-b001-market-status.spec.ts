/**
 * TEST-B001: Market Status Test
 *
 * Tests market status query with priority fast request and low verbosity
 * Implements dynamic port detection and two-phase auto-retry detection
 * Part of continuous browser session protocol
 *
 * @fileoverview Market Status CLI test with auto-retry detection and validation
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  sendMessageAndWaitForResponse,
  validateSystemReadiness,
  classifyPerformance,

  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  PerformanceClassification,
  FINANCIAL_EMOJIS,

  // Browser session management
  BrowserSessionManager
} from './helpers/index';

// Import new auto-retry validation
import { validateMarketStatusResponse } from './helpers/response-validators';

/**
 * TEST-B001: Market Status Test Suite
 */
test.describe('TEST-B001: Market Status', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before testing', async () => {
    console.log('[TEST-B001] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B001] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B001] System validation completed');
    console.log(`[TEST-B001] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B001] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should execute market status query with performance tracking', async ({ browser }) => {
    console.log('[TEST-B001] Starting market status test execution...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session (part of continuous session)
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend with dynamic port detection
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B001] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000); // Allow interface to stabilize
      
      // Define test query with priority fast request and low verbosity
      const testQuery = "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
      
      console.log(`[TEST-B001] Sending query: ${testQuery}`);
      
      // Execute test with auto-retry detection and 120-second timeout
      const startTime = Date.now();
      const executionResult = await sendMessageAndWaitForResponse(
        page,
        testQuery,
        'TEST-B001-MarketStatus'
      );
      
      const responseTime = Date.now() - startTime;
      const performanceClass = classifyPerformance(responseTime, COMPREHENSIVE_TEST_CONFIG.polling);
      
      console.log(`[TEST-B001] Execution completed in ${responseTime}ms (${performanceClass})`);
      
      // Validate execution success
      expect(executionResult.success).toBe(true);
      expect(executionResult.responseTime).toBeGreaterThan(0);
      expect(executionResult.classification).toBeDefined();
      
      if (!executionResult.success) {
        console.log('[TEST-B001] Execution failed:', executionResult.error);
        throw new Error(`Test execution failed: ${executionResult.error}`);
      }
      
      // Validate response content using new auto-retry validation
      console.log('[TEST-B001] Validating market status response with auto-retry...');

      // Get response content from execution result
      const responseContent = executionResult.responseContent || '';

      // Use specific market status validation
      const validationResult = validateMarketStatusResponse(responseContent, 'TEST-B001-MarketStatus');

      // Log auto-retry phase timings if available
      if (executionResult.phase1Time && executionResult.phase2Time) {
        console.log(`[TEST-B001] Auto-retry phases: Phase1=${executionResult.phase1Time}ms, Phase2=${executionResult.phase2Time}ms`);
      }

      // Log detailed validation results
      console.log(`[TEST-B001] Response validation status: ${validationResult.status}`);
      console.log(`[TEST-B001] Market status content: ${validationResult.hasMarketStatusContent}`);
      console.log(`[TEST-B001] Emoji indicators: ${validationResult.hasEmojiIndicators}`);
      console.log(`[TEST-B001] Content length: ${validationResult.contentLength} characters`);

      if (validationResult.detectedEmojis.length > 0) {
        console.log(`[TEST-B001] Detected emojis: ${validationResult.detectedEmojis.join(', ')}`);
      }

      if (validationResult.detectedTickers.length > 0) {
        console.log(`[TEST-B001] Detected tickers: ${validationResult.detectedTickers.join(', ')}`);
      }

      if (validationResult.status === 'FAIL') {
        console.log(`[TEST-B001] Validation failures: ${validationResult.failureReasons.join(', ')}`);
      }

      // Market status should contain financial indicators and pass validation
      expect(validationResult.status).toBe('PASS');
      expect(validationResult.hasMarketStatusContent).toBe(true);
      expect(validationResult.hasEmojiIndicators).toBe(true);
      expect(validationResult.contentLength).toBeGreaterThan(50);
      
      // Performance classification validation
      console.log(`[TEST-B001] Performance classification: ${performanceClass}`);
      
      if (performanceClass === PerformanceClassification.SUCCESS) {
        console.log(`[TEST-B001] ✅ SUCCESS: Fast response (< 45 seconds)`);
      } else if (performanceClass === PerformanceClassification.SLOW_PERFORMANCE) {
        console.log(`[TEST-B001] ⚠️ SLOW_PERFORMANCE: Response took 45-120 seconds`);
      } else {
        console.log(`[TEST-B001] ❌ TIMEOUT: Response exceeded 120 seconds`);
      }
      
      // Log specific market status detection result
      if (validationResult.hasMarketStatusContent) {
        console.log('[TEST-B001] ✅ Market status content detected');
      } else {
        console.log('[TEST-B001] ⚠️ Market status content not detected');
      }

      // Final test assertions with auto-retry validation
      expect(executionResult.success).toBe(true);
      expect(validationResult.status).toBe('PASS');
      expect(validationResult.hasMarketStatusContent).toBe(true);
      expect(responseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      
      console.log('[TEST-B001] ✅ Market status test completed successfully');
      
    } catch (error) {
      console.log('[TEST-B001] ❌ Test execution failed:', error);
      throw error;
      
    } finally {
      // Session cleanup (will be part of continuous session in actual test runs)
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate market status response format', async ({ browser }) => {
    console.log('[TEST-B001] Validating market status response format requirements...');
    
    // This test validates the specific format requirements for market status responses
    // It can be run independently or as part of the main test
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      // Navigate and send query
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testQuery = "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
      
      const executionResult = await sendMessageAndWaitForResponse(
        page,
        testQuery,
        'TEST-B001-Format-Validation'
      );

      if (executionResult.success) {
        // Use auto-retry validation for format checking
        const responseContent = executionResult.responseContent || '';
        const validationResult = validateMarketStatusResponse(responseContent, 'TEST-B001-Format-Validation');

        console.log(`[TEST-B001] Format validation status: ${validationResult.status}`);
        console.log(`[TEST-B001] Format validation - KEY TAKEAWAYS: ${validationResult.hasKeyTakeaways}`);
        console.log(`[TEST-B001] Format validation - Financial emojis: ${validationResult.hasEmojiIndicators}`);

        // Log response structure for analysis
        if (responseContent.length > 0) {
          const lines = responseContent.split('\n').filter(line => line.trim().length > 0);
          console.log(`[TEST-B001] Response structure: ${lines.length} lines`);

          if (validationResult.detectedEmojis.length > 0) {
            console.log(`[TEST-B001] Structured sections with emojis: ${validationResult.detectedEmojis.join(', ')}`);
          }
        }

        expect(validationResult.hasEmojiIndicators).toBe(true);
        expect(validationResult.status).toBe('PASS');
        console.log('[TEST-B001] ✅ Format validation completed');
        
      } else {
        console.log('[TEST-B001] ⚠️ Skipping format validation due to execution failure');
        test.skip(true, 'Format validation skipped due to execution failure');
      }
      
    } catch (error) {
      console.log('[TEST-B001] Format validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B001 development
 */
test.describe('TEST-B001: Development Utilities', () => {
  
  test('should validate TEST-B001 configuration', async () => {
    console.log('[TEST-B001] Validating test configuration...');
    
    // Validate auto-retry configuration for market status test
    expect(COMPREHENSIVE_TEST_CONFIG.polling.maxTimeoutMs).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.successThresholdMs).toBe(45000);

    // Auto-retry uses dynamic detection instead of fixed polling intervals
    console.log('[TEST-B001] Auto-retry detection enabled (no fixed polling intervals)');
    
    // Validate performance thresholds
    expect(COMPREHENSIVE_TEST_CONFIG.performance.success).toBe(45000);
    expect(COMPREHENSIVE_TEST_CONFIG.performance.slowPerformance).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.performance.timeout).toBe(120000);
    
    // Validate financial emojis are available
    const emojiValues = Object.values(FINANCIAL_EMOJIS);
    expect(emojiValues.length).toBeGreaterThan(0);
    expect(emojiValues).toContain('📈');
    expect(emojiValues).toContain('📉');
    expect(emojiValues).toContain('💰');
    
    console.log('[TEST-B001] Configuration validation completed');
    console.log(`[TEST-B001] Auto-retry detection: enabled`);
    console.log(`[TEST-B001] Max timeout: ${COMPREHENSIVE_TEST_CONFIG.polling.maxTimeoutMs}ms`);
    console.log(`[TEST-B001] Success threshold: ${COMPREHENSIVE_TEST_CONFIG.performance.success}ms`);
  });
  
  test('should validate market status query format', async () => {
    console.log('[TEST-B001] Validating query format...');
    
    const testQuery = "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
    
    // Validate query contains required elements
    expect(testQuery).toContain('Market Status');
    expect(testQuery).toContain('PRIORITY FAST REQUEST');
    expect(testQuery).toContain('MINIMAL TOOL CALLS ONLY');
    expect(testQuery).toContain('LOW Verbosity');
    
    // Validate query length is reasonable
    expect(testQuery.length).toBeGreaterThan(50);
    expect(testQuery.length).toBeLessThan(200);
    
    console.log('[TEST-B001] Query format validation completed');
    console.log(`[TEST-B001] Query: ${testQuery}`);
    console.log(`[TEST-B001] Query length: ${testQuery.length} characters`);
  });
  
});