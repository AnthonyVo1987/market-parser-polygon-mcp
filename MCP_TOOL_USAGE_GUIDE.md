# 🛠️ MCP Server Tool Usage Guide - Comprehensive Reference

> **Target Audience**: AI Coding Agents  
> **Purpose**: Definitive guide for proper MCP tool usage, syntax, and best practices  
> **Last Updated**: Current Session

## 📋 Executive Summary

This guide provides comprehensive documentation for the three primary MCP (Model Context Protocol) tools available in our development environment. Proper usage of these tools is **MANDATORY** for specific AI specialist roles and development scenarios.

## 🚨 Critical Usage Requirements by Role

### **@code-reviewer** - MUST use:
- ✅ `sequential-thinking` - For systematic code analysis
- ✅ `context7` - For latest framework/library best practices

### **@frontend-developer** - MUST use:
- ✅ `sequential-thinking` - For planning UI/UX implementations
- ✅ `context7` - For researching latest frontend framework patterns
- ✅ `filesystem` - For efficient file operations

### **@backend-developer** - MUST use:
- ✅ `sequential-thinking` - For architecture planning
- ✅ `context7` - For latest backend framework patterns  
- ✅ `filesystem` - For efficient file operations

### **@documentation-specialist** - MUST use:
- ✅ `sequential-thinking` - For structuring documentation
- ✅ `filesystem` - For file operations

---

## 🔧 Tool 1: Context7 - Latest Documentation Research

### **Purpose**
Context7 provides access to the most up-to-date documentation, best practices, and code examples for any library or framework. It's your primary tool for researching current development patterns.

### **When to Use**
- ✅ Researching latest framework versions (React 18+, Vue 3+, Gradio 4+, etc.)
- ✅ Finding current API syntax and best practices
- ✅ Getting code examples for modern patterns
- ✅ Understanding breaking changes between versions
- ✅ Before implementing any frontend/backend features

### **When NOT to Use**
- ❌ For general programming concepts (use standard knowledge)
- ❌ For project-specific code (use filesystem tools)
- ❌ For debugging existing code (use other analysis tools)

### **Proper Tool Call Syntax**

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

### **Best Practices**

1. **Always resolve library ID first** - Don't guess the Context7 ID format
2. **Be specific with topics** - "async handling in gradio 4.0" vs just "gradio"
3. **Use appropriate token limits** - 5000-10000 for detailed research
4. **Document findings** - Save key patterns found for team reference

### **Common Mistakes to Avoid**

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

### **Example Usage Scenarios**

**Scenario 1: Frontend Framework Research**
```javascript
// Research modern React patterns
resolve-library-id: {"libraryName": "react"}
get-library-docs: {
  "context7CompatibleLibraryID": "/facebook/react", 
  "topic": "hooks and concurrent features",
  "tokens": 8000
}
```

**Scenario 2: Backend Framework Research** 
```javascript
// Research FastAPI async patterns
resolve-library-id: {"libraryName": "fastapi"}
get-library-docs: {
  "context7CompatibleLibraryID": "/tiangolo/fastapi",
  "topic": "async dependency injection",
  "tokens": 6000
}
```

---

## 🧠 Tool 2: Sequential Thinking - Problem Decomposition

### **Purpose**
Breaks down complex problems into manageable, step-by-step thought processes. Essential for planning, architecture decisions, and systematic problem-solving.

### **When to Use**
- ✅ Planning complex feature implementations
- ✅ Debugging multi-component issues
- ✅ Architecture and design decisions
- ✅ Code review analysis
- ✅ Before starting any non-trivial development task

### **When NOT to Use**
- ❌ Simple, single-step tasks
- ❌ Routine operations (file editing, simple fixes)
- ❌ When immediate action is more appropriate

### **Proper Tool Call Syntax**

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

### **Best Practices**

1. **Start with clear problem statement** - Define what you're trying to solve
2. **Estimate total thoughts** - Can be adjusted as you progress
3. **Use revisions when needed** - Mark thoughts that change previous analysis
4. **Branch for alternatives** - Explore different approaches
5. **Be specific in each thought** - Each step should add clear value

### **Common Mistakes to Avoid**

❌ **Wrong**: Vague, non-actionable thoughts
```javascript
"thought": "I need to fix this somehow"  // Too vague
```

✅ **Correct**: Specific, actionable thoughts
```javascript
"thought": "I need to identify the root cause of the async handler failure by examining the lambda wrapper pattern in lines 685-700 of chat_ui.py and comparing it to modern Gradio 4.0+ async patterns"
```

### **Example Usage Scenarios**

**Scenario 1: Feature Planning**
```javascript
// Thought 1: Problem analysis
{
  "thought": "Planning implementation of real-time stock data feature. Need to identify: 1) data source integration, 2) WebSocket handling, 3) UI update patterns, 4) error handling strategies",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 4
}

// Thought 2: Technical approach
{
  "thought": "For data source integration, I'll use Polygon.io WebSocket API. Need to research latest WebSocket patterns in Python and determine if we need asyncio or threading approach",
  "nextThoughtNeeded": true, 
  "thoughtNumber": 2,
  "totalThoughts": 4
}
```

**Scenario 2: Bug Analysis**
```javascript
// Thought 1: Symptom identification
{
  "thought": "Button click handlers are failing silently. Symptoms: no errors in console, no function execution, UI remains responsive. This suggests event binding issues rather than function logic problems",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1, 
  "totalThoughts": 3
}
```

---

## 📁 Tool 3: Filesystem - Efficient File Operations

### **Purpose**
Provides comprehensive file system operations that are more efficient and reliable than terminal-based commands. Handles reading, writing, searching, and managing files and directories.

### **When to Use**
- ✅ Reading file contents (single or multiple files)
- ✅ Writing or editing files
- ✅ Searching for files or patterns within files
- ✅ Getting file/directory information
- ✅ Directory traversal and listing
- ✅ Any file system operation

### **When NOT to Use**
- ❌ When you need git operations (use terminal/git tools)
- ❌ When you need to run executables
- ❌ For operations outside allowed directories

### **Available Operations & Syntax**

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

#### File Writing/Editing Operations
```javascript
// Write new file or overwrite existing
mcp_filesystem_write_file
{
  "path": "/path/to/new/file.py",
  "content": "file contents here"
}

// Edit existing file with line-based replacements
mcp_filesystem_edit_file
{
  "path": "/path/to/file.py", 
  "edits": [
    {
      "oldText": "exact text to replace",
      "newText": "replacement text"
    }
  ],
  "dryRun": false  // Optional: preview changes
}
```

#### Directory Operations
```javascript
// List directory contents
mcp_filesystem_list_directory
{
  "path": "/path/to/directory"
}

// Get directory structure as JSON tree
mcp_filesystem_directory_tree
{
  "path": "/path/to/directory"
}

// Create directory
mcp_filesystem_create_directory
{
  "path": "/path/to/new/directory"
}
```

#### Search Operations
```javascript
// Search for files by name pattern
mcp_filesystem_search_files
{
  "path": "/search/root/directory",
  "pattern": "*.py",
  "excludePatterns": ["__pycache__", "*.pyc"]
}
```

### **Best Practices**

1. **Use absolute paths** - More reliable than relative paths
2. **Read multiple files in parallel** - Use read_multiple_files for efficiency
3. **Use directory_tree for structure overview** - Better than list_directory for nested exploration
4. **Preview edits with dryRun** - Validate changes before applying
5. **Batch edit operations** - Group related file changes together

### **Common Mistakes to Avoid**

❌ **Wrong**: Using relative paths inconsistently
```javascript
"path": "./src/components/Button.tsx"  // May fail
```

✅ **Correct**: Use absolute paths from workspace root
```javascript
"path": "/mnt/d/Github/project/src/components/Button.tsx"
```

❌ **Wrong**: Reading files sequentially when could be parallel
```javascript
// Don't do this
read_text_file({"path": "/path/file1.py"})
// Wait for result
read_text_file({"path": "/path/file2.py"})
// Wait for result  
```

✅ **Correct**: Read multiple files in parallel
```javascript
read_multiple_files({
  "paths": ["/path/file1.py", "/path/file2.py", "/path/file3.py"]
})
```

### **Example Usage Scenarios**

**Scenario 1: Code Analysis**
```javascript
// Get project structure overview
directory_tree({"path": "/mnt/d/Github/project"})

// Read key files for analysis
read_multiple_files({
  "paths": [
    "/mnt/d/Github/project/src/main.py",
    "/mnt/d/Github/project/config/settings.py", 
    "/mnt/d/Github/project/requirements.txt"
  ]
})
```

**Scenario 2: Bug Fix Implementation**
```javascript
// Read current problematic file
read_text_file({"path": "/mnt/d/Github/project/chat_ui.py"})

// Edit with specific fixes
edit_file({
  "path": "/mnt/d/Github/project/chat_ui.py",
  "edits": [
    {
      "oldText": "lambda: async_function_call()",
      "newText": "async_function_call"
    }
  ]
})
```

---

## 🔄 Tool Integration Patterns

### **Pattern 1: Research → Plan → Implement**
```javascript
// 1. Research latest patterns
context7_resolve_library_id({"libraryName": "framework"})
context7_get_library_docs({...})

// 2. Plan implementation  
sequential_thinking({
  "thought": "Based on research, I need to implement X using pattern Y..."
})

// 3. Implement changes
filesystem_edit_file({...})
```

### **Pattern 2: Problem Analysis → Solution Planning**
```javascript
// 1. Break down the problem
sequential_thinking({
  "thought": "Complex bug has multiple symptoms: A, B, C. Need to identify root cause..."
})

// 2. Research current best practices
context7_get_library_docs({...})

// 3. Examine current code
filesystem_read_multiple_files({...})

// 4. Continue planning with new information
sequential_thinking({
  "thought": "After research and code review, root cause appears to be..."
})
```

---

## ✅ Validation and Testing

### **Tool Call Validation Checklist**

Before using any MCP tool, verify:

- [ ] **Context7**: Have you resolved the library ID first?
- [ ] **Sequential Thinking**: Is the problem complex enough to warrant step-by-step analysis?
- [ ] **Filesystem**: Are you using absolute paths from workspace root?
- [ ] **Role Requirements**: Does your specialist role mandate specific tool usage?

### **Quality Indicators**

**Good tool usage:**
- Specific, actionable parameters
- Appropriate tool selection for the task
- Parallel execution when possible
- Clear integration between tools

**Poor tool usage:**
- Vague or missing parameters
- Wrong tool for the task
- Sequential execution when parallel would work
- Isolated tool usage without integration

---

## 📚 Quick Reference

### **Context7 Quick Commands**
```bash
# Research React patterns
resolve-library-id("react") → get-library-docs("/facebook/react", "hooks")

# Research Python async patterns  
resolve-library-id("asyncio") → get-library-docs("/python/asyncio", "coroutines")
```

### **Sequential Thinking Quick Commands**
```bash
# Start planning session
sequential-thinking("Planning X feature implementation...")

# Continue with analysis
sequential-thinking("Based on research, technical approach should be...")
```

### **Filesystem Quick Commands**
```bash
# Project overview
directory_tree("/project/root")

# Multi-file read
read_multiple_files(["/path/file1", "/path/file2"])

# Safe edit with preview
edit_file("/path/file", edits=[...], dryRun=true)
```

---

## 🚨 Enforcement Protocol

### **Mandatory Tool Usage Violations**

If a specialist agent fails to use required tools:

1. **@code-reviewer** not using sequential-thinking or context7 → Review is incomplete
2. **@frontend-developer** not researching latest patterns → Implementation may use outdated practices  
3. **@backend-developer** not using systematic planning → Architecture may be flawed

### **Tool Misuse Corrections**

Common corrections needed:
- Wrong Context7 library ID format → Always resolve first
- Vague sequential thinking → Be specific and actionable
- Relative filesystem paths → Use absolute paths
- Sequential tool calls → Use parallel when possible

### **Quality Standards**

All tool usage must meet these standards:
- **Purposeful**: Clear reason for tool selection
- **Efficient**: Parallel execution when appropriate
- **Complete**: All required parameters provided
- **Integrated**: Tools work together toward the goal

---

*This guide is the definitive reference for MCP tool usage. All AI coding agents must follow these patterns and requirements.*