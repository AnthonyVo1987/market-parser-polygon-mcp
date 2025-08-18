# 🛠️ MCP Server Tool Usage Guide - Comprehensive Reference

> **Target Audience**: AI Coding Agents  
> **Purpose**: Definitive guide for proper MCP tool usage, syntax, and best practices  
> **Last Updated**: 2025-08-18 (Policy Update)

## 📋 Executive Summary

This guide provides comprehensive documentation for the three primary MCP (Model Context Protocol) tools available in our development environment. **IMPORTANT: Current enforcement policy has been updated - see Critical Usage Requirements section.**

## 🚨 UPDATED ENFORCEMENT POLICY (2025-08-18)

### **TEMPORARY WAIVER FOR SPECIALIST AGENTS**

**SPECIALIST AGENTS (MCP ENFORCEMENT WAIVED):**

- ✅ **NOT REQUIRED to use MCP tools** - Temporary waiver active
- ✅ **Standard Claude tools sufficient** - Read, Write, Edit, LS, Grep, Bash are acceptable
- ✅ **Quality standards maintained** - All other protocols remain fully enforced
- ✅ **Focus on deliverables** - Emphasis on high-quality implementation

**TECH LEAD ORCHESTRATOR (FULL MCP ENFORCEMENT CONTINUES):**

- ❌ **NO WAIVER GRANTED** - @tech-lead-orchestrator must still use ALL MCP tools
- ❌ **MCP tools mandatory** - All existing enforcement protocols remain active
- ❌ **No standard tools** - Cannot use Read, Write, Edit, LS, Grep, Bash

## 🔄 Critical Usage Requirements by Role (UPDATED)

### **@code-reviewer** - WAIVER ACTIVE

- ~~NOT REQUIRED: sequential-thinking~~ - Waived under current policy
- ~~NOT REQUIRED: context7 research~~ - Waived under current policy
- ✅ **ACCEPTABLE**: Standard systematic analysis using Claude tools

### **@frontend-developer** - WAIVER ACTIVE

- ~~NOT REQUIRED: sequential-thinking~~ - Waived under current policy
- ~~NOT REQUIRED: context7 research~~ - Waived under current policy
- ~~NOT REQUIRED: filesystem tools~~ - Waived under current policy
- ✅ **ACCEPTABLE**: Standard Claude tools for all operations

### **@backend-developer** - WAIVER ACTIVE

- ~~NOT REQUIRED: sequential-thinking~~ - Waived under current policy
- ~~NOT REQUIRED: context7 research~~ - Waived under current policy
- ~~NOT REQUIRED: filesystem tools~~ - Waived under current policy
- ✅ **ACCEPTABLE**: Standard Claude tools for all operations

### **@documentation-specialist** - WAIVER ACTIVE

- ~~NOT REQUIRED: sequential-thinking~~ - Waived under current policy
- ~~NOT REQUIRED: filesystem tools~~ - Waived under current policy
- ✅ **ACCEPTABLE**: Standard Claude tools for documentation work

### **@tech-lead-orchestrator** - FULL MCP ENFORCEMENT (NO WAIVER)

- ✅ **STILL REQUIRED: sequential-thinking** - For systematic orchestration analysis
- ✅ **STILL REQUIRED: context7** - For research of orchestration patterns
- ✅ **STILL REQUIRED: filesystem** - For orchestration file operations

---

## 🔧 Tool 1: Context7 - Latest Documentation Research

### **Current Enforcement Status**

- **SPECIALIST AGENTS**: ~~NOT REQUIRED~~ (Waived under current policy)
- **TECH LEAD ORCHESTRATOR**: **REQUIRED** (Full enforcement continues)

### **Purpose**

Context7 provides access to the most up-to-date documentation, best practices, and code examples for any library or framework. It's your primary tool for researching current development patterns.

### **When to Use (Orchestrator Only)**

- ✅ Researching latest framework versions (React 18+, Vue 3+, Gradio 4+, etc.)
- ✅ Finding current API syntax and best practices
- ✅ Getting code examples for modern patterns
- ✅ Understanding breaking changes between versions
- ✅ Before orchestrating any complex development delegation

### **When NOT to Use**

- ❌ For general programming concepts (use standard knowledge)
- ❌ For project-specific code (use filesystem tools)
- ❌ For debugging existing code (use other analysis tools)
- ❌ **SPECIALIST AGENTS: Not required under current waiver policy**

### **Proper Tool Call Syntax (Orchestrator Only)**

#### Step 1: Resolve Library ID

```javascript
mcp_context7_resolve-library-id
Parameters:
{
  "libraryName": "exact-library-name"  // e.g., "gradio", "react", "fastapi"
}
```

#### Step 2: Get Documentation

```javascript
mcp_context7_get-library-docs
Parameters:
{
  "context7CompatibleLibraryID": "/org/project",     // From step 1 result
  "topic": "specific-topic",                          // Optional: focus area
  "tokens": 5000                                      // Optional: response size limit
}
```

### **Best Practices (Orchestrator Only)**

1. **Always resolve library ID first** - Don't guess the Context7 ID format
2. **Be specific with topics** - "async handling in gradio 4.0" vs just "gradio"
3. **Use appropriate token limits** - 5000-10000 for detailed research
4. **Document findings** - Save key patterns found for team reference

### **Common Mistakes to Avoid (Orchestrator Only)**

❌ **Wrong**: Guessing library IDs

```javascript
// DON'T DO THIS
"context7CompatibleLibraryID": "/gradio/gradio"  // Wrong format
```

✅ **Correct**: Always resolve first

```javascript
// Step 1: Resolve
mcp_context7_resolve-library-id({"libraryName": "gradio"})
// Result: "/gradio-app/gradio"

// Step 2: Use resolved ID
mcp_context7_get-library-docs({"context7CompatibleLibraryID": "/gradio-app/gradio"})
```

### **Alternative Research Methods for Specialists (Under Waiver)**

**ACCEPTABLE for specialist agents:**

- Review existing project documentation and patterns
- Analyze current codebase implementation conventions
- Study framework usage examples in existing code
- Research through standard documentation analysis methods

---

## 🧠 Tool 2: Sequential Thinking - Problem Decomposition

### **Current Enforcement Status for Sequential Thinking**

- **SPECIALIST AGENTS**: ~~NOT REQUIRED~~ (Waived under current policy)
- **TECH LEAD ORCHESTRATOR**: **REQUIRED** (Full enforcement continues)

### **Sequential Thinking Purpose**

Breaks down complex problems into manageable, step-by-step thought processes. Essential for planning, architecture decisions, and systematic problem-solving.

### **When to Use (Orchestrator Only)**

- ✅ Planning complex delegation strategies
- ✅ Orchestrating multi-component development tasks
- ✅ Strategic architecture and design decisions
- ✅ Complex team coordination analysis
- ✅ Before delegating any non-trivial development work

### **When NOT to Use**

- ❌ Simple, single-step orchestration tasks
- ❌ Routine delegation operations
- ❌ **SPECIALIST AGENTS: Not required under current waiver policy**

### **Proper Tool Call Syntax (Orchestrator Only)**

```javascript
mcp_sequential-thinking_sequentialthinking
Parameters:
{
  "thought": "Your current thinking step",
  "nextThoughtNeeded": true/false,
  "thoughtNumber": 1,           // Current step number
  "totalThoughts": 5,           // Estimated total steps
  "isRevision": false,          // Optional: if revising previous thought
  "revisesThought": 2,          // Optional: which thought to revise
  "branchFromThought": 3,       // Optional: branching point
  "branchId": "alternative-a", // Optional: branch identifier
  "needsMoreThoughts": false    // Optional: if need to extend
}
```

### **Alternative Analysis Methods for Specialists (Under Waiver)**

**ACCEPTABLE for specialist agents:**

- Use structured analytical thinking approach
- Break down problems systematically using standard methods
- Document step-by-step reasoning process
- Apply logical problem-solving methodology

**Required Analysis Pattern for Specialists:**

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

---

## 📁 Tool 3: Filesystem - Efficient File Operations

### **Current Enforcement Status for Filesystem Tools**

- **SPECIALIST AGENTS**: ~~NOT REQUIRED~~ (Waived under current policy)
- **TECH LEAD ORCHESTRATOR**: **REQUIRED** (Full enforcement continues)

### **Filesystem Tool Purpose**

Provides comprehensive file system operations that are more efficient and reliable than terminal-based commands. Handles reading, writing, searching, and managing files and directories.

### **When to Use Filesystem Tools (Orchestrator Only)**

- ✅ Reading multiple files for orchestration analysis
- ✅ Searching for architectural patterns across codebase
- ✅ Getting comprehensive file/directory information
- ✅ Directory traversal for delegation planning
- ✅ Any orchestration-related file system operation

### **When NOT to Use Filesystem Tools**

- ❌ When you need git operations (use terminal/git tools)
- ❌ When you need to run executables
- ❌ For operations outside allowed directories
- ❌ **SPECIALIST AGENTS: Not required under current waiver policy**

### **Filesystem Operations & Syntax (Orchestrator Only)**

#### File Reading Operations

```javascript
// Read single file
mcp_filesystem_read_text_file
{
  "path": "/full/path/to/file.py",
  "head": 50,     // Optional: first N lines
  "tail": 50      // Optional: last N lines
}

// Read multiple files efficiently
mcp_filesystem_read_multiple_files  
{
  "paths": ["/path/file1.py", "/path/file2.py"]
}

// Get file metadata
mcp_filesystem_get_file_info
{
  "path": "/path/to/file.py"
}
```

### **Alternative File Operations for Specialists (Under Waiver)**

**ACCEPTABLE for specialist agents:**

- Use standard Claude Read tool for file operations
- Use standard Claude LS tool for directory listing
- Use standard Claude Write tool for file creation/updates
- Use standard Claude Edit tool for file modifications
- Use standard Claude Grep tool for searching within files

---

## 🔄 Updated Tool Integration Patterns

### **Pattern 1: Orchestrator Research → Delegate → Monitor**

```javascript
// 1. Research latest patterns (ORCHESTRATOR ONLY)
context7_resolve_library_id({"libraryName": "framework"})
context7_get_library_docs({...})

// 2. Plan delegation strategy (ORCHESTRATOR ONLY)
sequential_thinking({
  "thought": "Based on research, I need to delegate X to specialist Y using pattern Z..."
})

// 3. Delegate to specialists (SPECIALISTS USE STANDARD TOOLS)
// Specialists implement using Read, Write, Edit, LS, Grep, Bash
```

### **Pattern 2: Orchestrator Analysis → Multi-Agent Coordination**

```javascript
// 1. Break down the problem (ORCHESTRATOR ONLY)
sequential_thinking({
  "thought": "Complex task has multiple components: A, B, C. Need to coordinate specialists..."
})

// 2. Research current best practices (ORCHESTRATOR ONLY)
context7_get_library_docs({...})

// 3. Examine current codebase (ORCHESTRATOR ONLY)
filesystem_read_multiple_files({...})

// 4. Delegate coordinated tasks (SPECIALISTS USE STANDARD TOOLS)
// Each specialist uses their preferred standard Claude tools
```

---

## ✅ Updated Validation and Testing

### **Tool Call Validation Checklist**

**FOR ORCHESTRATOR (MCP tools still required):**

- [ ] **Context7**: Have you resolved the library ID first?
- [ ] **Sequential Thinking**: Is the orchestration complex enough to warrant step-by-step analysis?
- [ ] **Filesystem**: Are you using absolute paths from workspace root?
- [ ] **Evidence**: Can you provide specific evidence of MCP tool usage?

**FOR SPECIALISTS (Standard tools acceptable):**

- [ ] **Analysis**: Have you used systematic thinking approach?
- [ ] **Research**: Have you investigated project patterns and best practices?
- [ ] **Implementation**: Are you using the most efficient available tools?
- [ ] **Documentation**: Have you documented your approach and decisions?

### **Quality Indicators**

**Good orchestrator tool usage (MCP tools):**

- Specific, actionable MCP tool parameters
- Appropriate MCP tool selection for orchestration tasks
- Parallel MCP execution when possible
- Clear integration between MCP tools

**Good specialist implementation (Standard tools):**

- Systematic analysis using structured thinking
- Research through documentation and codebase review
- Efficient use of standard Claude tools
- Clear documentation of implementation decisions

---

## 📚 Updated Quick Reference

### **Context7 Quick Commands (Orchestrator Only)**

```bash
# Research React patterns (ORCHESTRATOR ONLY)
resolve-library-id("react") → get-library-docs("/facebook/react", "hooks")

# Research Python async patterns (ORCHESTRATOR ONLY)
resolve-library-id("asyncio") → get-library-docs("/python/asyncio", "coroutines")

# SPECIALISTS: Use documentation analysis and codebase review instead
```

### **Sequential Thinking Quick Commands (Orchestrator Only)**

```bash
# Start orchestration planning session (ORCHESTRATOR ONLY)
sequential-thinking("Planning delegation strategy for X feature...")

# Continue with delegation analysis (ORCHESTRATOR ONLY)
sequential-thinking("Based on research, technical approach should involve...")

# SPECIALISTS: Use structured analysis templates instead
```

### **Filesystem Quick Commands (Orchestrator Only)**

```bash
# Project overview for orchestration (ORCHESTRATOR ONLY)
directory_tree("/project/root")

# Multi-file read for delegation planning (ORCHESTRATOR ONLY)
read_multiple_files(["/path/file1", "/path/file2"])

# SPECIALISTS: Use standard Claude Read, LS, Write, Edit tools instead
```

---

## 🚨 UPDATED: Delegation-Specific Requirements

### **MCP Tool Requirements ONLY for @tech-lead-orchestrator**

**TECH LEAD ORCHESTRATOR MUST provide explicit evidence of MCP tool usage:**

1. **Sequential Thinking Evidence**:
   - Must show numbered thought progression from `mcp__sequential-thinking__sequentialthinking`
   - Include systematic problem breakdown and delegation analysis steps
   - Document orchestration decision-making process clearly

2. **Context7 Research Evidence** (when applicable):
   - Must show library ID resolution: `mcp__context7__resolve-library-id`
   - Must show documentation retrieval: `mcp__context7__get-library-docs`
   - Include specific research findings and delegation patterns discovered

3. **Filesystem Operations Evidence** (when applicable):
   - Must use `mcp__filesystem__*` tools for orchestration file operations
   - Include specific filesystem tool calls made
   - Document file operations performed for delegation planning

### **NO MCP Requirements for Specialist Agents (Under Waiver)**

**SPECIALIST AGENTS are NOT required to provide:**

- ~~MCP sequential thinking evidence~~
- ~~MCP context7 research evidence~~
- ~~MCP filesystem operations evidence~~

**SPECIALIST AGENTS MUST still provide:**

- ✅ Evidence of systematic analysis using structured thinking
- ✅ Evidence of research through documentation and codebase review
- ✅ Clear documentation of implementation approach and decisions
- ✅ Test scripts for bug fixes and validation procedures

### **Updated Role-Specific Requirements**

**@tech-lead-orchestrator MUST provide evidence of (UNCHANGED):**

```text
✅ mcp__sequential-thinking__sequentialthinking - Orchestration planning steps
✅ mcp__context7__resolve-library-id + get-library-docs - Delegation research  
✅ mcp__filesystem__* - Orchestration file operations evidence
```

**Specialist agents (@code-reviewer, @backend-developer, @frontend-developer, @documentation-specialist) MUST provide evidence of (UPDATED):**

```text
✅ Structured analysis using systematic thinking approach
✅ Research through documentation review and codebase analysis
✅ Implementation decisions documented with clear reasoning
✅ Test scripts and validation procedures for bug fixes
```

### **Updated Evidence Examples**

**✅ Good Orchestrator Evidence (MCP Required)**:

```text
I used mcp__sequential-thinking__sequentialthinking to break down this orchestration:
Thought 1: Analyzed the delegation requirements and team coordination needs...
Thought 2: Identified specialists needed and task dependencies...
Thought 3: Planned delegation sequence with risk mitigation...

I used mcp__context7__resolve-library-id to research delegation patterns...
```

**✅ Good Specialist Evidence (Standard Tools Acceptable)**:

```text
I performed systematic analysis of this implementation task:
Step 1: Analyzed current code structure using Read and LS tools...
Step 2: Researched best practices through documentation review...
Step 3: Planned implementation approach with comprehensive testing...
Step 4: Implemented using Write and Edit tools following project patterns...
```

## 🚨 Updated Enforcement Protocol

### **Tool Usage Violations**

**For @tech-lead-orchestrator (Full MCP Enforcement):**

1. **Not using MCP sequential-thinking** → Orchestration lacks systematic analysis
2. **Not using MCP context7 research** → Delegation may use outdated patterns
3. **Not using MCP filesystem tools** → Orchestration file operations inefficient

**For Specialist Agents (Under Waiver - No MCP Violations):**

1. **Not using systematic analysis** → Implementation lacks structure
2. **Not researching project patterns** → May use inconsistent approaches
3. **Poor documentation** → Implementation decisions not explained
4. **Missing test scripts** → Bug fixes not properly validated

### **Quality Standards (All Agents)**

All tool usage must meet these standards:

- **Purposeful**: Clear reason for approach selection
- **Efficient**: Use most appropriate tools available
- **Complete**: All required analysis and documentation provided
- **Integrated**: Tools work together toward the goal

---

**FINAL REMINDER**:

- **SPECIALIST AGENTS**: Currently operate under temporary MCP tool waiver - use standard Claude tools with high quality standards
- **TECH LEAD ORCHESTRATOR**: Remains fully subject to MCP tool enforcement with no waiver granted
- All quality standards and development protocols remain fully enforced for all agents
