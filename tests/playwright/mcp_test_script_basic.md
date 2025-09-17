# MCP Test Script: Basic Functionality Test Sequence (Self-Contained)

## Test Objective
To perform a basic functional test of the Market Parser application by executing a sequence of three core interactions: a "Market Status" query, an "NVDA Snapshot" query, and a "Support & Resistance" button click, verifying proper responses for each using intelligent two-phase auto-retry detection. This script ensures the application's core AI and UI functionalities are operational with enhanced response detection.

## Global Configuration & Assumptions
*   **Application URLs:**
    *   Frontend: `http://127.0.0.1:3000`
    *   Backend: `http://127.0.0.1:8000`
*   **Auto-Retry Detection:** Two-phase intelligent detection (Phase 1: ANY response detection, Phase 2: content validation).
*   **Max AI Response Timeout:** 120 seconds per AI-driven step.
*   **Tool Access:** Assumes direct access to `default_api` tools (e.g., `run_shell_command`, `browser_navigate`, `browser_snapshot`, `browser_type`, `browser_press_key`, `browser_wait_for`, `browser_click`, `browser_console_messages`, `browser_network_requests`, `write_file`, `read_file`).
*   **AI Capabilities:** Assumes AI can parse YAML/JSON output from tools, perform string formatting, and manage basic control flow (loops, conditionals).

## Prerequisites & Environment Setup

### Step P1: Start Application Servers
*   **Action:** Start the Market Parser application (backend and frontend) in the background.
    *   **Tool:** `run_shell_command`
    *   **Parameters:** `command = "npm run start:app &"`
    *   **Expected Output:** Command executes without immediate errors.
    *   **Lessons Learned:** The AI should capture the PID of this background process for later cleanup if `pkill` is not sufficient.
*   **Action:** Wait for application servers to be ready.
    *   **AI Action:** Implement a retry loop for this verification.
    *   **Loop:** Repeat up to 10 times with a 5-second delay between attempts.
    *   **Tool:** `run_shell_command`
    *   **Parameters:** `command = "curl -s http://127.0.0.1:8000/health && curl -s http://127.0.0.1:3000/ && echo 'Application ready.'"`
    *   **Expected Output:** "Application ready."
    *   **Corrective Action:** If this command fails after all retries, declare a setup failure and terminate the test.

## Test Steps

### Test 1: Market Status Query

#### Step 1.1: Navigate to Frontend
*   **Action:** Navigate to the Market Parser frontend.
    *   **Tool:** `browser_navigate`
    *   **Parameters:** `url = "http://127.0.0.1:3000"`
    *   **Expected Output:** Page loaded successfully, title "Market Parser OpenAI Chat".
    *   **Corrective Action:** If navigation fails (e.g., `ERR_CONNECTION_REFUSED` or `browser not found` error), then execute `browser_install` and restart the entire test sequence from 'Prerequisites & Environment Setup'.

#### Step 1.2: Type and Send Market Status Query
*   **Action:** Get a snapshot of the current page state to identify the message input field.
    *   **Tool:** `browser_snapshot`
    *   **Parameters:** None
    *   **Expected Output:** A YAML snapshot. **AI Action:** Parse the snapshot to find the `ref` for the message input textbox (e.g., `e19` or `textarea[placeholder*='message']`). Store this `ref` in a variable (e.g., `MESSAGE_INPUT_REF`).
*   **Action:** Type the "Market Status" query into the message input field.
    *   **Tool:** `browser_type`
    *   **Parameters:**
        *   `element = "Message input field"`
        *   `ref = "[MESSAGE_INPUT_REF]"`
        *   `text = "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"`
*   **Action:** Press Enter to send the message.
    *   **Tool:** `browser_press_key`
    *   **Parameters:** `key = "Enter"`

#### Step 1.3: Wait for Market Status Response (Auto-Retry Detection)
*   **Action:** Wait for the AI response using intelligent two-phase auto-retry detection.
    *   **Phase 1 - ANY Response Detection:**
        *   **AI Action:** Monitor for ANY response completion using multiple detection methods:
            *   Loading indicators disappearing (e.g., loading spinners, "Thinking..." text)
            *   Response containers becoming visible (e.g., new message elements)
            *   Message count increases in chat interface
            *   DOM changes indicating response completion
        *   **Timeout:** 120 seconds maximum for Phase 1 detection
        *   **Tools:** Use `browser_wait_for`, `browser_snapshot`, and `browser_evaluate` for dynamic detection
    *   **Phase 2 - Content Validation:**
        *   **AI Action:** Once ANY response is detected, immediately validate content:
            *   Check for market status keywords ("market", "status", "trading", "session", "hours")
            *   Verify financial emojis presence (📈, 📉, 💰, 📊)
            *   Ensure minimum content length (>50 characters)
            *   Validate response structure (KEY TAKEAWAYS, analysis content)
        *   **Result:** Determine PASS (correct market status response) or FAIL (incorrect/incomplete response)
    *   **Lessons Learned:** Two-phase detection eliminates polling overhead and provides immediate detection with proper validation.

#### Step 1.4: Verify Market Status Response (Enhanced Validation)
*   **Action:** Get a snapshot of the page after auto-retry detection completes.
    *   **Tool:** `browser_snapshot`
    *   **Parameters:** None
    *   **AI Action:** Parse the snapshot using the Phase 2 validation results:
        *   Confirm market status content detection from Phase 2
        *   Verify financial emojis and response structure
        *   Cross-reference validation results with snapshot content
        *   Record detailed verification result (PASS/FAIL with specific reasons)
    *   **Expected Output:** Snapshot confirms auto-retry detection accuracy and response quality.

### Test 2: NVDA Snapshot Query

#### Step 2.1: Type and Send NVDA Snapshot Query
*   **Action:** Type the "NVDA Snapshot" query into the message input field.
    *   **Tool:** `browser_type`
    *   **Parameters:**
        *   `element = "Message input field"`
        *   `ref = "[MESSAGE_INPUT_REF]"`
        *   `text = "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"`
*   **Action:** Press Enter to send the message.
    *   **Tool:** `browser_press_key`
    *   **Parameters:** `key = "Enter"`

#### Step 2.2: Wait for NVDA Snapshot Response (Auto-Retry Detection)
*   **Action:** Wait for the AI response using intelligent two-phase auto-retry detection.
    *   **Phase 1:** Same ANY response detection as Step 1.3
    *   **Phase 2 - NVDA-Specific Validation:**
        *   Check for ticker-specific content ("NVDA", "NVIDIA", stock analysis keywords)
        *   Verify financial emojis and metrics (price, volume, market cap indicators)
        *   Ensure comprehensive analysis content (>100 characters)
        *   Validate ticker-specific response structure
        *   **Result:** PASS (correct NVDA analysis) or FAIL (generic/incorrect response)
    *   **Expected Output:** Auto-retry detection with NVDA-specific validation.

#### Step 2.3: Verify NVDA Snapshot Response (Enhanced Validation)
*   **Action:** Get a snapshot of the page after auto-retry detection completes.
    *   **Tool:** `browser_snapshot`
    *   **Parameters:** None
    *   **AI Action:** Parse the snapshot using Phase 2 NVDA-specific validation results:
        *   Confirm NVDA ticker analysis detection
        *   Verify stock-specific metrics and analysis depth
        *   Cross-reference validation results with snapshot content
        *   Record detailed verification result (PASS/FAIL with NVDA-specific criteria)
    *   **Expected Output:** Snapshot confirms NVDA analysis accuracy and completeness.

### Test 3: Support & Resistance Button Click

#### Step 3.1: Identify Support & Resistance Button
*   **Action:** Get a snapshot of the current page state to identify the "Support & Resistance" button.
    *   **Tool:** `browser_snapshot`
    *   **Parameters:** None
    *   **Expected Output:** Snapshot containing element references. **AI Action:** Parse the snapshot to find the `ref` for the "Support & Resistance" button (e.g., `e45` or `button[data-testid='support-resistance-button']`). Store this `ref` in a variable (e.g., `SR_BUTTON_REF`).

#### Step 3.2: Click Support & Resistance Button
*   **Action:** Click the "Support & Resistance" button.
    *   **Tool:** `browser_click`
    *   **Parameters:**
        *   `element = "Support Resistance Analysis button"`
        *   `ref = "[SR_BUTTON_REF]"`

#### Step 3.3: Wait for Support & Resistance Response (Auto-Retry Detection)
*   **Action:** Wait for the AI response using intelligent two-phase auto-retry detection.
    *   **Phase 1:** Same ANY response detection as Step 1.3
    *   **Phase 2 - Support & Resistance Validation:**
        *   Check for technical analysis keywords ("support", "resistance", "levels", "technical")
        *   Verify technical analysis emojis and indicators (📊, 📈, 📉, technical markers)
        *   Ensure technical analysis content (charts, levels, price points)
        *   Validate button-triggered response structure
        *   **Result:** PASS (correct S&R analysis) or FAIL (missing technical content)
    *   **Expected Output:** Auto-retry detection with technical analysis validation.

#### Step 3.4: Verify Support & Resistance Response (Enhanced Validation)
*   **Action:** Get a snapshot of the page after auto-retry detection completes.
    *   **Tool:** `browser_snapshot`
    *   **Parameters:** None
    *   **AI Action:** Parse the snapshot using Phase 2 S&R validation results:
        *   Confirm technical analysis content detection
        *   Verify support/resistance levels and technical indicators
        *   Cross-reference validation results with snapshot content
        *   Record detailed verification result (PASS/FAIL with technical analysis criteria)
    *   **Expected Output:** Snapshot confirms technical analysis accuracy and depth.

## Report Generation

### Step R1: Gather Test Data
*   **Action:** Gather console messages from the entire test sequence.
    *   **Tool:** `browser_console_messages`
    *   **Parameters:** None
    *   **Expected Output:** Array of console log entries. Store in a variable (e.g., `CONSOLE_LOGS`).
*   **Action:** Gather network requests from the entire test sequence.
    *   **Tool:** `browser_network_requests`
    *   **Parameters:** None
    *   **Expected Output:** Array of network request details. Store in a variable (e.g., `NETWORK_REQUESTS`).

### Step R2: Format and Save Report
*   **Action:** Format the gathered data into a single Markdown test report with auto-retry methodology details.
    *   **AI Action:**
        *   Get current timestamp (YYYYMMDD_HHMM).
        *   Construct a Markdown string including:
            *   Auto-retry detection phase timings (Phase 1 and Phase 2 times)
            *   Detailed validation results for each test (PASS/FAIL with specific criteria)
            *   Performance classifications (Good/OK/Slow based on response times)
            *   Detection method effectiveness (which methods succeeded)
            *   Collected test results, `CONSOLE_LOGS`, and `NETWORK_REQUESTS`
        *   Determine overall test result with auto-retry methodology assessment.
    *   **Naming Convention:** `mcp_auto_retry_test_report_[YYYYMMDD_HHMM].md`
    *   **File Path:** `/home/1000211866/Github/market-parser-polygon-mcp/docs/test_reports/mcp/`
*   **Action:** Save the generated report.
    *   **Tool:** `write_file`
    *   **Parameters:**
        *   `file_path = "/home/1000211866/Github/market-parser-polygon-mcp/docs/test_reports/gemini/gemini_basic_test_report_[CURRENT_TIMESTAMP].md"`
        *   `content = "[FORMATTED_MARKDOWN_REPORT_STRING]"`
    *   **Expected Output:** Confirmation of file creation.

## Cleanup

### Step C1: Close Browser Session
*   **Action:** Close the browser session.
    *   **Tool:** `browser_close`
    *   **Parameters:** None
    *   **Expected Output:** Browser closed confirmation.

### Step C2: Stop Application Processes
*   **Action:** Stop the background application process.
    *   **Tool:** `run_shell_command`
    *   **Parameters:** `command = "pkill -f \"npm run start:app\""`
    *   **Expected Output:** Application processes terminated.
    *   **Lessons Learned:** Using `pkill -f` is more reliable for stopping background `npm` processes than trying to capture and `kill` a specific PID, as it targets the command string.