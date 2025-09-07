# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market Parser is a Python CLI and web GUI application for natural language financial queries using the Polygon.io MCP server and OpenAI's gpt-5-mini via the Pydantic AI Agent Framework. The application provides conversational responses to user queries and is being expanded with a React frontend to supplement the current Gradio interface.

## Recent Updates

The project has been recently updated to consolidate migration documentation into a single comprehensive guide. See `/gpt5-openai-agents-sdk-polygon-mcp/OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md` for complete migration instructions.

## Prototyping Principles (ENFORCED)

**CRITICAL PROJECT STAGE NOTICE:** This project is currently in the prototyping stage. All development work must adhere to the following principles:

### Core Prototyping Requirements

- **Do NOT over-engineer ANYTHING** - Focus on functional prototypes, not perfect solutions
- **Prioritize functionality over optimization** - Get features working before making them efficient
- **Maintain prototype simplicity** - Avoid complex architectural patterns unless absolutely necessary

### NOT REQUIRED for Prototyping Stage

- **Enterprise Grade solutions** - Simple, functional implementations are preferred
- **Production Ready implementations** - Focus on demonstrating functionality
- **Performance Optimization** - Optimize only if performance blocks functionality
- **Comprehensive Testing** - Basic functional validation is sufficient
- **Test Scripts or Unit Tests** - Manual testing is acceptable for prototyping
- **CI/CD Pipeline implementation** - Basic git workflows are sufficient

### Prototyping Development Guidelines

- **Rapid iteration over perfect implementation** - Build, test, learn, iterate
- **Functional completeness over code quality** - Make it work first, refine later
- **Future scalability awareness without over-engineering** - Consider future needs but don't implement them yet
- **Documentation focused on usage, not internal architecture** - Help users understand what it does, not how it works internally

All specialists and development work must respect these prototyping constraints to maintain project momentum and avoid premature optimization.

## /new_task Workflow (Enhanced A-I Process)

**UPDATED WORKFLOW:** The `/new_task` command follows a systematic A-I process with tech-lead orchestration for all modes.

### Core Workflow Steps

**A. User Invokes `/new_task`**
- User provides task details via `/new_task` command
- Task details captured for analysis and planning

**B. Tech-Lead Orchestrator Analysis (ALWAYS REQUIRED)**
- Main Agent MUST use `@agent-tech-lead-orchestrator` regardless of Plan Mode or Non-Plan Mode
- Tech-lead reads, analyzes, and reviews task details in `new_task_details.md`
- Systematic evaluation of requirements and constraints

**C. Plan Mode: Tech-Lead Orchestrated Planning**
- `@agent-tech-lead-orchestrator` generates comprehensive plan WITH Specialist Assignments
- Detailed task breakdown with specialist role allocations
- Resource requirements and dependency mapping

**D. Non-Plan Mode: Tech-Lead Orchestrated Planning**
- `@agent-tech-lead-orchestrator` generates streamlined plan WITH Specialist Assignments
- Focused task execution plan with specialist coordination
- Efficient resource allocation for immediate implementation

**E. Specialist Execution**
- Specialists execute plan from `@agent-tech-lead-orchestrator`
- ALL specialists MUST use MCP tools as primary method:
  - `mcp__sequential-thinking__sequentialthinking` for systematic analysis
  - `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` for research
  - `mcp__filesystem__*` for all file operations
- Prototyping principles enforced throughout execution

**F. Documentation Updates (Post-Execution)**
- Generate detailed Last Completed Task Summary → overwrite `LAST_TASK_SUMMARY.md`
- Generate high-level 20-line summary → update CLAUDE.md task summary section
- Ensure comprehensive documentation of all changes and outcomes

**G. Primary GitHub Tools Usage**
- PRIMARY: `mcp__github__push_files` for all atomic commit operations
- Secondary: Traditional git commands only when GitHub MCP tools insufficient
- Must justify fallback to traditional git commands

**H. Atomic Commit Execution**
- Single atomic commit containing ALL changes:
  - Code/file changes
  - Documentation updates
  - CLAUDE.md updates  
  - LAST_TASK_SUMMARY.md updates
- No separation between code changes and documentation changes

**I. Single Commit Completion**
- All code, documentation, and task summary changes belong in same commit
- Comprehensive commit message documenting all changes
- Clean working tree with all changes properly versioned

### Workflow Enforcement

**Tech-Lead Orchestrator Requirements:**
- MANDATORY for both Plan Mode and Non-Plan Mode
- Ensures consistent specialist assignments across all task types
- Provides systematic analysis and resource coordination
- Maintains quality standards and prototyping principles compliance

**Prototyping Constraints Integration:**
- All workflow steps respect prototyping stage limitations
- Focus on functional delivery over perfect implementation
- Avoid over-engineering during specialist execution
- Rapid iteration and prototype-appropriate solutions

**Quality Assurance Integration:**
- Review/Fix Loop with PASSING status required before documentation
- Comprehensive validation using MCP tools for systematic analysis
- Atomic commit ensures complete change integration
- Final verification confirms successful completion

This enhanced A-I workflow ensures consistent tech-lead orchestration, proper specialist coordination, prototyping principles compliance, and comprehensive atomic commit management for all `/new_task` operations.

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
● ✅ COMPLETE: [OpenAI] Pre-migration Docs Prep & Updates: OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md - Successfully Delivered

**Quick Overview:**
- **Task:** Pre-migration documentation preparation with Scenario B removal, development environment enhancement, and CI workflow management
- **Result:** Migration guide streamlined for single-path migration with comprehensive development environment integration
- **Impact:** Streamlined user experience eliminating dual-path confusion with enhanced development capabilities

**Key Deliverables:**
- Complete Scenario B removal with zero remaining references across all documentation
- Comprehensive Vite and Live Server setup integrated across all 4 migration methods
- Professional CI workflow disable implementation with configuration preservation and clear restoration procedures
- Enhanced cross-references and navigation supporting optimal user experience throughout migration workflow

**Specialist Coordination:** Tech-lead orchestrated workflow with systematic execution across @code-archaeologist, @documentation-specialist, @backend-developer, and @code-reviewer

**Quality Status:** PASSING with comprehensive validation and all specialist approvals | **Files Updated:** 2 core files

📋 **Full Details:** See `/LAST_TASK_SUMMARY.md` for complete specialist reports, technical achievements, and quality validation results.

**Git Commit:** de5ba48 | **Completion:** 2025-09-07

**Note:** Corrective actions documented for atomic commit principles and GitHub MCP tools compliance in future workflows.
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

**1. Prototyping-First Development (ENFORCED):**

- **CRITICAL**: Project is in prototyping stage - Do NOT over-engineer ANYTHING
- Focus on getting core functionality working reliably
- Prioritize feature completeness over optimization during prototype phase
- **NOT REQUIRED**: Enterprise Grade, Production Ready, Performance Optimization solutions
- **NOT REQUIRED**: Testing, Test Scripts, Unit Tests, CI/CD Pipeline
- Test early and iterate based on functionality feedback
- Build with future scalability in mind but maintain prototype simplicity

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

### GitHub MCP Tools Requirements

**PRIMARY Git Operations Method:**

- `mcp__github__create_or_update_file` - For single file operations
- `mcp__github__push_files` - For multi-file atomic commits (REQUIRED for all task completion)
- `mcp__github__create_branch` - For feature branch creation
- `mcp__github__search_code` - For code discovery and analysis

**Secondary Fallback:**

- Traditional git commands via Bash tool only when GitHub MCP tools are insufficient
- Must justify why GitHub MCP tools cannot be used for the specific operation
- All atomic commits for task completion MUST use `mcp__github__push_files` as primary method

**Atomic Commit Requirements:**

- ALL task completions require single atomic commit containing:
  - Code/file changes
  - Documentation updates 
  - CLAUDE.md task summary updates
  - LAST_TASK_SUMMARY.md updates (if applicable)
- Use `mcp__github__push_files` for atomic operations
- No separation of code changes vs documentation changes
- Single commit with comprehensive change documentation

### Development Workflow (Prototyping-Optimized)

**Backend Development (Prototype Focus):**

1. **Planning**: `@backend-developer` for functional Python implementation (avoid over-engineering)
2. **Implementation**: Backend specialist handles core development (basic functional validation sufficient)
3. **API Design**: `@api-architect` ensures working API contracts (simple, functional designs preferred)
4. **Review**: MANDATORY `@code-reviewer` validation (focus on functionality, not perfect code quality)

**Frontend Development (Prototype Focus):**

1. **React Planning**: `@react-component-architect` for functional component design (avoid complex patterns)
2. **Implementation**: React specialist handles frontend development (working prototypes over perfect architecture)
3. **Integration**: `@api-architect` ensures basic API integration works (functional connection sufficient)
4. **Testing**: Manual functional validation (automated testing not required for prototyping)
5. **Review**: MANDATORY `@code-reviewer` validation for React code (functional focus)

**Full-Stack Features (Prototype Focus):**

1. **API Design**: `@api-architect` designs functional end-to-end contracts (simple, working solutions)
2. **Backend Implementation**: `@backend-developer` implements functional backend (prototype-appropriate complexity)
3. **Frontend Implementation**: `@react-component-architect` implements working React frontend (rapid iteration focus)
4. **Testing**: Basic functional validation ensuring feature works (comprehensive testing not required)
5. **Documentation**: `@documentation-specialist` documents usage and functionality (internal architecture details not required)

**Prototyping Workflow Principles:**

- **Functionality First**: Make it work before making it perfect
- **Rapid Iteration**: Quick implementation cycles with immediate feedback
- **Simple Solutions**: Avoid complex patterns unless absolutely necessary for functionality
- **Manual Validation**: Basic testing to confirm features work as intended
- **Usage Documentation**: Focus on how to use features, not internal implementation details

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

# Vite-optimized React frontend with comprehensive performance optimizations
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm install
npm run dev  # Optimized development (~337ms startup)

# Additional Vite optimization commands:
# npm run build          # Production build with PWA (45% bundle reduction)
# npm run build:staging  # Staging environment build
# npm run analyze        # Bundle analysis with performance insights
# npm run lighthouse     # Lighthouse CI performance validation
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

- Button confirmation prompts eliminated ("Execute immediately" directive in all templates)
- Token cost tracking fixed (proper PydanticAI usage capture)
- Emoji formatting enhanced (mandatory emojis in all responses)
- XSS protection implemented (content sanitization in exports)
- Secure file operations (0o600 permissions for temp files)

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