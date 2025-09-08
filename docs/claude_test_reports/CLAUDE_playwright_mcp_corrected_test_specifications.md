# CLAUDE Playwright MCP Corrected Test Specifications

**Market Parser Complete Testing Framework - 51-Test Suite**

**Date**: 2025-01-15  
**Version**: 3.0.0  
**Purpose**: Complete redesign of Playwright MCP tests based on comprehensive error analysis  
**Target System**: Market Parser with React Frontend + FastAPI Backend

---

## Executive Summary

This document provides comprehensive test specifications for the Market Parser system, correcting critical errors identified in previous implementations. The specifications cover 51 tests designed to validate the button-click → JSON response architecture with proper schema validation.

### Critical Errors Corrected

**Previous Implementation Issues:**
- ❌ Used verbose AI analysis queries instead of simple raw JSON requests
- ❌ Expected emoji-formatted responses instead of raw JSON API data
- ❌ Only executed 3 tests instead of required 51-test suite
- ❌ Completely missed the button-click → JSON response architecture

**New Implementation Focus:**
- ✅ Simple "Raw Output Format Only with NO verbosity" requests
- ✅ Raw JSON responses matching defined schemas
- ✅ Complete 51-test suite across 9 categories
- ✅ Button-click → JSON response methodology with schema validation

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

**Data Flow**: User Input → Button Click → Backend Processing → JSON Schema Response

### JSON Response Schemas

**Snapshot Schema**:
```json
{
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "ticker_symbol": "AAPL",
    "confidence_score": 0.95,
    "schema_version": "1.0"
  },
  "snapshot_data": {
    "current_price": 150.25,
    "percentage_change": 2.5,
    "dollar_change": 3.75,
    "volume": 45000000,
    "vwap": 149.80,
    "open": 148.50,
    "high": 151.00,
    "low": 147.25,
    "close": 146.50
  }
}
```

**Support & Resistance Schema**:
```json
{
  "metadata": {...},
  "support_levels": {
    "S1": {"price": 145.50, "strength": "strong", "confidence": 0.9},
    "S2": {"price": 142.00, "strength": "moderate", "confidence": 0.8},
    "S3": {"price": 138.75, "strength": "weak", "confidence": 0.7}
  },
  "resistance_levels": {
    "R1": {"price": 155.25, "strength": "moderate", "confidence": 0.85},
    "R2": {"price": 158.50, "strength": "strong", "confidence": 0.9},
    "R3": {"price": 162.00, "strength": "weak", "confidence": 0.75}
  }
}
```

**Technical Analysis Schema**:
```json
{
  "metadata": {...},
  "oscillators": {
    "RSI": {"value": 65.2, "interpretation": "neutral", "period": 14},
    "MACD": {"value": 2.1, "signal": 1.8, "histogram": 0.3, "interpretation": "bullish"}
  },
  "moving_averages": {
    "exponential": {"EMA_5": 151.2, "EMA_10": 149.8, "EMA_20": 148.5},
    "simple": {"SMA_5": 150.9, "SMA_10": 149.5, "SMA_20": 148.2}
  }
}
```

---

## Complete 51-Test Suite Specification

### Priority Tests (5 Tests)

#### TEST-P001: Market Status Raw JSON
**Purpose**: Verify system can return raw market status data
**Input Method**: Chat message
**Query**: "Raw Output Format Only with NO verbosity"
**Expected Response**: JSON with market status fields
**Schema Validation**: 
```json
{
  "afterHours": boolean,
  "currencies": {...},
  "exchanges": {...},
  "indicesGroups": {...},
  "market": "string",
  "serverTime": "2025-01-15T10:30:00.000Z"
}
```
**Timeout**: 120 seconds
**MCP Tools**: `mcp__playwright__browser_navigate`, `mcp__playwright__browser_type`, `mcp__playwright__browser_click`

#### TEST-P002: Single Ticker NVDA Raw JSON
**Purpose**: Test individual ticker snapshot request
**Input Method**: Button click (📈 Stock Snapshot)
**Pre-Input**: Type "NVDA" in chat input
**Query Generated**: "Raw Output Format Only with NO verbosity"
**Expected Response**: Snapshot schema JSON for NVDA
**Schema Validation**: Full snapshot schema with NVDA ticker_symbol
**Timeout**: 120 seconds

#### TEST-P003: Single Ticker SPY Raw JSON
**Purpose**: Test individual ticker snapshot request
**Input Method**: Button click (📈 Stock Snapshot)  
**Pre-Input**: Type "SPY" in chat input
**Query Generated**: "Raw Output Format Only with NO verbosity"
**Expected Response**: Snapshot schema JSON for SPY
**Schema Validation**: Full snapshot schema with SPY ticker_symbol
**Timeout**: 120 seconds

#### TEST-P004: Single Ticker GME Raw JSON
**Purpose**: Test individual ticker snapshot request
**Input Method**: Button click (📈 Stock Snapshot)
**Pre-Input**: Type "GME" in chat input  
**Query Generated**: "Raw Output Format Only with NO verbosity"
**Expected Response**: Snapshot schema JSON for GME
**Schema Validation**: Full snapshot schema with GME ticker_symbol
**Timeout**: 120 seconds

#### TEST-P005: Multi-Ticker Combined Raw JSON
**Purpose**: Test multiple ticker combined request
**Input Method**: Button click (📈 Stock Snapshot)
**Pre-Input**: Type "NVDA, SPY, QQQ, IWM" in chat input
**Query Generated**: "Raw Output Format Only with NO verbosity"  
**Expected Response**: JSON array with multiple ticker snapshots
**Schema Validation**: Array of snapshot schemas for all 4 tickers
**Timeout**: 120 seconds

### Template Button Interactions (8 Tests)

#### TEST-T001: Snapshot Button Response Time
**Purpose**: Measure response time for snapshot button
**Method**: Click 📈 Stock Snapshot button with "AAPL" pre-input
**Expected**: JSON response within 120 seconds
**Validation**: Response contains valid snapshot schema
**Performance**: Log response time for baseline

#### TEST-T002: Support & Resistance Button Response Time
**Purpose**: Measure response time for S&R button
**Method**: Click 🎯 Support & Resistance button with "TSLA" pre-input
**Expected**: JSON response within 120 seconds
**Validation**: Response contains valid support_resistance schema
**Performance**: Log response time for baseline

#### TEST-T003: Technical Analysis Button Response Time
**Purpose**: Measure response time for technical button
**Method**: Click 🔧 Technical Analysis button with "MSFT" pre-input
**Expected**: JSON response within 120 seconds
**Validation**: Response contains valid technical schema
**Performance**: Log response time for baseline

#### TEST-T004: Button State During Processing
**Purpose**: Verify buttons show processing state
**Method**: Click any analysis button and immediately check state
**Expected**: Button shows loading/disabled state during processing
**Validation**: UI state changes appropriately

#### TEST-T005: Multiple Button Clicks Sequential
**Purpose**: Test sequential button clicks
**Method**: Click Snapshot → wait for response → click S&R → wait for response
**Expected**: Each button produces independent valid responses
**Validation**: Both responses match respective schemas

#### TEST-T006: Button Click Without Input
**Purpose**: Test button behavior with empty input
**Method**: Clear input field, click 📈 Stock Snapshot
**Expected**: Appropriate error handling or default behavior
**Validation**: System handles gracefully without crashing

#### TEST-T007: Button Click with Invalid Ticker
**Purpose**: Test button with invalid ticker symbol
**Method**: Input "INVALID123", click 📈 Stock Snapshot
**Expected**: Error response or appropriate handling
**Validation**: System provides meaningful error feedback

#### TEST-T008: Button Visual Feedback
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

### JSON Schema Validation Approach

**Validation Pipeline**:
```javascript
// 1. Extract JSON from UI element
const jsonText = await page.locator('[data-testid="snapshot-json"]').textContent();

// 2. Parse JSON
const responseData = JSON.parse(jsonText);

// 3. Validate against schema
const isValid = validateSchema(responseData, 'snapshot');

// 4. Assert specific fields
assert(responseData.metadata.ticker_symbol === expectedTicker);
assert(typeof responseData.snapshot_data.current_price === 'number');
```

**Schema Validation Functions**:
- `validateSnapshotSchema(data)`: Validates snapshot response structure
- `validateSupportResistanceSchema(data)`: Validates S&R response structure  
- `validateTechnicalSchema(data)`: Validates technical analysis response structure
- `validateMetadata(metadata)`: Validates common metadata fields

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

**Timeout Configuration**:
- **Page Load**: 30 seconds
- **Button Clicks**: 5 seconds  
- **API Response**: 120 seconds maximum
- **JSON Validation**: 5 seconds

**Timeout Handling Strategy**:
```javascript
// Configure timeout per operation type
const timeouts = {
    navigation: 30000,
    click: 5000,
    apiResponse: 120000,
    validation: 5000
};

// Use appropriate timeout for each operation
await browserClick('button', { timeout: timeouts.click });
await browserWaitFor({ text: 'response', timeout: timeouts.apiResponse });
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

**Execution Order**:
1. **Setup Phase**: Verify backend running, frontend accessible
2. **Priority Tests**: 5 tests validating core functionality  
3. **Functional Tests**: 43 tests covering all features
4. **Performance Tests**: 4 tests measuring system performance
5. **Cleanup Phase**: Generate reports, cleanup resources

### Reporting and Documentation

**Test Report Format**:
```markdown
# Playwright MCP Test Execution Report
**Date**: 2025-01-15
**Duration**: 45 minutes
**Total Tests**: 51
**Passed**: 49
**Failed**: 2
**Skipped**: 0

## Priority Tests Results
- TEST-P001: Market Status Raw JSON ✅ PASS (12.3s)
- TEST-P002: Single Ticker NVDA Raw JSON ✅ PASS (8.7s)
- TEST-P003: Single Ticker SPY Raw JSON ❌ FAIL (timeout after 120s)
...

## Performance Metrics
- Average Response Time: 23.4 seconds
- Memory Usage: Stable (±50MB)
- Error Rate: 3.9%
```

**Failure Analysis Template**:
```markdown
## Failed Test Analysis
**Test**: TEST-P003 Single Ticker SPY Raw JSON
**Error**: Timeout after 120 seconds
**Investigation**:
- Backend logs show SPY data request succeeded
- Frontend timeout occurred during response processing
- JSON response was valid but took 127 seconds
**Recommendation**: Increase timeout to 150 seconds for SPY ticker
```

---

## Success Criteria and Validation

### Test Suite Success Metrics

**Priority Tests**: 100% pass rate required
- All 5 priority tests must pass for system validation
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

**Schema Validation Requirements**:
- 100% of successful responses must pass schema validation
- All required fields must be present and correctly typed
- Data values must be within expected ranges
- Timestamps must be in correct ISO format

**Data Quality Validation**:
- Ticker symbols must match requested symbols
- Numeric values must be reasonable (no negative prices, etc.)
- Confidence scores must be between 0.0 and 1.0
- Timestamps must be recent (within last 24 hours)

---

## Conclusion

This comprehensive test specification provides a complete framework for validating the Market Parser system using Playwright MCP tools. The specification directly addresses the critical errors identified in previous implementations:

✅ **Simple Raw JSON Requests**: All tests use "Raw Output Format Only with NO verbosity"  
✅ **Raw JSON Response Validation**: Expect and validate raw JSON matching defined schemas  
✅ **Complete 51-Test Suite**: Full coverage across all functional areas  
✅ **Button-Click Architecture**: Tests focus on UI button interactions producing JSON responses  

The framework ensures reliable, comprehensive testing that validates both functional correctness and system performance while establishing clear baselines for future development.

**Next Steps**: 
1. Implement test execution framework using specified MCP tools
2. Execute priority tests to validate core functionality
3. Run comprehensive test suite and generate detailed reports
4. Use results to establish performance baselines and identify optimization opportunities