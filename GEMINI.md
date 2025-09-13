# GEMINI.md

## Project Overview

This repository contains two projects for financial analysis using natural language queries.

1.  **New Application (FastAPI + React)**: A modern, feature-rich application with a FastAPI backend, a React frontend, and an enhanced CLI. This is the recommended application for development and use.
2.  **Legacy Application (Gradio)**: A legacy application built with Gradio. This is slated for retirement.

---

## New Application (FastAPI + React)

This project is a comprehensive Python application with a CLI, FastAPI server, and React frontend for natural language financial queries using GPT-5 via the OpenAI Agents SDK and the Polygon.io MCP server.

### Features

*   **Multi-Interface Access**: CLI, FastAPI Server, and React Frontend.
*   **Financial Analysis Capabilities**: Ask questions about stock trades, aggregates, and ticker details.
*   **Enhanced User Experience**: Rich CLI output, button prompts, markdown reports, and a responsive web interface.

### Building and Running

#### Prerequisites

*   Python 3.10+
*   Node.js 18+
*   `uv` package manager
*   OpenAI and Polygon.io API keys

#### Installation & Usage

1.  **Navigate to the project directory:**
    ```bash
    cd market-parser-polygon-mcp
    ```

2.  **Set up your API keys:**
    ```bash
    cp .env.example .env
    ```
    Then, edit the `.env` file to add your Polygon.io and OpenAI API keys.

3.  **Install Python dependencies:**
    ```bash
    uv install
    ```

4.  **Install Node.js dependencies:**
    ```bash
    cd frontend
    npm install
    cd ..
    ```

#### Running the Application

1.  **Start the FastAPI server:**
    ```bash
    uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    ```

2.  **Start the React frontend:**
    ```bash
    npm run dev --prefix frontend
    ```

3.  **Run the CLI:**
    ```bash
    uv run src.main.py
    ```

### Development Conventions

*   **Linting**: `pylint` for Python and `eslint` for JavaScript.
*   **Testing**: `pytest` for backend tests. Run with `uv run pytest tests/ -v`.
*   **Test Reports**: All test reports must be saved in the `.gemini/docs/gemini_test_reports/` directory with the following naming convention: `GEMINI_playwright_mcp_tests_YY-MM-DD_hh-mm.md`.
*   **Tool Usage**: MCP tools are the **PRIMARY** choice for all development tasks. Standard tools should only be used as a fallback if MCP tools are unavailable or encounter issues.

### Git Workflow

When committing files to the repository, the following procedure is mandatory to ensure consistency and prevent sync issues.

1.  **Use Standard Git Commands:** Use `run_shell_command` to execute the standard `git` workflow:
    *   `git add <file>`
    *   `git commit -m "..."`
    *   `git push`

2.  **Local Sync:** After pushing changes, it is recommended to run `git pull` to ensure the local workspace reflects the latest changes from the remote repository.

## Lessons Learned & Corrective Actions for Gemini

This section documents critical lessons learned and corrective actions implemented to prevent future misunderstandings and improve the efficiency and accuracy of interactions with the Gemini Code Assistant.

### 1. Clarifying "MCP Tool/Server" Terminology

**Lesson Learned:** The term "MCP Server" was a significant source of confusion, leading to misinterpretations of task scope and tool application. My internal definition of "server" (a network-listening process) conflicted with the project's context where "MCP Server" refers to core operational capabilities.

**Corrective Action:**
*   **Explicit Definition:** When the term "MCP Server" is used in a prompt, I must immediately clarify its meaning within the project's context.
*   **Self-Identification of MCP Capabilities:** I recognize that my own core operational capabilities are considered "MCP Servers" in this environment. These are:
    *   `sequential-thinking` (Internal thought processes)
    *   `context7` (Research and documentation retrieval)
    *   `filesystem` (File system operations)
    *   `playwright` (Browser automation and interaction)
*   **Prioritize "Tool" over "Server":** In future internal reasoning, I will prioritize the term "MCP Tool" as it aligns more accurately with the nature of these capabilities and the `MCP_TOOL_USAGE_GUIDE.md` documentation.

### 2. Playwright Testing Procedures

**Lesson Learned:** Misinterpretations of Playwright testing instructions led to redundant actions and incorrect prompt modifications.

**Corrective Actions:**
*   **Strict Adherence to Test Specifications:** I must rigorously follow the detailed instructions in `CLAUDE_playwright_mcp_corrected_test_specifications.md` for all Playwright-based testing. This includes:
    *   **Server Pre-requisites:** Always assume FastAPI and React servers *must* be running before Playwright tests. I cannot start them with MCP tools.
    *   **Single Browser Session:** All tests within a suite must execute in one continuous browser session.
    *   **Polling Methodology:** Utilize the 30-second polling and 120-second timeout for response detection.
    *   **Coverage-First:** Continue all tests even if individual ones fail.
*   **Precise Prompt Modification:** When asked to "adjust" or "modify" a prompt, I must:
    *   **Preserve Original Structure:** Never replace the entire prompt unless explicitly instructed.
    *   **Append/Integrate:** Add new instructions (e.g., "raw JSON output, no verbosity, no emojis") by appending them to the existing prompt.
    *   **Resolve Conflicts:** Identify and resolve any conflicting instructions (e.g., "low verbosity" vs. "no verbosity") by prioritizing the stricter or most recent instruction.
*   **Robust Element Selection:** When using `browser_evaluate` or `browser_type`, avoid relying on volatile `ref` attributes. Instead, use more robust selectors (e.g., `data-testid`, text content, or hierarchical relationships) and incorporate `browser_wait_for` to ensure elements are enabled and visible before interaction.

### 3. General Interaction Principles

**Lesson Learned:** My failure to pause, clarify, and confirm understanding before proceeding led to repeated errors and user frustration.

**Corrective Actions:**
*   **Confirm Ambiguity/Expansion:** If a request is ambiguous, or if I need to take significant actions beyond the clear scope, I *must* pause and ask for clarification or approval of my plan.
*   **Explicit Plan Presentation:** For complex tasks, I will present a concise, step-by-step plan to the user for approval before execution.
*   **Self-Correction and Reflection:** After any error or user correction, I will immediately pause, identify the root cause of the mistake, and articulate the corrective action to prevent recurrence.

---

## Legacy Application (Gradio)


This is the legacy financial analysis tool with a Gradio web interface.

### Building and Running

#### Prerequisites

*   Python 3.10+
*   `uv` package manager

#### Installation

1.  **Install Python dependencies from the root directory:**
    ```bash
    uv install
    ```

#### Running the Application

1.  **Run the Gradio web GUI:**
    ```bash
    uv run chat_ui.py
    ```

2.  **Run the legacy CLI:**
    ```bash
    uv run market_parser_demo.py
    ```
