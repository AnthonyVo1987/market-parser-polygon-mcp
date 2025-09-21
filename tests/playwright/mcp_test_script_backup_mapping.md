# Playwright Backup Tools Mapping: Microsoft → ExecuteAutomation

**Document Purpose:** Maps Microsoft Playwright Tools MCP Server commands to ExecuteAutomation Playwright Backup Tools for seamless test execution.

**Target Audience:** AI Coding Agents performing MCP testing with backup tools
**Expected Outcome:** Direct tool substitution without functionality loss
**Methodology:** 1:1 mapping with polling implementation for wait functionality

---

## CRITICAL MAPPING OVERVIEW

**Microsoft Playwright Tools** → **ExecuteAutomation Backup Tools**

| Microsoft Tool | Backup Tool | Status | Notes |
|----------------|-------------|--------|-------|
| `mcp__playwright__browser_navigate` | `mcp_playwright-backup_playwright_navigate` | ✅ Direct | Same parameters |
| `mcp__playwright__browser_snapshot` | `mcp_playwright-backup_playwright_get_visible_text` | ✅ Equivalent | Get page state |
| `mcp__playwright__browser_type` | `mcp_playwright-backup_playwright_fill` | ✅ Mapped | Parameter conversion needed |
| `mcp__playwright__browser_press_key` | `mcp_playwright-backup_playwright_press_key` | ✅ Direct | Same parameters |
| `mcp__playwright__browser_wait_for` | **POLLING IMPLEMENTATION** | ⚠️ Custom | Requires polling logic |
| `mcp__playwright__browser_click` | `mcp_playwright-backup_playwright_click` | ✅ Mapped | Parameter conversion needed |
| `mcp__playwright__browser_evaluate` | `mcp_playwright-backup_playwright_evaluate` | ✅ Mapped | Parameter conversion needed |

---

## DETAILED TOOL MAPPINGS

### 1. Navigation Tool

```json
// Microsoft
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Backup
{
  "tool": "mcp_playwright-backup_playwright_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}
```

**Status:** ✅ Direct mapping - no changes needed

### 2. Snapshot Tool

```json
// Microsoft
{
  "tool": "mcp__playwright__browser_snapshot",
  "parameters": {}
}

// Backup
{
  "tool": "mcp_playwright-backup_playwright_get_visible_text",
  "parameters": {}
}
```

**Status:** ✅ Equivalent functionality - gets page state for element identification

### 3. Type Tool

```json
// Microsoft
{
  "tool": "mcp__playwright__browser_type",
  "parameters": {
    "element": "message input field",
    "ref": "textarea[placeholder*='message'], .chat-input textarea",
    "text": "Market Status: PRIORITY FAST REQUEST..."
  }
}

// Backup
{
  "tool": "mcp_playwright-backup_playwright_fill",
  "parameters": {
    "selector": "textarea[placeholder*='message']",
    "value": "Market Status: PRIORITY FAST REQUEST..."
  }
}
```

**Status:** ✅ Mapped - use first selector from `ref` as `selector`, `text` becomes `value`

### 4. Press Key Tool

```json
// Microsoft
{
  "tool": "mcp__playwright__browser_press_key",
  "parameters": {
    "key": "Enter"
  }
}

// Backup
{
  "tool": "mcp_playwright-backup_playwright_press_key",
  "parameters": {
    "key": "Enter"
  }
}
```

**Status:** ✅ Direct mapping - no changes needed

### 5. Wait For Tool (CRITICAL DIFFERENCE)

```json
// Microsoft (Auto-retry built-in)
{
  "tool": "mcp__playwright__browser_wait_for",
  "parameters": {
    "text": "KEY TAKEAWAYS",
    "time": 120
  }
}

// Backup (Requires polling implementation)
// Step 1: Get current page text
{
  "tool": "mcp_playwright-backup_playwright_get_visible_text",
  "parameters": {}
}

// Step 2: Check if text contains search term
// If not found, wait 2 seconds and repeat until timeout
// Implementation: Custom polling loop with 120-second timeout
```

**Status:** ⚠️ Custom implementation required - see polling section below

### 6. Click Tool

```json
// Microsoft
{
  "tool": "mcp__playwright__browser_click",
  "parameters": {
    "element": "Stock Snapshot button",
    "ref": "button:has-text('Stock Snapshot'), button[title*='Stock']"
  }
}

// Backup
{
  "tool": "mcp_playwright-backup_playwright_click",
  "parameters": {
    "selector": "button:has-text('Stock Snapshot')"
  }
}
```

**Status:** ✅ Mapped - use first selector from `ref` as `selector`

### 7. Evaluate Tool

```json
// Microsoft
{
  "tool": "mcp__playwright__browser_evaluate",
  "parameters": {
    "function": "() => { const messages = document.querySelectorAll('.message-content'); return messages[messages.length-1]?.textContent || 'No response found'; }"
  }
}

// Backup
{
  "tool": "mcp_playwright-backup_playwright_evaluate",
  "parameters": {
    "script": "() => { const messages = document.querySelectorAll('.message-content'); return messages[messages.length-1]?.textContent || 'No response found'; }"
  }
}
```

**Status:** ✅ Mapped - `function` parameter becomes `script`

---

## POLLING IMPLEMENTATION FOR WAIT_FOR

**CRITICAL:** The backup tools don't have built-in auto-retry detection, so we must implement polling.

### Polling Algorithm

```javascript
// Pseudo-code for wait_for functionality
function wait_for_text(searchText, timeoutSeconds) {
  const startTime = Date.now();
  const timeoutMs = timeoutSeconds * 1000;
  const pollInterval = 2000; // 2 seconds
  
  while (Date.now() - startTime < timeoutMs) {
    // Get current page text
    const pageText = get_visible_text();
    
    // Check if search text is found
    if (pageText.includes(searchText)) {
      return { 
        success: true, 
        foundText: searchText,
        elapsedTime: Date.now() - startTime
      };
    }
    
    // Wait before next poll
    sleep(pollInterval);
  }
  
  return { 
    success: false, 
    timeout: true,
    elapsedTime: timeoutMs
  };
}
```

### Implementation Steps

1. **Start Timer:** Record start time
2. **Get Page Text:** Use `mcp_playwright-backup_playwright_get_visible_text`
3. **Check for Text:** Search for target text in page content
4. **If Found:** Return success with elapsed time
5. **If Not Found:** Wait 2 seconds and repeat
6. **If Timeout:** Return failure after 120 seconds

---

## COMPLETE TEST SEQUENCE MAPPINGS

### Test 1: Market Status Test

```json
// Step 1: Navigate
{
  "tool": "mcp_playwright-backup_playwright_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Get page state
{
  "tool": "mcp_playwright-backup_playwright_get_visible_text",
  "parameters": {}
}

// Step 3: Input message
{
  "tool": "mcp_playwright-backup_playwright_fill",
  "parameters": {
    "selector": "textarea[placeholder*='message']",
    "value": "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
}

// Step 4: Submit message
{
  "tool": "mcp_playwright-backup_playwright_press_key",
  "parameters": {
    "key": "Enter"
  }
}

// Step 5: Wait for response (POLLING)
// Implement custom polling loop:
// - Get visible text every 2 seconds
// - Check for "KEY TAKEAWAYS" in text
// - Continue until found or 120 seconds timeout

// Step 6: Validate response
{
  "tool": "mcp_playwright-backup_playwright_evaluate",
  "parameters": {
    "script": "() => { const messages = document.querySelectorAll('.message-content'); const lastMessage = messages[messages.length-1]?.textContent || ''; return { hasStructuredContent: /KEY\\s*TAKEAWAYS|DETAILED\\s*ANALYSIS|DISCLAIMER/i.test(lastMessage), contentLength: lastMessage.length, containsMarketData: /market|trading|status/i.test(lastMessage) }; }"
  }
}
```

### Test 2: NVDA Ticker Snapshot Test

```json
// Step 1: Navigate
{
  "tool": "mcp_playwright-backup_playwright_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Get page state
{
  "tool": "mcp_playwright-backup_playwright_get_visible_text",
  "parameters": {}
}

// Step 3: Input NVDA ticker query
{
  "tool": "mcp_playwright-backup_playwright_fill",
  "parameters": {
    "selector": "textarea[placeholder*='message']",
    "value": "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
  }
}

// Step 4: Submit message
{
  "tool": "mcp_playwright-backup_playwright_press_key",
  "parameters": {
    "key": "Enter"
  }
}

// Step 5: Wait for NVDA response (POLLING)
// Implement custom polling loop:
// - Get visible text every 2 seconds
// - Check for "NVIDIA" in text
// - Continue until found or 120 seconds timeout

// Step 6: Validate NVDA-specific response
{
  "tool": "mcp_playwright-backup_playwright_evaluate",
  "parameters": {
    "script": "() => { const messages = document.querySelectorAll('.message-content'); const lastMessage = messages[messages.length-1]?.textContent || ''; return { hasStructuredContent: /KEY\\s*TAKEAWAYS|DETAILED\\s*ANALYSIS|DISCLAIMER/i.test(lastMessage), contentLength: lastMessage.length, containsNVDA: /nvda|nvidia/i.test(lastMessage), hasStockData: /price|volume|market cap|current/i.test(lastMessage) }; }"
  }
}
```

### Test 3: Stock Snapshot Button Test

```json
// Step 1: Navigate
{
  "tool": "mcp_playwright-backup_playwright_navigate",
  "parameters": {
    "url": "http://127.0.0.1:3000"
  }
}

// Step 2: Get page state
{
  "tool": "mcp_playwright-backup_playwright_get_visible_text",
  "parameters": {}
}

// Step 3: Input ticker for button test
{
  "tool": "mcp_playwright-backup_playwright_fill",
  "parameters": {
    "selector": "textarea[placeholder*='message']",
    "value": "NVDA"
  }
}

// Step 4: Click Stock Snapshot button
{
  "tool": "mcp_playwright-backup_playwright_click",
  "parameters": {
    "selector": "button:has-text('Stock Snapshot')"
  }
}

// Step 5: Wait for button-triggered response (POLLING)
// Implement custom polling loop:
// - Get visible text every 2 seconds
// - Check for "DETAILED ANALYSIS" in text
// - Continue until found or 120 seconds timeout

// Step 6: Validate button-triggered response
{
  "tool": "mcp_playwright-backup_playwright_evaluate",
  "parameters": {
    "script": "() => { const messages = document.querySelectorAll('.message-content'); const lastMessage = messages[messages.length-1]?.textContent || ''; return { hasStructuredContent: /KEY\\s*TAKEAWAYS|DETAILED\\s*ANALYSIS|DISCLAIMER/i.test(lastMessage), contentLength: lastMessage.length, hasSnapshotContent: /snapshot|stock|price|volume/i.test(lastMessage), buttonTriggered: true }; }"
  }
}
```

---

## PARAMETER CONVERSION RULES

### Element Selection

- **Microsoft:** `element` + `ref` with fallback selectors
- **Backup:** Single `selector` parameter
- **Rule:** Use first selector from `ref` parameter as `selector`

### Text Input

- **Microsoft:** `text` parameter
- **Backup:** `value` parameter
- **Rule:** Direct mapping - `text` → `value`

### JavaScript Execution

- **Microsoft:** `function` parameter
- **Backup:** `script` parameter
- **Rule:** Direct mapping - `function` → `script`

### Timeout Handling

- **Microsoft:** Built-in auto-retry with `time` parameter
- **Backup:** Custom polling implementation
- **Rule:** Implement 2-second polling intervals with specified timeout

---

## CRITICAL SUCCESS FACTORS

### 1. Polling Implementation

- **MUST** implement custom polling for `wait_for` functionality
- **MUST** use 2-second intervals between polls
- **MUST** respect 120-second timeout limit
- **MUST** return success immediately when text found

### 2. Element Selection Strategy

- **MUST** use first selector from Microsoft `ref` parameter
- **MUST** handle fallback selectors gracefully
- **MUST** verify element exists before interaction

### 3. Error Handling

- **MUST** handle timeout scenarios gracefully
- **MUST** provide clear error messages for debugging
- **MUST** maintain test sequence integrity

### 4. Performance Considerations

- **MUST** minimize polling frequency to avoid performance impact
- **MUST** stop polling immediately when condition met
- **MUST** document actual response times for analysis

---

## IMPLEMENTATION CHECKLIST

Before executing tests with backup tools:

- [ ] Verify all backup tools are available and functional
- [ ] Implement polling mechanism for `wait_for` functionality
- [ ] Test element selectors on target application
- [ ] Validate parameter conversion logic
- [ ] Set up proper error handling and logging
- [ ] Confirm 120-second timeout implementation
- [ ] Test polling performance and reliability

---

**Document Version:** 1.0 - Complete Microsoft to Backup Tool Mapping
**Last Updated:** Based on ExecuteAutomation Playwright MCP Server capabilities
**Validation Status:** Ready for implementation with backup tools
**Supersedes:** Microsoft Playwright Tools MCP Server dependencies
