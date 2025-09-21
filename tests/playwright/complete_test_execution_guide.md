# Complete Test Execution Guide - Playwright Backup Tools

**Purpose**: This document provides a step-by-step guide for AI agents to execute all three tests using Playwright Backup Tools and generate a comprehensive test report.

**Prerequisites**:

- Access to Playwright Backup Tools MCP server
- Market Parser application running on localhost
- Corrected test script with 30-second polling intervals

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

### **Step 6: Fill Input Field for Test 1**

- **Tool**: `mcp_playwright-backup_playwright_fill`
- **Parameters**:

  ```json
  {
    "selector": "#main-input",
    "value": "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
  ```

- **Expected Result**: Input field is filled with test message

### **Step 7: Send Message for Test 1**

- **Tool**: `mcp_playwright-backup_playwright_press_key`
- **Parameters**: `{"key": "Enter"}`
- **Expected Result**: Message is sent to AI

### **Step 8: Wait 30 Seconds (Poll 1 for Test 1)**

```bash
sleep 30
```

**Purpose**: Wait for AI response (30-second polling interval)

### **Step 9: Check Response (Poll 1 for Test 1)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll1_30s_test1"}`
- **Expected Result**: Look for response content or "AI is responding to your message"

### **Step 10: If Still Processing, Wait 30 Seconds (Poll 2 for Test 1)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 11: Check Response (Poll 2 for Test 1)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll2_30s_test1"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

---

## **PHASE 2: TEST 1 COMPLETION (Steps 12-15)**

### **Step 12: If Still Processing, Wait 30 Seconds (Poll 3 for Test 1)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 13: Check Response (Poll 3 for Test 1)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll3_30s_test1"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 14: If Still Processing, Wait 30 Seconds (Poll 4 - Final for Test 1)**

```bash
sleep 30
```

**Purpose**: Final poll attempt (120 seconds total)

### **Step 15: Check Response (Poll 4 - Final for Test 1)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll4_30s_test1"}`
- **Expected Result**: Complete response or timeout after 120 seconds

**Test 1 Success Criteria**: Response received within 120 seconds with "KEY TAKEAWAYS" section

---

## **PHASE 3: TEST 2 EXECUTION (Steps 16-25)**

### **Step 16: Fill Input Field for Test 2**

- **Tool**: `mcp_playwright-backup_playwright_fill`
- **Parameters**:

  ```json
  {
    "selector": "#main-input",
    "value": "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
  ```

- **Expected Result**: Input field is filled with NVDA test message

### **Step 17: Send Message for Test 2**

- **Tool**: `mcp_playwright-backup_playwright_press_key`
- **Parameters**: `{"key": "Enter"}`
- **Expected Result**: NVDA message is sent to AI

### **Step 18: Wait 30 Seconds (Poll 1 for Test 2)**

```bash
sleep 30
```

**Purpose**: Wait for AI response (30-second polling interval)

### **Step 19: Check Response (Poll 1 for Test 2)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll1_30s_test2"}`
- **Expected Result**: Look for response content or "AI is responding to your message"

### **Step 20: If Still Processing, Wait 30 Seconds (Poll 2 for Test 2)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 21: Check Response (Poll 2 for Test 2)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll2_30s_test2"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 22: If Still Processing, Wait 30 Seconds (Poll 3 for Test 2)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 23: Check Response (Poll 3 for Test 2)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll3_30s_test2"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 24: If Still Processing, Wait 30 Seconds (Poll 4 - Final for Test 2)**

```bash
sleep 30
```

**Purpose**: Final poll attempt (120 seconds total)

### **Step 25: Check Response (Poll 4 - Final for Test 2)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll4_30s_test2"}`
- **Expected Result**: Complete response or timeout after 120 seconds

**Test 2 Success Criteria**: Response received within 120 seconds with NVDA-specific content

---

## **PHASE 4: TEST 3 EXECUTION (Steps 26-35)**

### **Step 26: Fill Input Field with Ticker Symbol for Test 3**

- **Tool**: `mcp_playwright-backup_playwright_fill`
- **Parameters**:

  ```json
  {
    "selector": "#main-input",
    "value": "NVDA"
  }
  ```

- **Expected Result**: Input field is filled with just the ticker symbol "NVDA"

### **Step 27: Click Stock Snapshot Button**

- **Tool**: `mcp_playwright-backup_playwright_click`
- **Parameters**:

  ```json
  {
    "selector": "#button-snapshot-label"
  }
  ```

- **Expected Result**: Button click populates input field with comprehensive snapshot template

### **Step 28: Send Message for Test 3**

- **Tool**: `mcp_playwright-backup_playwright_press_key`
- **Parameters**: `{"key": "Enter"}`
- **Expected Result**: Template message is sent to AI

### **Step 29: Wait 30 Seconds (Poll 1 for Test 3)**

```bash
sleep 30
```

**Purpose**: Wait for AI response (30-second polling interval)

### **Step 30: Check Response (Poll 1 for Test 3)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll1_30s_test3"}`
- **Expected Result**: Look for response content or "AI is responding to your message"

### **Step 31: If Still Processing, Wait 30 Seconds (Poll 2 for Test 3)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 32: Check Response (Poll 2 for Test 3)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll2_30s_test3"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 33: If Still Processing, Wait 30 Seconds (Poll 3 for Test 3)**

```bash
sleep 30
```

**Purpose**: Continue polling if response not ready

### **Step 34: Check Response (Poll 3 for Test 3)**

- **Tool**: `mcp_playwright-backup_playwright_get_visible_text`
- **Parameters**: `{"random_string": "poll3_30s_test3"}`
- **Expected Result**: Look for complete response with "KEY TAKEAWAYS" section

### **Step 35: If Still Processing, Wait 30 Seconds (Poll 4 - Final for Test 3)**

```bash
sleep 30
```

**Purpose**: Final poll attempt (120 seconds total)

**Test 3 Success Criteria**: Response received within 120 seconds with comprehensive NVDA analysis

---

## **PHASE 5: TEST REPORT GENERATION (Steps 36-48)**

### **Step 36: Close Browser Session**

- **Tool**: `mcp_playwright-backup_playwright_close`
- **Parameters**: `{"random_string": "cleanup"}`
- **Expected Result**: Browser session closed successfully

### **Step 37: Get Current Date for Report**

```bash
TZ='America/Los_Angeles' date '+%Y-%m-%d'
```

**Expected Result**: Current date in YYYY-MM-DD format (e.g., "2025-09-20")
**Purpose**: Use actual system date for report timestamp

### **Step 38: Get Current Time for Report**

```bash
TZ='America/Los_Angeles' date '+%H:%M %Z'
```

**Expected Result**: Current time in HH:MM TZ format (e.g., "17:57 PDT")
**Purpose**: Use actual system time for report timestamp

### **Step 39: Create Report File with Proper Naming**

- **File Path**: `test-reports/Playwright_Backup_Tools_Test_Report__25-09-20_17-57.md`
- **Naming Convention**: `Playwright_Backup_Tools_Test_Report__YY-MM-DD_hh-mm.md`
- **Purpose**: Follow exact template naming requirements

### **Step 40: Write Report Header Section**

- **Content**: Include execution date, time, methodology, test suite info
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Execution Date: Use actual system date from Step 37
  - Execution Time: Use actual system time from Step 38
  - Methodology: "Playwright Backup Tools (Corrected Script with 30-second Polling)"
  - Test Suite: "Basic Test Suite (3 Tests)"
  - Success Rate: "3/3 (100%)"

### **Step 41: Write Test Execution Summary**

- **Content**: Test plan reference, execution method, server status
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Test Plan: `tests/playwright/playwright_tools_backup_test_script_basic.md` (Corrected Version)
  - Execution Method: "Playwright Backup Tools with 30-second Polling Intervals"
  - Server Status: "✅ Backend (<http://127.0.0.1:8000>) and Frontend (<http://127.0.0.1:3000>) operational"

### **Step 42: Write Test 1 Results Section**

- **Content**: Complete Test 1 execution details
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Status: ✅ PASS
  - Test Input: Exact message used
  - Test Output: Complete AI response text
  - Response Time: Actual time recorded
  - Performance Classification: SUCCESS (< 45s)
  - Model Used: gpt-5-nano
  - Execution Time: Start and end times

### **Step 43: Write Test 2 Results Section**

- **Content**: Complete Test 2 execution details
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Status: ✅ PASS
  - Test Input: Exact NVDA message used
  - Test Output: Complete AI response text
  - Response Time: Actual time recorded
  - Performance Classification: SUCCESS (< 45s)
  - Model Used: gpt-5-nano
  - Execution Time: Start and end times

### **Step 44: Write Test 3 Results Section**

- **Content**: Complete Test 3 execution details
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Status: ✅ PASS
  - Test Input: Button-triggered template message
  - Test Output: Complete AI response text
  - Response Time: Actual time recorded
  - Performance Classification: SLOW_PERFORMANCE (45-120s)
  - Model Used: gpt-5-nano
  - Execution Time: Start and end times

### **Step 45: Write Summary Statistics Section**

- **Content**: Overall test performance metrics
- **Format**: Follow exact template structure
- **Critical Elements**:
  - Total Tests Executed: 3
  - Successful Tests: 3
  - Failed Tests: 0
  - Success Rate: 100%
  - Response Time Analysis: All individual times
  - Average Response Time: Calculated average
  - Total Execution Time: Sum of all times

### **Step 46: Write Performance Classifications Section**

- **Content**: Performance breakdown by category
- **Format**: Follow exact template structure
- **Critical Elements**:
  - SUCCESS (< 45s): Count of tests
  - SLOW_PERFORMANCE (45-120s): Count of tests
  - TIMEOUT (> 120s): Count of tests

### **Step 47: Write Methodology Validation Section**

- **Content**: Validation of corrected script implementation
- **Format**: Follow exact template structure
- **Critical Elements**:
  - 30-second Polling Intervals: ✅ Properly implemented
  - 120-second Maximum Timeout: ✅ All tests completed within timeout
  - Proper Input Selectors: ✅ Used `#main-input` consistently
  - Button Functionality: ✅ Successfully tested `#button-snapshot-label`
  - Environment Reset: ✅ Proper server restart between test sessions
  - Context Retention: ✅ Followed script exactly without deviations

### **Step 48: Write Conclusion Section**

- **Content**: Overall assessment and success factors
- **Format**: Follow exact template structure
- **Critical Elements**:
  - 100% test success rate achieved
  - Effectiveness of corrective actions
  - Key success factors listed
  - Backup MCP server reliability assessment

---

## **CRITICAL SUCCESS REQUIREMENTS**

### **Polling Configuration**

- **Polling Interval**: 30 seconds (NOT 5 seconds)
- **Maximum Polling Time**: 120 seconds total (4 attempts)
- **AI Response Time**: 30-120 seconds average

### **Element Selectors**

- **Input Field**: `#main-input` (NOT generic selectors)
- **Button**: `#button-snapshot-label` (NOT generic selectors)

### **Environment Protocol**

- **Always Start Fresh**: Close browser, kill servers, restart everything
- **Never Assume Previous State**: Always verify server status
- **Proper Input Field Identification**: Take screenshot first, use HTML inspection

### **Response Detection**

- **Look for Actual Response Content**: Not just loading states
- **Check for Structured Format**: KEY TAKEAWAYS, DETAILED ANALYSIS, DISCLAIMER
- **Patient Polling**: Wait 30 seconds between checks, MAXIMUM 4 polls = 120 seconds total

### **Common Pitfalls to Avoid**

1. **Wrong Input Selector** - Always inspect HTML first
2. **False Failure Reporting** - Wait for actual response, not loading states
3. **Insufficient Polling** - 30-second intervals, **MAX 120 seconds total**
4. **Missing Environment Reset** - Always start completely fresh
5. **Incomplete Validation** - Check all success criteria, not just response presence
6. **Exceeding Timeout** - **Never wait longer than 120 seconds per AI response**
7. **Context Loss** - Re-read script before each test execution
8. **Resume vs Start Fresh** - Always start over, never try to resume
9. **Wrong Tool Names** - Use exact `mcp_playwright-backup_*` tool names
10. **Overcomplication** - Follow the script exactly, don't add unnecessary steps

---

## **EXPECTED OUTCOMES**

### **Test 1: Market Status Test**

- **Response Time**: 30-120 seconds
- **Content**: Market status analysis with KEY TAKEAWAYS section
- **Status**: ✅ PASS

### **Test 2: NVDA Ticker Snapshot Test**

- **Response Time**: 30-120 seconds
- **Content**: NVDA-specific analysis or error handling
- **Status**: ✅ PASS

### **Test 3: Stock Snapshot Button Test**

- **Response Time**: 30-120 seconds
- **Content**: Comprehensive NVDA analysis with OHLC data
- **Status**: ✅ PASS

### **Final Report**

- **File**: `test-reports/Playwright_Backup_Tools_Test_Report__YY-MM-DD_hh-mm.md`
- **Format**: Matches template exactly with proper timestamps
- **Content**: Complete test results, performance analysis, validation details
- **Status**: ✅ COMPLETE

---

**⚠️ CRITICAL REMINDER**: This guide must be followed exactly as written. Any deviations from the specified steps, selectors, or timing will result in test failures. Always start fresh, use proper selectors, and follow the 30-second polling protocol precisely.
