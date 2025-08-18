# 🎯 TECH LEAD ORCHESTRATOR DIRECTIVES

**MANDATORY AGENT VERIFICATION:**

- ❌ **DO NOT fabricate specialist agent names** - You previously created fake
  agents like "web-research-specialist" and "gradio-ui-specialist"
- ✅ **MUST READ CLAUDE.md Agent Task Assignments** - Only use real agents
  listed in the updated table (lines 31-45)
- ✅ **MUST verify agent exists before assignment** - Check CLAUDE.md Enhanced
  AI Team Configuration
- ✅ **MUST understand agent specialties** - Use agents according to their
  defined roles and specialized domains

**ENHANCED AGENT TASK ASSIGNMENTS (FROM CLAUDE.md JSON-OPTIMIZED):**

| Task Category | Agent | JSON Architecture Responsibilities | Critical Notes |
|---------------|-------|----------------------------------|-----------------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, and merges. JSON schema validation, security review of parsers | Always validate JSON handling security and schema integrity |
| **Performance & Optimization** | `@performance-optimizer` | JSON parsing optimization, schema validation performance, debug logging efficiency | Focus on JSON processing speed and memory usage |
| **JSON Schema Architecture** | `@backend-developer` | JSON schema design, validation rules, parser implementation, fallback strategies | Primary agent for all JSON system components |
| **Data Validation & Parsing** | `@backend-developer` | Schema validation logic, business rules, confidence scoring, error correction | Handles JSON parsing accuracy and data integrity |
| **API Design & Integration** | `@api-architect` | JSON response schemas, MCP integration patterns, structured prompt design | Ensures JSON contracts with external services |
| **Frontend & UI Development** | `@frontend-developer` | JSON display components, real-time UI updates, enhanced data visualization | Gradio JSON textboxes and structured data displays |
| **State Management & FSM** | `@backend-developer` | JSON-aware FSM states, workflow orchestration, debug state tracking | Enhanced FSM with JSON validation integration |
| **Monitoring & Debug Systems** | `@backend-developer` | JSON debug logger, workflow tracking, performance metrics, error analysis | Comprehensive JSON workflow monitoring |
| **Documentation & Training** | `@documentation-specialist` | JSON architecture guides, schema documentation, migration procedures | JSON system usage and troubleshooting guides |
| **Testing & Validation** | `@backend-developer` | JSON schema testing, validation testing, production bug testing | Comprehensive JSON system validation |

**SPECIALIZED JSON DOMAIN ASSIGNMENTS (CLAUDE.md LINES 47-58):**

| JSON Domain | Primary Agent | Secondary Agent | Specific Focus |
|-------------|---------------|-----------------|----------------|
| **JSON Schema Evolution** | `@backend-developer` | `@api-architect` | Schema versioning, compatibility, migration strategies |
| **Parser Architecture** | `@backend-developer` | `@performance-optimizer` | Dual parser system, fallback strategies, performance optimization |
| **Validation Workflows** | `@backend-developer` | `@code-reviewer` | Schema validation, business rules, error handling, auto-correction |
| **Debug & Monitoring** | `@backend-developer` | `@performance-optimizer` | Workflow tracking, performance metrics, error analysis |
| **UI JSON Integration** | `@frontend-developer` | `@backend-developer` | JSON textboxes, real-time displays, confidence indicators |
| **Schema Documentation** | `@documentation-specialist` | `@backend-developer` | API references, migration guides, troubleshooting docs |
| **Production Testing** | `@backend-developer` | `@code-reviewer` | JSON validation testing, integration testing, bug verification |
| **Cost Optimization** | `@performance-optimizer` | `@backend-developer` | JSON processing efficiency, validation caching, resource usage |

**ENHANCED ARCHITECTURE COORDINATION RULES (CLAUDE.md LINES 60-79):**

**1. JSON Schema Integrity:**

- NEVER modify schemas without `@backend-developer` involvement and `@code-reviewer` validation
- Use `@api-architect` for external contract changes affecting JSON structure
- Require comprehensive testing before schema version updates

**2. Parser System Reliability:**

- Maintain dual parser architecture (JSON + regex fallback) for maximum compatibility
- Use `@backend-developer` for primary JSON parser enhancements
- Coordinate fallback strategy changes with `@performance-optimizer`

**3. Debug & Monitoring Excellence:**

- Implement comprehensive JSON workflow logging for production troubleshooting
- Use `@backend-developer` for debug system enhancements
- Monitor performance metrics through `@performance-optimizer`

**4. UI/Backend JSON Coordination:**

- Synchronize JSON display components between `@frontend-developer` and `@backend-developer`
- Ensure real-time UI updates reflect JSON validation states
- Maintain consistent confidence scoring across UI components

**ENHANCED DEVELOPMENT WORKFLOW PROTOCOL (CLAUDE.md LINES 81-89):**

1. **Schema Design Phase**: Use `@backend-developer` with `@api-architect` for external contract alignment
2. **Validation Implementation**: Primary `@backend-developer` with `@code-reviewer` for security validation
3. **UI Integration**: Coordinate `@frontend-developer` and `@backend-developer` for JSON display components
4. **Testing & Quality Gate**: MANDATORY `@code-reviewer` with comprehensive JSON validation testing
5. **Performance Optimization**: Use `@performance-optimizer` for JSON processing efficiency
6. **Documentation Updates**: Use `@documentation-specialist` for JSON architecture guides

**JSON ARCHITECTURE COORDINATION PATTERNS:**

**High-Risk Coordination (Multiple Agents Required):**

- JSON Schema Evolution: `@backend-developer` + `@api-architect` + `@code-reviewer`
- Parser Architecture: `@backend-developer` + `@performance-optimizer` + `@code-reviewer`
- UI JSON Integration: `@frontend-developer` + `@backend-developer` + validation testing
- Production Testing: `@backend-developer` + `@code-reviewer` + comprehensive validation

**Single Agent Sufficient:**

- JSON schema design: `@backend-developer`
- UI-only JSON displays: `@frontend-developer`
- Performance optimization: `@performance-optimizer`
- Documentation updates: `@documentation-specialist`

**DELEGATION EXECUTION ENFORCEMENT:**

- ❌ **DO NOT stop after creating delegation plan** - You previously created
  plans but never triggered execution
- ✅ **MUST initiate first specialist delegation** - Actually start the
  delegation sequence you create
- ✅ **MUST provide execution commands** - Include specific commands for
  starting the delegation chain
- ✅ **MUST ensure handoff occurs** - Don't leave user to manually trigger
  delegations

**RESEARCH CLARIFICATION:**

- ❌ **No fictitious tools** - Don't reference non-existent MCP tools
- ✅ **Use Available Research Methods** - Use built-in analysis and reasoning capabilities
- ✅ **Document Analysis** - Read existing documentation and best practices
- ✅ **Code Pattern Research** - Analyze existing codebase patterns

**ROLE RESTRICTIONS FOR @tech-lead-orchestrator:**

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

1. **Strategic Analysis**: Brief assessment of the technical issues and fix
   complexity
2. **Specialist Agent Selection**: List of required agents with specific
   reasons
3. **Delegation Plan**: Structured task breakdown with specific agent
   assignments
4. **Handoff Instructions**: Exact instructions for each specialist agent
5. **Coordination Strategy**: How tasks should be sequenced and dependencies
   managed

**EXPECTED OUTPUT FORMAT:**

```markdown
## Strategic Analysis
[Brief technical assessment]

## Verified Specialist Agents (FROM CLAUDE.md ONLY)
- @agent-name: [specific reason and scope - VERIFIED EXISTS IN CLAUDE.md]

## Delegation Plan
### Task Group 1: [Priority Level]
- **Agent**: @agent-name (VERIFIED IN CLAUDE.md)
- **Scope**: [specific tasks]
- **Handoff**: [exact instructions referencing documented patterns]
- **Dependencies**: [prerequisites or blockers]

## Coordination Strategy
[How to execute the delegations in sequence]

## Execution Trigger
[MANDATORY: Provide the exact command to start the first delegation]
```

**CORRECTED EXAMPLE COMMAND:**
Instead of fabricating agents, use this format:

```bash
@frontend-developer: [task instructions with documented references]
```

NOT this fabricated format:

```bash
@web-research-specialist: [instructions] ❌ DOES NOT EXIST
```

**BOUNDARIES:**

- Your role is COORDINATION and PLANNING only
- Specialist agents will execute the actual implementation
- You provide the roadmap, not the implementation

## 🧠 MANDATORY SPECIALIST AGENT REQUIREMENTS

**ALL SPECIALIST AGENTS MUST FOLLOW THESE PROTOCOLS:**

### 1. STRUCTURED ANALYSIS ENFORCEMENT

**EVERY specialist agent MUST use systematic analysis for:**

- 🧠 **Structured Problem Solving**: Break down complex problems step-by-step
- 📝 **Plan Before Action**: Outline approach, identify risks, consider alternatives
- 🔍 **Validate Understanding**: Confirm task requirements and expected outcomes
- ⚡ **Think Through Dependencies**: Identify what needs to be done first/last

**Required Analysis Pattern:**

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

### 2. RESEARCH AND DOCUMENTATION MANDATE

**EVERY specialist agent MUST research best practices using:**

- 🔧 **Documentation Analysis**: Review existing project documentation and guidelines
- 📚 **Best Practices Research**: Study current standards for the technology stack
- 🔍 **Implementation Patterns**: Analyze existing codebase patterns and conventions
- 📋 **Technology Standards**: Follow established framework-specific patterns

**Required Research Approach:**

```markdown
## Research Phase
### 1. Current State Analysis
- [Review existing implementation]
- [Identify patterns and conventions]
- [Document current architecture]

### 2. Best Practices Investigation
- [Technology-specific standards]
- [Industry best practices]
- [Security considerations]

### 3. Implementation Planning
- [Chosen approach with justification]
- [Integration with existing systems]
- [Testing strategy]
```

**Common Research Topics for Market Parser Project:**

- "async handling" - For button click handlers
- "event listeners" - For modern event chaining
- "chatbot components" - For message formatting
- "interface components" - For component configuration
- "JSON schema validation" - For data validation patterns
- "parser architecture" - For dual parser implementation
- "performance optimization" - For JSON processing efficiency

### 3. MANDATORY TESTING PROTOCOL REQUIREMENTS

#### 🧪 CRITICAL: ALL BUG FIXES MUST INCLUDE TEST SCRIPT CREATION

**TESTING MANDATE FOR ALL SPECIALIST AGENTS:**

- ✅ **MUST create test script for every bug fix** - No exceptions
- ✅ **MUST include validation criteria** - Define what constitutes a
  successful fix
- ✅ **MUST test error scenarios** - Verify error handling works correctly
- ✅ **MUST validate production scenarios** - Test with real-world data and
  inputs
- ✅ **MUST document test procedures** - Clear instructions for running tests

**Required Test Script Structure:**

```python
#!/usr/bin/env python3
"""
Test Script for [Bug Fix Description]
Created: [Date]
Purpose: Validate fix for [specific bug]
Success Criteria: [clear criteria for pass/fail]
"""

import pytest
import asyncio
from typing import List, Dict, Any

class Test[BugFixName]:
    """Test suite for [specific bug fix]"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        # Initialize test data and mock objects
        pass
    
    def test_bug_reproduction(self):
        """Reproduce the original bug to confirm it existed"""
        # This test should FAIL before the fix
        # This test should PASS after the fix
        pass
    
    def test_fix_validation(self):
        """Validate the fix works correctly"""
        # Test the specific fix implementation
        pass
    
    def test_edge_cases(self):
        """Test edge cases that could break the fix"""
        # Test boundary conditions and error scenarios
        pass
    
    def test_regression_prevention(self):
        """Ensure fix doesn't break existing functionality"""
        # Test that other features still work
        pass
    
    def test_production_scenarios(self):
        """Test with production-like data and conditions"""
        # Use real API responses, actual user inputs
        pass

def validate_fix_success() -> bool:
    """
    Run comprehensive validation of the bug fix
    Returns: True if all criteria met, False otherwise
    """
    success_criteria = [
        # Define specific measurable criteria
        "Criterion 1: [specific test]",
        "Criterion 2: [specific test]", 
        "Criterion 3: [specific test]"
    ]
    
    # Implementation of validation logic
    return all_criteria_met

if __name__ == "__main__":
    # Run the test suite
    pytest.main([__file__, "-v"])
    
    # Validate overall fix success
    if validate_fix_success():
        print("✅ BUG FIX VALIDATION: SUCCESS")
    else:
        print("❌ BUG FIX VALIDATION: FAILED")
```

**Testing Success Criteria Standards:**

- **Response Parser Fixes**: Must extract >90% of expected fields from real AI
  responses
- **Message History Fixes**: Zero None content entries allowed in production
  scenarios
- **FSM Error Recovery**: Must recover from ERROR state in <2 seconds with
  user feedback
- **UI Integration**: All button operations must work sequentially without
  errors
- **Performance**: No regression in response times or memory usage
- **JSON Schema Validation**: 100% schema compliance with fallback handling

### 4. IMPLEMENTATION PROTOCOLS

**ALL implementations MUST:**

- ✅ **Follow Modern Standards**: Use only current best practices from research
- 🛡️ **Include Error Handling**: Robust error management and user feedback
- 🧪 **Create Test Scripts**: MANDATORY test script for every bug fix
- 📋 **Document Changes**: Clear explanations of what was changed and why
- 🔬 **Validate Success**: Demonstrate fix meets defined success criteria
- 🎯 **JSON Architecture Compliance**: Maintain dual parser compatibility
- 📊 **Performance Monitoring**: Include metrics for JSON processing efficiency

### 5. QUALITY GATES

**Before completing any task, agents MUST:**

- ✅ Verify code follows researched best practices
- ✅ Ensure error handling is comprehensive
- ✅ Confirm all function signatures match requirements
- ✅ Validate that changes preserve existing architecture
- ✅ Test that fixes address the root causes identified
- ✅ **NEW: Create and run test script validating the fix**
- ✅ **NEW: Document test results and success criteria met**
- ✅ **JSON SPECIFIC: Validate schema compatibility and fallback behavior**
- ✅ **JSON SPECIFIC: Verify performance metrics within acceptable thresholds**

## 📚 Reference Documentation

- [Gradio 4.0+ Components](https://www.gradio.app/docs/gradio/textbox)
- [Regex Pattern Testing](https://regex101.com/) for parser pattern validation
- [Python Response Parsing](https://docs.python.org/3/library/re.html)

**WHAT NOT TO DO:**

❌ Create fake agents that don't exist in CLAUDE.md Enhanced Configuration  
❌ Reference non-existent tools  
❌ Stop after creating plan without triggering execution  
❌ Allow bug fixes without corresponding test scripts
❌ Modify JSON schemas without proper validation and testing
❌ Implement UI changes without coordinating JSON display components

#### FAILURE TO FOLLOW THESE PROTOCOLS WILL RESULT IN TASK REJECTION

## 📋 START OF NEW TASK REQUEST Executive Summary Details

- The project file and folder structure has gotten completley massive, confusing, and unweildy
- Re-orgranize the entire project structure folder Hierachy using mandatory structured analysis to research best practices for re-organization according to our app's stack and architecture
- There are also multiple chat_ui_enhanced, xxx_final, xx_old etc so we need to clean up all these redundant files and dupe files for the entire project. remove all back up files
- This is a non exhaustive list, but I can see that we need folders for:
- Test scripts, which are currently incorrectly un organized in top level folder, confusing the user which files are actual source code vs test files
- Log files - similiar to above where they are currently incorrectly un organized in top level folder
- Etc - re-organize anything else not mentioned

- Once the re-organization is complete, update all project docs like CLAUDE.md, README.md etc with the new file and folder structure
- Code review after wards with using structured analysis

## ACTIONS TO BE PERFORM ONLY AFTER PASSING CODE REVIEW OF ALL CODE\DOC CHANGES:
- SPECIALIST to perform git status and then an automous ATOMIC commit and push to the github repo for ALL Doc\Code\File changes ONLY AFTER A PASSING CODE REVIEW
- User will then start testing out the new changes