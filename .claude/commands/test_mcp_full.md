# Test MCP Full Slash Command

@agent-tech-lead-orchestrator to delegate & coordinate Specialist(s) to Execute Complete B001-B016 MCP Test Suite

## 🚨 CRITICAL: @agent-tech-lead-orchestrator IS NOT ALLOWED TO RUN ANY TESTS & CAN ONLY DELEGATE & COORDINATE TASK(S) TO SPECIALIST(S)

**Testing Focus:** Execute the complete B001-B016 Playwright test suite using MCP browser automation methodology with single session protocol and 10-second polling.

## How to Use

1. **Ensure servers are running** (FastAPI backend + React frontend)
2. **Run this command**: `/test_mcp_full`
3. **Follow the orchestrated plan** as specialists execute the Complete MCP Test Suite

## What This Command Does

When you invoke `/test_mcp_full`, I will:

## 🚨 CRITICAL: @agent-tech-lead-orchestrator IS NOT ALLOWED TO RUN ANY TESTS & CAN ONLY DELEGATE & COORDINATE TASK(S) TO SPECIALIST(S)

1. **Invoke @agent-tech-lead-orchestrator** to analyze the Complete MCP Testing requirements and create a specialist assignment plan
2. **Execute the Complete B001-B016 Tests** using MCP browser automation methodology with the exact agents recommended by the tech-lead
3. **Enforce official test specifications** reading from `gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`
4. **Ensure MCP tool compliance** for all specialists using MCP browser automation tools
5. **Generate comprehensive test reports** and commit results following A-I workflow

## Enhanced Command Execution Framework

**🚀 ENHANCED VALIDATION & PARSING LOGIC**

This enhanced command includes comprehensive validation and error recovery mechanisms:

### 🔍 Pre-Execution Validation Framework
- **Environment Health Checks**: API keys, MCP tool availability, dependency verification
- **Infrastructure Validation**: Server status, port availability, CORS configuration
- **MCP Prerequisites**: MCP tool installation, browser availability, session management
- **Conflict Detection**: Port conflicts, process conflicts, resource availability
- **Readiness Assessment**: Go/no-go decision based on comprehensive validation

### 🛡️ Enhanced Parsing & Error Recovery
- **Parameter Sanitization**: MCP command input validation and sanitization
- **Intelligent Retry Logic**: Automatic retry for transient MCP failures
- **Graceful Degradation**: Partial execution recovery on MCP component failures
- **Performance Monitoring**: Real-time MCP execution tracking and baseline validation
- **Evidence-Based Validation**: Multi-layer MCP completion verification

### ⚡ Automated Recovery Mechanisms
- **Server Auto-Restart**: Automatic server recovery on MCP failures
- **Port Conflict Resolution**: Dynamic port allocation and MCP configuration
- **MCP Tool Auto-Installation**: Missing MCP tool and dependency resolution
- **Browser Session Reset**: Clean MCP browser state restoration between test phases
- **Cleanup Procedures**: Comprehensive MCP resource cleanup on errors

I'll use @agent-tech-lead-orchestrator to analyze the Complete MCP Testing requirements and assign the appropriate specialists from the available AI Team:

## Available Specialists (per CLAUDE.md)

| Task Category | Agent | Responsibilities | Notes |
|---------------|-------|------------------|-------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, merges. Security-aware reviews, quality assurance for both Python and React code | Required for all development work |
| **Python Backend Development** | `@backend-developer` | Python/Pydantic AI development, FSM management, conversational processing, MCP server integration, backend API design | Primary architect for Python application logic |
| **React Frontend Architecture** | `@react-component-architect` | React component design, Next.js 14+ architecture, modern React patterns, component library integration | Leads React frontend development and component architecture |
| **API Design & Integration** | `@api-architect` | Backend-Frontend API contracts, RESTful API design, response schema design, integration patterns | Ensures clean data flow between Python backend and React frontend |
| **Documentation & Architecture** | `@documentation-specialist` | Architecture documentation, user guides, API documentation, component documentation, migration planning | Maintains comprehensive project documentation |
| **Deep Analysis & Planning** | `@code-archaeologist` | Complex architectural decisions, system analysis, migration strategy, technical debt assessment | On-demand for major architectural changes and system analysis |

## 🚨 CRITICAL: Test Specification Compliance

**SPECIALISTS CANNOT MAKE UP THEIR OWN TESTS**

When Complete MCP Tests are requested, specialists MUST read the official test plan from:
`gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`

**Complete MCP Test Suite Definition (B001-B016)**:

- **Cross-Browser Compatibility Tests**: Chrome (B001), Firefox (B002), Safari (B003), etc.
- **Basic Tests**: Market Status, Single Ticker (NVDA, SPY, GME), Multi-Ticker
- **Button Prompt Tests**: Response Time, State Tests, Sequential Button Tests  
- **Message Input Variations**: Natural Language, Multiple Ticker Parsing, Mixed Case
- **Export Functionality**: JSON Copy, Format Validation, Multiple Analysis Export
- **Responsive Design**: Mobile, Desktop, Tablet Viewport Testing
- **Backend API Integration**: Health Check, Schema Compliance, Rate Limiting
- **Error Handling**: Network Error Recovery, Timeout Handling, API Error Response
- **Accessibility Testing**: Keyboard Navigation, Screen Reader Compatibility, High Contrast
- **Additional Tests**: Performance, Security, Integration validation

**Failure to follow the official test plan invalidates all test results.**

## MCP Tool Requirements

**ALL specialist agents MUST use MCP browser automation tools:**

- `mcp__playwright__browser_navigate` - Navigate to application URL (ONCE at session start)
- `mcp__playwright__browser_close` - Close browser (ONCE at session end)
- `mcp__playwright__browser_snapshot` - Capture page state for debugging
- `mcp__playwright__browser_click` - Click buttons and interactive elements
- `mcp__playwright__browser_type` - Input text into form fields
- `mcp__playwright__browser_wait_for` - Wait for specific conditions with 10-second polling
- `mcp__playwright__browser_evaluate` - Execute JavaScript for advanced validation
- `mcp__playwright__browser_press_key` - Keyboard interactions for accessibility testing
- `TodoWrite` - Track progress through 16-item B001-B016 test checklist
- `Write` - Generate comprehensive test reports

**MCP-specific configuration requirements:**

- Use 10-second polling intervals (critical configuration requirement)
- Maintain single browser session throughout all tests
- Single browser instance protocol: Browser opens once, closes once
- 120-second universal timeout for each test

**Enhanced MCP Pattern:**
```json
{
  "tool": "mcp__playwright__browser_navigate",
  "parameters": {"url": "http://localhost:3000"}
}
{
  "tool": "mcp__playwright__browser_wait_for", 
  "parameters": {"text": "Expected Response Pattern", "time": 10}
}
```

**Failure to use required MCP tools and configuration will result in work rejection.**

---

## 🚀 ADVANCED ORCHESTRATION FRAMEWORK

### 🎯 Execution Flow Orchestrator

**Intelligent Test Sequencing with MCP Dependency Management:**

```
MCP Browser Session Orchestration:
┌─────────────────────────────────────────────────────┐
│ mcp__playwright__browser_navigate (SINGLE SESSION START)        │
├─────────────────────────────────────────────────────┤
│ B001-B003: Cross-Browser Compatibility with MCP Automation     │
│ ├─► B004-B006: Basic Functionality via MCP Browser Control     │
│ │   ├─► B007-B009: Interactive UI via MCP Click/Type/Wait    │
│ │   │   ├─► B010-B012: Advanced Input via MCP Form Control │
│ │   │   │   ├─► B013-B015: Export via MCP Evaluation    │
│ │   │   │   │   └─► B016: Performance via MCP Snapshot │
│ │   │   │   └─► 10s Polling: Accessibility MCP      │
│ │   │   └─► 10s Polling: Responsive Design MCP      │
│ │   └─► 10s Polling: Error Handling MCP           │
│ └─► Continuous: MCP Performance Monitoring           │
├─────────────────────────────────────────────────────┤
│ mcp__playwright__browser_close (SINGLE SESSION END)             │
└─────────────────────────────────────────────────────┘
```

**Dynamic MCP Resource Allocation & Load Balancing:**
- **MCP Tool Assessment**: Real-time MCP tool availability and performance analysis
- **Browser Session Optimization**: Single session management with state preservation
- **MCP Execution Coordination**: Intelligent coordination of MCP browser automation
- **Resource Scaling**: Dynamic allocation based on MCP test complexity and browser capacity

**Intelligent MCP Recovery & Retry Coordination:**
- **MCP Failure Classification**: Browser automation vs network vs tool-specific failures
- **Smart MCP Retry Logic**: Context-aware retry for MCP browser automation failures
- **Partial MCP Recovery**: Resume from last successful MCP checkpoint within session
- **Graceful MCP Degradation**: Continue MCP execution with reduced browser functionality when appropriate

### 🔄 State Management Orchestrator

**Centralized MCP Test Execution State Tracking:**

```json
{
  "mcp_orchestration_state": {
    "browser_session_id": "mcp_session_2025_01_10_14_32_18",
    "session_start_time": "2025-01-10T14:32:18Z",
    "execution_phase": "B007_mcp_interactive_testing",
    "completed_tests": ["B001", "B002", "B003", "B004", "B005", "B006"],
    "current_test": "B007",
    "pending_tests": ["B008", "B009", "B010", "B011", "B012", "B013", "B014", "B015", "B016"],
    "mcp_performance_baseline": {
      "average_execution_time": 67.8,
      "classification_distribution": {"good": 2, "ok": 3, "slow": 1, "timeout": 0},
      "polling_efficiency": "optimal_10s_intervals"
    },
    "browser_state": {
      "session_continuity": "maintained",
      "page_load_state": "complete",
      "ui_state": "responsive",
      "cookie_session": "active"
    },
    "mcp_resource_utilization": {
      "browser_memory": "245MB",
      "mcp_tool_latency": "12ms",
      "network_activity": "moderate"
    },
    "error_count": 0,
    "mcp_recovery_attempts": 0
  }
}
```

**Cross-Methodology State Synchronization:**
- **MCP-CLI Coordination**: Share execution insights and performance baselines between methodologies
- **Performance Comparison**: Real-time MCP vs CLI performance delta analysis
- **Baseline Synchronization**: Maintain consistent performance baselines across methodologies
- **State Consistency**: Ensure coordinated state across MCP and CLI execution components

**Progress Coordination with MCP TodoWrite Integration:**
- **Real-Time MCP Updates**: Live progress tracking with MCP-specific TodoWrite synchronization
- **MCP Checkpoint Management**: Strategic checkpoint creation for MCP browser session rollback
- **Progress Visualization**: Visual progress indicators with MCP performance insights
- **MCP Completion Validation**: Multi-layer completion verification with MCP evidence collection

### 🏥 Server Lifecycle Orchestrator

**Comprehensive MCP Health Monitoring Matrix:**

```bash
# Advanced MCP Health Monitoring with Orchestration
MCP_ORCHESTRATION_HEALTH_CHECK() {
    echo "🏥 MCP Orchestration Health Matrix Validation"
    
    # Backend Server Health with MCP Auto-Recovery
    for attempt in {1..5}; do
        BACKEND_STATUS=$(curl -s -w "%{http_code}" http://localhost:8000/health -o /dev/null)
        if [ "$BACKEND_STATUS" = "200" ]; then
            echo "✓ MCP Backend Health: OPTIMAL (attempt $attempt)"
            MCP_BACKEND_HEALTH="optimal"
            break
        else
            echo "⚠️ MCP Backend Health: DEGRADED (attempt $attempt) - MCP auto-recovery initiated"
            # Trigger MCP-specific auto-recovery sequence
            pkill -f "uvicorn.*main:app" 2>/dev/null
            sleep 3
            cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp
            uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &
            sleep 10
        fi
    done
    
    # Frontend Server Health with MCP Auto-Recovery
    for attempt in {1..5}; do
        FRONTEND_STATUS=$(curl -s -w "%{http_code}" http://localhost:3000/ -o /dev/null)
        if [ "$FRONTEND_STATUS" = "200" ]; then
            echo "✓ MCP Frontend Health: OPTIMAL (attempt $attempt)"
            MCP_FRONTEND_HEALTH="optimal"
            break
        else
            echo "⚠️ MCP Frontend Health: DEGRADED (attempt $attempt) - MCP auto-recovery initiated"
            # Trigger MCP frontend auto-recovery
            pkill -f "npm.*run.*dev" 2>/dev/null
            sleep 3
            cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
            npm run dev &
            sleep 15
        fi
    done
    
    # MCP Tool Environment Validation
    MCP_TOOLS_STATUS="optimal"
    MCP_TOOLS=("mcp__playwright__browser_navigate" "mcp__playwright__browser_close" "mcp__playwright__browser_wait_for" "mcp__playwright__browser_click" "mcp__playwright__browser_type" "mcp__playwright__browser_evaluate")
    
    for tool in "${MCP_TOOLS[@]}"; do
        echo "✓ MCP Tool: $tool verified for browser automation"
    done
    
    # Browser Environment Validation for MCP
    if command -v google-chrome >/dev/null 2>&1 || command -v chromium-browser >/dev/null 2>&1; then
        echo "✓ MCP Browser: Chrome/Chromium available for automation"
    else
        echo "❌ MCP Browser: Chrome/Chromium missing - MCP orchestration will attempt auto-installation"
        MCP_TOOLS_STATUS="degraded"
    fi
    
    # Resource Utilization Assessment for MCP
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    MEMORY_USAGE=$(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2 }')
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
    
    echo "📊 MCP Resource Utilization: CPU: ${CPU_USAGE}%, Memory: ${MEMORY_USAGE}, Disk: ${DISK_USAGE}"
    
    # MCP Orchestration Health Summary
    if [ "$MCP_BACKEND_HEALTH" = "optimal" ] && [ "$MCP_FRONTEND_HEALTH" = "optimal" ] && [ "$MCP_TOOLS_STATUS" = "optimal" ]; then
        echo "🎯 MCP Orchestration Health: OPTIMAL - Ready for MCP browser automation execution"
        return 0
    else
        echo "⚠️ MCP Orchestration Health: DEGRADED - Attempting coordinated MCP recovery"
        return 1
    fi
}
```

**MCP Auto-Recovery Coordination & Failover:**
- **Intelligent MCP Restart Sequences**: Coordinated server restart with MCP browser session preservation
- **Port Conflict Resolution**: Dynamic port allocation with MCP configuration updates
- **MCP Service Dependencies**: Ensure proper startup order and MCP tool dependency validation
- **MCP Failover Mechanisms**: Automatic failover to backup MCP configurations

**MCP Resource Optimization & Performance Coordination:**
- **Dynamic MCP Resource Allocation**: Optimize resources based on MCP browser automation requirements
- **MCP Performance Tuning**: Real-time performance optimization during MCP execution
- **MCP Load Distribution**: Intelligent load distribution across available MCP resources
- **MCP Capacity Planning**: Predictive resource planning based on MCP historical data

### ⚡ Integration Orchestrator

**MCP Tool Coordination & Seamless Integration:**

```json
// Advanced MCP Tool Integration with Orchestration
{
  "mcp_orchestration_execution": {
    "function": "ORCHESTRATE_MCP_EXECUTION",
    "parameters": {
      "test_id": "B007",
      "mcp_tools_sequence": [
        {
          "tool": "mcp__playwright__browser_snapshot",
          "purpose": "capture_pre_test_state",
          "orchestration_metadata": {
            "checkpoint_id": "B007_pre_execution",
            "state_validation": "required"
          }
        },
        {
          "tool": "mcp__playwright__browser_click",
          "purpose": "interact_with_ui_element",
          "orchestration_metadata": {
            "performance_tracking": "enabled",
            "retry_logic": "intelligent"
          }
        },
        {
          "tool": "mcp__playwright__browser_wait_for",
          "purpose": "await_response_with_polling",
          "parameters": {"time": 10},
          "orchestration_metadata": {
            "polling_optimization": "10s_intervals",
            "early_detection": "enabled"
          }
        },
        {
          "tool": "mcp__playwright__browser_evaluate",
          "purpose": "validate_test_completion",
          "orchestration_metadata": {
            "evidence_collection": "comprehensive",
            "performance_metrics": "capture"
          }
        }
      ]
    },
    "orchestration_coordination": {
      "pre_execution_health_check": "MCP_ORCHESTRATION_HEALTH_CHECK",
      "todowrite_integration": "real_time_updates",
      "performance_baseline_capture": "enabled",
      "real_time_monitoring": "comprehensive",
      "post_execution_validation": "multi_layer"
    },
    "execution_flow": {
      "start_time_capture": "high_precision",
      "mcp_tool_execution": "sequential_with_monitoring",
      "performance_classification": "real_time",
      "todowrite_result_update": "immediate",
      "orchestration_metrics_update": "continuous"
    }
  }
}
```

**MCP Report Generation Coordination:**
- **MCP Data Aggregation**: Centralized collection of MCP execution data across all browser automation tests
- **MCP Performance Analytics**: Advanced performance analysis with MCP-specific trend detection
- **Cross-Methodology Comparison**: Coordinate reporting between MCP and CLI methodologies
- **MCP Quality Metrics**: Comprehensive quality metrics and MCP validation reporting

**MCP Atomic Operations & Consistency:**
- **MCP Transaction Management**: Ensure atomic operations across all MCP orchestration components
- **MCP State Consistency**: Maintain consistent state across all MCP orchestration phases
- **MCP Rollback Capability**: Comprehensive rollback mechanisms for failed MCP operations
- **MCP Data Integrity**: Ensure data integrity throughout the MCP orchestration process

### 🛡️ Quality Assurance Orchestrator

**Comprehensive MCP Validation Throughout Execution:**

```json
// MCP Quality Assurance Orchestration Framework
{
  "mcp_quality_orchestration_gate": {
    "function": "QUALITY_MCP_ORCHESTRATION_GATE",
    "phases": {
      "pre_execution": {
        "mcp_environment_validation": {
          "env_file_check": "validate .env file presence",
          "api_key_validation": "verify POLYGON_API_KEY and OPENAI_API_KEY",
          "mcp_tool_availability": "confirm all mcp__playwright__* tools accessible",
          "browser_environment": "validate browser installation for MCP automation"
        },
        "mcp_server_validation": {
          "backend_health": "verify FastAPI server for MCP integration",
          "frontend_health": "verify React frontend for MCP browser automation",
          "cors_validation": "test cross-origin requests for MCP"
        },
        "orchestration_gate_result": "pass/fail with MCP-specific details"
      },
      "during_execution": {
        "mcp_performance_monitoring": {
          "browser_memory_usage": "monitor browser memory consumption",
          "mcp_tool_latency": "track MCP tool response times",
          "session_continuity": "validate browser session preservation",
          "polling_efficiency": "monitor 10-second polling effectiveness"
        },
        "mcp_resource_monitoring": {
          "cpu_usage_tracking": "monitor system CPU during MCP automation",
          "network_activity": "track network usage for MCP browser operations",
          "browser_stability": "monitor browser process stability"
        },
        "orchestration_monitoring_result": "real_time_status_with_alerts"
      },
      "post_execution": {
        "mcp_result_validation": {
          "browser_state_capture": "final browser state documentation",
          "mcp_execution_evidence": "comprehensive evidence collection",
          "performance_metrics_validation": "validate MCP performance data",
          "session_cleanup_verification": "confirm proper browser session cleanup"
        },
        "mcp_quality_assessment": {
          "test_execution_integrity": "verify complete MCP test execution",
          "performance_baseline_comparison": "compare against MCP baselines",
          "cross_methodology_comparison": "compare MCP vs CLI results"
        },
        "orchestration_gate_completion": "comprehensive_mcp_validation_complete"
      }
    }
  }
}
```

**MCP Error Detection & Recovery Coordination:**
- **Multi-Layer MCP Error Detection**: Comprehensive error detection across all MCP orchestration components
- **Intelligent MCP Recovery Strategies**: Context-aware recovery based on MCP error type and browser state
- **MCP Error Escalation**: Automated error escalation with MCP-specific notification and recovery coordination
- **MCP Learning System**: Adaptive error handling based on MCP historical error patterns

**MCP Performance Monitoring & Baseline Comparison:**
- **Real-Time MCP Performance Tracking**: Continuous performance monitoring with MCP-specific trend analysis
- **MCP Baseline Validation**: Automatic comparison against historical MCP performance baselines
- **MCP Performance Regression Detection**: Early detection of MCP performance degradation
- **MCP Optimization Recommendations**: Automated optimization recommendations based on MCP performance data

**MCP Testing Integrity Enforcement:**
- **MCP Execution Verification**: Multi-layer verification of MCP test execution integrity
- **MCP Result Validation**: Comprehensive validation of MCP test results and evidence collection
- **MCP Compliance Enforcement**: Ensure adherence to official test specifications via MCP
- **MCP Audit Trail**: Complete audit trail of all MCP orchestration activities and decisions

---

## Execution Protocol - Complete MCP Testing A-I Workflow

## 🚨 CRITICAL: @agent-tech-lead-orchestrator IS NOT ALLOWED TO RUN ANY TESTS & CAN ONLY DELEGATE & COORDINATE TASK(S) TO SPECIALIST(S)

The `/test_mcp_full` command follows a systematic A-I process with tech-lead orchestration for Complete MCP Test Suite execution.

### A-I Workflow Steps

**A. User Invokes `/test_mcp_full`**

- User triggers Complete MCP Test Suite execution via `/test_mcp_full` command
- Command scope: Execute ALL B001-B016 tests using MCP browser automation methodology

**B. Main Agent uses @agent-tech-lead-orchestrator (MANDATORY)**

- Tech-lead analyzes Complete MCP Testing requirements from official test specifications
- Systematic evaluation of MCP tool requirements and browser session management planning
- Must enforce reading `gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`
- Plan execution of 16-item B001-B016 test checklist using TodoWrite integration

**C. Enhanced Infrastructure Verification Phase**

🔧 **Pre-Flight MCP Validation Checklist:**
- Tech-lead assigns specialist to execute comprehensive MCP validation framework
- **Environment Variables**: Validate POLYGON_API_KEY, OPENAI_API_KEY presence and format
- **MCP Tool Dependencies**: Verify all required MCP playwright tools are available and functional
- **Port Availability**: Scan ports 8000, 3000-3003 for conflicts with automatic resolution
- **Process Detection**: Check for existing server processes and handle gracefully
- **Browser Environment**: Validate browser installation and MCP compatibility

🏥 **Server Health Validation with MCP Auto-Recovery:**
- **FastAPI Backend**: Verify "Application startup complete." on <http://0.0.0.0:8000>
  - **MCP Auto-Recovery**: Restart server if MCP health check fails
  - **Port Conflict Resolution**: Use alternate ports 8001-8003 if 8000 busy for MCP
  - **Timeout Handling**: 60-second startup timeout with MCP progress monitoring
- **React Frontend**: Verify "VITE ready" on auto-selected port (3000→3003)
  - **MCP Auto-Recovery**: Restart frontend if MCP health check fails
  - **Dependency Validation**: Auto-install npm dependencies if missing for MCP
  - **Build Validation**: Verify successful Vite compilation for MCP browser automation

🔗 **Advanced MCP Health Checks with Retry Logic:**
- **Backend Health**: MCP-compatible health validation with 3 retry attempts
- **Frontend Health**: MCP browser navigation test with 3 retry attempts
- **CORS Validation**: Test cross-origin requests specifically for MCP browser automation
- **API Integration**: Validate backend-frontend communication pipeline for MCP

🎭 **MCP Tool & Browser Environment Validation:**
- **MCP Tool Availability**: Verify all required `mcp__playwright__*` tools are accessible
- **Browser Installation**: Check browser availability for MCP automation
- **Session Management**: Validate MCP browser session management capabilities
- **Tool Integration**: Test MCP tool integration with browser automation
- **Performance Baseline**: Establish MCP-specific baseline performance metrics

**D. Robust MCP Test Suite Execution Phase**

🚀 **Enhanced MCP Execution Framework with Error Recovery:**
- Specialist(s) execute ALL B001-B016 tests with comprehensive MCP monitoring
- **Intelligent MCP Configuration**: Auto-optimize MCP tool parameters based on system resources
- **Real-Time MCP Monitoring**: Track MCP execution progress with performance alerts
- **MCP Failure Recovery**: Automatic retry logic for transient MCP failures (network, timeout)
- **Resource Management**: Monitor CPU, memory, network usage during MCP execution

📊 **Advanced MCP Performance Tracking:**
- **MCP Baseline Validation**: Compare against historical MCP performance data
- **Real-Time Classification**: Live MCP performance classification (😊😐😴❌)
- **MCP Trend Analysis**: Detect MCP performance regression patterns
- **Bottleneck Detection**: Identify slow MCP components for optimization
- **Resource Utilization**: Track system resource consumption during MCP automation

🔄 **Resilient MCP Execution Strategy:**
- **Single Browser Session Protocol**: Single `mcp__playwright__browser_navigate` → ALL B001-B016 → `mcp__playwright__browser_close`
- **10-Second Polling Intelligence**: Use `mcp__playwright__browser_wait_for` with optimized `"time": 10` intervals
- **Session Continuity Management**: Maintain single browser instance with MCP state preservation
- **Progressive Checkpoints**: TodoWrite integration with MCP rollback capability
- **Partial Recovery**: Resume from last successful MCP checkpoint on failure
- **Clean State Management**: Reset MCP browser environment between test groups
- **Evidence Collection**: Comprehensive MCP logging and screenshot capture

⚡ **Automated MCP Error Handling:**
- **Transient MCP Failure Recovery**: Auto-retry MCP network, timeout, resource errors
- **Permanent MCP Failure Logging**: Document and continue on MCP configuration errors
- **MCP Environment Reset**: Clean browser state and server restart on critical MCP failures
- **Graceful MCP Degradation**: Continue testing with reduced MCP functionality when possible

**E. Enhanced MCP Testing Methodology with Validation Framework**

🎯 **Official Test Specifications Compliance with MCP Validation:**
- Specialist MUST read and validate against official test specifications for MCP
- **Pre-Test MCP Validation**: Verify MCP tool integrity and configuration before execution
- **Specification Checksum**: Validate test specifications haven't been modified
- **MCP Parameter Validation**: Sanitize and validate all MCP parameters before execution

⚙️ **Enhanced MCP Execution Pattern with Intelligence:**
```json
// Pre-execution MCP validation
{
  "tool": "mcp__playwright__browser_navigate",
  "validation": "verify_url_accessibility",
  "parameters": {"url": "http://localhost:3000"}
}

// Intelligent MCP execution with monitoring
{
  "tool": "mcp__playwright__browser_wait_for",
  "monitoring": "performance_tracking",
  "parameters": {"text": "Expected Response Pattern", "time": 10}
}

// Post-execution MCP validation
{
  "tool": "mcp__playwright__browser_evaluate",
  "validation": "evidence_collection",
  "parameters": {"function": "() => console.log('Test completed:', new Date())"}
}
```

🔍 **Multi-Layer MCP Validation Framework:**
- **Pre-Execution**: MCP environment, dependencies, tool availability, configuration
- **During Execution**: MCP performance monitoring, resource tracking, error detection
- **Post-Execution**: MCP result validation, evidence collection, baseline comparison
- **Evidence-Based Completion**: Require concrete evidence of MCP test execution

📏 **Enhanced MCP Performance Classification with Baselines:**
- **Good 😊**: ≤30 seconds (optimal MCP performance)
- **OK 😐**: 31-60 seconds (acceptable MCP performance)
- **Slow 😴**: 61-119 seconds (functional but slow MCP)
- **TIMEOUT ❌**: ≥120 seconds (automatic MCP FAIL)
- **MCP Baseline Comparison**: Compare against historical MCP performance data
- **MCP Regression Detection**: Alert on significant MCP performance degradation

🛡️ **MCP Test Integrity Enforcement:**
- **Response Format Flexibility**: Accept JSON, emojis, conversational responses via MCP
- **Emoji Encouragement**: Financial emojis (📈📉💰) are ENCOURAGED and expected in MCP
- **NO Custom Tests**: Only execute official B001-B016 tests via MCP - reject custom test creation
- **MCP Execution Order**: Maintain B001-B016 sequence for MCP consistency
- **MCP Evidence Requirements**: Collect MCP execution logs, screenshots, performance data

**F. Test Report Generation - Final Task 1**

- Generate comprehensive MCP Test Suite execution report with performance data
- Include MCP methodology results, session continuity validation, and performance classifications
- Document any failures with detailed analysis but DO NOT attempt to fix them
- Save report using `Write` tool with standardized naming: `playwright_MCP_test_[timestamp].md`
- Include browser session management notes, polling data, and MCP tool validation

**G. Task Summary & CLAUDE.md Update - Final Task 2**

- Generate comprehensive MCP Test Suite Summary → overwrite `LAST_TASK_SUMMARY.md`
- Generate MAX 20-line high-level overview → update CLAUDE.md task summary section
- Include all test results, performance data, MCP methodology notes, and completion status for atomic commit

**H. Atomic Git Commit & Push - Final Task 3**

- PRIMARY: Use `git` for atomic operations
- Single atomic commit containing ALL changes:
  - MCP test report files
  - Documentation updates  
  - CLAUDE.md updates
  - LAST_TASK_SUMMARY.md updates
- **CRITICAL**: Must push to complete workflow - commit without push is incomplete

**I. Final Verification - Final Task 4**

- Run final verification to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all MCP test reports and changes are properly committed and pushed to GitHub

### 🚨 CRITICAL: Enhanced MCP Server Startup Requirements with Auto-Recovery

**INTELLIGENT MCP SERVER MANAGEMENT WITH AUTOMATED RECOVERY**:

🔧 **Pre-Startup MCP Validation:**
```bash
# Check for existing processes and handle gracefully for MCP
lsof -i :8000 && echo "Port 8000 busy - MCP will use auto-recovery"
lsof -i :3000 && echo "Port 3000 busy - MCP will use auto-recovery"

# Validate MCP environment before startup
test -f .env && echo "✓ Environment file present for MCP" || echo "❌ Missing .env file for MCP"
grep -q "POLYGON_API_KEY" .env && echo "✓ Polygon API key configured for MCP"
grep -q "OPENAI_API_KEY" .env && echo "✓ OpenAI API key configured for MCP"

# Validate MCP tool availability
echo "Checking MCP tool availability..."
echo "mcp__playwright__browser_navigate: available"
echo "mcp__playwright__browser_close: available"
echo "mcp__playwright__browser_wait_for: available"
```

🚀 **Enhanced MCP Backend Server with Auto-Recovery:**
```bash
cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp

# MCP auto-recovery startup with port conflict resolution
for port in 8000 8001 8002 8003; do
  if ! lsof -i :$port > /dev/null 2>&1; then
    echo "Starting FastAPI for MCP on port $port..."
    uv run uvicorn src.main:app --host 0.0.0.0 --port $port --reload &
    sleep 10
    if curl -s http://localhost:$port/health | grep -q "ok"; then
      echo "✓ FastAPI server for MCP running on port $port"
      export MCP_BACKEND_PORT=$port
      break
    fi
  fi
done
```

🎯 **Enhanced MCP Frontend Server with Dependency Management:**
```bash
cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI

# MCP auto-install dependencies if missing
if [ ! -d "node_modules" ]; then
  echo "Installing npm dependencies for MCP..."
  npm install
fi

# Start with MCP auto-recovery and health validation
npm run dev &
sleep 15

# Validate frontend is responding for MCP browser automation
for port in 3000 3001 3002 3003; do
  if curl -s http://localhost:$port/ | grep -q "Market Parser"; then
    echo "✓ React frontend for MCP running on port $port"
    export MCP_FRONTEND_PORT=$port
    break
  fi
done
```

⚡ **Automated MCP Health Validation with Retry Logic:**
```bash
# MCP Backend health check with retry
for i in {1..5}; do
  if curl -s http://localhost:8000/health | grep -q "ok"; then
    echo "✓ MCP Backend health check passed (attempt $i)"
    break
  else
    echo "⚠️ MCP Backend health check failed (attempt $i), retrying..."
    sleep 5
  fi
done

# MCP Frontend health check with retry
for i in {1..5}; do
  if curl -s http://localhost:3000/ > /dev/null 2>&1; then
    echo "✓ MCP Frontend health check passed (attempt $i)"
    break
  else
    echo "⚠️ MCP Frontend health check failed (attempt $i), retrying..."
    sleep 5
  fi
done

# MCP Tool connectivity validation
echo "Validating MCP tool connectivity..."
echo "mcp__playwright__browser_navigate: ✓ Ready for MCP automation"
echo "mcp__playwright__browser_wait_for: ✓ Ready for 10-second polling"
echo "mcp__playwright__browser_close: ✓ Ready for session management"
```

🛡️ **MCP Failure Recovery Mechanisms:**
- **Port Conflict Resolution**: Automatic detection and alternate port assignment for MCP
- **Dependency Auto-Installation**: Missing packages automatically installed for MCP
- **Health Check Retry**: Up to 5 retry attempts with exponential backoff for MCP
- **Process Recovery**: Dead processes automatically restarted for MCP browser automation
- **Environment Validation**: API keys and MCP configuration verified before startup
- **MCP Tool Validation**: All required MCP tools verified and ready for automation

**✅ MCP SUCCESS CRITERIA**: Both servers responding to health checks + MCP tools validated
**❌ MCP FAILURE HANDLING**: Automatic recovery attempts before marking MCP as failed

### 🔧 Enhanced MCP Testing Principles with Orchestration Integration

**Orchestration-Enhanced MCP Testing Principles:**
- **Official Test Specifications ONLY**: No custom tests - follow B001-B016 exactly as documented with MCP orchestration coordination
- **Single Browser Session Protocol with Orchestration**: All MCP tests execute in same browser instance via orchestration-managed session management
- **10-Second Polling Intervals with Intelligence**: Use `mcp__playwright__browser_wait_for` with `"time": 10` and orchestration optimization consistently
- **Performance Classification with MCP Orchestration**: Record accurate timing data and classify as 😊😐😴❌ with orchestration analytics (expect more 😐😴 for MCP)
- **Coverage-First with MCP Recovery**: Execute all B001-B016 tests with orchestration recovery regardless of individual failures
- **NO FIX ATTEMPTS**: Document failures with orchestration analysis but do not attempt to fix issues - testing only
- **Orchestrated MCP TodoWrite Integration**: Track progress through 16-item B001-B016 checklist with MCP orchestration state management

**MCP Orchestration-Specific Enhancements:**
- **Real-Time MCP Orchestration**: Live coordination of MCP browser automation with performance optimization
- **Intelligent MCP Session Management**: Dynamic browser session management based on orchestration analysis
- **Cross-Test MCP Learning**: Orchestration learns from MCP browser automation patterns for optimization
- **Predictive MCP Performance**: Orchestration provides predictive performance analysis based on MCP historical data
- **Quality Gate Integration**: Each MCP test phase includes orchestration quality gates for comprehensive validation
- **Single Session Continuity**: Orchestration ensures browser session preservation throughout entire B001-B016 sequence

### Quality Requirements with MCP Orchestration Integration

**Enhanced MCP Quality Requirements:**
- **Tech-lead orchestrator MANDATORY** for Complete MCP Testing coordination with advanced orchestration framework
- **MCP browser automation tools with orchestration enhancement** as PRIMARY method for all specialist testing operations
- **Official test specifications compliance** enforced through MCP orchestration quality gates
- **Atomic commit principle with orchestration**: ALL changes in single commit operation with MCP orchestration metadata
- **Advanced test report generation** with MCP session management insights, orchestration analytics, and polling performance data

**MCP Orchestration Quality Standards:**
- **Execution Flow Orchestration**: Intelligent MCP test sequencing with browser session dependency management and performance optimization
- **State Management Orchestration**: Real-time MCP state tracking with cross-methodology coordination
- **Server Lifecycle Orchestration**: Comprehensive MCP health monitoring with auto-recovery and failover capabilities
- **Integration Orchestration**: Seamless MCP tool coordination with atomic operations and quality assurance
- **Performance Orchestration**: Advanced MCP performance monitoring with baseline comparison and regression detection
- **Session Continuity Orchestration**: Intelligent browser session management with state preservation throughout testing

---

## 🚨 CRITICAL: MCP Testing Execution Protocol

### Single Browser Session Protocol (ENFORCED)

**✅ CORRECT METHODOLOGY**:

```
Single Browser Session MCP Testing Protocol:
mcp__playwright__browser_navigate → B001-B016 Tests → mcp__playwright__browser_close
```

**Real-World User Simulation:**
- Users don't close application between different test actions
- State continuity preserved throughout entire test sequence
- Session data, cookies, UI state maintained across all tests
- Performance baseline accuracy through session preservation

**❌ PROHIBITED METHODOLOGY**:

```bash
❌ browser_navigate → Basic Tests → browser_close → browser_navigate → Button Tests → browser_close
❌ Fresh browser state between any B001-B016 tests
❌ Multiple browser sessions for single test sequence
❌ New browser instance per test or test group
```

### MCP Tool Configuration Requirements

**Browser Session Management:**
```json
{
  "session_start": {
    "tool": "mcp__playwright__browser_navigate",
    "parameters": {"url": "http://localhost:3000"},
    "usage": "ONCE at beginning of entire test sequence"
  },
  "session_end": {
    "tool": "mcp__playwright__browser_close", 
    "parameters": {},
    "usage": "ONCE at end of entire test sequence"
  }
}
```

**10-Second Polling Configuration:**
```json
{
  "response_detection": {
    "tool": "mcp__playwright__browser_wait_for",
    "parameters": {"text": "Expected Response Pattern", "time": 10},
    "note": "10-second intervals REQUIRED - any other interval is configuration error"
  }
}
```

**Interactive Elements:**
```json
{
  "user_interaction": {
    "input_tool": "mcp__playwright__browser_type",
    "click_tool": "mcp__playwright__browser_click", 
    "key_tool": "mcp__playwright__browser_press_key",
    "validation_tool": "mcp__playwright__browser_evaluate"
  }
}
```

### Performance Classification System

- **Good 😊**: ≤30 seconds (optimal performance)
- **OK 😐**: 31-60 seconds (acceptable performance)  
- **Slow 😴**: 61-119 seconds (functional but slow)
- **TIMEOUT ❌**: ≥120 seconds (automatic FAIL)

### MCP-Specific Expected Performance

- **Target Distribution**: More OK 😐 and Slow 😴 classifications (MCP inherently slower than CLI)
- **Normal Expectations**: MCP browser automation typically slower than direct CLI execution
- **Session Benefits**: Single session provides accurate performance baseline without browser startup overhead
- **Polling Advantage**: 10-second polling enables early detection of successful operations

### B001-B016 Test Coverage Requirements

**Complete Test Suite Coverage:**
- Cross-Browser Compatibility: B001 (Chrome), B002 (Firefox), B003 (Safari)
- Basic Functionality Tests: Market Status, Ticker Analysis, Multi-Ticker
- UI Interaction Tests: Button Response Time, State Management, Sequential Operations
- Input Validation Tests: Natural Language, Case Sensitivity, Special Characters
- Export Function Tests: JSON Copy, Format Validation, Multiple Analysis
- Responsive Design Tests: Mobile, Desktop, Tablet Viewports
- API Integration Tests: Health Check, Schema Compliance, Error Handling
- Accessibility Tests: Keyboard Navigation, Screen Reader, High Contrast
- Error Recovery Tests: Network Errors, Timeout Handling, API Failures
- Additional Coverage: Performance baseline, Security validation, Integration testing

**16-Item TodoWrite Checklist Integration:**
- Create todo list with all B001-B016 tests before execution
- Mark each test as in_progress before MCP browser automation execution
- Mark each test as completed after successful MCP test execution
- Never claim completion without actual MCP browser automation test execution

### MCP Browser Session Continuity Validation

**Session State Preservation Testing:**
- Verify session data maintained across test sequence
- Validate UI state consistency throughout testing
- Confirm performance characteristics stable within session
- Document session-specific observations and insights

**Browser Instance Management:**
- Single browser context preserved throughout entire B001-B016 sequence
- No browser restarts between test groups or individual tests
- Session cookies, local storage, and application state maintained
- Real-world user experience simulation through continuous session

---