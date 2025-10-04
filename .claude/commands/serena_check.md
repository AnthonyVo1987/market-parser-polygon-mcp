---
name: serena_check
description: Comprehensive Serena system health check to verify all tools and configurations are working correctly after IDE restart
category: development
---

# Serena System Health Check

You are performing a comprehensive health check of the Serena system to verify all tools and configurations are working correctly after an IDE restart. This command will systematically test all Serena tool categories and provide a detailed health summary.

## 🎯 **HEALTH CHECK OBJECTIVES**

- ✅ Verify project activation and configuration
- ✅ Check onboarding completion status  
- ✅ Validate language server status (clangd)
- ✅ Test all Serena tool categories systematically
- ✅ Verify memory system functionality
- ✅ Generate comprehensive health report
- ✅ Store results in project memory

## 🔍 **HEALTH CHECK PROCEDURE**

### **STEP 1: Initial System Status Check**

First, get the tool instructions and  current Serena configuration and project status:
use docs-serena tools to understand proper usage of Serena

1. **Get Serena Documentation & Initial Instuctions**
   - First, Use docs-serena tools to retreive and understand Serena tools
   - Second, use Serena `initial_instructions` tool to understand how to use Serena tools

2. **Get Current Configuration**
   - Use `get_current_config` to verify Serena version, active project, context, and modes
   - Check available tools count and status
   - Verify project path and language detection

3. **Check Project Activation**
   - Verify the current project is properly activated
   - Confirm project path matches expected location
   - Check if project appears in available projects list

### **STEP 2: Project Onboarding Verification**

1. **Check Onboarding Status**
   - Use `check_onboarding_performed` to verify onboarding completion
   - Confirm available memories count
   - Verify project-specific configuration exists

2. **Memory System Test**
   - Use `list_memories` to verify memory system access
   - Check memory count and accessibility
   - Verify memory names are properly listed

### **STEP 3: Language Server Status Check**

1. **Check Language Server Processes**
   - Use terminal command to check for running clangd processes
   - Verify both Cursor's and Serena's clangd instances are running
   - Check for any language server errors or warnings

2. **Language Server Configuration**
   - Verify .clangd configuration file exists and is properly configured
   - Check compile_commands.json is present and valid
   - Confirm include paths and compiler flags are set correctly

### **STEP 4: Serena Tool Category Testing**

Test each category of Serena tools systematically:

#### **4.1 Project Management Tools**

- `activate_project` - Test project activation capability
- `get_current_config` - Verify configuration retrieval
- `check_onboarding_performed` - Test onboarding status check

#### **4.2 File Operations Tools**

- `list_dir` - Test directory listing (use project root)
- `find_file` - Test file discovery (search for *.cpp files)
- `search_for_pattern` - Test pattern search (search for "main" function)

#### **4.3 Code Analysis Tools**

- `get_symbols_overview` - Test symbol analysis (use ArmMhost.cpp)
- `find_symbol` - Test symbol discovery (find "main" function)
- `find_referencing_symbols` - Test reference finding (if applicable)

#### **4.4 Memory Management Tools**

- `list_memories` - Test memory listing
- `read_memory` - Test memory reading (read a known memory)
- `write_memory` - Test memory writing (create health check memory)

#### **4.5 Thinking Tools**

- `think_about_collected_information` - Test information analysis
- `think_about_task_adherence` - Test task adherence checking

#### **4.6 Mode Management Tools**

- `switch_modes` - Test mode switching capability

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
   - Measure response times for key operations
   - Check for any timeout or performance issues
   - Verify tool execution reliability

2. **Error Handling**
   - Test error handling for invalid inputs
   - Verify graceful degradation on failures
   - Check error message clarity and usefulness

## 📊 **HEALTH REPORT GENERATION**

Create a comprehensive health summary with the following sections and do NOT CREATE ANY NEW DOCS OR MEMORIES:

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
   - Solution: Use `activate_project` with project name or path
   - Command: "Activate the project CCB"

2. **Language Server Issues**
   - Check clangd processes: `ps aux | grep clangd`
   - Verify .clangd configuration
   - Check compile_commands.json

3. **Memory System Issues**
   - Verify .serena directory exists
   - Check memory file permissions
   - Confirm project onboarding completion

4. **Tool Availability Issues**
   - Check project configuration in .serena/project.yml
   - Verify context and mode settings
   - Review tool restrictions

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

**Begin the Serena System Health Check now.**
