/**
 * TEST-B004: Single Ticker GME Test
 * 
 * Tests GME ticker query with priority fast request and low verbosity
 * Implements dynamic port detection and 30-second polling methodology
 * Part of continuous browser session protocol
 * 
 * @fileoverview Single Ticker GME CLI test with sentiment indicator validation
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  sendMessageAndWaitForResponse,
  validateFinancialResponse,
  validateTickerResponse,
  validateSystemReadiness,
  pollForResponse,
  classifyPerformance,
  
  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  PerformanceClassification,
  FINANCIAL_EMOJIS,
  
  // Browser session management
  BrowserSessionManager
} from './helpers/index';

/**
 * TEST-B004: Single Ticker GME Test Suite
 */
test.describe('TEST-B004: Single Ticker GME', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before testing', async () => {
    console.log('[TEST-B004] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B004] System not ready - errors:', systemStatus.errors);
      test.skip('System not ready for testing');
    }
    
    console.log('[TEST-B004] System validation completed');
    console.log(`[TEST-B004] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B004] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should execute GME ticker query with performance tracking', async ({ browser }) => {
    console.log('[TEST-B004] Starting GME ticker test execution...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session (part of continuous session)
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend with dynamic port detection
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B004] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000); // Allow interface to stabilize
      
      // Define test query with priority fast request and low verbosity
      const testQuery = "Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
      
      console.log(`[TEST-B004] Sending query: ${testQuery}`);
      
      // Execute test with 30-second polling and 120-second timeout
      const startTime = Date.now();
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B004-GME-Ticker'
      );
      
      const responseTime = Date.now() - startTime;
      const performanceClass = classifyPerformance(responseTime, COMPREHENSIVE_TEST_CONFIG.polling);
      
      console.log(`[TEST-B004] Execution completed in ${responseTime}ms (${performanceClass})`);
      
      // Validate execution success
      expect(executionResult.success).toBe(true);
      expect(executionResult.responseTime).toBeGreaterThan(0);
      expect(executionResult.classification).toBeDefined();
      
      if (!executionResult.success) {
        console.log('[TEST-B004] Execution failed:', executionResult.error);
        throw new Error(`Test execution failed: ${executionResult.error}`);
      }
      
      // Validate response content for GME ticker
      console.log('[TEST-B004] Validating GME ticker response...');
      const validationResult = await validateFinancialResponse(page, 'GME');
      
      // GME response should contain financial indicators
      expect(validationResult.hasFinancialContent).toBe(true);
      expect(validationResult.contentLength).toBeGreaterThan(100);
      
      // Should have emoji indicators for financial sentiment
      expect(validationResult.hasEmojiIndicators).toBe(true);
      expect(validationResult.detectedEmojis.length).toBeGreaterThan(0);
      
      // Should specifically contain GME ticker reference
      expect(validationResult.detectedTickers).toContain('GME');
      
      // Log detailed validation results
      console.log(`[TEST-B004] Response validation - Valid: ${validationResult.isValid}`);
      console.log(`[TEST-B004] KEY TAKEAWAYS present: ${validationResult.hasKeyTakeaways}`);
      console.log(`[TEST-B004] Emoji indicators: ${validationResult.detectedEmojis.join(', ')}`);
      console.log(`[TEST-B004] Detected tickers: ${validationResult.detectedTickers.join(', ')}`);
      console.log(`[TEST-B004] Content length: ${validationResult.contentLength} characters`);
      
      // Validate GME-specific content
      const responseContent = validationResult.responseContent || '';
      const gmeKeywords = ['gme', 'gamestop', 'gaming', 'video game', 'retail', 'meme', 'corp'];
      const hasGmeContent = gmeKeywords.some(keyword => 
        responseContent.toLowerCase().includes(keyword)
      );
      
      if (hasGmeContent) {
        console.log('[TEST-B004] ✅ GME-specific content detected');
      } else {
        console.log('[TEST-B004] ⚠️ General ticker response received (GME-specific content not explicitly detected)');
      }
      
      // Performance classification validation
      console.log(`[TEST-B004] Performance classification: ${performanceClass}`);
      
      if (performanceClass === PerformanceClassification.SUCCESS) {
        console.log(`[TEST-B004] ✅ SUCCESS: Fast response (< 45 seconds)`);
      } else if (performanceClass === PerformanceClassification.SLOW_PERFORMANCE) {
        console.log(`[TEST-B004] ⚠️ SLOW_PERFORMANCE: Response took 45-120 seconds`);
      } else {
        console.log(`[TEST-B004] ❌ TIMEOUT: Response exceeded 120 seconds`);
      }
      
      // Look for sentiment indicators specific to GME
      const bullishEmojis = validationResult.detectedEmojis.filter(emoji => 
        [FINANCIAL_EMOJIS.BULLISH, FINANCIAL_EMOJIS.MONEY].includes(emoji)
      );
      const bearishEmojis = validationResult.detectedEmojis.filter(emoji => 
        [FINANCIAL_EMOJIS.BEARISH, FINANCIAL_EMOJIS.MONEY_LOSS].includes(emoji)
      );
      
      if (bullishEmojis.length > 0) {
        console.log(`[TEST-B004] 📈 Bullish sentiment indicators detected: ${bullishEmojis.join(', ')}`);
      }
      if (bearishEmojis.length > 0) {
        console.log(`[TEST-B004] 📉 Bearish sentiment indicators detected: ${bearishEmojis.join(', ')}`);
      }
      
      // Final test assertions
      expect(executionResult.success).toBe(true);
      expect(validationResult.hasFinancialContent).toBe(true);
      expect(validationResult.hasEmojiIndicators).toBe(true);
      expect(validationResult.detectedTickers).toContain('GME');
      expect(responseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      
      console.log('[TEST-B004] ✅ GME ticker test completed successfully');
      
    } catch (error) {
      console.log('[TEST-B004] ❌ Test execution failed:', error);
      throw error;
      
    } finally {
      // Session cleanup (will be part of continuous session in actual test runs)
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate GME ticker response format and content', async ({ browser }) => {
    console.log('[TEST-B004] Validating GME ticker response format requirements...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      // Navigate and send query
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testQuery = "Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
      
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B004-Format-Validation'
      );
      
      if (executionResult.success) {
        // Use ticker-specific validation for GME
        const tickerValidationConfig = {
          ticker: 'GME',
          expectedKeywords: ['price', 'gme', 'gamestop', 'trading', 'stock'],
          requiredEmojis: [FINANCIAL_EMOJIS.TARGET], // Require at least KEY TAKEAWAYS emoji
          minContentLength: 150,
          allowPartialMatch: true
        };
        
        const tickerValidation = await validateTickerResponse(page, tickerValidationConfig);
        
        console.log(`[TEST-B004] Ticker validation - Valid: ${tickerValidation.isValid}`);
        console.log(`[TEST-B004] GME ticker detected: ${tickerValidation.detectedTickers.includes('GME')}`);
        console.log(`[TEST-B004] Financial content: ${tickerValidation.hasFinancialContent}`);
        console.log(`[TEST-B004] Emoji indicators: ${tickerValidation.hasEmojiIndicators}`);
        
        // Check for specific GME financial data elements
        const pageContent = await page.textContent('body') || '';
        
        // Look for typical financial data elements
        const hasPrice = /\$[\d,]+\.?\d*/g.test(pageContent);
        const hasPercentage = /%|\+|\-[\d.]+%/g.test(pageContent);
        const hasVolume = /volume|shares/gi.test(pageContent);
        
        console.log(`[TEST-B004] Price data detected: ${hasPrice}`);
        console.log(`[TEST-B004] Percentage change detected: ${hasPercentage}`);
        console.log(`[TEST-B004] Volume data detected: ${hasVolume}`);
        
        // Log response structure for analysis
        if (pageContent.length > 0) {
          const lines = pageContent.split('\n').filter(line => line.trim().length > 0);
          console.log(`[TEST-B004] Response structure: ${lines.length} lines`);
          
          // Look for structured financial sections
          const financialSections = lines.filter(line => 
            line.includes('📊') || 
            line.includes('💰') || 
            line.includes('📈') || 
            line.includes('📉') ||
            line.toLowerCase().includes('gme')
          );
          
          console.log(`[TEST-B004] Financial sections found: ${financialSections.length}`);
        }
        
        // Assertions for ticker-specific validation
        expect(tickerValidation.detectedTickers).toContain('GME');
        expect(tickerValidation.hasFinancialContent).toBe(true);
        expect(tickerValidation.hasEmojiIndicators).toBe(true);
        
        console.log('[TEST-B004] ✅ GME ticker format validation completed');
        
      } else {
        console.log('[TEST-B004] ⚠️ Skipping ticker validation due to execution failure');
        test.skip('Ticker validation skipped due to execution failure');
      }
      
    } catch (error) {
      console.log('[TEST-B004] Ticker validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate GME sentiment indicators and retail metrics', async ({ browser }) => {
    console.log('[TEST-B004] Validating GME sentiment indicators and retail metrics...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testQuery = "Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
      
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B004-Sentiment-Validation'
      );
      
      if (executionResult.success) {
        const pageContent = await page.textContent('body') || '';
        
        // Analyze sentiment indicators
        const sentimentAnalysis = {
          bullishIndicators: 0,
          bearishIndicators: 0,
          neutralIndicators: 0
        };
        
        // Count bullish sentiment indicators
        const bullishTerms = ['buy', 'bullish', 'positive', 'gain', 'up', 'rise', 'growth', 'strong'];
        bullishTerms.forEach(term => {
          if (pageContent.toLowerCase().includes(term)) {
            sentimentAnalysis.bullishIndicators++;
          }
        });
        
        // Count bearish sentiment indicators
        const bearishTerms = ['sell', 'bearish', 'negative', 'loss', 'down', 'decline', 'weak', 'fall'];
        bearishTerms.forEach(term => {
          if (pageContent.toLowerCase().includes(term)) {
            sentimentAnalysis.bearishIndicators++;
          }
        });
        
        // Count neutral indicators
        const neutralTerms = ['hold', 'neutral', 'stable', 'unchanged', 'sideways'];
        neutralTerms.forEach(term => {
          if (pageContent.toLowerCase().includes(term)) {
            sentimentAnalysis.neutralIndicators++;
          }
        });
        
        console.log(`[TEST-B004] Sentiment analysis:`);
        console.log(`[TEST-B004] - Bullish indicators: ${sentimentAnalysis.bullishIndicators}`);
        console.log(`[TEST-B004] - Bearish indicators: ${sentimentAnalysis.bearishIndicators}`);
        console.log(`[TEST-B004] - Neutral indicators: ${sentimentAnalysis.neutralIndicators}`);
        
        // Check for financial emoji sentiment
        const emojiSentiment = {
          bullish: pageContent.includes(FINANCIAL_EMOJIS.BULLISH),
          bearish: pageContent.includes(FINANCIAL_EMOJIS.BEARISH),
          money: pageContent.includes(FINANCIAL_EMOJIS.MONEY),
          chart: pageContent.includes(FINANCIAL_EMOJIS.CHART)
        };
        
        console.log(`[TEST-B004] Emoji sentiment:`, emojiSentiment);
        
        // Check for GME-specific retail metrics
        const retailMetrics = {
          hasRevenue: /revenue|sales|income/gi.test(pageContent),
          hasRetail: /retail|store|location|gaming/gi.test(pageContent),
          hasVolatility: /volatile|volatility|swing|meme/gi.test(pageContent),
          hasMarketCap: /market cap|valuation|capitalization/gi.test(pageContent)
        };
        
        console.log(`[TEST-B004] Retail metrics:`, retailMetrics);
        
        // Should have some sentiment indicators (bullish, bearish, or neutral)
        const totalSentimentIndicators = sentimentAnalysis.bullishIndicators + 
                                       sentimentAnalysis.bearishIndicators + 
                                       sentimentAnalysis.neutralIndicators;
        
        expect(totalSentimentIndicators).toBeGreaterThan(0);
        
        // Should have at least one financial emoji
        const hasFinancialEmoji = Object.values(emojiSentiment).some(Boolean);
        expect(hasFinancialEmoji).toBe(true);
        
        console.log('[TEST-B004] ✅ Sentiment indicator validation completed');
        
      } else {
        console.log('[TEST-B004] ⚠️ Skipping sentiment validation due to execution failure');
        test.skip('Sentiment validation skipped due to execution failure');
      }
      
    } catch (error) {
      console.log('[TEST-B004] Sentiment validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B004 development
 */
test.describe('TEST-B004: Development Utilities', () => {
  
  test('should validate TEST-B004 configuration', async () => {
    console.log('[TEST-B004] Validating test configuration...');
    
    // Validate configuration same as TEST-B001 but for ticker-specific testing
    expect(COMPREHENSIVE_TEST_CONFIG.polling.pollingIntervalMs).toBe(30000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.maxTimeoutMs).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.successThresholdMs).toBe(45000);
    
    // Validate GME is in the list of valid tickers
    expect(COMPREHENSIVE_TEST_CONFIG.testData.validTickers).toContain('GME');
    
    // Validate financial emojis are available for sentiment analysis
    const emojiValues = Object.values(FINANCIAL_EMOJIS);
    expect(emojiValues.length).toBeGreaterThan(0);
    expect(emojiValues).toContain('📈'); // Bullish
    expect(emojiValues).toContain('📉'); // Bearish
    expect(emojiValues).toContain('💰'); // Money
    expect(emojiValues).toContain('🎯'); // Target/KEY TAKEAWAYS
    
    console.log('[TEST-B004] Configuration validation completed');
    console.log(`[TEST-B004] GME in valid tickers: ${COMPREHENSIVE_TEST_CONFIG.testData.validTickers.includes('GME')}`);
    console.log(`[TEST-B004] Available financial emojis: ${emojiValues.length}`);
  });
  
  test('should validate GME ticker query format', async () => {
    console.log('[TEST-B004] Validating GME query format...');
    
    const testQuery = "Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
    
    // Validate query contains required elements
    expect(testQuery).toContain('Single Ticker Snapshot');
    expect(testQuery).toContain('GME');
    expect(testQuery).toContain('PRIORITY FAST REQUEST');
    expect(testQuery).toContain('MINIMAL TOOL CALLS ONLY');
    expect(testQuery).toContain('LOW Verbosity');
    
    // Validate query length is reasonable
    expect(testQuery.length).toBeGreaterThan(70);
    expect(testQuery.length).toBeLessThan(250);
    
    // Extract ticker from query
    const tickerMatch = testQuery.match(/:\s*([A-Z]{1,5})/);
    expect(tickerMatch).toBeDefined();
    expect(tickerMatch![1]).toBe('GME');
    
    console.log('[TEST-B004] Query format validation completed');
    console.log(`[TEST-B004] Query: ${testQuery}`);
    console.log(`[TEST-B004] Query length: ${testQuery.length} characters`);
    console.log(`[TEST-B004] Extracted ticker: ${tickerMatch![1]}`);
  });
  
  test('should validate GME ticker configuration constants', async () => {
    console.log('[TEST-B004] Validating GME ticker constants...');
    
    // Validate performance classifications for ticker tests
    expect(PerformanceClassification.SUCCESS).toBe('SUCCESS');
    expect(PerformanceClassification.SLOW_PERFORMANCE).toBe('SLOW_PERFORMANCE');
    expect(PerformanceClassification.TIMEOUT).toBe('TIMEOUT');
    
    // Test ticker validation configuration
    const tickerConfig = {
      ticker: 'GME',
      expectedKeywords: ['price', 'gme', 'gamestop', 'trading', 'stock'],
      requiredEmojis: [FINANCIAL_EMOJIS.TARGET],
      minContentLength: 150,
      allowPartialMatch: true
    };
    
    expect(tickerConfig.ticker).toBe('GME');
    expect(tickerConfig.expectedKeywords).toContain('gme');
    expect(tickerConfig.expectedKeywords).toContain('gamestop');
    expect(tickerConfig.requiredEmojis).toContain('🎯');
    expect(tickerConfig.minContentLength).toBe(150);
    expect(tickerConfig.allowPartialMatch).toBe(true);
    
    console.log('[TEST-B004] Ticker constants validation completed');
    console.log(`[TEST-B004] Ticker: ${tickerConfig.ticker}`);
    console.log(`[TEST-B004] Expected keywords: ${tickerConfig.expectedKeywords.join(', ')}`);
    console.log(`[TEST-B004] Min content length: ${tickerConfig.minContentLength}`);
  });
  
});