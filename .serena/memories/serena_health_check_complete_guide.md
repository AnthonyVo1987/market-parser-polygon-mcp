# Serena System Health Check - Complete Guide & Backup

**Date:** October 6, 2025  
**Purpose:** Comprehensive Serena system health check guide and backup memory  
**Source:** .cursor/commands/serena_check.md  
**Status:** VERBATIM BACKUP - Complete guide for proper Serena tool usage and health checks

---

## 🎯 **HEALTH CHECK OBJECTIVES**

- ✅ Verify project activation and configuration
- ✅ Check onboarding completion status  
- ✅ Validate language server status (language-specific)
- ✅ Test all Serena tool categories systematically
- ✅ Verify memory system functionality
- ✅ Generate comprehensive health report

## 🔍 **HEALTH CHECK PROCEDURE**

### ⚠️ **CRITICAL: PROPER SERENA TOOL USAGE**

**Before proceeding with any health check, understand these fundamental requirements:**

### **📋 Tool Usage Rules**

1. **READ BEFORE ANALYZE:** Always use `mcp_serena_read_file` before any code analysis tools
2. **USE CORRECT FILE TYPES:** Code analysis tools only work on source code files matching the project's language
3. **AVOID NON-SOURCE FILES:** Never use code analysis on .txt, .md, .yml, .json, .xml, .csv, or other non-source files
4. **FOLLOW TOOL SEQUENCE:** Find files → Read files → Analyze files (in that order)
5. **DETECT PROJECT LANGUAGE:** Use `mcp_serena_get_current_config` to determine the project's language and select appropriate file extensions

### **🌐 Language-Specific File Extensions**

**Use these file patterns based on the project's configured language:**

#### **C/C++ Projects (cpp)**

- Source files: `*.c`, `*.cpp`, `*.cc`, `*.cxx`, `*.c++`
- Header files: `*.h`, `*.hpp`, `*.hxx`, `*.h++`
- **Pattern for testing:** `*.cpp` or `*.c`

#### **Python Projects (python)**

- Source files: `*.py`, `*.pyw`
- **Pattern for testing:** `*.py`

#### **TypeScript Projects (typescript)**

- Source files: `*.ts`, `*.tsx`
- **Pattern for testing:** `*.ts`

#### **JavaScript Projects (javascript)**

- Source files: `*.js`, `*.jsx`, `*.mjs`
- **Pattern for testing:** `*.js`

### **🔧 Tool-Specific Requirements**

#### **File Operations Tools**

- `list_dir` - Works on any directory
- `find_file` - Works with file patterns (e.g., "*.cpp", "*.py", "*.ts", "*.js")
- `read_file` - Works on any readable file
- `search_for_pattern` - Works on any text file

#### **Code Analysis Tools (REQUIRE READ_FILE FIRST)**

- `get_symbols_overview` - ONLY on source code files matching project language
- `find_symbol` - ONLY on source code files matching project language
- `find_referencing_symbols` - ONLY on source code files matching project language

#### **Memory Management Tools**

- `write_memory` - Creates new memories
- `read_memory` - Reads existing memories
- `delete_memory` - Deletes memories
- `list_memories` - Lists all memories

### **❌ COMMON MISTAKES TO AVOID**

- Using code analysis on build files (CMakeLists.txt, Makefile, package.json, etc.)
- Using code analysis on documentation files (.txt, .md, .rst, etc.)
- Using code analysis on configuration files (.yml, .json, .xml, .ini, etc.)
- Attempting analysis without reading files first
- Using wrong file types for specific tool categories
- Not detecting project language before selecting file patterns

### **STEP 1: Initial System Status Check**

First, get the tool instructions and current Serena configuration and project status:

1. **Get Serena Documentation & Initial Instructions**
   - **Primary Method (Preferred)**: Use `mcp__serena__initial_instructions` tool to understand how to use Serena tools
   - **Fallback Method**: If tool fails, use `mcp__serena__read_memory` with memory name: `serena_initial_instructions`

2. **Get Current Configuration**
   - Use `mcp_serena_get_current_config` to verify Serena version, active project, context, and modes
   - Check available tools count and status
   - Verify project path and language detection

3. **Check Project Activation**
   - Verify the current project is properly activated
   - Confirm project path matches expected location
   - Check if project appears in available projects list

### **STEP 2: Project Onboarding Verification**

1. **Check Onboarding Status**
   - Use `mcp_serena_check_onboarding_performed` to verify onboarding completion
   - Confirm available memories count
   - Verify project-specific configuration exists

2. **Memory System Test**
   - Use `mcp_serena_list_memories` to verify memory system access
   - Check memory count and accessibility
   - Verify memory names are properly listed

### **STEP 3: Language Server Status Check**

1. **Check Language Server Processes**
   - Use terminal command to check for running language server processes
   - **C/C++:** Check for `clangd` processes
   - **Python:** Check for `pylsp` or `pyright` processes
   - **TypeScript/JavaScript:** Check for `typescript-language-server` or `tsserver` processes
   - Verify both Cursor's and Serena's language server instances are running
   - Check for any language server errors or warnings

2. **Language Server Configuration**
   - **C/C++:** Verify .clangd configuration file and compile_commands.json
   - **Python:** Check for pyproject.toml, setup.cfg, or requirements.txt
   - **TypeScript/JavaScript:** Check for tsconfig.json or jsconfig.json
   - Confirm language-specific configuration files are present and valid

3. **Language Server Restart Test**
   - Use `mcp_serena_restart_language_server` to test restart capability
   - Verify language server recovers properly after restart
   - Check for any errors during restart process

### **STEP 4: Serena Tool Category Testing**

Test each category of Serena tools systematically:

#### **4.1 Project Management Tools**

- `mcp_serena_activate_project` - Test project activation capability
- `mcp_serena_get_current_config` - Verify configuration retrieval
- `mcp_serena_check_onboarding_performed` - Test onboarding status check

#### **4.2 File Operations Tools**

- `mcp_serena_list_dir` - Test directory listing (use project root)
- `mcp_serena_find_file` - Test file discovery (search for language-specific source files)
- `mcp_serena_search_for_pattern` - Test pattern search (search for common function patterns)
- `mcp_serena_read_file` - Test file reading (read a source file for analysis)

**Language-Specific Testing:**

- **C/C++:** Search for `*.cpp` files, look for "main" function
- **Python:** Search for `*.py` files, look for "def main" or "if \_\_name\_\_"
- **TypeScript/JavaScript:** Search for `*.ts`/`*.js` files, look for "function" or "const"

#### **4.3 Code Analysis Tools**

#### **🔴 CRITICAL: PROPER TOOL USAGE REQUIREMENTS**

- **MUST READ FILES FIRST:** All code analysis tools require files to be read using `mcp_serena_read_file` before analysis
- **USE APPROPRIATE SOURCE FILES:** Only use actual source code files matching the project's language, NOT build files or configuration files
- **FILE SELECTION:** Use `mcp_serena_find_file` to locate appropriate source files first, then read them before analysis
- **DETECT LANGUAGE FIRST:** Always check project language before selecting file patterns

#### **Testing Steps (MANDATORY SEQUENCE)**

1. **Detect Project Language:** Use `mcp_serena_get_current_config` to determine the project's language
2. **Find Source Files:** Use `mcp_serena_find_file` with language-specific pattern (e.g., "*.cpp", "*.py", "*.ts")
3. **Select Appropriate File:** Choose a source file with actual code (not empty or minimal)
   - **Note:** If no source files are found, check the project structure and language configuration
4. **Read Source File:** Use `mcp_serena_read_file` to read the selected source file completely
5. **Test Analysis Tools (in order):**

   - `mcp_serena_get_symbols_overview` - Test symbol analysis (use the read source file)
   - `mcp_serena_find_symbol` - Test symbol discovery (find functions/classes in the read source file)
   - `mcp_serena_find_referencing_symbols` - Test reference finding (if applicable)

#### **Language-Specific Examples**

**C/C++ Project:**

```text
1. mcp_serena_get_current_config() → language: "cpp"
2. mcp_serena_find_file("*.cpp", ".") → Returns list of .cpp files
3. mcp_serena_read_file("src/main.cpp") → Reads the file
4. mcp_serena_get_symbols_overview("src/main.cpp") → Analyzes symbols
5. mcp_serena_find_symbol("main", "src/main.cpp") → Finds main function
```

**Python Project:**

```text
1. mcp_serena_get_current_config() → language: "python"
2. mcp_serena_find_file("*.py", ".") → Returns list of .py files
3. mcp_serena_read_file("main.py") → Reads the file
4. mcp_serena_get_symbols_overview("main.py") → Analyzes symbols
5. mcp_serena_find_symbol("main", "main.py") → Finds main function
```

**TypeScript Project:**

```text
1. mcp_serena_get_current_config() → language: "typescript"
2. mcp_serena_find_file("*.ts", ".") → Returns list of .ts files
3. mcp_serena_read_file("src/index.ts") → Reads the file
4. mcp_serena_get_symbols_overview("src/index.ts") → Analyzes symbols
5. mcp_serena_find_symbol("main", "src/index.ts") → Finds main function
```

#### **❌ CODE ANALYSIS MISTAKES TO AVOID**

- Using code analysis tools on build files (CMakeLists.txt, Makefile, package.json, etc.)
- Using code analysis tools on documentation files (.txt, .md, .rst, .doc, etc.)
- Using code analysis tools on configuration files (.yml, .json, .xml, .ini, .cfg, etc.)
- Using code analysis tools on data files (.csv, .dat, .log, etc.)
- Attempting analysis without first reading the file
- Using non-source files for code analysis
- Not detecting project language before selecting file patterns
- Using wrong file extensions for the project's language

#### **4.4 Memory Management Tools**

- `mcp_serena_list_memories` - Test memory listing
- `mcp_serena_read_memory` - Test memory reading (read a known memory)
- `mcp_serena_write_memory` - Test memory writing (create health check memory)
- `mcp_serena_delete_memory` - Test memory deletion (clean up test memory)

#### **4.5 Thinking Tools**

- `mcp_serena_think_about_collected_information` - Test information analysis
- `mcp_serena_think_about_task_adherence` - Test task adherence checking
- `mcp_serena_think_about_whether_you_are_done` - Test completion assessment

#### **4.6 Mode Management Tools**

- `mcp_serena_switch_modes` - Test mode switching capability

### **STEP 5: Configuration Validation**

1. **Project Configuration**
   - Verify .serena/project.yml exists and is properly configured
   - Check project-specific settings and tool restrictions
   - Confirm context and mode settings

2. **Global Configuration**
   - Check serena_config.yml for global settings
   - Verify language server configurations
   - Confirm tool availability and restrictions

### **STEP 6: Performance and Stability Check**

1. **Response Time Testing**
   - Time key operations using system clock or stopwatch
   - Test: `mcp_serena_get_current_config` (should complete in <2 seconds)
   - Test: `mcp_serena_find_file` with simple pattern (should complete in <5 seconds)
   - Test: `mcp_serena_read_file` on small file (should complete in <1 second)
   - Check for any timeout or performance issues
   - Verify tool execution reliability

2. **Error Handling**
   - Test with invalid file paths: `mcp_serena_read_file("nonexistent.txt")`
   - Test with invalid patterns: `mcp_serena_find_file("*.invalid", ".")`
   - Test with non-source files: `mcp_serena_get_symbols_overview("README.md")`
   - Verify graceful degradation on failures
   - Check error message clarity and usefulness

## 📊 **HEALTH REPORT GENERATION**

Create a comprehensive health summary with the following sections and do NOT CREATE ANY NEW DOCS OR MEMORIES:

### 🔴 CRITICAL: DO NOT CREATE OR UPDATE ANY MEMORIES OR NEW FILES/DOCS FOR THE comprehensive summary: JUST RESPOND WITH THE SUMMARY ONLY AND DO NOT WASTE TOKENS BY CREATING NEW FILES/MEMORIES

### **System Status Summary**

- Overall health status (✅ HEALTHY / ⚠️ WARNINGS / ❌ ISSUES)
- Serena version and configuration
- Active project and context information
- Available tools count and status

### **Component Status**

- Project Activation: ✅/❌
- Onboarding Status: ✅/❌  
- Language Servers: ✅/❌
- Memory System: ✅/❌
- Tool Categories: ✅/❌ (with details for each)

### **Performance Metrics**

- Response times for key operations
- Tool execution success rates
- Memory system performance
- Language server responsiveness

### **Issues and Recommendations**

- List any identified issues
- Provide specific troubleshooting steps
- Suggest configuration improvements
- Recommend next actions

## 🛡️ **SAFETY CONSIDERATIONS**

- **DO NOT** interrupt ongoing indexing processes
- **DO NOT** restart language servers unless absolutely necessary
- **DO NOT** modify critical configuration files
- **USE** read-only operations where possible
- **CONTINUE** testing other components if one fails
- **PRESERVE** existing project state and settings

## 🔧 **TROUBLESHOOTING GUIDANCE**

If issues are found, provide specific guidance:

### **Common Issues and Solutions**

1. **Project Not Activated**
   - Solution: Use `mcp_serena_activate_project` with project name or path
   - Command: "Activate the project CCB"

2. **Language Server Issues**
   - **C/C++:** Check clangd processes: `ps aux | grep clangd`
   - **Python:** Check pylsp/pyright processes: `ps aux | grep -E "(pylsp|pyright)"`
   - **TypeScript/JavaScript:** Check tsserver processes: `ps aux | grep tsserver`
   - Verify language-specific configuration files
   - Check for language server errors in logs

3. **Memory System Issues**
   - Verify .serena directory exists
   - Check memory file permissions
   - Confirm project onboarding completion

4. **Tool Availability Issues**
   - Check project configuration in .serena/project.yml
   - Verify context and mode settings
   - Review tool restrictions

5. **Code Analysis Tool Errors**

   - **Error: "File read failed"** → Solution: Use `mcp_serena_read_file` first before analysis
   - **Error: "invalid AST"** → Solution: Use source code files matching project language, not build files
   - **Error: "No symbols found"** → Solution: Ensure file is read and is actual source code
   - **Error: "File not found"** → Solution: Use `mcp_serena_find_file` to locate correct files first

6. **File Type Mismatch Errors**

   - **Using build files for code analysis** → Solution: Use language-specific source files
   - **Using documentation files for analysis** → Solution: Use actual source code files
   - **Using configuration files for analysis** → Solution: Use source code files only
   - **Using wrong file extensions** → Solution: Match file extensions to project language
   - **Not detecting project language first** → Solution: Always use `mcp_serena_get_current_config` first

## 🎯 **SUCCESS CRITERIA**

The health check is successful when:

- ✅ All tool categories pass their tests
- ✅ Language servers are running properly
- ✅ Memory system is fully functional
- ✅ Project is properly activated and onboarded
- ✅ Configuration is valid and complete
- ✅ Performance is within acceptable ranges

## 📋 **EXECUTION INSTRUCTIONS**

1. **Start the health check** by following the procedure above
2. **Test each component systematically** using the specified tools
3. **Record results** for each test with clear pass/fail indicators
4. **Generate comprehensive summary** with all findings
5. **Provide actionable recommendations** for any issues found
6. **🔴 CRITICAL: DO NOT CREATE OR UPDATE ANY MEMORIES OR NEW FILES/DOCS FOR THE comprehensive summary**

**Begin the Serena System Health Check now.**

---

## 🔄 **USAGE INSTRUCTIONS**

### **Primary Method: Custom Command**

- Use `/serena_check` command from .cursor/commands/serena_check.md
- This is the primary method for running health checks

### **Backup Method: Memory Reference**

- If the custom command is unavailable, reference this memory
- Use `mcp_serena_read_memory` with memory name: `serena_health_check_complete_guide_2025_01_23`
- Follow the procedures outlined in this memory

### **Key Benefits of This Memory**

1. **Complete Backup:** Verbatim copy of the custom command
2. **Tool Usage Guide:** Comprehensive guide for proper Serena tool usage
3. **Language-Agnostic:** Works with C/C++, Python, TypeScript, JavaScript projects
4. **Troubleshooting:** Detailed solutions for common issues
5. **Fallback Option:** Available when custom commands are not accessible

### **Memory Maintenance**

- This memory should be updated whenever the .cursor/commands/serena_check.md file is modified
- Keep this memory synchronized with the primary command file
- Use this memory as a reference for proper Serena tool usage patterns

---

**Memory Created:** January 23, 2025  
**Status:** ✅ ACTIVE - Ready for use as backup and guide  
**Last Updated:** January 23, 2025  
**Source:** .cursor/commands/serena_check.md (VERBATIM)
