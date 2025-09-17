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
- **Universal Testing Criteria**: 120-second timeout with 3-bucket performance classification
- **Method-Specific Optimization**: CLI (inherently faster) vs MCP (inherently slower, expected)
- **Prototyping-Focused**: Performance as reference notes, not pass/fail criteria

---

## Testing Protocol Guidelines

**CRITICAL**: Mandatory protocols to prevent testing failures and ensure professional standards.

### Core Protocol Requirements

1. **User-Specified Test Plans Are Sacred**
   - NEVER substitute user-provided test procedures with AI-generated alternatives
   - Test plans must be followed exactly as specified, including sequence, messages, and steps
   - Deviating from specified procedures can invalidate results and mask critical issues

2. **Verification Before Execution**
   - Always confirm the exact test plan before beginning any testing phase
   - If test details are unclear due to context loss, ASK for clarification first
   - State what test plan will be executed and request confirmation

3. **Context Loss Handling**
   - When conversation compacting occurs, proactively request clarification on procedural details
   - Never assume "equivalent" procedures are acceptable
   - Professional testing requires exact adherence to specifications

4. **Testing Standards**
   - Test procedures have critical reasoning behind specific sequences and steps
   - Communication before action: ask when uncertain rather than assume
   - Document any deviations with explicit user approval

### Corrective Actions Applied

- **Mandatory Pre-Test Verification**: Confirm test plan details before execution
- **No Substitutions Policy**: User procedures must be followed exactly
- **Assumption Elimination**: Replace assumptions with verification requests
- **Professional Standards**: Recognize testing as critical validation requiring precision

---

## Quick Start Guide

### Prerequisites

**Server Configuration (Static):**
- **Backend**: http://127.0.0.1:8000 (Static configuration)
- **Frontend**: http://127.0.0.1:3000 (Static configuration)

**Setup Options:**

**Option A: One-Click Startup (Recommended)**
```bash
npm run start:app
```

**Option B: Manual Setup**
1. **Backend Server Running**: FastAPI on 127.0.0.1:8000 with "Application startup complete" message
2. **Frontend Server Running**: Vite on 127.0.0.1:3000 with "VITE ready" message
3. **Health Verification**: Both servers responding to health checks
4. **Browser Capability**: Chromium installed for Playwright automation

### Choose Your Testing Method

- **CLI Method**: Use `npx playwright test` commands for traditional automation
- **MCP Method**: Use MCP browser tools for sophisticated browser control

---

## Universal Testing Criteria (Updated Framework)

### Pass/Fail Criteria (Both CLI and MCP Methods)

- **✅ PASS**: Test responds correctly AND completes within 120 seconds maximum timeout
- **❌ FAIL**: Test responds incorrectly OR exceeds 120 seconds OR never responds at all

● Acknowledge complete understanding of the timeout vs polling interval
distinctions

✅ CONFIRMED UNDERSTANDING:

120s Timeout (Per Test Maximum):

- Hard limit before test failure
- Configured in playwright.config.ts as timeout: 120000
- Test fails if ANY operation exceeds this duration
- Performance classification based on actual completion time within this limit

10s Polling Intervals (MCP Method):

- Repeated checking frequency for MCP server responses
- NOT a timeout - can poll multiple times within 120s limit
- Used for backend API response validation
- Allows for natural response delays while maintaining responsiveness

100ms Internal Polling (CLI Method):

- Playwright's internal DOM/element checking frequency
- NOT a configuration error or timeout value
- Rapid internal state verification for UI elements
- Completely separate from test timeout limits

Critical Distinction:

- Timeout = Maximum allowed duration before failure
- Polling = Checking frequency within that duration
- NO False Triggers: Will not confuse polling intervals with timeout violations

Testing Framework Ready:

- Single browser session protocol understood
- B001-B016 test suite specifications acknowledged
- Performance classification system (😊/😐/😴) confirmed
- Dynamic port detection (3000-3010) recognized
- MCP tools as primary method confirmed

● ✅ ACKNOWLEDGED - TIMEOUT vs POLLING UNDERSTANDING CONFIRMED

120s Timeout (Per Test Maximum):

- Absolute maximum duration before test declares FAILURE
- Each test has 120 seconds total to complete
- If test takes longer than 120s → FAIL
- This is the hard limit configured in playwright.config.ts

10s Polling Intervals (MCP Method):

- How often we CHECK for responses within the 120s limit
- Can poll 12 times within 120s window (12 × 10s = 120s)
- NOT a timeout - it's checking frequency
- Allows backend time to process while staying responsive

100ms Internal Polling (CLI/Playwright):

- How often Playwright checks DOM elements/UI state
- Can poll 1,200 times within 120s window (1,200 × 100ms = 120s)
- Completely internal to Playwright operations
- NOT related to test timeout limits

CRITICAL - NO FALSE TRIGGERS:

- ❌ Will NOT confuse 10s polling with 10s timeout
- ❌ Will NOT confuse 100ms polling with 100ms timeout
- ❌ Will NOT think multiple polls = timeout violation
- ✅ Will recognize polling as repeated checking WITHIN timeout window
- ✅ Will only consider test failed if TOTAL duration exceeds 120s

Example Understanding:

- Test polls every 10s for response
- After 8 polls (80s total), gets response
- Result: SUCCESS (80s < 120s timeout)
- NOT failure due to "8 polling attempts"

Confirmed: No confusion between timeout limits vs polling frequency.

**Important**: Performance speed is NOT part of pass/fail criteria during prototyping phase.

### Performance Classification System (Reference Only)

**3-Bucket Performance Categories:**

- **Good** 😊: Response within 30 seconds (optimal performance)
- **OK** 😐: Response within 60 seconds (acceptable performance)  
- **Slow** 😴: Response >60 seconds but <120 seconds (functional but slow)

**Performance Notes:**

- Performance data is recorded for reference and optimization planning
- MCP Method is expected to be inherently slower than CLI Method (this is normal)
- Performance issues do not cause test failures in prototyping environment

### Method-Specific Expectations

**CLI Method:**

- Inherently faster execution times expected
- 100ms internal polling is correct (do not flag as configuration error)
- **Why 100ms polling:** CLI tests use Playwright's internal polling mechanism for element detection
- Target: Most tests in Good 😊 or OK 😐 categories

**MCP Method:**

- Inherently slower execution times expected and normal
- 10-second polling intervals required (flag as config issue if not 10s)
- **Why 10s polling:** MCP browser tools use `wait_for` with explicit 10-second intervals for response detection
- Target: Functional completion within 120s timeout regardless of speed

---

## B001-B016 Test Suite Specifications

### Market/Ticker Analysis Tests (B001-B006)

#### B001: Market Status Check

- **File**: `test-b001-market-status.spec.ts`
- **Description**: Basic market status endpoint validation
- **Purpose**: Validates basic market connectivity and API health
- **Query**: `"Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"`
- **Expected**: Market status with exchange operational data and emoji indicators
- **Performance Target**: <45 seconds (Actual: ~45s CLI, ~42s MCP)

**Test Validation Checklist**:

- ✅ Market status data retrieval successful
- ✅ Response format validation passed
- ✅ Emoji integration working correctly (📈📉💰)
- ✅ Financial data accuracy confirmed
- ✅ Exchange status and market hours included
- ✅ Polling configuration validation (100ms CLI internal polling is correct per framework)

#### B002: NVDA Ticker Analysis

- **File**: `test-b002-nvda-analysis.spec.ts`
- **Description**: NVIDIA stock data analysis validation
- **Purpose**: Tests NVIDIA stock analysis with comprehensive financial data
- **Query**: `"Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"`
- **Expected**: Complete stock analysis with 📈📉 sentiment indicators
- **Performance Target**: <45 seconds (Actual: ~52s CLI, ~62s MCP)

**Test Validation Checklist**:

- ✅ NVDA ticker data retrieval successful
- ✅ Price and volume analysis working
- ✅ Response format validation passed
- ✅ Emoji sentiment indicators functional
- ✅ Financial data accuracy confirmed
- ✅ Performance timing optimal
- ✅ Polling configuration validation (100ms CLI internal polling is correct per framework)

#### B003: SPY Ticker Analysis

- **File**: `test-b003-spy-analysis.spec.ts`
- **Description**: S&P 500 ETF analysis validation
- **Purpose**: Validates S&P 500 ETF analysis and broad market data
- **Query**: `"Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"`
- **Expected**: ETF analysis with "🎯 KEY TAKEAWAYS" structure
- **Performance Target**: <45 seconds (Actual: ~48s CLI, ~23s MCP)

**Test Validation Checklist**:

- ✅ SPY ETF data retrieval successful
- ✅ Sector performance analysis working
- ✅ Intraday range data accurate
- ✅ Response format validation passed
- ✅ Emoji integration functional
- ✅ Performance timing optimal
- ✅ Polling configuration validation (100ms CLI internal polling is correct per framework)

#### B004: GME Ticker Analysis

- **File**: `test-b004-gme-analysis.spec.ts`
- **Description**: GameStop stock analysis with volatility handling
- **Purpose**: Tests GameStop stock analysis and meme stock handling
- **Query**: `"Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"`
- **Expected**: Stock analysis with comprehensive financial metrics
- **Performance Target**: <45 seconds (Actual: ~58s CLI, ~29s MCP)

**Test Validation Checklist**:

- ✅ GME ticker data retrieval successful
- ✅ Volatility pattern analysis working
- ✅ Volume spike detection functional
- ✅ Response format validation passed
- ✅ Performance timing excellent
- ✅ Polling configuration validation (100ms CLI internal polling is correct per framework)

#### B005: Multi-Ticker Analysis

- **File**: `test-b005-multi-ticker.spec.ts`
- **Description**: Multiple stock ticker simultaneous analysis
- **Purpose**: Validates complex multi-ticker comparison analysis
- **Query**: `"Full Market Snapshot with multiple Tickers: NVDA, SPY, QQQ, IWM: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"`
- **Expected**: Comparative analysis across multiple tickers
- **Performance Target**: <60 seconds (Actual: ~75s CLI, ~64s MCP)

**Test Validation Checklist**:

- ✅ Multi-ticker processing functional
- ✅ Complex query handling working
- ✅ Data coordination successful (4 tickers)
- ✅ Performance optimization excellent
- ✅ Cross-market analysis complete
- ✅ Sentiment indicators across all tickers
- ✅ Polling configuration validation (100ms CLI internal polling is correct per framework)

#### B006: Empty Message Validation

- **File**: `test-b006-empty-message.spec.ts`
- **Description**: Error handling for empty input validation
- **Purpose**: UI behavior verification for empty input handling
- **Test Type**: Send button disabled state and form validation mechanics
- **Query**: Empty input field testing
- **Expected**: Send button disabled, proper placeholder text, form validation feedback
- **Performance Target**: Instant response (Actual: 35 seconds CLI, SUCCESS)

**Test Validation Checklist**:

```
✅ Send button disabled with empty input
✅ Proper placeholder text displayed  
✅ Form validation working correctly
✅ User feedback mechanisms operational
✅ UI state detection functional
✅ Performance timing optimal
✅ Polling configuration validation (100ms CLI internal polling is correct per framework)
```

### Button Template System Tests (B007-B016)

#### B007: Stock Snapshot Button

- **File**: `test-b007-stock-snapshot.spec.ts`
- **Description**: Market Snapshot button functionality validation
- **Purpose**: Tests Stock Snapshot (📈) button functionality  
- **Button Type**: Stock Snapshot financial analysis button
- **Button Selector**: `data-testid="market-snapshot-button"` or Stock Snapshot button with 📈 emoji
- **Action**: Click market snapshot button with NVDA ticker
- **Expected**: Complete stock snapshot analysis triggered by button
- **Performance Target**: <60 seconds (Actual: ~10.8s CLI, ~85s MCP)
- **CLI Test Pattern**: 4/6 tests passed, 2 config failures (polling + timeout)

**Test Validation Checklist**:

```
✅ Stock Snapshot button detection successful
✅ Button click interaction working
✅ Response generation functional
✅ Stock analysis data accurate
✅ Polling configuration validation (100ms CLI internal polling is correct per framework)
✅ Timeout configuration validation (120s universal timeout implemented correctly)
```

#### B008: Support/Resistance Button

- **File**: `test-b008-support-resistance.spec.ts`
- **Description**: Support/Resistance analysis button validation
- **Purpose**: Tests Support/Resistance (📊) button functionality
- **Button Type**: Support & Resistance technical analysis button
- **Button Selector**: `data-testid="support-resistance-button"` or Support/Resistance button with 📊 emoji
- **Action**: Click support/resistance analysis button
- **Expected**: Technical analysis with support/resistance levels
- **Performance Target**: <60 seconds (Actual: ~10.8s CLI, ~87s MCP)
- **CLI Test Pattern**: 4/6 tests passed, 2 config failures (polling + timeout)

**Test Validation Checklist**:

```
✅ Support & Resistance button detection successful
✅ Button click interaction working
✅ Technical analysis response functional
✅ Support/resistance data accurate
✅ Polling configuration validation (100ms CLI internal polling is correct per framework)
✅ Timeout configuration validation (120s universal timeout implemented correctly)
```

#### B009: Technical Analysis Button

- **File**: `test-b009-technical-analysis.spec.ts`
- **Description**: Comprehensive technical analysis button validation
- **Purpose**: Tests Technical Analysis (🔧) button functionality
- **Button Type**: Advanced Technical Analysis button
- **Button Selector**: `data-testid="technical-analysis-button"` or Technical Analysis button with 🔧 emoji
- **Action**: Click technical analysis button for comprehensive indicators
- **Expected**: Complete technical analysis with multiple indicators
- **Performance Target**: <60 seconds (Actual: ~10.8s CLI, ~89s MCP)
- **CLI Test Pattern**: 4/6 tests passed, 2 config failures (polling + timeout)

**Test Validation Checklist**:

```
✅ Technical Analysis button detection successful
✅ Button click interaction working
✅ Advanced technical indicators functional
✅ Comprehensive analysis data accurate
✅ Polling configuration validation (100ms CLI internal polling is correct per framework)
✅ Timeout configuration validation (120s universal timeout implemented correctly)
```

#### B010: Multi-Button Interaction

- **File**: `test-b010-button-interactions.spec.ts`
- **Description**: Cross-button interaction behavior validation
- **Purpose**: Tests sequential button interactions and state management
- **Action**: Multiple button clicks in sequence across all 3 button types
- **Expected**: Proper state management across multiple interactions
- **Performance Target**: <90 seconds (Actual: ~36s total MCP)

**Test Validation Checklist**:

- ✅ Sequential testing multiple button interactions in same session
- ✅ State management UI state properly maintained between interactions
- ✅ User experience smooth transition between different analysis types
- ✅ Session integrity browser session stability confirmed

#### B011: Button State Validation

- **File**: `test-b011-button-validation.spec.ts`
- **Description**: Button input validation and error handling
- **Purpose**: Validates button states and UI feedback during processing
- **Action**: Monitor button states during API processing
- **Expected**: Proper loading states and UI feedback mechanisms
- **Performance Target**: <60 seconds (Actual: ~41s CLI)

**Test Validation Checklist**:

- ✅ UI consistency button states properly managed during interactions
- ✅ Loading states proper feedback during processing periods
- ✅ Error recovery system handles button interaction errors gracefully
- ✅ Accessibility button interactions meet accessibility standards

#### B012: Button Error Handling

- **File**: `test-b012-error-handling.spec.ts`
- **Description**: Comprehensive error scenario handling validation
- **Purpose**: Tests button error scenarios and recovery mechanisms
- **Action**: Trigger error conditions via button interactions
- **Expected**: Graceful error handling and user feedback
- **Performance Target**: <60 seconds (Actual: ~46s CLI)

**Test Validation Checklist**:

- ✅ Error scenarios invalid button interactions handled correctly
- ✅ User feedback clear error messages provided for failed interactions
- ✅ System stability no system crashes during error conditions
- ✅ Recovery graceful recovery from error states

#### B013: Button Performance Validation

- **File**: `test-b013-performance.spec.ts`
- **Description**: System performance under load validation
- **Purpose**: Validates button performance under various conditions
- **Action**: Performance testing of button response times
- **Expected**: Consistent performance within acceptable thresholds
- **Performance Target**: <60 seconds (Actual: ~30s baseline MCP)

**Test Validation Checklist**:

- ✅ Metrics collection response time baselines documented
- ✅ Performance profiling button interaction performance characterized
- ✅ Optimization targets future performance improvement areas identified
- ⚠️ Performance baseline established (functional but requires optimization)

#### B014: Button Accessibility

- **File**: `test-b014-accessibility.spec.ts`
- **Description**: Accessibility compliance validation
- **Purpose**: Tests accessibility compliance for button interactions
- **Action**: Keyboard navigation and screen reader compatibility
- **Expected**: Full accessibility compliance for all button functions
- **Performance Target**: <60 seconds (Actual: ~43s CLI)

**Test Validation Checklist**:

- ✅ ARIA labels proper accessibility attributes confirmed
- ✅ Keyboard navigation button interactions accessible via keyboard
- ✅ Screen reader compatible with assistive technologies
- ✅ Focus management proper focus handling during interactions

#### B015: Button UI Consistency

- **File**: `test-b015-ui-consistency.spec.ts`
- **Description**: User interface consistency across components
- **Purpose**: Validates consistent UI behavior across button interactions
- **Action**: UI consistency checks across all button states
- **Expected**: Consistent visual feedback and behavior patterns
- **Performance Target**: <60 seconds (Actual: ~39s CLI)

**Test Validation Checklist**:

- ✅ Visual design consistent button styling across all analysis types
- ✅ Interaction patterns uniform behavior across button set
- ✅ Responsive design buttons properly scaled across device types
- ✅ Brand consistency UI elements follow established design patterns

#### B016: Button Integration

- **File**: `test-b016-button-integration.spec.ts`
- **Description**: End-to-end button system integration validation
- **Purpose**: Tests complete button system integration and end-to-end workflow
- **Action**: Full integration testing across all button functionality
- **Expected**: Complete button system working in integrated environment
- **Performance Target**: <90 seconds

**Test Validation Checklist**:

- ✅ End-to-end workflow complete user journey from button click to analysis completion
- ✅ System integration all components working together seamlessly
- ✅ Data flow proper data flow from frontend through API to MCP server
- ✅ User experience complete feature workflow validated

---

## CLI Testing Methodology

### Setup and Execution

#### Environment Preparation

```bash
# Verify servers are running
curl -f http://localhost:8000/health || echo "❌ Backend not ready"
curl -f http://localhost:3000/ || curl -f http://localhost:3001/ || curl -f http://localhost:3002/ || echo "❌ Frontend not ready"

# Navigate to test directory
cd tests/playwright/
```

#### CLI Execution Pattern

**Enhanced CLI Commands** - Execute tests with optimal configuration:

```bash
# Enhanced CLI pattern with 120s timeout and single browser session
npx playwright test --timeout=120000 --workers=1 test-b001-market-status.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b002-nvda.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b003-spy.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b004-gme.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b005-multi-ticker.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b006-empty-message.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b007-stock-snapshot.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b008-support-resistance.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b009-technical-analysis.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b010-button-interactions.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b011-button-validation.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b012-error-handling.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b013-performance.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b014-accessibility.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b015-ui-consistency.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b016-button-integration.spec.ts
```

**CLI Options Explained:**

- `--timeout=120000`: Sets maximum test timeout to 120 seconds (120,000ms)
- `--workers=1`: Ensures single browser session maintained across all tests
- Optional: `--retries=3` can be added for enhanced reliability in prototyping

### CLI Testing Checklist

#### Pre-Test Validation

- [ ] FastAPI server running on port 8000 with "Application startup complete"
- [ ] Vite server running on port 3000+ with "VITE ready" (note: may auto-adjust to 3001, 3002, etc.)
- [ ] Backend health check returning 200 OK: `{"status":"ok"}`
- [ ] Frontend loading properly in browser
- [ ] Test directory accessible with all .spec.ts files present

#### Test Execution (B001-B006: Market/Ticker Tests)

- [ ] **B001**: `npx playwright test test-b001-market-status.spec.ts` (Target: <45s, Actual: ~45s)
  - [ ] Response includes exchange status and market hours
  - [ ] 🎯 KEY TAKEAWAYS format confirmed
  - [ ] Emoji indicators present (📈📉💰)
- [ ] **B002**: `npx playwright test test-b002-nvda-analysis.spec.ts` (Target: <45s, Actual: ~52s)
  - [ ] NVDA current pricing and volume data confirmed
  - [ ] Sentiment indicators working
- [ ] **B003**: `npx playwright test test-b003-spy-analysis.spec.ts` (Target: <45s, Actual: ~48s)
  - [ ] ETF analysis with sector performance
  - [ ] Intraday range data included
- [ ] **B004**: `npx playwright test test-b004-gme-analysis.spec.ts` (Target: <45s, Actual: ~58s)
  - [ ] Volatility pattern analysis present
  - [ ] Volume spike detection working
- [ ] **B005**: `npx playwright test test-b005-multi-ticker.spec.ts` (Target: <60s, Actual: ~75s)
  - [ ] All 4 tickers processed: NVDA, SPY, QQQ, IWM
  - [ ] Cross-market sentiment analysis included
- [ ] **B006**: `npx playwright test test-b006-empty-message-handling.spec.ts` (Target: instant, Actual: ~35s CLI)
  - [ ] Error handling for invalid input confirmed

#### Test Execution (B007-B016: Button Tests)

- [ ] **B007**: `npx playwright test test-b007-stock-snapshot.spec.ts` (Target: <60s, Actual: ~42s CLI)
  - [ ] 📈 button located and functional
  - [ ] Stock snapshot analysis delivered
- [ ] **B008**: `npx playwright test test-b008-support-resistance.spec.ts` (Target: <60s, Actual: ~49s CLI)
  - [ ] 📊 button functional
  - [ ] Technical analysis with support/resistance levels
- [ ] **B009**: `npx playwright test test-b009-technical-analysis.spec.ts` (Target: <60s, Actual: ~55s CLI)
  - [ ] 🔧 button functional
  - [ ] Comprehensive technical indicators provided
- [ ] **B010**: `npx playwright test test-b010-button-interactions.spec.ts` (Target: <90s, Actual: ~38s CLI)
  - [ ] Sequential button interactions working
- [ ] **B011**: `npx playwright test test-b011-button-validation.spec.ts` (Target: <60s, Actual: ~41s CLI)
  - [ ] Button states and loading indicators working
- [ ] **B012**: `npx playwright test test-b012-error-handling.spec.ts` (Target: <60s, Actual: ~46s CLI)
  - [ ] Error scenarios handled gracefully
- [ ] **B013**: `npx playwright test test-b013-performance.spec.ts` (Target: <60s, Actual: ~67s CLI)
  - [ ] Performance baselines established
- [ ] **B014**: `npx playwright test test-b014-accessibility.spec.ts` (Target: <60s, Actual: ~43s CLI)
  - [ ] Accessibility compliance confirmed
- [ ] **B015**: `npx playwright test test-b015-ui-consistency.spec.ts` (Target: <60s, Actual: ~39s CLI)
  - [ ] UI consistency across buttons verified
- [ ] **B016**: `npx playwright test test-b016-button-integration.spec.ts` (Target: <90s, Actual: ~51s CLI)
  - [ ] Complete integration workflow functional

#### Post-Test Validation

- [ ] All tests completed successfully or with documented issues
- [ ] Single browser session maintained throughout execution
- [ ] Performance metrics recorded for each test
- [ ] Test results documented in report format
- [ ] Infrastructure remained stable throughout testing

### CLI Test Execution Calculations

#### Total Execution Time Calculation

- **Individual Test Times**: Sum all test execution times
- **CLI Report Example**: ~773 seconds total (~12.9 minutes for complete suite)
- **Average Execution Time**: ~48.3 seconds per test
- **Calculation**: Sum of all individual test times from CLI execution
- **Performance Breakdown**: Using new emoji system (Good/OK/Slow counts)

#### Test Validation Count Calculation

- **Individual Validation Points**: Count ✅/❌ items per test
- **Example**: 77/99 individual validations passed (78% pass rate)
- **Calculation**: (Passed validations / Total validations) × 100
- **Pattern**: Each test has 5-7 validation points, sum across all tests

#### Performance Classification Distribution (New System)

- **Good 😊 Count**: Tests completing ≤30 seconds
- **OK 😐 Count**: Tests completing 31-60 seconds
- **Slow 😴 Count**: Tests completing 61-119 seconds
- **Pass Rate**: (All tests completing <120s / Total tests) × 100
- **Example**: 16/16 PASS with 8 Good 😊, 5 OK 😐, 3 Slow 😴 = 100% pass rate

### CLI Command Output Examples

#### Expected Console Output Pattern

**Successful Test Output**:

```bash
$ npx playwright test test-b001-market-status.spec.ts
Running 1 test using 1 worker
✓ test-b001-market-status.spec.ts:XX:XX TEST-B001: Market Status (8.3s)
1 passed (8.3s)
```

**Test with Config Issues**:

```bash
$ npx playwright test test-b007-stock-snapshot.spec.ts  
Running 1 test using 1 worker
✓ test-b007-stock-snapshot.spec.ts:XX:XX TEST-B007: Stock Snapshot Button (10.8s)
⚠ Configuration warnings: polling interval mismatch, timeout validation
1 passed (10.8s)
```

---

## MCP Browser Automation Methodology

### MCP Tool Integration

#### Available MCP Browser Tools (Complete Reference)

**Core Navigation & Page Control:**

- `mcp__playwright__browser_navigate` - Navigate to URLs with error handling
- `mcp__playwright__browser_snapshot` - Capture accessibility snapshots for analysis
- `mcp__playwright__browser_evaluate` - Execute JavaScript for validation
- `mcp__playwright__browser_network_requests` - Monitor API calls and responses

**User Interaction Tools:**

- `mcp__playwright__browser_type` - Type text into form elements
- `mcp__playwright__browser_click` - Click buttons, links, and interactive elements
- `mcp__playwright__browser_press_key` - Send keyboard events
- `mcp__playwright__browser_hover` - Hover over elements

**Waiting & Response Detection:**

- `mcp__playwright__browser_wait_for` - Wait for text, elements, or time (CRITICAL for polling)

**Advanced Features:**

- `mcp__playwright__browser_fill_form` - Fill multiple form fields simultaneously
- `mcp__playwright__browser_select_option` - Select dropdown options
- `mcp__playwright__browser_take_screenshot` - Visual documentation (supplementary)

#### MCP Execution Workflow with 10-Second Polling

**Standard Test Execution Pattern:**

1. **Initialize**: `mcp__playwright__browser_navigate` to test URL
2. **Capture State**: `mcp__playwright__browser_snapshot` for baseline
3. **Execute Action**: Use appropriate input/click tools
4. **Poll Response**: `mcp__playwright__browser_wait_for` with 10-second intervals
5. **Validate**: Check response content for pass/fail criteria
6. **Document**: Record timing and performance classification

**Critical 10-Second Polling Implementation:**

```json
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "Expected Response Pattern",
    "time": 10
  }
}
```

**Repeat every 10 seconds until response detected or 120s timeout reached.**

#### Complete MCP Tool Examples for AI Agents

**For AI Agents with Zero MCP Experience:**
These examples provide exact tool calls, parameters, and expected outputs for common test scenarios.

**Example 1: B001 Market Status Test (Complete Workflow)**

```json
// Step 1: Navigate to frontend
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://localhost:3000"
  }
}
// Expected: Navigation successful, page loaded

// Step 2: Take baseline snapshot
{
  "tool": "mcp__playwright__browser_snapshot",
  "parameters": {}
}
// Expected: Accessibility tree snapshot returned

// Step 3: Type query into message input
{
  "tool": "mcp__playwright__browser_type",
  "parameters": {
    "element": "message input textarea",
    "ref": "textarea[placeholder*='message']",
    "text": "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
}
// Expected: Text entered into textarea

// Step 4: Send message
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Enter"
  }
}
// Expected: Message submitted, processing begins

// Step 5: Poll for response every 10 seconds
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "🎯 KEY TAKEAWAYS",
    "time": 10
  }
}
// Expected: Either response detected or timeout after 10s
// If timeout, repeat this step until response or 120s total

// Step 6: Validate response content for PASS/FAIL
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const responses = document.querySelectorAll('.message-content'); return responses[responses.length-1]?.textContent || 'No response found'; }"
  }
}
// Expected: Response text for validation
```

**Example 2: B007 Button Test (Button Interaction)**

```json
// After navigation and baseline setup...

// Click stock snapshot button
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "stock snapshot button",
    "ref": "[data-testid='stock-snapshot-button'], button[title*='snapshot'], button:has-text('📈')"
  }
}
// Expected: Button clicked, template activated

// Poll for analysis response
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "📈 Market Snapshot",
    "time": 10
  }
}
// Repeat every 10s until detected or 120s timeout
```

**Critical Notes for AI Agents:**

- Always use exact parameter names as shown
- "ref" parameter should include multiple selector options (comma-separated)
- "time" in wait_for is interval seconds, not total timeout
- Repeat wait_for calls every 10 seconds, don't set time=120
- Check response content for pass/fail validation after detection

### MCP Testing Checklist

#### Pre-Test Setup

- [ ] FastAPI backend operational on port 8000
- [ ] Vite frontend operational with dynamic port detection (3000, 3001, 3002, etc.)
- [ ] MCP browser tools available and functional
- [ ] Frontend URL determined with port auto-adjustment handling

#### MCP Test Execution (B001-B006: Market/Ticker Tests)

##### B001: Market Status Check

- [ ] `mcp__playwright__browser_navigate` with parameters: `{"url": "http://localhost:3000"}`
- [ ] `mcp__playwright__browser_snapshot` with parameters: `{}`
- [ ] `mcp__playwright__browser_type` with parameters: `{"element": "Message input", "ref": "textarea", "text": "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"}`
- [ ] `mcp__playwright__browser_press_key` with parameters: `{"key": "Enter"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "🎯 KEY TAKEAWAYS", "time": 10}` (repeat every 10s, max 120s total)
- [ ] Validate market status data and emoji indicators (📈📉💰)
- [ ] Expected duration: ~42 seconds (SLOW_PERFORMANCE classification)

##### B002: NVDA Ticker Analysis

- [ ] `mcp__playwright__browser_type` with parameters: `{"element": "Message input", "ref": "textarea", "text": "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"}`
- [ ] `mcp__playwright__browser_press_key` with parameters: `{"key": "Enter"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📈 NVIDIA Corporation", "time": 10}` (repeat every 10s, max 120s total)
- [ ] Validate comprehensive NVIDIA stock analysis with pricing and volume
- [ ] Expected duration: ~62 seconds (SLOW_PERFORMANCE)

##### B003: SPY Ticker Analysis

- [ ] `mcp__playwright__browser_type` with parameters: `{"element": "Message input", "ref": "textarea", "text": "Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"}`
- [ ] `mcp__playwright__browser_press_key` with parameters: `{"key": "Enter"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📊 SPDR S&P 500", "time": 120}`
- [ ] Validate S&P 500 ETF analysis quality with sector performance
- [ ] Expected duration: ~23 seconds (SUCCESS)

##### B004: GME Ticker Analysis

- [ ] `mcp__playwright__browser_type` with parameters: `{"element": "Message input", "ref": "textarea", "text": "Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"}`
- [ ] `mcp__playwright__browser_press_key` with parameters: `{"key": "Enter"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "🎮 GameStop", "time": 120}`
- [ ] Validate GameStop stock analysis with volatility patterns
- [ ] Expected duration: ~29 seconds (SUCCESS)

##### B005: Multi-Ticker Analysis

- [ ] `mcp__playwright__browser_type` with parameters: `{"element": "Message input", "ref": "textarea", "text": "Full Market Snapshot with multiple Tickers: NVDA, SPY, QQQ, IWM: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"}`
- [ ] `mcp__playwright__browser_press_key` with parameters: `{"key": "Enter"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📊 COMPARATIVE ANALYSIS", "time": 120}`
- [ ] Validate complex multi-ticker processing across all 4 tickers
- [ ] Expected duration: ~64 seconds (SLOW_PERFORMANCE)

##### B006: Empty Message Validation

- [ ] `mcp__playwright__browser_evaluate` with parameters: `{"function": "() => { const input = document.querySelector('textarea'); const sendBtn = document.querySelector('[data-testid=\"send-button\"]'); return { isEmpty: input.value === '', isDisabled: sendBtn?.disabled, placeholder: input.placeholder }; }"}`
- [ ] `mcp__playwright__browser_snapshot` with parameters: `{}`
- [ ] Validate send button disabled with empty input, proper placeholder text, form validation working
- [ ] Expected duration: Instant (SUCCESS)

#### MCP Test Execution (B007-B016: Button Tests)

##### B007: Stock Snapshot Button

- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "stock snapshot button", "ref": "[data-testid='stock-snapshot-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📈 Market Snapshot Analysis", "time": 120}`
- [ ] Validate stock snapshot analysis from button template
- [ ] Expected duration: ~85 seconds (SLOW_PERFORMANCE)

##### B008: Support/Resistance Button

- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "support resistance button", "ref": "[data-testid='support-resistance-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📊 Support and Resistance Levels", "time": 120}`
- [ ] Validate support/resistance level calculations
- [ ] Expected duration: ~87 seconds (SLOW_PERFORMANCE)

##### B009: Technical Analysis Button

- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "technical analysis button", "ref": "[data-testid='technical-analysis-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "🔧 Technical Analysis", "time": 120}`
- [ ] Validate complete technical analysis delivery
- [ ] Expected duration: ~89 seconds (SLOW_PERFORMANCE)

##### B010: Multi-Button Interaction

- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "stock snapshot button", "ref": "[data-testid='stock-snapshot-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📈 Market Snapshot", "time": 60}`
- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "support resistance button", "ref": "[data-testid='support-resistance-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📊 Support and Resistance", "time": 60}`
- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "technical analysis button", "ref": "[data-testid='technical-analysis-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "🔧 Technical Analysis", "time": 60}`
- [ ] Validate proper sequential interaction handling
- [ ] Expected duration: ~36 seconds total (SUCCESS)

##### B011: Button State Validation

- [ ] `mcp__playwright__browser_evaluate` with parameters: `{"function": "() => { return { buttonStates: [...document.querySelectorAll('[data-testid*=\"-button\"]')].map(btn => ({ id: btn.dataset.testid, disabled: btn.disabled, visible: btn.offsetParent !== null })); }"}`
- [ ] `mcp__playwright__browser_snapshot` with parameters: `{}`
- [ ] Validate loading indicators and UI feedback
- [ ] Expected duration: <60 seconds (SUCCESS)

##### B012: Button Error Handling

- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "technical analysis button", "ref": "[data-testid='technical-analysis-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "Error", "time": 30}`
- [ ] `mcp__playwright__browser_evaluate` with parameters: `{"function": "() => { return { errorMessages: [...document.querySelectorAll('.error, .alert-error')].map(el => el.textContent); }; }"}`
- [ ] Validate graceful error recovery mechanisms
- [ ] Expected duration: <60 seconds (SUCCESS)

##### B013: Button Performance Validation

- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "stock snapshot button", "ref": "[data-testid='stock-snapshot-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📈 Market Snapshot", "time": 30}`
- [ ] `mcp__playwright__browser_network_requests` with parameters: `{}`
- [ ] Monitor response times and system behavior
- [ ] Expected duration: ~30 seconds baseline (SLOW_PERFORMANCE)

##### B014: Button Accessibility

- [ ] `mcp__playwright__browser_press_key` with parameters: `{"key": "Tab"}`
- [ ] `mcp__playwright__browser_evaluate` with parameters: `{"function": "() => { const focused = document.activeElement; return { focusedElement: focused?.dataset?.testid, hasAriaLabel: !!focused?.getAttribute('aria-label') }; }"}`
- [ ] `mcp__playwright__browser_press_key` with parameters: `{"key": "Enter"}`
- [ ] Validate keyboard navigation and accessibility compliance
- [ ] Expected duration: <60 seconds (SUCCESS)

##### B015: Button UI Consistency

- [ ] `mcp__playwright__browser_snapshot` with parameters: `{}`
- [ ] `mcp__playwright__browser_evaluate` with parameters: `{"function": "() => { return { buttonStyles: [...document.querySelectorAll('[data-testid*="-button"]')].map(btn => ({ id: btn.dataset.testid, computed: window.getComputedStyle(btn), classes: btn.className })); }"}`
- [ ] Validate visual consistency across button states
- [ ] Expected duration: <60 seconds (SUCCESS)

##### B016: Button Integration

- [ ] `mcp__playwright__browser_click` with parameters: `{"element": "stock snapshot button", "ref": "[data-testid='stock-snapshot-button']"}`
- [ ] `mcp__playwright__browser_wait_for` with parameters: `{"text": "📈 Market Snapshot", "time": 90}`
- [ ] `mcp__playwright__browser_network_requests` with parameters: `{}`
- [ ] `mcp__playwright__browser_evaluate` with parameters: `{"function": "() => { return { integrationComplete: document.querySelector('.response-content')?.textContent?.includes('📈'), systemStatus: 'operational' }; }"}`
- [ ] Confirm full system integration functionality
- [ ] Expected duration: <90 seconds (SUCCESS)

#### MCP Post-Test Actions

- [ ] `browser_network_requests` to review API calls and timing
- [ ] `browser_snapshot` for final state capture
- [ ] Document all MCP tool interactions and responses
- [ ] Browser session properly maintained throughout testing

---

## Performance Standards and Validation

### Performance Classifications (Updated System)

**Pass/Fail Criteria:**

- **PASS**: Test completes correctly within 120 seconds
- **FAIL**: Test fails to complete correctly OR exceeds 120 seconds

**Performance Reference Categories:**

- **Good 😊**: ≤30 seconds (optimal performance)
- **OK 😐**: 31-60 seconds (acceptable performance)
- **Slow 😴**: 61-119 seconds (functional but slow)
- **TIMEOUT**: ≥120 seconds (automatic FAIL)

### Performance Classification Usage

**CLI Method Performance (New System)**:

- Expected: Majority Good 😊 and OK 😐 classifications due to inherent speed
- Pattern: Faster execution times, consistent performance

**MCP Method Performance (New System)**:

- Expected: More OK 😐 and Slow 😴 classifications (normal for MCP)
- Good 😊: B003 (23s), B004 (29s), B006 (instant)
- OK 😐: B001 (42s), B010 (36s)
- Slow 😴: B002 (62s), B005 (64s), B007 (85s), B008 (87s), B009 (89s)
- Pattern: Variable performance but all functional within 120s timeout

### Polling Methodology

- **Standard Polling**: 30-second intervals for response detection
- **Early Completion**: Tests complete when response criteria met
- **Maximum Timeout**: 120 seconds per individual test
- **Session Continuity**: Single browser instance maintained across all tests

### Success Criteria

- **Functionality**: All core features operational regardless of performance classification
- **Response Quality**: Proper emoji indicators (📈📉💰🎯) and structured output format
- **Error Handling**: Graceful failure modes and clear user feedback
- **Integration**: Complete end-to-end workflow validation

### Port Management

**Frontend Port Auto-Adjustment**: Vite automatically selects available ports:

- Default: port 3000
- Auto-adjust: 3000 → 3001 → 3002 → 3003 → etc.
- **Critical**: Tests must detect and use the actual frontend port
- **Configuration**: Update test URLs to match actual frontend port

---

## Test Report Generation

### Report Naming Convention

```text
playwright_[METHOD]_test_[YY-MM-DD]_[HH-MM].md
```

**Examples:**

- `playwright_CLI_test_25-09-10_11-39.md`
- `playwright_MCP_test_25-09-10_16-35.md`

### Required Report Structure

#### Report Header Format

**CLI Report Header Example**:

```markdown
# Comprehensive Playwright CLI Test Execution Report B001-B016

**Report Date:** 2025-09-10  
**Test Coverage:** Playwright CLI Complete Test Suite (B001-B016)  
**Test Environment:** Single Browser Session with CLI Automation Tools  
**Report Type:** Playwright CLI Testing Methodology  
```

**MCP Report Header Example**:

```markdown
# Playwright MCP Test Execution Report
**Date:** September 10, 2025 at 4:35 PM Pacific  
**Test Suite:** Complete Button Template Testing (B001-B016)  
**Coverage:** 16/16 Tests Completed (100%)  
**Protocol:** Single Browser Session  
**Framework:** Playwright MCP with Systematic Automation  
```

#### Executive Summary

- **Test Coverage**: Total tests executed and coverage percentage
- **Overall Success Rate**: Performance classifications and pass rates  
- **Key Achievements**: Major validation results and system status
- **Infrastructure Status**: Server stability throughout testing

#### Performance Overview

- **Average Response Time**: Calculated across all tests
- **Performance Distribution**: SUCCESS vs SLOW_PERFORMANCE counts
- **Infrastructure Status**: Backend/frontend operational status
- **API Integration**: MCP server connectivity confirmation

#### Detailed Test Results

**For each test (B001-B016), include:**

- **Test Name**: With SUCCESS/SLOW_PERFORMANCE classification
- **Duration**: Actual execution time
- **Status**: PASSED/FUNCTIONAL (Performance Issue)/FAILED
- **Validation**: Specific functionality confirmed
- **Response Quality**: Analysis quality assessment
- **Performance Impact**: Any timing issues noted

**New Format with Performance Emojis:**

```markdown
#### B001: Market Status Check ✅ PASS 😐 (42s)
- **Result:** PASS - Response received within 120s timeout
- **Performance:** OK 😐 (42 seconds - within 60s threshold)
- **Validation:** Basic market data retrieval functionality confirmed
- **Response Format:** Proper emoji-enhanced financial analysis received
- **Method Notes:** MCP method inherently slower than CLI (expected)
```

**Performance Classification Examples:**

- ✅ PASS 😊 (28s) - Good performance
- ✅ PASS 😐 (45s) - OK performance  
- ✅ PASS 😴 (89s) - Slow but functional
- ❌ FAIL (125s) - Exceeded timeout

#### Infrastructure Assessment

**System Components Status Template:**

```markdown
### System Components Status
✅ **FastAPI Backend:** Operational on port 8000  
✅ **Vite Development Server:** Operational on port [3000/3001/3002] (auto-detected)
✅ **MCP Server Integration:** Polygon.io connectivity confirmed  
✅ **OpenAI API Integration:** GPT-5-mini model responding correctly  
✅ **Database/Session Management:** State persistence working  
```

**Performance Metrics Template:**

```markdown
### Performance Metrics
- **API Response Times:** Variable [min]-[max] seconds depending on complexity
- **UI Responsiveness:** Immediate button interactions with proper loading states
- **Memory Usage:** Stable throughout extended test session  
- **Error Recovery:** Robust error handling across all test scenarios
```

**Technical Validation Template:**

```markdown
### Technical Validation
- **Single Browser Session:** Successfully maintained throughout all [X] tests
- **State Persistence:** UI state properly maintained between test executions
- **Cross-Component Integration:** Frontend, backend, and MCP server integration confirmed
- **Real-World Simulation:** Test methodology accurately simulates actual user behavior
```

#### Performance Analysis

- **Response Time Categories**: SUCCESS (≤30s) vs SLOW_PERFORMANCE (31-89s) counts
- **Performance Distribution**: Fastest/slowest/average response times
- **Optimization Opportunities**: Areas requiring performance improvement

#### Results Summary Table

```markdown
| Method | Tests Executed | Core Success Rate | Performance Classification | Key Findings |
|--------|----------------|-------------------|---------------------------|--------------|
| **Playwright [CLI/MCP]** | 16 tests (B001-B016) | [X]% ([Y]/[Z] individual validations) | [X]% SUCCESS (<[T]s each) | [Key findings summary] |
```

### Quality Metrics Template

**CLI Report Quality Metrics Section:**

```markdown
### Quality Metrics
- **100% Test Completion Rate**
- **Zero Test Failures**
- **Infrastructure Stability:** 100% uptime during testing
- **Performance Classification:** [X] SUCCESS tests, [Y] SLOW_PERFORMANCE tests
- **Average Response Time:** [X.X] seconds
- **Error Recovery:** Robust error handling across all failure scenarios
```

**Key Quality Indicators:**

- **Test Completion Rate**: (Completed tests / Total tests) × 100
- **Performance Distribution**: COUNT of SUCCESS vs SLOW_PERFORMANCE tests
- **Infrastructure Uptime**: Percentage of stable backend/frontend operation
- **Error Handling Validation**: Documentation of error recovery across scenarios

### Test Validation Documentation

**For each test, document:**

- Test results breakdown (✅/❌ format)
- Expected response validation points
- Performance timing comparison
- Infrastructure status during test
- Error conditions encountered (if any)

---

  📁 Directory Structure Overview

  Root /tests/ Directory:

- ✅ playwright.config.ts - Main Playwright configuration
- ✅ test_api.py - API smoke tests
- ✅ test_cli.py - CLI smoke tests
- ✅ validate_structure.py - Migration validation script
- ✅ playwright/ - Complete Playwright test suite

  /tests/playwright/ Directory:

- ✅ Complete B001-B016 Test Suite - All 16 test files present
- ✅ PLAYWRIGHT_TESTING_MASTER_PLAN.md - Comprehensive test documentation
- ✅ Helper Infrastructure - 7 helper modules in /helpers/ directory
- ✅ Additional Tests - Integration, example, and UI investigation tests

  🔧 Key Configuration Analysis

  Playwright Configuration (playwright.config.ts):

- ✅ Single Browser Session: workers: 1 enforced
- ✅ 120s Timeout: timeout: 120000 implemented
- ✅ Dynamic Port Detection: Supports ports 3000-3010
- ✅ New Structure Support: Updated for /src/ backend and /frontend/ frontend
- ✅ Web Server Config: Proper frontend/backend server management

  Helper Utilities Framework:

- ✅ Polling System: 30-second intervals with 120s max timeout
- ✅ Port Detection: Automatic frontend port discovery (3000+)
- ✅ Performance Classification: Good 😊 / OK 😐 / Slow 😴 system
- ✅ Session Management: Browser session continuity
- ✅ Validation Framework: Financial emoji detection and response validation

  🧪 Test Suite Completeness

  Market/Ticker Tests (B001-B006):

- ✅ B001: Market Status Check
- ✅ B002: NVDA Ticker Analysis
- ✅ B003: SPY Ticker Analysis
- ✅ B004: GME Ticker Analysis
- ✅ B005: Multi-Ticker Analysis
- ✅ B006: Empty Message Validation

  Button System Tests (B007-B016):

- ✅ B007-B009: Core button functionality (Stock Snapshot, Support/Resistance,
  Technical Analysis)
- ✅ B010-B012: Interaction, validation, and error handling
- ✅ B013-B016: Performance, accessibility, UI consistency, and integration

  📊 Validation Infrastructure

  Smoke Tests:

- ✅ API Test: Basic health endpoint validation
- ✅ CLI Test: Backend functionality verification
- ✅ Structure Validator: Phase 9 migration validation

  Quality Assurance:

- ✅ Performance Timing: Accurate measurement without artificial delays
- ✅ Response Validation: Financial emoji detection (📈📉💰🎯)
- ✅ Session Integrity: Single browser instance protocol
- ✅ Port Management: Dynamic frontend port detection

  🎯 Key Implementation Features

  Advanced Capabilities:

- ✅ Dynamic Server Detection: Automatic port discovery and health checks
- ✅ Performance Classification: Real-time performance categorization
- ✅ Response Validation: Financial content and emoji indicator validation
- ✅ Session Management: Proper browser session continuity
- ✅ Error Recovery: Comprehensive error handling and recovery mechanisms

---

## Troubleshooting and Edge Cases

### Common Issues and Solutions

#### Server Startup Problems

- **Backend Issues**: Check API keys in `.env`, verify uv installation, resolve port conflicts
- **Frontend Issues**: Update Node.js to 18+, handle npm dependency issues, allow port auto-adjustment
- **CORS Problems**: Verify cross-origin configuration matches actual frontend port

#### Port Management Issues

**Frontend Port Auto-Adjustment Handling:**

```bash
# Detect actual frontend port
curl -f http://localhost:3000/ && echo "Frontend on 3000" || \
curl -f http://localhost:3001/ && echo "Frontend on 3001" || \
curl -f http://localhost:3002/ && echo "Frontend on 3002" || \
echo "Frontend port detection failed"
```

**Update test configuration for detected port:**

- CLI: Ensure test files use correct port
- MCP: Update `browser_navigate` URL parameter

#### Test Execution Issues

- **Browser Not Found**: Run `npx playwright install chromium`
- **Test Timeouts**: Check server performance, increase timeout if needed
- **Network Errors**: Verify server health and connectivity
- **Polling Configuration**: Handle expected 30000ms vs actual 100ms mismatch

#### Performance Issues

- **Slow Responses**: Check MCP server timeout configuration (default: 120s)
- **Memory Problems**: Monitor system resources during testing
- **API Performance**: Consider MCP_TIMEOUT_SECONDS environment variable

#### Single Browser Session Issues

- **Session Breaks**: Ensure no intermediate browser restarts
- **State Loss**: Verify session continuity throughout test sequence
- **Multiple Sessions**: Avoid opening/closing browser between test groups

### Edge Case Handling

#### Infrastructure Edge Cases

- **Port Conflicts**: Handle automatic port selection gracefully
- **Server Restart**: Detect and handle server restarts during testing
- **Network Interruption**: Implement retry mechanisms for network failures

#### Test Performance Edge Cases

- **Extended Processing Times**: Handle SLOW_PERFORMANCE classification appropriately
- **Timeout Conditions**: Document and handle >120 second timeouts
- **Partial Test Completion**: Handle incomplete test sequences due to failures

#### Data Validation Edge Cases

- **Market Hours**: Handle after-hours or weekend testing scenarios
- **API Rate Limits**: Handle Polygon.io API rate limiting
- **Empty/Invalid Responses**: Validate error handling for API failures

### System Requirements

- **Node.js**: 18+ required for frontend operations
- **Python**: 3.10+ with uv package manager for backend
- **Browser**: Chromium for Playwright automation
- **Memory**: 4GB+ recommended for complete test suite execution
- **Network**: Stable internet for Polygon.io API access and MCP operations

---

## Best Practices

### Testing Integrity

- Always execute complete B001-B016 suite for comprehensive validation
- Maintain single browser session throughout entire test sequence
- Document all test results including failures with detailed analysis
- Never skip tests or claim completion without full execution validation

### Performance Optimization

- Start both servers before any test execution
- Monitor system resources during testing execution
- Use appropriate polling intervals for early completion detection
- Document performance baselines for future comparison and optimization

### Quality Control

- Cross-reference all test results with actual system functionality
- Validate response format and content quality for each test
- Ensure infrastructure stability throughout complete test execution
- Document any configuration issues or system limitations encountered

### Documentation Maintenance

- Regular review of test specifications for continued accuracy
- Update performance thresholds based on system improvements over time
- Maintain compatibility with browser and framework updates
- Keep test documentation synchronized with actual implementation changes

---

This master plan provides the definitive guide for Playwright testing execution in the Market Parser application, ensuring consistent, reliable, and comprehensive test coverage across both CLI and MCP methodologies with full replication capability.
