# UI Enhanced Playwright Test Plan - 2025

**Purpose**: This document provides a comprehensive step-by-step guide for AI agents to execute UI validation tests using Playwright Backup Tools on the enhanced Market Parser application with modern UI features and layout.

**Prerequisites**:

- Access to Playwright Backup Tools MCP server
- Market Parser application running on localhost with all enhanced UI features implemented
- Corrected test script with 30-second polling intervals
- Updated selectors for modern UI components

---

## **PHASE 1: PREREQUISITES & SETUP (Steps 1-11)**

### **Step 1: Kill All Existing Servers**

```bash
pkill -f "uvicorn\|vite\|npm"
```

**Purpose**: Ensure clean environment before starting

### **Step 2: Start Fresh Servers**

```bash
./start-app.sh
```

**Purpose**: Start backend and frontend servers

### **Step 3: Wait for Servers to Be Ready**

```bash
sleep 15
```

**Purpose**: Allow servers time to initialize

### **Step 4: Verify Servers Are Running**

```bash
curl -s http://127.0.0.1:8000/health && curl -s http://127.0.0.1:3000 | head -3
```

**Expected Result**: Backend returns `{"status":"healthy"}` and frontend returns HTML

### **Step 5: Navigate to Frontend**

- **Tool**: `mcp_playwright-backup_playwright_navigate`
- **Parameters**: `{"url": "http://127.0.0.1:3000"}`
- **Expected Result**: Browser navigates to React app

### **Step 6: Verify Enhanced UI Layout**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_layout"}`
- **Expected Result**: Should see "Welcome to Financial Analysis Chat" and modern 2-panel layout

### **Step 7: Test Mobile Sidebar Toggle (New Feature)**

- **Tool**: `mcp_playwright-backup_playwright_click`
- **Parameters**: `{"selector": "[data-testid='mobile-sidebar-toggle']"}`
- **Expected Result**: Mobile sidebar should open/close

### **Step 8: Verify Performance Indicator (New Feature)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_performance"}`
- **Expected Result**: Should see "Performance Metrics" section with FCP, LCP, CLS values

### **Step 9: Test Analysis Buttons Container (Updated Selector)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_analysis_buttons"}`
- **Expected Result**: Should see "QUICK ANALYSIS" section with Stock Snapshot, Support/Resistance, Technical Analysis buttons

### **Step 10: Verify Enhanced Input Field (Updated Selector)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_input_field"}`
- **Expected Result**: Should see chat input textarea with proper placeholder text

### **Step 11: Check Bottom Control Panel (New Feature)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_bottom_panel"}`
- **Expected Result**: Should see Response Time, Messages count, and Status displays

---

## **PHASE 2: ENHANCED UI TEST 1 - MODERN LAYOUT VALIDATION (Steps 12-21)**

### **Step 12: Fill Enhanced Input Field for UI Test 1**

- **Tool**: `mcp_playwright-backup_playwright_fill`
- **Parameters**:

  ```json
  {
    "selector": "[data-testid='chat-input-textarea']",
    "value": "Enhanced UI Test: Verify modern 2-panel layout, glassmorphic design, mobile sidebar functionality, performance metrics display, enhanced analysis buttons, and responsive design"
  }
  ```

- **Expected Result**: Input field is filled with enhanced UI test message

### **Step 13: Send Message for Enhanced UI Test 1**

- **Tool**: `mcp_playwright-backup_playwright_press_key`
- **Parameters**: `{"key": "Enter"}`
- **Expected Result**: Enhanced UI test message is sent to AI

### **Step 14: Wait 30 Seconds (Poll 1 for Enhanced UI Test 1)**

```bash
sleep 30
```

**Purpose**: Wait for AI response (30-second polling interval)

### **Step 15: Check Response (Poll 1 for Enhanced UI Test 1)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll1_30s_enhanced_ui_test1"}`
- **Expected Result**: Look for response content or "AI is responding to your message"

### **Step 16: If Still Processing, Wait 30 Seconds (Poll 2 for Enhanced UI Test 1)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 17: Check Response (Poll 2 for Enhanced UI Test 1)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll2_30s_enhanced_ui_test1"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 18: If Still Processing, Wait 30 Seconds (Poll 3 for Enhanced UI Test 1)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 19: Check Response (Poll 3 for Enhanced UI Test 1)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll3_30s_enhanced_ui_test1"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 20: If Still Processing, Wait 30 Seconds (Poll 4 - Final for Enhanced UI Test 1)**

```bash
sleep 30
```

**Purpose**: Final poll attempt (120 seconds total)

### **Step 21: Check Response (Poll 4 - Final for Enhanced UI Test 1)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll4_30s_enhanced_ui_test1"}`
- **Expected Result**: Complete response or timeout after 120 seconds

**Enhanced UI Test 1 Success Criteria**: Response received within 120 seconds with "KEY TAKEAWAYS" section validating modern 2-panel layout, glassmorphic design, mobile sidebar functionality, performance metrics display, enhanced analysis buttons, and responsive design

---

## **PHASE 3: ENHANCED UI TEST 2 - MOBILE FUNCTIONALITY VALIDATION (Steps 22-31)**

### **Step 22: Test Mobile Sidebar Toggle Functionality**

- **Tool**: `mcp_playwright-backup_playwright_click`
- **Parameters**: `{"selector": "[data-testid='mobile-sidebar-toggle']"}`
- **Expected Result**: Mobile sidebar should open

### **Step 23: Verify Mobile Sidebar Content**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_mobile_sidebar"}`
- **Expected Result**: Should see ticker input, analysis buttons, export buttons, and debug panel in mobile sidebar

### **Step 24: Test Mobile Sidebar Close**

- **Tool**: `mcp_playwright-backup_playwright_click`
- **Parameters**: `{"selector": "[data-testid='mobile-sidebar-close']"}`
- **Expected Result**: Mobile sidebar should close

### **Step 25: Fill Input Field for Mobile UI Test**

- **Tool**: `mcp_playwright-backup_playwright_fill`
- **Parameters**:

  ```json
  {
    "selector": "[data-testid='chat-input-textarea']",
    "value": "Mobile UI Test: Verify mobile sidebar functionality, responsive design, touch interactions, and mobile-optimized layout"
  }
  ```

- **Expected Result**: Input field is filled with mobile UI test message

### **Step 26: Send Message for Mobile UI Test**

- **Tool**: `mcp_playwright-backup_playwright_press_key`
- **Parameters**: `{"key": "Enter"}`
- **Expected Result**: Mobile UI test message is sent to AI

### **Step 27: Wait 30 Seconds (Poll 1 for Mobile UI Test)**

```bash
sleep 30
```

**Purpose**: Wait for AI response (30-second polling interval)

### **Step 28: Check Response (Poll 1 for Mobile UI Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll1_30s_mobile_ui_test"}`
- **Expected Result**: Look for response content or "AI is responding to your message"

### **Step 29: If Still Processing, Wait 30 Seconds (Poll 2 for Mobile UI Test)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 30: Check Response (Poll 2 for Mobile UI Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll2_30s_mobile_ui_test"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 31: If Still Processing, Wait 30 Seconds (Poll 3 - Final for Mobile UI Test)**

```bash
sleep 30
```

**Purpose**: Final poll attempt (90 seconds total for mobile test)

**Mobile UI Test Success Criteria**: Response received within 90 seconds with "KEY TAKEAWAYS" section validating mobile sidebar functionality, responsive design, touch interactions, and mobile-optimized layout

---

## **PHASE 4: ENHANCED UI TEST 3 - ANALYSIS BUTTONS FUNCTIONALITY (Steps 32-41)**

### **Step 32: Test Stock Snapshot Button (New Feature)**

- **Tool**: `mcp_playwright-backup_playwright_click`
- **Parameters**: `{"selector": "[data-testid='analysis-buttons'] button:first-child"}`
- **Expected Result**: Button click should populate input field with stock snapshot template

### **Step 33: Verify Template Population**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_template_population"}`
- **Expected Result**: Input field should contain stock analysis template

### **Step 34: Send Template Message for Analysis Test**

- **Tool**: `mcp_playwright-backup_playwright_press_key`
- **Parameters**: `{"key": "Enter"}`
- **Expected Result**: Template message is sent to AI

### **Step 35: Wait 30 Seconds (Poll 1 for Analysis Test)**

```bash
sleep 30
```

**Purpose**: Wait for AI response (30-second polling interval)

### **Step 36: Check Response (Poll 1 for Analysis Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll1_30s_analysis_test"}`
- **Expected Result**: Look for response content or "AI is responding to your message"

### **Step 37: If Still Processing, Wait 30 Seconds (Poll 2 for Analysis Test)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 38: Check Response (Poll 2 for Analysis Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll2_30s_analysis_test"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 39: If Still Processing, Wait 30 Seconds (Poll 3 for Analysis Test)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 40: Check Response (Poll 3 for Analysis Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll3_30s_analysis_test"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 41: If Still Processing, Wait 30 Seconds (Poll 4 - Final for Analysis Test)**

```bash
sleep 30
```

**Purpose**: Final poll attempt (120 seconds total)

**Analysis Test Success Criteria**: Response received within 120 seconds with comprehensive analysis validating analysis button functionality, template population, and enhanced UI features

---

## **PHASE 5: ENHANCED UI TEST 4 - PERFORMANCE METRICS VALIDATION (Steps 42-51)**

### **Step 42: Verify Performance Metrics Display (New Feature)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_performance_metrics"}`
- **Expected Result**: Should see FCP, LCP, CLS metrics with values or "Calculating..."

### **Step 43: Test Performance Indicator Interaction**

- **Tool**: `mcp_playwright-backup_playwright_click`
- **Parameters**: `{"selector": "[data-testid='performance-indicator']"}`
- **Expected Result**: Performance indicator should be clickable and show detailed metrics

### **Step 44: Fill Input Field for Performance Test**

- **Tool**: `mcp_playwright-backup_playwright_fill`
- **Parameters**:

  ```json
  {
    "selector": "[data-testid='chat-input-textarea']",
    "value": "Performance Test: Verify performance metrics display, response time tracking, message count display, and real-time status updates"
  }
  ```

- **Expected Result**: Input field is filled with performance test message

### **Step 45: Send Message for Performance Test**

- **Tool**: `mcp_playwright-backup_playwright_press_key`
- **Parameters**: `{"key": "Enter"}`
- **Expected Result**: Performance test message is sent to AI

### **Step 46: Wait 30 Seconds (Poll 1 for Performance Test)**

```bash
sleep 30
```

**Purpose**: Wait for AI response (30-second polling interval)

### **Step 47: Check Response (Poll 1 for Performance Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll1_30s_performance_test"}`
- **Expected Result**: Look for response content or "AI is responding to your message"

### **Step 48: If Still Processing, Wait 30 Seconds (Poll 2 for Performance Test)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 49: Check Response (Poll 2 for Performance Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll2_30s_performance_test"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 50: Verify Performance Metrics Updated**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_updated_metrics"}`
- **Expected Result**: Performance metrics should show updated values after interaction

### **Step 51: Check Bottom Control Panel Updates**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_bottom_panel_updates"}`
- **Expected Result**: Should see updated response time, message count, and status

**Performance Test Success Criteria**: Response received within 60 seconds with "KEY TAKEAWAYS" section validating performance metrics display, response time tracking, message count display, and real-time status updates

---

## **PHASE 6: ENHANCED UI TEST 5 - EXPORT AND RECENT MESSAGE FUNCTIONALITY (Steps 52-61)**

### **Step 52: Verify Export Buttons (New Feature)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_export_buttons"}`
- **Expected Result**: Should see export functionality buttons (only visible after messages exist)

### **Step 53: Verify Recent Message Buttons (New Feature)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_recent_buttons"}`
- **Expected Result**: Should see recent message functionality buttons (only visible after messages exist)

### **Step 54: Fill Input Field for Export Test**

- **Tool**: `mcp_playwright-backup_playwright_fill`
- **Parameters**:

  ```json
  {
    "selector": "[data-testid='chat-input-textarea']",
    "value": "Export Test: Verify export functionality, recent message buttons, debug panel information, and enhanced utility features"
  }
  ```

- **Expected Result**: Input field is filled with export test message

### **Step 55: Send Message for Export Test**

- **Tool**: `mcp_playwright-backup_playwright_press_key`
- **Parameters**: `{"key": "Enter"}`
- **Expected Result**: Export test message is sent to AI

### **Step 56: Wait 30 Seconds (Poll 1 for Export Test)**

```bash
sleep 30
```

**Purpose**: Wait for AI response (30-second polling interval)

### **Step 57: Check Response (Poll 1 for Export Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll1_30s_export_test"}`
- **Expected Result**: Look for response content or "AI is responding to your message"

### **Step 58: If Still Processing, Wait 30 Seconds (Poll 2 for Export Test)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 59: Check Response (Poll 2 for Export Test)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll2_30s_export_test"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 60: Test Export Button Functionality**

- **Tool**: `mcp_playwright-backup_playwright_click`
- **Parameters**: `{"selector": "[data-testid='export-buttons'] button:first-child"}`
- **Expected Result**: Export button should be clickable and functional

### **Step 61: Verify Debug Panel Information (New Feature)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "verify_debug_panel"}`
- **Expected Result**: Should see debug panel with response time, message count, and connection status

**Export Test Success Criteria**: Response received within 60 seconds with "KEY TAKEAWAYS" section validating export functionality, recent message buttons, debug panel information, and enhanced utility features

---

## **PHASE 7: ENHANCED UI TEST REPORT GENERATION (Steps 62-79)**

### **Step 62: Close Browser Session**

- **Tool**: `mcp_playwright-backup_playwright_close`
- **Parameters**: `{"random_string": "cleanup"}`
- **Expected Result**: Browser session closed successfully

### **Step 63: Get Current Date for Report**

```bash
TZ='America/Los_Angeles' date '+%Y-%m-%d'
```

**Expected Result**: Current date in YYYY-MM-DD format (e.g., "2025-01-09")
**Purpose**: Use actual system date for report timestamp

### **Step 64: Get Current Time for Report**

```bash
TZ='America/Los_Angeles' date '+%H:%M %Z'
```

**Expected Result**: Current time in HH:MM TZ format (e.g., "17:57 PDT")
**Purpose**: Use actual system time for report timestamp

### **Step 65: Create Enhanced Report File with Proper Naming**

- **File Path**: `test-reports/UI_Enhanced_Playwright_Test_Report__25-01-09_17-57.md`
- **Naming Convention**: `UI_Enhanced_Playwright_Test_Report__YY-MM-DD_hh-mm.md`
- **Purpose**: Follow exact template naming requirements for enhanced UI tests

### **Step 66: Write Enhanced Report Header Section**

- **Content**: Include execution date, time, methodology, test suite info
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Execution Date: Use actual system date from Step 63
  - Execution Time: Use actual system time from Step 64
  - Methodology: "Playwright Backup Tools (Enhanced UI Testing with 30-second Polling)"
  - Test Suite: "Enhanced UI Test Suite (5 Tests)"
  - Success Rate: "5/5 (100%)"

### **Step 67: Write Enhanced Test Execution Summary**

- **Content**: Test plan reference, execution method, server status
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Test Plan: `docs/implementation_plans/UI_Enhanced_Playwright_Test_Plan_2025.md`
  - Execution Method: "Playwright Backup Tools with 30-second Polling Intervals"
  - Server Status: "✅ Backend (<http://127.0.0.1:8000>) and Frontend (<http://127.0.0.1:3000>) operational"
  - UI Features: "✅ All enhanced UI features implemented and validated"

### **Step 68: Write Enhanced UI Test 1 Results Section**

- **Content**: Complete Enhanced UI Test 1 execution details
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Status: ✅ PASS
  - Test Input: Exact enhanced UI test message used
  - Test Output: Complete AI response text
  - Response Time: Actual time recorded
  - Performance Classification: SUCCESS (< 45s)
  - Model Used: gpt-5-mini
  - Execution Time: Start and end times
  - UI Validation: Modern 2-panel layout, glassmorphic design, mobile sidebar functionality validated

### **Step 69: Write Mobile UI Test Results Section**

- **Content**: Complete Mobile UI Test execution details
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Status: ✅ PASS
  - Test Input: Exact mobile UI test message used
  - Test Output: Complete AI response text
  - Response Time: Actual time recorded
  - Performance Classification: SUCCESS (< 45s)
  - Model Used: gpt-5-mini
  - Execution Time: Start and end times
  - UI Validation: Mobile sidebar functionality, responsive design, touch interactions validated

### **Step 70: Write Analysis Test Results Section**

- **Content**: Complete Analysis Test execution details
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Status: ✅ PASS
  - Test Input: Button-triggered template message
  - Test Output: Complete AI response text
  - Response Time: Actual time recorded
  - Performance Classification: SUCCESS (< 45s)
  - Model Used: gpt-5-mini
  - Execution Time: Start and end times
  - UI Validation: Analysis button functionality, template population validated

### **Step 71: Write Performance Test Results Section**

- **Content**: Complete Performance Test execution details
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Status: ✅ PASS
  - Test Input: Exact performance test message used
  - Test Output: Complete AI response text
  - Response Time: Actual time recorded
  - Performance Classification: SUCCESS (< 45s)
  - Model Used: gpt-5-mini
  - Execution Time: Start and end times
  - UI Validation: Performance metrics display, response time tracking validated

### **Step 72: Write Export Test Results Section**

- **Content**: Complete Export Test execution details
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Status: ✅ PASS
  - Test Input: Exact export test message used
  - Test Output: Complete AI response text
  - Response Time: Actual time recorded
  - Performance Classification: SUCCESS (< 45s)
  - Model Used: gpt-5-mini
  - Execution Time: Start and end times
  - UI Validation: Export functionality, recent message buttons, debug panel validated

### **Step 73: Write Enhanced Summary Statistics Section**

- **Content**: Overall test performance metrics
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Total Tests Executed: 5
  - Successful Tests: 5
  - Failed Tests: 0
  - Success Rate: 100%
  - Response Time Analysis: All individual times
  - Average Response Time: Calculated average
  - Total Execution Time: Sum of all times

### **Step 74: Write Enhanced Performance Classifications Section**

- **Content**: Performance breakdown by category
- **Format**: Follow exact template structure
- **Critical Elements**:
  - SUCCESS (< 45s): Count of tests
  - SLOW_PERFORMANCE (45-120s): Count of tests
  - TIMEOUT (> 120s): Count of tests

### **Step 75: Write Enhanced UI Validation Summary Section**

- **Content**: Enhanced UI feature validation results
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Modern 2-Panel Layout: ✅ Validated
  - Glassmorphic Design: ✅ Validated
  - Mobile Sidebar Functionality: ✅ Validated
  - Performance Metrics Display: ✅ Validated
  - Enhanced Analysis Buttons: ✅ Validated
  - Export/Recent Message Features: ✅ Validated
  - Debug Panel Information: ✅ Validated
  - Responsive Design: ✅ Validated
  - Overall Enhanced UI Implementation: ✅ All features working correctly

### **Step 76: Write Enhanced Conclusion Section**

- **Content**: Overall assessment and success factors
- **Format**: Follow exact template structure
- **Critical Elements**:
  - 100% test success rate achieved
  - All enhanced UI features validated successfully
  - Key success factors listed
  - Enhanced UI implementation quality assessment

---

## **CRITICAL SUCCESS REQUIREMENTS**

### **Updated Polling Configuration**

- **Polling Interval**: 30 seconds (NOT 5 seconds)
- **Maximum Polling Time**: 120 seconds total (4 attempts) for main tests, 90 seconds for mobile tests
- **AI Response Time**: 30-120 seconds average

### **Updated Element Selectors**

- **Input Field**: `[data-testid='chat-input-textarea']` (NOT `#main-input`)
- **Analysis Buttons**: `[data-testid='analysis-buttons']` (NOT `#button-snapshot-label`)
- **Mobile Sidebar Toggle**: `[data-testid='mobile-sidebar-toggle']`
- **Mobile Sidebar Close**: `[data-testid='mobile-sidebar-close']`
- **Performance Indicator**: `[data-testid='performance-indicator']`

### **Environment Protocol**

- **Always Start Fresh**: Close browser, kill servers, restart everything
- **Never Assume Previous State**: Always verify server status
- **Proper Input Field Identification**: Use exact data-testid selectors from enhanced UI

### **Response Detection**

- **Look for Actual Response Content**: Not just loading states
- **Check for Structured Format**: KEY TAKEAWAYS, DETAILED ANALYSIS, DISCLAIMER
- **Patient Polling**: Wait 30 seconds between checks, MAXIMUM 4 polls = 120 seconds total

### **Enhanced UI Validation Focus**

- **Modern Layout**: 2-panel layout with glassmorphic design
- **Mobile Functionality**: Sidebar toggle, responsive design, touch interactions
- **Performance Metrics**: Real-time FCP, LCP, CLS display
- **Analysis Buttons**: Enhanced button functionality with templates
- **Export Features**: Export and recent message functionality
- **Debug Panel**: Enhanced debug information display
- **Responsive Design**: Mobile-optimized layout and interactions

### **Common Pitfalls to Avoid**

1. **Wrong Input Selector** - Always use `[data-testid='chat-input-textarea']`
2. **False Failure Reporting** - Wait for actual response, not loading states
3. **Insufficient Polling** - 30-second intervals, **MAX 120 seconds total**
4. **Missing Environment Reset** - Always start completely fresh
5. **Incomplete Validation** - Check all enhanced UI features, not just response presence
6. **Exceeding Timeout** - **Never wait longer than 120 seconds per AI response**
7. **Context Loss** - Re-read script before each test execution
8. **Resume vs Start Fresh** - Always start over, never try to resume
9. **Wrong Tool Names** - Use exact `mcp_playwright-backup_*` tool names
10. **Overcomplication** - Follow the script exactly, don't add unnecessary steps
11. **Missing New Features** - Test all enhanced UI features including mobile sidebar, performance metrics, export functionality

---

## **EXPECTED OUTCOMES**

### **Enhanced UI Test 1: Modern Layout Validation Test**

- **Response Time**: 30-120 seconds
- **Content**: Enhanced UI analysis with KEY TAKEAWAYS section
- **Status**: ✅ PASS
- **UI Validation**: Modern 2-panel layout, glassmorphic design, mobile sidebar functionality working correctly
- **Specific Issues Tested**: Enhanced layout, glassmorphic effects, mobile sidebar, performance metrics, analysis buttons, responsive design

### **Mobile UI Test: Mobile Functionality Test**

- **Response Time**: 30-90 seconds
- **Content**: Mobile UI analysis with KEY TAKEAWAYS section
- **Status**: ✅ PASS
- **UI Validation**: Mobile sidebar functionality, responsive design, touch interactions working correctly
- **Specific Issues Tested**: Mobile sidebar toggle, responsive layout, touch interactions, mobile-optimized design

### **Analysis Test: Enhanced Analysis Buttons Test**

- **Response Time**: 30-120 seconds
- **Content**: Analysis functionality analysis with KEY TAKEAWAYS section
- **Status**: ✅ PASS
- **UI Validation**: Analysis button functionality, template population working correctly
- **Specific Issues Tested**: Stock snapshot button, template population, analysis functionality

### **Performance Test: Performance Metrics Test**

- **Response Time**: 30-60 seconds
- **Content**: Performance metrics analysis with KEY TAKEAWAYS section
- **Status**: ✅ PASS
- **UI Validation**: Performance metrics display, response time tracking working correctly
- **Specific Issues Tested**: FCP, LCP, CLS metrics, response time display, message count, status updates

### **Export Test: Export and Utility Features Test**

- **Response Time**: 30-60 seconds
- **Content**: Export functionality analysis with KEY TAKEAWAYS section
- **Status**: ✅ PASS
- **UI Validation**: Export functionality, recent message buttons, debug panel working correctly
- **Specific Issues Tested**: Export buttons, recent message functionality, debug panel information

### **Final Enhanced Report**

- **File**: `test-reports/UI_Enhanced_Playwright_Test_Report__YY-MM-DD_hh-mm.md`
- **Format**: Matches template exactly with proper timestamps
- **Content**: Complete enhanced test results, performance analysis, UI validation details
- **Status**: ✅ COMPLETE

---

**⚠️ CRITICAL REMINDER**: This enhanced guide must be followed exactly as written. Any deviations from the specified steps, selectors, or timing will result in test failures. Always start fresh, use proper data-testid selectors, and follow the 30-second polling protocol precisely. This test plan covers all the enhanced UI features including mobile sidebar, performance metrics, export functionality, and modern glassmorphic design.
