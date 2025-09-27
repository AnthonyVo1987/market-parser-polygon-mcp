# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and React web application for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
feat: Implement Dynamic Adaptive Prompting System (Phases 1-5)

Implement comprehensive dynamic prompting system with user customization,
security features, and performance optimization for financial analysis.

## Core Implementation (Phase 1-2)
- Add DynamicPromptManager with instruction parsing and template engine
- Implement InstructionParser for extracting user preferences from input
- Add TemplateEngine with variable substitution and customization
- Create InputValidator with security validation and sanitization
- Implement PromptCache with LRU caching for performance

## Integration & Advanced Features (Phase 3-4)
- Integrate with existing CLI and GUI systems via dynamic_prompt_integration.py
- Preserve existing button prompt functionality (DirectPromptManager unchanged)
- Add advanced prompting features with custom templates and learning system
- Implement performance monitoring and analytics capabilities
- Add MarketParserDynamicPromptManager for financial analysis context

## Security & Resilience (Phase 5)
- Implement comprehensive security features with rate limiting
- Add EnhancedInputValidator with threat detection and pattern matching
- Create SecurityManager with audit logging and circuit breaker patterns
- Implement SecureDynamicPromptManager with full security integration
- Add IP whitelisting and comprehensive input validation

## Files Added/Modified
- src/backend/dynamic_prompts.py: Core dynamic prompting system
- src/backend/dynamic_prompt_manager.py: Market-specific prompt manager
- src/backend/dynamic_prompt_integration.py: Integration layer
- src/backend/advanced_prompting_features.py: Advanced features
- src/backend/security_features.py: Security implementation
- src/backend/secure_prompt_manager.py: Secure prompt manager
- src/backend/main.py: Integration with existing system
- tests/test_dynamic_prompting_system.py: Comprehensive test suite
- docs/dynamic_prompting_system_usage.md: Usage documentation
- .serena/memories/: Implementation documentation and guides

## Technical Features
- User preference parsing: [verbose], [minimal tools], [structured], [formal]
- Template engine with variable substitution and customization
- LRU caching with configurable TTL and size limits
- Rate limiting with sliding window algorithm
- Input validation with threat detection and sanitization
- Audit logging with security event tracking
- Circuit breaker pattern for system resilience
- Performance monitoring and analytics

## Backward Compatibility
- Maintains existing DirectPromptManager for button prompts
- Preserves all existing API endpoints and functionality
- Fallback mechanisms for error handling and system resilience
- No breaking changes to existing user workflows

## Security Enhancements
- Comprehensive input validation and sanitization
- Rate limiting with configurable rules and IP tracking
- Threat detection with pattern matching and keyword analysis
- Audit logging with security event classification
- Circuit breaker for system protection and recovery

This implementation provides a robust, secure, and performant dynamic
prompting system while maintaining full backward compatibility.
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
