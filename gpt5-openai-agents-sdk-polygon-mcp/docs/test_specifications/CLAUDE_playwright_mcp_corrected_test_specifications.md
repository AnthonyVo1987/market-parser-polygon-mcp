# CLAUDE Playwright MCP Corrected Test Specifications

**Market Parser Complete Testing Framework - 51-Test Suite**

**Date**: 2025-01-15  
**Version**: 3.0.0  
**Purpose**: Complete redesign of Playwright MCP tests based on comprehensive error analysis  
**Target System**: Market Parser with React Frontend + FastAPI Backend

---

## Executive Summary

This document provides comprehensive test specifications for the Market Parser system, correcting critical errors identified in previous implementations. The specifications cover 51 tests designed to validate the button-click → response architecture with basic functionality testing, allowing emojis and any response format.

### Critical Errors Corrected

**Previous Implementation Issues:**
- ❌ Used verbose AI analysis queries instead of simple priority requests
- ❌ Incorrectly enforced JSON-only responses when user wants emojis allowed
- ❌ Only executed 3 tests instead of required 51-test suite
- ❌ Missed the button-click → response architecture

**New Implementation Focus:**
- ✅ Simple "PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity" requests
- ✅ Any response format acceptable including emojis and conversational responses
- ✅ Complete 51-test suite across 9 categories
- ✅ Button-click → response methodology with basic functionality validation
- ✅ Emojis are ALLOWED and encouraged in all responses

---

## System Architecture Overview

### Target Application Stack

**Frontend**: React at `http://localhost:3000/`
- Three analysis buttons: 📈 Stock Snapshot, 🎯 Support & Resistance, 🔧 Technical Analysis
- JSON display textboxes for each analysis type
- Chat interface with message input

**Backend**: FastAPI at `http://localhost:8000/`
- REST API providing structured JSON responses
- Integration with Polygon.io MCP server
- OpenAI GPT-5-mini processing

**Data Flow**: User Input → Button Click → Backend Processing → Any Format Response (JSON, text, emojis, conversational)

## Testing Methodology Standards

### Polling-Based Timeout Detection
- **30-second polling cycles** for completion detection  
- **120-second individual timeout** per test (not cumulative)
- **Performance classification**: SUCCESS (<45s), SLOW_PERFORMANCE (45-120s), TIMEOUT (>120s)
- **Accurate timestamp recording** for all test phases
- **Early completion detection** to prevent false positive timeouts

### Test Execution Protocol
1. **Start Test**: Record start timestamp
2. **Polling Loop**: Check for completion every 30 seconds
3. **Early Detection**: Stop polling when response received
4. **Performance Classification**: Categorize based on actual completion time
5. **Timeout Enforcement**: Hard timeout at 120 seconds if no response
6. **Result Recording**: Log actual completion time and classification
7. **Coverage-First Execution**: Continue running ALL requested tests regardless of individual failures

### Coverage-First Testing Principle

**COVERAGE IS MORE IMPORTANT THAN PASSING TESTS**

- **Never stop on first failure** - Record the failure and continue with remaining tests
- **Complete all requested tests** - Run every test in the requested suite, even if early tests fail
- **Comprehensive reporting** - Better to report "10/10 tests executed, 0/10 passed" than "3/10 tests executed, stopped early"
- **Maximize data collection** - Each test provides valuable performance and functionality data regardless of pass/fail status
- **Prevent wasted time** - Avoid having to restart entire test suites due to early termination
- **Full system validation** - Only by running all tests can we identify patterns, bottlenecks, and system-wide issues

**Example Reporting:**
```
Test Execution Summary:
✅ P001 Market Status: SUCCESS (32s)
❌ P002 NVDA Ticker: TIMEOUT (>120s)
✅ P003 SPY Ticker: SUCCESS (41s)

Result: 3/3 tests executed, 2/3 passed (66% success rate)
Total Coverage: 100% - All requested tests completed
```

**Anti-Pattern to Avoid:**
```
Test Execution Summary:
✅ P001 Market Status: SUCCESS (32s)
❌ P002 NVDA Ticker: TIMEOUT (>120s)
⏹️ P003 SPY Ticker: SKIPPED (stopped after P002 failure)

Result: 2/3 tests executed, 1/2 passed (50% success rate)
Total Coverage: 66% - Incomplete due to early termination
```

### Response Format Guidelines

**Response Format**: Any format acceptable including:
- JSON responses for structured data
- Text responses with emojis for enhanced readability
- Conversational responses with financial indicators
- Mixed format responses combining text, emojis, and data

**Emoji Usage**: Emojis are ENCOURAGED and should be used for:
- Financial sentiment indicators (📈 📉 💰 💸)
- Visual enhancement of responses
- Improved user experience and readability

**Basic Functionality Focus**: Tests validate that system responds appropriately to user requests, regardless of format.

---

## Complete 51-Test Suite Specification

### Priority Tests (3 Tests)

#### TEST-P001: Market Status Request
**Purpose**: Verify system responds to market status requests
**Input Method**: Chat message
**Query**: "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
**Expected Response**: Any format response with market status information (JSON, text with emojis, or conversational)
**Success Criteria**: System provides market status information in any readable format
**Timeout**: 120 seconds (30s polling intervals)
**Failure Handling**: Record failure details but continue to next test
**MCP Tools**: `mcp__playwright__browser_navigate`, `mcp__playwright__browser_type`, `mcp__playwright__browser_click`

#### TEST-P002: Single Ticker NVDA Request
**Purpose**: Test individual ticker snapshot request
**Input Method**: Button click (📈 Stock Snapshot)
**Pre-Input**: Type "NVDA" in chat input
**Query Generated**: "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
**Expected Response**: Any format response with NVDA stock information (JSON, emojis like 📈📉💰, or conversational)
**Success Criteria**: System provides NVDA stock information in readable format
**Timeout**: 120 seconds (30s polling intervals)

#### TEST-P003: Single Ticker SPY Request
**Purpose**: Test individual ETF ticker snapshot request
**Input Method**: Button click (📈 Stock Snapshot)  
**Pre-Input**: Type "SPY" in chat input
**Query Generated**: "Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
**Expected Response**: Any format response with SPY ETF information (JSON, emojis like 📈📉💰, or conversational)
**Success Criteria**: System provides SPY ETF information in readable format
**Timeout**: 120 seconds (30s polling intervals)

### Performance Validation Tests

#### TEST-P004: Single Ticker GME Request
**Purpose**: Test individual ticker snapshot request (performance validation)
**Input Method**: Button click (📈 Stock Snapshot)
**Pre-Input**: Type "GME" in chat input  
**Query Generated**: "Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
**Expected Response**: Any format response with GME stock information (JSON, emojis like 📈📉💰, or conversational)
**Success Criteria**: System provides GME stock information in readable format
**Timeout**: 120 seconds (30s polling intervals)
**Note**: Performance monitoring test - may exhibit slower response times, use polling to distinguish between slow performance vs timeout

### Complex Query Tests

#### TEST-P005: Multi-Ticker Combined Request
**Purpose**: Test multiple ticker combined request
**Input Method**: Button click (📈 Stock Snapshot)
**Pre-Input**: Type "NVDA, SPY, QQQ, IWM" in chat input
**Query Generated**: "Full Market Snapshot with multiple Tickers: NVDA, SPY, QQQ, IWM: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"  
**Expected Response**: Any format response with multiple ticker information (JSON array, text with emojis, or conversational summary)
**Success Criteria**: System provides information for multiple tickers in readable format
**Timeout**: 120 seconds (30s polling intervals)

### Button Template Tests

#### TEST-P006: Snapshot Button Response Time
**Purpose**: Measure response time for snapshot button
**Method**: Click 📈 Stock Snapshot button with "AAPL" pre-input
**Expected**: Any format response within 120 seconds (JSON, emojis, conversational)
**Validation**: Response contains AAPL stock information in readable format
**Performance**: Log response time for baseline

#### TEST-P007: Support & Resistance Button Response Time
**Purpose**: Measure response time for S&R button
**Method**: Click 🎯 Support & Resistance button with "TSLA" pre-input
**Expected**: Any format response within 120 seconds (JSON, emojis, conversational)
**Validation**: Response contains TSLA support/resistance information in readable format
**Performance**: Log response time for baseline

#### TEST-P008: Technical Analysis Button Response Time
**Purpose**: Measure response time for technical button
**Method**: Click 🔧 Technical Analysis button with "MSFT" pre-input
**Expected**: Any format response within 120 seconds (JSON, emojis, conversational)
**Validation**: Response contains MSFT technical analysis information in readable format
**Performance**: Log response time for baseline

#### TEST-P009: Button State During Processing
**Purpose**: Verify buttons show processing state
**Method**: Click any analysis button and immediately check state
**Expected**: Button shows loading/disabled state during processing
**Validation**: UI state changes appropriately

#### TEST-P010: Multiple Button Clicks Sequential
**Purpose**: Test sequential button clicks
**Method**: Click Snapshot → wait for response → click S&R → wait for response
**Expected**: Each button produces independent responses in any format
**Validation**: Both responses contain relevant financial information

#### TEST-P011: Button Click Without Input
**Purpose**: Test button behavior with empty input
**Method**: Clear input field, click 📈 Stock Snapshot
**Expected**: Appropriate error handling or default behavior
**Validation**: System handles gracefully without crashing

#### TEST-P012: Button Click with Invalid Ticker
**Purpose**: Test button with invalid ticker symbol
**Method**: Input "INVALID123", click 📈 Stock Snapshot
**Expected**: Error response or appropriate handling
**Validation**: System provides meaningful error feedback

#### TEST-P013: Button Visual Feedback
**Purpose**: Verify buttons provide visual feedback
**Method**: Click each button and observe visual changes
**Expected**: Buttons show hover, active, and processing states
**Validation**: All visual states function correctly



### Message Input Variations (6 Tests)

#### TEST-M001: Natural Language Query Processing
**Purpose**: Test natural language input processing
**Method**: Type "What's the current price of Apple stock?" and send
**Expected**: System processes and provides relevant response
**Validation**: Response relates to AAPL stock data

#### TEST-M002: Multiple Ticker Input Parsing
**Purpose**: Test parsing of multiple ticker symbols
**Method**: Input "AAPL MSFT GOOGL" and click analysis button
**Expected**: System recognizes all three tickers
**Validation**: Response includes data for all requested tickers

#### TEST-M003: Mixed Case Ticker Input
**Purpose**: Test ticker symbol case sensitivity
**Method**: Input "aapl" (lowercase) and click analysis button
**Expected**: System normalizes to uppercase and processes
**Validation**: Response shows "AAPL" in ticker_symbol field

#### TEST-M004: Special Characters in Input
**Purpose**: Test input sanitization
**Method**: Input "AAPL; DROP TABLE;" and click analysis button
**Expected**: System sanitizes input safely
**Validation**: No system errors, appropriate error handling

#### TEST-M005: Empty Message Handling
**Purpose**: Test behavior with empty input
**Method**: Send empty message via Send button
**Expected**: System handles gracefully
**Validation**: No crashes, appropriate user feedback

#### TEST-M006: Long Message Input
**Purpose**: Test very long message handling
**Method**: Input 500+ character message about stocks
**Expected**: System processes or truncates appropriately
**Validation**: System remains stable and responsive

### Export Functionality (5 Tests)

#### TEST-E001: JSON Copy to Clipboard
**Purpose**: Test JSON export via copy functionality
**Method**: Generate JSON response, click copy button
**Expected**: JSON copied to clipboard successfully
**Validation**: Clipboard contains valid JSON

#### TEST-E002: JSON Format Validation
**Purpose**: Verify exported JSON is properly formatted
**Method**: Export JSON and validate syntax
**Expected**: JSON passes syntax validation
**Validation**: JSON.parse() succeeds without errors

#### TEST-E003: Multiple Analysis Export
**Purpose**: Test exporting data from all three analysis types
**Method**: Generate responses from all buttons, export each
**Expected**: All exports contain valid respective schemas
**Validation**: Each export matches its analysis type schema

#### TEST-E004: Large Response Export
**Purpose**: Test exporting large JSON responses
**Method**: Generate multi-ticker response, export JSON
**Expected**: Full response exported without truncation
**Validation**: Exported data matches displayed data

#### TEST-E005: Export Error Handling
**Purpose**: Test export functionality with malformed responses
**Method**: Trigger export when response contains errors
**Expected**: Export handles errors gracefully
**Validation**: Export either works or provides clear error message

### Responsive Design (4 Tests)

#### TEST-R001: Mobile Viewport Testing
**Purpose**: Test interface on mobile screen size
**Method**: Resize viewport to 375x667 (iPhone SE)
**Expected**: Interface adapts to mobile layout
**Validation**: All buttons and elements remain accessible

#### TEST-R002: Desktop Viewport Testing
**Purpose**: Test interface on desktop screen size
**Method**: Resize viewport to 1920x1080
**Expected**: Interface utilizes desktop space effectively
**Validation**: Layout optimized for larger screen

#### TEST-R003: Tablet Viewport Testing
**Purpose**: Test interface on tablet screen size
**Method**: Resize viewport to 768x1024 (iPad)
**Expected**: Interface adapts to tablet layout
**Validation**: Touch-friendly elements and appropriate spacing

#### TEST-R004: Dynamic Resize Testing
**Purpose**: Test interface during dynamic resizing
**Method**: Gradually resize viewport during active session
**Expected**: Interface adapts smoothly without breaking
**Validation**: No layout breaks or element overlaps

### Backend API Integration (7 Tests)

#### TEST-A001: FastAPI Health Check
**Purpose**: Verify backend API is accessible
**Method**: Direct request to backend health endpoint
**Expected**: 200 OK response from FastAPI server
**Validation**: Server responds within expected timeframe

#### TEST-A002: JSON Schema Compliance
**Purpose**: Test all responses comply with defined schemas
**Method**: Generate responses from all analysis types
**Expected**: All responses pass schema validation
**Validation**: JSONSchema validation passes for each response

#### TEST-A003: API Response Headers
**Purpose**: Verify correct HTTP headers in responses
**Method**: Monitor network requests during button clicks
**Expected**: Appropriate Content-Type and CORS headers
**Validation**: Headers meet API specification requirements

#### TEST-A004: Rate Limiting Behavior
**Purpose**: Test API rate limiting if implemented
**Method**: Make rapid sequential requests
**Expected**: System handles rate limiting gracefully
**Validation**: Either processes all requests or provides appropriate rate limit feedback

#### TEST-A005: Request Payload Validation
**Purpose**: Test API validates request payloads
**Method**: Send malformed requests to API
**Expected**: API rejects invalid requests appropriately
**Validation**: Error responses are properly formatted

#### TEST-A006: Timeout Handling
**Purpose**: Test API timeout behavior
**Method**: Trigger requests that may timeout
**Expected**: API handles timeouts gracefully
**Validation**: Timeout responses are user-friendly

#### TEST-A007: Error Response Formatting
**Purpose**: Verify error responses follow standard format
**Method**: Trigger various error conditions
**Expected**: All errors follow consistent schema
**Validation**: Error responses include proper error codes and messages

### Error Handling (6 Tests)

#### TEST-H001: Network Error Recovery
**Purpose**: Test behavior when backend is unavailable
**Method**: Stop backend server, attempt button clicks
**Expected**: Frontend handles network errors gracefully
**Validation**: Clear error messages, no UI crashes

#### TEST-H002: Invalid JSON Response Handling
**Purpose**: Test handling of malformed JSON responses
**Method**: Mock backend to return invalid JSON
**Expected**: Frontend handles parsing errors appropriately
**Validation**: Error displayed to user, system remains stable

#### TEST-H003: API Error Response Handling
**Purpose**: Test handling of API error responses
**Method**: Trigger API errors (invalid ticker, etc.)
**Expected**: Frontend displays API error messages clearly
**Validation**: Error messages are user-friendly and actionable

#### TEST-H004: Timeout Error Handling
**Purpose**: Test behavior when requests timeout
**Method**: Mock slow API responses exceeding timeout
**Expected**: Frontend handles timeouts gracefully
**Validation**: Timeout message displayed, option to retry

#### TEST-H005: Concurrent Request Error Handling
**Purpose**: Test handling of multiple simultaneous requests
**Method**: Click multiple buttons rapidly
**Expected**: System handles concurrent requests appropriately
**Validation**: No race conditions or UI inconsistencies

#### TEST-H006: Browser Error Recovery
**Purpose**: Test recovery from browser-level errors
**Method**: Trigger browser errors (memory issues, etc.)
**Expected**: System recovers or fails gracefully
**Validation**: No data loss, clear error communication

### Performance Validation (4 Tests)

#### TEST-F001: Response Time Benchmarking
**Purpose**: Establish baseline response times
**Method**: Measure response times for all analysis types
**Expected**: All responses within acceptable time limits
**Validation**: Response times logged for performance tracking

#### TEST-F002: Memory Usage Monitoring
**Purpose**: Monitor browser memory usage during testing
**Method**: Run extended test session while monitoring memory
**Expected**: No significant memory leaks
**Validation**: Memory usage remains stable over time

#### TEST-F003: Large Dataset Handling
**Purpose**: Test performance with large JSON responses
**Method**: Request multi-ticker analysis with many stocks
**Expected**: System handles large responses efficiently
**Validation**: No performance degradation with large datasets

#### TEST-F004: Concurrent User Simulation
**Purpose**: Test system under concurrent load
**Method**: Simulate multiple users accessing system
**Expected**: System maintains performance under load
**Validation**: Response times remain acceptable with multiple users

### Accessibility Testing (5 Tests)

#### TEST-C001: Keyboard Navigation
**Purpose**: Test full keyboard accessibility
**Method**: Navigate entire interface using only keyboard
**Expected**: All functionality accessible via keyboard
**Validation**: Tab order logical, all buttons reachable

#### TEST-C002: Screen Reader Compatibility
**Purpose**: Test compatibility with screen readers
**Method**: Use screen reader to navigate interface
**Expected**: All elements properly announced
**Validation**: ARIA labels correct, content accessible

#### TEST-C003: High Contrast Mode
**Purpose**: Test interface in high contrast mode
**Method**: Enable OS high contrast mode
**Expected**: Interface remains usable and readable
**Validation**: All text and buttons visible in high contrast

#### TEST-C004: Focus Management
**Purpose**: Test focus management during interactions
**Method**: Monitor focus behavior during button clicks
**Expected**: Focus managed appropriately throughout interactions
**Validation**: Focus never lost, logical focus progression

#### TEST-C005: Alternative Text Validation
**Purpose**: Verify all images have appropriate alt text
**Method**: Check all image elements for alt attributes
**Expected**: All images have descriptive alt text
**Validation**: Alt text accurately describes image content

### Cross-Browser Compatibility (3 Tests)

#### TEST-B001: Chrome Compatibility Testing
**Purpose**: Verify full functionality in Chrome
**Method**: Run complete test suite in Chrome browser
**Expected**: All functionality works correctly in Chrome
**Validation**: No Chrome-specific issues or quirks

#### TEST-B002: Firefox Compatibility Testing
**Purpose**: Verify full functionality in Firefox
**Method**: Run complete test suite in Firefox browser
**Expected**: All functionality works correctly in Firefox
**Validation**: No Firefox-specific issues or quirks

#### TEST-B003: Safari Compatibility Testing
**Purpose**: Verify full functionality in Safari/WebKit
**Method**: Run complete test suite in WebKit browser
**Expected**: All functionality works correctly in Safari/WebKit
**Validation**: No Safari-specific issues or quirks

---

## Test Architecture Design

### Button-Click → JSON Response Methodology

**Core Testing Pattern**:
1. **Navigate** to `http://localhost:3000/`
2. **Input** ticker symbol in chat input field
3. **Click** specific analysis button (📈/🎯/🔧)
4. **Wait** for response (max 120 seconds)
5. **Validate** JSON response against schema
6. **Extract** JSON from response textbox
7. **Assert** schema compliance and data validity

### Basic Response Validation Approach

**Validation Pipeline**:
```javascript
// 1. Extract response content from UI element
const responseText = await page.locator('[data-testid="response-content"]').textContent();

// 2. Validate basic functionality
const hasContent = responseText && responseText.trim().length > 0;

// 3. Check for relevant information
const hasTickerInfo = responseText.includes(expectedTicker);

// 4. Verify readable response (any format acceptable)
assert(hasContent, 'Response should contain readable content');
assert(hasTickerInfo, 'Response should contain ticker information');
```

**Basic Validation Functions**:
- `validateResponseExists(data)`: Validates response contains content
- `validateTickerPresent(data, ticker)`: Validates ticker information present
- `validateReadableFormat(data)`: Validates response is in readable format (JSON, text, emojis acceptable)
- `validateBasicFunctionality(data)`: Validates system responds appropriately to requests

### Test Data Management

**Ticker Symbol Test Set**:
- **Primary**: NVDA, SPY, GME (user-specified priority tickers)
- **Secondary**: AAPL, MSFT, TSLA, GOOGL (common test tickers)
- **Edge Cases**: Invalid symbols, special characters, empty strings

**Expected Response Times**:
- **Snapshot**: 5-30 seconds typical
- **Support & Resistance**: 10-45 seconds typical
- **Technical Analysis**: 15-60 seconds typical
- **Maximum Timeout**: 120 seconds for all tests

---

## Implementation Guidelines

### Required MCP Tools Usage

**Primary Playwright MCP Tools**:
- `mcp__playwright__browser_navigate`: Navigate to application URL
- `mcp__playwright__browser_snapshot`: Capture page state for debugging
- `mcp__playwright__browser_click`: Click buttons and interactive elements
- `mcp__playwright__browser_type`: Input text into form fields
- `mcp__playwright__browser_wait_for`: Wait for specific conditions
- `mcp__playwright__browser_evaluate`: Execute JavaScript for advanced validation

**Sequential Thinking Tool**:
- `mcp__sequential-thinking__sequentialthinking`: Use for complex test logic and validation sequences

**File System Tools**:
- `mcp__filesystem__write_file`: Save test reports and results
- `mcp__filesystem__read_text_file`: Load test configurations and expected data

### Playwright MCP Implementation Patterns

**Basic Test Structure**:
```javascript
// 1. Setup and Navigation
await browserNavigate('http://localhost:3000/');
await browserSnapshot(); // Capture initial state

// 2. Input Preparation
await browserType('chat-input', 'NVDA');

// 3. Action Execution
await browserClick('snapshot-button', { timeout: 5000 });

// 4. Response Waiting
await browserWaitFor({ text: 'metadata', timeout: 120000 });

// 5. Result Validation
const jsonResponse = await browserEvaluate('() => document.querySelector("#snapshot-json").textContent');
const parsedData = JSON.parse(jsonResponse);

// 6. Schema Assertion
assert(parsedData.metadata.ticker_symbol === 'NVDA');
assert(typeof parsedData.snapshot_data.current_price === 'number');
```

**Error Handling Pattern**:
```javascript
try {
    await browserClick('snapshot-button');
    await browserWaitFor({ text: 'error', timeout: 120000 });
    const errorText = await browserEvaluate('() => document.querySelector(".error-message").textContent');
    // Validate error message format and content
} catch (timeout) {
    // Handle timeout scenario - this is a test failure
    throw new Error(`Test failed: Response timeout after 120 seconds`);
}
```

**Multi-Browser Testing Pattern**:
```javascript
const browsers = ['chromium', 'firefox', 'webkit'];
for (const browserType of browsers) {
    await browserNavigate('http://localhost:3000/');
    // Run test suite for each browser
    // Validate consistent behavior across browsers
}
```

### Response Monitoring and Timeout Handling

**Polling-Based Timeout Configuration**:
- **Page Load**: 30 seconds
- **Button Clicks**: 5 seconds  
- **API Response**: 120 seconds maximum with 30s polling intervals
- **JSON Validation**: 5 seconds
- **Polling Interval**: 30 seconds for response detection

**30-Second Polling Strategy**:
```javascript
// Configure polling-based timeout handling
const pollingConfig = {
    navigation: 30000,
    click: 5000,
    apiResponse: 120000,
    pollingInterval: 30000,
    validation: 5000
};

// Implement 30-second polling for response detection
async function pollForResponse(selector, maxTimeout = 120000) {
    const startTime = Date.now();
    const pollingInterval = 30000; // 30 seconds
    
    while (Date.now() - startTime < maxTimeout) {
        try {
            const response = await page.locator(selector).textContent({ timeout: 5000 });
            if (response && response.trim().length > 0) {
                const elapsedTime = Date.now() - startTime;
                const classification = getPerformanceClassification(elapsedTime);
                return { response, elapsedTime, classification };
            }
        } catch (error) {
            // Continue polling if element not found yet
        }
        
        // Wait 30 seconds before next poll
        await new Promise(resolve => setTimeout(resolve, pollingInterval));
    }
    
    throw new Error(`Timeout: No response after ${maxTimeout}ms`);
}

// Performance classification function
function getPerformanceClassification(elapsedTime) {
    if (elapsedTime < 45000) return 'SUCCESS';
    if (elapsedTime < 120000) return 'SLOW_PERFORMANCE';
    return 'TIMEOUT';
}

// Use polling for API response detection
await browserClick('button', { timeout: pollingConfig.click });
const result = await pollForResponse('.response-content', pollingConfig.apiResponse);
```

### JSON Validation Methodology

**Schema Validation Implementation**:
```javascript
function validateSnapshotSchema(data) {
    // Required metadata fields
    assert(data.metadata, 'Missing metadata object');
    assert(data.metadata.timestamp, 'Missing timestamp');
    assert(data.metadata.ticker_symbol, 'Missing ticker_symbol');
    assert(data.metadata.schema_version === '1.0', 'Invalid schema_version');
    
    // Required snapshot_data fields
    assert(data.snapshot_data, 'Missing snapshot_data object');
    assert(typeof data.snapshot_data.current_price === 'number', 'Invalid current_price type');
    assert(typeof data.snapshot_data.volume === 'number', 'Invalid volume type');
    
    // Data range validation
    assert(data.snapshot_data.current_price > 0, 'Invalid current_price value');
    assert(data.snapshot_data.volume >= 0, 'Invalid volume value');
    
    return true;
}
```

**Field-Level Validation**:
```javascript
function validateFieldTypes(data, schema) {
    for (const [field, expectedType] of Object.entries(schema)) {
        const actualType = typeof data[field];
        assert(actualType === expectedType, 
               `Field ${field}: expected ${expectedType}, got ${actualType}`);
    }
}
```

### Error Scenarios and Handling

**Expected Error Conditions**:
1. **Invalid Ticker**: System should return error JSON with proper error code
2. **Network Timeout**: Frontend should display timeout message
3. **Server Error**: API errors should be properly formatted and displayed
4. **Malformed Response**: System should handle JSON parsing errors gracefully

**Error Validation Pattern**:
```javascript
// Test error response structure
if (response.error) {
    assert(response.error.code, 'Missing error code');
    assert(response.error.message, 'Missing error message');
    assert(response.error.timestamp, 'Missing error timestamp');
} else {
    // Validate success response
    validateSnapshotSchema(response);
}
```

---

## Test Execution Framework

### Test Runner Configuration

**Test Organization**:
- **Priority Tests**: Run first, must pass for continuation
- **Comprehensive Tests**: Run in parallel where possible
- **Browser Tests**: Run sequentially per browser type
- **Performance Tests**: Run separately with clean environment

**Execution Order with 30s Polling**:
1. **Setup Phase**: Verify backend running, frontend accessible
2. **Priority Tests**: 3 tests validating core functionality with 30s polling (~6 minutes)  
3. **Functional Tests**: 48 tests covering all features with polling-based timeout detection
4. **Performance Tests**: 4 tests measuring system performance using polling methodology
5. **Cleanup Phase**: Generate reports with performance classification, cleanup resources

**Polling Implementation Standards**:
- **Early Completion Detection**: Stop polling immediately when response received
- **Performance Classification**: Classify all test results as SUCCESS/SLOW_PERFORMANCE/TIMEOUT
- **Accurate Timing**: Record actual completion times, not polling intervals
- **False Positive Prevention**: Use polling to distinguish slow performance from timeouts

### Reporting and Documentation

**Test Report Format with Performance Classification**:
```markdown
# Playwright MCP Test Execution Report
**Date**: 2025-01-15
**Duration**: 45 minutes
**Total Tests**: 51
**Passed**: 49
**Failed**: 2
**Skipped**: 0

## Priority Tests Results (30s Polling Methodology)
- TEST-P001: Market Status ✅ SUCCESS (12.3s) - Completed on first poll
- TEST-P002: Single Ticker NVDA ✅ SUCCESS (8.7s) - Completed on first poll
- TEST-P003: Single Ticker SPY ⚠️ SLOW_PERFORMANCE (67.4s) - Completed on third poll
- TEST-P004: Single Ticker GME ⚠️ SLOW_PERFORMANCE (89.1s) - Completed on fourth poll
- TEST-P005: Multi-Ticker ❌ TIMEOUT (120s+) - No response after 4 polling cycles
...

## Performance Classification Summary
- SUCCESS (<45s): 35 tests (68.6%)
- SLOW_PERFORMANCE (45-120s): 14 tests (27.5%)
- TIMEOUT (>120s): 2 tests (3.9%)
- Average Response Time: 34.7 seconds
- Memory Usage: Stable (±50MB)
- Polling Efficiency: 47% first-poll completions
```

**Failure Analysis Template with Polling Data**:
```markdown
## Performance Analysis
**Test**: TEST-P003 Single Ticker SPY
**Classification**: SLOW_PERFORMANCE (67.4s)
**Polling Data**:
- Poll 1 (30s): No response
- Poll 2 (60s): No response  
- Poll 3 (67.4s): Response received
**Investigation**:
- Backend logs show SPY data request succeeded
- Response completed within timeout window
- Valid response received on third polling cycle
**Classification**: Correctly identified as SLOW_PERFORMANCE, not timeout
**Recommendation**: Monitor SPY performance trends, consider optimization if pattern persists

## Timeout Analysis
**Test**: TEST-P005 Multi-Ticker Request
**Classification**: TIMEOUT (>120s)
**Polling Data**:
- Poll 1 (30s): No response
- Poll 2 (60s): No response
- Poll 3 (90s): No response
- Poll 4 (120s): Hard timeout enforced
**Investigation**:
- No response received within 4 polling cycles
- True timeout condition confirmed
- Multiple ticker complexity may exceed processing capacity
**Recommendation**: Investigate multi-ticker processing bottleneck
```

---

## Success Criteria and Validation

### Test Suite Success Metrics

**Priority Tests**: 100% pass rate required
- All 3 priority tests must pass for system validation
- Any priority test failure indicates critical system issue

**Comprehensive Tests**: 90% pass rate target
- 43/48 comprehensive tests should pass
- Failed tests must be analyzed and documented
- Known limitations acceptable if documented

**Performance Tests**: Baseline establishment
- Tests establish performance baselines
- Failures indicate performance regression
- Results used for future optimization planning

### JSON Schema Compliance

**Basic Functionality Requirements**:
- 100% of successful responses must contain readable content
- Responses must relate to the requested ticker or market data
- Any format acceptable (JSON, text with emojis, conversational)
- Emojis encouraged for enhanced user experience

**Content Quality Validation**:
- Response must contain information relevant to the request
- Financial data should be reasonable (no obviously incorrect values)
- Emojis like 📈📉💰 encouraged for sentiment indicators
- Response format should be user-friendly and readable

---

## Conclusion

This comprehensive test specification provides a complete framework for validating the Market Parser system using Playwright MCP tools with advanced 30-second polling methodology. The specification directly addresses the critical errors identified in previous implementations:

✅ **Priority Fast Requests**: All tests use "PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"  
✅ **Any Format Response Validation**: Accept and validate any response format including JSON, emojis, and conversational responses  
✅ **Complete 51-Test Suite**: Full coverage across all functional areas  
✅ **Button-Click Architecture**: Tests focus on UI button interactions producing readable responses  
✅ **Emoji Encouragement**: Emojis are allowed and encouraged for enhanced user experience
✅ **30-Second Polling Methodology**: Prevents false positive timeouts through intelligent completion detection
✅ **Performance Classification**: SUCCESS/SLOW_PERFORMANCE/TIMEOUT categories for accurate analysis
✅ **Early Completion Detection**: Stops polling immediately when response received, eliminating false positives

The framework ensures reliable, comprehensive testing that validates basic functionality and user experience while providing accurate performance data through polling-based timeout detection.

**Key Polling Advantages**: 
- **Eliminates False Positives**: Distinguishes between slow performance and true timeouts
- **Accurate Performance Data**: Records actual completion times, not polling intervals
- **Early Detection**: Stops polling immediately upon response completion
- **Proper Classification**: Categorizes all responses for meaningful analysis

**Next Steps**: 
1. Implement 30-second polling test execution framework using specified MCP tools
2. Execute priority tests with polling methodology to validate core functionality
3. Run comprehensive test suite with performance classification
4. Generate detailed reports with polling data and performance insights
5. Use accurate performance data to establish baselines and identify optimization opportunities