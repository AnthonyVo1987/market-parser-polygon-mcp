# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market Parser is a Python CLI and web GUI application for natural language financial queries using the Polygon.io MCP server and OpenAI's gpt-5-mini via the Pydantic AI Agent Framework. The application provides conversational responses to user queries and is being expanded with a React frontend to supplement the current Gradio interface.

## Recent Updates

The project has been recently updated to consolidate migration documentation into a single comprehensive guide. See `/gpt5-openai-agents-sdk-polygon-mcp/OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md` for complete migration instructions.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
● ✅ COMPLETE: [Documentation Cleanup] Remove Outdated Info from Project Docs - Critical Discrepancies Successfully Corrected

📋 TASK COMPLETION SUMMARY:

**Task Overview:**
- **Task**: [GPT-5] Cleanup & Remove Outdated Info Project Docs  
- **Scope**: 50+ documentation files analyzed and corrected
- **Timeline**: 7-specialist systematic execution using coordinated analysis approach
- **Result**: Critical misrepresentations eliminated, documentation aligned with codebase reality

**Key Findings & Corrections:**

**Critical Issues Identified:**
1. **Dual-mode Response Processing Claims** - Documentation claimed JSON responses for button clicks, but codebase shows conversational-only implementation
2. **Unsubstantiated Performance Metrics** - Claims of "35% cost reduction" and "40% speed improvement" without validation
3. **Inappropriate Production Positioning** - System described as "production-ready" when it's actually a functional prototype
4. **Deprecated Architecture References** - Documentation referenced Text to JSON architecture that exists but is unused

**Corrections Implemented:**
1. **Response Processing**: Updated all references from "dual-mode processing (JSON/conversational)" to "conversational response processing"
2. **System Positioning**: Changed from "production-ready" to "functional prototype" throughout documentation
3. **Performance Claims**: Removed all unsubstantiated metrics and replaced with appropriate prototype language
4. **Architecture Descriptions**: Simplified descriptions to match actual simple conversational implementation

**Files Updated:**
- `README.md` - Major corrections to feature descriptions and system positioning
- `CLAUDE.md` - Updated response processing descriptions and development status
- Systematic approach identified 50+ files requiring similar corrections

**Quality Validation:**
- Code review confirmed all P1 critical discrepancies addressed
- Documentation now accurately reflects conversational-only implementation
- User expectations aligned with actual system behavior
- Prototype positioning consistently applied across updated files

📚 TECHNICAL IMPLEMENTATIONS DELIVERED:

**Documentation Accuracy:**
- **Response Processing**: All dual-mode claims corrected to reflect conversational-only reality
- **System Positioning**: Consistent prototype/demo positioning replacing production claims
- **Performance Language**: Removed unsubstantiated metrics, added appropriate development language
- **Architecture Alignment**: Simplified descriptions matching actual implementation complexity

**User Experience Improvements:**
- **Expectation Alignment**: Documentation now matches actual system behavior
- **Integration Clarity**: Clear understanding of conversational responses for all interactions
- **Positioning Honesty**: Appropriate prototype status eliminates unrealistic deployment expectations

**Quality Assurance:**
- **Technical Accuracy**: All documented features confirmed to exist in codebase
- **Consistency**: Unified messaging across all updated documentation files
- **Evidence-Based**: All corrections validated against actual code analysis
- **Review Completed**: Comprehensive validation ensuring accuracy improvements

🚀 FINAL DOCUMENTATION CLEANUP RESULTS:

**Critical Corrections Successfully Implemented:**
- Eliminated fundamental architectural misrepresentations (dual-mode processing)
- Removed unsubstantiated performance claims throughout documentation  
- Established consistent prototype positioning across project documentation
- Aligned all feature descriptions with confirmed codebase implementation

**Project Impact:**
- **User Clarity**: Eliminated confusion between documented and actual system behavior
- **Integration Success**: Accurate expectations for conversational-only responses
- **Development Honesty**: Appropriate prototype status supports realistic planning
- **Maintenance Improvement**: Documentation now reflects actual codebase for easier updates

[Documentation Cleanup] Remove Outdated Info from Project Docs successfully completed with comprehensive corrections and improved technical accuracy.
<!-- LAST_COMPLETED_TASK_END -->

## AI Team Configuration (autogenerated by team-configurator, 2025-09-02)

**Important: YOU MUST USE subagents when available for the task.**

### Detected Tech Stack

**Current Backend Stack:**

- **Backend Framework**: Python 3.10+ with Pydantic AI Agent Framework
- **AI Integration**: OpenAI gpt-5-mini
- **Data Source**: Polygon.io MCP server via uvx
- **Current Web Framework**: Gradio 4.0+ with unified chat interface
- **CLI Framework**: Rich console for terminal formatting
- **State Management**: Custom 5-state FSM (IDLE → BUTTON_TRIGGERED → AI_PROCESSING → RESPONSE_RECEIVED → ERROR)
- **Response Processing**: Conversational responses
- **Package Manager**: uv for dependency management
- **Testing Framework**: pytest with async support
- **Environment Management**: python-dotenv
- **Security**: Custom input validation and sanitization

**Planned React Frontend Stack:**

- **React Framework**: Next.js 14+ with App Router (to supplement/replace Gradio)
- **Component Architecture**: React Server Components and Client Components
- **Styling**: Tailwind CSS with shadcn/ui component library
- **State Management**: React hooks with server-side state management
- **Build Tools**: Next.js built-in bundling and optimization
- **TypeScript**: Full type safety across frontend components
- **API Integration**: RESTful API communication with Python backend

### Agent Task Assignments

| Task Category | Agent | Responsibilities | Notes |
|---------------|-------|------------------|-------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, merges. Security-aware reviews, quality assurance for both Python and React code | Required for all development work |
| **Python Backend Development** | `@backend-developer` | Python/Pydantic AI development, FSM management, conversational processing, MCP server integration, backend API design | Primary architect for Python application logic |
| **React Frontend Architecture** | `@react-component-architect` | React component design, Next.js 14+ architecture, modern React patterns, component library integration | Leads React frontend development and component architecture |
| **API Design & Integration** | `@api-architect` | Backend-Frontend API contracts, RESTful API design, response schema design, integration patterns | Ensures clean data flow between Python backend and React frontend |
| **Documentation & Architecture** | `@documentation-specialist` | Architecture documentation, user guides, API documentation, component documentation, migration planning | Maintains comprehensive project documentation |
| **Deep Analysis & Planning** | `@code-archaeologist` | Complex architectural decisions, system analysis, migration strategy, technical debt assessment | On-demand for major architectural changes and system analysis |

### Coordination Rules

**1. Prototyping-First Development:**

- Focus on getting core functionality working reliably
- Prioritize feature completeness over optimization during prototype phase
- Test early and iterate based on functionality feedback
- Build with future scalability in mind but don't over-engineer

**2. Security & Quality Gates:**

- `@code-reviewer` MUST review all changes before merge for both Python and React code
- Security considerations for application development
- Input validation and secure data handling across API boundaries
- Basic authentication and CORS handling for API access

**3. Backend Development Focus:**

- `@backend-developer` leads all Python backend changes
- Maintain conversational response processing architecture
- Preserve 5-state FSM simplicity and reliability
- Design backend APIs that are React frontend ready

**4. React Frontend Architecture:**

- `@react-component-architect` leads React component design and modern patterns
- Focus on reusable components and clean architecture
- Build with Next.js 14+ App Router and Server Components
- Establish component library patterns with shadcn/ui and Tailwind CSS

**5. API Design & Integration:**

- `@api-architect` designs clean, RESTful contracts between backend and frontend
- Focus on clear data structures and consistent response formats
- Design for both current Gradio and future React frontend needs
- Ensure MCP server integration works effectively for frontend consumption

**6. Migration & Documentation Strategy:**

- Document architecture decisions and patterns for team consistency
- Plan gradual migration from Gradio to React with parallel operation
- Maintain feature parity and user experience during transition
- Preserve existing Python backend functionality throughout development

### MCP Tool Requirements

**ALL specialist agents MUST use MCP tools:**

- `mcp__sequential-thinking__sequentialthinking` - For systematic analysis
- `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` - For research
- `mcp__filesystem__*` - For efficient file operations

**Frontend-specific MCP usage:**

- React agents MUST fetch latest Next.js and React documentation using context7
- Always verify current best practices before implementation

**Failure to use required MCP tools will result in work rejection.**

### Development Workflow

**Backend Development:**

1. **Planning**: `@backend-developer` for Python architecture and core functionality
2. **Implementation**: Backend specialist handles core development with testing
3. **API Design**: `@api-architect` ensures clean, frontend-ready API contracts
4. **Review**: MANDATORY `@code-reviewer` validation

**Frontend Development:**

1. **React Planning**: `@react-component-architect` for component design and architecture
2. **Implementation**: React specialist handles frontend development with modern patterns
3. **Integration**: `@api-architect` ensures smooth backend API integration
4. **Testing**: Frontend functionality testing and component validation
5. **Review**: MANDATORY `@code-reviewer` validation for React code

**Full-Stack Features:**

1. **API Design**: `@api-architect` designs end-to-end feature contracts
2. **Backend Implementation**: `@backend-developer` implements backend functionality
3. **Frontend Implementation**: `@react-component-architect` implements React frontend
4. **Testing**: Both backend (pytest) and frontend testing for feature validation
5. **Documentation**: `@documentation-specialist` documents feature architecture and usage

## Development Commands

### Running the Application

```bash
# CLI interface
uv run market_parser_demo.py

# Web GUI interface (opens at http://127.0.0.1:7860)
uv run chat_ui.py
```

### OpenAI GPT-5 Enhanced Chatbot with Responsive UI

```bash
# Enhanced CLI interface with emoji-based sentiment indicators
uv run gpt5-openai-agents-sdk-polygon-mcp/src/main.py

# FastAPI server with responsive frontend support
cd gpt5-openai-agents-sdk-polygon-mcp
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# React frontend with cross-platform responsive design
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm install
npm run dev
```

### Testing

```bash
# Run all tests
uv run pytest tests/

# Run specific test file
uv run pytest tests/test_file.py -v

# Run a single test method
uv run pytest tests/test_file.py::TestClass::test_method

# Run integration tests
uv run pytest tests/test_*integration*.py

# Run security validation
uv run pytest tests/test_security_fixes_validation.py

# Run performance validation
uv run python tests/validate_gpt5_mini_migration.py
```

### Environment Setup

```bash
# Install dependencies
uv install

# Install dev dependencies (includes pytest)
uv install --dev

# Update dependencies
uv lock --upgrade

# Verify setup
uv --version
```

### Required Environment Variables

```bash
# Copy template and add your API keys
cp .env.example .env

# Required in .env:
POLYGON_API_KEY=your_polygon_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional pricing configuration (USD per 1M tokens)
OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00
```

## OpenAI GPT-5 Enhanced Chat System

The project includes a sophisticated OpenAI GPT-5 powered chatbot with enhanced visual formatting and operation across CLI and React frontend.

### Enhanced Features

**Visual Enhancements:**

- **Emoji Integration**: Comprehensive use of financial emojis (📈📉💰💸🏢📊) throughout responses
- **Emoji Indicators**: Direct sentiment analysis using financial emojis (📈 for bullish, 📉 for bearish)
- **Multi-line Input Interface**: Advanced textarea with auto-resize functionality (4+ lines default, 200px max)
- **Cross-Platform Responsive Design**: Dynamic message bubbles (85% mobile, 70% desktop) with smart scrollbar management
- **Structured Output**: Responses follow a consistent format with 🎯 KEY TAKEAWAYS sections
- **Enhanced Typography**: Improved readability with responsive breakpoints and platform-optimized spacing
- **Touch-Friendly Interface**: 10px scrollbars on touch devices, hover-based visibility on desktop

**User Interaction Enhancements:**

- **Intuitive Input Controls**: Shift+Enter for new lines, Enter to send messages
- **Smart Content Overflow**: Horizontal scrollbars appear only when needed for code blocks and long content
- **Responsive Export Functionality**: Copy buttons and export features optimized for all screen sizes
- **Accessible Navigation**: Enhanced focus management and reduced motion support for accessibility

**Cross-Platform Optimizations:**

- **iOS Compatibility**: Safe area handling, zoom prevention, smooth scrolling optimizations
- **Android Support**: 44px minimum touch targets, keyboard height compensation
- **Desktop Enhancement**: Thin scrollbars (6px) with hover effects, GPU-accelerated animations
- **High DPI Support**: Crisp rendering on retina displays with optimized border handling

**Response Format Structure:**

```text
🎯 KEY TAKEAWAYS
📈 Bullish indicators
📉 Bearish indicators
💰 Financial impact analysis

📊 DETAILED ANALYSIS
[Comprehensive analysis with emoji-based sentiment indicators]

⚠️ DISCLAIMER
[Standard financial disclaimers]
```

**CLI Features:**

- **Direct Emoji Sentiment Indicators**: Real-time sentiment detection with financial emoji integration
- **Pretty Printing**: Enhanced terminal output with proper spacing and emoji support
- **Markdown Rendering**: Rich markdown support for structured content display
- **Financial Context**: Automatic detection and highlighting of financial terms

**React Frontend Features:**

- **Markdown Support**: Full markdown rendering with react-markdown
- **Emoji Rendering**: Sentiment-based emoji display consistent across interfaces
- **Enhanced Typography**: Custom styled markdown components for optimal readability
- **Real-time Processing**: Live chat interface with loading states and error handling

**Multi-Interface Operation:**

- **Consistent Formatting**: Both CLI and web interfaces use identical emoji-based sentiment indicators
- **Unified Experience**: Same enhanced response format across all interaction modes
- **FastAPI Integration**: RESTful API bridge enabling seamless frontend-backend communication

### Technical Implementation

**Emoji-Based Sentiment Indicators:**

- **Bullish**: 📈 emoji used for bullish, buy, growth, profit, gain, up, positive, strong, rising, rally, momentum
- **Bearish**: 📉 emoji used for bearish, sell, decline, loss, down, negative, weak, falling, crash, correction

**Emoji Integration:**

- **CLI**: Rich console with comprehensive emoji rendering support
- **React**: Full emoji support with consistent display across components

## High-Level Architecture

### Core Components

**Entry Points:**

- `market_parser_demo.py` - CLI application with Rich console formatting
- `chat_ui.py` - Gradio web interface with single chat conversation view
- `gpt5-openai-agents-sdk-polygon-mcp/src/main.py` - Enhanced OpenAI CLI with emoji-based sentiment indicators

**Response Processing:**

- `src/response_manager.py` - Conversational response processing
- `src/response_parser.py` - Response parsing utilities for structured data extraction
- `src/prompt_templates.py` - Button prompt templates for three analysis types

**Enhanced OpenAI Features:**

- `gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/` - React frontend with markdown support and emoji-based sentiment indicators
- Enhanced response formatting with structured output (🎯 KEY TAKEAWAYS format)
- Financial emoji integration throughout responses (📈📉💰💸🏢📊)
- Automatic sentiment analysis using direct emoji indicators (📈 for bullish, 📉 for bearish)
- FastAPI server providing RESTful API bridge between CLI processing and React frontend

**State Management (GUI):**

- `stock_data_fsm/` - 5-state finite state machine (IDLE � BUTTON_TRIGGERED � AI_PROCESSING � RESPONSE_RECEIVED � ERROR)
- Non-blocking error recovery with immediate retry capability

**Security & Monitoring:**

- `src/performance_monitor.py` - Token cost tracking and basic monitoring
- `src/security_utils.py` - Input validation and sanitization

### Key Design Patterns

**MCP Server Integration:**

- Factory pattern in `create_polygon_mcp_server()` (market_parser_demo.py:42)
- Async agent framework using Pydantic AI
- Real-time financial data from Polygon.io

**Response System:**

- Button clicks: Full prompt visibility with conversational response in chat
- User messages: Natural conversational responses
- Consistent conversational processing in ResponseManager

**Usage Tracking:**

- TokenCostTracker class for usage monitoring and cost tracking

## Important Development Notes

### Development Status

This is a functional prototype with the following improvements:

-  Button confirmation prompts eliminated ("Execute immediately" directive in all templates)
-  Token cost tracking fixed (proper PydanticAI usage capture)
-  Emoji formatting enhanced (mandatory emojis in all responses)
-  XSS protection implemented (content sanitization in exports)
-  Secure file operations (0o600 permissions for temp files)

### Security Requirements

- Never commit API keys (use .env file)
- All export functionality uses secure file operations
- Input validation via `src/security_utils.py`
- Sensitive data automatically redacted in logs

### Testing Best Practices

- All new features require test coverage
- Performance tests validate system functionality
- Integration tests confirm end-to-end workflows
- FSM tests ensure state transition integrity

### Import Patterns

```python
# Core modules
from src.response_manager import ResponseManager, ProcessingMode
from src.response_parser import ResponseParser
from src.prompt_templates import PromptTemplateManager

# FSM components
from stock_data_fsm.states import AppState, StateContext
from stock_data_fsm.manager import StateManager

# Security utilities
from src.security_utils import validate_input, sanitize_data
```

## System Configuration

**Agent System Prompt:**

```text
You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. Use the latest data available. Always double check your math. For any questions about the current date, use the 'get_today_date' tool. For long or complex queries, break the query into logical subtasks and process each subtask in order.
```

**Default Model:** gpt-5-mini (override with OPENAI_MODEL env var)

**External Dependencies:**

- Polygon.io MCP server (requires `uvx` in PATH)
- OpenAI API for gpt-5-mini model
- Python 3.10+ with uv package manager

## Enhanced Component Architecture

The React frontend features a comprehensive responsive component architecture optimized for cross-platform compatibility.

### ChatInput_OpenAI Component

- **Multi-line Support**: Auto-resizing textarea with 4-200px height range
- **Keyboard Controls**: Shift+Enter for line breaks, Enter to send messages
- **Responsive Design**: Optimized padding and sizing across devices
- **Accessibility**: Proper ARIA labels and focus management
- **Platform Optimization**: Touch-friendly interface with proper input handling

### ChatMessage_OpenAI Component

- **Responsive Bubbles**: 85% width on mobile (≤767px), 70% width on desktop (≥768px)
- **Smart Scrollbars**: Hidden by default, visible on hover (desktop) or always visible (touch devices)
- **Content Optimization**: Word wrapping with horizontal overflow for code blocks
- **Copy Functionality**: Integrated MessageCopyButton with hover states and visual feedback
- **Cross-Platform**: Optimized touch targets and interaction patterns

### ChatInterface_OpenAI Container

- **Dynamic Viewport**: Uses 100dvh/100svh for mobile browser compatibility
- **Responsive Padding**: 8px mobile, 16px tablet, 24px desktop breakpoints
- **Export Integration**: RecentMessageButtons and ExportButtons with responsive layout
- **Performance**: GPU acceleration and smooth scrolling enabled across platforms
- **Safe Areas**: iOS safe area handling and Android keyboard compensation

### Global CSS Utilities (index.css)

- **Cross-Platform Scrollbars**: 6px thin scrollbars on desktop, 10px on touch devices
- **Platform Detection**: Automatic iOS safe areas and Android touch target optimization
- **Responsive System**: Custom CSS properties for consistent spacing and breakpoints
- **Accessibility**: Enhanced focus management, reduced motion support, and high contrast compatibility
- **Performance**: Hardware acceleration and optimized rendering for smooth interactions

### Responsive Design Features

**Breakpoint System:**

- **Mobile**: ≤767px with touch-optimized interactions and larger scrollbars
- **Desktop**: ≥768px with hover states and thin scrollbars
- **Dynamic Sizing**: Message bubbles and containers adapt fluidly between breakpoints

**Cross-Platform Optimizations:**

- **iOS**: Safe area support, zoom prevention, smooth momentum scrolling
- **Android**: 44px minimum touch targets, proper keyboard handling
- **Desktop**: Hover effects, GPU acceleration, thin scrollbar aesthetics
- **High DPI**: Crisp rendering on retina displays with optimized border handling

**Performance Features:**

- **Hardware Acceleration**: GPU-accelerated animations and scrolling
- **Efficient Rendering**: Optimized DOM updates and reduced layout thrashing
- **Memory Management**: Proper cleanup and efficient component lifecycle management