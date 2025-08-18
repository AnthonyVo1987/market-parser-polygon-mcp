# 🚨 MCP Tool Enforcement Guide for Delegated AI Specialists

> **CRITICAL**: This document provides enforcement protocols and templates. **TEMPORARY WAIVER ACTIVE** for specialist agents - see updated enforcement policy below.

## 📋 Overview

This enforcement guide addresses MCP tool enforcement protocols for AI specialists. **NOTE: Current policy includes a temporary waiver for specialist agents while maintaining full enforcement for Tech Lead Orchestrator.**

## 🚨 CURRENT ENFORCEMENT POLICY (Updated 2025-08-18)

### **TEMPORARY WAIVER FOR SPECIALIST AGENTS**

**SPECIALIST AGENTS (WAIVER ACTIVE):**
- ✅ **MCP Tool Enforcement WAIVED**: All specialist agents are temporarily **NOT REQUIRED** to use MCP tools
- ✅ **Standard Claude Tools ACCEPTABLE**: Read, Write, Edit, LS, Grep, Bash tools are sufficient
- ✅ **Quality Standards MAINTAINED**: All other development protocols remain fully enforced
- ✅ **Focus on Implementation**: Emphasis on high-quality deliverables using available tools

**TECH LEAD ORCHESTRATOR (FULL ENFORCEMENT CONTINUES):**
- ❌ **NO WAIVER GRANTED**: @tech-lead-orchestrator remains fully subject to ALL MCP tool requirements
- ❌ **Must Use MCP Tools**: All existing enforcement protocols remain active for orchestrator role
- ❌ **No Standard Tools**: Cannot use Read, Write, Edit, LS, Grep, Bash for orchestrator responsibilities

### **Rationale for Temporary Waiver**

**Technical Constraints Identified:**
- Sub-agent specialists currently cannot properly implement MCP tool calls due to system limitations
- Enforcement was preventing productive work completion
- Standard Claude tools provide adequate functionality for specialist implementation tasks

**Waiver Scope:**
- **APPLIES TO**: All specialist agents (`@code-reviewer`, `@backend-developer`, `@frontend-developer`, `@documentation-specialist`, `@performance-optimizer`, `@api-architect`, `@code-archaeologist`)
- **DOES NOT APPLY TO**: `@tech-lead-orchestrator` (remains fully subject to MCP enforcement)

## 📝 UPDATED DELEGATION TEMPLATE (CURRENT POLICY)

### **Standard Delegation Template for Specialist Agents**

When delegating to ANY specialist agent, use this updated template:

```markdown
## 📋 TASK DELEGATION TO SPECIALIST AGENT

**CURRENT POLICY**: MCP tool enforcement is temporarily waived for specialist agents.

## ✅ ACCEPTABLE TOOLS FOR SPECIALISTS:
- Standard Claude tools: Read, Write, Edit, LS, Grep, Bash
- Use the most efficient tools available for your task
- Focus on high-quality implementation and documentation

## 🎯 QUALITY STANDARDS (STILL MANDATORY):
- Follow all structured analysis protocols
- Research best practices using available documentation analysis
- Create comprehensive test scripts for all bug fixes
- Maintain all architectural patterns and coding standards
- Document all changes and implementation decisions thoroughly

## 📋 TASK DESCRIPTION:
[Insert specific task details here]

## 🎯 EXPECTED DELIVERABLES:
[Insert expected outcomes here]

## 📚 REFERENCE MATERIALS:
- Review existing project documentation and patterns
- Follow established coding conventions in codebase
- Maintain compatibility with JSON architecture standards
```

## 🔧 UPDATED ROLE-SPECIFIC CHECKLISTS

### **@code-reviewer Enforcement Checklist (WAIVED)**

**CURRENT REQUIREMENTS (Standard Tools Acceptable):**
- [ ] Performed systematic code analysis using structured approach
- [ ] Researched best practices through documentation review
- [ ] Applied framework knowledge from project patterns
- [ ] Provided specific evidence of analysis methodology
- [ ] Documented review findings with actionable recommendations

**NO LONGER REQUIRED:**
- ~~MCP sequential thinking tool usage~~
- ~~MCP context7 research evidence~~
- ~~Specific MCP tool verification~~

### **@backend-developer Enforcement Checklist (WAIVED)**

**CURRENT REQUIREMENTS (Standard Tools Acceptable):**
- [ ] Used structured planning approach for implementation
- [ ] Researched backend patterns through codebase analysis
- [ ] Applied current best practices from documentation
- [ ] Used efficient file operations for development
- [ ] Documented architectural decisions and implementation approach

**NO LONGER REQUIRED:**
- ~~MCP sequential thinking evidence~~
- ~~MCP context7 framework research~~
- ~~MCP filesystem tool requirements~~

### **@frontend-developer Enforcement Checklist (WAIVED)**

**CURRENT REQUIREMENTS (Standard Tools Acceptable):**
- [ ] Used systematic UI/UX planning approach
- [ ] Researched frontend patterns through project analysis
- [ ] Applied modern UI patterns from documentation
- [ ] Implemented efficient file operations
- [ ] Documented frontend architecture decisions

**NO LONGER REQUIRED:**
- ~~MCP sequential thinking for UI planning~~
- ~~MCP context7 frontend research~~
- ~~MCP filesystem tool requirements~~

### **@documentation-specialist Enforcement Checklist (WAIVED)**

**CURRENT REQUIREMENTS (Standard Tools Acceptable):**
- [ ] Used structured approach to documentation organization
- [ ] Applied efficient file operations for documentation updates
- [ ] Researched documentation standards through existing patterns
- [ ] Maintained consistency with project documentation style

**NO LONGER REQUIRED:**
- ~~MCP sequential thinking for structure planning~~
- ~~MCP filesystem tool requirements~~

## 🎯 UPDATED EVIDENCE VALIDATION

### **✅ ACCEPTABLE Evidence (Under Current Policy)**

**Structured Analysis Evidence:**
```
I performed systematic analysis of this task:

Step 1: Analyzed current code structure and identified key issues...
Step 2: Researched best practices through documentation review...
Step 3: Planned implementation approach with risk assessment...
Step 4: Validated approach against project requirements...
```

**Documentation Research Evidence:**
```
I researched current patterns by:
- Reviewing existing project documentation and coding patterns
- Analyzing framework usage in current codebase
- Studying established architectural conventions
- Applied findings: [specific patterns and practices used]
```

**Implementation Evidence:**
```
Used standard Claude tools for efficient development:
- Read multiple files to understand current implementation
- Analyzed project structure and conventions
- Implemented changes following established patterns
- Tested implementation against project standards
```

### **❌ STILL UNACCEPTABLE (Even Under Waiver)**

**Poor Quality Analysis:**
```
I fixed the code and it should work now...
[VIOLATION: No systematic analysis performed]
```

**No Research Performed:**
```
I implemented the feature using basic patterns...
[VIOLATION: No investigation of project standards or best practices]
```

**Missing Documentation:**
```
Updated the files as requested...
[VIOLATION: No documentation of changes or implementation decisions]
```

## 🚨 TECH LEAD ORCHESTRATOR ENFORCEMENT (UNCHANGED - FULL ENFORCEMENT)

### **@tech-lead-orchestrator MUST STILL USE MCP TOOLS**

**NO WAIVER GRANTED**: Tech Lead Orchestrator remains fully subject to all MCP tool requirements.

**MANDATORY MCP TOOLS FOR @tech-lead-orchestrator:**
```markdown
## 🚨 MANDATORY MCP TOOL REQUIREMENTS FOR ORCHESTRATOR:
You MUST use these MCP tools (VIOLATION = IMMEDIATE REJECTION):
- ✅ mcp__sequential-thinking__sequentialthinking - For systematic analysis
- ✅ mcp__context7__resolve-library-id + get-library-docs - For research
- ✅ mcp__filesystem__* - For file operations

## 📝 EVIDENCE REQUIREMENTS FOR ORCHESTRATOR:
You MUST provide explicit evidence of MCP tool usage:
1. Sequential thinking steps showing systematic approach
2. Context7 research findings with specific discoveries
3. Filesystem operations evidence with specific tool calls

⚠️ CRITICAL: @tech-lead-orchestrator using only standard Claude tools 
will result in IMMEDIATE WORK REJECTION and re-delegation.
```

## 🔄 UPDATED VIOLATION RESPONSE PROTOCOL

### **For Specialist Agents (Under Waiver):**

**Acceptable Violations (No Longer Enforced):**
- Using only standard Claude tools (Read, Write, Edit, LS, Grep, Bash)
- Not providing MCP sequential thinking evidence
- Not using MCP context7 for research
- Not using MCP filesystem tools

**Still Unacceptable Violations:**
- No systematic analysis or structured approach
- No research of project patterns and standards
- Poor quality implementation without documentation
- Failure to follow established architectural patterns

### **For Tech Lead Orchestrator (Full Enforcement):**

**When MCP Tool Violations Occur:**

1. **IMMEDIATE REJECTION**: Stop the task and reject the work
2. **SPECIFY VIOLATIONS**: Clearly identify which MCP tools were missing
3. **PROVIDE TEMPLATE**: Give the orchestrator the exact MCP enforcement template
4. **RE-DELEGATE**: Use the mandatory delegation template for retry
5. **VERIFY COMPLIANCE**: Check all evidence requirements before acceptance

**Rejection Message Template for Orchestrator:**

```markdown
## 🚨 ORCHESTRATOR WORK REJECTED - MCP TOOL VIOLATION

Your work as @tech-lead-orchestrator has been rejected for failing to use mandatory MCP tools.

**VIOLATIONS IDENTIFIED:**
- [ ] Missing mcp__sequential-thinking__sequentialthinking evidence
- [ ] Missing mcp__context7 research evidence  
- [ ] Missing mcp__filesystem tool evidence
- [ ] Used only standard Claude tools (NOT ALLOWED for orchestrator)

**REQUIRED CORRECTIVE ACTION:**
You must redo this orchestration task using the mandatory MCP tools for your role.
Refer to the full MCP enforcement requirements for orchestrator.

**REMINDER**: The temporary waiver applies ONLY to specialist agents, NOT to orchestrator.
```

## 📚 UPDATED DELEGATION EXAMPLES

### **Example 1: Code Review with Updated Policy**

```markdown
@code-reviewer: Perform comprehensive code review of project restructuring changes.

## 📋 TASK DELEGATION TO SPECIALIST AGENT

**CURRENT POLICY**: MCP tool enforcement is temporarily waived for specialist agents.

## ✅ ACCEPTABLE TOOLS:
- Standard Claude tools: Read, Write, Edit, LS, Grep, Bash
- Use the most efficient approach for comprehensive code review

## 🎯 QUALITY STANDARDS (STILL REQUIRED):
- Perform systematic code analysis with structured approach
- Research best practices through documentation and codebase analysis
- Validate new src/ and tests/ structure follows Python best practices
- Check import updates and path references thoroughly
- Ensure documentation accuracy and completeness
- Verify no functionality was broken in restructuring

## 📋 TASK: Review all code and documentation changes from project restructuring
- Analyze project structure against established Python conventions
- Validate architectural patterns and import dependencies
- Check for security implications and code quality issues
- Provide specific recommendations for any improvements needed

## 🎯 DELIVERABLES:
- Systematic analysis following structured review process
- Validation of chosen architectural patterns
- Comprehensive review report with specific actionable recommendations
```

### **Example 2: Backend Development with Updated Policy**

```markdown
@backend-developer: Implement async handler fixes for GUI components.

## 📋 TASK DELEGATION TO SPECIALIST AGENT

**CURRENT POLICY**: MCP tool enforcement is temporarily waived for specialist agents.

## ✅ ACCEPTABLE TOOLS:
- Standard Claude tools: Read, Write, Edit, LS, Grep, Bash
- Focus on efficient implementation using available tools

## 🎯 QUALITY STANDARDS (STILL REQUIRED):
- Use systematic planning for async implementation architecture
- Research current Python async/await patterns through documentation
- Apply established project patterns and coding conventions
- Create comprehensive test script for validation
- Document implementation decisions and architectural choices

## 📋 TASK: Fix async button handlers in chat_ui.py
- Analyze current async handling issues and root causes
- Research best practices for Gradio async event handling
- Implement modern async patterns compatible with project architecture
- Ensure proper error handling and user feedback
- Test implementation thoroughly with production scenarios

## 🎯 DELIVERABLES:
- Systematic implementation plan with risk assessment
- Fixed async handlers using researched best practices
- Comprehensive test script validating the fixes
- Documentation of changes and implementation approach
```

## 🎯 SUCCESS METRICS UNDER CURRENT POLICY

### **✅ COMPLIANT Specialist Response (Under Waiver):**
- Uses systematic structured analysis approach
- Demonstrates research through documentation and codebase review
- Applies established project patterns and coding standards
- Provides clear documentation of implementation decisions
- Creates test scripts for bug fixes when applicable
- Maintains architectural consistency with existing codebase

### **❌ NON-COMPLIANT Specialist Response (Still Rejected):**
- No systematic analysis or planning evident
- No research of project standards or best practices
- Poor quality implementation without proper documentation
- Breaks established architectural patterns or conventions
- Missing test scripts for bug fixes
- No explanation of implementation decisions or approach

### **✅ COMPLIANT Orchestrator Response (Full MCP Enforcement):**
- Uses all mandatory MCP tools for the orchestrator role
- Provides specific evidence of MCP tool usage with concrete results
- Shows systematic thinking progression using MCP sequential thinking
- Documents research findings from MCP context7 tools
- Demonstrates MCP filesystem operations when applicable

### **❌ NON-COMPLIANT Orchestrator Response (Still Rejected):**
- Uses only standard Claude tools instead of required MCP tools
- No systematic analysis evidence from MCP tools
- No research performed using MCP context7
- Vague or incomplete documentation without MCP tool evidence
- Any attempt to use standard tools for orchestrator responsibilities

## 🔄 FUTURE POLICY CONSIDERATIONS

### **Monitoring Current Policy:**

1. **Track Specialist Quality**: Monitor work quality under the waiver system
2. **Evaluate Effectiveness**: Assess whether quality standards are maintained
3. **Technical Progress**: Watch for improvements in MCP tool accessibility
4. **Policy Adjustment**: Modify enforcement as technical constraints change

### **Potential Policy Updates:**

This waiver policy should be reviewed when:
- MCP tool accessibility improves for specialist agents
- Quality standards require adjustment under the waiver system  
- Technical limitations are resolved
- Better enforcement strategies are developed

---

**CRITICAL REMINDER**: 
- **SPECIALIST AGENTS**: Currently operate under temporary MCP tool waiver - use standard Claude tools
- **TECH LEAD ORCHESTRATOR**: Remains fully subject to MCP tool enforcement with no waiver granted
- All quality standards and development protocols remain fully enforced for all agents