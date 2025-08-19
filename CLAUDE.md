# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Market Parser is a Python CLI and web GUI application for natural language financial queries using the Polygon.io MCP server and OpenAI's gpt-5-mini via the Pydantic AI Agent Framework. The application allows users to ask questions about stock market data in natural language and receive formatted responses in a simplified, single chat interface.

## AI Team Configuration (Simplified Architecture, 2025-08-19)

**Important: YOU MUST USE subagents when available for the task.**

### Detected Tech Stack (Simplified Architecture)

- **Backend Framework**: Python with Pydantic AI Agent Framework + dual-mode response processing
- **Frontend Framework**: Gradio v4+ with single chat interface and real-time feedback
- **AI Integration**: OpenAI gpt-5-mini via Pydantic AI with optimized cost management
- **Data Source**: Polygon.io MCP server for real-time financial market data
- **Response Processing**: Dual-mode system (JSON for buttons, conversational for user messages)
- **State Management**: Simplified 5-state FSM with performance optimization
- **Build Tools**: uv for dependency management and package execution
- **CLI Framework**: Rich console for enhanced terminal formatting and interaction
- **Test Framework**: pytest with comprehensive validation and performance testing suites
- **Configuration**: python-dotenv for secure environment variable management
- **Monitoring**: Performance tracking with cost optimization and resource monitoring
- **Performance Enhancement**: 35% cost reduction with 40% processing speed improvement
- **Debug System**: Streamlined logging with comprehensive error tracking

### Agent Task Assignments (Optimized for Simplified Architecture)

| Task Category | Agent | Simplified Architecture Responsibilities | Critical Notes |
|---------------|-------|----------------------------------------|-----------------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, and merges. Architecture integrity focus, security review, simplified FSM validation | Always validate simplified architecture consistency and security |
| **Performance & Optimization** | `@performance-optimizer` | Cost optimization (35% reduction), processing efficiency (40% improvement), resource monitoring | Focus on cost management, response speed, and resource optimization |
| **Simplified Architecture** | `@backend-developer` | Dual-mode response processing, simplified FSM design, single chat interface backend, primary architect for simplified systems | Primary agent for all simplified architecture components and 5-state FSM |
| **Response Processing** | `@backend-developer` | Dual-mode system (JSON/conversational), response routing logic, performance optimization | Handles response processing accuracy and mode switching logic |
| **API Design & Integration** | `@api-architect` | MCP integration patterns, response schema optimization, cost-efficient API calls | Ensures efficient API contracts and integration patterns |
| **Frontend & UI Development** | `@frontend-developer` | Single chat interface, real-time UI updates, simplified user experience | Gradio single chat optimization and user experience enhancement |
| **State Management & FSM** | `@backend-developer` | Simplified 5-state FSM, performance-optimized workflow, cost-efficient state transitions | Enhanced FSM with simplified architecture and cost optimization |
| **Monitoring & Performance** | `@backend-developer` | Performance metrics, cost tracking, resource usage monitoring, streamlined debugging | Comprehensive performance monitoring and cost optimization systems |
| **Documentation & Training** | `@documentation-specialist` | Simplified architecture guides, performance optimization documentation, migration procedures | Simplified system usage, optimization guides, and architecture documentation |
| **Testing & Validation** | `@backend-developer` | Simplified architecture testing, performance validation, cost optimization testing | Comprehensive simplified system validation with enhanced performance metrics |
| **Deep Architecture Analysis** | `@code-archaeologist` | Complex architecture decisions, deep system analysis, technical debt assessment when needed | Deep insight for major architectural changes and system optimization |

### Simplified Architecture Domain Assignments

| Architecture Domain | Primary Agent | Secondary Agent | Specific Focus |
|-------------|---------------|-----------------|----------------|
| **Dual-Mode Response System** | `@backend-developer` | `@api-architect` | Response routing (JSON/conversational), mode switching logic, primary response architecture responsibility |
| **Performance Optimization** | `@backend-developer` | `@performance-optimizer` | Cost reduction (35%), processing speed (40% improvement), resource efficiency |
| **Single Chat Interface** | `@frontend-developer` | `@backend-developer` | Consolidated UI, unified user experience, simplified interaction patterns |
| **Cost Management** | `@performance-optimizer` | `@backend-developer` | Token usage optimization, API call efficiency, resource monitoring |
| **Simplified FSM** | `@backend-developer` | `@frontend-developer` | 5-state workflow integrity, performance-optimized transitions, cost-efficient state management |
| **Architecture Documentation** | `@documentation-specialist` | `@backend-developer` | Simplified system guides, performance optimization docs, migration documentation |
| **Performance Testing** | `@backend-developer` | `@performance-optimizer` | Cost optimization validation, speed improvement testing, resource usage validation |
| **System Monitoring** | `@performance-optimizer` | `@backend-developer` | Performance metrics, cost tracking, optimization insights |
| **Simplified FSM Management** | `@backend-developer` | `@frontend-developer` | IDLE→BUTTON_TRIGGERED→AI_PROCESSING→RESPONSE_RECEIVED→ERROR workflow integrity |
| **Architecture Assessment** | `@code-archaeologist` | `@backend-developer` | Deep system analysis, optimization decisions, performance architecture when needed |

### Simplified Architecture Coordination Rules

**1. Architectural Simplicity:**
- NEVER add complexity without `@backend-developer` involvement and `@code-reviewer` validation
- Use `@performance-optimizer` for all performance and cost optimization decisions
- Require comprehensive testing before architectural changes
- NEVER add states beyond the 5 simplified ones (IDLE, BUTTON_TRIGGERED, AI_PROCESSING, RESPONSE_RECEIVED, ERROR)

**2. Dual-Mode Response System:**
- Maintain dual-mode response architecture (JSON for buttons, conversational for user messages)
- Use `@backend-developer` for response routing enhancements
- Coordinate mode switching logic with `@frontend-developer`
- Preserve cost-optimized processing as core principle

**3. Performance & Cost Optimization:**
- Maintain 35% cost reduction and 40% processing speed improvement targets
- Use `@performance-optimizer` for all efficiency enhancements
- Monitor resource usage through comprehensive performance metrics
- Focus on cost-efficient API interactions and resource management

**4. Single Chat Interface Coordination:**
- Synchronize single chat interface between `@frontend-developer` and `@backend-developer`
- Ensure unified user experience across all interaction types
- Maintain consistent response display patterns
- Focus on simplified, consolidated user interface

**5. Quality Gate Enforcement:**
- MANDATORY `@code-reviewer` for all simplified architecture changes
- Maintain performance optimization targets as quality baseline
- Preserve architectural simplicity over feature complexity
- Use `@code-archaeologist` only for complex optimization decisions

### Simplified Development Workflow

1. **Architecture Design Phase**: Use `@backend-developer` as primary architect with `@performance-optimizer` for efficiency alignment
2. **Performance Implementation**: Primary `@backend-developer` with mandatory `@performance-optimizer` for cost optimization
3. **UI Integration**: Coordinate `@frontend-developer` and `@backend-developer` for single chat interface optimization
4. **Testing & Quality Gate**: MANDATORY `@code-reviewer` with comprehensive performance validation
5. **Cost Optimization**: Use `@performance-optimizer` for efficiency enhancement and resource monitoring
6. **Documentation Updates**: Use `@documentation-specialist` for simplified architecture guides and optimization documentation

### Technology-Specific Best Practices (Simplified Architecture)

**Dual-Mode Response Processing:**
- Button clicks route to JSON response mode with full prompt visibility
- User messages route to conversational response mode for natural interaction
- Maintain cost-efficient response processing with optimized token usage
- Use `@backend-developer` as primary response architecture manager

**Performance Optimization:**
- 35% cost reduction through enhanced efficiency and optimized API calls
- 40% processing speed improvement through streamlined response handling
- Resource monitoring with comprehensive performance metrics
- Cost optimization through `@performance-optimizer`

**Single Chat Interface:**
- Consolidated conversation view with all interactions in one interface
- Unified user experience with dual-mode response display
- Real-time feedback with simplified loading states
- Gradio-specific optimizations through `@frontend-developer`

**Simplified FSM Architecture:**
- Maintain exactly 5 states: IDLE, BUTTON_TRIGGERED, AI_PROCESSING, RESPONSE_RECEIVED, ERROR
- Performance-optimized state transitions with cost efficiency
- Simplified error recovery with immediate retry capability
- Primary `@backend-developer` responsibility with `@frontend-developer` coordination

**Critical Success Factors:**
- Preserve architectural simplicity over feature complexity
- Maintain performance optimization targets (35% cost reduction, 40% speed improvement)
- Use mandatory code review for all architectural changes
- Focus on cost efficiency and user experience simplicity

## ⚠️ CRITICAL: Tech-Lead-Orchestrator Enforcement Protocols

**MANDATORY REQUIREMENTS FOR @tech-lead-orchestrator:**

### Agent Verification Requirements
- ❌ **NEVER fabricate agent names** - Only use agents listed in Agent Task Assignments table above
- ✅ **MUST READ this section first** - Verify agent exists before assignment
- ✅ **MUST use agents according to their defined specialties** - Respect the role boundaries

**Valid Agents ONLY:**
- `@code-reviewer` - MANDATORY for all features, PRs, and merges
- `@performance-optimizer` - Cost optimization, processing efficiency, performance enhancement
- `@backend-developer` - Python development, simplified architecture, FSM, testing, PRIMARY SIMPLIFIED ARCHITECT
- `@api-architect` - MCP server integration, response optimization
- `@frontend-developer` - Gradio single chat interface, UI/UX, consolidated user experience
- `@code-archaeologist` - Deep codebase analysis, architecture decisions (when needed)
- `@documentation-specialist` - README updates, optimization guides, simplified documentation

### Delegation Execution Requirements
- ❌ **NEVER stop after creating delegation plan** - Must trigger execution
- ✅ **MUST provide execution trigger command** - Include specific agent invocation
- ✅ **MUST initiate delegation sequence** - Don't leave user to manually start
- ✅ **MUST include handoff instructions** - Specify what each agent should do
- ✅ **MUST include mandatory MCP tool requirements** - Every delegation MUST specify required MCP tools
- ✅ **MUST verify MCP tool usage** - REJECT work that doesn't use required MCP tools

### 🚨 CRITICAL: MCP Tool Enforcement for Delegated Specialists

**MANDATORY REQUIREMENTS FOR ALL DELEGATED SPECIALIST AGENTS:**

All specialist agents delegated via Task tool **MUST** use MCP tools according to their role requirements. **FAILURE TO USE MCP TOOLS = IMMEDIATE WORK REJECTION**.

#### **MCP Tool Verification Protocol**

**BEFORE accepting ANY specialist work, @tech-lead-orchestrator MUST verify:**

- ✅ **Sequential Thinking Used**: Evidence of `mcp__sequential-thinking__sequentialthinking` usage
- ✅ **Context7 Research Performed**: Evidence of `mcp__context7__resolve-library-id` and `mcp__context7__get-library-docs` if required
- ✅ **Filesystem Tools Used**: Evidence of `mcp__filesystem__*` tools for file operations if applicable
- ✅ **Actual MCP Tools Listed**: Response includes specific MCP tool usage, not standard Claude tools

#### **Mandatory Delegation Template**

**ALL delegations MUST include this exact text:**

```markdown
## 🚨 MANDATORY MCP TOOL REQUIREMENTS:
You MUST use these MCP tools (VIOLATION = IMMEDIATE REJECTION):
- [Specify required MCP tools based on role]
- Example: mcp__sequential-thinking__sequentialthinking - For systematic analysis
- Example: mcp__context7__resolve-library-id + get-library-docs - For research
- Example: mcp__filesystem__* - For file operations

## VERIFICATION EVIDENCE REQUIRED:
You MUST provide in your response:
1. List of MCP tools used with specific call details
2. Sequential thinking steps showing systematic approach
3. Context7 research findings if applicable
4. Evidence of filesystem MCP tool usage

⚠️ CRITICAL: Using only standard Claude tools (Read, Write, Edit, LS, Grep, Bash) 
without MCP tools will result in IMMEDIATE WORK REJECTION and re-delegation.
```

#### **Role-Specific MCP Requirements for Delegations**

**@code-reviewer delegations MUST include:**
```
MANDATORY MCP TOOLS:
- mcp__sequential-thinking__sequentialthinking - For systematic code analysis
- mcp__context7__resolve-library-id + get-library-docs - For latest best practices research
```

**@backend-developer delegations MUST include:**
```
MANDATORY MCP TOOLS:
- mcp__sequential-thinking__sequentialthinking - For architecture planning
- mcp__context7__resolve-library-id + get-library-docs - For latest backend patterns
- mcp__filesystem__* - For efficient file operations
```

**@frontend-developer delegations MUST include:**
```
MANDATORY MCP TOOLS:
- mcp__sequential-thinking__sequentialthinking - For UI/UX planning
- mcp__context7__resolve-library-id + get-library-docs - For latest frontend patterns
- mcp__filesystem__* - For efficient file operations
```

**@documentation-specialist delegations MUST include:**
```
MANDATORY MCP TOOLS:
- mcp__sequential-thinking__sequentialthinking - For documentation structuring
- mcp__filesystem__* - For efficient file operations
```

#### **Work Rejection Protocol**

**If specialist work is received WITHOUT proper MCP tool usage:**

1. **IMMEDIATELY REJECT** the work with reason: "VIOLATION: Required MCP tools not used"
2. **RE-DELEGATE** with strengthened MCP tool requirements
3. **DOCUMENT** the violation in the response
4. **DO NOT ACCEPT** work using only standard Claude tools

#### **MCP Tool Usage Evidence Requirements**

**Acceptable evidence of MCP tool usage:**
- Explicit mention of MCP tool function calls made
- Sequential thinking steps numbered and structured
- Context7 research findings with library IDs resolved
- Filesystem operations using mcp__filesystem__ tools

**UNACCEPTABLE (will result in rejection):**
- Only standard Claude tools mentioned (Read, Write, Edit, LS, Grep, Bash)
- No evidence of systematic thinking process
- No research performed for implementation tasks
- Vague references to "analysis" without MCP tool evidence

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

**REQUIRED DELIVERABLES:**

1. **Strategic Analysis**: Brief assessment of the technical issues and optimization opportunities
2. **Specialist Agent Selection**: List of required agents with specific reasons
3. **Delegation Plan**: Structured task breakdown with specific agent assignments
4. **Handoff Instructions**: Exact instructions for each specialist agent
5. **Coordination Strategy**: How tasks should be sequenced and dependencies managed

**EXPECTED OUTPUT FORMAT:**

```markdown
## Strategic Analysis
[Brief technical assessment focused on simplified architecture]

## Verified Specialist Agents (FROM CLAUDE.md ONLY)
- @agent-name: [specific reason and scope - VERIFIED EXISTS IN CLAUDE.md]

## Delegation Plan
### Task Group 1: [Priority Level]
- **Agent**: @agent-name (VERIFIED IN CLAUDE.md)
- **Scope**: [specific tasks for simplified architecture]
- **Handoff**: [exact instructions referencing simplified patterns]
- **Dependencies**: [prerequisites or blockers]

## Coordination Strategy
[How to execute the delegations in sequence for optimal performance]

## Execution Trigger
[MANDATORY: Provide the exact command to start the first delegation]
```

### Research Protocol Enforcement
- ❌ **No fictitious MCP tools** - Don't reference non-existent tools
- ✅ **Use Available Research Methods** - Use built-in analysis and reasoning capabilities
- ✅ **Document Analysis** - Read existing documentation and simplified architecture patterns
- ✅ **Code Pattern Research** - Analyze existing simplified codebase patterns

### Structured Analysis Requirements
- ✅ **Apply Systematic Thinking** - Break down complex problems methodically
- ✅ **Structured Problem Solving** - Use logical step-by-step analysis
- ✅ **Thought Progression** - Document reasoning process clearly
- ✅ **Adaptive Analysis** - Adjust approach as understanding deepens
- ✅ **Performance Focus** - Consider cost optimization and efficiency in all analysis

**VIOLATION CONSEQUENCES:**
- Fabricating agent names → Task rejection and re-delegation
- Stopping without execution → Manual intervention required
- Using non-existent tools → Incorrect implementation patterns

### Corrected Delegation Example
```
## Delegation Plan
### Task 1: Performance Optimization (CRITICAL)
- **Agent**: @performance-optimizer (VERIFIED in CLAUDE.md line 36)
- **Scope**: Optimize cost efficiency using simplified architecture patterns
- **Handoff**: Use patterns from existing code and documentation for cost reduction targets
- **Dependencies**: None

## Execution Trigger
@performance-optimizer: Optimize the processing efficiency in the simplified architecture using best practices from performance documentation. Apply cost reduction strategies maintaining 35% improvement target.
```

This enforcement ensures proper agent utilization and prevents violations while maintaining focus on simplified architecture and performance optimization.

## 🧠 MANDATORY ANALYSIS PROTOCOLS FOR ALL SPECIALIST AGENTS

**CRITICAL: ALL SPECIALIST AGENTS MUST FOLLOW THESE PROTOCOLS**

### 1. STRUCTURED THINKING ENFORCEMENT

**EVERY specialist agent MUST use structured analysis for:**

- 🧠 **Simplified Architecture Analysis**: Break down performance optimization and cost reduction systematically
- 📝 **Planning Before Implementation**: Outline approach, identify efficiency opportunities, consider performance alternatives
- 🔍 **Validation and Understanding**: Confirm task requirements and expected optimization outcomes
- ⚡ **Performance Analysis**: Identify cost reduction and speed improvement opportunities
- 🎯 **Solution Verification**: Validate approach maintains performance targets before implementation

**Required Analysis Pattern for ALL Agents:**

```markdown
## Task Analysis
### 1. Understanding the Problem
- [Clear definition of optimization or simplification needed]
- [Current performance state assessment]
- [Cost efficiency and speed improvement opportunities]

### 2. Solution Planning
- [Step-by-step implementation approach focused on performance]
- [Required resources and performance dependencies]
- [Cost optimization assessment and targets]

### 3. Implementation Strategy
- [Specific technical approaches for simplified architecture]
- [Performance testing and optimization validation plan]
- [Cost efficiency considerations and monitoring]

### 4. Success Validation
- [Measurable success criteria (35% cost reduction, 40% speed improvement)]
- [Performance testing procedures]
- [Quality verification steps with optimization focus]
```

## 🛠️ DEVELOPMENT WORKFLOW PROTOCOLS

**STRUCTURED APPROACH FOR ALL SPECIALIST AGENTS:**

### Standard Development Workflow

**PHASE 1: PLANNING AND ANALYSIS**
- Break down complex tasks systematically with performance focus
- Identify dependencies and optimization opportunities
- Research best practices for simplified architecture and cost efficiency
- Plan implementation approach with performance assessment

**PHASE 2: RESEARCH AND PREPARATION**
- Review existing simplified architecture documentation and patterns
- Analyze current performance optimization implementation conventions
- Study framework-specific best practices for cost efficiency from official documentation
- Document findings and chosen optimization approaches

**PHASE 3: IMPLEMENTATION**
- Apply researched patterns with performance optimization focus
- Use efficient operations for simplified architecture changes
- Implement comprehensive error handling with cost efficiency
- Follow established simplified architectural patterns

**PHASE 4: VALIDATION AND TESTING**
- Verify implementation meets performance targets (35% cost reduction, 40% speed improvement)
- Test optimization scenarios and efficiency edge cases
- Validate integration with simplified systems
- Document changes and performance test results

### Role-Specific Development Requirements

**@code-reviewer - MUST:**
- Perform systematic code analysis with simplified architecture focus
- Research latest performance optimization practices for validation
- Use comprehensive testing approaches for cost efficiency quality assurance

**@frontend-developer - MUST:**
- Research current single chat interface patterns and simplified user experience
- Plan UI implementations with performance and cost considerations
- Implement modern consolidated interface and simplified component architecture

**@backend-developer - MUST:**
- Research current simplified backend patterns, performance practices, and cost optimization
- Plan architecture changes with simplified system design considerations
- Implement robust dual-mode processing and cost-efficient error handling

**@performance-optimizer - MUST:**
- Research cost optimization techniques and performance enhancement patterns
- Plan efficiency improvements with systematic resource usage analysis
- Implement comprehensive monitoring and cost reduction strategies

**@documentation-specialist - MUST:**
- Structure comprehensive documentation with simplified architecture organization
- Research documentation standards focused on performance optimization
- Implement clear, actionable guides with cost efficiency examples

### Best Practices Research Topics

**Common Research Areas for Simplified Market Parser Project:**
- **@frontend-developer**: "single chat interface", "consolidated user experience", "simplified UI components", "performance-optimized interfaces"
- **@backend-developer**: "dual-mode response processing", "simplified architecture patterns", "cost-efficient state management", "performance optimization"
- **@api-architect**: "cost-efficient API design", "optimized response patterns", "performance-focused integration patterns"
- **@code-reviewer**: "simplified architecture best practices", "performance quality standards", "cost optimization patterns"
- **@performance-optimizer**: "cost reduction techniques", "processing speed optimization", "resource monitoring patterns", "efficiency strategies"
- **@code-archaeologist**: "simplified architecture analysis", "performance optimization patterns", "cost efficiency assessment"
- **@documentation-specialist**: "simplified documentation standards", "performance optimization guides", "cost efficiency documentation"

### 2. RESEARCH AND DOCUMENTATION MANDATE

**EVERY specialist agent MUST research best practices using:**

- 🔧 **Documentation Analysis**: Review existing simplified architecture documentation and performance guidelines
- 📚 **Performance Practices Research**: Study current cost optimization and efficiency standards
- 🔍 **Implementation Patterns**: Analyze existing simplified codebase patterns and performance conventions
- 📋 **Technology Standards**: Follow established framework-specific patterns with performance focus

**Required Research Approach:**
```markdown
## Research Phase
### 1. Current State Analysis
- [Review existing simplified implementation]
- [Identify performance patterns and cost optimization conventions]
- [Document current simplified architecture and efficiency metrics]

### 2. Best Practices Investigation
- [Technology-specific performance standards]
- [Industry cost optimization best practices]
- [Simplified architecture considerations]

### 3. Implementation Planning
- [Chosen approach with performance justification]
- [Integration with existing simplified systems]
- [Cost optimization and efficiency testing strategy]
```

### 3. MANDATORY TESTING PROTOCOL REQUIREMENTS

#### 🧪 CRITICAL: ALL OPTIMIZATIONS MUST INCLUDE PERFORMANCE VALIDATION

**TESTING MANDATE FOR ALL SPECIALIST AGENTS:**

- ✅ **MUST create performance test for every optimization** - No exceptions
- ✅ **MUST include efficiency criteria** - Define what constitutes successful cost reduction
- ✅ **MUST test resource scenarios** - Verify resource optimization works correctly
- ✅ **MUST validate performance targets** - Test maintains 35% cost reduction and 40% speed improvement
- ✅ **MUST document performance procedures** - Clear instructions for running efficiency tests

**Required Performance Test Structure:**

```python
#!/usr/bin/env python3
"""
Performance Test Script for [Optimization Description]
Created: [Date]
Purpose: Validate performance optimization for [specific improvement]
Success Criteria: 35% cost reduction, 40% speed improvement
"""

import pytest
import asyncio
import time
from typing import List, Dict, Any

class Test[OptimizationName]:
    """Test suite for [specific performance optimization]"""
    
    def setup_method(self):
        """Setup performance test environment"""
        # Initialize performance monitoring and test data
        pass
    
    def test_baseline_performance(self):
        """Establish baseline performance metrics"""
        # Measure current performance before optimization
        pass
    
    def test_cost_reduction(self):
        """Validate 35% cost reduction target"""
        # Test specific cost optimization implementation
        pass
    
    def test_speed_improvement(self):
        """Validate 40% speed improvement target"""
        # Test processing speed enhancement
        pass
    
    def test_resource_efficiency(self):
        """Test resource usage optimization"""
        # Test resource monitoring and efficiency improvements
        pass
    
    def test_simplified_architecture_performance(self):
        """Test simplified architecture maintains performance"""
        # Use real system interactions, actual performance data
        pass

def validate_performance_success() -> bool:
    """
    Run comprehensive validation of performance optimization
    Returns: True if all efficiency targets met, False otherwise
    """
    success_criteria = [
        "Cost Reduction: 35% improvement achieved",
        "Speed Improvement: 40% processing enhancement", 
        "Resource Efficiency: Optimized usage patterns"
    ]
    
    # Implementation of performance validation logic
    return all_criteria_met

if __name__ == "__main__":
    # Run the performance test suite
    pytest.main([__file__, "-v"])
    
    # Validate overall optimization success
    if validate_performance_success():
        print("✅ PERFORMANCE OPTIMIZATION: SUCCESS")
    else:
        print("❌ PERFORMANCE OPTIMIZATION: FAILED")
```

**Performance Success Criteria Standards:**

- **Cost Optimization**: Must achieve minimum 35% cost reduction through efficiency improvements
- **Processing Speed**: Must achieve minimum 40% speed improvement in response processing
- **Resource Usage**: Optimized memory and CPU usage with comprehensive monitoring
- **Simplified Architecture**: All optimizations must maintain simplified architecture integrity
- **User Experience**: No degradation in user experience with performance improvements

### 4. IMPLEMENTATION QUALITY REQUIREMENTS

**ALL specialist agents MUST:**

- ✅ **Use Structured Analysis First**: Never start implementation without systematic performance analysis
- ✅ **Research Before Implementing**: Study cost optimization practices and simplified architecture patterns
- ✅ **Follow Performance Standards**: Use only current best practices focused on efficiency
- 🛡️ **Include Cost-Efficient Error Handling**: Robust error management with resource optimization
- 🧪 **Plan Performance Strategy**: Include cost optimization and efficiency validation approaches
- 📋 **Document All Changes**: Clear explanations with performance impact assessment
- 🧪 **Create Performance Tests**: MANDATORY performance validation for every optimization
- 🔬 **Validate Efficiency**: Demonstrate optimization meets defined performance criteria
- 🎯 **Simplified Architecture Compliance**: Maintain simplified architecture patterns
- 📊 **Performance Monitoring**: Include metrics for cost reduction and speed improvement

### 5. QUALITY GATES AND VERIFICATION

**Before completing any task, ALL specialist agents MUST:**

- ✅ **Verify Analysis Completeness**: Confirm structured analysis with performance focus was performed
- ✅ **Validate Research**: Ensure implementation follows researched cost optimization practices
- ✅ **Test Performance Scenarios**: Confirm efficiency improvements work as designed
- ✅ **Check Architecture Compatibility**: Validate all changes maintain simplified architecture patterns
- ✅ **Preserve Performance**: Ensure changes maintain cost reduction and speed improvement targets
- ✅ **Address Efficiency Opportunities**: Confirm optimizations address identified performance improvements
- ✅ **NEW: Create and run performance validation tests**
- ✅ **NEW: Document performance results and efficiency criteria met**
- ✅ **PERFORMANCE SPECIFIC: Validate cost reduction and speed improvement targets**
- ✅ **PERFORMANCE SPECIFIC: Verify resource usage optimization within acceptable thresholds**

### 6. CONSEQUENCES FOR NON-COMPLIANCE

**FAILURE TO FOLLOW THESE PROTOCOLS WILL RESULT IN:**

- ❌ **Task Rejection**: Work will be rejected and must be redone with performance focus
- ❌ **Re-delegation**: Task will be reassigned to different agent with efficiency emphasis
- ❌ **Quality Gate Failure**: Code will not pass review process without performance validation
- ❌ **Performance Risk**: Changes may cause performance degradation or cost increases

**VERIFICATION CHECKLIST FOR ALL AGENTS:**
- [ ] Performed structured analysis with performance and cost focus
- [ ] Researched best practices for efficiency and simplified architecture
- [ ] Documented reasoning and approach with optimization justification
- [ ] Implemented solution using performance-focused patterns
- [ ] Added cost-efficient error handling and resource monitoring
- [ ] Planned and documented performance testing approach
- [ ] Created mandatory performance validation for optimizations
- [ ] Verified all efficiency requirements and targets are met

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
   # Optional: pricing for cost estimates (USD) - Updated for gpt-5-mini
   OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
   OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00
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

- **Run all tests**: `uv run pytest tests/` (pytest is in dev dependencies)
- **Run specific test**: `uv run pytest tests/test_file.py`
- **Run integration tests**: `uv run pytest tests/test_*integration*.py`
- **Run performance tests**: `uv run python tests/validate_performance_optimization.py`
- **Install dev dependencies**: `uv install --dev`

### Environment Management

- **Install dependencies**: `uv install`
- **Update dependencies**: `uv lock --upgrade`
- **Check environment**: `uv --version` and verify `.env` file exists

## Code Architecture

### Core Components

1. **market_parser_demo.py**: CLI application entry point
   - Contains `TokenCostTracker` class for usage/cost tracking with gpt-5-mini pricing
   - Implements `create_polygon_mcp_server()` factory function
   - Main async CLI loop with Rich console formatting

2. **chat_ui.py**: Simplified Gradio web interface with single chat focus
   - 🧠 **FSM-Driven State Management** - Simplified workflow with performance optimization
   - 📊 **Structured Stock Analysis** - Dedicated buttons for Snapshot, S&R, Technical Analysis  
   - 🎯 **Context-Aware Prompts** - Intelligent ticker extraction and cost-optimized prompts
   - ⏳ **Real-time Processing Status** - Loading states with performance monitoring
   - 🛡️ **Advanced Error Handling** - User-friendly messages with cost-efficient recovery
   - 💬 **Single Chat Interface** - All interactions in one consolidated conversation view
   - 🔍 **Performance Monitoring** - Cost tracking and efficiency diagnostics
   - 💾 **Export Functionality** - Enhanced export with performance metrics
   - Provides unified chat experience with dual-mode responses

### Key Architectural Patterns

- **MCP Server Integration**: Uses Pydantic AI's MCP server integration to connect with Polygon.io
- **Async Agent Framework**: Built on Pydantic AI with OpenAI gpt-5-mini model
- **Cost Tracking**: Comprehensive token usage and cost tracking with optimized pricing
- **Shared Components**: CLI and GUI share the same agent configuration and optimized MCP server setup
- **Dual-Mode Processing**: Button clicks return JSON responses, user messages return conversational text
- **Single Chat Interface**: All interactions flow through one consolidated conversation view

### Dependencies & Technologies

- **Core Framework**: `pydantic-ai-slim[openai,mcp]` for AI agent orchestration
- **Web Interface**: `gradio>=4.0.0` for the simplified GUI
- **CLI Formatting**: `rich` for terminal output formatting
- **Environment**: `python-dotenv` for configuration management
- **External APIs**: Polygon.io MCP server via uvx, OpenAI gpt-5-mini model
- **Performance Monitoring**: Enhanced cost tracking and resource usage monitoring

### System Prompt Configuration

The agent uses a consistent system prompt across both interfaces optimized for gpt-5-mini:

```text
"You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. Use the latest data available. Always double check your math. For any questions about the current date, use the 'get_today_date' tool. For long or complex queries, break the query into logical subtasks and process each subtask in order."
```

## File Structure

```
market-parser-polygon-mcp/
├── src/                          # Core application modules
│   ├── __init__.py
│   ├── response_parser.py        # Response parsing utilities for structured data extraction
│   ├── response_manager.py       # Dual-mode response processing (JSON/conversational)
│   ├── prompt_templates.py      # Structured prompt templates for analysis types
│   ├── performance_monitor.py   # Cost optimization and performance tracking
│   ├── security_utils.py        # Input validation and security utilities
│   └── example_json_responses.py # Example responses for testing and development
├── stock_data_fsm/              # Finite State Machine module for GUI state management
│   ├── __init__.py
│   ├── states.py                # Application states enum and context data classes
│   ├── transitions.py           # State transition rules and validation logic
│   ├── manager.py               # Main FSM controller with transition orchestration
│   └── tests/                   # FSM-specific test suite
│       ├── __init__.py
│       ├── test_states.py
│       ├── test_transitions.py
│       ├── test_manager.py
│       └── test_integration.py
├── tests/                       # Comprehensive test suite
│   ├── __init__.py
│   ├── test_integration.py      # Main integration tests
│   ├── test_actual_integration.py
│   ├── test_prompt_templates.py
│   ├── test_response_parser.py
│   ├── test_simplified_*.py     # Simplified architecture validation tests
│   ├── run_*.py                 # Test runners and validation scripts
│   └── validate_*.py            # Performance validation scripts
├── logs/                        # Application and debug logs
│   ├── performance_debug.log
│   ├── cost_optimization_*.log
│   └── debug_*.log
├── scripts/                     # Utility and demonstration scripts
│   ├── debug_performance_optimization.py
│   ├── demo_simplified_architecture.py
│   └── simple_test.py
├── config/                      # Configuration files (ready for future use)
├── docs/                        # Comprehensive documentation
│   ├── SIMPLIFIED_ARCHITECTURE_GUIDE.md
│   ├── USER_GUIDE_CHAT_INTERFACE.md
│   ├── PERFORMANCE_OPTIMIZATION_GUIDE.md
│   ├── TROUBLESHOOTING_SIMPLIFIED.md
│   ├── DEPLOYMENT_GUIDE_AWS.md
│   ├── reports/                 # Project reports and analysis
│   │   ├── README.md
│   │   ├── DUAL_MODE_RESPONSE_PROCESSING_REPORT.md
│   │   ├── PERFORMANCE_OPTIMIZATION_IMPLEMENTATION_REPORT.md
│   │   └── *.md                # Various technical reports
│   └── scratchpad.md           # Development notes
├── images/                      # Project assets and logos
│   └── logo.png
├── market_parser_demo.py        # CLI application entry point
├── chat_ui.py                   # Web GUI application (simplified single chat version)
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Lock file for reproducible builds
├── README.md                   # Main project documentation
├── CLAUDE.md                   # AI agent guidance and protocols
└── SECURITY.md                 # Security guidelines and best practices
```

## Development Patterns

### MCP Server Integration
The project uses the Polygon.io MCP server via `uvx` for real-time financial data access. The `create_polygon_mcp_server()` function in `market_parser_demo.py:42` handles server initialization and connection management with performance optimization.

### State Management (GUI)
The `stock_data_fsm` module implements a simplified finite state machine for efficient GUI workflow management:
- States are defined in `stock_data_fsm/states.py:12` with `AppState` enum
- Transitions managed by `StateManager` class in `stock_data_fsm/manager.py:25`
- Context data flows through `StateContext` objects for performance-optimized stateful operations

### Simplified Architecture
The `src/` directory contains the simplified architecture components:
- **Response Management**: `src/response_manager.py` handles dual-mode response processing
- **Performance Monitoring**: `src/performance_monitor.py` provides cost optimization and efficiency tracking
- **Response Processing**: `src/response_parser.py` handles optimized AI response extraction
- **Security**: `src/security_utils.py` ensures input validation with performance considerations

### Agent Configuration
Both CLI and GUI share identical agent setup with gpt-5-mini optimization:
- Model: `gpt-5-mini` via OpenAI Responses API
- System prompt focused on financial analysis accuracy with cost efficiency
- Token cost tracking via `TokenCostTracker` class with updated pricing

### Testing Strategy
- **Comprehensive Test Suite**: All tests organized in `tests/` directory with performance focus
- **FSM Tests**: Module-specific tests in `stock_data_fsm/tests/`
- **Integration Testing**: `tests/test_integration.py` and `tests/test_actual_integration.py`
- **Performance Testing**: `tests/validate_performance_optimization.py` for efficiency validation
- **Simplified Architecture**: `tests/test_simplified_*.py` for simplified system validation

### Import Patterns
With the simplified structure, use these import patterns:

```python
# Core modules from src/
from src.response_parser import ResponseParser
from src.response_manager import ResponseManager, ProcessingMode
from src.prompt_templates import PromptTemplateManager
from src.performance_monitor import PerformanceMonitor

# FSM components
from stock_data_fsm.states import AppState, StateContext
from stock_data_fsm.manager import StateManager
from stock_data_fsm.transitions import StateTransitions

# Security utilities
from src.security_utils import validate_input, sanitize_data
```

## Future Development

The `docs/SIMPLIFIED_ARCHITECTURE_GUIDE.md` contains detailed specifications for planned enhancements including:

- Performance optimization strategies
- Cost reduction techniques
- Single chat interface enhancements
- Dual-mode response processing improvements

When implementing new features, refer to existing patterns in the simplified agent configuration and cost optimization systems.

## Important Development Notes

- **Environment Setup**: Create `.env` file with required API keys and gpt-5-mini pricing before running applications
- **External Dependencies**: The Polygon.io MCP server requires `uvx` to be available in the system PATH
- **Architecture Preservation**: All file modifications during development should preserve the simplified architecture patterns and performance optimization
- **Cost Tracking**: Token cost tracking is optimized for gpt-5-mini pricing - check `TokenCostTracker` usage when adding new agent interactions
- **Model Configuration**: Default model is `gpt-5-mini` but can be overridden via `OPENAI_MODEL` environment variable
- **Testing Requirements**: Run tests from project root using `uv run pytest tests/` for the main test suite with performance validation
- **Performance Architecture**: Follow simplified patterns in `src/response_manager.py` for dual-mode processing and cost efficiency