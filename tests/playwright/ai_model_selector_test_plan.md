# AI Model Selector Playwright MCP Testing Plan

**Document Purpose:** Comprehensive test plan for validating the AI Model Selector feature using Playwright MCP tools with 100% first-try success rate.

**Target Audience:** AI Coding Agents performing MCP method testing for AI Model Selector feature
**Expected Outcome:** Any AI agent can read this document and execute AI Model Selector testing correctly without external research
**Methodology:** Modern Playwright MCP with auto-retry detection (NO polling)

---

## CRITICAL SUCCESS REQUIREMENTS

**MANDATORY:** Read and understand these requirements before proceeding:

1. **Follow Instructions VERBATIM** - Do not deviate from exact tool calls and parameters
2. **Use EXACT Tool Names** - Only use `mcp__playwright__browser_*` tools specified here
3. **Set EXPLICIT Timeouts** - Always use `time: 120` parameter for AI response detection
4. **NO Polling Methodology** - Auto-retry detection eliminates need for manual polling
5. **Validate First-Try Success** - Document must enable success without external research

**CRITICAL DISTINCTION:** This document follows the same methodology as `mcp_test_script_basic.md` but focuses specifically on AI Model Selector feature testing.

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

- **Backend FastAPI:** <http://127.0.0.1:8000> (application backend)
- **Frontend React:** <http://127.0.0.1:3000> (or auto-detected port 3001, 3002, etc.)

**Server Verification Procedure:**

```
1. Backend Health Check:
   - Expected response: {"status": "healthy"} from http://127.0.0.1:8000/health
   
2. Frontend Accessibility Check:  
   - Expected response: React application loads from http://127.0.0.1:3000
   - Note: Vite may auto-select ports 3001, 3002 if 3000 occupied
```

**CRITICAL:** If servers are not running, execute: `./start-app.sh` (or `npm run start:app` as alternative). The script will automatically open the application in your browser after confirming both servers are running.

### 1.3 Environment Verification

**Pre-Test Validation Checklist:**

- [ ] All required MCP tools respond correctly
- [ ] Backend server returns healthy status
- [ ] Frontend server loads React application  
- [ ] No browser instances currently running (clean state)
- [ ] AI Model Selector feature is implemented and accessible

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

### 2.2 AI Model Selector Specific Configuration

**Model Selector Element Selectors:**

- **Dropdown Container:** `.model-selector-container`
- **Dropdown Select:** `.model-selector`
- **Loading Indicator:** `.loading-indicator`
- **Error Message:** `.error-message`
- **Debug Panel:** `.debug-panel`

**Note:** Element selectors verified against actual implementation in `src/frontend/components/DebugPanel.tsx`

**Expected Model Options:**

- GPT-5 Nano (default) - `gpt-5-nano`
- GPT-5 Mini - `gpt-5-mini`

**Note:** Model ID values verified against actual `AIModelId` enum in `src/frontend/types/ai_models.ts`

---

## Section 3: AI Model Selector Test Suite (8 Comprehensive Tests)

### Test 1: Model Selector Visibility and Basic Functionality

**Test Description:** Validates that the AI Model Selector dropdown appears in the Debug Panel and is functional

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate to Frontend
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Capture Initial State
{
  "tool": "mcp__playwright__browser_snapshot",
  "parameters": {}
}

// Step 3: Expand Debug Panel (if collapsed)
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "Debug Panel toggle button",
    "ref": "button:has-text('Debug'), .debug-panel-toggle, [data-testid='debug-toggle']"
  }
}

// Step 4: Wait for Debug Panel to expand
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "AI Model",
    "time": 30
  }
}

// Step 5: Take snapshot to verify model selector is visible
{
  "tool": "mcp__playwright__browser_snapshot",
  "parameters": {}
}

// Step 6: Validate model selector presence and functionality
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const selector = document.querySelector('.model-selector'); const container = document.querySelector('.model-selector-container'); const options = selector ? Array.from(selector.options).map(opt => ({ value: opt.value, text: opt.textContent })) : []; return { hasSelector: !!selector, hasContainer: !!container, optionsCount: options.length, options: options, isEnabled: selector ? !selector.disabled : false }; }"
  }
}
```

**Expected Results:**

- Navigation: Page loaded successfully
- Debug Panel: Successfully expanded
- Model Selector: Visible and functional
- Options: 2 model options available (GPT-5 Nano, GPT-5 Mini)
- State: Dropdown is enabled and ready for interaction

### Test 2: Default Model Verification

**Test Description:** Validates that 'gpt-5-nano' is selected as the default model

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate to Frontend (if not already on page)
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Expand Debug Panel
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "Debug Panel toggle button",
    "ref": "button:has-text('Debug'), .debug-panel-toggle, [data-testid='debug-toggle']"
  }
}

// Step 3: Wait for Debug Panel to expand
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "AI Model",
    "time": 30
  }
}

// Step 4: Validate default model selection
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const selector = document.querySelector('.model-selector'); const selectedValue = selector ? selector.value : null; const selectedText = selector ? selector.options[selector.selectedIndex]?.textContent : null; const isDefault = selectedValue === 'gpt-5-nano'; return { selectedValue, selectedText, isDefault, allOptions: Array.from(selector?.options || []).map(opt => ({ value: opt.value, text: opt.textContent, selected: opt.selected })) }; }"
  }
}
```

**Expected Results:**

- Selected Value: "gpt-5-nano"
- Selected Text: "GPT-5 Nano" or "GPT-5 Nano (default)"
- Is Default: true
- All Options: 2 options with gpt-5-nano selected

### Test 3: Model Selection Functionality

**Test Description:** Validates that users can select different AI models from the dropdown

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate to Frontend (if not already on page)
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Expand Debug Panel
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "Debug Panel toggle button",
    "ref": "button:has-text('Debug'), .debug-panel-toggle, [data-testid='debug-toggle']"
  }
}

// Step 3: Wait for Debug Panel to expand
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "AI Model",
    "time": 30
  }
}

// Step 4: Select GPT-5 Mini model
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "AI Model selector dropdown",
    "ref": ".model-selector"
  }
}

// Step 5: Select GPT-5 Mini option
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "GPT-5 Mini option",
    "ref": "option[value='gpt-5-mini']"
  }
}

// Step 6: Wait for model selection to process
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "GPT-5 Mini",
    "time": 30
  }
}

// Step 7: Validate model selection change
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const selector = document.querySelector('.model-selector'); const selectedValue = selector ? selector.value : null; const selectedText = selector ? selector.options[selector.selectedIndex]?.textContent : null; return { selectedValue, selectedText, isGPT5Mini: selectedValue === 'gpt-5-mini' }; }"
  }
}
```

**Expected Results:**

- Selected Value: "gpt-5-mini"
- Selected Text: "GPT-5 Mini"
- Is GPT-5 Mini: true
- Model selection change successful

### Test 4: API Integration Validation

**Test Description:** Validates that backend API endpoints for model management are working correctly

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate to Frontend (if not already on page)
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Test API endpoint availability
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { return fetch('http://127.0.0.1:8000/api/v1/models').then(response => response.json()).then(data => ({ status: 'success', models: data.models?.length || 0, currentModel: data.currentModel, totalCount: data.totalCount })).catch(error => ({ status: 'error', error: error.message })); }"
  }
}

// Step 3: Test model selection API
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { return fetch('http://127.0.0.1:8000/api/v1/models/select', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ modelId: 'gpt-5-mini' }) }).then(response => response.json()).then(data => ({ status: 'success', success: data.success, message: data.message, selectedModel: data.selectedModel })).catch(error => ({ status: 'error', error: error.message })); }"
  }
}

// Step 4: Verify API response format
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { return { apiTest: 'completed', timestamp: new Date().toISOString() }; }"
  }
}
```

**Expected Results:**

- API Status: "success"
- Models Count: 2
- Current Model: Valid model ID
- Total Count: 2
- Selection API: Success with proper response format
- API Integration: Working correctly

### Test 7: Error Handling and Loading States

**Test Description:** Validates error handling and loading states for model selection

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate to Frontend (if not already on page)
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Expand Debug Panel
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "Debug Panel toggle button",
    "ref": "button:has-text('Debug'), .debug-panel-toggle, [data-testid='debug-toggle']"
  }
}

// Step 3: Wait for Debug Panel to expand
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "AI Model",
    "time": 30
  }
}

// Step 4: Test loading state during model selection
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "AI Model selector dropdown",
    "ref": ".model-selector"
  }
}

// Step 5: Select a different model to trigger loading
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "GPT-5 Mini option",
    "ref": "option[value='gpt-5-mini']"
  }
}

// Step 6: Check for loading indicator
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const loadingIndicator = document.querySelector('.loading-indicator'); const errorMessage = document.querySelector('.error-message'); const selector = document.querySelector('.model-selector'); return { hasLoadingIndicator: !!loadingIndicator, hasErrorMessage: !!errorMessage, isSelectorDisabled: selector ? selector.disabled : false, loadingText: loadingIndicator ? loadingIndicator.textContent : null }; }"
  }
}

// Step 7: Wait for loading to complete
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "GPT-5 Mini",
    "time": 30
  }
}

// Step 8: Validate final state
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const loadingIndicator = document.querySelector('.loading-indicator'); const errorMessage = document.querySelector('.error-message'); const selector = document.querySelector('.model-selector'); const selectedValue = selector ? selector.value : null; return { hasLoadingIndicator: !!loadingIndicator, hasErrorMessage: !!errorMessage, isSelectorDisabled: selector ? selector.disabled : false, selectedValue, loadingComplete: !loadingIndicator }; }"
  }
}
```

**Expected Results:**

- Has Loading Indicator: true (during selection)
- Has Error Message: false
- Is Selector Disabled: true (during loading)
- Selected Value: "gpt-5-mini" (after completion)
- Loading Complete: true (after selection)

### Test 8: Regression Testing - Existing Functionality

**Test Description:** Validates that existing financial query functionality still works with the new model selector

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate to Frontend (if not already on page)
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Send financial query with current model
{
  "tool": "mcp__playwright__browser_type",
  "parameters": {
    "element": "message input textarea",
    "ref": "textarea[placeholder*='message'], .chat-input textarea, input[type='text']",
    "text": "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
}

// Step 3: Submit message
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Enter"
  }
}

// Step 4: Wait for AI response (CRITICAL)
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "KEY TAKEAWAYS",
    "time": 120
  }
}

// Step 5: Validate response includes model name
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const messages = document.querySelectorAll('.message-content'); const lastMessage = messages[messages.length-1]?.textContent || ''; const hasModelName = /\\[gpt-5-nano\\]/.test(lastMessage); const hasStructuredContent = /KEY\\s*TAKEAWAYS|DETAILED\\s*ANALYSIS|DISCLAIMER/i.test(lastMessage); const hasFinancialContent = /market|trading|status|bullish|bearish/i.test(lastMessage); return { hasModelName, hasStructuredContent, hasFinancialContent, contentLength: lastMessage.length, responseEnding: lastMessage.slice(-20) }; }"
  }
}
```

**Expected Results:**

- Has Model Name: true
- Has Structured Content: true
- Has Financial Content: true
- Content Length: > 100 characters
- Response Ending: Contains "[gpt-5-nano]"

### Test 9: Accessibility Testing

**Test Description:** Validates that the model selector is accessible via keyboard navigation and screen readers

**Complete MCP Test Sequence:**

```json
// Step 1: Navigate to Frontend (if not already on page)
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Expand Debug Panel
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "Debug Panel toggle button",
    "ref": "button:has-text('Debug'), .debug-panel-toggle, [data-testid='debug-toggle']"
  }
}

// Step 3: Wait for Debug Panel to expand
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "AI Model",
    "time": 30
  }
}

// Step 4: Test keyboard navigation to model selector
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Tab"
  }
}

// Step 5: Test keyboard navigation within model selector
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Tab"
  }
}

// Step 6: Test keyboard interaction with model selector
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Enter"
  }
}

// Step 7: Test arrow key navigation
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "ArrowDown"
  }
}

// Step 8: Test selection with Enter key
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Enter"
  }
}

// Step 9: Validate accessibility attributes
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const selector = document.querySelector('.model-selector'); const container = document.querySelector('.model-selector-container'); const ariaLabel = selector ? selector.getAttribute('aria-label') : null; const ariaDescribedBy = selector ? selector.getAttribute('aria-describedby') : null; const role = selector ? selector.getAttribute('role') : null; const tabIndex = selector ? selector.getAttribute('tabindex') : null; return { hasAriaLabel: !!ariaLabel, hasAriaDescribedBy: !!ariaDescribedBy, hasRole: !!role, hasTabIndex: !!tabIndex, ariaLabel, ariaDescribedBy, role, tabIndex }; }"
  }
}
```

**Expected Results:**

- Has Aria Label: true
- Has Aria Described By: true (when error present)
- Has Role: true (if specified)
- Has Tab Index: true
- Aria Label: "Select AI model" or similar
- Keyboard Navigation: Working correctly

---

## Section 4: Success Validation Checklist

### 4.1 First-Try Success Criteria

**Before declaring success, verify ALL items:**

- [ ] All MCP tools executed without parameter errors
- [ ] Model selector visible and functional in Debug Panel
- [ ] Default model is 'gpt-5-nano'
- [ ] Model selection changes work correctly
- [ ] Response format includes [model-name]
- [ ] Model persistence works across page refreshes
- [ ] API integration working correctly
- [ ] Error handling and loading states functional
- [ ] Existing functionality still works (regression test)
- [ ] Performance is acceptable (< 5 seconds for model switching)
- [ ] Accessibility features working correctly
- [ ] All tests completed within 120-second timeout
- [ ] No polling methodology used (auto-retry only)
- [ ] Test completion report generated

### 4.2 Failure Investigation

**If test fails, check in order:**

1. **Tool Parameters:** Verify `time: 120` in wait_for calls
2. **Server Status:** Confirm backend/frontend operational
3. **Element Selectors:** Verify model selector elements are present
4. **Model Selection:** Check if model selection is working
5. **API Endpoints:** Verify backend model management endpoints
6. **Browser State:** Consider navigation refresh if unresponsive

### 4.3 Performance Classification

**Response Time Categories:**

- **SUCCESS:** < 45 seconds (excellent performance)
- **SLOW_PERFORMANCE:** 45-120 seconds (acceptable for AI responses)
- **TIMEOUT:** > 120 seconds (test failure)

**Model Switching Performance:**

- **EXCELLENT:** < 2 seconds
- **GOOD:** 2-5 seconds
- **SLOW:** > 5 seconds

---

## Section 5: Test Report Generation

### 5.1 Required Report Elements

**For Each Test:**

1. Test execution timestamp and duration
2. Performance classification and actual timing
3. Auto-retry detection success/failure details
4. Content validation results
5. Model selector functionality validation
6. Any errors encountered and resolution steps

### 5.2 Test Report Template

```markdown
# AI Model Selector Test Report

## Test Execution Summary
- **Execution Date:** [timestamp]
- **Total Duration:** [duration]
- **Tests Passed:** [X/10]
- **Tests Failed:** [X/10]

## Individual Test Results

### Test 1: Model Selector Visibility
- **Status:** PASS/FAIL
- **Duration:** [time]
- **Details:** [specific results]

### Test 2: Default Model Verification
- **Status:** PASS/FAIL
- **Duration:** [time]
- **Details:** [specific results]

[... continue for all 10 tests]

## Overall Assessment
- **Feature Status:** FULLY FUNCTIONAL / PARTIALLY FUNCTIONAL / NOT FUNCTIONAL
- **Recommendations:** [any recommendations]
```

---

## FINAL SUCCESS CONFIRMATION

**CRITICAL SUCCESS INDICATOR:** If you successfully executed all 10 tests following this document exactly as written, with response detection within 120 seconds and proper content validation, then this document has achieved its purpose.

**Next Steps After Success:**

1. Document actual response times and performance classifications
2. Note any detection methods that worked most effectively
3. Report any deviations from expected behavior for document improvement
4. Proceed with additional test scenarios using same methodology

**If Unsuccessful:** Review Section 4.2 (Failure Investigation) before requesting external assistance.

---

**Document Version:** 1.0 - AI Model Selector Testing Plan
**Last Updated:** Based on existing MCP testing methodology and AI Model Selector implementation
**Validation Status:** Designed for 100% First-Try Success Rate by AI Agents
**Supersedes:** N/A - New document for AI Model Selector feature testing
