# PLAYWRIGHT TESTING MASTER PLAN

**Single Source of Truth for Playwright Testing Framework**  
**Market Parser Application - Complete B001-B016 Test Suite**

---

## Overview

This document provides comprehensive guidance for executing the complete B001-B016 Playwright test suite for the Market Parser application. It consolidates all testing knowledge into a single authoritative reference, offering two proven methodologies: CLI automation and MCP browser tools.

### Key Features
- **Complete Test Coverage**: All 16 real B001-B016 tests with accurate specifications
- **Dual Methodology Support**: Both CLI (`npx playwright test`) and MCP browser automation
- **Single Browser Session Protocol**: Maintains session continuity for realistic user simulation
- **Performance Validation**: 30-second polling with 120-second timeout per test
- **Proven Success**: Based on actual successful test executions with 78%+ pass rates

---

## Quick Start Guide

### Prerequisites
1. **Backend Server Running**: FastAPI on port 8000 with "Application startup complete" message
2. **Frontend Server Running**: Vite on port 3000+ (auto-adjusts) with "VITE ready" message
3. **Health Verification**: Both servers responding to health checks
4. **Browser Capability**: Chromium installed for Playwright automation

### Choose Your Testing Method
- **CLI Method**: Use `npx playwright test` commands for traditional automation
- **MCP Method**: Use MCP browser tools for sophisticated browser control

---

## B001-B016 Test Suite Specifications

### Market/Ticker Analysis Tests (B001-B006)

#### B001: Market Status Check
- **File**: `test-b001-market-status.spec.ts`
- **Purpose**: Validates basic market connectivity and API health
- **Query**: "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
- **Expected**: Market status with exchange operational data and emoji indicators
- **Performance Target**: <45 seconds

#### B002: NVDA Ticker Analysis  
- **File**: `test-b002-nvda.spec.ts`
- **Purpose**: Tests NVIDIA stock analysis with comprehensive financial data
- **Query**: NVDA ticker analysis with priority fast request
- **Expected**: Complete stock analysis with 📈📉 sentiment indicators
- **Performance Target**: <45 seconds

#### B003: SPY Ticker Analysis
- **File**: `test-b003-spy.spec.ts`  
- **Purpose**: Validates S&P 500 ETF analysis and broad market data
- **Query**: SPY ticker analysis with priority fast request
- **Expected**: ETF analysis with "🎯 KEY TAKEAWAYS" structure
- **Performance Target**: <45 seconds

#### B004: GME Ticker Analysis
- **File**: `test-b004-gme.spec.ts`
- **Purpose**: Tests GameStop stock analysis and meme stock handling
- **Query**: GME ticker analysis with priority fast request
- **Expected**: Stock analysis with comprehensive financial metrics
- **Performance Target**: <45 seconds

#### B005: Multi-Ticker Analysis
- **File**: `test-b005-multi-ticker.spec.ts`
- **Purpose**: Validates complex multi-ticker comparison analysis
- **Query**: Multiple stock comparison with priority fast request
- **Expected**: Comparative analysis across multiple tickers
- **Performance Target**: <60 seconds (complex processing)

#### B006: Empty Message Handling
- **File**: `test-b006-empty-message.spec.ts`
- **Purpose**: Tests error handling for invalid input validation
- **Query**: Empty or invalid input submission
- **Expected**: Clear error feedback and proper input validation
- **Performance Target**: Instant response

### Button Template System Tests (B007-B016)

#### B007: Stock Snapshot Button
- **File**: `test-b007-stock-snapshot-button.spec.ts`
- **Purpose**: Tests Stock Snapshot (📈) button functionality
- **Action**: Click market snapshot button with NVDA ticker
- **Expected**: Complete stock snapshot analysis triggered by button
- **Performance Target**: <60 seconds

#### B008: Support/Resistance Button
- **File**: `test-b008-support-resistance-button.spec.ts`
- **Purpose**: Tests Support/Resistance (📊) button functionality
- **Action**: Click support/resistance analysis button
- **Expected**: Technical analysis with support/resistance levels
- **Performance Target**: <60 seconds

#### B009: Technical Analysis Button
- **File**: `test-b009-technical-analysis-button.spec.ts`
- **Purpose**: Tests Technical Analysis (🔧) button functionality
- **Action**: Click technical analysis button for comprehensive indicators
- **Expected**: Complete technical analysis with multiple indicators
- **Performance Target**: <60 seconds

#### B010: Multi-Button Interaction
- **File**: `test-b010-multi-button-interaction.spec.ts`
- **Purpose**: Tests sequential button interactions and state management
- **Action**: Multiple button clicks in sequence
- **Expected**: Proper state management across multiple interactions
- **Performance Target**: <90 seconds

#### B011: Button State Validation
- **File**: `test-b011-button-state-validation.spec.ts`
- **Purpose**: Validates button states and UI feedback during processing
- **Action**: Monitor button states during API processing
- **Expected**: Proper loading states and UI feedback mechanisms
- **Performance Target**: <60 seconds

#### B012: Button Error Handling
- **File**: `test-b012-button-error-handling.spec.ts`
- **Purpose**: Tests button error scenarios and recovery mechanisms
- **Action**: Trigger error conditions via button interactions
- **Expected**: Graceful error handling and user feedback
- **Performance Target**: <60 seconds

#### B013: Button Performance Validation
- **File**: `test-b013-button-performance-validation.spec.ts`
- **Purpose**: Validates button performance under various conditions
- **Action**: Performance testing of button response times
- **Expected**: Consistent performance within acceptable thresholds
- **Performance Target**: <60 seconds

#### B014: Button Accessibility
- **File**: `test-b014-button-accessibility.spec.ts`
- **Purpose**: Tests accessibility compliance for button interactions
- **Action**: Keyboard navigation and screen reader compatibility
- **Expected**: Full accessibility compliance for all button functions
- **Performance Target**: <60 seconds

#### B015: Button UI Consistency
- **File**: `test-b015-button-ui-consistency.spec.ts`
- **Purpose**: Validates consistent UI behavior across button interactions
- **Action**: UI consistency checks across all button states
- **Expected**: Consistent visual feedback and behavior patterns
- **Performance Target**: <60 seconds

#### B016: Button Integration
- **File**: `test-b016-button-integration.spec.ts`
- **Purpose**: Tests complete button system integration and end-to-end workflow
- **Action**: Full integration testing across all button functionality
- **Expected**: Complete button system working in integrated environment
- **Performance Target**: <90 seconds

---

## CLI Testing Methodology

### Setup and Execution

#### Environment Preparation
```bash
# Verify servers are running
curl -f http://localhost:8000/health || echo "❌ Backend not ready"
curl -f http://localhost:3000/ || curl -f http://localhost:3001/ || echo "❌ Frontend not ready"

# Navigate to test directory
cd gpt5-openai-agents-sdk-polygon-mcp/tests/playwright/
```

#### CLI Execution Pattern
```bash
# Execute tests sequentially (single browser session)
npx playwright test test-b001-market-status.spec.ts
npx playwright test test-b002-nvda.spec.ts
npx playwright test test-b003-spy.spec.ts
# ... continue through B016 ...
npx playwright test test-b016-button-integration.spec.ts
```

### CLI Testing Checklist

#### Pre-Test Validation
- [ ] FastAPI server running on port 8000 with "Application startup complete"
- [ ] Vite server running on port 3000+ with "VITE ready"
- [ ] Backend health check returning 200 OK
- [ ] Frontend loading properly in browser
- [ ] Test directory accessible with all .spec.ts files present

#### Test Execution (B001-B006: Market/Ticker Tests)
- [ ] **B001**: `npx playwright test test-b001-market-status.spec.ts` (Target: <45s)
- [ ] **B002**: `npx playwright test test-b002-nvda.spec.ts` (Target: <45s)
- [ ] **B003**: `npx playwright test test-b003-spy.spec.ts` (Target: <45s)
- [ ] **B004**: `npx playwright test test-b004-gme.spec.ts` (Target: <45s)
- [ ] **B005**: `npx playwright test test-b005-multi-ticker.spec.ts` (Target: <60s)
- [ ] **B006**: `npx playwright test test-b006-empty-message.spec.ts` (Target: instant)

#### Test Execution (B007-B016: Button Tests)
- [ ] **B007**: `npx playwright test test-b007-stock-snapshot-button.spec.ts` (Target: <60s)
- [ ] **B008**: `npx playwright test test-b008-support-resistance-button.spec.ts` (Target: <60s)
- [ ] **B009**: `npx playwright test test-b009-technical-analysis-button.spec.ts` (Target: <60s)
- [ ] **B010**: `npx playwright test test-b010-multi-button-interaction.spec.ts` (Target: <90s)
- [ ] **B011**: `npx playwright test test-b011-button-state-validation.spec.ts` (Target: <60s)
- [ ] **B012**: `npx playwright test test-b012-button-error-handling.spec.ts` (Target: <60s)
- [ ] **B013**: `npx playwright test test-b013-button-performance-validation.spec.ts` (Target: <60s)
- [ ] **B014**: `npx playwright test test-b014-button-accessibility.spec.ts` (Target: <60s)
- [ ] **B015**: `npx playwright test test-b015-button-ui-consistency.spec.ts` (Target: <60s)
- [ ] **B016**: `npx playwright test test-b016-button-integration.spec.ts` (Target: <90s)

#### Post-Test Validation
- [ ] All tests completed successfully or with documented issues
- [ ] Single browser session maintained throughout execution
- [ ] Performance metrics recorded for each test
- [ ] Test results documented in report format

---

## MCP Browser Automation Methodology

### MCP Tool Integration

#### Available MCP Browser Tools
- `mcp__playwright__browser_navigate` - Navigate to URLs
- `mcp__playwright__browser_snapshot` - Capture page snapshots  
- `mcp__playwright__browser_type` - Type text into elements
- `mcp__playwright__browser_click` - Click buttons and elements
- `mcp__playwright__browser_wait_for` - Wait for elements or time
- `mcp__playwright__browser_network_requests` - Monitor network activity

#### MCP Execution Workflow
1. **Browser Session Start**: Single browser instance initialization
2. **Navigate**: `browser_navigate` to frontend URL (port detection)
3. **Test Execution**: Use appropriate MCP tools for each test
4. **Validation**: Verify responses and performance metrics
5. **Session End**: Complete testing in same browser instance

### MCP Testing Checklist

#### Pre-Test Setup
- [ ] FastAPI backend operational on port 8000
- [ ] Vite frontend operational with dynamic port detection
- [ ] MCP browser tools available and functional
- [ ] Frontend URL determined (http://localhost:3000+ with auto-adjustment)

#### MCP Test Execution (B001-B006: Market/Ticker Tests)

##### B001: Market Status Check
- [ ] `browser_navigate` to frontend URL
- [ ] `browser_snapshot` to capture initial state
- [ ] `browser_type` with text: "Market Status: PRIORITY FAST REQUEST..."
- [ ] `browser_press_key` Enter to submit
- [ ] `browser_wait_for` response with 🎯 KEY TAKEAWAYS (30s polling, 120s timeout)
- [ ] Validate market status data and emoji indicators

##### B002: NVDA Ticker Analysis
- [ ] `browser_type` with NVDA analysis query
- [ ] `browser_press_key` Enter to submit
- [ ] `browser_wait_for` response with 📈📉 sentiment indicators
- [ ] Validate comprehensive NVIDIA stock analysis

##### B003: SPY Ticker Analysis
- [ ] `browser_type` with SPY analysis query
- [ ] `browser_press_key` Enter to submit
- [ ] `browser_wait_for` response with proper structure
- [ ] Validate S&P 500 ETF analysis quality

##### B004: GME Ticker Analysis
- [ ] `browser_type` with GME analysis query
- [ ] `browser_press_key` Enter to submit
- [ ] `browser_wait_for` response with financial metrics
- [ ] Validate GameStop stock analysis completeness

##### B005: Multi-Ticker Analysis
- [ ] `browser_type` with multi-ticker comparison query
- [ ] `browser_press_key` Enter to submit
- [ ] `browser_wait_for` response with comparative analysis
- [ ] Validate complex multi-ticker processing

##### B006: Empty Message Handling
- [ ] `browser_type` with empty or invalid input
- [ ] `browser_press_key` Enter to submit
- [ ] Validate proper error handling and user feedback

#### MCP Test Execution (B007-B016: Button Tests)

##### B007: Stock Snapshot Button
- [ ] `browser_click` on Stock Snapshot button (📈)
- [ ] `browser_wait_for` button response processing
- [ ] Validate stock snapshot analysis from button template

##### B008: Support/Resistance Button
- [ ] `browser_click` on Support/Resistance button (📊)
- [ ] `browser_wait_for` technical analysis response
- [ ] Validate support/resistance level calculations

##### B009: Technical Analysis Button
- [ ] `browser_click` on Technical Analysis button (🔧)
- [ ] `browser_wait_for` comprehensive technical indicators
- [ ] Validate complete technical analysis delivery

##### B010: Multi-Button Interaction
- [ ] Sequential button clicks across all 3 button types
- [ ] Monitor state management during transitions
- [ ] Validate proper sequential interaction handling

##### B011: Button State Validation
- [ ] Monitor button states during API processing
- [ ] Validate loading indicators and UI feedback
- [ ] Confirm proper state transitions

##### B012: Button Error Handling
- [ ] Trigger error conditions via button interactions
- [ ] Validate graceful error recovery mechanisms
- [ ] Confirm proper error user feedback

##### B013: Button Performance Validation
- [ ] Performance testing across all button interactions
- [ ] Monitor response times and system behavior
- [ ] Validate consistent performance thresholds

##### B014: Button Accessibility
- [ ] Keyboard navigation testing for all buttons
- [ ] Screen reader compatibility validation
- [ ] Confirm full accessibility compliance

##### B015: Button UI Consistency
- [ ] UI consistency checks across all button states
- [ ] Visual feedback validation during interactions
- [ ] Confirm consistent behavior patterns

##### B016: Button Integration
- [ ] Complete integration testing across button system
- [ ] End-to-end workflow validation
- [ ] Confirm full system integration functionality

#### MCP Post-Test Actions
- [ ] `browser_network_requests` to review API calls
- [ ] `browser_snapshot` for final state capture
- [ ] Document all MCP tool interactions and responses
- [ ] Browser session properly maintained throughout testing

---

## Performance Standards and Validation

### Performance Classifications
- **SUCCESS**: <45 seconds response time
- **SLOW_PERFORMANCE**: 45-90 seconds response time (functional but requires optimization)
- **TIMEOUT**: >120 seconds (failure condition)

### Polling Methodology
- **Standard Polling**: 30-second intervals for response detection
- **Early Completion**: Tests complete when response criteria met
- **Maximum Timeout**: 120 seconds per individual test
- **Session Continuity**: Single browser instance maintained across all tests

### Success Criteria
- **Functionality**: All core features operational regardless of performance
- **Response Quality**: Proper emoji indicators and structured output
- **Error Handling**: Graceful failure modes and user feedback
- **Integration**: Complete end-to-end workflow validation

---

## Test Report Format

### Report Naming Convention
```
playwright_[METHOD]_test_[YY-MM-DD]_[HH-MM].md
```

**Examples:**
- `playwright_CLI_test_25-09-10_11-39.md`
- `playwright_MCP_test_25-09-10_16-35.md`

### Required Report Sections

#### Executive Summary
- Total tests executed and coverage percentage
- Overall success rate and performance classification
- Key achievements and system validation results
- Infrastructure status throughout testing

#### Detailed Test Results
- Individual test results for all B001-B016 tests
- Performance metrics and timing data
- Success/failure status with detailed notes
- Response quality assessment

#### Performance Analysis
- Average response times across test categories
- Performance classification distribution
- Infrastructure stability metrics
- Optimization recommendations

#### Technical Details
- Server configuration and port management
- Browser session management approach
- Error conditions encountered and resolutions
- Network requests and API integration status

#### Recommendations
- Performance optimization opportunities
- Configuration improvements needed
- Future testing considerations
- System scalability observations

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Server Startup Problems
- **Backend Issues**: Check API keys, uv installation, port conflicts
- **Frontend Issues**: Node.js version, npm dependencies, port availability
- **CORS Problems**: Verify cross-origin configuration between servers

#### Test Execution Issues
- **Browser Not Found**: Run `npx playwright install chromium`
- **Test Timeouts**: Increase timeout or check server performance
- **Network Errors**: Verify server health and connectivity

#### Performance Issues
- **Slow Responses**: Check MCP server timeout configuration
- **Memory Problems**: Monitor system resources during testing
- **Port Conflicts**: Allow automatic port adjustment or configure manually

### System Requirements
- **Node.js**: 18+ required for frontend
- **Python**: 3.10+ with uv package manager
- **Browser**: Chromium for Playwright automation
- **Memory**: 4GB+ recommended for complete test suite
- **Network**: Stable internet for Polygon.io API access

---

## Best Practices

### Testing Integrity
- Always execute complete B001-B016 suite for comprehensive validation
- Maintain single browser session throughout entire test sequence
- Document all test results including failures for transparency
- Never skip tests or claim completion without full execution

### Performance Optimization
- Start both servers before any test execution
- Monitor system resources during testing
- Use appropriate polling intervals for early completion detection
- Document performance baselines for future comparison

### Maintenance
- Regular review of test specifications for accuracy
- Update performance thresholds based on system improvements
- Maintain compatibility with browser and framework updates
- Keep test documentation synchronized with actual implementations

---

This master plan provides the definitive guide for Playwright testing execution in the Market Parser application, ensuring consistent, reliable, and comprehensive test coverage across both CLI and MCP methodologies.