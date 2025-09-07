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
    cd gpt5-openai-agents-sdk-polygon-mcp
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
    cd frontend_OpenAI
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
    npm run dev --prefix frontend_OpenAI
    ```

3.  **Run the CLI:**
    ```bash
    uv run src.main.py
    ```

### Development Conventions

*   **Linting**: `pylint` for Python and `eslint` for JavaScript.
*   **Testing**: `pytest` for backend tests. Run with `uv run pytest tests/ -v`.
*   **Tool Usage**: MCP tools are the **PRIMARY** choice for all development tasks. Standard tools should only be used as a fallback if MCP tools are unavailable or encounter issues.

### MCP GitHub Tool Workflow & Fallback Procedure

When committing files to the repository, the following procedure is mandatory to ensure consistency and prevent sync issues.

#### 1. Primary Method: `mcp_github` Tools

This is the preferred method for all repository file operations.

1.  **Get Latest File SHA:** Before updating a file, always get its latest SHA hash using `mcp_github_get_file_contents`. This is critical to avoid conflicts.
2.  **Update Remote File:** Use `mcp_github_create_or_update_file` with the new content and the SHA obtained in the previous step.
3.  **Verify Success:** Check the tool's output to confirm the commit was created successfully.

#### 2. Automatic Fallback Procedure

If the primary method fails for any reason, the following fallback must be triggered **automatically** without user intervention.

1.  **Diagnose and Retry (Once):** If the failure is due to a SHA mismatch (a 409 Conflict error), the agent must re-fetch the latest SHA and attempt the `mcp_github_create_or_update_file` call exactly **one** more time.
2.  **Execute Fallback:** If the retry fails, or if the initial error was not a SHA mismatch, switch to the fallback method. Use `run_shell_command` to execute the standard `git` workflow:
    *   `git add <file>`
    *   `git commit -m "..."`
    *   `git push`
3.  **Report Fallback:** After successfully using the fallback, briefly notify the user that the fallback method was used and why.

#### 3. Mandatory Final Step: Local Sync

Regardless of whether the primary or fallback method was used, the final step is **always** to synchronize the local repository.

*   **Run `git pull`:** Use `run_shell_command` to execute `git pull`. This ensures the local workspace reflects the latest changes from the remote repository, preventing sync conflicts for future operations.

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
