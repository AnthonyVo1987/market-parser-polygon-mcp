# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the Pydantic AI Agent Framework.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
feat: Remove button validation system for performance optimization

- Remove validation system from SharedTickerInput component
- Remove validation system from ChatInput_OpenAI component  
- Delete validation utility files (validation.ts, useInputValidation.ts)
- Replace validation-based input handling with simple state management
- Remove validation error displays and validation-based CSS classes
- Remove validation-based ARIA attributes and accessibility features
- Maintain full input functionality without validation overhead
- Simplify component logic and reduce complexity

Performance improvements:
- Reduced JavaScript execution time (no validation calculations)
- Simplified state management (removed validation state)
- Cleaner component logic (less complex validation handling)
- Improved maintainability (removed validation dependencies)
- Faster input responsiveness (no validation checks on every keystroke)

Files modified:
- src/frontend/components/SharedTickerInput.tsx
- src/frontend/components/ChatInput_OpenAI.tsx

Files deleted:
- src/frontend/utils/validation.ts
- src/frontend/hooks/useInputValidation.ts

Phase 3 of CLI/GUI Performance Optimization Implementation Plan completed successfully.
<!-- LAST_COMPLETED_TASK_END -->

## STANDARDIZED TEST PROMPTS

**CRITICAL:** All testing MUST use these standardized prompts to ensure
consistent, quick responses (30-60 seconds) and avoid false failures from
complex prompts.

### Quick Response Test Prompts (Use These Only)

1. **"Quick Response Needed with minimal tool calls: What is the current
   Market Status?"**
2. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Single Stock Snapshot NVDA"**
3. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Full Market Snapshot: SPY, QQQ, IWM"**
4. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, what was the closing price of GME today?"**
5. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, how is SOUN performance doing this week?"**
6. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Top Market Movers Today for Gainers"**
7. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Top Market Movers Today for Losers"**
8. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Support & Resistance Levels NVDA"**
9. **"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Technical Analysis SPY"**

**MANDATORY RULES:**

- ✅ Use ONLY these prompts for testing
- ✅ Copy prompts EXACTLY as written
- ✅ Expected response time: 30-60 seconds
- ❌ DO NOT create custom prompts
- ❌ DO NOT modify these prompts
- ❌ DO NOT use complex, open-ended queries

**📋 COMPLETE PROMPT REFERENCE:** For the full standardized test
prompts documentation, see `tests/playwright/test_prompts.md`

## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop

using tools - continue using them until tasks completion!!!! 🔴

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout
the entire task execution. This is NOT a one-time checklist - you must
continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them
  before
- Use tools for investigation, analysis, verification, and implementation
  at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation,
   Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Context7 for research and best up to date Implementation Practices
   & Library documentation lookups
3. Use Serena Tools for code analysis, symbol manipulation, pattern search
   with context, and memory management for complex financial algorithm
   development and refactoring; Use standard Read/Write/Edit for simple file
   content modifications
4. Use Filesystem Tools for Batch File operations (3+), file discovery,
   configuration management, metadata analysis, project organization, project
   structure analysis, and documentation generation for comprehensive project
   management; Use standard Read/Write/Edit for single-file content
   modifications
5. Use Standard Read/Write/Edit for single-file content modifications,
   simple edits, and direct file operations; use Serena/Filesystem for
   complex analysis, batch operations, and project management
6. Use Playwright Tools for Testing with Browser automation for React GUI & App Validation
7. 🔴 REPEAT any tool as needed throughout the process
8. 🔴 NEVER stop using tools - continue using them until task completion

TOOL OVERLAP RESOLUTION:

- Filesystem Tools: Use for 3+ file operations, batch processing, project
  management, metadata analysis, comprehensive project operations
- Standard Read/Write/Edit: Use for single-file modifications, simple
  edits, direct file operations
- Serena Tools: Use for complex code analysis, symbol manipulation,
  pattern search with context
- When in doubt: Use Filesystem for batch/complex operations, Standard
  for simple single-file operations

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're
  failing
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch
  operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

REMEMBER: The tool list is your toolkit - use every tool as often as
needed, in any order, throughout the entire task execution. Choose the
right tool for the right operation

## Quick Start

**One-Click Application Startup (Recommended):**

The startup scripts automatically START all development servers BUT **DOES
NOT OPEN THE APP IN BROWSER AUTOMATICALLY**.

```bash
# Option 1: Main startup script (recommended)
./start-app.sh
```

**Prerequisites:** uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (Main Script)

- **Terminal Support**: Tries `gnome-terminal` first, falls back to `xterm`
- **Cross-Platform**: Works on most Linux distributions and macOS
- **Automatic Fallback**: Gracefully handles missing terminal emulators

## What the Scripts Do

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, vite)
- **Preserves MCP servers** - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- **Backend**: Starts FastAPI server on `http://127.0.0.1:8000`
- **Frontend**: Starts Vite dev server on `http://127.0.0.1:3000`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent hard-coded ports (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch

- **NOTIFIES USER TO LAUNCH BROWSER TO START THE APP WHEN SERVERS ARE READY**

**Access:** <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

## Features

### ⚡ High-Performance UI

- **Lightning Fast Loading**: 85%+ improvement in Core Web Vitals
- **Optimized Performance**: 256ms First Contentful Paint (FCP)
- **Smooth Interactions**: All UI interactions are instant and responsive
- **Memory Efficient**: Optimized memory usage with 13.8MB heap size
- **Accessibility First**: Full WCAG 2.1 AA compliance

### Natural Language Financial Queries

Ask questions like:

- `Tesla stock price analysis`
- `AAPL volume trends this week`
- `Show me MSFT support and resistance levels`

### Enhanced Response Format

Responses use a structured format with clear sentiment analysis:

```text
KEY TAKEAWAYS
• NVDA showing strong bullish momentum with 12% weekly gain
• Strong earnings beat with $35.08B revenue (+122% YoY)
• AI chip demand driving continued growth trajectory

DETAILED ANALYSIS
[Comprehensive analysis with clear directional indicators]
```

### Multiple Interfaces

- **React Web App** - Modern responsive interface with real-time chat
- **Enhanced CLI** - Terminal interface with rich formatting
- **API Endpoints** - RESTful API for integration

## Example Usage

### Web Interface

1. Open <http://127.0.0.1:3000>
2. Type your financial query
3. Get instant structured responses with sentiment analysis

### CLI Interface

```bash
uv run src/backend/main.py

> Tesla stock analysis
KEY TAKEAWAYS
• TSLA showing bullish momentum...
```

## Performance Optimizations

### UI Performance Improvements

This application has been optimized for maximum performance while
maintaining visual quality:

#### Core Web Vitals

- **First Contentful Paint (FCP)**: 256ms (85% better than target)
- **Largest Contentful Paint (LCP)**: < 500ms (80%+ improvement)
- **Cumulative Layout Shift (CLS)**: < 0.1 (50%+ improvement)
- **Time to Interactive (TTI)**: < 1s (70%+ improvement)

#### Optimization Techniques

- **CSS Minification**: Automated CSS optimization with cssnano
- **Removed High-Impact Effects**: Eliminated backdrop filters, complex
  shadows, gradients
- **Simplified Transitions**: Optimized to simple opacity and color transitions
- **Container Query Replacement**: Replaced with efficient media queries
- **Bundle Optimization**: Vite build optimizations with tree shaking
- **Memory Management**: Efficient JavaScript heap usage

#### Performance Monitoring

- **Real-time Metrics**: Live performance monitoring in the UI
- **Core Web Vitals Tracking**: Continuous monitoring of key metrics
- **Memory Usage**: Real-time memory usage display
- **Response Time**: API response time monitoring

### Performance Testing

- **Lighthouse CI**: Automated performance testing
- **Visual Regression Testing**: Ensures visual consistency
- **User Acceptance Testing**: Validates user experience
- **Cross-browser Testing**: Ensures compatibility

## Architecture

- **Backend**: FastAPI with OpenAI Agents SDK and Polygon.io MCP integration
- **Frontend**: React 18.2+ with Vite 5.2+ and TypeScript
- **Testing**: Playwright E2E test suite
- **Deployment**: Fixed ports (8000/3000/5500) with one-click startup

## Development

### Available Commands

```bash
# Application startup
npm run start:app          # One-click startup
npm run frontend:dev       # Frontend development
npm run build             # Production build

# Testing with Playwright MCP Tools only - see `/tests/playwright/mcp_test_script_basic.md`

# Code quality
npm run lint              # All linting
npm run type-check        # TypeScript validation
```

### Project Structure

```text
src/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application
│   ├── api_models.py    # API schemas
│   └── prompt_templates.py # Analysis templates
├── frontend/            # React frontend
│   ├── components/      # React components
│   ├── hooks/          # Custom hooks
│   └── config/         # Configuration loader
config/                  # Centralized configuration
│   └── app.config.json # Non-sensitive settings
tests/playwright/        # E2E test suite
```

## Troubleshooting

### Common Issues

**Backend not starting:**

```bash
# Check .env file has API keys
cat .env | grep API_KEY

# Verify dependencies
uv install
```

**Frontend connection errors:**

```bash
# Verify backend is running
curl http://127.0.0.1:8000/health

# Check ports are available
netstat -tlnp | grep :8000
```

**API key issues:**

- Ensure both `POLYGON_API_KEY` and `OPENAI_API_KEY` are set in `.env`
- Verify API keys are valid and have sufficient credits

## Disclaimer

**Warning:** This application uses AI and large language models.
Outputs may contain inaccuracies and should not be treated as financial
advice. Always verify information independently before making financial
decisions. Use for informational purposes only.

## License

This project is licensed under the [MIT License](LICENSE).
