/**
 * Response Validation Functions for Playwright Tests
 *
 * Test-specific validation logic for Phase 2 of auto-retry detection.
 * Each validator checks response content against expected criteria for PASS/FAIL determination.
 *
 * @fileoverview Test-specific response validation for financial data analysis
 */

import { ValidationResult } from './auto-retry';

/**
 * Test-specific validation result
 */
export interface TestValidationResult {
  testName: string;
  status: 'PASS' | 'FAIL';
  responseContent: string;
  validationDetails: ValidationResult;
  specificChecks: Record<string, boolean>;
  failureReasons: string[];
}

/**
 * Validate B001: Market Status response
 */
export function validateMarketStatusResponse(
  responseContent: string,
  testName: string = 'B001'
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for market status keywords
  const marketStatusKeywords = ['market', 'status', 'trading', 'session', 'hours', 'open', 'closed', 'exchange'];
  const hasMarketStatusContent = marketStatusKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasMarketStatusContent = hasMarketStatusContent;
  if (!hasMarketStatusContent) {
    failureReasons.push('Missing market status indicators (market, trading, session, etc.)');
  }

  // Check for exchange information
  const exchangeKeywords = ['NYSE', 'NASDAQ', 'exchange', 'market hours'];
  const hasExchangeInfo = exchangeKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword.toLowerCase())
  );
  specificChecks.hasExchangeInfo = hasExchangeInfo;
  if (!hasExchangeInfo) {
    failureReasons.push('Missing exchange information');
  }

  // Check for financial emojis
  const financialEmojis = ['📈', '📉', '💰', '💸', '🏢', '📊'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  // Check response length
  const hasMinimumLength = responseContent.length > 100;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 100)`);
  }

  // Overall validation
  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasMarketStatusContent && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Validate B002: NVDA Ticker Analysis response
 */
export function validateNVDAResponse(
  responseContent: string,
  testName: string = 'B002'
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for NVDA/NVIDIA content
  const hasNVDAContent = responseContent.toLowerCase().includes('nvda') ||
                        responseContent.toLowerCase().includes('nvidia');
  specificChecks.hasNVDAContent = hasNVDAContent;
  if (!hasNVDAContent) {
    failureReasons.push('Missing NVDA/NVIDIA ticker content');
  }

  // Check for stock analysis indicators
  const stockAnalysisKeywords = ['price', 'volume', 'analysis', 'stock', 'shares'];
  const hasStockAnalysis = stockAnalysisKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasStockAnalysis = hasStockAnalysis;
  if (!hasStockAnalysis) {
    failureReasons.push('Missing stock analysis indicators');
  }

  // Check for sentiment indicators
  const sentimentKeywords = ['bullish', 'bearish', 'buy', 'sell', 'hold'];
  const hasSentiment = sentimentKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasSentiment = hasSentiment;

  // Check for financial emojis
  const financialEmojis = ['📈', '📉', '💰', '🎯'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  // Check response length
  const hasMinimumLength = responseContent.length > 150;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 150)`);
  }

  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasNVDAContent && hasStockAnalysis && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Validate B003: SPY ETF Analysis response
 */
export function validateSPYResponse(
  responseContent: string,
  testName: string = 'B003'
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for SPY content
  const hasSPYContent = responseContent.toLowerCase().includes('spy') ||
                       responseContent.toLowerCase().includes('s&p 500') ||
                       responseContent.toLowerCase().includes('spdr');
  specificChecks.hasSPYContent = hasSPYContent;
  if (!hasSPYContent) {
    failureReasons.push('Missing SPY/S&P 500 ETF content');
  }

  // Check for ETF analysis indicators
  const etfKeywords = ['etf', 'fund', 'portfolio', 'sectors', 'holdings'];
  const hasETFAnalysis = etfKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasETFAnalysis = hasETFAnalysis;
  if (!hasETFAnalysis) {
    failureReasons.push('Missing ETF analysis indicators');
  }

  // Check for sector performance
  const sectorKeywords = ['technology', 'sector', 'performance', 'allocation'];
  const hasSectorInfo = sectorKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasSectorInfo = hasSectorInfo;

  const financialEmojis = ['📈', '📉', '💰', '📊'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  const hasMinimumLength = responseContent.length > 150;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 150)`);
  }

  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasSPYContent && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Validate B004: GME Analysis response
 */
export function validateGMEResponse(
  responseContent: string,
  testName: string = 'B004'
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for GME content
  const hasGMEContent = responseContent.toLowerCase().includes('gme') ||
                       responseContent.toLowerCase().includes('gamestop');
  specificChecks.hasGMEContent = hasGMEContent;
  if (!hasGMEContent) {
    failureReasons.push('Missing GME/GameStop content');
  }

  // Check for volatility indicators
  const volatilityKeywords = ['volatility', 'volatile', 'meme', 'retail', 'squeeze'];
  const hasVolatilityInfo = volatilityKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasVolatilityInfo = hasVolatilityInfo;

  // Check for volume analysis
  const volumeKeywords = ['volume', 'trading volume', 'spike'];
  const hasVolumeInfo = volumeKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasVolumeInfo = hasVolumeInfo;

  const financialEmojis = ['📈', '📉', '💰', '🎮'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  const hasMinimumLength = responseContent.length > 150;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 150)`);
  }

  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasGMEContent && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Validate B005: Multi-Ticker Analysis response
 */
export function validateMultiTickerResponse(
  responseContent: string,
  testName: string = 'B005'
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for multiple tickers
  const expectedTickers = ['NVDA', 'SPY', 'QQQ', 'IWM'];
  const foundTickers = expectedTickers.filter(ticker =>
    responseContent.toUpperCase().includes(ticker)
  );
  const hasMultipleTickers = foundTickers.length >= 3;
  specificChecks.hasMultipleTickers = hasMultipleTickers;
  if (!hasMultipleTickers) {
    failureReasons.push(`Only found ${foundTickers.length}/4 expected tickers: ${foundTickers.join(', ')}`);
  }

  // Check for comparative analysis
  const comparisonKeywords = ['comparison', 'compare', 'versus', 'relative', 'correlation'];
  const hasComparison = comparisonKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasComparison = hasComparison;

  // Check for cross-market analysis
  const marketKeywords = ['market', 'sector', 'index', 'performance'];
  const hasMarketAnalysis = marketKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasMarketAnalysis = hasMarketAnalysis;

  const financialEmojis = ['📈', '📉', '💰', '📊'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  const hasMinimumLength = responseContent.length > 200;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 200)`);
  }

  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasMultipleTickers && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Validate B007: Stock Snapshot Button response
 */
export function validateStockSnapshotResponse(
  responseContent: string,
  testName: string = 'B007'
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for snapshot indicators
  const snapshotKeywords = ['snapshot', 'overview', 'summary', 'current'];
  const hasSnapshotContent = snapshotKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasSnapshotContent = hasSnapshotContent;
  if (!hasSnapshotContent) {
    failureReasons.push('Missing snapshot/overview content');
  }

  // Check for stock analysis
  const stockKeywords = ['price', 'stock', 'shares', 'value'];
  const hasStockAnalysis = stockKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasStockAnalysis = hasStockAnalysis;
  if (!hasStockAnalysis) {
    failureReasons.push('Missing stock analysis content');
  }

  const financialEmojis = ['📈', '📉', '💰', '📊'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  const hasMinimumLength = responseContent.length > 100;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 100)`);
  }

  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasSnapshotContent && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Validate B008: Support/Resistance Button response
 */
export function validateSupportResistanceResponse(
  responseContent: string,
  testName: string = 'B008'
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for support/resistance content
  const srKeywords = ['support', 'resistance', 'levels', 'technical'];
  const hasSRContent = srKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasSRContent = hasSRContent;
  if (!hasSRContent) {
    failureReasons.push('Missing support/resistance content');
  }

  // Check for technical analysis indicators
  const technicalKeywords = ['technical', 'analysis', 'chart', 'pattern'];
  const hasTechnicalAnalysis = technicalKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasTechnicalAnalysis = hasTechnicalAnalysis;

  const financialEmojis = ['📈', '📉', '💰', '📊'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  const hasMinimumLength = responseContent.length > 100;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 100)`);
  }

  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasSRContent && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Validate B009: Technical Analysis Button response
 */
export function validateTechnicalAnalysisResponse(
  responseContent: string,
  testName: string = 'B009'
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for technical analysis content
  const technicalKeywords = ['technical', 'analysis', 'indicators', 'signals'];
  const hasTechnicalContent = technicalKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasTechnicalContent = hasTechnicalContent;
  if (!hasTechnicalContent) {
    failureReasons.push('Missing technical analysis content');
  }

  // Check for indicator mentions
  const indicatorKeywords = ['rsi', 'macd', 'moving average', 'bollinger', 'stochastic'];
  const hasIndicators = indicatorKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasIndicators = hasIndicators;

  const financialEmojis = ['📈', '📉', '💰', '🔧'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  const hasMinimumLength = responseContent.length > 150;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 150)`);
  }

  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasTechnicalContent && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Generic validation for any financial response
 */
export function validateGenericFinancialResponse(
  responseContent: string,
  testName: string
): TestValidationResult {

  const specificChecks: Record<string, boolean> = {};
  const failureReasons: string[] = [];

  // Check for any financial content
  const financialKeywords = [
    'stock', 'price', 'volume', 'market', 'trading', 'analysis',
    'bullish', 'bearish', 'buy', 'sell', 'investment'
  ];
  const hasFinancialContent = financialKeywords.some(keyword =>
    responseContent.toLowerCase().includes(keyword)
  );
  specificChecks.hasFinancialContent = hasFinancialContent;
  if (!hasFinancialContent) {
    failureReasons.push('Missing financial content');
  }

  const financialEmojis = ['📈', '📉', '💰', '📊', '🎯'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;
  specificChecks.hasEmojiIndicators = hasEmojiIndicators;
  if (!hasEmojiIndicators) {
    failureReasons.push('Missing financial emoji indicators');
  }

  const hasMinimumLength = responseContent.length > 50;
  specificChecks.hasMinimumLength = hasMinimumLength;
  if (!hasMinimumLength) {
    failureReasons.push(`Response too short (${responseContent.length} chars, minimum 50)`);
  }

  const baseValidation = createBaseValidation(responseContent);
  const status: 'PASS' | 'FAIL' =
    hasFinancialContent && hasEmojiIndicators && hasMinimumLength ? 'PASS' : 'FAIL';

  return {
    testName,
    status,
    responseContent,
    validationDetails: baseValidation,
    specificChecks,
    failureReasons
  };
}

/**
 * Route to appropriate validator based on test name
 */
export function validateResponseByTestName(
  testName: string,
  responseContent: string
): TestValidationResult {

  switch (testName.toUpperCase()) {
    case 'B001':
    case 'TEST-B001':
    case 'MARKET-STATUS':
      return validateMarketStatusResponse(responseContent, testName);

    case 'B002':
    case 'TEST-B002':
    case 'NVDA':
      return validateNVDAResponse(responseContent, testName);

    case 'B003':
    case 'TEST-B003':
    case 'SPY':
      return validateSPYResponse(responseContent, testName);

    case 'B004':
    case 'TEST-B004':
    case 'GME':
      return validateGMEResponse(responseContent, testName);

    case 'B005':
    case 'TEST-B005':
    case 'MULTI-TICKER':
      return validateMultiTickerResponse(responseContent, testName);

    case 'B007':
    case 'TEST-B007':
    case 'STOCK-SNAPSHOT':
      return validateStockSnapshotResponse(responseContent, testName);

    case 'B008':
    case 'TEST-B008':
    case 'SUPPORT-RESISTANCE':
      return validateSupportResistanceResponse(responseContent, testName);

    case 'B009':
    case 'TEST-B009':
    case 'TECHNICAL-ANALYSIS':
      return validateTechnicalAnalysisResponse(responseContent, testName);

    default:
      return validateGenericFinancialResponse(responseContent, testName);
  }
}

/**
 * Create base validation structure
 */
function createBaseValidation(responseContent: string): ValidationResult {
  // Detect financial content
  const financialKeywords = [
    'stock', 'price', 'volume', 'market', 'trading', 'analysis',
    'bullish', 'bearish', 'buy', 'sell', 'investment', 'portfolio'
  ];
  const contentLower = responseContent.toLowerCase();
  const matchCount = financialKeywords.filter(keyword =>
    contentLower.includes(keyword)
  ).length;
  const hasFinancialContent = matchCount >= 2;

  // Detect emojis
  const financialEmojis = ['📈', '📉', '💰', '💸', '🏢', '📊', '🎯'];
  const detectedEmojis = financialEmojis.filter(emoji => responseContent.includes(emoji));
  const hasEmojiIndicators = detectedEmojis.length > 0;

  // Detect tickers
  const tickerRegex = /\b[A-Z]{2,5}\b/g;
  const matches = responseContent.match(tickerRegex) || [];
  const detectedTickers = [...new Set(matches.filter(match =>
    match.length >= 2 && match.length <= 5 &&
    !['THE', 'AND', 'FOR', 'ARE', 'YOU', 'NOT', 'BUT'].includes(match)
  ))];

  return {
    isValid: hasFinancialContent && hasEmojiIndicators && responseContent.length > 50,
    hasFinancialContent,
    hasEmojiIndicators,
    contentLength: responseContent.length,
    detectedEmojis,
    detectedTickers
  };
}