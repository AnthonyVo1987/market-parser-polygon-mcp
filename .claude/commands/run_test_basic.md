# Run Test Basic Slash Command

Execute Basic Tests using AI Team orchestration with the @agent-tech-lead-orchestrator.

**Testing Focus:** Run ONLY the Basic Tests as defined in the official test specifications. NO custom test creation allowed.

## How to Use

1. **Ensure servers are running** (FastAPI backend + React frontend)
2. **Run this command**: `/run_test_basic`
3. **Follow the orchestrated plan** as specialists execute the Basic Tests

## What This Command Does

When you invoke `/run_test_basic`, I will:

1. **Invoke @agent-tech-lead-orchestrator** to analyze the Basic Testing requirements and create a specialist assignment plan
2. **Execute the Basic Tests** using the exact agents recommended by the tech-lead
3. **Enforce official test specifications** reading from `gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`
4. **Ensure MCP tool compliance** for all specialists
5. **Generate test reports** and commit results WITHOUT attempting to fix any failures

## Command Execution

I'll use @agent-tech-lead-orchestrator to analyze the Basic Testing requirements and assign the appropriate specialists from the available AI Team:

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

When Basic Tests are requested, specialists MUST read the official test plan from:
`gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`

**Basic Tests Definition**:
- **Market Status Tests**: System response to market status requests
- **Single Ticker Tests**: Individual ticker snapshot requests (NVDA, SPY, GME)  
- **Multi-Ticker Tests**: Combined multiple ticker requests

**Failure to follow the official test plan invalidates all test results.**

## MCP Tool Requirements

**ALL specialist agents MUST use MCP tools:**

- `mcp__sequential-thinking__sequentialthinking` - For systematic analysis
- `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` - For research
- `mcp__filesystem__*` - For efficient file operations
- `mcp__playwright__*` - For all browser testing operations

**Testing-specific MCP usage:**

- Testing agents MUST use `mcp__playwright__browser_navigate`, `mcp__playwright__browser_click`, `mcp__playwright__browser_type`, etc.
- ALL browser operations must use MCP playwright tools
- File operations for test reports must use `mcp__filesystem__write_file`

**Failure to use required MCP tools will result in work rejection.**

---

## Execution Protocol - Basic Testing A-I Workflow

The `/run_test_basic` command follows a systematic A-I process with tech-lead orchestration for Basic Tests execution.

### A-I Workflow Steps

**A. User Invokes `/run_test_basic`**

- User triggers Basic Tests execution via `/run_test_basic` command
- Command scope: Execute ONLY Basic Tests as defined in official test specifications

**B. Main Agent uses @agent-tech-lead-orchestrator (MANDATORY)**

- Tech-lead analyzes Basic Testing requirements from official test specifications
- Systematic evaluation of server requirements and testing specialist assignment planning
- Must enforce reading `gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`

**C. Server Verification Phase**

- Tech-lead assigns specialist to verify MANDATORY server startup requirements
- **FastAPI Backend**: Must show "Application startup complete." on http://0.0.0.0:8000
- **React Frontend**: Must show "VITE ready" on auto-selected port (3000→3003, etc.)
- **Health Checks**: Both servers must respond to health check requests
- **CORS Configuration**: Verify cross-origin requests work properly

**D. Basic Testing Execution Phase**

- Specialist(s) execute Basic Tests using MCP playwright tools
- **Single Browser Session**: ALL tests execute in SAME browser instance 
- **30-Second Polling**: Use polling methodology for accurate timeout detection
- **Performance Classification**: Record SUCCESS/SLOW_PERFORMANCE/TIMEOUT for each test
- **Coverage-First**: Continue ALL tests even if early tests fail

**E. Testing Methodology Enforcement**

- Specialist MUST follow official test specifications exactly
- Use "PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity" for all test queries
- Accept ANY response format (JSON, emojis, conversational) - emojis are ENCOURAGED
- NO custom test creation - only execute Basic Tests as officially defined

**F. Test Report Generation - Final Task 1**

- Generate comprehensive Basic Tests execution report with performance data
- Include polling methodology results and performance classifications
- Document any failures with detailed analysis but DO NOT attempt to fix them
- Save report using `mcp__filesystem__write_file`

**G. Task Summary & CLAUDE.md Update - Final Task 2**

- Generate comprehensive Basic Tests Summary → overwrite `LAST_TASK_SUMMARY.md`
- Generate MAX 20-line high-level overview → update CLAUDE.md task summary section
- Include all test results, performance data, and completion status for atomic commit

**H. Atomic Git Commit & Push - Final Task 3**

- PRIMARY: Use `git` for atomic operations
- Single atomic commit containing ALL changes:
  - Test report files
  - Documentation updates  
  - CLAUDE.md updates
  - LAST_TASK_SUMMARY.md updates
- **CRITICAL**: Must push to complete workflow - commit without push is incomplete

**I. Final Verification - Final Task 4**

- Run final verification to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all test reports and changes are properly committed and pushed to GitHub

### 🚨 CRITICAL: Server Startup Requirements (MANDATORY)

**BOTH SERVERS MUST BE RUNNING BEFORE ANY TEST EXECUTION**:

1. **FastAPI Backend Server**:
```bash
cd gpt5-openai-agents-sdk-polygon-mcp
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

2. **React Frontend Server**:
```bash
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm run dev
```

**⚠️ FAILURE TO START SERVERS = AUTOMATIC TEST FAILURE**

### Basic Testing Principles Enforcement

- **Official Test Specifications ONLY**: No custom tests - follow Basic Tests exactly as documented
- **Single Browser Session**: ALL Basic tests execute in SAME browser instance for real-world simulation
- **30-Second Polling**: Use polling methodology to distinguish slow performance from timeouts
- **Coverage-First**: Execute all Basic tests regardless of individual failures
- **NO FIX ATTEMPTS**: Document failures but do not attempt to fix issues - testing only
- **Performance Classification**: Record accurate timing data and performance classifications

### Quality Requirements

- Tech-lead orchestrator MANDATORY for Basic Testing coordination
- MCP tools as PRIMARY method for all specialist testing operations
- Official test specifications compliance enforced
- Atomic commit principle: ALL changes in single commit operation
- Test report generation with polling data and performance insights

---

## 🚨 CRITICAL: Testing Execution Protocol

### Single Browser Session Testing (ENFORCED)

**✅ CORRECT METHODOLOGY**:
```
Single Browser Session: Browser Start → All Basic Tests → Browser End
```

**❌ PROHIBITED METHODOLOGY**:
```
❌ Browser → Test → Close → Browser → Test → Close → etc.
❌ Fresh browser state between any Basic tests
```

### Official Test Queries (ENFORCED)

**Market Status Query Pattern**: "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"

**Single Ticker Query Pattern**: "Single Ticker Snapshot: [TICKER], PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
- Example tickers: NVDA, SPY, GME

**Multi-Ticker Query Pattern**: "Full Market Snapshot with multiple Tickers: [TICKER_LIST]: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
- Example ticker list: NVDA, SPY, QQQ, IWM

### Response Format Requirements

- **ANY FORMAT ACCEPTABLE**: JSON, text with emojis, conversational responses
- **EMOJIS ENCOURAGED**: 📈📉💰💸 for financial sentiment indicators
- **BASIC FUNCTIONALITY FOCUS**: Verify system responds appropriately to requests
- **NO JSON-ONLY ENFORCEMENT**: Accept any readable response format

### Timeout and Performance Configuration

- **Individual Test Timeout**: 120 seconds maximum
- **Polling Interval**: 30 seconds for completion detection
- **Performance Classifications**: SUCCESS (<45s), SLOW_PERFORMANCE (45-120s), TIMEOUT (>120s)
- **Early Completion**: Stop polling immediately when response received

---