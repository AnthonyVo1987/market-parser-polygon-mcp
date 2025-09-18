# Playwright MCP Tools Usage Guide for Market Parser Application

**Target Audience:** AI Coding Agents working on the Market Parser financial analysis application  
**Purpose:** Specific guidance for proper Playwright MCP tool usage in our FastAPI + React financial app context

---

## Application Context

**Market Parser Application Stack:**
- **Backend**: FastAPI server on http://127.0.0.1:8000 (fixed port for consistent testing)
- **Frontend**: React + Vite on http://127.0.0.1:3000
- **Production**: Static build on http://127.0.0.1:5500
- **Key Features**: Financial chat interface, analysis buttons, emoji-based responses, Polygon.io data integration

**Server Startup (PRIMARY METHOD):**
- **RECOMMENDED**: Use `./start-app.sh` for one-click startup of both servers
- **Alternative**: Use `npm run start:app` or `./start-app-xterm.sh` variants
- All methods handle server cleanup, health verification, and proper startup sequence
- Ensures consistent server ports and proper backend/frontend coordination

**Network Configuration Notes:**
- Backend and frontend use fixed ports (8000/3000) for reliable testing
- No dynamic port allocation - ensures consistent MCP tool targeting
- Production builds are served on 127.0.0.1:5500 via Live Server

**TypeScript Configuration Note:**
- Ensure `@types/node` is available as devDependency for proper TypeScript support when using file system operations and setTimeout/clearTimeout functions

**Critical UI Components to Test:**
- `ChatInput_OpenAI`: Multi-line text input with financial queries
- `AnalysisButtons`: Stock Snapshot, Support/Resistance, Technical Analysis buttons  
- `ChatInterface_OpenAI`: Message container with emoji indicators
- `DebugPanel`: Expandable debugging information
- `ExportButtons`: Copy and export functionality

---

## AI Response Testing Procedures (CRITICAL)

**⚠️ IMPORTANT: AI responses take 30-90 seconds on average. Use modern Playwright MCP auto-retry patterns!**

### Modern Auto-Retry Approach
- **Per Test Timeout**: 120 seconds maximum for AI responses, 30s for UI changes
- **AI Response Time**: Typically 30-90 seconds
- **Auto-Retry Mechanism**: Built-in Playwright MCP auto-retry handles continuous checking
- **Success Condition**: Response detected immediately when available (no fixed intervals)
- **Failure Condition**: Only after timeout period without response
- **Alternative**: Use `expect.poll()` pattern for complex conditions

### Modern AI Response Testing Workflow

```typescript
// MODERN: Auto-retry with Playwright MCP built-in mechanisms
1. Send AI query (via browser_type or browser_click)
2. Use browser_wait_for() with appropriate timeout
3. Playwright MCP automatically retries until condition met or timeout
4. No manual polling loops required
5. Immediate success when response appears
6. Alternative: browser_evaluate() with promise-based waiting
```

### Modern Auto-Retry Patterns

**✅ MODERN Approach (Recommended):**
- Use `browser_wait_for()` with appropriate timeout (120s for AI, 30s for UI)
- Employ Playwright MCP auto-retry mechanisms
- Let Playwright MCP handle retry logic automatically
- Use `browser_evaluate()` with promise-based waiting for complex conditions
- Alternative: `expect.poll()` pattern for custom condition checking

**❌ OUTDATED Patterns (Replace These):**
- Manual polling loops with fixed intervals
- Custom retry logic when Playwright MCP provides built-in solutions
- setTimeout-based waiting instead of condition-based waiting
- Checking for responses at predetermined intervals instead of auto-retry
- Multiple sequential timeout calls instead of single auto-retry call

---

## Tool Categories and Usage

### 1. Browser Session Management

#### `mcp__playwright__browser_install`
**Correct Usage:** Always call FIRST before any browser automation
```
Purpose: Install required Playwright browsers for testing
When: At start of any test session
Input: No parameters required
Output: Browser installation confirmation
```

**Example - Correct:**
```typescript
// Call at beginning of test setup
await mcp__playwright__browser_install()
```

**Incorrect:** Never skip browser installation in new environments

---

#### `mcp__playwright__browser_navigate`
**Correct Usage:** Navigate to our specific application URLs
```
Purpose: Load Market Parser frontend for testing
Input: url (string) - Must be our application URLs
Correct URLs: 
  - "http://127.0.0.1:3000" (development)
  - "http://127.0.0.1:5500" (production)
Expected Output: Page loaded with React app
```

**Example - Correct:**
```typescript
// Navigate to development frontend
await mcp__playwright__browser_navigate({
  url: "http://127.0.0.1:3000"
})
```

**Incorrect Examples:**
- Using external URLs when testing our app
- Navigating without backend server running
- Missing protocol (http://) in URL

---

#### `mcp__playwright__browser_close`
**Correct Usage:** Clean up at end of test sessions
```
Purpose: Close browser and cleanup resources
When: After completing test scenarios
Input: No parameters
Output: Browser closed confirmation
```

---

### 2. Page Analysis and Snapshots

#### `mcp__playwright__browser_snapshot`
**Correct Usage:** ESSENTIAL for understanding our financial chat interface
```
Purpose: Get accessibility snapshot of current page state
When: 
  ✅ Before interacting with financial chat interface
  ✅ After sending financial queries to validate responses
  ✅ To locate specific UI elements (buttons, inputs)
  ✅ To verify emoji indicators in responses
Input: No parameters required
Output: Structured accessibility tree with element references
```

**Example - Market Parser Specific:**
```typescript
// Take snapshot to find analysis buttons
const snapshot = await mcp__playwright__browser_snapshot()
// Look for: "Stock Snapshot", "Support/Resistance", "Technical Analysis" buttons
// Look for: textarea with placeholder "Ask about stocks..."
// Look for: emoji indicators like 📈📉💰 in responses
```

**Correct Conditions:**
- Use to find ChatInput_OpenAI textarea
- Use to locate AnalysisButtons before clicking
- Use to verify financial response content with emojis
- Use to find element references (ref values) for interactions

**Incorrect Conditions:**
- Taking snapshots of external sites
- Using without understanding element refs returned

---

#### `mcp__playwright__browser_take_screenshot`
**Correct Usage:** Visual verification of financial interface states
```
Purpose: Capture visual state for verification
Input: 
  - filename (optional): Save path for screenshot
  - fullPage (boolean): true for complete page capture
  - element + ref: Capture specific UI component
Output: Screenshot saved to specified location
```

**Example - Financial Interface:**
```typescript
// Screenshot full financial chat interface
await mcp__playwright__browser_take_screenshot({
  fullPage: true,
  filename: "financial-chat-interface.png"
})

// Screenshot specific analysis buttons area
await mcp__playwright__browser_take_screenshot({
  element: "Analysis buttons container",
  ref: "[element_ref_from_snapshot]",
  filename: "analysis-buttons.png"
})
```

---

### 3. User Interactions

#### `mcp__playwright__browser_click`
**Correct Usage:** Interact with our financial analysis buttons and UI
```
Purpose: Click Market Parser UI elements
Input:
  - element (string): Human description of element
  - ref (string): Exact element reference from snapshot
  - button (optional): "left" | "right" | "middle"
Expected Output: Element clicked, UI state updated
```

**Example - Financial App Specific:**
```typescript
// Click Stock Snapshot analysis button
await mcp__playwright__browser_click({
  element: "Stock Snapshot analysis button",
  ref: "button[2]" // From snapshot
})

// Click Technical Analysis button  
await mcp__playwright__browser_click({
  element: "Technical Analysis button", 
  ref: "button[4]" // From snapshot
})
```

**Correct Conditions:**
- Use element ref from `browser_snapshot`
- Describe element in Market Parser context
- Click AnalysisButtons to trigger financial queries
- Click export/copy buttons for response handling

**Incorrect Conditions:**
- Clicking without taking snapshot first
- Using generic element descriptions
- Clicking non-Market Parser elements

---

#### `mcp__playwright__browser_type`
**Correct Usage:** Enter financial queries in our chat interface
```
Purpose: Input financial queries into ChatInput_OpenAI
Input:
  - element (string): Description of input field
  - ref (string): Element reference from snapshot  
  - text (string): Financial query to send
  - submit (boolean): true to send message
Expected Output: Text entered, message sent if submit=true
```

**Example - Financial Queries:**
```typescript
// Type stock analysis query
await mcp__playwright__browser_type({
  element: "Financial chat input field",
  ref: "textarea[0]", // From snapshot
  text: "Tell me about NVDA stock performance",
  submit: true
})

// Type market status query
await mcp__playwright__browser_type({
  element: "Chat input textarea",
  ref: "textarea[0]",
  text: "Market status: PRIORITY FAST REQUEST",
  submit: true  
})
```

**Correct Financial Query Patterns:**
- Stock analysis: "Tell me about [TICKER] stock"
- Market status: "Market status: PRIORITY FAST REQUEST"  
- Multi-ticker: "Compare AAPL vs TSLA vs NVDA"
- Technical analysis: "Technical analysis for SPY"

**Incorrect Conditions:**
- Typing non-financial queries in financial app
- Not using submit=true when sending messages
- Using wrong element references

---

#### `mcp__playwright__browser_fill_form`
**Correct Usage:** Fill multiple inputs in Market Parser forms
```
Purpose: Fill form fields in our financial interface
Input: 
  - fields: Array of field objects with name, type, ref, value
Expected Output: All specified fields filled
```

**Example - Market Parser Context:**
```typescript
// Fill debug panel settings
await mcp__playwright__browser_fill_form({
  fields: [
    {
      name: "Debug level selector",
      type: "combobox", 
      ref: "select[0]",
      value: "verbose"
    },
    {
      name: "Enable emoji indicators",
      type: "checkbox",
      ref: "input[1]", 
      value: "true"
    }
  ]
})
```

---

### 4. Content Validation and Waiting

#### `mcp__playwright__browser_wait_for`
**Modern Usage:** Wait for financial responses with built-in auto-retry
```
Purpose: Wait for Market Parser specific content/states
Input:
  - text (string): Specific text to wait for
  - textGone (string): Text to wait for disappearance
  - time (number): Maximum timeout (120s for AI responses)
Expected Output: Condition met or timeout
```

**Example - MODERN Auto-Retry Approach:**
```typescript
// MODERN: Single wait with auto-retry (recommended)
await mcp__playwright__browser_wait_for({
  text: "🎯 KEY TAKEAWAYS", // Our response format
  time: 120 // Maximum timeout - auto-retries until found
});
console.log(`✅ AI response detected via auto-retry`);

// Alternative modern patterns
// Wait for bullish indicator with auto-retry
await mcp__playwright__browser_wait_for({
  text: "📈", // Bullish indicator
  time: 120 // Auto-retries until found or timeout
})

// Wait for loading completion
await mcp__playwright__browser_wait_for({
  textGone: "Analyzing financial data...",
  time: 120 // Auto-retries until condition met
})

// For sophisticated conditions, use promise-based evaluation
const responseContent = await mcp__playwright__browser_evaluate({
  function: `() => {
    return new Promise((resolve) => {
      const checkForResponse = () => {
        const messages = document.querySelectorAll('.chat-message');
        const lastMessage = Array.from(messages).pop();
        if (lastMessage && lastMessage.textContent.includes('🎯 KEY TAKEAWAYS')) {
          resolve({ found: true, content: lastMessage.textContent });
        } else {
          setTimeout(checkForResponse, 1000); // Built-in retry
        }
      };
      checkForResponse();
    });
  }`
});

// Alternative: expect.poll() pattern (for complex assertions)
// Note: This is standard Playwright pattern, not MCP specific
// await expect.poll(async () => {
//   const snapshot = await browser_snapshot();
//   return snapshot.includes('🎯 KEY TAKEAWAYS');
// }, { timeout: 120000 }).toBe(true);
```

**MODERN Best Practices:**
```typescript
// ✅ RECOMMENDED: Use context-appropriate timeouts
// AI responses: 120s timeout (backend processing time)
await mcp__playwright__browser_wait_for({
  text: "🎯 KEY TAKEAWAYS",
  time: 120
});

// UI state changes: 30s timeout (React updates)
await mcp__playwright__browser_wait_for({
  text: "Analysis complete",
  time: 30
});

// Fast UI feedback: 10s timeout (immediate responses)
await mcp__playwright__browser_wait_for({
  text: "Button clicked",
  time: 10
});

// Network completion: Use built-in network waiting
await mcp__playwright__browser_evaluate({
  function: `() => {
    return new Promise(resolve => {
      if (document.readyState === 'complete') resolve(true);
      else window.addEventListener('load', () => resolve(true));
    });
  }`
});
```

**OUTDATED Patterns (Replace These):**
```typescript
// ❌ OUTDATED: Manual polling loops
let found = false;
while (!found) {
  try {
    await mcp__playwright__browser_wait_for({text: "response", time: 30});
    found = true;
  } catch (e) {
    // Continue polling... (AVOID THIS)
  }
}

// ❌ OUTDATED: Fixed interval checking
for (let i = 0; i < 4; i++) {
  await mcp__playwright__browser_wait_for({text: "response", time: 30});
}

// ❌ OUTDATED: Multiple sequential calls
try {
  await browser_wait_for({text: "response", time: 30});
} catch {
  await browser_wait_for({text: "response", time: 30});
  // Repeated calls instead of single auto-retry
}
```

**Market Parser Specific Wait Patterns:**
- Wait for "🎯 KEY TAKEAWAYS" (our response format)
- Wait for financial emojis: 📈📉💰💸🏢📊
- Wait for analysis completion
- Wait for button state changes

**Incorrect Conditions:**
- Waiting for non-Market Parser content
- Using inappropriate timeouts (>120s)
- Not accounting for backend API delays

---

#### `mcp__playwright__browser_evaluate`
**Correct Usage:** Extract financial data from our React interface
```
Purpose: Execute JavaScript to extract Market Parser state
Input:
  - function: JavaScript function to execute
  - element + ref: Target specific element
Expected Output: Function return value
```

**Example - Financial Data Extraction:**
```typescript
// Extract financial emojis from response
const emojiData = await mcp__playwright__browser_evaluate({
  function: `() => {
    const messages = document.querySelectorAll('.chat-message');
    const emojis = [];
    messages.forEach(msg => {
      const text = msg.textContent;
      if (text.includes('📈')) emojis.push('bullish');
      if (text.includes('📉')) emojis.push('bearish'); 
      if (text.includes('💰')) emojis.push('financial');
    });
    return emojis;
  }`
})

// Check if analysis buttons are enabled
const buttonStates = await mcp__playwright__browser_evaluate({
  function: `() => {
    const buttons = document.querySelectorAll('.analysis-button');
    return Array.from(buttons).map(btn => ({
      text: btn.textContent,
      disabled: btn.disabled
    }));
  }`
})
```

---

### 5. Advanced Testing Features

#### `mcp__playwright__browser_console_messages`
**Correct Usage:** Debug our React application console output
```
Purpose: Monitor Market Parser console logs and errors
Input: No parameters
Expected Output: Array of console messages
```

**Example - Financial App Debugging:**
```typescript
// Check for React errors in financial interface
const messages = await mcp__playwright__browser_console_messages()
// Look for: API errors, financial data parsing issues, emoji rendering problems
```

---

#### `mcp__playwright__browser_network_requests`
**Correct Usage:** Monitor API calls to our FastAPI backend
```
Purpose: Verify financial data API communications
Input: No parameters  
Expected Output: Network request details
```

**Example - Backend API Monitoring:**
```typescript
// Monitor calls to our FastAPI endpoints
const requests = await mcp__playwright__browser_network_requests()
// Look for: POST /chat, GET /health, Polygon.io API calls
// Verify: 200 status codes, proper response times
```

---

## Market Parser Specific Testing Patterns

### Financial Query Test Pattern (Modern Auto-Retry)
```typescript
1. browser_install() // Setup
2. browser_navigate({url: "http://127.0.0.1:3000"}) // Load app
3. browser_snapshot() // Get element refs
4. browser_type({
     element: "Chat input",
     ref: "textarea[0]", 
     text: "Tell me about NVDA",
     submit: true
   }) // Send query
   
// MODERN: Single wait with auto-retry
5. await browser_wait_for({
     text: "🎯 KEY TAKEAWAYS",
     time: 120 // Auto-retries until found or timeout
   });
   console.log(`✅ Response detected via auto-retry`);

6. browser_snapshot() // Verify response content

// Alternative: Promise-based evaluation for complex conditions
// const result = await browser_evaluate({
//   function: `() => {
//     return new Promise(resolve => {
//       const checkCondition = () => {
//         if (document.body.textContent.includes('🎯 KEY TAKEAWAYS')) {
//           resolve(true);
//         } else {
//           setTimeout(checkCondition, 1000);
//         }
//       };
//       checkCondition();
//     });
//   }`
// });
```

### Analysis Button Test Pattern (Modern Auto-Retry)
```typescript
1. browser_navigate({url: "http://127.0.0.1:3000"})
2. browser_snapshot() // Find buttons
3. browser_click({
     element: "Stock Snapshot button",
     ref: "button[2]"
   }) // Click analysis button
   
// MODERN: Auto-retry waiting
4. await browser_wait_for({
     text: "📊", // Financial data indicator
     time: 120 // Auto-retries until condition met
   });
   console.log(`✅ Button response detected`);

5. browser_snapshot() // Verify populated query

// Alternative: Multiple condition checking with auto-retry
const checkResponse = async () => {
  const conditions = ["📊", "🎯 KEY TAKEAWAYS", "📈", "💰"];
  for (const condition of conditions) {
    try {
      await browser_wait_for({text: condition, time: 30});
      return condition;
    } catch {
      continue; // Try next condition
    }
  }
  throw new Error("No financial response detected after 120s total");
};
const responseType = await checkResponse();
```

### Response Validation Pattern
```typescript
1. [Send financial query]
2. browser_wait_for({text: "🎯 KEY TAKEAWAYS"})
3. browser_evaluate({
     function: `() => {
       const content = document.body.textContent;
       return {
         hasKeyTakeaways: content.includes('🎯 KEY TAKEAWAYS'),
         hasBullishEmoji: content.includes('📈'),
         hasBearishEmoji: content.includes('📉'),
         hasFinancialEmoji: content.includes('💰')
       };
     }`
   }) // Extract validation data
```

---

## Modern Auto-Retry vs Timeout Detection (CRITICAL)

**⚠️ Most Critical Section: Leverages Playwright's built-in retry mechanisms**

### Understanding Modern Auto-Retry

**🔄 AUTO-RETRY (Modern Behavior):**
- AI Agent sends query at 0s
- `browser_wait_for()` continuously checks for condition
- No manual intervals - checks as frequently as possible
- Response detected immediately when available (could be 45s, 67s, 89s, etc.)
- **Total Time**: Variable based on actual response time
- **Result**: PASS ✅ as soon as condition met

**⏰ TRUE TIMEOUT (Actual Failure):**
- AI Agent sends query at 0s
- Auto-retry continues for full timeout period (120s)
- No response detected within timeout period
- **Total Time**: 120s elapsed without response
- **Result**: FAIL ❌

### Modern Implementation Pattern

```typescript
// ✅ MODERN: Single wait with built-in auto-retry
async function waitForAIResponse(expectedText: string): Promise<boolean> {
  try {
    // Single call with auto-retry built-in
    await mcp__playwright__browser_wait_for({
      text: expectedText,
      time: 120 // Maximum timeout - auto-retries internally
    });
    
    console.log(`✅ SUCCESS: Response detected via auto-retry`);
    return true;
    
  } catch (error) {
    console.log(`❌ TRUE TIMEOUT: No response after 120s`);
    throw new Error(`AI response timeout after 120s`);
  }
}

// Alternative: Progressive timeout strategy
async function waitWithFallbacks(primaryText: string, fallbackText: string): Promise<string> {
  try {
    await mcp__playwright__browser_wait_for({text: primaryText, time: 90});
    return "primary_response";
  } catch {
    try {
      await mcp__playwright__browser_wait_for({text: fallbackText, time: 30});
      return "fallback_response";
    } catch {
      throw new Error("No response after 120s total");
    }
  }
}
```

### OUTDATED Implementations (Replace These)

```typescript
// ❌ OUTDATED: Manual polling loops
let found = false;
let attempts = 0;
while (!found && attempts < 4) {
  try {
    await mcp__playwright__browser_wait_for({text: "response", time: 30});
    found = true;
  } catch {
    attempts++;
    console.log(`Attempt ${attempts} failed, retrying...`);
  }
}

// ❌ OUTDATED: Fixed interval checking
for (let i = 0; i < 4; i++) {
  try {
    await mcp__playwright__browser_wait_for({text: "response", time: 30});
    break;
  } catch {
    if (i === 3) throw new Error("Final timeout");
  }
}

// ❌ OUTDATED: Custom timeout management
const startTime = Date.now();
while (Date.now() - startTime < 120000) {
  // Custom retry logic
}
```

### Modern Best Practices

**✅ Recommended Patterns:**
```typescript
// Simple auto-retry wait (most common)
await browser_wait_for({text: "🎯 KEY TAKEAWAYS", time: 120});

// Multiple condition checking with early exit
const waitForAnyResponse = async () => {
  const conditions = ["🎯 KEY TAKEAWAYS", "📈", "📊", "💰"];
  for (const condition of conditions) {
    try {
      await browser_wait_for({text: condition, time: 30});
      return condition; // Exit immediately when found
    } catch {
      continue; // Try next condition
    }
  }
  throw new Error("No financial response detected after 120s total");
};

// Promise-based custom condition waiting
await browser_evaluate({
  function: `() => {
    return new Promise(resolve => {
      const checkCondition = () => {
        const hasResponse = document.body.textContent.includes('🎯 KEY TAKEAWAYS');
        if (hasResponse || document.readyState === 'complete') {
          resolve(true);
        } else {
          setTimeout(checkCondition, 1000); // Built-in retry
        }
      };
      checkCondition();
    });
  }`
});

// Alternative: expect.poll() for complex assertions (standard Playwright)
// await expect.poll(async () => {
//   const snapshot = await browser_snapshot();
//   return snapshot.includes('financial_indicator');
// }, { timeout: 120000 }).toBe(true);
```

### Key Debugging Indicators

**✅ Modern Auto-Retry Logs:**
```
⏳ Waiting for response (auto-retry active)...
✅ SUCCESS: Response detected after 67s
```

**❌ Outdated Manual Polling Logs:**
```
⏳ POLLING: No response at 30s mark - continuing...
⏳ POLLING: No response at 60s mark - continuing...
```

### Validation Checklist

Before reporting a timeout failure, verify:
- [ ] Did you use a single `browser_wait_for()` call with appropriate timeout?
- [ ] Did you avoid manual polling loops?
- [ ] Did you set timeout to 120s for AI responses?
- [ ] Did you check for multiple possible response indicators?
- [ ] Did you let auto-retry handle the timing?

**If using manual polling, you're using outdated patterns that should be replaced.**

---

## Common Mistakes to Avoid

### ❌ Navigation Errors
- **Wrong:** Using external URLs in Market Parser tests
- **Wrong:** Not checking if backend (0.0.0.0:8000) is running
- **Wrong:** Missing http:// protocol in URLs

### ❌ Element Interaction Errors  
- **Wrong:** Clicking without getting element refs from snapshot
- **Wrong:** Using generic element descriptions instead of Market Parser specific ones
- **Wrong:** Not waiting for dynamic content to load

### ❌ Content Validation Errors
- **Wrong:** Looking for generic success messages instead of "🎯 KEY TAKEAWAYS"
- **Wrong:** Not validating financial emoji indicators (📈📉💰)
- **Wrong:** Ignoring Market Parser specific response format

### ❌ Timing Errors
- **Wrong:** Using timeouts < 120s for backend responses  
- **Wrong:** Not waiting for React component mounting
- **Wrong:** Not accounting for Polygon.io API latency

---

## Required Tool Sequence for Market Parser

### Basic Test Setup:
```
1. browser_install
2. browser_navigate (to 127.0.0.1:3000)
3. browser_snapshot (get current state)
```

### Financial Query Testing:
```
4. browser_type (financial query + submit)
5. browser_wait_for (response indicators)
6. browser_snapshot (verify response)
7. browser_evaluate (extract validation data)
```

### Cleanup:
```
8. browser_close
```

**Always follow this sequence for reliable Market Parser testing.**