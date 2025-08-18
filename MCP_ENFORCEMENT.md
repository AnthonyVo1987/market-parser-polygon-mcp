# 🚨 MCP Tool Enforcement Guide for Delegated AI Specialists

> **CRITICAL**: This document provides enforcement protocols and templates to ensure ALL delegated AI specialists use mandatory MCP tools according to their role requirements.

## 📋 Overview

This enforcement guide addresses the critical issue where delegated AI specialists were using only standard Claude tools (Read, Write, Edit, LS, Grep, Bash) instead of the mandatory MCP tools required by their roles. This violation undermines the project's quality standards and must be prevented.

## 🚨 DELEGATION TEMPLATE WITH MCP ENFORCEMENT

### **Standard Delegation Template (MANDATORY)**

When delegating to ANY specialist, use this exact template structure:

```markdown
## 🚨 MANDATORY MCP TOOL REQUIREMENTS:
You MUST use these MCP tools (VIOLATION = IMMEDIATE REJECTION):

**For @code-reviewer:**
- ✅ mcp__sequential-thinking__sequentialthinking - For systematic code analysis
- ✅ mcp__context7__resolve-library-id + get-library-docs - For best practices research

**For @backend-developer:**
- ✅ mcp__sequential-thinking__sequentialthinking - For architecture planning
- ✅ mcp__context7__resolve-library-id + get-library-docs - For backend patterns research
- ✅ mcp__filesystem__* - For file operations

**For @frontend-developer:**
- ✅ mcp__sequential-thinking__sequentialthinking - For UI/UX planning
- ✅ mcp__context7__resolve-library-id + get-library-docs - For frontend patterns research
- ✅ mcp__filesystem__* - For file operations

**For @documentation-specialist:**
- ✅ mcp__sequential-thinking__sequentialthinking - For documentation structuring
- ✅ mcp__filesystem__* - For file operations

## 📝 EVIDENCE REQUIREMENTS:
You MUST provide explicit evidence of MCP tool usage in your response:

1. **Sequential Thinking Evidence**: Show numbered thought progression
2. **Context7 Research Evidence**: Show library resolution and documentation retrieval
3. **Filesystem Evidence**: Show specific MCP filesystem tool calls made

## ❌ UNACCEPTABLE (WILL RESULT IN REJECTION):
- Using only: Read, Write, Edit, LS, Grep, Bash
- No systematic thinking evidence
- No research performed
- Vague analysis without structured steps

## 📋 TASK DESCRIPTION:
[Insert specific task details here]

## 🎯 EXPECTED DELIVERABLES:
[Insert expected outcomes here]
```

## 🔧 ROLE-SPECIFIC ENFORCEMENT CHECKLISTS

### **@code-reviewer Enforcement Checklist**

**BEFORE accepting code review results, verify:**
- [ ] Used `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- [ ] Used `mcp__context7__resolve-library-id` to research best practices
- [ ] Used `mcp__context7__get-library-docs` to get current framework patterns
- [ ] Provided specific evidence of each MCP tool call made
- [ ] Analysis includes numbered thought progression
- [ ] Research findings are documented with specific discoveries

**REJECTION CRITERIA:**
- ❌ Only mentions standard Claude tools
- ❌ No systematic thinking evidence provided
- ❌ No framework research performed
- ❌ Vague analysis without structured breakdown

### **@backend-developer Enforcement Checklist**

**BEFORE accepting backend implementation, verify:**
- [ ] Used `mcp__sequential-thinking__sequentialthinking` for planning
- [ ] Used `mcp__context7__resolve-library-id` for framework research
- [ ] Used `mcp__context7__get-library-docs` for backend patterns
- [ ] Used `mcp__filesystem__*` tools for file operations
- [ ] Provided evidence of architectural planning steps
- [ ] Documented research findings and chosen patterns

**REJECTION CRITERIA:**
- ❌ Implementation without systematic planning
- ❌ No research of current backend patterns
- ❌ Using outdated implementation approaches
- ❌ Missing MCP filesystem tool evidence

### **@frontend-developer Enforcement Checklist**

**BEFORE accepting frontend implementation, verify:**
- [ ] Used `mcp__sequential-thinking__sequentialthinking` for UI planning
- [ ] Used `mcp__context7__resolve-library-id` for frontend framework research
- [ ] Used `mcp__context7__get-library-docs` for current UI patterns
- [ ] Used `mcp__filesystem__*` tools for file operations
- [ ] Provided evidence of UI/UX planning steps
- [ ] Documented modern frontend patterns discovered

**REJECTION CRITERIA:**
- ❌ UI implementation without systematic planning
- ❌ No research of current frontend patterns
- ❌ Using outdated UI/UX approaches
- ❌ Missing MCP filesystem tool evidence

### **@documentation-specialist Enforcement Checklist**

**BEFORE accepting documentation, verify:**
- [ ] Used `mcp__sequential-thinking__sequentialthinking` for structure planning
- [ ] Used `mcp__filesystem__*` tools for file operations
- [ ] Provided evidence of documentation structuring steps
- [ ] Clear systematic approach to documentation organization

**REJECTION CRITERIA:**
- ❌ Documentation without systematic planning
- ❌ No structured approach to organization
- ❌ Missing MCP filesystem tool evidence

## 🎯 EVIDENCE VALIDATION EXAMPLES

### **✅ ACCEPTABLE Evidence Examples**

**Sequential Thinking Evidence:**
```
I used mcp__sequential-thinking__sequentialthinking to systematically analyze this task:

Thought 1: Analyzed current code structure and identified 3 main issues...
Thought 2: Researched best practices for addressing these patterns...
Thought 3: Planned implementation approach with risk mitigation...
Thought 4: Validated approach against project requirements...
```

**Context7 Research Evidence:**
```
I used mcp__context7__resolve-library-id to research "react" patterns:
- Resolved library ID: /facebook/react
- Used mcp__context7__get-library-docs with topic "hooks and concurrent features"
- Key findings: [specific patterns and best practices discovered]
- Applied findings to implementation: [how research informed the solution]
```

**Filesystem Evidence:**
```
Used MCP filesystem tools for efficient operations:
- mcp__filesystem__read_multiple_files: Examined /path/file1.py, /path/file2.py
- mcp__filesystem__directory_tree: Analyzed project structure
- mcp__filesystem__edit_file: Updated imports and configurations
```

### **❌ UNACCEPTABLE Evidence Examples**

**Missing MCP Tools:**
```
I used Read, Write, and Edit tools to review the code...
[VIOLATION: No MCP tools used]
```

**Vague Analysis:**
```
I analyzed the code and it looks good...
[VIOLATION: No systematic thinking evidence]
```

**No Research:**
```
I implemented the feature using standard patterns...
[VIOLATION: No Context7 research performed]
```

## 🚨 VIOLATION RESPONSE PROTOCOL

### **When MCP Tool Violations Occur:**

1. **IMMEDIATE REJECTION**: Stop the task and reject the work
2. **SPECIFY VIOLATIONS**: Clearly identify which MCP tools were missing
3. **PROVIDE TEMPLATE**: Give the specialist the exact MCP enforcement template
4. **RE-DELEGATE**: Use the mandatory delegation template for retry
5. **VERIFY COMPLIANCE**: Check all evidence requirements before acceptance

### **Rejection Message Template:**

```markdown
## 🚨 WORK REJECTED - MCP TOOL VIOLATION

Your work has been rejected for failing to use mandatory MCP tools.

**VIOLATIONS IDENTIFIED:**
- [ ] Missing mcp__sequential-thinking__sequentialthinking evidence
- [ ] Missing mcp__context7 research evidence  
- [ ] Missing mcp__filesystem tool evidence
- [ ] Used only standard Claude tools (Read, Write, Edit, etc.)

**REQUIRED CORRECTIVE ACTION:**
You must redo this task using the mandatory MCP tools for your role.
Refer to the delegation template above for exact requirements.

**EVIDENCE REQUIREMENTS:**
Provide explicit proof of each MCP tool call made with specific results.
```

## 📚 DELEGATION EXAMPLES

### **Example 1: Code Review with MCP Enforcement**

```markdown
@code-reviewer: Perform comprehensive code review of project restructuring changes.

## 🚨 MANDATORY MCP TOOL REQUIREMENTS:
You MUST use these MCP tools (VIOLATION = IMMEDIATE REJECTION):
- ✅ mcp__sequential-thinking__sequentialthinking - For systematic code analysis
- ✅ mcp__context7__resolve-library-id + get-library-docs - For best practices research

## 📝 EVIDENCE REQUIREMENTS:
Provide explicit evidence showing:
1. Sequential thinking with numbered thought progression
2. Context7 research of Python project best practices
3. Specific findings from framework research

## 📋 TASK: Review all code and documentation changes from project restructuring
- Verify new src/ and tests/ structure follows Python best practices
- Check import updates and path references
- Validate documentation accuracy
- Ensure no functionality was broken

## 🎯 DELIVERABLES:
- Systematic analysis using sequential thinking
- Research validation of chosen patterns
- Comprehensive review report with specific recommendations
```

### **Example 2: Backend Development with MCP Enforcement**

```markdown
@backend-developer: Implement async handler fixes for GUI components.

## 🚨 MANDATORY MCP TOOL REQUIREMENTS:
You MUST use these MCP tools (VIOLATION = IMMEDIATE REJECTION):
- ✅ mcp__sequential-thinking__sequentialthinking - For architecture planning
- ✅ mcp__context7__resolve-library-id + get-library-docs - For async patterns research
- ✅ mcp__filesystem__* - For file operations

## 📝 EVIDENCE REQUIREMENTS:
1. Show systematic planning steps for async implementation
2. Research current Python async/await best practices
3. Document MCP filesystem operations performed

## 📋 TASK: Fix async button handlers in chat_ui.py
[Task details...]
```

## 🎯 SUCCESS METRICS

### **Quality Indicators for MCP Compliance:**

**✅ COMPLIANT Specialist Response:**
- Uses all mandatory MCP tools for their role
- Provides specific evidence of tool usage
- Shows systematic thinking progression
- Documents research findings clearly
- Applies discovered patterns appropriately

**❌ NON-COMPLIANT Specialist Response:**
- Uses only standard Claude tools
- No systematic analysis evidence
- No research performed
- Vague or incomplete documentation
- No integration of best practices

## 🔄 CONTINUOUS IMPROVEMENT

### **Monitoring and Adjustment:**

1. **Track Compliance**: Monitor which specialists consistently use MCP tools
2. **Identify Patterns**: Note common violation types and adjust templates
3. **Update Documentation**: Refine enforcement based on observed issues
4. **Training Updates**: Improve delegation templates based on results

### **Template Evolution:**

This enforcement guide should be updated whenever:
- New MCP tools become available
- Specialist role requirements change
- Violation patterns emerge that need addressing
- Better enforcement strategies are discovered

---

**CRITICAL REMINDER**: This enforcement guide must be referenced and applied for EVERY specialist delegation to ensure quality standards are maintained and MCP tool violations are prevented.