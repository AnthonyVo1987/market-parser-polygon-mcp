# Test CLI Full Slash Command

@agent-tech-lead-orchestrator to delegate & coordinate Specialist(s) to Execute Complete B001-B016 CLI Test Suite

## 🚨 CRITICAL: @agent-tech-lead-orchestrator IS NOT ALLOWED TO RUN ANY TESTS & CAN ONLY DELEGATE & COORDINATE TASK(S) TO SPECIALIST(S)

**Testing Focus:** Execute the complete B001-B016 Playwright test suite using CLI methodology with enhanced configuration and comprehensive reporting.

## How to Use

1. **Ensure servers are running** (FastAPI backend + React frontend)
2. **Run this command**: `/test_cli_full`
3. **Follow the orchestrated plan** as specialists execute the Complete CLI Test Suite

## What This Command Does

When you invoke `/test_cli_full`, I will:

## 🚨 CRITICAL: @agent-tech-lead-orchestrator IS NOT ALLOWED TO RUN ANY TESTS & CAN ONLY DELEGATE & COORDINATE TASK(S) TO SPECIALIST(S)

1. **Invoke @agent-tech-lead-orchestrator** to analyze the Complete CLI Testing requirements and create a specialist assignment plan
2. **Execute the Complete B001-B016 Tests** using CLI methodology with the exact agents recommended by the tech-lead
3. **Enforce official test specifications** reading from `gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`
4. **Ensure CLI tool compliance** for all specialists using Bash commands with enhanced configuration
5. **Generate comprehensive test reports** and commit results following A-I workflow

## Enhanced Command Execution Framework

**🚀 ENHANCED VALIDATION & PARSING LOGIC**

This enhanced command includes comprehensive validation and error recovery mechanisms:

### 🔍 Pre-Execution Validation Framework
- **Environment Health Checks**: API keys, tool availability, dependency verification
- **Infrastructure Validation**: Server status, port availability, CORS configuration
- **Test Prerequisites**: Playwright installation, test file existence, browser availability
- **Conflict Detection**: Port conflicts, process conflicts, resource availability
- **Readiness Assessment**: Go/no-go decision based on comprehensive validation

### 🛡️ Enhanced Parsing & Error Recovery
- **Parameter Sanitization**: Command input validation and sanitization
- **Intelligent Retry Logic**: Automatic retry for transient failures
- **Graceful Degradation**: Partial execution recovery on component failures
- **Performance Monitoring**: Real-time execution tracking and baseline validation
- **Evidence-Based Validation**: Multi-layer completion verification

### ⚡ Automated Recovery Mechanisms
- **Server Auto-Restart**: Automatic server recovery on failures
- **Port Conflict Resolution**: Dynamic port allocation and configuration
- **Dependency Auto-Installation**: Missing tool and dependency resolution
- **Test Environment Reset**: Clean state restoration between test phases
- **Cleanup Procedures**: Comprehensive resource cleanup on errors

I'll use @agent-tech-lead-orchestrator to analyze the Complete CLI Testing requirements and assign the appropriate specialists from the available AI Team:

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

When Complete CLI Tests are requested, specialists MUST read the official test plan from:
`gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`

**Complete CLI Test Suite Definition (B001-B016)**:

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

## CLI Tool Requirements

**ALL specialist agents MUST use CLI tools with enhanced configuration:**

- `Bash(cd:*)` - Navigate to test directories
- `Bash(npx:*)` - Execute Playwright CLI commands with proper configuration
- `Bash(curl:*)` - Health check validation and server verification
- `Bash(ls:*)` - Test file verification and directory listing
- `TodoWrite` - Track progress through 16-item B001-B016 test checklist
- `Write` - Generate comprehensive test reports

**CLI-specific configuration requirements:**

- Use `--timeout=120000` (120-second universal timeout)
- Use `--workers=1` (single browser session requirement)
- Include descriptive error messages for failures
- Capture and report actual execution times

**Enhanced CLI Pattern:**
```bash
npx playwright test --timeout=120000 --workers=1 test-b001-chrome-compatibility.spec.ts
npx playwright test --timeout=120000 --workers=1 test-b002-firefox-compatibility.spec.ts
# ... continue for all B001-B016 tests
```

**Failure to use required CLI configuration will result in work rejection.**

---

## 🚀 ADVANCED ORCHESTRATION FRAMEWORK

### 🎯 Execution Flow Orchestrator

**Intelligent Test Sequencing with Dependency Management:**

```
B001-B003: Cross-Browser Compatibility Foundation
├─► B004-B006: Basic Functionality Validation
│   ├─► B007-B009: Interactive UI Components
│   │   ├─► B010-B012: Advanced Input Processing
│   │   │   ├─► B013-B015: Export & Integration
│   │   │   │   └─► B016: Performance & Security
│   │   │   └─► Parallel: Accessibility Testing
│   │   └─► Parallel: Responsive Design Testing
│   └─► Parallel: Error Handling Testing
└─► Continuous: Performance Monitoring & Baseline Validation
```

**Dynamic Resource Allocation & Load Balancing:**
- **System Resource Assessment**: Real-time CPU, memory, network analysis
- **CLI Optimization**: Direct execution path optimization for maximum performance
- **Parallel Execution Coordination**: Safe parallelization within CLI constraints
- **Resource Scaling**: Dynamic allocation based on test complexity and system capacity

**Intelligent Recovery & Retry Coordination:**
- **Failure Classification**: Transient vs permanent failure detection
- **Smart Retry Logic**: Exponential backoff with intelligent retry decisions
- **Partial Recovery**: Resume from last successful checkpoint
- **Graceful Degradation**: Continue execution with reduced functionality when appropriate

### 🔄 State Management Orchestrator

**Centralized Test Execution State Tracking:**

```json
{
  "orchestration_state": {
    "execution_phase": "B007_interactive_testing",
    "completed_tests": ["B001", "B002", "B003", "B004", "B005", "B006"],
    "current_test": "B007",
    "pending_tests": ["B008", "B009", "B010", "B011", "B012", "B013", "B014", "B015", "B016"],
    "performance_baseline": {"average_execution_time": 42.3, "classification_distribution": {"good": 4, "ok": 2, "slow": 0, "timeout": 0}},
    "resource_utilization": {"cpu_usage": "23%", "memory_usage": "1.2GB", "network_activity": "moderate"},
    "error_count": 0,
    "recovery_attempts": 0
  }
}
```

**Cross-Methodology State Synchronization:**
- **CLI-MCP Coordination**: Share execution insights between methodologies
- **Performance Comparison**: Real-time performance delta analysis
- **Baseline Synchronization**: Maintain consistent performance baselines
- **State Consistency**: Ensure coordinated state across all execution components

**Progress Coordination with TodoWrite Integration:**
- **Real-Time Updates**: Live progress tracking with TodoWrite synchronization
- **Checkpoint Management**: Strategic checkpoint creation for rollback capability
- **Progress Visualization**: Visual progress indicators with performance insights
- **Completion Validation**: Multi-layer completion verification with evidence collection

### 🏥 Server Lifecycle Orchestrator

**Comprehensive Health Monitoring Matrix:**

```bash
# Advanced Health Monitoring with Orchestration
ORCHESTRATION_HEALTH_CHECK() {
    echo "🏥 Orchestration Health Matrix Validation"
    
    # Backend Server Health with Auto-Recovery
    for attempt in {1..5}; do
        BACKEND_STATUS=$(curl -s -w "%{http_code}" http://localhost:8000/health -o /dev/null)
        if [ "$BACKEND_STATUS" = "200" ]; then
            echo "✓ Backend Health: OPTIMAL (attempt $attempt)"
            BACKEND_HEALTH="optimal"
            break
        else
            echo "⚠️ Backend Health: DEGRADED (attempt $attempt) - Auto-recovery initiated"
            # Trigger auto-recovery sequence
            pkill -f "uvicorn.*main:app" 2>/dev/null
            sleep 3
            cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp
            uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &
            sleep 10
        fi
    done
    
    # Frontend Server Health with Auto-Recovery
    for attempt in {1..5}; do
        FRONTEND_STATUS=$(curl -s -w "%{http_code}" http://localhost:3000/ -o /dev/null)
        if [ "$FRONTEND_STATUS" = "200" ]; then
            echo "✓ Frontend Health: OPTIMAL (attempt $attempt)"
            FRONTEND_HEALTH="optimal"
            break
        else
            echo "⚠️ Frontend Health: DEGRADED (attempt $attempt) - Auto-recovery initiated"
            # Trigger frontend auto-recovery
            pkill -f "npm.*run.*dev" 2>/dev/null
            sleep 3
            cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
            npm run dev &
            sleep 15
        fi
    done
    
    # CLI Tool Environment Validation
    CLI_TOOLS_STATUS="optimal"
    for tool in npx playwright curl uv node npm; do
        if command -v $tool >/dev/null 2>&1; then
            echo "✓ CLI Tool: $tool available"
        else
            echo "❌ CLI Tool: $tool missing - orchestration will attempt auto-installation"
            CLI_TOOLS_STATUS="degraded"
        fi
    done
    
    # Resource Utilization Assessment
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    MEMORY_USAGE=$(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2 }')
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
    
    echo "📊 Resource Utilization: CPU: ${CPU_USAGE}%, Memory: ${MEMORY_USAGE}, Disk: ${DISK_USAGE}"
    
    # Orchestration Health Summary
    if [ "$BACKEND_HEALTH" = "optimal" ] && [ "$FRONTEND_HEALTH" = "optimal" ] && [ "$CLI_TOOLS_STATUS" = "optimal" ]; then
        echo "🎯 Orchestration Health: OPTIMAL - Ready for CLI test execution"
        return 0
    else
        echo "⚠️ Orchestration Health: DEGRADED - Attempting coordinated recovery"
        return 1
    fi
}
```

**Auto-Recovery Coordination & Failover:**
- **Intelligent Restart Sequences**: Coordinated server restart with dependency management
- **Port Conflict Resolution**: Dynamic port allocation with configuration updates
- **Service Dependencies**: Ensure proper startup order and dependency validation
- **Failover Mechanisms**: Automatic failover to backup configurations

**Resource Optimization & Performance Coordination:**
- **Dynamic Resource Allocation**: Optimize resources based on test execution requirements
- **Performance Tuning**: Real-time performance optimization during execution
- **Load Distribution**: Intelligent load distribution across available resources
- **Capacity Planning**: Predictive resource planning based on historical data

### ⚡ Integration Orchestrator

**Tool Coordination & Seamless Integration:**

```bash
# Advanced Tool Integration with Orchestration
ORCHESTRATE_CLI_EXECUTION() {
    local test_file=$1
    local test_id=$2
    
    echo "🔧 Orchestrating CLI execution for $test_id"
    
    # Pre-execution orchestration
    ORCHESTRATION_HEALTH_CHECK || {
        echo "❌ Health check failed - aborting $test_id"
        return 1
    }
    
    # TodoWrite integration with orchestration
    echo "📝 Updating orchestration state for $test_id"
    # TodoWrite: Mark test as in_progress with orchestration metadata
    
    # Performance baseline capture
    START_TIME=$(date +%s.%N)
    
    # CLI execution with orchestration monitoring
    echo "🚀 Executing: npx playwright test --timeout=120000 --workers=1 --reporter=line $test_file"
    
    # Execute with real-time monitoring
    timeout 125s npx playwright test --timeout=120000 --workers=1 --reporter=line "$test_file" 2>&1 | while IFS= read -r line; do
        echo "$line"
        # Real-time performance analysis
        if echo "$line" | grep -q "PASSED\|FAILED\|ERROR"; then
            echo "📊 Test result detected: $line"
        fi
    done
    
    # Capture execution results
    EXIT_CODE=${PIPESTATUS[0]}
    END_TIME=$(date +%s.%N)
    EXECUTION_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    
    # Performance classification with orchestration
    if (( $(echo "$EXECUTION_TIME <= 30" | bc -l) )); then
        CLASSIFICATION="😊 GOOD"
    elif (( $(echo "$EXECUTION_TIME <= 60" | bc -l) )); then
        CLASSIFICATION="😐 OK"
    elif (( $(echo "$EXECUTION_TIME <= 119" | bc -l) )); then
        CLASSIFICATION="😴 SLOW"
    else
        CLASSIFICATION="❌ TIMEOUT"
    fi
    
    echo "⏱️ $test_id completed in ${EXECUTION_TIME}s - Classification: $CLASSIFICATION"
    
    # TodoWrite integration with results
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ $test_id: PASSED - Updating orchestration state"
        # TodoWrite: Mark as completed with performance data
    else
        echo "❌ $test_id: FAILED - Orchestration will continue with next test"
        # TodoWrite: Mark as failed but continue execution
    fi
    
    # Update orchestration metrics
    echo "📊 Orchestration metrics updated for $test_id"
    
    return $EXIT_CODE
}
```

**Report Generation Coordination:**
- **Data Aggregation**: Centralized collection of execution data across all tests
- **Performance Analytics**: Advanced performance analysis with trend detection
- **Cross-Methodology Comparison**: Coordinate reporting between CLI and MCP methodologies
- **Quality Metrics**: Comprehensive quality metrics and validation reporting

**Atomic Operations & Consistency:**
- **Transaction Management**: Ensure atomic operations across all orchestration components
- **State Consistency**: Maintain consistent state across all orchestration phases
- **Rollback Capability**: Comprehensive rollback mechanisms for failed operations
- **Data Integrity**: Ensure data integrity throughout the orchestration process

### 🛡️ Quality Assurance Orchestrator

**Comprehensive Validation Throughout Execution:**

```bash
# Quality Assurance Orchestration Framework
QUALITY_ORCHESTRATION_GATE() {
    local phase=$1
    local test_id=$2
    
    echo "🛡️ Quality Gate: $phase for $test_id"
    
    case $phase in
        "pre_execution")
            # Pre-execution validation
            echo "🔍 Pre-execution quality validation"
            
            # Environment validation
            [ -f ".env" ] && echo "✓ Environment file present" || {
                echo "❌ Missing .env file - orchestration blocked"
                return 1
            }
            
            # API key validation
            grep -q "POLYGON_API_KEY" .env && echo "✓ Polygon API key configured" || {
                echo "❌ Missing Polygon API key - orchestration blocked"
                return 1
            }
            
            # Test file validation
            [ -f "tests/playwright/$test_id.spec.ts" ] && echo "✓ Test file exists" || {
                echo "❌ Test file missing - orchestration blocked"
                return 1
            }
            
            echo "✅ Pre-execution quality gate passed"
            ;;
            
        "during_execution")
            # Real-time execution validation
            echo "🔍 During-execution quality monitoring"
            
            # Performance monitoring
            CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
            if (( $(echo "$CPU_USAGE > 90" | bc -l) )); then
                echo "⚠️ High CPU usage detected: ${CPU_USAGE}% - orchestration monitoring"
            fi
            
            # Memory monitoring
            MEMORY_USAGE=$(free | awk 'FNR==2{printf "%.2f", $3/($3+$4)*100}')
            if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
                echo "⚠️ High memory usage detected: ${MEMORY_USAGE}% - orchestration monitoring"
            fi
            
            echo "✅ During-execution quality monitoring active"
            ;;
            
        "post_execution")
            # Post-execution validation
            echo "🔍 Post-execution quality validation"
            
            # Result validation
            if [ -f "test-results/$test_id-results.json" ]; then
                echo "✓ Test results captured"
            else
                echo "⚠️ Test results not found - orchestration will continue"
            fi
            
            # Performance validation
            echo "📊 Performance metrics validated"
            
            echo "✅ Post-execution quality gate completed"
            ;;
    esac
    
    return 0
}
```

**Error Detection & Recovery Coordination:**
- **Multi-Layer Error Detection**: Comprehensive error detection across all orchestration components
- **Intelligent Recovery Strategies**: Context-aware recovery based on error type and system state
- **Error Escalation**: Automated error escalation with notification and recovery coordination
- **Learning System**: Adaptive error handling based on historical error patterns

**Performance Monitoring & Baseline Comparison:**
- **Real-Time Performance Tracking**: Continuous performance monitoring with trend analysis
- **Baseline Validation**: Automatic comparison against historical performance baselines
- **Performance Regression Detection**: Early detection of performance degradation
- **Optimization Recommendations**: Automated optimization recommendations based on performance data

**Testing Integrity Enforcement:**
- **Execution Verification**: Multi-layer verification of test execution integrity
- **Result Validation**: Comprehensive validation of test results and evidence collection
- **Compliance Enforcement**: Ensure adherence to official test specifications
- **Audit Trail**: Complete audit trail of all orchestration activities and decisions

---

## Execution Protocol - Complete CLI Testing A-I Workflow

## 🚨 CRITICAL: @agent-tech-lead-orchestrator IS NOT ALLOWED TO RUN ANY TESTS & CAN ONLY DELEGATE & COORDINATE TASK(S) TO SPECIALIST(S)

The `/test_cli_full` command follows a systematic A-I process with tech-lead orchestration for Complete CLI Test Suite execution.

### A-I Workflow Steps

**A. User Invokes `/test_cli_full`**

- User triggers Complete CLI Test Suite execution via `/test_cli_full` command
- Command scope: Execute ALL B001-B016 tests using CLI methodology with enhanced configuration

**B. Main Agent uses @agent-tech-lead-orchestrator (MANDATORY)**

- Tech-lead analyzes Complete CLI Testing requirements from official test specifications
- Systematic evaluation of CLI configuration requirements and testing specialist assignment planning
- Must enforce reading `gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`
- Plan execution of 16-item B001-B016 test checklist using TodoWrite integration

**C. Enhanced Infrastructure Verification Phase**

🔧 **Pre-Flight Validation Checklist:**
- Tech-lead assigns specialist to execute comprehensive validation framework
- **Environment Variables**: Validate POLYGON_API_KEY, OPENAI_API_KEY presence and format
- **Tool Dependencies**: Verify uv, npm, node, npx, curl availability and versions
- **Port Availability**: Scan ports 8000, 3000-3003 for conflicts with automatic resolution
- **Process Detection**: Check for existing server processes and handle gracefully

🏥 **Server Health Validation with Auto-Recovery:**
- **FastAPI Backend**: Verify "Application startup complete." on <http://0.0.0.0:8000>
  - **Auto-Recovery**: Restart server if health check fails
  - **Port Conflict Resolution**: Use alternate ports 8001-8003 if 8000 busy
  - **Timeout Handling**: 60-second startup timeout with progress monitoring
- **React Frontend**: Verify "VITE ready" on auto-selected port (3000→3003)
  - **Auto-Recovery**: Restart frontend if health check fails
  - **Dependency Validation**: Auto-install npm dependencies if missing
  - **Build Validation**: Verify successful Vite compilation

🔗 **Advanced Health Checks with Retry Logic:**
- **Backend Health**: `curl http://localhost:8000/health` with 3 retry attempts
- **Frontend Health**: `curl http://localhost:3000/` with 3 retry attempts
- **CORS Validation**: Test cross-origin requests with automatic CORS fix
- **API Integration**: Validate backend-frontend communication pipeline

🎭 **Playwright & Test Environment Validation:**
- **Playwright CLI**: Verify `npx playwright --version` with auto-installation
- **Browser Installation**: Check browser availability with `npx playwright install`
- **Test File Integrity**: Validate all B001-B016 test files exist and are executable
- **Test Directory**: Verify proper test directory structure and permissions
- **Performance Baseline**: Establish baseline performance metrics for comparison

**D. Robust CLI Test Suite Execution Phase**

🚀 **Enhanced Execution Framework with Error Recovery:**
- Specialist(s) execute ALL B001-B016 tests with comprehensive monitoring
- **Intelligent Configuration**: Auto-optimize `--workers=1 --timeout=120000` based on system resources
- **Real-Time Monitoring**: Track execution progress with performance alerts
- **Failure Recovery**: Automatic retry logic for transient failures (network, timeout)
- **Resource Management**: Monitor CPU, memory, network usage during execution

📊 **Advanced Performance Tracking:**
- **Baseline Validation**: Compare against historical performance data
- **Real-Time Classification**: Live performance classification (😊😐😴❌)
- **Trend Analysis**: Detect performance regression patterns
- **Bottleneck Detection**: Identify slow components for optimization
- **Resource Utilization**: Track system resource consumption

🔄 **Resilient Execution Strategy:**
- **Coverage-First Policy**: Execute ALL B001-B016 tests regardless of individual failures
- **Progressive Checkpoints**: TodoWrite integration with rollback capability
- **Partial Recovery**: Resume from last successful checkpoint on failure
- **Clean State Management**: Reset test environment between test groups
- **Evidence Collection**: Comprehensive logging and screenshot capture

⚡ **Automated Error Handling:**
- **Transient Failure Recovery**: Auto-retry network, timeout, resource errors
- **Permanent Failure Logging**: Document and continue on configuration errors
- **Environment Reset**: Clean browser state and server restart on critical failures
- **Graceful Degradation**: Continue testing with reduced functionality when possible

**E. Enhanced CLI Testing Methodology with Validation Framework**

🎯 **Official Test Specifications Compliance with Validation:**
- Specialist MUST read and validate against official test specifications
- **Pre-Test Validation**: Verify test file integrity and configuration before execution
- **Specification Checksum**: Validate test specifications haven't been modified
- **Parameter Validation**: Sanitize and validate all CLI parameters before execution

⚙️ **Enhanced CLI Execution Pattern with Intelligence:**
```bash
# Pre-execution validation
npx playwright --version && echo "✓ Playwright available"
ls tests/playwright/test-b*.spec.ts | wc -l | grep 16 && echo "✓ All 16 tests present"

# Intelligent execution with monitoring
npx playwright test --timeout=120000 --workers=1 --reporter=line [test-file]
# Post-execution validation
echo "Test completed: $(date)" >> execution.log
```

🔍 **Multi-Layer Validation Framework:**
- **Pre-Execution**: Environment, dependencies, test files, configuration
- **During Execution**: Performance monitoring, resource tracking, error detection
- **Post-Execution**: Result validation, evidence collection, baseline comparison
- **Evidence-Based Completion**: Require concrete evidence of test execution

📏 **Enhanced Performance Classification with Baselines:**
- **Good 😊**: ≤30 seconds (optimal performance)
- **OK 😐**: 31-60 seconds (acceptable performance)
- **Slow 😴**: 61-119 seconds (functional but slow)
- **TIMEOUT ❌**: ≥120 seconds (automatic FAIL)
- **Baseline Comparison**: Compare against historical performance data
- **Regression Detection**: Alert on significant performance degradation

🛡️ **Test Integrity Enforcement:**
- **Response Format Flexibility**: Accept JSON, emojis, conversational responses
- **Emoji Encouragement**: Financial emojis (📈📉💰) are ENCOURAGED and expected
- **NO Custom Tests**: Only execute official B001-B016 tests - reject custom test creation
- **Execution Order**: Maintain B001-B016 sequence for consistency
- **Evidence Requirements**: Collect execution logs, screenshots, performance data

**F. Test Report Generation - Final Task 1**

- Generate comprehensive CLI Test Suite execution report with performance data
- Include CLI methodology results and performance classifications
- Document any failures with detailed analysis but DO NOT attempt to fix them
- Save report using `Write` tool with standardized naming: `playwright_CLI_test_[timestamp].md`
- Include infrastructure status, CLI configuration validation, and error analysis

**G. Task Summary & CLAUDE.md Update - Final Task 2**

- Generate comprehensive CLI Test Suite Summary → overwrite `LAST_TASK_SUMMARY.md`
- Generate MAX 20-line high-level overview → update CLAUDE.md task summary section
- Include all test results, performance data, CLI methodology notes, and completion status for atomic commit

**H. Atomic Git Commit & Push - Final Task 3**

- PRIMARY: Use `git` for atomic operations
- Single atomic commit containing ALL changes:
  - CLI test report files
  - Documentation updates  
  - CLAUDE.md updates
  - LAST_TASK_SUMMARY.md updates
- **CRITICAL**: Must push to complete workflow - commit without push is incomplete

**I. Final Verification - Final Task 4**

- Run final verification to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all CLI test reports and changes are properly committed and pushed to GitHub

### 🚨 CRITICAL: Enhanced Server Startup Requirements with Auto-Recovery

**INTELLIGENT SERVER MANAGEMENT WITH AUTOMATED RECOVERY**:

🔧 **Pre-Startup Validation:**
```bash
# Check for existing processes and handle gracefully
lsof -i :8000 && echo "Port 8000 busy - will use auto-recovery"
lsof -i :3000 && echo "Port 3000 busy - will use auto-recovery"

# Validate environment before startup
test -f .env && echo "✓ Environment file present" || echo "❌ Missing .env file"
grep -q "POLYGON_API_KEY" .env && echo "✓ Polygon API key configured"
grep -q "OPENAI_API_KEY" .env && echo "✓ OpenAI API key configured"
```

🚀 **Enhanced Backend Server with Auto-Recovery:**
```bash
cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp

# Auto-recovery startup with port conflict resolution
for port in 8000 8001 8002 8003; do
  if ! lsof -i :$port > /dev/null 2>&1; then
    echo "Starting FastAPI on port $port..."
    uv run uvicorn src.main:app --host 0.0.0.0 --port $port --reload &
    sleep 10
    if curl -s http://localhost:$port/health | grep -q "ok"; then
      echo "✓ FastAPI server running on port $port"
      break
    fi
  fi
done
```

🎯 **Enhanced Frontend Server with Dependency Management:**
```bash
cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI

# Auto-install dependencies if missing
if [ ! -d "node_modules" ]; then
  echo "Installing npm dependencies..."
  npm install
fi

# Start with auto-recovery and health validation
npm run dev &
sleep 15

# Validate frontend is responding
for port in 3000 3001 3002 3003; do
  if curl -s http://localhost:$port/ | grep -q "Market Parser"; then
    echo "✓ React frontend running on port $port"
    break
  fi
done
```

⚡ **Automated Health Validation with Retry Logic:**
```bash
# Backend health check with retry
for i in {1..5}; do
  if curl -s http://localhost:8000/health | grep -q "ok"; then
    echo "✓ Backend health check passed (attempt $i)"
    break
  else
    echo "⚠️ Backend health check failed (attempt $i), retrying..."
    sleep 5
  fi
done

# Frontend health check with retry
for i in {1..5}; do
  if curl -s http://localhost:3000/ > /dev/null 2>&1; then
    echo "✓ Frontend health check passed (attempt $i)"
    break
  else
    echo "⚠️ Frontend health check failed (attempt $i), retrying..."
    sleep 5
  fi
done
```

🛡️ **Failure Recovery Mechanisms:**
- **Port Conflict Resolution**: Automatic detection and alternate port assignment
- **Dependency Auto-Installation**: Missing packages automatically installed
- **Health Check Retry**: Up to 5 retry attempts with exponential backoff
- **Process Recovery**: Dead processes automatically restarted
- **Environment Validation**: API keys and configuration verified before startup

**✅ SUCCESS CRITERIA**: Both servers responding to health checks
**❌ FAILURE HANDLING**: Automatic recovery attempts before marking as failed

### 🔧 Enhanced CLI Testing Principles with Orchestration Integration

**Orchestration-Enhanced Testing Principles:**
- **Official Test Specifications ONLY**: No custom tests - follow B001-B016 exactly as documented with orchestration coordination
- **Enhanced CLI Configuration**: Use `--timeout=120000 --workers=1` with orchestration monitoring for all test executions
- **Intelligent Test Sequencing**: All CLI tests execute with orchestration-managed dependency coordination
- **Performance Classification with Orchestration**: Record accurate timing data and classify as 😊😐😴❌ with orchestration analytics
- **Coverage-First with Recovery**: Execute all B001-B016 tests with orchestration recovery regardless of individual failures
- **NO FIX ATTEMPTS**: Document failures with orchestration analysis but do not attempt to fix issues - testing only
- **Orchestrated TodoWrite Integration**: Track progress through 16-item B001-B016 checklist with orchestration state management

**Orchestration-Specific CLI Enhancements:**
- **Real-Time Orchestration**: Live coordination of test execution with performance optimization
- **Intelligent Resource Management**: Dynamic resource allocation based on orchestration analysis
- **Cross-Test Learning**: Orchestration learns from test execution patterns for optimization
- **Predictive Performance**: Orchestration provides predictive performance analysis based on historical data
- **Quality Gate Integration**: Each test phase includes orchestration quality gates for comprehensive validation

### Quality Requirements with Orchestration Integration

**Enhanced Quality Requirements:**
- **Tech-lead orchestrator MANDATORY** for Complete CLI Testing coordination with advanced orchestration framework
- **CLI tools with orchestration enhancement** as PRIMARY method for all specialist testing operations
- **Official test specifications compliance** enforced through orchestration quality gates
- **Atomic commit principle with orchestration**: ALL changes in single commit operation with orchestration metadata
- **Advanced test report generation** with CLI performance insights, orchestration analytics, and configuration validation

**Orchestration Quality Standards:**
- **Execution Flow Orchestration**: Intelligent test sequencing with dependency management and performance optimization
- **State Management Orchestration**: Real-time state tracking with cross-methodology coordination
- **Server Lifecycle Orchestration**: Comprehensive health monitoring with auto-recovery and failover capabilities
- **Integration Orchestration**: Seamless tool coordination with atomic operations and quality assurance
- **Performance Orchestration**: Advanced performance monitoring with baseline comparison and regression detection

---

## 🚨 CRITICAL: CLI Testing Execution Protocol

### Enhanced CLI Execution Pattern (ENFORCED)

**✅ CORRECT METHODOLOGY**:

```bash
# Navigate to test directory
cd /home/1000211866/Github/market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp/tests/playwright

# Execute with enhanced configuration
npx playwright test --timeout=120000 --workers=1 --reporter=line test-b001-chrome-compatibility.spec.ts
npx playwright test --timeout=120000 --workers=1 --reporter=line test-b002-firefox-compatibility.spec.ts
npx playwright test --timeout=120000 --workers=1 --reporter=line test-b003-safari-compatibility.spec.ts
# ... continue for all B001-B016 tests
```

**❌ PROHIBITED METHODOLOGY**:

```bash
❌ npx playwright test  # Missing required configuration
❌ npx playwright test --workers=4  # Breaks single session requirement
❌ npx playwright test --timeout=60000  # Wrong timeout value
```

### CLI Configuration Requirements

- **Timeout Configuration**: `--timeout=120000` (120-second universal timeout)
- **Worker Configuration**: `--workers=1` (single browser session requirement)
- **Reporter Configuration**: `--reporter=line` (fast line reporter for CLI)
- **Retry Configuration**: `--retries=0` (no automatic retries for accurate timing)

### Performance Classification System

- **Good 😊**: ≤30 seconds (optimal performance)
- **OK 😐**: 31-60 seconds (acceptable performance)  
- **Slow 😴**: 61-119 seconds (functional but slow)
- **TIMEOUT ❌**: ≥120 seconds (automatic FAIL)

### CLI-Specific Expected Performance

- **Target Distribution**: Majority Good 😊 and OK 😐 classifications (CLI inherently faster than MCP)
- **Average Execution**: ~48 seconds per test based on historical CLI data
- **Performance Advantage**: CLI method typically faster than MCP browser automation

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
- Mark each test as in_progress before CLI execution
- Mark each test as completed after successful CLI execution
- Never claim completion without actual CLI test execution

---