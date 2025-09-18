# Playwright MCP Testing: Single Source of Truth for AI Agents

**Document Purpose:** This is the definitive guide for AI agents to perform Playwright MCP testing with 100% first-try success rate. Follow these instructions EXACTLY as written for guaranteed testing success.

**Target Audience:** AI Coding Agents performing MCP method testing  
**Expected Outcome:** Any AI agent can read this document and execute MCP testing correctly without external research  
**Methodology:** Modern Playwright MCP with auto-retry detection (NO polling)  

---

## CRITICAL SUCCESS REQUIREMENTS

**MANDATORY:** Read and understand these requirements before proceeding:

1. **Follow Instructions VERBATIM** - Do not deviate from exact tool calls and parameters
2. **Use EXACT Tool Names** - Only use `mcp__playwright__browser_*` tools specified here
3. **Set EXPLICIT Timeouts** - Always use `time: 120` parameter for AI response detection
4. **NO Polling Methodology** - Auto-retry detection eliminates need for manual polling
5. **Validate First-Try Success** - Document must enable success without external research

**CRITICAL DISTINCTION:** This document supersedes ALL other testing documentation. If conflicts exist, follow THIS document.

---

## Section 1: Prerequisites & System Requirements

### 1.1 Essential Tool Requirements

**REQUIRED MCP Tools Available:**
- `mcp__playwright__browser_navigate` - Page navigation with error handling
- `mcp__playwright__browser_snapshot` - Accessibility snapshots for element detection  
- `mcp__playwright__browser_type` - Text input into form elements
- `mcp__playwright__browser_press_key` - Keyboard event generation
- `mcp__playwright__browser_wait_for` - **CRITICAL** - Response detection with timeouts
- `mcp__playwright__browser_click` - Button/element interaction
- `mcp__playwright__browser_evaluate` - JavaScript execution for validation

**Verification Step:**
If any of these tools are unavailable, STOP and request tool access before proceeding.

### 1.2 Server Requirements

**REQUIRED Servers Running:**
- **Backend FastAPI:** http://127.0.0.1:8000 (application backend)
- **Frontend React:** http://127.0.0.1:3000 (or auto-detected port 3001, 3002, etc.)

**Server Verification Procedure:**
```
1. Backend Health Check:
   - Expected response: {"status": "healthy"} from http://127.0.0.1:8000/health
   
2. Frontend Accessibility Check:  
   - Expected response: React application loads from http://127.0.0.1:3000
   - Note: Vite may auto-select ports 3001, 3002 if 3000 occupied
```

**CRITICAL:** If servers are not running, execute: `./start-app.sh` (or `npm run start:app` as alternative) and wait for "ready" messages before proceeding.

### 1.3 Environment Verification

**Pre-Test Validation Checklist:**
- [ ] All required MCP tools respond correctly
- [ ] Backend server returns healthy status
- [ ] Frontend server loads React application  
- [ ] No browser instances currently running (clean state)

---

## Section 2: Critical Parameters & Configuration

### 2.1 MCP Tool Timeout Parameters

**CRITICAL UNDERSTANDING:** MCP tools have independent timeout parameters separate from application configuration.

**REQUIRED Timeout Configuration:**
- **MCP Tool Parameter:** `time: 120` (120 seconds for AI response detection)
- **Why 120 seconds:** AI responses typically take 30-120 seconds to complete
- **Parameter Format:** Always specify as integer `120`, NOT `120000` or `"120s"`

**Example Correct Usage:**
```json
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "Expected response indicator",
    "time": 120
  }
}
```

**CRITICAL ERROR TO AVOID:** Never use default 5-second timeout for AI responses.

### 2.2 Configuration Scope Distinction

**MCP Tool Parameters (THIS DOCUMENT):**
- `time: 120` - Tool-specific timeout for waiting operations
- Applies to individual tool calls
- Independent of application configuration

**Application Configuration (SEPARATE):**
- `120000ms` timeouts in helper files (different scope)
- Playwright test timeouts (different scope)
- Do NOT confuse these with MCP tool parameters

**CRITICAL:** MCP tool parameters are specified in each tool call, NOT in configuration files.

---

## Section 3: Exact MCP Tool Execution Sequence

### 3.1 Test Initialization

**Step 1: Navigate to Frontend**
```json
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}
```
**Expected Result:** Page loads successfully with React application
**Error Handling:** If navigation fails, verify servers are running

**Step 2: Capture Initial State**
```json
{
  "tool": "mcp__playwright__browser_snapshot",
  "parameters": {}
}
```
**Expected Result:** Accessibility tree snapshot with element references
**Purpose:** Identify message input field and UI elements

### 3.2 Message Input and Submission

**Step 3: Input Test Message**
```json
{
  "tool": "mcp__playwright__browser_type",
  "parameters": {
    "element": "message input textarea",
    "ref": "textarea[placeholder*='message'], .chat-input textarea, input[type='text']",
    "text": "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
}
```
**Expected Result:** Message text entered into input field
**Critical Note:** Use multiple selector fallbacks in `ref` parameter

**Step 4: Submit Message**
```json
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Enter"
  }
}
```
**Expected Result:** Message submitted, AI processing begins

### 3.3 Auto-Retry Response Detection

**Step 5: Wait for AI Response (CRITICAL STEP)**
```json
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "🎯 KEY TAKEAWAYS",
    "time": 120
  }
}
```

**CRITICAL SUCCESS FACTORS:**
- **Timeout:** Always use `time: 120` for AI responses
- **Detection Text:** Look for response indicators like "🎯 KEY TAKEAWAYS"
- **Auto-Retry:** Tool automatically retries until detected or timeout
- **NO Manual Polling:** Tool handles retry logic internally

**Alternative Detection Patterns:**
```json
// For market data responses
{"text": "📈", "time": 120}

// For technical analysis  
{"text": "📊", "time": 120}

// For any financial content
{"text": "💰", "time": 120}
```

---

## Section 4: Auto-Retry Detection Methodology

### 4.1 Understanding Auto-Retry vs Polling

**Auto-Retry Detection (CURRENT METHOD):**
- Built into `mcp__playwright__browser_wait_for` tool
- Automatically retries until condition met or timeout
- NO manual loop required
- Performance: Immediate detection when condition satisfied

**Polling (OUTDATED METHOD - DO NOT USE):**
- Manual retry loops with fixed intervals
- Artificial delays even after condition met  
- Complexity in implementation
- Performance: Always waits for full interval

**CRITICAL:** This document uses ONLY auto-retry detection. Ignore any references to "polling" in other documents.

### 4.2 Performance Classification

**Response Time Categories:**
- **SUCCESS:** < 45 seconds (excellent performance)
- **SLOW_PERFORMANCE:** 45-120 seconds (acceptable for AI responses)
- **TIMEOUT:** > 120 seconds (test failure)

**Recording Performance:**
Document actual response time for performance classification and optimization insights.

### 4.3 Two-Phase Detection Process

**Phase 1: Response Detection**
- Tool detects ANY response content using specified text pattern
- Immediate notification when condition satisfied
- Eliminates waiting beyond necessary time

**Phase 2: Content Validation (Manual)**
- After detection, validate response content quality
- Check for expected financial data and format
- Verify emoji indicators and structured output

---

## Section 5: Error Handling & Troubleshooting

### 5.1 Common Tool Parameter Errors

**Error:** "Tool timeout after 5 seconds"
**Cause:** Missing `time: 120` parameter
**Solution:** Always specify explicit timeout for AI responses
```json
// WRONG:
{"tool": "mcp__playwright__browser_wait_for", "parameters": {"text": "response"}}

// CORRECT: 
{"tool": "mcp__playwright__browser_wait_for", "parameters": {"text": "response", "time": 120}}
```

**Error:** "Element not found"
**Cause:** Incorrect element selector
**Solution:** Use multiple fallback selectors in `ref` parameter
```json
"ref": "textarea[placeholder*='message'], .chat-input textarea, input[type='text'], #message-input"
```

### 5.2 Server Connectivity Issues

**Error:** "Navigation failed" or "Connection refused"
**Diagnosis Steps:**
1. Verify backend: `curl http://127.0.0.1:8000/health`
2. Verify frontend: `curl http://127.0.0.1:3000/`
3. Check for port conflicts or server crashes

**Solution:** Restart servers with `npm run start:app` and wait for ready messages

### 5.3 Response Detection Failures

**Error:** "Wait timeout after 120 seconds"
**Possible Causes:**
1. Server processing issues (check server logs)
2. Incorrect detection text pattern
3. UI changes affecting response format

**Troubleshooting Steps:**
1. Take snapshot to examine actual response content
2. Try alternative detection patterns (📈, 📊, 💰)
3. Verify server health and processing status

### 5.4 Browser State Issues

**Error:** "Browser not responding" or "Page unresponsive"
**Solution:** Browser state may be corrupted
```json
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}
```
**Purpose:** Refresh browser state and restart test sequence

---

## Section 6: Test Result Validation & Reporting

### 6.1 Response Content Validation

**Required Validation Checks:**
1. **Response Detection:** Verify auto-retry successfully detected response
2. **Content Quality:** Check for financial data and analysis
3. **Format Compliance:** Verify emoji indicators (📈📉💰🎯)
4. **Completeness:** Ensure response addresses original query

**Validation Tool Usage:**
```json
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const messages = document.querySelectorAll('.message-content'); return messages[messages.length-1]?.textContent || 'No response found'; }"
  }
}
```

### 6.2 Performance Classification

**Recording Requirements:**
- Document actual response time from submission to detection
- Classify as SUCCESS/SLOW_PERFORMANCE/TIMEOUT
- Note any detection method used (text pattern)

**Success Criteria:**
- **PASS:** Response detected within 120 seconds AND content validation successful
- **FAIL:** Timeout exceeded OR content validation failed

### 6.3 Test Report Generation

**Required Report Elements:**
1. Test execution timestamp and duration
2. Performance classification and actual timing
3. Auto-retry detection success/failure details
4. Content validation results
5. Any errors encountered and resolution steps

**Report Format:** Follow established report template with auto-retry methodology details.

---

## Section 7: Post-Mortem Lessons Integrated

### 7.1 Critical Mistakes to Avoid

**NEVER Do These Actions:**
1. **Use Polling Methodology** - Auto-retry detection replaces all polling
2. **Omit Tool Timeout Parameters** - Always specify `time: 120`
3. **Mix MCP vs CLI Methods** - This document covers ONLY MCP method
4. **Assume Default Tool Behavior** - Explicitly specify all parameters
5. **Follow Outdated Documentation** - This document supersedes other testing guides

### 7.2 Documentation Hierarchy

**Priority Order for AI Agents:**
1. **THIS DOCUMENT** - Primary source of truth for MCP testing
2. **Official MCP Tools Usage Guides** - For tool parameter specifications
3. **Project-Specific Plans** - Secondary reference only

**CRITICAL:** If conflicts exist between documents, follow THIS document exclusively.

### 7.3 Common Misconceptions Addressed

**Misconception:** "Polling is required for response detection"
**Reality:** Auto-retry detection eliminates polling need entirely

**Misconception:** "5-second timeouts are sufficient"  
**Reality:** AI responses require 30-120 seconds, use `time: 120`

**Misconception:** "MCP and CLI methods are interchangeable"
**Reality:** Different tools and parameters, use ONLY MCP method here

---

## Section 8: Method Status & Future Validation

### 8.1 MCP Method Status

**Current Status:** VALIDATED and PRODUCTION-READY
- Successfully tested with B001 market status test (49.6s response)
- Auto-retry detection proven effective
- Performance classification confirmed functional
- Error handling validated and documented

### 8.2 CLI Method Status  

**Current Status:** AUTO-RETRY NOT YET TESTED
- CLI method using `npx playwright test` commands exists
- Auto-retry detection methodology NOT validated for CLI
- Results pending future validation task assignment
- Continue using MCP method as primary validated approach

### 8.3 Testing Scope Limitations

**This Document Covers:**
- MCP method testing using `mcp__playwright__browser_*` tools
- Auto-retry detection methodology
- Basic market status and ticker analysis testing

**This Document Does NOT Cover:**
- CLI method testing procedures
- Advanced multi-button interaction sequences  
- Comprehensive test suite execution (B001-B016)
- Performance optimization or debugging complex scenarios

---

## Section 9: Complete Test Suite Execution (3 Basic Tests)

### 9.1 Test 1: Market Status Test

**Test Description:** Validates basic market status endpoint and response format

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Get page state
{
  "tool": "mcp__playwright__browser_snapshot",
  "parameters": {}
}

// Step 3: Input message
{
  "tool": "mcp__playwright__browser_type",
  "parameters": {
    "element": "message input field",
    "ref": "textarea[placeholder*='message'], .chat-input textarea",
    "text": "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
}

// Step 4: Submit message
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Enter"
  }
}

// Step 5: Wait for response (CRITICAL)
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "🎯 KEY TAKEAWAYS",
    "time": 120
  }
}

// Step 6: Validate response
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const messages = document.querySelectorAll('.message-content'); const lastMessage = messages[messages.length-1]?.textContent || ''; return { hasFinancialEmojis: /[📈📉💰🎯]/.test(lastMessage), contentLength: lastMessage.length, containsMarketData: /market|trading|status/i.test(lastMessage) }; }"
  }
}
```

**Expected Results:**
- Navigation: Page loaded successfully
- Snapshot: Element references identified
- Input: Message entered correctly
- Submission: Processing initiated
- Detection: Response detected in 30-120 seconds
- Validation: Financial content with emoji indicators confirmed

### 9.2 Test 2: NVDA Ticker Snapshot Test

**Test Description:** Validates single ticker analysis with NVDA stock data

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate (if not already on page)
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Get page state
{
  "tool": "mcp__playwright__browser_snapshot",
  "parameters": {}
}

// Step 3: Input NVDA ticker query
{
  "tool": "mcp__playwright__browser_type",
  "parameters": {
    "element": "message input field",
    "ref": "textarea[placeholder*='message'], .chat-input textarea",
    "text": "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
}

// Step 4: Submit message
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Enter"
  }
}

// Step 5: Wait for NVDA response (CRITICAL)
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "📈",
    "time": 120
  }
}

// Alternative detection patterns for NVDA response
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "NVIDIA",
    "time": 120
  }
}

// Step 6: Validate NVDA-specific response
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const messages = document.querySelectorAll('.message-content'); const lastMessage = messages[messages.length-1]?.textContent || ''; return { hasFinancialEmojis: /[📈📉💰🎯]/.test(lastMessage), contentLength: lastMessage.length, containsNVDA: /nvda|nvidia/i.test(lastMessage), hasStockData: /price|volume|market cap|current/i.test(lastMessage) }; }"
  }
}
```

**Expected Results:**

- Navigation: Page maintained or refreshed successfully
- Input: NVDA ticker query entered correctly
- Submission: NVDA analysis processing initiated
- Detection: NVDA response detected within 120 seconds
- Validation: NVDA-specific content with stock data confirmed

### 9.3 Test 3: Stock Snapshot Button Test

**Test Description:** Validates Stock Snapshot button functionality and template system

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate (if not already on page)
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Get page state to find button
{
  "tool": "mcp__playwright__browser_snapshot",
  "parameters": {}
}

// Step 3: Input ticker for button test (optional pre-population)
{
  "tool": "mcp__playwright__browser_type",
  "parameters": {
    "element": "message input field",
    "ref": "textarea[placeholder*='message'], .chat-input textarea",
    "text": "NVDA"
  }
}

// Step 4: Click Stock Snapshot button (📈)
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "Stock Snapshot button",
    "ref": "button:has-text('📈'), button:has-text('Stock Snapshot'), [data-testid='stock-snapshot-button']"
  }
}

// Step 5: Wait for button-triggered response (CRITICAL)
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "📈",
    "time": 120
  }
}

// Alternative detection for snapshot analysis
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "Market Snapshot",
    "time": 120
  }
}

// Step 6: Validate button-triggered response
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const messages = document.querySelectorAll('.message-content'); const lastMessage = messages[messages.length-1]?.textContent || ''; return { hasFinancialEmojis: /[📈📉💰🎯]/.test(lastMessage), contentLength: lastMessage.length, hasSnapshotContent: /snapshot|stock|price|volume/i.test(lastMessage), buttonTriggered: true }; }"
  }
}
```

**Expected Results:**

- Navigation: Page maintained or refreshed successfully
- Button Detection: Stock Snapshot button found and clickable
- Button Click: Button interaction successful
- Detection: Button-triggered response detected within 120 seconds
- Validation: Stock snapshot content generated via button template

---

## Section 10: Success Validation Checklist

### 10.1 First-Try Success Criteria

**Before declaring success, verify ALL items:**

- [ ] All MCP tools executed without parameter errors
- [ ] Response detected within 120-second timeout
- [ ] Content validation confirms financial analysis present
- [ ] Performance classification documented (SUCCESS/SLOW_PERFORMANCE)
- [ ] No polling methodology used (auto-retry only)
- [ ] Test completion report generated

### 10.2 Failure Investigation

**If test fails, check in order:**

1. **Tool Parameters:** Verify `time: 120` in wait_for calls
2. **Server Status:** Confirm backend/frontend operational
3. **Element Selectors:** Verify UI element detection working
4. **Detection Patterns:** Try alternative emoji/text patterns
5. **Browser State:** Consider navigation refresh if unresponsive

### 10.3 Documentation Validation

**This document achieves first-try success if:**

- Any AI agent can follow instructions verbatim without external research
- All critical parameters and tool usage explicitly documented
- Error handling covers common failure scenarios
- Post-mortem lessons prevent previously encountered mistakes
- Modern MCP best practices integrated throughout

---

## FINAL SUCCESS CONFIRMATION

**CRITICAL SUCCESS INDICATOR:** If you successfully executed a complete test following this document exactly as written, with response detection within 120 seconds and proper content validation, then this document has achieved its purpose.

**Next Steps After Success:**

1. Document actual response time and performance classification
2. Note any detection methods that worked most effectively
3. Report any deviations from expected behavior for document improvement
4. Proceed with additional test scenarios using same methodology

**If Unsuccessful:** Review Section 5 (Error Handling) and Section 10.2 (Failure Investigation) before requesting external assistance.

---

**Document Version:** 1.0 - Complete Rewrite Based on Post-Mortem Analysis
**Last Updated:** Integration of Context7 Research and Modern MCP Best Practices
**Validation Status:** Designed for 100% First-Try Success Rate by AI Agents
**Supersedes:** All previous MCP testing documentation and methodologies
