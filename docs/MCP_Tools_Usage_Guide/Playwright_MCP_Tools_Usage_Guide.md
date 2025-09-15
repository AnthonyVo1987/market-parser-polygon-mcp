# Playwright MCP Tools Usage Guide for Market Parser Application

**Target Audience:** AI Coding Agents working on the Market Parser financial analysis application  
**Purpose:** Specific guidance for proper Playwright MCP tool usage in our FastAPI + React financial app context

---

## Application Context

**Market Parser Application Stack:**
- **Backend**: FastAPI server on http://0.0.0.0:8000 (accessible via http://127.0.0.1:8000 for testing)
- **Frontend**: React + Vite on http://127.0.0.1:3000
- **Production**: Static build on http://127.0.0.1:5500
- **Key Features**: Financial chat interface, analysis buttons, emoji-based responses, Polygon.io data integration

**Network Configuration Notes:**
- Backend binds to 0.0.0.0 for network accessibility but AI agents should use 127.0.0.1:8000 for testing
- Frontend strictly binds to 127.0.0.1:3000 with no dynamic port allocation
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

**⚠️ IMPORTANT: AI responses take 30-90 seconds on average. Never expect immediate responses!**

### Testing Timeline Requirements
- **Per Test Timeout**: 120 seconds maximum
- **AI Response Time**: Typically 30-90 seconds
- **Polling Interval**: Every 30 seconds
- **Success Condition**: CORRECT response received within any 30s polling cycle
- **Failure Condition**: ONLY after 120s max timeout WITHOUT correct response

### Proper AI Response Testing Workflow

```typescript
// CORRECT: 30-second polling approach
1. Send AI query (via browser_type or browser_click)
2. Start polling every 30s using browser_wait_for with 30s timeout
3. Check for CORRECT response after each 30s poll
4. If CORRECT response found: SUCCESS (no need to wait full 120s)
5. If no response after 30s: Continue polling (NOT a failure yet)
6. Repeat polling until either:
   - CORRECT response received (SUCCESS)
   - 120s total time elapsed (TIMEOUT FAILURE)
```

### Critical Polling Rules

**✅ CORRECT Expectations:**
- First poll at 30s mark (never expect response in 5-10s)
- Continue polling every 30s until success or 120s timeout
- Only mark as failure after 120s without correct response
- Distinguish between "no response yet" vs "true timeout"

**❌ INCORRECT Expectations (Causes False Positives):**
- Expecting immediate response within 5-30 seconds
- Single 30s poll and marking as timeout failure
- Not distinguishing polling from actual timeout
- Using timeout values less than 30s for AI responses

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
**Correct Usage:** Wait for financial responses and UI updates with proper AI polling
```
Purpose: Wait for Market Parser specific content/states
Input:
  - text (string): Specific text to wait for
  - textGone (string): Text to wait for disappearance
  - time (number): Seconds to wait (30s for polling, NOT 5s)
Expected Output: Condition met or timeout
```

**Example - CORRECT AI Response Polling:**
```typescript
// CORRECT: 30-second polling for AI response
let responseReceived = false;
let totalTimeElapsed = 0;
const maxTimeout = 120; // 120 seconds total
const pollInterval = 30; // 30 seconds per poll

while (totalTimeElapsed < maxTimeout && !responseReceived) {
  try {
    // Poll for AI response every 30 seconds
    await mcp__playwright__browser_wait_for({
      text: "🎯 KEY TAKEAWAYS", // Our response format
      time: 30 // 30-second poll interval
    });
    responseReceived = true; // SUCCESS - found response!
    console.log(`✅ AI response received after ${totalTimeElapsed + 30}s`);
  } catch (error) {
    // No response yet - continue polling (NOT a failure)
    totalTimeElapsed += 30;
    console.log(`⏳ No response yet at ${totalTimeElapsed}s - continuing polling...`);
    
    if (totalTimeElapsed >= maxTimeout) {
      console.log(`❌ TRUE TIMEOUT: No response after ${maxTimeout}s`);
      throw new Error(`AI response timeout after ${maxTimeout}s`);
    }
  }
}

// Additional polling examples for different response types
// Poll for bullish indicator
await mcp__playwright__browser_wait_for({
  text: "📈", // Bullish indicator
  time: 30 // 30-second poll, NOT immediate expectation
})

// Poll for loading completion
await mcp__playwright__browser_wait_for({
  textGone: "Analyzing financial data...",
  time: 30 // 30-second poll interval
})
```

**INCORRECT Examples (Cause False Positives):**
```typescript
// ❌ WRONG: Expecting immediate response
await mcp__playwright__browser_wait_for({
  text: "🎯 KEY TAKEAWAYS",
  time: 5 // TOO SHORT - AI needs 30-90s
})

// ❌ WRONG: Single 30s poll and failing
try {
  await mcp__playwright__browser_wait_for({
    text: "🎯 KEY TAKEAWAYS",
    time: 30
  });
} catch (error) {
  throw new Error("Timeout"); // WRONG - this is just first poll!
}

// ❌ WRONG: Not accounting for AI processing time
await mcp__playwright__browser_wait_for({
  text: "📈",
  time: 10 // Too short for AI responses
})
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

### Financial Query Test Pattern (with Proper AI Polling)
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
   
// CRITICAL: Proper AI response polling (30s intervals)
5. let responseReceived = false;
   let totalTimeElapsed = 0;
   const maxTimeout = 120;
   
   while (totalTimeElapsed < maxTimeout && !responseReceived) {
     try {
       await browser_wait_for({
         text: "🎯 KEY TAKEAWAYS",
         time: 30 // 30-second poll
       });
       responseReceived = true;
       console.log(`✅ Response received after ${totalTimeElapsed + 30}s`);
     } catch (error) {
       totalTimeElapsed += 30;
       if (totalTimeElapsed >= maxTimeout) {
         throw new Error(`AI response timeout after ${maxTimeout}s`);
       }
       console.log(`⏳ Continuing to poll at ${totalTimeElapsed}s...`);
     }
   }
   
6. browser_snapshot() // Verify response content
```

### Analysis Button Test Pattern (with Proper AI Polling)
```typescript
1. browser_navigate({url: "http://127.0.0.1:3000"})
2. browser_snapshot() // Find buttons
3. browser_click({
     element: "Stock Snapshot button",
     ref: "button[2]"
   }) // Click analysis button
   
// CRITICAL: Wait for AI response with proper polling
4. let responseReceived = false;
   let totalTimeElapsed = 0;
   const maxTimeout = 120;
   
   while (totalTimeElapsed < maxTimeout && !responseReceived) {
     try {
       await browser_wait_for({
         text: "📊", // Financial data indicator
         time: 30 // 30-second poll interval
       });
       responseReceived = true;
     } catch (error) {
       totalTimeElapsed += 30;
       if (totalTimeElapsed >= maxTimeout) {
         throw new Error(`Button response timeout after ${maxTimeout}s`);
       }
     }
   }
   
5. browser_snapshot() // Verify populated query
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

## Polling vs Timeout Failure Detection (CRITICAL)

**⚠️ Most Critical Section: Prevents 95% of false positive test failures**

### Understanding the Difference

**🔄 POLLING (Expected Behavior):**
- AI Agent sends query at 0s
- First check at 30s: No response yet → CONTINUE POLLING (NOT failure)
- Second check at 60s: No response yet → CONTINUE POLLING (NOT failure)  
- Third check at 90s: Response received → SUCCESS!
- **Total Time**: 90s (within 120s limit)
- **Result**: PASS ✅

**⏰ TRUE TIMEOUT (Actual Failure):**
- AI Agent sends query at 0s
- Polling at 30s, 60s, 90s, 120s: No response
- **Total Time**: 120s elapsed without response
- **Result**: FAIL ❌

### Correct Implementation Pattern

```typescript
// ✅ CORRECT: Distinguishes polling from timeout
function waitForAIResponse(expectedText: string): Promise<boolean> {
  return new Promise(async (resolve, reject) => {
    let responseReceived = false;
    let totalTimeElapsed = 0;
    const maxTimeout = 120;
    const pollInterval = 30;
    
    while (totalTimeElapsed < maxTimeout && !responseReceived) {
      try {
        // This is a POLL, not a final timeout check
        await mcp__playwright__browser_wait_for({
          text: expectedText,
          time: pollInterval // 30-second poll
        });
        
        console.log(`✅ SUCCESS: Response found after ${totalTimeElapsed + pollInterval}s`);
        responseReceived = true;
        resolve(true);
        return;
        
      } catch (pollError) {
        // No response in this 30s window - CONTINUE POLLING
        totalTimeElapsed += pollInterval;
        console.log(`⏳ POLLING: No response at ${totalTimeElapsed}s mark - continuing...`);
        
        // Only fail if we've reached the TRUE timeout
        if (totalTimeElapsed >= maxTimeout) {
          console.log(`❌ TRUE TIMEOUT: No response after ${maxTimeout}s`);
          reject(new Error(`AI response timeout after ${maxTimeout}s`));
          return;
        }
        
        // Continue to next poll cycle
      }
    }
  });
}
```

### INCORRECT Implementations (Cause False Positives)

```typescript
// ❌ WRONG: Treats first poll as timeout
try {
  await mcp__playwright__browser_wait_for({
    text: "🎯 KEY TAKEAWAYS",
    time: 30
  });
  console.log("Success");
} catch (error) {
  // WRONG: This is just the first poll, NOT a timeout!
  throw new Error("Timeout after 30s"); // FALSE POSITIVE!
}

// ❌ WRONG: Too short timeout
try {
  await mcp__playwright__browser_wait_for({
    text: "🎯 KEY TAKEAWAYS", 
    time: 5 // Way too short for AI
  });
} catch (error) {
  throw new Error("Timeout"); // FALSE POSITIVE!
}

// ❌ WRONG: Not implementing polling loop
await mcp__playwright__browser_wait_for({
  text: "🎯 KEY TAKEAWAYS",
  time: 120 // Single 120s wait - doesn't show progress
});
```

### Key Debugging Indicators

**✅ Proper Polling Logs:**
```
⏳ POLLING: No response at 30s mark - continuing...
⏳ POLLING: No response at 60s mark - continuing... 
✅ SUCCESS: Response found after 90s
```

**❌ False Positive Logs:**
```
❌ Timeout after 30s  // WRONG - this is just first poll!
❌ Timeout after 5s   // WRONG - AI needs 30-90s
```

### Validation Checklist

Before reporting a timeout failure, verify:
- [ ] Did you poll for at least 120 seconds total?
- [ ] Did you use 30-second polling intervals?
- [ ] Did you distinguish between "no response yet" vs "true timeout"?
- [ ] Did you log each polling attempt?
- [ ] Did you only fail after 120s without ANY response?

**If any answer is "No", it's likely a false positive, not a real timeout.**

---

## Common Mistakes to Avoid

### ❌ Navigation Errors
- **Wrong:** Using external URLs in Market Parser tests
- **Wrong:** Not checking if backend (127.0.0.1:8000) is running
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