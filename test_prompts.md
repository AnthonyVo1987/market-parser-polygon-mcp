# Standardized Test Prompts with Playwright GUI Testing Procedure

**Document Purpose:** This is the single source of truth for all
standardized test prompts used in Market Parser testing. All AI agents
and testing procedures MUST use these exact prompts to ensure
consistent, quick responses and avoid false failures.

**Target Audience:** AI Coding Agents, Test Specialists, and anyone
performing Market Parser testing
**Expected Outcome:** Consistent 20-30 second response times with minimal
tool calls (optimized performance with 60s max timeout per test)
**Methodology:** Quick response prompts designed to leverage GPT-5 model
efficiency and quick response optimization system

---

## CRITICAL TESTING RULES

**MANDATORY REQUIREMENTS:**

- ✅ Use ONLY these prompts for testing
- ✅ Copy prompts EXACTLY as written
- ✅ Expected response time: 20-30 seconds (optimized performance)
- ✅ Max timeout per test: 60 seconds (30s breathing room)
- ✅ Response validation: MUST detect "Response Time" in AI response message
- ❌ DO NOT create custom prompts
- ❌ DO NOT modify these prompts
- ❌ DO NOT use complex, open-ended queries
- ❌ DO NOT accept "Loading" messages as valid responses

---

## Quick Response Test Prompts

### 1. Market Status Query

#### Test Prompt 1: Market Status Query

"What the current Market Status?"

### 2. Single Stock Snapshot

#### Test Prompt 2: Single Stock Snapshot Price

"Stock Snapshot: NVDA"

### 3. Full Market Snapshot Price

#### Test Prompt 3: Full Market Snapshot

"Stock Snapshot: SPY, QQQ, IWM"

### 4. Closing Price Query

#### Test Prompt 4: Closing Price Query

"What was closing price today for: SPY"

### 5. Performance Analysis

#### Test Prompt 5: Performance Analysis

"Current weekly Price Change $ and % for: SPY"

### 6. Support & Resistance

#### Test Prompt 6: Support & Resistance

"Support & Resistance Levels: SPY"

### 7. Technical Analysis

#### Test Prompt 7: Technical Analysis

"Technical Analysis: SPY"

---

## 🎭 PLAYWRIGHT GUI TESTING PROCEDURE

### ⚠️ CRITICAL PREREQUISITES

**BEFORE STARTING ANY TESTS, AI AGENT MUST:**

1. **Start Backend Server Manually** (REQUIRED)

   ```bash
   uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Start Frontend Server Manually** (REQUIRED)

   ```bash
   npm run frontend:dev
   ```

3. **Keep Both Servers Running** (MANDATORY)
   - Backend server MUST remain running on port 8000
   - Frontend server MUST remain running on port 3000
   - Both servers MUST be running throughout the entire test session
   - NO startup scripts allowed - manual server management only

4. **Verify Server Status** (BEFORE TESTING)

   ```bash
   # Both commands MUST return 200 OK
   curl -s http://127.0.0.1:8000/health
   curl -s http://127.0.0.1:3000
   ```

**❌ TESTING WILL FAIL IF:**

- Backend server is not running
- Frontend server is not running
- Either server stops during testing
- Servers are started using startup scripts

### Step-by-Step Test Execution

#### **PHASE 1: PREPARATION & SETUP**

1. **Environment Verification**

   ```bash
   # Check if application is running
   curl -s http://127.0.0.1:8000/health || echo "Backend not running"
   curl -s http://127.0.0.1:3000 || echo "Frontend not running"
   ```

2. **MANDATORY: Start Backend Server Manually**

   ```bash
   # AI Agent MUST manually start the backend server
   # Run this command in a separate terminal/background process
   uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload
   
   # Keep this process running in the background
   # Do NOT close this terminal/process during testing
   ```

3. **MANDATORY: Start Frontend Server Manually**

   ```bash
   # AI Agent MUST manually start the frontend server
   # Run this command in a separate terminal/background process
   npm run frontend:dev
   
   # Keep this process running in the background
   # Do NOT close this terminal/process during testing
   ```

4. **CRITICAL: Verify Both Servers Are Running**

   ```bash
   # Backend health check - MUST return 200 OK
   curl -s http://127.0.0.1:8000/health
   echo "Backend status: $?"
   
   # Frontend availability check - MUST return 200 OK
   curl -s http://127.0.0.1:3000
   echo "Frontend status: $?"
   
   # Both servers MUST be running before proceeding to testing
   ```

5. **Server Status Validation**

   ```bash
   # Verify backend is responding with proper JSON
   curl -s http://127.0.0.1:8000/health | jq .
   
   # Verify frontend is serving content
   curl -s http://127.0.0.1:3000 | head -20
   
   # Check if both servers are running on correct ports
   netstat -tlnp | grep -E ":(8000|3000)"
   ```

#### **PHASE 2: PLAYWRIGHT GUI TESTING EXECUTION**

6. **CRITICAL: Pre-Test Server Validation**

   ```bash
   # MANDATORY: Verify both servers are still running before testing
   # This check MUST pass before proceeding to Playwright testing
   
   # Backend validation
   if ! curl -s http://127.0.0.1:8000/health > /dev/null; then
     echo "❌ CRITICAL ERROR: Backend server is not running!"
     echo "   You MUST start the backend server first:"
     echo "   uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload"
     exit 1
   fi
   
   # Frontend validation
   if ! curl -s http://127.0.0.1:3000 > /dev/null; then
     echo "❌ CRITICAL ERROR: Frontend server is not running!"
     echo "   You MUST start the frontend server first:"
     echo "   npm run frontend:dev"
     exit 1
   fi
   
   echo "✅ Both servers are running - proceeding with Playwright testing"
   ```

7. **Initialize Playwright Session**

   ```javascript
   // Start Playwright browser session
   await playwright_navigate({
     url: "http://127.0.0.1:3000",
     browserType: "chromium",
     headless: false,
     width: 1280,
     height: 720
   });
   ```

8. **Take Initial Screenshot**

   ```javascript
   // Capture initial application state
   await playwright_screenshot({
     name: "initial_application_state",
     fullPage: true,
     savePng: true
   });
   ```

9. **Verify GUI Elements**

   ```javascript
   // Check if main UI elements are present
   const visibleText = await playwright_get_visible_text();
   console.log("Initial page content:", visibleText);
   ```

#### **PHASE 3: EXECUTE STANDARDIZED TEST PROMPTS**

**For EACH of the 7 test prompts, follow this exact procedure:**

10. **Send Test Prompt**

    ```javascript
    // Navigate to chat interface and input prompt
    await playwright_fill({
      selector: "input[type='text'], textarea, [contenteditable='true']",
      value: "[EXACT_PROMPT_FROM_LIST_BELOW]"
    });

    await playwright_click({
      selector: "button[type='submit'], button:contains('Send'), .send-button"
    });
    ```

11. **First Response Check (30 seconds)**

    ```javascript
    // Wait 30 seconds for initial response
    await new Promise(resolve => setTimeout(resolve, 30000));
    
    // Check for response
    const responseText = await playwright_get_visible_text();
    
    // CRITICAL: Check if "Response Time" is present in the LATEST response
    // Look for the most recent "Response Time" text in the conversation
    const responseTimeMatches = responseText.match(/Response Time:\s*([\d.]+)\s*s/g);
    const latestResponseTime = responseTimeMatches ? responseTimeMatches[responseTimeMatches.length - 1] : null;
    
    if (latestResponseTime) {
      // SUCCESS: AI responded with response time - move to next test
      console.log("✅ Test PASSED - Response Time detected:", latestResponseTime);
      await playwright_screenshot({
        name: "test_[N]_[PROMPT_NAME]_response",
        fullPage: true
      });
    } else if (responseText.includes("Loading") || responseText.includes("thinking") || responseText.includes("Sending message")) {
      // AI still thinking - proceed to second check
      console.log("⏳ AI still thinking - waiting for second check");
    } else {
      // Unexpected response - log and continue
      console.log("⚠️ Unexpected response format");
    }
    ```

12. **Second Response Check (30 seconds) - ONLY if first check failed**

    ```javascript
    // Wait additional 30 seconds (total 60s max)
    await new Promise(resolve => setTimeout(resolve, 30000));
    
    // Final response check
    const finalResponseText = await playwright_get_visible_text();
    
    // Check for the most recent "Response Time" text in the conversation
    const responseTimeMatches = finalResponseText.match(/Response Time:\s*([\d.]+)\s*s/g);
    const latestResponseTime = responseTimeMatches ? responseTimeMatches[responseTimeMatches.length - 1] : null;
    
    if (latestResponseTime) {
      // SUCCESS: AI responded with response time
      console.log("✅ Test PASSED - Response Time detected after 60s:", latestResponseTime);
      await playwright_screenshot({
        name: "test_[N]_[PROMPT_NAME]_response",
        fullPage: true
      });
    } else {
      // FAILURE: No valid response within 60s timeout
      console.log("❌ Test FAILED - No Response Time detected within 60s");
      await playwright_screenshot({
        name: "test_[N]_[PROMPT_NAME]_timeout",
        fullPage: true
      });
    }
    ```

#### **PHASE 4: RESPONSE VALIDATION CRITERIA**

**CRITICAL VALIDATION RULES:**

- ✅ **PASS CRITERIA**: Response MUST contain NEW "Response Time" text (not from previous tests)
- ✅ **DETECTION LOGIC**: Use regex to find the LATEST "Response Time: X.XXX s" in conversation
- ❌ **FAIL CRITERIA**: "Loading" messages are NOT valid responses
- ❌ **FAIL CRITERIA**: Empty responses are NOT valid
- ❌ **FAIL CRITERIA**: Error messages without "Response Time" are NOT valid
- ❌ **FAIL CRITERIA**: OLD "Response Time" from previous tests are NOT valid
- ⏰ **TIMEOUT**: 60 seconds maximum per test (30s + 30s checks)

#### **PHASE 5: REPORT GENERATION**

13. **Generate Test Report**

    ```javascript
    // Create comprehensive test report
    const testReport = {
      timestamp: new Date().toISOString(),
      summary: {
        totalTests: 7,
        passed: passedTests,
        failed: failedTests,
        successRate: (passedTests / 7) * 100
      },
      performance: {
        averageResponseTime: calculateAverageResponseTime(),
        maxTimeout: 60,
        responseValidation: "Response Time detection required"
      },
      screenshots: generateScreenshotList(),
      consoleLogs: await playwright_console_logs({ type: "all" })
    };
    ```

14. **Save Test Report**

    ```bash
    # Save the comprehensive test report
    echo "$testReport" > test-reports/gui_playwright_test_report_$(date +%Y%m%d_%H%M%S).json
    ```

### Performance Classification (Updated)

- **SUCCESS:** < 30 seconds (excellent performance with optimization)
- **GOOD:** 30-45 seconds (good performance, within expected range)
- **SLOW_PERFORMANCE:** 45-60 seconds (acceptable but investigate optimization)
- **TIMEOUT:** > 60 seconds (failure - test fails)

### Response Validation Requirements

- **MUST DETECT**: "Response Time" text in AI response message
- **MUST IGNORE**: "Loading" messages, "thinking" indicators
- **MUST REJECT**: Empty responses, error messages without response time
- **VALIDATION LOGIC**: Only responses containing "Response Time" are considered valid

---

## 🎯 TEST EXECUTION SUMMARY

### **Complete 7-Prompt Test Sequence**

1. **Test 1**: "What the current Market Status, Date, & Time: Open, Closed, After-Hours, Pre-market, Overnight?"
2. **Test 2**: "Single Stock Snapshot Price NVDA"
3. **Test 3**: "Full Market Snapshot Price: SPY, QQQ, IWM"
4. **Test 4**: "GME closing price today"
5. **Test 5**: "SOUN Price performance this week"
6. **Test 6**: "NVDA Price Support & Resistance Levels"
7. **Test 7**: "SPY Price Technical Analysis"

### **Expected Test Duration**

- **Per Test**: 30-60 seconds (30s + 30s max)
- **Total Duration**: 3.5-7 minutes (7 tests × 30-60s)
- **Server Setup Time**: 2-3 minutes (manual server startup)
- **Total Time**: 5.5-10 minutes

### **Success Criteria**

- ✅ **7/7 tests must pass** (100% success rate)
- ✅ **Each test must detect "Response Time"** in AI response
- ✅ **No "Loading" messages accepted** as valid responses
- ✅ **All tests complete within 60s timeout** per test
- ✅ **Both servers MUST remain running** throughout entire test session

### **Manual Server Management Requirements**

- 🔴 **NO startup scripts allowed** - manual server management only
- 🔴 **Backend server MUST be started manually** before testing
- 🔴 **Frontend server MUST be started manually** before testing
- 🔴 **Both servers MUST remain running** during entire test session
- 🔴 **Server validation checks** before each test phase

---

## Integration Notes

This file is referenced by:

- `CLAUDE.md` - Main project guidance
- `AGENTS.md` - Agent instructions
- `README.md` - Project documentation
- `tests/playwright/mcp_test_script_basic.md` - MCP testing guide
- `tests/playwright/complete_test_execution_guide.md` - Complete test
  guide
- `tests/playwright/UI_complete_test_execution_guide.md` - UI test guide
- All other test documentation files

**Last Updated:** 2025-01-28
**Version:** 3.0
**Status:** Production Ready with Optimized Performance & Response Validation
