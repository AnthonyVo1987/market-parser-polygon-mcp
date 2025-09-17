# MCP Test Script: Basic Functionality Test Sequence (Self-Contained)

## Test Objective
To perform a basic functional test of the Market Parser application by executing a sequence of three core interactions: a "Market Status" query, an "NVDA Snapshot" query, and a "Support & Resistance" button click, verifying proper responses for each. This script ensures the application's core AI and UI functionalities are operational.

## Global Configuration & Assumptions
*   **Application URLs:**
    *   Frontend: `http://127.0.0.1:3000`
    *   Backend: `http://127.0.0.1:8000`
*   **Polling Interval:** 10 seconds for AI responses.
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

#### Step 1.3: Wait for Market Status Response
*   **Action:** Wait for the AI response using a polling mechanism.
    *   **AI Action (Polling Logic):
        *   Initialize `total_time_elapsed = 0`.
        *   **Loop:** While `total_time_elapsed < 120` seconds:
            *   **Tool:** `browser_wait_for`
            *   **Parameters:**
                *   `text = "🎯 KEY TAKEAWAYS"`
                *   `time = 10` (maximum wait time for this specific `browser_wait_for` call)
            *   **Expected Output:** If successful, the response containing "🎯 KEY TAKEAWAYS" is visible.
            *   **AI Action (Conditional):
                *   If `browser_wait_for` succeeds: Mark this step as PASSED. Break loop.
                *   If `browser_wait_for` times out: Increment `total_time_elapsed` by 10 seconds. Continue loop.
        *   If loop finishes without success: Mark this step as FAILED.
    *   **Lessons Learned:** Previous attempts experienced timeouts. The 10-second polling interval within a 120-second total timeout is crucial for AI responses.

#### Step 1.4: Verify Market Status Response
*   **Action:** Get a snapshot of the page after the response to verify content.
    *   **Tool:** `browser_snapshot`
    *   **Parameters:** None
    *   **AI Action:** Parse the snapshot to confirm the presence of "🎯 KEY TAKEAWAYS" and relevant financial emojis (e.g., 📈, 📉, 💰) in the latest message. Record verification result (PASSED/FAILED).
    *   **Expected Output:** Snapshot confirms correct response format and content.

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

#### Step 2.2: Wait for NVDA Snapshot Response
*   **Action:** Wait for the AI response using a polling mechanism.
    *   **AI Action (Polling Logic):** Same as Step 1.3.
    *   **Tool:** `browser_wait_for`
    *   **Parameters:**
        *   `text = "📈 NVIDIA Corporation"` (or "🎯 KEY TAKEAWAYS")
        *   `time = 10`
    *   **Expected Output:** Response containing NVDA analysis.

#### Step 2.3: Verify NVDA Snapshot Response
*   **Action:** Get a snapshot of the page after the response to verify content.
    *   **Tool:** `browser_snapshot`
    *   **Parameters:** None
    *   **AI Action:** Parse the snapshot to confirm the presence of NVDA-specific analysis and relevant financial emojis. Record verification result (PASSED/FAILED).
    *   **Expected Output:** Snapshot confirms correct response for NVDA.

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

#### Step 3.3: Wait for Support & Resistance Response
*   **Action:** Wait for the AI response using a polling mechanism.
    *   **AI Action (Polling Logic):** Same as Step 1.3.
    *   **Tool:** `browser_wait_for`
    *   **Parameters:**
        *   `text = "📊 Support and Resistance Levels"` (or "🎯 KEY TAKEAWAYS")
        *   `time = 10`
    *   **Expected Output:** Response containing support and resistance analysis.

#### Step 3.4: Verify Support & Resistance Response
*   **Action:** Get a snapshot of the page after the response to verify content.
    *   **Tool:** `browser_snapshot`
    *   **Parameters:** None
    *   **AI Action:** Parse the snapshot to confirm the presence of support and resistance analysis and relevant financial emojis. Record verification result (PASSED/FAILED).
    *   **Expected Output:** Snapshot confirms correct response for Support & Resistance.

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
*   **Action:** Format the gathered data into a single Markdown test report.
    *   **AI Action:**
        *   Get current timestamp (YYYYMMDD_HHMM).
        *   Construct a Markdown string using the collected test results (PASSED/FAILED for each step), `CONSOLE_LOGS`, and `NETWORK_REQUESTS`.
        *   Determine overall test result (PASSED if all steps passed, FAILED otherwise).
    *   **Naming Convention:** `gemini_basic_test_report_[YYYYMMDD_HHMM].md`
    *   **File Path:** `/home/1000211866/Github/market-parser-polygon-mcp/docs/test_reports/gemini/`
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