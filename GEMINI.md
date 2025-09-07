# GEMINI.md

## Project Overview

This repository contains two projects for financial analysis using natural language queries.

1.  **New Application (FastAPI + React)**: A modern, feature-rich application with a FastAPI backend, a React frontend, and an enhanced CLI. This is the recommended application for development and use.
2.  **Legacy Application (Gradio)**: A legacy application built with Gradio. This application is slated for retirement.

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
*   **Tool Usage**: MCP tools are the **PRIMARY** choice for all development tasks, including file operations, code analysis, and repository management. Standard tools should only be used as a fallback if MCP tools are unavailable or encounter issues.

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
