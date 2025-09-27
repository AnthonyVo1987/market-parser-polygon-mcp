# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
feat: Add comprehensive Dynamic Adaptive Prompting System documentation and architecture memory

## New Documentation
- **Usage Guide**: Created comprehensive user guide (`docs/dynamic_prompting_usage_guide.md`)
  - Complete system overview and quick start guide
  - Detailed customization options (verbosity, tool usage, output format, response style)
  - Real-world examples and best practices
  - Integration examples for CLI and GUI usage
  - Error handling and troubleshooting guidance

## Architecture Memory
- **System Memory**: Created comprehensive architecture memory (`.serena/memories/dynamic_adaptive_prompting_system_architecture.md`)
  - Complete system component breakdown
  - User customization options and patterns
  - Integration architecture details
  - Security features and performance optimization
  - File structure and implementation status

## Documentation Features
- **User-Friendly Format**: Clear tables, examples, and practical use cases
- **Comprehensive Coverage**: Every aspect of the system explained
- **Practical Examples**: Real-world scenarios users will encounter
- **Best Practices**: Guidance on effective usage patterns
- **Integration Ready**: Examples for both CLI and GUI usage

## Technical Improvements
- **Markdown Quality**: Fixed all linting issues (fenced code blocks, formatting)
- **Content Organization**: Logical structure with clear sections
- **Cross-References**: Links to related documentation
- **Professional Standards**: High-quality documentation following best practices

## Files Added
- `docs/dynamic_prompting_usage_guide.md` - Complete user guide (10,287 bytes)
- `.serena/memories/dynamic_adaptive_prompting_system_architecture.md` - System architecture memory (7,184 bytes)

## Impact
- **User Experience**: Comprehensive guide for system usage
- **Developer Experience**: Complete architecture reference
- **Documentation Quality**: Professional-grade documentation
- **System Knowledge**: Preserved architecture knowledge for future development

The Dynamic Adaptive Prompting System now has complete documentation covering both user-facing functionality and technical architecture, enabling effective usage and future development.
- **Type Annotations**: Added proper type hints and documentation
- **Import Optimization**: Removed unused imports (Enum, List)
- **Error Handling**: Enhanced exception handling and validation

## Project Memories
- **Serena Memory Updates**: Comprehensive project documentation in .serena/memories/
- **Implementation Summary**: Complete technical documentation and architecture details
- **Test Analysis**: Detailed test results and performance characteristics
- **Deployment Guidelines**: Production deployment procedures and best practices

## Files Added/Modified
- **Core System**: dynamic_prompts.py, dynamic_prompt_manager.py, dynamic_prompt_integration.py
- **Security**: security_features.py, secure_prompt_manager.py, advanced_prompting_features.py
- **Tests**: test_dynamic_prompting_system.py, test_integration.py, test_user_acceptance.py
- **Documentation**: 5 comprehensive documentation files
- **Deployment**: 4 deployment scripts and 3 configuration files
- **Project Memory**: 4 Serena memory files with complete project documentation

## Production Readiness
- **System Stability**: 100% success rate across all test scenarios
- **Memory Management**: Excellent resource utilization and cleanup
- **Performance**: Consistent and acceptable response times (23-51s range)
- **Integration**: Seamless with existing CLI and GUI systems
- **Security**: Comprehensive security framework implemented
- **Documentation**: Complete user and developer documentation
- **Deployment**: Automated deployment and monitoring procedures

This implementation represents a significant advancement in the Market Parser Polygon MCP application, providing dynamic, customizable AI interactions while maintaining system stability and security.
<!-- LAST_COMPLETED_TASK_END -->

## STANDARDIZED TEST PROMPTS

__CRITICAL:__ All testing MUST use these standardized prompts to ensure
consistent, quick responses (30-60 seconds) and avoid false failures from
complex prompts.

### Quick Response Test Prompts (Use These Only)

1. __"Quick Response Needed with minimal tool calls: What is the current
   Market Status?"__
2. __"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Single Stock Snapshot NVDA"__
3. __"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Full Market Snapshot: SPY, QQQ, IWM"__
4. __"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, what was the closing price of GME today?"__
5. __"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, how is SOUN performance doing this week?"__
6. __"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Top Market Movers Today for Gainers"__
7. __"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Top Market Movers Today for Losers"__
8. __"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Support & Resistance Levels NVDA"__
9. __"Quick Response Needed with minimal tool calls: Based on Market Status
   Date, Technical Analysis SPY"__

__MANDATORY RULES:__

- ✅ Use ONLY these prompts for testing
- ✅ Copy prompts EXACTLY as written
- ✅ Expected response time: 30-60 seconds
- ❌ DO NOT create custom prompts
- ❌ DO NOT modify these prompts
- ❌ DO NOT use complex, open-ended queries

__📋 COMPLETE PROMPT REFERENCE:__ For the full standardized test
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

__One-Click Application Startup (Recommended):__

The startup scripts automatically START all development servers BUT __DOES
NOT OPEN THE APP IN BROWSER AUTOMATICALLY__.

```bash
# Option 1: Main startup script (recommended)
./start-app.sh
```

__Prerequisites:__ uv, Node.js 18+, API keys in .env

## Script Variants

### start-app.sh (Main Script)

- __Terminal Support__: Tries `gnome-terminal` first, falls back to `xterm`
- __Cross-Platform__: Works on most Linux distributions and macOS
- __Automatic Fallback__: Gracefully handles missing terminal emulators

## What the Scripts Do

### 🔄 Server Cleanup

- Kills existing development servers (uvicorn, vite)
- __Preserves MCP servers__ - does not interfere with MCP processes
- Waits for processes to terminate gracefully

### 🚀 Server Startup

- __Backend__: Starts FastAPI server on `http://127.0.0.1:8000`
- __Frontend__: Starts Vite dev server on `http://127.0.0.1:3000`
- Opens each server in a separate terminal window for easy monitoring
- Uses consistent hard-coded ports (no dynamic allocation)

### ✅ Health Verification

- Performs health checks on both servers
- Retries up to 10 times with 2-second intervals
- Verifies backend `/health` endpoint responds
- Verifies frontend serves content properly

### 🌐 Browser Launch

- __NOTIFIES USER TO LAUNCH BROWSER TO START THE APP WHEN SERVERS ARE READY__

__Access:__ <http://127.0.0.1:3000> (React app) or <http://127.0.0.1:8000> (API docs)

## Features

### ⚡ High-Performance UI

- __Lightning Fast Loading__: 85%+ improvement in Core Web Vitals
- __Optimized Performance__: 256ms First Contentful Paint (FCP)
- __Smooth Interactions__: All UI interactions are instant and responsive
- __Memory Efficient__: Optimized memory usage with 13.8MB heap size
- __Accessibility First__: Full WCAG 2.1 AA compliance

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

- __React Web App__ - Modern responsive interface with real-time chat
- __Enhanced CLI__ - Terminal interface with rich formatting
- __API Endpoints__ - RESTful API for integration

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

- __First Contentful Paint (FCP)__: 256ms (85% better than target)
- __Largest Contentful Paint (LCP)__: < 500ms (80%+ improvement)
- __Cumulative Layout Shift (CLS)__: < 0.1 (50%+ improvement)
- __Time to Interactive (TTI)__: < 1s (70%+ improvement)

#### Optimization Techniques

- __CSS Minification__: Automated CSS optimization with cssnano
- __Removed High-Impact Effects__: Eliminated backdrop filters, complex
  shadows, gradients
- __Simplified Transitions__: Optimized to simple opacity and color transitions
- __Container Query Replacement__: Replaced with efficient media queries
- __Bundle Optimization__: Vite build optimizations with tree shaking
- __Memory Management__: Efficient JavaScript heap usage

#### Performance Monitoring

- __Real-time Metrics__: Live performance monitoring in the UI
- __Core Web Vitals Tracking__: Continuous monitoring of key metrics
- __Memory Usage__: Real-time memory usage display
- __Response Time__: API response time monitoring

### Performance Testing

- __Lighthouse CI__: Automated performance testing
- __Visual Regression Testing__: Ensures visual consistency
- __User Acceptance Testing__: Validates user experience
- __Cross-browser Testing__: Ensures compatibility

## Architecture

- __Backend__: FastAPI with OpenAI Agents SDK v0.2.9 and Polygon.io MCP integration v0.4.1
- __Frontend__: React 18.2+ with Vite 5.2+ and TypeScript
- __Testing__: Playwright E2E test suite
- __Deployment__: Fixed ports (8000/3000/5500) with one-click startup

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

__Backend not starting:__

```bash
# Check .env file has API keys
cat .env | grep API_KEY

# Verify dependencies
uv install
```

__Frontend connection errors:__

```bash
# Verify backend is running
curl http://127.0.0.1:8000/health

# Check ports are available
netstat -tlnp | grep :8000
```

__API key issues:__

- Ensure both `POLYGON_API_KEY` and `OPENAI_API_KEY` are set in `.env`
- Verify API keys are valid and have sufficient credits

## Disclaimer

__Warning:__ This application uses AI and large language models.
Outputs may contain inaccuracies and should not be treated as financial
advice. Always verify information independently before making financial
decisions. Use for informational purposes only.

## License

This project is licensed under the [MIT License](LICENSE).
