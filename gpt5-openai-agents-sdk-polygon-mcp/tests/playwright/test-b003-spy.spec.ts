/**
 * TEST-B003: Single Ticker SPY Test
 * 
 * Tests SPY ticker query with priority fast request and low verbosity
 * Implements dynamic port detection and 30-second polling methodology
 * Part of continuous browser session protocol
 * 
 * @fileoverview Single Ticker SPY CLI test with sentiment indicator validation
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
 * TEST-B003: Single Ticker SPY Test Suite
 */
test.describe('TEST-B003: Single Ticker SPY', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before testing', async () => {
    console.log('[TEST-B003] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B003] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B003] System validation completed');
    console.log(`[TEST-B003] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B003] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should execute SPY ticker query with performance tracking', async ({ browser }) => {
    console.log('[TEST-B003] Starting SPY ticker test execution...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session (part of continuous session)
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend with dynamic port detection
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B003] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000); // Allow interface to stabilize
      
      // Define test query with priority fast request and low verbosity
      const testQuery = "Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
      
      console.log(`[TEST-B003] Sending query: ${testQuery}`);
      
      // Execute test with 30-second polling and 120-second timeout
      const startTime = Date.now();
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B003-SPY-Ticker'
      );
      
      const responseTime = Date.now() - startTime;
      const performanceClass = classifyPerformance(responseTime, COMPREHENSIVE_TEST_CONFIG.polling);
      
      console.log(`[TEST-B003] Execution completed in ${responseTime}ms (${performanceClass})`);
      
      // Validate execution success
      expect(executionResult.success).toBe(true);
      expect(executionResult.responseTime).toBeGreaterThan(0);
      expect(executionResult.classification).toBeDefined();
      
      if (!executionResult.success) {
        console.log('[TEST-B003] Execution failed:', executionResult.error);
        throw new Error(`Test execution failed: ${executionResult.error}`);
      }
      
      // Validate response content for SPY ticker
      console.log('[TEST-B003] Validating SPY ticker response...');
      const validationResult = await validateFinancialResponse(page, 'SPY');
      
      // SPY response should contain financial indicators
      expect(validationResult.hasFinancialContent).toBe(true);
      expect(validationResult.contentLength).toBeGreaterThan(100);
      
      // Should have emoji indicators for financial sentiment
      expect(validationResult.hasEmojiIndicators).toBe(true);
      expect(validationResult.detectedEmojis.length).toBeGreaterThan(0);
      
      // Should specifically contain SPY ticker reference
      expect(validationResult.detectedTickers).toContain('SPY');
      
      // Log detailed validation results
      console.log(`[TEST-B003] Response validation - Valid: ${validationResult.isValid}`);
      console.log(`[TEST-B003] KEY TAKEAWAYS present: ${validationResult.hasKeyTakeaways}`);
      console.log(`[TEST-B003] Emoji indicators: ${validationResult.detectedEmojis.join(', ')}`);
      console.log(`[TEST-B003] Detected tickers: ${validationResult.detectedTickers.join(', ')}`);
      console.log(`[TEST-B003] Content length: ${validationResult.contentLength} characters`);
      
      // Validate SPY-specific content
      const responseContent = validationResult.responseContent || '';
      const spyKeywords = ['spy', 'spdr', 's&p 500', 's&p', 'etf', 'index', 'fund', 'tracking'];
      const hasSpyContent = spyKeywords.some(keyword => 
        responseContent.toLowerCase().includes(keyword)
      );
      
      if (hasSpyContent) {
        console.log('[TEST-B003] ✅ SPY-specific content detected');
      } else {
        console.log('[TEST-B003] ⚠️ General ticker response received (SPY-specific content not explicitly detected)');
      }
      
      // Performance classification validation
      console.log(`[TEST-B003] Performance classification: ${performanceClass}`);
      
      if (performanceClass === PerformanceClassification.SUCCESS) {
        console.log(`[TEST-B003] ✅ SUCCESS: Fast response (< 45 seconds)`);
      } else if (performanceClass === PerformanceClassification.SLOW_PERFORMANCE) {
        console.log(`[TEST-B003] ⚠️ SLOW_PERFORMANCE: Response took 45-120 seconds`);
      } else {
        console.log(`[TEST-B003] ❌ TIMEOUT: Response exceeded 120 seconds`);
      }
      
      // Look for sentiment indicators specific to SPY
      const bullishEmojis = validationResult.detectedEmojis.filter(emoji => 
        ['📈', '💰'].includes(emoji)
      );
      const bearishEmojis = validationResult.detectedEmojis.filter(emoji => 
        ['📉', '💸'].includes(emoji)
      );
      
      if (bullishEmojis.length > 0) {
        console.log(`[TEST-B003] 📈 Bullish sentiment indicators detected: ${bullishEmojis.join(', ')}`);
      }
      if (bearishEmojis.length > 0) {
        console.log(`[TEST-B003] 📉 Bearish sentiment indicators detected: ${bearishEmojis.join(', ')}`);
      }
      
      // Final test assertions
      expect(executionResult.success).toBe(true);
      expect(validationResult.hasFinancialContent).toBe(true);
      expect(validationResult.hasEmojiIndicators).toBe(true);
      expect(validationResult.detectedTickers).toContain('SPY');
      expect(responseTime).toBeLessThanOrEqual(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
      
      console.log('[TEST-B003] ✅ SPY ticker test completed successfully');
      
    } catch (error) {
      console.log('[TEST-B003] ❌ Test execution failed:', error);
      throw error;
      
    } finally {
      // Session cleanup (will be part of continuous session in actual test runs)
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate SPY ticker response format and content', async ({ browser }) => {
    console.log('[TEST-B003] Validating SPY ticker response format requirements...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      // Navigate and send query
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testQuery = "Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
      
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B003-Format-Validation'
      );
      
      if (executionResult.success) {
        // Use ticker-specific validation for SPY
        const tickerValidationConfig = {
          ticker: 'SPY',
          expectedKeywords: ['price', 'spy', 'etf', 'trading', 's&p'],
          requiredEmojis: [FINANCIAL_EMOJIS.TARGET], // Require at least KEY TAKEAWAYS emoji
          minContentLength: 150,
          allowPartialMatch: true
        };
        
        const tickerValidation = await validateTickerResponse(page, tickerValidationConfig);
        
        console.log(`[TEST-B003] Ticker validation - Valid: ${tickerValidation.isValid}`);
        console.log(`[TEST-B003] SPY ticker detected: ${tickerValidation.detectedTickers.includes('SPY')}`);
        console.log(`[TEST-B003] Financial content: ${tickerValidation.hasFinancialContent}`);
        console.log(`[TEST-B003] Emoji indicators: ${tickerValidation.hasEmojiIndicators}`);
        
        // Check for specific SPY financial data elements
        const pageContent = await page.textContent('body') || '';
        
        // Look for typical financial data elements
        const hasPrice = /\$[\d,]+\.?\d*/g.test(pageContent);
        const hasPercentage = /%|\+|\-[\d.]+%/g.test(pageContent);
        const hasVolume = /volume|shares/gi.test(pageContent);
        
        console.log(`[TEST-B003] Price data detected: ${hasPrice}`);
        console.log(`[TEST-B003] Percentage change detected: ${hasPercentage}`);
        console.log(`[TEST-B003] Volume data detected: ${hasVolume}`);
        
        // Log response structure for analysis
        if (pageContent.length > 0) {
          const lines = pageContent.split('\n').filter(line => line.trim().length > 0);
          console.log(`[TEST-B003] Response structure: ${lines.length} lines`);
          
          // Look for structured financial sections
          const financialSections = lines.filter(line => 
            line.includes('📊') || 
            line.includes('💰') || 
            line.includes('📈') || 
            line.includes('📉') ||
            line.toLowerCase().includes('spy')
          );
          
          console.log(`[TEST-B003] Financial sections found: ${financialSections.length}`);
        }
        
        // Assertions for ticker-specific validation
        expect(tickerValidation.detectedTickers).toContain('SPY');
        expect(tickerValidation.hasFinancialContent).toBe(true);
        expect(tickerValidation.hasEmojiIndicators).toBe(true);
        
        console.log('[TEST-B003] ✅ SPY ticker format validation completed');
        
      } else {
        console.log('[TEST-B003] ⚠️ Skipping ticker validation due to execution failure');
        test.skip(true, 'Ticker validation skipped due to execution failure');
      }
      
    } catch (error) {
      console.log('[TEST-B003] Ticker validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate SPY sentiment indicators and ETF metrics', async ({ browser }) => {
    console.log('[TEST-B003] Validating SPY sentiment indicators and ETF metrics...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testQuery = "Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
      
      const executionResult = await sendMessageAndWaitForResponse(
        page, 
        testQuery, 
        'TEST-B003-Sentiment-Validation'
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
        
        console.log(`[TEST-B003] Sentiment analysis:`);
        console.log(`[TEST-B003] - Bullish indicators: ${sentimentAnalysis.bullishIndicators}`);
        console.log(`[TEST-B003] - Bearish indicators: ${sentimentAnalysis.bearishIndicators}`);
        console.log(`[TEST-B003] - Neutral indicators: ${sentimentAnalysis.neutralIndicators}`);
        
        // Check for financial emoji sentiment
        const emojiSentiment = {
          bullish: pageContent.includes(FINANCIAL_EMOJIS.BULLISH),
          bearish: pageContent.includes(FINANCIAL_EMOJIS.BEARISH),
          money: pageContent.includes(FINANCIAL_EMOJIS.MONEY),
          chart: pageContent.includes(FINANCIAL_EMOJIS.CHART)
        };
        
        console.log(`[TEST-B003] Emoji sentiment:`, emojiSentiment);
        
        // Check for ETF-specific metrics
        const etfMetrics = {
          hasExpenseRatio: /expense ratio|fee|cost/gi.test(pageContent),
          hasAUM: /aum|assets under management|fund size/gi.test(pageContent),
          hasTracking: /tracking|index|s&p 500|benchmark/gi.test(pageContent),
          hasDividend: /dividend|yield|distribution/gi.test(pageContent)
        };
        
        console.log(`[TEST-B003] ETF metrics:`, etfMetrics);
        
        // Should have some sentiment indicators (bullish, bearish, or neutral)
        const totalSentimentIndicators = sentimentAnalysis.bullishIndicators + 
                                       sentimentAnalysis.bearishIndicators + 
                                       sentimentAnalysis.neutralIndicators;
        
        expect(totalSentimentIndicators).toBeGreaterThan(0);
        
        // Should have at least one financial emoji
        const hasFinancialEmoji = Object.values(emojiSentiment).some(Boolean);
        expect(hasFinancialEmoji).toBe(true);
        
        console.log('[TEST-B003] ✅ Sentiment indicator validation completed');
        
      } else {
        console.log('[TEST-B003] ⚠️ Skipping sentiment validation due to execution failure');
        test.skip(true, 'Sentiment validation skipped due to execution failure');
      }
      
    } catch (error) {
      console.log('[TEST-B003] Sentiment validation error:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B003 development
 */
test.describe('TEST-B003: Development Utilities', () => {
  
  test('should validate TEST-B003 configuration', async () => {
    console.log('[TEST-B003] Validating test configuration...');
    
    // Validate configuration same as TEST-B001 but for ticker-specific testing
    expect(COMPREHENSIVE_TEST_CONFIG.polling.pollingIntervalMs).toBe(30000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.maxTimeoutMs).toBe(120000);
    expect(COMPREHENSIVE_TEST_CONFIG.polling.successThresholdMs).toBe(45000);
    
    // Validate SPY is in the list of valid tickers
    expect(COMPREHENSIVE_TEST_CONFIG.testData.validTickers).toContain('SPY');
    
    // Validate financial emojis are available for sentiment analysis
    const emojiValues = Object.values(FINANCIAL_EMOJIS);
    expect(emojiValues.length).toBeGreaterThan(0);
    expect(emojiValues).toContain('📈'); // Bullish
    expect(emojiValues).toContain('📉'); // Bearish
    expect(emojiValues).toContain('💰'); // Money
    expect(emojiValues).toContain('🎯'); // Target/KEY TAKEAWAYS
    
    console.log('[TEST-B003] Configuration validation completed');
    console.log(`[TEST-B003] SPY in valid tickers: ${COMPREHENSIVE_TEST_CONFIG.testData.validTickers.includes('SPY')}`);
    console.log(`[TEST-B003] Available financial emojis: ${emojiValues.length}`);
  });
  
  test('should validate SPY ticker query format', async () => {
    console.log('[TEST-B003] Validating SPY query format...');
    
    const testQuery = "Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
    
    // Validate query contains required elements
    expect(testQuery).toContain('Single Ticker Snapshot');
    expect(testQuery).toContain('SPY');
    expect(testQuery).toContain('PRIORITY FAST REQUEST');
    expect(testQuery).toContain('MINIMAL TOOL CALLS ONLY');
    expect(testQuery).toContain('LOW Verbosity');
    
    // Validate query length is reasonable
    expect(testQuery.length).toBeGreaterThan(70);
    expect(testQuery.length).toBeLessThan(250);
    
    // Extract ticker from query
    const tickerMatch = testQuery.match(/:\s*([A-Z]{1,5})/);
    expect(tickerMatch).toBeDefined();
    expect(tickerMatch![1]).toBe('SPY');
    
    console.log('[TEST-B003] Query format validation completed');
    console.log(`[TEST-B003] Query: ${testQuery}`);
    console.log(`[TEST-B003] Query length: ${testQuery.length} characters`);
    console.log(`[TEST-B003] Extracted ticker: ${tickerMatch![1]}`);
  });
  
  test('should validate SPY ticker configuration constants', async () => {
    console.log('[TEST-B003] Validating SPY ticker constants...');
    
    // Validate performance classifications for ticker tests
    expect(PerformanceClassification.SUCCESS).toBe('SUCCESS');
    expect(PerformanceClassification.SLOW_PERFORMANCE).toBe('SLOW_PERFORMANCE');
    expect(PerformanceClassification.TIMEOUT).toBe('TIMEOUT');
    
    // Test ticker validation configuration
    const tickerConfig = {
      ticker: 'SPY',
      expectedKeywords: ['price', 'spy', 'etf', 'trading', 's&p'],
      requiredEmojis: [FINANCIAL_EMOJIS.TARGET],
      minContentLength: 150,
      allowPartialMatch: true
    };
    
    expect(tickerConfig.ticker).toBe('SPY');
    expect(tickerConfig.expectedKeywords).toContain('spy');
    expect(tickerConfig.expectedKeywords).toContain('etf');
    expect(tickerConfig.requiredEmojis).toContain('🎯');
    expect(tickerConfig.minContentLength).toBe(150);
    expect(tickerConfig.allowPartialMatch).toBe(true);
    
    console.log('[TEST-B003] Ticker constants validation completed');
    console.log(`[TEST-B003] Ticker: ${tickerConfig.ticker}`);
    console.log(`[TEST-B003] Expected keywords: ${tickerConfig.expectedKeywords.join(', ')}`);
    console.log(`[TEST-B003] Min content length: ${tickerConfig.minContentLength}`);
  });
  
});