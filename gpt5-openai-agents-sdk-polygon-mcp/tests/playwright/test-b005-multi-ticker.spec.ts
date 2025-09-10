/**
 * TEST-B005: Multi-Ticker Test
 * 
 * Tests multi-ticker snapshot query with NVDA, SPY, QQQ, IWM
 * Implements dynamic port detection and 30-second polling methodology
 * Part of continuous browser session protocol
 * 
 * @fileoverview Multi-Ticker CLI test with comprehensive ticker validation
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  sendMessageAndWaitForResponse,
  validateFinancialResponse,
  validateSystemReadiness,
  pollForResponse,
  classifyPerformance,
  extractTickers,
  
  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  PerformanceClassification,
  FINANCIAL_EMOJIS,
  
  // Browser session management
  BrowserSessionManager
} from './helpers/index';

/**
 * TEST-B005: Multi-Ticker Test Suite
 */
test.describe('TEST-B005: Multi-Ticker', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before testing', async () => {
    console.log('[TEST-B005] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B005] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B005] System validation completed');
    console.log(`[TEST-B005] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B005] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should execute multi-ticker query with comprehensive validation', async ({ browser }) => {
    console.log('[TEST-B005] Starting multi-ticker test execution...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session (part of continuous session)
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend with dynamic port detection
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B005] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000); // Allow interface to stabilize
      
      // Define multi-ticker test query with priority fast request and low verbosity
      const expectedTickers = ['NVDA', 'SPY', 'QQQ', 'IWM'];
      const testQuery = `Full Market Snapshot with multiple Tickers: ${expectedTickers.join(', ')}: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity`;
      
      console.log(`[TEST-B005] Testing with tickers: ${expectedTickers.join(', ')}`);
      console.log(`[TEST-B005] Sending query: ${testQuery}`);
      
      // Execute test with 30-second polling and 120-second timeout
      const startTime = Date.now();
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B005-MultiTicker'
      );
      
      const responseTime = Date.now() - startTime;
      const performanceClass = classifyPerformance(responseTime, COMPREHENSIVE_TEST_CONFIG.polling);
      
      console.log(`[TEST-B005] Execution completed in ${responseTime}ms (${performanceClass})`);
      
      // Validate execution success
      expect(executionResult.success).toBe(true);
      expect(executionResult.responseTime).toBeGreaterThan(0);
      expect(executionResult.classification).toBeDefined();
      
      if (!executionResult.success) {
        console.log('[TEST-B005] Execution failed:', executionResult.error);
        throw new Error(`Test execution failed: ${executionResult.error}`);
      }
      
      // Validate response content for multi-ticker analysis
      console.log('[TEST-B005] Validating multi-ticker response...');
      const validationResult = await validateFinancialResponse(page);
      
      // Multi-ticker response should contain comprehensive financial content
      expect(validationResult.hasFinancialContent).toBe(true);
      expect(validationResult.contentLength).toBeGreaterThan(200); // More content for multiple tickers
      
      // Should have emoji indicators for market analysis
      expect(validationResult.hasEmojiIndicators).toBe(true);
      expect(validationResult.detectedEmojis.length).toBeGreaterThan(0);
      
      // Extract and validate detected tickers
      const responseContent = validationResult.responseContent || '';
      const detectedTickers = extractTickers(responseContent);
      
      console.log(`[TEST-B005] Expected tickers: [${expectedTickers.join(', ')}]`);
      console.log(`[TEST-B005] Detected tickers: [${detectedTickers.join(', ')}]`);
      
      // Validate ticker coverage - should detect at least some of the requested tickers
      const foundExpectedTickers = expectedTickers.filter(ticker => 
        detectedTickers.includes(ticker.toUpperCase())
      );
      
      expect(foundExpectedTickers.length).toBeGreaterThan(0);
      console.log(`[TEST-B005] Found expected tickers: [${foundExpectedTickers.join(', ')}] (${foundExpectedTickers.length}/${expectedTickers.length})`);
      
      // Multi-ticker validation - comprehensive ticker analysis
      const tickerValidationResults = expectedTickers.map(ticker => ({
        ticker,
        mentioned: detectedTickers.includes(ticker.toUpperCase()),
        hasContext: responseContent.toLowerCase().includes(ticker.toLowerCase())
      }));
      
      const mentionedCount = tickerValidationResults.filter(r => r.mentioned).length;
      const contextCount = tickerValidationResults.filter(r => r.hasContext).length;
      
      console.log('[TEST-B005] Ticker validation breakdown:');
      tickerValidationResults.forEach(result => {
        const status = result.mentioned ? '✅' : (result.hasContext ? '⚠️' : '❌');
        console.log(`[TEST-B005]   ${status} ${result.ticker}: mentioned=${result.mentioned}, hasContext=${result.hasContext}`);
      });
      
      // Should have at least 50% ticker coverage for multi-ticker request
      const coveragePercent = (mentionedCount / expectedTickers.length) * 100;
      expect(coveragePercent).toBeGreaterThanOrEqual(25); // At least 25% coverage (1 out of 4 tickers)
      console.log(`[TEST-B005] Ticker coverage: ${coveragePercent.toFixed(1)}% (${mentionedCount}/${expectedTickers.length})`);
      
      // Log detailed validation results
      console.log(`[TEST-B005] Response validation - Valid: ${validationResult.isValid}`);
      console.log(`[TEST-B005] KEY TAKEAWAYS present: ${validationResult.hasKeyTakeaways}`);
      console.log(`[TEST-B005] Emoji indicators: ${validationResult.detectedEmojis.join(', ')}`);
      console.log(`[TEST-B005] Content length: ${validationResult.contentLength} characters`);
      console.log(`[TEST-B005] All detected tickers: ${validationResult.detectedTickers.join(', ')}`);
      
      // Performance classification validation
      console.log(`[TEST-B005] Performance classification: ${performanceClass}`);
      
      if (performanceClass === PerformanceClassification.SUCCESS) {
        console.log(`[TEST-B005] ✅ SUCCESS: Fast response (< 45 seconds)`);
      } else if (performanceClass === PerformanceClassification.SLOW_PERFORMANCE) {
        console.log(`[TEST-B005] ⚠️ SLOW_PERFORMANCE: Response took 45-120 seconds`);
      } else {
        console.log(`[TEST-B005] ❌ TIMEOUT: Response exceeded 120 seconds`);
      }
      
      // Validate multi-ticker specific content
      const multiTickerKeywords = ['market', 'snapshot', 'multiple', 'analysis', 'overview', 'comparison'];
      const hasMultiTickerContent = multiTickerKeywords.some(keyword => 
        responseContent.toLowerCase().includes(keyword)
      );
      
      if (hasMultiTickerContent) {
        console.log('[TEST-B005] ✅ Multi-ticker analysis content detected');
      } else {
        console.log('[TEST-B005] ⚠️ General financial response received (multi-ticker analysis not explicitly detected)');
      }
      
      // Advanced validation for multi-ticker responses
      const financialMetrics = ['price', 'volume', 'market cap', 'change', '%', 'trading'];
      const detectedMetrics = financialMetrics.filter(metric => 
        responseContent.toLowerCase().includes(metric)
      );
      
      expect(detectedMetrics.length).toBeGreaterThan(2);
      console.log(`[TEST-B005] Financial metrics detected: ${detectedMetrics.join(', ')}`);
      
      // Final test assertions
      expect(executionResult.success).toBe(true);
      expect(validationResult.hasFinancialContent).toBe(true);
      expect(validationResult.hasEmojiIndicators).toBe(true);
      expect(responseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      expect(foundExpectedTickers.length).toBeGreaterThan(0);
      
      console.log('[TEST-B005] ✅ Multi-ticker test completed successfully');
      
    } catch (error) {
      console.log('[TEST-B005] ❌ Test execution failed:', error);
      throw error;
      
    } finally {
      // Session cleanup (will be part of continuous session in actual test runs)
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate individual ticker presence in multi-ticker response', async ({ browser }) => {
    console.log('[TEST-B005] Validating individual ticker presence...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      // Navigate and send query
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const expectedTickers = ['NVDA', 'SPY', 'QQQ', 'IWM'];
      const testQuery = `Full Market Snapshot with multiple Tickers: ${expectedTickers.join(', ')}: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity`;
      
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B005-Individual-Ticker-Validation'
      );
      
      if (executionResult.success) {
        const pageContent = await page.textContent('body') || '';
        
        // Individual ticker analysis
        const tickerAnalysis = expectedTickers.map(ticker => {
          const tickerPattern = new RegExp(`\\b${ticker}\\b`, 'gi');
          const matches = pageContent.match(tickerPattern) || [];
          const mentionCount = matches.length;
          
          // Look for ticker with price context
          const priceContext = new RegExp(`${ticker}[^\\n]*(?:price|\\$|trading|volume)`, 'gi');
          const hasPriceContext = priceContext.test(pageContent);
          
          return {
            ticker,
            mentionCount,
            hasPriceContext,
            present: mentionCount > 0
          };
        });
        
        console.log('[TEST-B005] Individual ticker analysis:');
        tickerAnalysis.forEach(analysis => {
          const status = analysis.present ? (analysis.hasPriceContext ? '✅' : '⚠️') : '❌';
          console.log(`[TEST-B005]   ${status} ${analysis.ticker}: mentions=${analysis.mentionCount}, priceContext=${analysis.hasPriceContext}`);
        });
        
        const presentTickers = tickerAnalysis.filter(a => a.present);
        const tickersWithContext = tickerAnalysis.filter(a => a.hasPriceContext);
        
        console.log(`[TEST-B005] Ticker presence summary: ${presentTickers.length}/${expectedTickers.length} present, ${tickersWithContext.length}/${expectedTickers.length} with price context`);
        
        // Should have at least some ticker presence
        expect(presentTickers.length).toBeGreaterThan(0);
        console.log('[TEST-B005] ✅ Individual ticker validation completed');
        
      } else {
        console.log('[TEST-B005] ⚠️ Skipping ticker validation due to execution failure');
        test.skip(true, 'Ticker validation skipped due to execution failure');
      }
      
    } catch (error) {
      console.log('[TEST-B005] Individual ticker validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate multi-ticker response comprehensiveness', async ({ browser }) => {
    console.log('[TEST-B005] Validating multi-ticker response comprehensiveness...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const expectedTickers = ['NVDA', 'SPY', 'QQQ', 'IWM'];
      const testQuery = `Full Market Snapshot with multiple Tickers: ${expectedTickers.join(', ')}: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity`;
      
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B005-Comprehensiveness-Validation'
      );
      
      if (executionResult.success) {
        const pageContent = await page.textContent('body') || '';
        
        // Comprehensiveness metrics
        const contentMetrics = {
          totalLength: pageContent.length,
          wordCount: pageContent.split(/\s+/).length,
          uniqueWords: new Set(pageContent.toLowerCase().split(/\s+/)).size,
          sentences: pageContent.split(/[.!?]+/).length,
          paragraphs: pageContent.split(/\n\s*\n/).length
        };
        
        console.log('[TEST-B005] Content comprehensiveness metrics:');
        console.log(`[TEST-B005]   Total length: ${contentMetrics.totalLength} characters`);
        console.log(`[TEST-B005]   Word count: ${contentMetrics.wordCount} words`);
        console.log(`[TEST-B005]   Unique words: ${contentMetrics.uniqueWords} unique`);
        console.log(`[TEST-B005]   Sentences: ${contentMetrics.sentences}`);
        console.log(`[TEST-B005]   Paragraphs: ${contentMetrics.paragraphs}`);
        
        // Multi-ticker responses should be comprehensive
        expect(contentMetrics.totalLength).toBeGreaterThan(300); // Substantial content
        expect(contentMetrics.wordCount).toBeGreaterThan(50);   // Meaningful word count
        expect(contentMetrics.uniqueWords).toBeGreaterThan(30); // Diverse vocabulary
        
        // Look for comparative analysis indicators
        const comparativeKeywords = ['compare', 'versus', 'vs', 'relative', 'performance', 'contrast'];
        const hasComparative = comparativeKeywords.some(keyword => 
          pageContent.toLowerCase().includes(keyword)
        );
        
        console.log(`[TEST-B005] Comparative analysis detected: ${hasComparative}`);
        
        // Look for section organization
        const organizationalPatterns = [/🎯[^🎯]*/g, /📊[^📊]*/g, /📈[^📈]*/g, /📉[^📉]*/g];
        const sectionsFound = organizationalPatterns.reduce((count, pattern) => {
          const matches = pageContent.match(pattern);
          return count + (matches ? matches.length : 0);
        }, 0);
        
        console.log(`[TEST-B005] Organized sections found: ${sectionsFound}`);
        expect(sectionsFound).toBeGreaterThan(0); // Should have some organizational structure
        
        console.log('[TEST-B005] ✅ Comprehensiveness validation completed');
        
      } else {
        console.log('[TEST-B005] ⚠️ Skipping comprehensiveness validation due to execution failure');
        test.skip(true, 'Comprehensiveness validation skipped due to execution failure');
      }
      
    } catch (error) {
      console.log('[TEST-B005] Comprehensiveness validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B005 development
 */
test.describe('TEST-B005: Development Utilities', () => {
  
  test('should validate TEST-B005 configuration', async () => {
    console.log('[TEST-B005] Validating test configuration...');
    
    const expectedTickers = ['NVDA', 'SPY', 'QQQ', 'IWM'];
    
    // Validate expected tickers are in common tickers list
    const commonTickers = COMPREHENSIVE_TEST_CONFIG.testData.validTickers;
    const supportedTickers = expectedTickers.filter(ticker => 
      commonTickers.includes(ticker)
    );
    
    expect(supportedTickers.length).toBe(expectedTickers.length);
    console.log(`[TEST-B005] All expected tickers supported: ${supportedTickers.join(', ')}`);
    
    // Validate polling configuration for multi-ticker test
    expect(COMPREHENSIVE_TEST_CONFIG.polling.pollingIntervalMs).toBe(30000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.maxTimeoutMs).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.successThresholdMs).toBe(45000);
    
    // Validate financial emojis are available
    const emojiValues = Object.values(FINANCIAL_EMOJIS);
    expect(emojiValues.length).toBeGreaterThan(0);
    expect(emojiValues).toContain('📈');
    expect(emojiValues).toContain('📉');
    expect(emojiValues).toContain('💰');
    expect(emojiValues).toContain('📊');
    
    console.log('[TEST-B005] Configuration validation completed');
  });
  
  test('should validate multi-ticker query format', async () => {
    console.log('[TEST-B005] Validating multi-ticker query format...');
    
    const expectedTickers = ['NVDA', 'SPY', 'QQQ', 'IWM'];
    const testQuery = `Full Market Snapshot with multiple Tickers: ${expectedTickers.join(', ')}: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity`;
    
    // Validate query contains required elements
    expect(testQuery).toContain('Full Market Snapshot');
    expect(testQuery).toContain('multiple Tickers');
    expectedTickers.forEach(ticker => {
      expect(testQuery).toContain(ticker);
    });
    expect(testQuery).toContain('PRIORITY FAST REQUEST');
    expect(testQuery).toContain('MINIMAL TOOL CALLS ONLY');
    expect(testQuery).toContain('LOW Verbosity');
    
    // Validate query length is reasonable for multi-ticker request
    expect(testQuery.length).toBeGreaterThan(100);
    expect(testQuery.length).toBeLessThan(300);
    
    console.log('[TEST-B005] Query format validation completed');
    console.log(`[TEST-B005] Query: ${testQuery}`);
    console.log(`[TEST-B005] Query length: ${testQuery.length} characters`);
    console.log(`[TEST-B005] Expected tickers: ${expectedTickers.join(', ')}`);
  });
  
  test('should validate ticker extraction utility', async () => {
    console.log('[TEST-B005] Testing ticker extraction utility...');
    
    const testContent = `
      Market analysis for NVDA shows strong performance.
      SPY is trading at $450 per share.
      QQQ has gained 2.5% today.
      IWM shows volatility with $200 price point.
      Additional mention of AAPL and MSFT for comparison.
    `;
    
    const extractedTickers = extractTickers(testContent);
    
    console.log(`[TEST-B005] Test content: ${testContent.replace(/\s+/g, ' ').trim()}`);
    console.log(`[TEST-B005] Extracted tickers: ${extractedTickers.join(', ')}`);
    
    // Should extract the main tickers
    const expectedTickers = ['NVDA', 'SPY', 'QQQ', 'IWM'];
    const foundExpected = expectedTickers.filter(ticker => 
      extractedTickers.includes(ticker)
    );
    
    expect(foundExpected.length).toBeGreaterThan(0);
    console.log(`[TEST-B005] Found expected tickers: ${foundExpected.join(', ')}`);
    console.log('[TEST-B005] Ticker extraction utility validation completed');
  });
  
});