# 🛠️ MCP Server Tool Usage Guide - Comprehensive Reference

> **Target Audience**: AI Coding Agents  
> **Purpose**: Definitive guide for mandatory MCP tool usage across all 26 validated agent specialists  
> **Last Updated**: 2025-08-31 (Universal MCP Tool Enforcement - Post Validation)

## 📋 Executive Summary

This guide provides comprehensive documentation for the three primary MCP (Model Context Protocol) tools available in our development environment. **IMPORTANT: Based on comprehensive validation testing of all 26 agent specialists, MCP tools are now MANDATORY for ALL agents - no exceptions or waivers remain in effect.**

## 🚨 UNIVERSAL MCP TOOL ENFORCEMENT POLICY (2025-08-31)

### **MANDATORY MCP TOOL USAGE FOR ALL AGENTS**

**ALL 26 VALIDATED AGENT SPECIALISTS:**

- ✅ **REQUIRED to use MCP tools** - Universal enforcement based on successful validation testing
- ✅ **Sequential thinking mandatory** - All agents must use mcp__sequential-thinking__sequentialthinking
- ✅ **Context7 research required** - All agents must use mcp__context7__resolve-library-id and mcp__context7__get-library-docs
- ✅ **Filesystem tools mandatory** - All agents must use mcp__filesystem__* tools
- ✅ **Enhanced architecture standards maintained** - All protocols remain fully enforced
- ✅ **Standard Claude tools deprecated** - Read, Write, Edit, LS, Grep, Bash no longer acceptable for MCP-capable tasks

**VALIDATION RESULTS:**

- ✅ **238+ successful tool calls** across all 26 specialists
- ✅ **100% success rate** in comprehensive MCP testing
- ✅ **All agents validated** with sequential-thinking, context7, and filesystem tools
- ✅ **Zero failures** in MCP tool usage validation testing

## 🔄 Critical Usage Requirements by Role (UNIVERSAL MCP ENFORCEMENT)

### **@code-reviewer** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic code review analysis
- ✅ **REQUIRED: context7 research** - For researching latest security patterns and best practices
- ✅ **REQUIRED: filesystem tools** - For efficient multi-file code review operations
- ✅ **ENHANCED**: Focus on JSON schema validation and FSM integrity
- ✅ **ENHANCED**: Validate enhanced architecture patterns and security

### **@frontend-developer** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic UI/UX development planning
- ✅ **REQUIRED: context7 research** - For researching latest Gradio and frontend patterns
- ✅ **REQUIRED: filesystem tools** - For efficient frontend file operations
- ✅ **ENHANCED**: Gradio-specific JSON textbox optimization
- ✅ **ENHANCED**: Real-time UI updates and enhanced data visualization

### **@backend-developer** - MCP TOOLS MANDATORY (PRIMARY ARCHITECT)

- ✅ **REQUIRED: sequential-thinking** - For systematic architecture and backend planning
- ✅ **REQUIRED: context7 research** - For researching latest Python/Pydantic AI patterns
- ✅ **REQUIRED: filesystem tools** - For efficient backend file operations
- ✅ **ENHANCED**: Primary architect for 5-state FSM and JSON systems
- ✅ **ENHANCED**: Maintain dual parser architecture (JSON + regex fallback)
- ✅ **ENHANCED**: Lead schema validation and performance optimization

### **@performance-optimizer** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic performance analysis and optimization planning
- ✅ **REQUIRED: context7 research** - For researching latest optimization patterns and techniques
- ✅ **REQUIRED: filesystem tools** - For efficient performance monitoring file operations
- ✅ **ENHANCED**: JSON parsing optimization and schema validation performance
- ✅ **ENHANCED**: Cost optimization and resource usage monitoring

### **@documentation-specialist** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic documentation planning and organization
- ✅ **REQUIRED: context7 research** - For researching latest documentation patterns and standards
- ✅ **REQUIRED: filesystem tools** - For efficient documentation file operations
- ✅ **ENHANCED**: JSON architecture guides and schema documentation
- ✅ **ENHANCED**: Migration procedures and system simplification guides

### **@api-architect** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic API design and architecture planning
- ✅ **REQUIRED: context7 research** - For researching latest API patterns and MCP integration
- ✅ **REQUIRED: filesystem tools** - For efficient API development file operations
- ✅ **ENHANCED**: JSON response schemas and MCP integration patterns
- ✅ **ENHANCED**: Ensure API design consistency with enhanced architecture

### **@code-archaeologist** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic deep architecture analysis
- ✅ **REQUIRED: context7 research** - For researching architectural patterns and technical debt solutions
- ✅ **REQUIRED: filesystem tools** - For efficient deep codebase analysis operations
- ✅ **ENHANCED**: Deep insight for major architectural changes when needed
- ✅ **ENHANCED**: Support for backend-developer on complex architecture decisions

### **@tech-lead-orchestrator** - MCP TOOLS MANDATORY (CONTINUED ENFORCEMENT)

- ✅ **REQUIRED: sequential-thinking** - For systematic orchestration analysis
- ✅ **REQUIRED: context7** - For research of orchestration patterns
- ✅ **REQUIRED: filesystem** - For orchestration file operations

---

## 🔧 Tool 1: Context7 - Latest Documentation Research

### **Current Enforcement Status**

- **ALL AGENTS**: **REQUIRED** (Universal enforcement based on successful validation)
- **NO EXCEPTIONS**: All 26 specialists must use Context7 for research tasks

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

### **Proper Tool Call Syntax (ALL AGENTS)**

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

### **Best Practices (ALL AGENTS)**

1. **Always resolve library ID first** - Don't guess the Context7 ID format
2. **Be specific with topics** - "async handling in gradio 4.0" vs just "gradio"
3. **Use appropriate token limits** - 5000-10000 for detailed research
4. **Document findings** - Save key patterns found for team reference

### **Common Mistakes to Avoid (ALL AGENTS)**

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

### **Supplementary Research Methods (ALL AGENTS)**

**IN ADDITION to mandatory MCP Context7 usage, agents may also:**

- Review existing project documentation and patterns
- Analyze current codebase implementation conventions
- Study framework usage examples in existing code
- Cross-reference MCP research with project-specific patterns
- **ENHANCED**: Focus on enhanced JSON architecture patterns
- **ENHANCED**: Study dual parser architecture and schema validation approaches

---

## 🧠 Tool 2: Sequential Thinking - Problem Decomposition

### **Current Enforcement Status for Sequential Thinking**

- **ALL AGENTS**: **REQUIRED** (Universal enforcement based on successful validation)
- **NO EXCEPTIONS**: All 26 specialists must use Sequential Thinking for complex analysis

### **Sequential Thinking Purpose**

Breaks down complex problems into manageable, step-by-step thought processes. Essential for planning, architecture decisions, and systematic problem-solving.

### **When to Use (Orchestrator Only)**

- ✅ Planning complex delegation strategies
- ✅ Orchestrating multi-component development tasks
- ✅ Strategic architecture and design decisions
- ✅ Complex team coordination analysis
- ✅ Before delegating any non-trivial development work

### **When NOT to Use**

- ❌ Simple, single-step tasks that don't require systematic breakdown
- ❌ Routine operations with obvious solutions
- ❌ Tasks with clear, predetermined approaches

### **Proper Tool Call Syntax (ALL AGENTS)**

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

### **Required Analysis Pattern for ALL AGENTS**

**When using Sequential Thinking, agents should follow this systematic approach:**

```markdown
## Sequential Thinking Analysis
### Thought 1: Understanding the Problem
- [Clear definition of what needs to be done]
- [Current state assessment]
- [Root cause identification]
- [Enhanced architecture impact assessment]

### Thought 2: Research and Context
- [Context7 research findings]
- [Relevant documentation patterns]
- [Best practices identified]
- [Enhanced JSON architecture considerations]

### Thought 3: Solution Planning
- [Step-by-step implementation approach]
- [Required resources and dependencies]
- [Risk assessment and mitigation]
- [Enhanced JSON architecture compliance]

### Thought 4: Implementation Strategy
- [Specific technical approaches]
- [Testing and validation plan]
- [Rollback considerations]
- [Coordination with primary architects]

### Thought 5: Success Validation
- [Measurable success criteria]
- [Testing procedures]
- [Quality verification steps]
- [Enhanced architecture standards verification]
```

---

## 📁 Tool 3: Filesystem - Efficient File Operations

### **Current Enforcement Status for Filesystem Tools**

- **ALL AGENTS**: **REQUIRED** (Universal enforcement based on successful validation)
- **NO EXCEPTIONS**: All 26 specialists must use MCP Filesystem tools

### **Filesystem Tool Purpose**

Provides comprehensive file system operations that are more efficient and reliable than terminal-based commands. Handles reading, writing, searching, and managing files and directories.

### **When to Use Filesystem Tools (ALL AGENTS)**

- ✅ Reading multiple files for orchestration analysis
- ✅ Searching for architectural patterns across codebase
- ✅ Getting comprehensive file/directory information
- ✅ Directory traversal for delegation planning
- ✅ Any orchestration-related file system operation

### **When NOT to Use Filesystem Tools**

- ❌ When you need git operations (use terminal/git tools)
- ❌ When you need to run executables
- ❌ For operations outside allowed directories

### **Filesystem Operations & Syntax (ALL AGENTS)**

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

### **Deprecated File Operations (NO LONGER ACCEPTABLE)**

**DEPRECATED - These tools are NO LONGER acceptable for MCP-capable tasks:**

- ~~Claude Read tool~~ - Use mcp__filesystem__read_text_file instead
- ~~Claude LS tool~~ - Use mcp__filesystem__list_directory instead
- ~~Claude Write tool~~ - Use mcp__filesystem__write_file instead
- ~~Claude Edit tool~~ - Use mcp__filesystem__edit_file instead
- ~~Claude Grep tool~~ - Use filesystem search or Context7 instead
- **ENHANCED**: All file operations must use MCP filesystem tools for consistency
- **ENHANCED**: Coordinate with primary architects for file structure decisions

---

## 🔄 Updated Tool Integration Patterns (Enhanced Architecture)

### **Pattern 1: Universal MCP Tool Usage**

```javascript
// 1. Research latest patterns (ALL AGENTS)
context7_resolve_library_id({"libraryName": "framework"})
context7_get_library_docs({...})

// 2. Plan implementation strategy (ALL AGENTS)
sequential_thinking({
  "thought": "Based on research, I need to implement enhanced JSON architecture work..."
})

// 3. Implement using MCP tools (ALL AGENTS)
// All agents implement using mcp__filesystem__* tools
// Focus on enhanced JSON architecture and coordination
```

### **Pattern 2: Systematic Analysis and Implementation**

```javascript
// 1. Break down the problem (ALL AGENTS)
sequential_thinking({
  "thought": "Complex enhanced architecture task has components: JSON schema, FSM, UI integration..."
})

// 2. Research current best practices (ALL AGENTS)
context7_get_library_docs({...})

// 3. Examine current codebase (ALL AGENTS)
filesystem_read_multiple_files({...})

// 4. Implement coordinated tasks (ALL AGENTS)
// Primary architect (backend-developer) leads with secondary agent support
// All agents use MCP tools for consistency and efficiency
```

---

## ✅ Updated Validation and Testing (Enhanced Architecture)

### **Tool Call Validation Checklist**

**FOR ALL AGENTS (MCP tools mandatory):**

- [ ] **Context7**: Have you resolved the library ID first?
- [ ] **Sequential Thinking**: Is the task complex enough to warrant step-by-step analysis?
- [ ] **Filesystem**: Are you using absolute paths from workspace root?
- [ ] **Evidence**: Can you provide specific evidence of MCP tool usage?
- [ ] **Enhanced Architecture**: Are you considering enhanced JSON architecture coordination?
- [ ] **Research**: Have you investigated latest patterns and best practices?
- [ ] **Implementation**: Are you using MCP tools for all file operations?
- [ ] **Documentation**: Have you documented your approach and decisions?
- [ ] **Coordination**: Are you properly coordinating with primary architects?

### **Quality Indicators**

**Good MCP tool usage (ALL AGENTS):**

- Specific, actionable MCP tool parameters
- Appropriate MCP tool selection for task requirements
- Parallel MCP execution when possible
- Clear integration between MCP tools
- **Enhanced**: Consideration of enhanced JSON architecture coordination
- Systematic analysis using Sequential Thinking
- Research through Context7 for latest patterns
- Efficient use of MCP Filesystem tools
- Clear documentation of implementation decisions
- **Enhanced**: Following enhanced JSON architecture patterns
- **Enhanced**: Proper coordination with primary architects

---

## 📚 Updated Quick Reference (Enhanced Architecture)

### **Context7 Quick Commands (ALL AGENTS)**

```bash
# Research React patterns (ALL AGENTS)
resolve-library-id("react") → get-library-docs("/facebook/react", "hooks")

# Research Python async patterns (ALL AGENTS)
resolve-library-id("asyncio") → get-library-docs("/python/asyncio", "coroutines")

# Research JSON schema patterns (ALL AGENTS)
resolve-library-id("jsonschema") → get-library-docs("/python-jsonschema/jsonschema", "validation")

# Research Gradio patterns (ALL AGENTS)
resolve-library-id("gradio") → get-library-docs("/gradio-app/gradio", "interface")
```

### **Sequential Thinking Quick Commands (ALL AGENTS)**

```bash
# Start systematic analysis session (ALL AGENTS)
sequential-thinking("Planning implementation strategy for enhanced JSON architecture...")

# Continue with detailed planning (ALL AGENTS)
sequential-thinking("Need to coordinate with backend-developer as primary architect...")

# Problem decomposition (ALL AGENTS)
sequential-thinking("Breaking down complex task into manageable components...")
```

### **Filesystem Quick Commands (ALL AGENTS)**

```bash
# Project overview (ALL AGENTS)
directory_tree("/project/root")

# Multi-file read for analysis (ALL AGENTS)
read_multiple_files(["/src/json_parser.py", "/src/json_schemas.py"])

# Efficient file operations (ALL AGENTS)
read_text_file("/path/to/file.py")
write_file("/path/to/new_file.py", "content")
edit_file("/path/to/file.py", [{"oldText": "...", "newText": "..."}])
```

---

## 🚨 UNIVERSAL MCP TOOL REQUIREMENTS (Enhanced Architecture)

### **MCP Tool Requirements for ALL AGENTS**

**ALL 26 VALIDATED AGENTS MUST provide explicit evidence of MCP tool usage:**

1. **Sequential Thinking Evidence**:
   - Must show numbered thought progression from `mcp__sequential-thinking__sequentialthinking`
   - Include systematic problem breakdown and analysis steps
   - Document decision-making process clearly
   - **Enhanced**: Consider enhanced JSON architecture coordination

2. **Context7 Research Evidence** (when applicable):
   - Must show library ID resolution: `mcp__context7__resolve-library-id`
   - Must show documentation retrieval: `mcp__context7__get-library-docs`
   - Include specific research findings and patterns discovered
   - **Enhanced**: Research enhanced JSON architecture patterns

3. **Filesystem Operations Evidence** (when applicable):
   - Must use `mcp__filesystem__*` tools for all file operations
   - Include specific filesystem tool calls made
   - Document file operations performed for implementation
   - **Enhanced**: Focus on enhanced JSON architecture file analysis

### **UNIVERSAL MCP REQUIREMENTS (No Exceptions)**

**ALL SPECIALIST AGENTS MUST provide:**

- ✅ **MCP sequential thinking evidence** - Mandatory for complex tasks
- ✅ **MCP context7 research evidence** - Mandatory for research tasks
- ✅ **MCP filesystem operations evidence** - Mandatory for file operations
- ✅ Clear documentation of implementation approach and decisions
- ✅ Test scripts for bug fixes and validation procedures
- ✅ **Enhanced**: Evidence of enhanced JSON architecture compliance
- ✅ **Enhanced**: Proper coordination with primary architects

### **Universal Role Requirements (Enhanced Architecture)**

**ALL AGENTS (@tech-lead-orchestrator, @code-reviewer, @backend-developer, @frontend-developer, @documentation-specialist, @performance-optimizer, @api-architect, @code-archaeologist) MUST provide evidence of:**

```text
✅ mcp__sequential-thinking__sequentialthinking - Systematic analysis steps
✅ mcp__context7__resolve-library-id + get-library-docs - Research evidence  
✅ mcp__filesystem__* - File operations evidence
✅ Implementation decisions documented with clear reasoning
✅ Test scripts and validation procedures for bug fixes
✅ Enhanced: Evidence of enhanced JSON architecture compliance
✅ Enhanced: Proper coordination with primary architects (especially backend-developer)
```

### **Updated Evidence Examples (Enhanced Architecture)**

**✅ Good MCP Tool Usage Evidence (ALL AGENTS)**:

```text
I used mcp__sequential-thinking__sequentialthinking to break down this enhanced architecture task:
Thought 1: Analyzed the requirements and enhanced JSON architecture coordination needs...
Thought 2: Researched latest patterns using Context7 for relevant libraries...
Thought 3: Planned implementation approach focusing on enhanced architecture integrity...
Thought 4: Coordinated with backend-developer as primary architect...
Thought 5: Validated approach against enhanced architecture standards...

I used mcp__context7__resolve-library-id to research enhanced JSON schema patterns...
I used mcp__filesystem__read_multiple_files to analyze current codebase structure...
```

**❌ Unacceptable Evidence (Deprecated Approach)**:

```text
I performed systematic analysis of this task:
Step 1: Analyzed current structure using Read and LS tools... (DEPRECATED)
Step 2: Researched best practices through documentation review... (INSUFFICIENT - must use Context7)
Step 3: Implemented using Write and Edit tools... (DEPRECATED - must use MCP filesystem)
```

## 🚨 Updated Enforcement Protocol (Enhanced Architecture)

### **Tool Usage Violations**

**For ALL AGENTS (Universal MCP Enforcement):**

1. **Not using MCP sequential-thinking** → Task lacks systematic analysis
2. **Not using MCP context7 research** → Implementation may use outdated patterns
3. **Not using MCP filesystem tools** → File operations inefficient and inconsistent
4. **Using deprecated Claude tools** → Non-compliance with MCP standards
5. **Enhanced**: Not considering enhanced JSON architecture coordination
6. **Enhanced**: Not following enhanced JSON architecture patterns
7. **Enhanced**: Not coordinating with primary architects

### **Quality Standards (All Agents - Universal MCP Enforcement)**

All tool usage must meet these standards:

- **Purposeful**: Clear reason for approach selection
- **Efficient**: Use most appropriate tools available
- **Complete**: All required analysis and documentation provided
- **Integrated**: Tools work together toward the goal
- **Enhanced**: Compliance with enhanced JSON architecture standards
- **Coordinated**: Proper coordination with primary architects

---

**FINAL REMINDER**:

- **ALL 26 AGENTS**: Must use MCP tools for all applicable tasks - no exceptions or waivers remain in effect
- **UNIVERSAL ENFORCEMENT**: Based on successful validation testing of all agent specialists
- **DEPRECATED TOOLS**: Standard Claude tools (Read, Write, Edit, LS, Grep, Bash) are no longer acceptable for MCP-capable tasks
- **VALIDATION PROVEN**: 238+ successful tool calls demonstrate all agents can effectively use MCP tools
- All enhanced JSON architecture quality standards and development protocols remain fully enforced for all agents