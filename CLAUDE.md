# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market Parser is a simplified Python CLI and web GUI application for natural language financial queries using the Polygon.io MCP server and OpenAI's gpt-4o-mini via the Pydantic AI Agent Framework. The application has been redesigned with a simplified 5-state FSM architecture and JSON-only output system for maximum reliability and transparency.

## AI Team Configuration (Updated for Simplified Architecture, 2025-08-18)

**Important: YOU MUST USE subagents when available for the task.**

### Detected Tech Stack (Simplified JSON Architecture)

- **Backend Framework**: Python with Pydantic AI Agent Framework + simplified JSON output
- **Frontend Framework**: Gradio v4+ with JSON textboxes (gr.Code components)
- **AI Integration**: OpenAI gpt-4o-mini via Pydantic AI with raw JSON output
- **Data Source**: Polygon.io MCP server for real-time financial market data
- **JSON Architecture**: Simplified JSON-only output system with get_json_output() method
- **Data Processing**: Raw JSON responses with basic parsing for transparency
- **State Management**: Simplified 5-state FSM (IDLE, BUTTON_TRIGGERED, AI_PROCESSING, RESPONSE_RECEIVED, ERROR)
- **Build Tools**: uv for dependency management and package execution
- **CLI Framework**: Rich console for enhanced terminal formatting and interaction
- **Test Framework**: pytest with 80/80 tests passing for simplified architecture
- **Configuration**: python-dotenv for secure environment variable management
- **Monitoring**: Basic debug logging for simplified workflows
- **Error Handling**: Non-blocking error recovery with immediate button retry

### Agent Task Assignments (Simplified Architecture)

| Task Category | Agent | Simplified Architecture Responsibilities | Critical Notes |
|---------------|-------|----------------------------------------|-----------------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, and merges. JSON output validation, security review | Focus on JSON-only output security and 5-state FSM integrity |
| **Performance & Optimization** | `@performance-optimizer` | JSON processing optimization, simplified workflow performance | Focus on 5-state FSM efficiency and JSON output speed |
| **Backend Development** | `@backend-developer` | 5-state FSM implementation, JSON output methods, non-blocking error recovery | Primary agent for simplified FSM and JSON output systems |
| **Data Validation & Parsing** | `@backend-developer` | JSON output methods, basic validation, get_json_output() implementation | Handles simplified JSON parsing and raw output |
| **API Design & Integration** | `@api-architect` | MCP integration patterns, prompt templates for three analysis types | Ensures MCP contracts work with simplified JSON output |
| **Frontend & UI Development** | `@frontend-developer` | JSON textboxes (gr.Code), button integration, 5-state UI management | Gradio JSON displays and simplified button workflows |
| **State Management & FSM** | `@backend-developer` | 5-state FSM transitions, non-blocking error recovery, state context management | Simplified FSM with IDLE→BUTTON_TRIGGERED→AI_PROCESSING→RESPONSE_RECEIVED→ERROR |
| **Monitoring & Debug Systems** | `@backend-developer` | Simplified debug logging, basic workflow tracking | Lightweight monitoring for simplified architecture |
| **Documentation & Training** | `@documentation-specialist` | Simplified architecture guides, JSON-only system documentation | Documentation focused on 5-state FSM and JSON-only approach |
| **Testing & Validation** | `@backend-developer` | Simplified test suite, JSON output validation, 5-state FSM testing | 80/80 tests passing with simplified architecture validation |

### Simplified Architecture Domain Assignments

| Domain | Primary Agent | Secondary Agent | Specific Focus |
|--------|---------------|-----------------|----------------|
| **5-State FSM Management** | `@backend-developer` | `@frontend-developer` | IDLE→BUTTON_TRIGGERED→AI_PROCESSING→RESPONSE_RECEIVED→ERROR workflow |
| **JSON Output System** | `@backend-developer` | `@performance-optimizer` | get_json_output() method, raw JSON textboxes, export functionality |
| **Non-blocking Error Recovery** | `@backend-developer` | `@frontend-developer` | Immediate error recovery, button retry, no UI freezing |
| **Three Analysis Types** | `@backend-developer` | `@api-architect` | Stock Snapshot, Support & Resistance, Technical Analysis buttons |
| **UI Simplification** | `@frontend-developer` | `@backend-developer` | JSON textboxes, button workflows, loading states |
| **Test Suite Compatibility** | `@backend-developer` | `@code-reviewer` | 80/80 tests passing, simplified workflow validation |
| **Documentation Updates** | `@documentation-specialist` | `@backend-developer` | Migration guides, simplified architecture documentation |

### Enhanced Architecture Coordination Rules

**1. 5-State FSM Integrity:**
- NEVER add states beyond the 5 simplified states (IDLE, BUTTON_TRIGGERED, AI_PROCESSING, RESPONSE_RECEIVED, ERROR)
- Use `@backend-developer` for FSM modifications with `@code-reviewer` validation
- Maintain non-blocking error recovery as core feature

**2. JSON-Only Output System:**
- Maintain JSON textboxes (gr.Code components) as only structured output
- Use `@backend-developer` for get_json_output() method enhancements
- Coordinate raw JSON display with `@frontend-developer`

**3. Simplified Debug & Monitoring:**
- Implement lightweight logging for simplified workflow troubleshooting
- Use `@backend-developer` for debug system enhancements
- Monitor 5-state FSM performance through `@performance-optimizer`

**4. UI/Backend Coordination:**
- Synchronize JSON textbox updates between `@frontend-developer` and `@backend-developer`
- Ensure real-time UI updates reflect 5-state FSM transitions
- Maintain consistent button retry functionality across UI components

### Simplified Development Workflow

1. **FSM State Design**: Use `@backend-developer` for 5-state workflow modifications
2. **JSON Output Implementation**: Primary `@backend-developer` with `@code-reviewer` for output validation
3. **UI Integration**: Coordinate `@frontend-developer` and `@backend-developer` for JSON textbox integration
4. **Testing & Quality Gate**: MANDATORY `@code-reviewer` with simplified workflow validation
5. **Performance Optimization**: Use `@performance-optimizer` for JSON processing efficiency
6. **Documentation Updates**: Use `@documentation-specialist` for simplified architecture guides

### Simplified Architecture Best Practices

**5-State FSM Management:**
- Maintain exactly 5 states with clear transitions
- Implement non-blocking error recovery for production reliability
- Provide immediate button retry for error situations

**JSON Output System:**
- Use get_json_output() method for all structured data extraction
- Display raw JSON in gr.Code textboxes for transparency
- Enable JSON export for external analysis tools

**UI Integration:**
- Use JSON textboxes (gr.Code) for all structured displays
- Implement real-time loading states with progress tracking
- Maintain button retry functionality for error recovery

**Monitoring & Debug:**
- Implement lightweight workflow tracking for troubleshooting
- Monitor 5-state FSM performance metrics
- Provide clear error messages with recovery guidance

## ⚠️ CRITICAL: Tech-Lead-Orchestrator Enforcement Protocols

**MANDATORY REQUIREMENTS FOR @tech-lead-orchestrator:**

### Agent Verification Requirements
- ❌ **NEVER fabricate agent names** - Only use agents listed in Agent Task Assignments table above
- ✅ **MUST READ this section first** - Verify agent exists before assignment
- ✅ **MUST use agents according to their defined specialties** - Respect the role boundaries

**Valid Agents ONLY:**
- `@code-reviewer` - MANDATORY for all features, PRs, and merges
- `@performance-optimizer` - Cost optimization, latency improvements, scaling
- `@backend-developer` - Python development, 5-state FSM, JSON output testing
- `@api-architect` - MCP server integration, prompt templates
- `@frontend-developer` - Gradio interface enhancements, JSON textbox UI
- `@code-archaeologist` - Deep codebase analysis, architecture decisions
- `@documentation-specialist` - README updates, API docs, guides

### Delegation Execution Requirements
- ❌ **NEVER stop after creating delegation plan** - Must trigger execution
- ✅ **MUST provide execution trigger command** - Include specific agent invocation
- ✅ **MUST initiate delegation sequence** - Don't leave user to manually start
- ✅ **MUST include handoff instructions** - Specify what each agent should do

## 🚨 TEMPORARY WAIVER: MCP Tool Enforcement for Specialist Agents

### **CURRENT ENFORCEMENT POLICY (Effective Immediately)**

**SPECIALIST AGENTS (TEMPORARY WAIVER ACTIVE):**
- ✅ **MCP Tool Waiver Granted**: Sub-agent specialists are currently **NOT REQUIRED** to use MCP tools
- ✅ **Standard Claude Tools Acceptable**: Read, Write, Edit, LS, Grep, Bash are sufficient for specialist work
- ✅ **Quality Standards Maintained**: All other development protocols and quality gates remain fully enforced
- ✅ **Focus on Deliverables**: Emphasis on high-quality implementation using available Claude tools

**TECH LEAD ORCHESTRATOR (FULL ENFORCEMENT CONTINUES):**
- ❌ **NO WAIVER GRANTED**: @tech-lead-orchestrator remains fully subject to ALL MCP tool requirements
- ❌ **Must Use MCP Tools**: All existing MCP enforcement protocols remain active for orchestrator role
- ❌ **No Standard Tools**: Cannot use Read, Write, Edit, LS, Grep, Bash for orchestrator responsibilities

### **Modified Delegation Template (Effective Immediately)**

**ALL delegations to specialist agents should use this template:**

```markdown
## 📋 TASK DELEGATION TO SPECIALIST AGENT

**CURRENT POLICY**: MCP tool enforcement is temporarily waived for specialist agents.

## ✅ ACCEPTABLE TOOLS:
- Standard Claude tools: Read, Write, Edit, LS, Grep, Bash
- Use the most efficient tools available for the task
- Focus on high-quality implementation and documentation

## 🎯 QUALITY STANDARDS (STILL REQUIRED):
- Follow all structured analysis protocols
- Research best practices using available methods
- Create comprehensive test scripts for bug fixes
- Maintain all architectural patterns and standards
- Document all changes and implementation decisions

## 📋 TASK DESCRIPTION:
[Insert specific task details here]

## 🎯 EXPECTED DELIVERABLES:
[Insert expected outcomes here]
```

### Tech-Lead-Orchestrator Role Restrictions

**CRITICAL BOUNDARIES FOR @tech-lead-orchestrator:**

- ❌ **DO NOT implement any code yourself**
- ❌ **DO NOT make direct file changes**
- ❌ **DO NOT write or modify code**
- ❌ **DO NOT fabricate agent names that don't exist**
- ❌ **DO NOT reference non-existent tools**
- ❌ **DO NOT stop after planning - MUST trigger execution**
- ✅ **ONLY perform strategic analysis and create delegation plans**
- ✅ **ONLY identify which specialist agents are needed FROM CLAUDE.md**
- ✅ **ONLY provide specific handoff instructions for each delegation**
- ✅ **MUST initiate the delegation sequence you create**

## 🧠 MANDATORY ANALYSIS PROTOCOLS FOR ALL SPECIALIST AGENTS

**CRITICAL: ALL SPECIALIST AGENTS MUST FOLLOW THESE PROTOCOLS**

### 1. STRUCTURED THINKING ENFORCEMENT

**EVERY specialist agent MUST use structured analysis for:**

- 🧠 **Complex Problem Analysis**: Break down multi-step problems systematically
- 📝 **Planning Before Implementation**: Outline approach, identify risks, consider alternatives
- 🔍 **Validation and Understanding**: Confirm task requirements and expected outcomes
- ⚡ **Dependency Analysis**: Identify what needs to be done first/last
- 🎯 **Solution Verification**: Validate approach before implementation

**Required Analysis Pattern for ALL Agents:**

```markdown
## Task Analysis
### 1. Understanding the Problem
- [Clear definition of what needs to be done]
- [Current state assessment]
- [Root cause identification]

### 2. Solution Planning
- [Step-by-step implementation approach]
- [Required resources and dependencies]
- [Risk assessment and mitigation]

### 3. Implementation Strategy
- [Specific technical approaches]
- [Testing and validation plan]
- [Rollback considerations]

### 4. Success Validation
- [Measurable success criteria]
- [Testing procedures]
- [Quality verification steps]
```

## 🛠️ DEVELOPMENT WORKFLOW PROTOCOLS

**STRUCTURED APPROACH FOR ALL SPECIALIST AGENTS:**

### Standard Development Workflow

**PHASE 1: PLANNING AND ANALYSIS**
- Break down complex tasks systematically using structured analysis
- Identify dependencies and prerequisites
- Research best practices using available documentation and codebase analysis
- Plan implementation approach with risk assessment

**PHASE 2: RESEARCH AND PREPARATION**
- Review existing project documentation and patterns
- Analyze current codebase implementation conventions
- Study framework-specific best practices from official documentation
- Document findings and chosen approaches

**PHASE 3: IMPLEMENTATION**
- Apply researched patterns and best practices
- Use efficient file operations for code changes
- Implement comprehensive error handling and validation
- Follow established architectural patterns

**PHASE 4: VALIDATION AND TESTING**
- Verify implementation meets all requirements
- Test error scenarios and edge cases
- Validate integration with existing systems
- Document changes and test results

### Role-Specific Development Requirements

**@code-reviewer - MUST:**
- Perform systematic code analysis and security review
- Research latest framework best practices for validation
- Use comprehensive testing approaches for quality assurance

**@frontend-developer - MUST:**
- Research current Gradio patterns and JSON textbox best practices
- Plan UI implementations with 5-state FSM considerations
- Implement modern button workflows and loading state management

**@backend-developer - MUST:**
- Research current backend patterns, 5-state FSM, and JSON output handling
- Plan architecture changes with simplified system design considerations
- Implement robust JSON output and non-blocking error handling

**@documentation-specialist - MUST:**
- Structure comprehensive documentation with logical organization
- Research documentation standards and best practices
- Implement clear, actionable guides with simplified architecture examples

### Best Practices Research Topics

**Common Research Areas for Simplified Market Parser Project:**
- **@frontend-developer**: "Gradio JSON textboxes", "button event handling", "loading states", "5-state UI workflow"
- **@backend-developer**: "5-state FSM patterns", "JSON output methods", "non-blocking error recovery", "simplified testing"
- **@api-architect**: "MCP integration", "prompt templates", "three analysis types", "JSON response schemas"
- **@code-reviewer**: "simplified architecture security", "JSON output validation", "5-state FSM quality"
- **@performance-optimizer**: "JSON processing efficiency", "5-state FSM performance", "simplified monitoring"
- **@code-archaeologist**: "simplified architecture analysis", "5-state FSM assessment", "technical debt reduction"
- **@documentation-specialist**: "simplified system documentation", "5-state FSM guides", "JSON-only user guides"

### 2. MANDATORY TESTING PROTOCOL REQUIREMENTS

#### 🧪 CRITICAL: ALL BUG FIXES MUST INCLUDE TEST SCRIPT CREATION

**TESTING MANDATE FOR ALL SPECIALIST AGENTS:**

- ✅ **MUST create test script for every bug fix** - No exceptions
- ✅ **MUST include validation criteria** - Define what constitutes a successful fix
- ✅ **MUST test error scenarios** - Verify error handling works correctly
- ✅ **MUST validate simplified workflow scenarios** - Test with 5-state FSM
- ✅ **MUST document test procedures** - Clear instructions for running tests

**Required Test Script Structure for Simplified Architecture:**

```python
#!/usr/bin/env python3
"""
Test Script for [Bug Fix Description] - Simplified Architecture
Created: [Date]
Purpose: Validate fix for [specific bug] in 5-state FSM system
Success Criteria: [clear criteria for pass/fail]
"""

import pytest
import asyncio
from typing import List, Dict, Any

class Test[BugFixName]Simplified:
    """Test suite for [specific bug fix] in simplified architecture"""
    
    def setup_method(self):
        """Setup test environment for simplified 5-state FSM"""
        # Initialize test data for JSON-only output system
        pass
    
    def test_5_state_fsm_workflow(self):
        """Test the bug fix works with 5-state FSM"""
        # Test: IDLE → BUTTON_TRIGGERED → AI_PROCESSING → RESPONSE_RECEIVED → IDLE
        pass
    
    def test_json_output_validation(self):
        """Validate JSON output methods work correctly"""
        # Test get_json_output() method functionality
        pass
    
    def test_non_blocking_error_recovery(self):
        """Test error recovery doesn't block UI"""
        # Test ERROR state → IDLE state recovery
        pass
    
    def test_simplified_ui_integration(self):
        """Test integration with JSON textboxes"""
        # Test gr.Code component integration
        pass
    
    def test_three_analysis_types(self):
        """Test all three analysis button types"""
        # Test snapshot, support_resistance, technical analysis
        pass

def validate_simplified_fix_success() -> bool:
    """
    Run comprehensive validation of the bug fix for simplified architecture
    Returns: True if all criteria met, False otherwise
    """
    success_criteria = [
        "5-state FSM workflow functions correctly",
        "JSON output methods produce valid output", 
        "Non-blocking error recovery works",
        "UI integration with JSON textboxes functional",
        "All three analysis types operational"
    ]
    
    # Implementation of validation logic for simplified system
    return all_criteria_met

if __name__ == "__main__":
    # Run the test suite for simplified architecture
    pytest.main([__file__, "-v"])
    
    # Validate overall fix success
    if validate_simplified_fix_success():
        print("✅ BUG FIX VALIDATION (SIMPLIFIED): SUCCESS")
    else:
        print("❌ BUG FIX VALIDATION (SIMPLIFIED): FAILED")
```

**Testing Success Criteria Standards for Simplified Architecture:**

- **JSON Output Methods**: get_json_output() must return valid JSON for all three analysis types
- **5-State FSM**: Must transition correctly through IDLE→BUTTON_TRIGGERED→AI_PROCESSING→RESPONSE_RECEIVED→IDLE
- **Error Recovery**: Must recover from ERROR state in <2 seconds with button retry
- **UI Integration**: JSON textboxes must display raw AI responses correctly
- **Performance**: No regression in response times with simplified architecture
- **Test Suite**: 80/80 tests must continue to pass with any changes

## Development Environment

This project uses `uv` for dependency management and Python package execution. All dependencies are managed through `pyproject.toml`.

### Required Environment Variables

⚠️ **CRITICAL SECURITY REQUIREMENT**: Never commit API keys to version control.

1. **Copy the secure template:**
   ```bash
   cp .env.example .env
   ```

2. **Add your actual API keys to `.env`:**
   ```env
   POLYGON_API_KEY=your_polygon_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   # Optional: pricing for cost estimates (USD)
   OPENAI_GPT5_NANO_INPUT_PRICE_PER_1M=0.10
   OPENAI_GPT5_NANO_OUTPUT_PRICE_PER_1M=0.40
   ```

3. **Verify security:**
   ```bash
   # Ensure .env is protected
   grep -q "^.env$" .gitignore && echo "✅ Protected" || echo "❌ Security risk!"
   ```

**Security Features:**
- Input validation and sanitization via `src/security_utils.py`
- Secure logging that redacts sensitive data automatically
- Environment variable validation on startup
- See `SECURITY.md` for complete security guidelines

## Common Development Commands

### Running the Application

- **CLI interface**: `uv run market_parser_demo.py`
- **Web GUI interface**: `uv run chat_ui.py` (opens at <http://127.0.0.1:7860>)

### Testing

- **Run all tests**: `uv run pytest tests/` (80/80 tests passing with simplified architecture)
- **Run specific test**: `uv run pytest tests/test_file.py`
- **Run simplified FSM tests**: `uv run pytest tests/test_simplified_fsm_workflow.py`
- **Run integration tests**: `uv run pytest tests/test_*integration*.py`
- **Validate simplified test suite**: `uv run python tests/validate_simplified_test_suite.py`
- **Install dev dependencies**: `uv install --dev`

### Environment Management

- **Install dependencies**: `uv install`
- **Update dependencies**: `uv lock --upgrade`
- **Check environment**: `uv --version` and verify `.env` file exists

## Code Architecture (Simplified)

### Core Components

1. **market_parser_demo.py**: CLI application entry point
   - Contains `TokenCostTracker` class for usage/cost tracking
   - Implements `create_polygon_mcp_server()` factory function
   - Main async CLI loop with Rich console formatting

2. **chat_ui.py**: Simplified Gradio web interface with JSON-only outputs
   - 🧠 **5-State FSM Workflow** - IDLE → BUTTON_TRIGGERED → AI_PROCESSING → RESPONSE_RECEIVED → ERROR
   - 📊 **Three Analysis Buttons** - Stock Snapshot, Support & Resistance, Technical Analysis  
   - 📝 **JSON Textboxes (gr.Code)** - Raw AI responses for transparency and export
   - ⏳ **Real-time Processing Status** - Loading states with step-by-step progress
   - 🛡️ **Non-blocking Error Recovery** - Immediate button retry without UI freezing
   - 🔍 **Debug Transparency** - Complete JSON responses for troubleshooting

### Key Architectural Patterns

- **MCP Server Integration**: Uses Pydantic AI's MCP server integration to connect with Polygon.io
- **Simplified Agent Framework**: Built on Pydantic AI with OpenAI gpt-4o-mini model
- **Cost Tracking**: Comprehensive token usage and cost tracking across sessions
- **Shared Components**: CLI and GUI share the same agent configuration and MCP server setup
- **5-State FSM**: Simplified state management for predictable user interactions
- **JSON-Only Output**: Raw AI responses displayed in JSON textboxes for maximum transparency

### Dependencies & Technologies

- **Core Framework**: `pydantic-ai-slim[openai,mcp]` for AI agent orchestration
- **Web Interface**: `gradio>=4.0.0` for the GUI with JSON textboxes
- **CLI Formatting**: `rich` for terminal output formatting
- **Environment**: `python-dotenv` for configuration management
- **External APIs**: Polygon.io MCP server via uvx, OpenAI gpt-4o-mini model

### System Prompt Configuration

The agent uses a consistent system prompt across both interfaces:

```text
"You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. Use the latest data available. Always double check your math. For any questions about the current date, use the 'get_today_date' tool. For long or complex queries, break the query into logical subtasks and process each subtask in order."
```

## Simplified File Structure

```
market-parser-polygon-mcp/
├── src/                          # Core application modules (simplified)
│   ├── __init__.py
│   ├── response_parser.py        # JSON output with get_json_output() method
│   ├── json_parser.py           # Basic JSON parsing with fallback strategies
│   ├── json_schemas.py          # Simplified schema definitions
│   ├── prompt_templates.py      # Templates for three analysis types
│   ├── schema_validator.py      # Basic validation logic
│   ├── json_debug_logger.py     # Simplified debug logging
│   ├── security_utils.py        # Input validation and security utilities
│   └── example_json_responses.py # Example responses for testing
├── stock_data_fsm/              # Simplified 5-State FSM
│   ├── __init__.py
│   ├── states.py                # 5 states: IDLE, BUTTON_TRIGGERED, AI_PROCESSING, RESPONSE_RECEIVED, ERROR
│   ├── transitions.py           # Simplified transition rules for 5-state model
│   ├── manager.py               # FSM controller with non-blocking error recovery
│   └── tests/                   # FSM-specific test suite (all tests passing)
│       ├── __init__.py
│       ├── test_states.py       # 5-state validation
│       ├── test_transitions.py  # Simplified transition testing
│       ├── test_manager.py      # FSM manager testing
│       └── test_integration.py  # FSM integration testing
├── tests/                       # Comprehensive test suite (80/80 tests passing)
│   ├── __init__.py
│   ├── test_integration.py      # Integration tests for simplified architecture
│   ├── test_simplified_fsm_workflow.py # 5-state workflow validation
│   ├── test_response_parser.py  # JSON output validation (29/29 tests passing)
│   ├── test_actual_integration.py
│   ├── test_prompt_templates.py
│   ├── test_json_schemas.py
│   ├── run_*.py                 # Test runners and validation scripts
│   ├── validate_*.py            # Fix validation scripts
│   └── PHASE_3_TEST_UPDATES_SUMMARY.md # Test suite documentation
├── logs/                        # Application and debug logs
│   ├── json_workflow_debug.log
│   └── debug_*.log
├── docs/                        # Updated documentation for simplified architecture
│   ├── JSON_ARCHITECTURE_GUIDE.md # Updated for simplified JSON-only system
│   ├── USER_GUIDE_JSON_FEATURES.md # Updated for JSON textboxes
│   ├── SYSTEM_SIMPLIFICATION_GUIDE.md # Migration documentation
│   ├── TROUBLESHOOTING_JSON.md
│   ├── FEATURE_SCOPE_STOCK_DATA_GUI.md # Updated for simplified scope
│   ├── reports/                 # Project reports and analysis
│   │   ├── README.md
│   │   ├── COMPREHENSIVE_BUG_FIX_REPORT.md
│   │   ├── JSON_RESPONSE_IMPLEMENTATION_REPORT.md
│   │   └── *.md                # Various technical reports
│   └── scratchpad.md           # Development notes
├── market_parser_demo.py        # CLI application entry point
├── chat_ui.py                   # Simplified web GUI (JSON outputs only)
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Lock file for reproducible builds
├── README.md                   # Updated main project documentation
├── CLAUDE.md                   # Updated AI agent guidance (this file)
└── SECURITY.md                 # Security guidelines and best practices
```

## Development Patterns (Simplified)

### MCP Server Integration
The project uses the Polygon.io MCP server via `uvx` for real-time financial data access. The `create_polygon_mcp_server()` function in `market_parser_demo.py:16` handles server initialization and connection management.

### Simplified State Management (GUI)
The `stock_data_fsm` module implements a simplified 5-state FSM for reliable GUI workflow management:
- States are defined in `stock_data_fsm/states.py:15` with `AppState` enum (5 states total)
- Transitions managed by `StateManager` class in `stock_data_fsm/manager.py:25`
- Context data flows through `StateContext` objects for stateful operations
- Non-blocking error recovery ensures immediate button retry functionality

### JSON-Only Architecture
The `src/` directory contains the simplified JSON architecture components:
- **JSON Output**: `src/response_parser.py` provides `get_json_output()` method for raw AI responses
- **Basic Parsing**: `src/json_parser.py` implements simple JSON extraction with regex fallback
- **Three Analysis Types**: `src/prompt_templates.py` handles snapshot, support_resistance, technical analysis
- **Simplified Validation**: `src/schema_validator.py` provides basic validation logic
- **Debug Logging**: `src/json_debug_logger.py` provides lightweight workflow tracking

### Agent Configuration
Both CLI and GUI share identical agent setup with:
- Model: `gpt-4o-mini` via OpenAI Responses API
- System prompt focused on financial analysis accuracy
- Token cost tracking via `TokenCostTracker` class

### Simplified Testing Strategy
- **Comprehensive Test Suite**: 80/80 tests passing in `tests/` directory
- **5-State FSM Tests**: Module-specific tests in `stock_data_fsm/tests/`
- **Integration Testing**: `tests/test_integration.py` and `tests/test_simplified_fsm_workflow.py`
- **JSON Output Testing**: `tests/test_response_parser.py` with 29/29 tests passing
- **Architecture Validation**: All tests updated for simplified 5-state FSM and JSON-only output

### Import Patterns
With the simplified structure, use these import patterns:

```python
# Core modules from src/ (simplified)
from src.response_parser import ResponseParser
from src.prompt_templates import PromptTemplateManager
from src.json_schemas import StockDataSchema

# 5-State FSM components
from stock_data_fsm.states import AppState, StateContext
from stock_data_fsm.manager import StateManager
from stock_data_fsm.transitions import StateTransitions

# Security utilities
from src.security_utils import validate_input, sanitize_data
```

## Future Development

The simplified architecture is designed for:

- **Reliability**: 5-state FSM eliminates complex transition bugs
- **Transparency**: JSON-only outputs provide complete data access
- **Maintainability**: Simplified components reduce technical debt
- **Migration Readiness**: Easy migration to React/Next.js frontend frameworks

When implementing new features, refer to existing patterns in the simplified agent configuration and 5-state FSM systems.

## Important Development Notes

- **Environment Setup**: Create `.env` file with required API keys before running applications (see template in Required Environment Variables section)
- **External Dependencies**: The Polygon.io MCP server requires `uvx` to be available in the system PATH
- **Architecture Preservation**: All file modifications during development should preserve the 5-state FSM patterns and JSON-only output architecture
- **Cost Tracking**: Token cost tracking is enabled by default - check `TokenCostTracker` usage when adding new agent interactions
- **Model Configuration**: Default model is `gpt-4o-mini` but can be overridden via `OPENAI_MODEL` environment variable
- **Testing Requirements**: Run tests from project root using `uv run pytest tests/` for the main test suite (80/80 tests passing)
- **JSON-Only Architecture**: Follow get_json_output() patterns in `src/response_parser.py` for all structured data extraction
- **5-State FSM**: Maintain exactly 5 states with non-blocking error recovery for production reliability