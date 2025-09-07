# Gemini Guide: Integrating Playwright for Automated React GUI Testing

**Author:** Gemini
**Date:** 2025-09-06
**Version:** 1.0

## 1. Introduction to Playwright

Playwright is a modern, powerful, and reliable framework for web testing and automation. Developed by Microsoft, it enables cross-browser testing of Chromium (Google Chrome, Microsoft Edge), Firefox, and WebKit (Apple Safari) with a single API.

### Key Capabilities:

*   **Cross-Browser:** Write one test and run it on all modern browsers.
*   **Cross-Platform:** Run tests on Windows, Linux, and macOS.
*   **Cross-Language:** Use the Playwright API in TypeScript, JavaScript, Python, .NET, and Java.
*   **Auto-Waits:** Playwright waits for elements to be actionable before performing actions, eliminating a major source of flakiness in tests.
*   **Rich Introspection:** Tools like the Playwright Inspector and Trace Viewer provide deep insights into test execution, making debugging easier.
*   **Network Interception:** Intercept and mock network requests to test edge cases and isolate the frontend from the backend.
*   **Authentication:** Save authentication state and reuse it in tests, bypassing repetitive login steps.
*   **Parallel Execution:** Run tests in parallel across multiple browsers and workers to speed up test execution.

## 2. Recommended Method for Our Environment

For the current development environment, which includes a FastAPI backend and a React frontend, the **Playwright CLI method with `pytest` is the recommended approach** for automated GUI testing.

### Rationale:

| Criteria              | Playwright CLI with `pytest`                                                              | Playwright MCP Server                                                                      |
| --------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Automation**        | Excellent. Tests are written in Python and can be fully automated in a CI/CD pipeline.      | Excellent. Designed for AI agent-driven automation.                                        |
| **Ease of Setup**     | **Good.** Requires installing Python dependencies and browser binaries, which is straightforward. | Moderate. Requires configuring and running a separate server process.                      |
| **Ease of Use**       | **Excellent.** Writing tests in Python with the `pytest-playwright` plugin is intuitive.    | Good. Requires understanding the MCP protocol and interacting with the server.            |
| **Token Usage**       | **Lower.** The AI agent's role is to generate the Python test scripts, not to drive the UI. | Higher. The AI agent needs to send commands to the MCP server for every interaction.       |
| **Flexibility**       | High. Full control over the test environment and execution.                               | Moderate. Limited to the capabilities exposed by the MCP server.                           |
| **Ecosystem**         | Rich. Leverages the extensive Python and `pytest` ecosystems for reporting, plugins, etc.   | Limited. Dependent on the MCP ecosystem.                                                   |

While the Playwright MCP Server is a powerful tool for AI-driven browser interaction, the CLI method offers a more traditional, robust, and cost-effective approach for automated GUI testing in our specific context. It allows for the creation of a maintainable and scalable test suite that can be easily integrated into our existing development and CI/CD workflows.

## 3. Playwright CLI Method with `pytest`

This section provides a full tutorial on setting up, installing, integrating, and using the Playwright CLI method with `pytest` for testing the React GUI.

### 3.1. Setup and Installation

1.  **Install Python Dependencies:**

    This assumes you have already set up the Python environment for the FastAPI application.

    ```bash
    # Navigate to the project root
    cd gpt5-openai-agents-sdk-polygon-mcp

    # Install pytest and the playwright plugin
    uv pip install pytest pytest-playwright
    ```

2.  **Install Playwright Browsers:**

    This command downloads the browser binaries (Chromium, Firefox, WebKit) that Playwright uses.

    ```bash
    uv run playwright install
    ```

### 3.2. Integration

1.  **Create a Test Directory:**

    Create a new directory to store the GUI tests.

    ```bash
    mkdir -p gpt5-openai-agents-sdk-polygon-mcp/tests/gui
    ```

2.  **Create a Sample Test File:**

    Create a new file named `gpt5-openai-agents-sdk-polygon-mcp/tests/gui/test_app.py`.

    ```python
    import re
    from playwright.sync_api import Page, expect

    def test_react_app_loads(page: Page):
        """
        Tests that the React application loads and the main title is visible.
        """
        # Navigate to the React application
        page.goto("http://localhost:3000") # Assuming the React dev server is running on port 3000

        # Expect the main heading to be visible
        heading = page.get_by_role("heading", name=re.compile("Financial Analysis", re.IGNORECASE))
        expect(heading).to_be_visible()

    def test_perform_query(page: Page):
        """
        Tests performing a simple query and displaying the result.
        """
        page.goto("http://localhost:3000")

        # Find the query input and enter a query
        query_input = page.get_by_placeholder("Ask a question...")
        query_input.fill("What is the latest price of AAPL?")
        query_input.press("Enter")

        # Wait for the response to appear
        response_element = page.locator(".response-class") # Replace with the actual selector for the response
        expect(response_element).to_be_visible()
        expect(response_element).not_to_be_empty()
    ```

### 3.3. Usage

1.  **Start the React Frontend:**

    Before running the tests, ensure the React development server is running.

    ```bash
    npm run dev --prefix gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
    ```

2.  **Run the Tests:**

    Execute the tests using `pytest`.

    ```bash
    uv run pytest gpt5-openai-agents-sdk-polygon-mcp/tests/gui
    ```

3.  **View the Test Report:**

    After the tests run, you can view a detailed HTML report.

    ```bash
    uv run pytest --headed gpt5-openai-agents-sdk-polygon-mcp/tests/gui # Run in headed mode to see the browser
    uv run playwright show-report
    ```

## 4. Playwright MCP Server Method

This section provides a full tutorial on setting up, installing, integrating, and using the Playwright MCP Server. This method is more suitable for interactive, AI-driven testing rather than automated test suites.

### 4.1. Setup and Installation

1.  **Install the Playwright MCP Server:**

    The MCP server is an NPM package.

    ```bash
    npm install -g @playwright/mcp
    ```

2.  **Configure the MCP Server:**

    The MCP server can be configured in your editor's settings. For example, in VS Code's `.vscode/settings.json`:

    ```json
    {
      "mcp.servers": {
        "playwright": {
          "command": "npx",
          "args": ["@playwright/mcp@latest"],
          "enabled": true
        }
      }
    }
    ```

### 4.2. Integration

The Playwright MCP server is integrated with the AI agent through the MCP protocol. The agent sends commands to the server to control the browser.

### 4.3. Comprehensive Test Plan

This test plan outlines the steps for a comprehensive "dry run" of the React GUI using the Playwright MCP Server.

**Test Configuration:**
*   **Default Timeout:** Each browser interaction will have a timeout of 120 seconds to accommodate for AI response times.
*   **Reporting:** A detailed markdown report will be generated and saved to `.gemini/docs/gemini_test_reports/` with the naming convention `GEMINI_playwright_mcp_tests_YY-MM-DD_hh-mm.md`.

**Execution Steps:**

1.  **Start the MCP Server:**
    ```bash
    npx @playwright/mcp@latest --port 8931
    ```

2.  **Start the React Frontend:**
    ```bash
    npm run dev --prefix gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
    ```

3.  **Navigate to the page:**
    ```json
    {
      "tool": "browser_navigate",
      "url": "http://localhost:3000"
    }
    ```

4.  **Take an initial snapshot:**
    ```json
    {
      "tool": "browser_snapshot"
    }
    ```

#### Module 1: Initial Prompts

**Test Case 1.1: Market Status**
*   **Action:** Type the query.
    ```json
    {
      "tool": "browser_type",
      "element": "The query input field",
      "ref": "...",
      "text": "Market Status: Low Verbosity, Raw response format output"
    }
    ```
*   **Action:** Press Enter.
    ```json
    {
      "tool": "browser_press_key",
      "key": "Enter"
    }
    ```
*   **Action:** Wait for the response and take a snapshot.
    ```json
    {
      "tool": "browser_wait_for",
      "time": 120
    }
    ```
    ```json
    {
      "tool": "browser_snapshot"
    }
    ```

**Test Case 1.2: Single Ticker Snapshot (NVDA)**
*   **Action:** Type the query.
    ```json
    {
      "tool": "browser_type",
      "element": "The query input field",
      "ref": "...",
      "text": "Single Ticker Snapshot: NVDA, Low Verbosity, Raw response format output"
    }
    ```
*   **Action:** Press Enter.
    ```json
    {
      "tool": "browser_press_key",
      "key": "Enter"
    }
    ```
*   **Action:** Wait for the response and take a snapshot.
    ```json
    {
      "tool": "browser_wait_for",
      "time": 120
    }
    ```
    ```json
    {
      "tool": "browser_snapshot"
    }
    ```

**Test Case 1.3: Single Ticker Snapshot (SPY)**
*   **Action:** Type the query.
    ```json
    {
      "tool": "browser_type",
      "element": "The query input field",
      "ref": "...",
      "text": "Single Ticker Snapshot: SPY, Low Verbosity, Raw response format output"
    }
    ```
*   **Action:** Press Enter.
    ```json
    {
      "tool": "browser_press_key",
      "key": "Enter"
    }
    ```
*   **Action:** Wait for the response and take a snapshot.
    ```json
    {
      "tool": "browser_wait_for",
      "time": 120
    }
    ```
    ```json
    {
      "tool": "browser_snapshot"
    }
    ```

**Test Case 1.4: Single Ticker Snapshot (WDC)**
*   **Action:** Type the query.
    ```json
    {
      "tool": "browser_type",
      "element": "The query input field",
      "ref": "...",
      "text": "Single Ticker Snapshot: WDC, Low Verbosity, Raw response format output"
    }
    ```
*   **Action:** Press Enter.
    ```json
    {
      "tool": "browser_press_key",
      "key": "Enter"
    }
    ```
*   **Action:** Wait for the response and take a snapshot.
    ```json
    {
      "tool": "browser_wait_for",
      "time": 120
    }
    ```
    ```json
    {
      "tool": "browser_snapshot"
    }
    ```

**Test Case 1.5: Full Market Snapshot**
*   **Action:** Type the query.
    ```json
    {
      "tool": "browser_type",
      "element": "The query input field",
      "ref": "...",
      "text": "Full Market Snapshot: NVDA, SPY, QQQ, IWM, Low Verbosity, Raw response format output"
    }
    ```
*   **Action:** Press Enter.
    ```json
    {
      "tool": "browser_press_key",
      "key": "Enter"
    }
    ```
*   **Action:** Wait for the response and take a snapshot.
    ```json
    {
      "tool": "browser_wait_for",
      "time": 120
    }
    ```
    ```json
    {
      "tool": "browser_snapshot"
    }
    ```

#### Module 2: Comprehensive Functionality

**Test Case 2.1: Technical Analysis**
*   **Action:** Type the query.
    ```json
    {
      "tool": "browser_type",
      "element": "The query input field",
      "ref": "...",
      "text": "Technical Analysis for MSFT"
    }
    ```
*   **Action:** Press Enter and wait for response.
    ```json
    {
      "tool": "browser_press_key",
      "key": "Enter"
    }
    ```
    ```json
    {
      "tool": "browser_wait_for",
      "time": 120
    }
    ```

**Test Case 2.2: Support Resistance Analysis**
*   **Action:** Type the query.
    ```json
    {
      "tool": "browser_type",
      "element": "The query input field",
      "ref": "...",
      "text": "Support Resistance Analysis for AAPL"
    }
    ```
*   **Action:** Press Enter and wait for response.
    ```json
    {
      "tool": "browser_press_key",
      "key": "Enter"
    }
    ```
    ```json
    {
      "tool": "browser_wait_for",
      "time": 120
    }
    ```

**Test Case 2.3: UI Button Tests**
*   **Action:** Click "Copy chat as markdown to clipboard".
    ```json
    {
      "tool": "browser_click",
      "element": "Copy chat as markdown to clipboard",
      "ref": "..."
    }
    ```
*   **Action:** Click "Copy chat as JSON to clipboard".
    ```json
    {
      "tool": "browser_click",
      "element": "Copy chat as JSON to clipboard",
      "ref": "..."
    }
    ```
*   **Action:** Click "Copy most recent AI response to clipboard as markdown".
    ```json
    {
      "tool": "browser_click",
      "element": "Copy most recent AI response to clipboard as markdown",
      "ref": "..."
    }
    ```
*   **Action:** Click "Copy most recent user request to clipboard as markdown".
    ```json
    {
      "tool": "browser_click",
      "element": "Copy most recent user request to clipboard as markdown",
      "ref": "..."
    }
    ```


This method is powerful for exploratory and interactive testing driven by an AI agent, but as mentioned, it is not the recommended approach for building a repeatable, automated test suite for our project.
