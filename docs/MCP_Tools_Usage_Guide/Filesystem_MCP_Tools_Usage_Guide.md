# Filesystem MCP Tools Usage Guide for Market Parser AI Agents

**Target Audience:** AI Coding Agents working on Market Parser project  
**Purpose:** Proper MCP filesystem tool usage vs standard Claude Code tools  
**Project Context:** Python FastAPI backend + React/Vite frontend with prototyping focus

## Quick Decision Matrix

| Operation Type | Use MCP Tools | Use Standard Tools |
|---|---|---|
| Single file read/write in current context | ❌ | ✅ Read, Write, Edit |
| Multiple file operations | ✅ `read_multiple_files` | ❌ |
| Directory exploration/analysis | ✅ `directory_tree`, `list_directory` | ❌ |
| File metadata/info gathering | ✅ `get_file_info`, `list_directory_with_sizes` | ❌ |
| Bulk search across directories | ✅ `search_files` | ❌ |
| Path verification before operations | ✅ `list_directory` | ❌ |
| Cross-directory file operations | ✅ `move_file` | ❌ |
| Quick single file edits | ❌ | ✅ Edit, MultiEdit |
| Pattern-based file finding | ❌ | ✅ Glob, Grep |
| Size analysis and disk usage | ✅ `list_directory_with_sizes` | ❌ |

## Project Context: Market Parser

**Allowed Directory:** `/home/1000211866/Github/market-parser-polygon-mcp` (all MCP operations restricted to this path)  
**Key Directories:** `src/backend/` (Python), `src/frontend/` (React), `docs/`, `tests/`  
**Configuration Files:** `.env`, `package.json`, `pyproject.toml`, `vite.config.ts`

## MCP Filesystem Tools - Market Parser Specific Usage

### `mcp__filesystem__read_text_file`

**Correct Usage:**
- Reading configuration files: `.env`, `package.json`, `pyproject.toml`
- Single file content analysis when path is known
- Reading files outside current working directory

**Correct Examples:**

```bash
# Read backend configuration
mcp__filesystem__read_text_file("/home/1000211866/Github/market-parser-polygon-mcp/src/backend/main.py")

# Read project config
mcp__filesystem__read_text_file("/home/1000211866/Github/market-parser-polygon-mcp/package.json")
```

**Incorrect Usage:**
- Reading files you plan to immediately edit (use Edit tool instead)
- Reading multiple related files (use `read_multiple_files`)

**Incorrect Examples:**

```bash
# DON'T: Reading file just to edit it
mcp__filesystem__read_text_file → Edit
# INSTEAD: Use Read tool then Edit tool

# DON'T: Reading multiple files one by one
mcp__filesystem__read_text_file(file1)
mcp__filesystem__read_text_file(file2)
# INSTEAD: Use read_multiple_files
```

### `mcp__filesystem__read_multiple_files`

**Correct Usage:**
- Analyzing related backend files: `main.py`, `api_models.py`, `prompt_templates.py`
- Comparing frontend components across directories
- Batch configuration file analysis

**Correct Examples:**

```json
# Analyze backend API structure
mcp__filesystem__read_multiple_files({
  "paths": [
    "/home/1000211866/Github/market-parser-polygon-mcp/src/backend/main.py",
    "/home/1000211866/Github/market-parser-polygon-mcp/src/backend/api_models.py",
    "/home/1000211866/Github/market-parser-polygon-mcp/src/backend/prompt_templates.py"
  ]
})

# Compare frontend configurations
mcp__filesystem__read_multiple_files({
  "paths": [
    "/home/1000211866/Github/market-parser-polygon-mcp/package.json",
    "/home/1000211866/Github/market-parser-polygon-mcp/vite.config.ts",
    "/home/1000211866/Github/market-parser-polygon-mcp/tsconfig.json"
  ]
})
```

**Incorrect Usage:**
- Reading files in sequence for editing (use standard tools)
- Reading large numbers of files (>10) without specific purpose

### `mcp__filesystem__list_directory`

**Correct Usage:**
- Exploring project structure before operations
- Verifying directory contents before file operations
- Understanding component organization in frontend/backend

**Correct Examples:**

```bash
# Explore backend structure
mcp__filesystem__list_directory("/home/1000211866/Github/market-parser-polygon-mcp/src/backend")

# Check documentation organization
mcp__filesystem__list_directory("/home/1000211866/Github/market-parser-polygon-mcp/docs")

# Verify test structure (includes: e2e, playwright, unit, integration, mcp subdirs)
mcp__filesystem__list_directory("/home/1000211866/Github/market-parser-polygon-mcp/tests")

# Explore specific test type
mcp__filesystem__list_directory("/home/1000211866/Github/market-parser-polygon-mcp/tests/playwright")
```

**Incorrect Usage:**
- Listing current working directory (use `ls` bash command)
- Checking single file existence (use standard Read tool)

### `mcp__filesystem__directory_tree`

**Correct Usage:**
- Initial project analysis for new AI agents
- Understanding complex nested structures
- Architecture documentation creation

**Correct Examples:**

```bash
# Analyze docs structure for navigation
mcp__filesystem__directory_tree("/home/1000211866/Github/market-parser-polygon-mcp/docs")

# Understand test organization (reveals e2e, playwright, unit, integration, mcp structure)
mcp__filesystem__directory_tree("/home/1000211866/Github/market-parser-polygon-mcp/tests")

# Focus on specific test directory
mcp__filesystem__directory_tree("/home/1000211866/Github/market-parser-polygon-mcp/tests/playwright")
```

**Incorrect Usage:**
- Exploring entire project root (too much data)
- Regular file operations (use `list_directory`)

**Expected Output:**
```json
{
  "name": "docs",
  "type": "directory",
  "children": [
    {
      "name": "MCP_Tools_Usage_Guide", 
      "type": "directory",
      "children": [...]
    }
  ]
}
```

### `mcp__filesystem__search_files`

**Correct Usage:**
- Finding specific file types across project: "*.py", "*.ts", "*.md"
- Locating configuration files when path unknown
- Finding test files matching patterns

**Correct Examples:**

```bash
# Find all Python API files
mcp__filesystem__search_files("/home/1000211866/Github/market-parser-polygon-mcp/src", "api")

# Locate all configuration files
mcp__filesystem__search_files("/home/1000211866/Github/market-parser-polygon-mcp", "config")

# Find test files
mcp__filesystem__search_files("/home/1000211866/Github/market-parser-polygon-mcp/tests", "test")
```

**Incorrect Usage:**
- Searching for code content (use Grep tool)
- Finding files in current directory (use Glob tool)

**Expected Output:**

```json
[
  "/home/1000211866/Github/market-parser-polygon-mcp/src/backend/api_models.py",
  "/home/1000211866/Github/market-parser-polygon-mcp/src/frontend/services/api_OpenAI.ts",
  "/home/1000211866/Github/market-parser-polygon-mcp/src/frontend/hooks/usePromptAPI.ts"
]
```

### `mcp__filesystem__get_file_info`

**Correct Usage:**
- Checking file modification times for build processes
- Verifying file sizes before operations
- Debugging file permission issues

**Correct Examples:**

```bash
# Check if config was recently modified
mcp__filesystem__get_file_info("/home/1000211866/Github/market-parser-polygon-mcp/.env")

# Verify large log file size (Note: logs directory may not exist initially)
mcp__filesystem__get_file_info("/home/1000211866/Github/market-parser-polygon-mcp/logs/debug.log")

# Check if logs directory exists before accessing log files
mcp__filesystem__list_directory("/home/1000211866/Github/market-parser-polygon-mcp/logs")
```

**Expected Output:**
```json
{
  "size": 15030,
  "created": "Sat Sep 13 2025 20:38:27 GMT-0700 (Pacific Daylight Time)",
  "modified": "Sat Sep 13 2025 20:38:27 GMT-0700 (Pacific Daylight Time)",
  "accessed": "Sun Sep 14 2025 21:23:21 GMT-0700 (Pacific Daylight Time)",
  "isDirectory": false,
  "isFile": true,
  "permissions": 644
}
```

### `mcp__filesystem__write_file`

**Correct Usage:**
- Creating new documentation files
- Writing configuration files
- Creating new component files from scratch

**Correct Examples:**

```json
# Create new API documentation
mcp__filesystem__write_file({
  "path": "/home/1000211866/Github/market-parser-polygon-mcp/docs/api/new_endpoint.md",
  "content": "# New Endpoint Documentation..."
})

# Create new React component (following existing naming pattern)
mcp__filesystem__write_file({
  "path": "/home/1000211866/Github/market-parser-polygon-mcp/src/frontend/components/NewAnalysisWidget.tsx",
  "content": "import React from 'react'...\n// Similar to ChatInput_OpenAI.tsx, ChatMessage_OpenAI.tsx patterns"
})
```

**Incorrect Usage:**
- Overwriting existing files without reading first (use Edit tool)
- Making small changes to existing files (use Edit tool)

### `mcp__filesystem__edit_file`

**Correct Usage:**
- Multiple targeted changes in single file
- Search-and-replace operations across file
- Batch modifications with known patterns

**Correct Examples:**

```json
# Update API endpoints in multiple locations
mcp__filesystem__edit_file({
  "path": "/home/1000211866/Github/market-parser-polygon-mcp/src/backend/main.py",
  "edits": [
    {"oldText": "http://localhost:8000", "newText": "http://127.0.0.1:8000"},
    {"oldText": "old_function_name", "newText": "new_function_name"}
  ]
})
```

**Incorrect Usage:**
- Single small changes (use standard Edit tool)
- Changes requiring context analysis (use Read + Edit)

### `mcp__filesystem__create_directory`

**Correct Usage:**
- Creating new feature directories
- Setting up new documentation sections
- Creating test directory structures

**Correct Examples:**

```bash
# Create new feature directory
mcp__filesystem__create_directory("/home/1000211866/Github/market-parser-polygon-mcp/src/backend/features/new_feature")

# Create documentation section
mcp__filesystem__create_directory("/home/1000211866/Github/market-parser-polygon-mcp/docs/new_section")
```

### `mcp__filesystem__move_file`

**Correct Usage:**
- Reorganizing project structure
- Moving files between feature directories
- Renaming files with path changes

**Correct Examples:**

```json
# Reorganize backend structure
mcp__filesystem__move_file({
  "source": "/home/1000211866/Github/market-parser-polygon-mcp/src/old_location.py",
  "destination": "/home/1000211866/Github/market-parser-polygon-mcp/src/backend/new_location.py"
})
```

### `mcp__filesystem__list_directory_with_sizes`

**Correct Usage:**
- Analyzing disk usage in project directories
- Identifying large files before operations
- Monitoring build output sizes

**Correct Examples:**

```bash
# Check build output sizes
mcp__filesystem__list_directory_with_sizes("/home/1000211866/Github/market-parser-polygon-mcp/dist")

# Analyze log file sizes (Note: logs directory may need to be created first)
mcp__filesystem__list_directory_with_sizes("/home/1000211866/Github/market-parser-polygon-mcp/logs")
```

**Expected Output:**

```text
[DIR] components (2.1 KB)
[FILE] main.js (156.3 KB)
[FILE] style.css (45.2 KB)
```

## Market Parser Project Patterns

### Backend Development Workflows

**Analyzing API Structure:**
1. `mcp__filesystem__list_directory("/home/1000211866/Github/market-parser-polygon-mcp/src/backend")`
2. `mcp__filesystem__read_multiple_files()` with paths array for main.py, api_models.py, etc.
3. Use standard Edit tools for modifications

**Adding New Features:**
1. `mcp__filesystem__create_directory("/home/1000211866/Github/market-parser-polygon-mcp/src/backend/features/new_feature")`
2. `mcp__filesystem__write_file()` for new component files
3. `mcp__filesystem__edit_file()` for configuration updates

### Frontend Development Workflows

**Component Analysis:**
1. `mcp__filesystem__search_files("/home/1000211866/Github/market-parser-polygon-mcp/src/frontend", "component")`
2. `mcp__filesystem__read_multiple_files()` with paths for ChatInput_OpenAI.tsx, ChatInterface_OpenAI.tsx, etc.
3. Use standard tools for individual edits

**Configuration Management:**
1. `mcp__filesystem__read_multiple_files()` with paths for package.json, vite.config.ts, tsconfig.json
2. Use standard Edit tools for specific changes

### Documentation Workflows

**Structure Analysis:**
1. `mcp__filesystem__directory_tree("/home/1000211866/Github/market-parser-polygon-mcp/docs")`
2. `mcp__filesystem__list_directory()` for specific sections
3. `mcp__filesystem__write_file()` for new documentation

## Common Anti-Patterns to Avoid

### ❌ Don't Use MCP Tools For:
- Single file edits in current working directory
- Quick configuration changes
- Sequential single-file operations
- Code content searching (use Grep)
- Pattern-based file finding (use Glob)

### ❌ Don't Use Standard Tools For:
- Bulk file operations
- Directory structure analysis
- Cross-directory file movements
- File metadata gathering
- Path verification before operations

## Error Handling Patterns

**MCP Tool Errors:**

```bash
# Path errors indicate directory doesn't exist
# Use mcp__filesystem__create_directory first

# Permission errors indicate path restrictions
# Use mcp__filesystem__list_allowed_directories to check
```

**Recovery Strategies:**
1. Path not found → Use `search_files` to locate
2. Permission denied → Check `list_allowed_directories`
3. File too large → Use standard Read tool with limit parameters

## Performance Considerations

**MCP Tools are Better For:**
- Operations requiring path validation
- Bulk operations (>3 files)
- Cross-directory workflows
- Metadata-dependent operations

**Standard Tools are Better For:**
- Single file operations
- Content-based searches
- Quick edits in current context
- Pattern matching operations

## Additional MCP Tools Coverage

### Tools Not Covered (Use with Caution)
- `mcp__filesystem__read_file` - Deprecated, use `read_text_file`
- `mcp__filesystem__read_media_file` - For images/binary files only

### Allowed Directory Verification

```bash
# Always check allowed directories when MCP tools fail
mcp__filesystem__list_allowed_directories()
# Returns: ["/home/1000211866/Github/market-parser-polygon-mcp"]
```

## Summary

This guide ensures AI agents use the most appropriate tools for Market Parser development workflows while maintaining efficiency and avoiding common mistakes. All MCP filesystem operations are restricted to the project directory for security.