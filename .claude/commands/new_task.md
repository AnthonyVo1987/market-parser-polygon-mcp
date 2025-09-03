# New Task Slash Command

Execute complex development tasks using AI Team orchestration with the tech-lead-orchestrator.

## How to Use

1. **Edit task details** in `/home/anthony/Github/market-parser-polygon-mcp/new_task_details.md`
2. **Run this command**: `/new_task`
3. **Follow the orchestrated plan** as specialists complete each task

## What This Command Does

When you invoke `/new_task`, I will:

1. **Read your task details** from `new_task_details.md`
2. **Invoke @tech-lead-orchestrator** to analyze the task and create a specialist assignment plan
3. **Execute the plan** using the exact agents recommended by the tech-lead
4. **Ensure MCP tool compliance** for all specialists
5. **Create actual deliverables** (not just summaries)

## Command Execution

I'll read the task details from new_task_details.md and use @tech-lead-orchestrator to analyze the requirements and assign the appropriate specialists from the available AI Team:

**Available Specialists (per CLAUDE.md):**

| Task Category | Agent | Responsibilities | Notes |
|---------------|-------|------------------|-------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, merges. Security-aware reviews, quality assurance for both Python and React code | Required for all development work |
| **Python Backend Development** | `@backend-developer` | Python/Pydantic AI development, FSM management, dual-mode processing, MCP server integration, backend API design | Primary architect for Python application logic |
| **React Frontend Architecture** | `@react-component-architect` | React component design, Next.js 14+ architecture, modern React patterns, component library integration | Leads React frontend development and component architecture |
| **API Design & Integration** | `@api-architect` | Backend-Frontend API contracts, RESTful API design, response schema design, integration patterns | Ensures clean data flow between Python backend and React frontend |
| **Documentation & Architecture** | `@documentation-specialist` | Architecture documentation, user guides, API documentation, component documentation, migration planning | Maintains comprehensive project documentation |
| **Deep Analysis & Planning** | `@code-archaeologist` | Complex architectural decisions, system analysis, migration strategy, technical debt assessment | On-demand for major architectural changes and system analysis |

**MCP Tool Requirements:**
All specialists MUST use:

- `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` for research
- `mcp__filesystem__*` tools for all file operations

---

## Execution Protocol

I'll read the task from new_task_details.md, then use @tech-lead-orchestrator to get proper agent assignments and execute the plan with those exact specialists, ensuring all MCP tools are used and actual deliverables are created. Upon task completion, I will execute the mandatory post-task actions outlined below.

---

## MANDATORY POST-TASK ACTIONS

After completing the primary task execution, the following 4-step procedure MUST be executed to ensure production readiness and quality assurance:

### Step 1: Code Review & Quality Validation (@code-reviewer)
**MANDATORY EXECUTION - NO EXCEPTIONS**

**Primary Responsibilities:**
- Comprehensive security-aware code review of all modified files
- Performance impact assessment for new implementations
- Testing validation (all existing tests must pass, new tests required)
- Code quality standards compliance (PEP 8, type hints, documentation)
- MCP tool compliance verification for all specialist work
- GitHub integration readiness check

**Required MCP Tools:**
- `mcp__sequential-thinking__sequentialthinking` for systematic review analysis
- `mcp__filesystem__read_multiple_files` for efficient multi-file review
- `mcp__filesystem__get_file_info` for change impact assessment

**Validation Criteria:**
- All tests pass (`uv run pytest tests/`)
- No security vulnerabilities detected
- Code coverage maintained or improved
- Performance benchmarks meet targets
- Documentation completeness verified

**Error Handling:**
- If validation fails, halt deployment and create remediation tasks
- Document all issues in GitHub issue format
- Require fixes before proceeding to Step 2

### Step 2: Performance & Security Assessment (@performance-optimizer)
**MANDATORY EXECUTION - PRODUCTION CRITICAL**

**Primary Responsibilities:**
- 35% cost reduction target validation (token usage optimization)
- 40% speed improvement confirmation (processing time benchmarks)
- Security vulnerability scanning and mitigation
- Resource optimization verification (memory, CPU, I/O)
- Performance regression testing
- Cost monitoring configuration updates

**Required MCP Tools:**
- `mcp__sequential-thinking__sequentialthinking` for performance analysis
- `mcp__filesystem__read_text_file` for performance test results
- `mcp__context7__get-library-docs` for optimization research

**Validation Criteria:**
- Performance targets met or exceeded
- Security scan shows no critical vulnerabilities
- Resource usage within acceptable limits
- Cost tracking properly configured
- Benchmark results documented

**Error Handling:**
- Performance failures require immediate optimization
- Security issues block deployment
- Resource problems need architectural review
- All issues logged with remediation timeline

### Step 3: Documentation & Architecture Update (@documentation-specialist)
**MANDATORY EXECUTION - KNOWLEDGE PRESERVATION**

**Primary Responsibilities:**
- Architecture documentation updates (CLAUDE.md modifications)
- API documentation refresh (if applicable)
- User guide modifications for new features
- Change log maintenance with detailed entries
- Migration guide updates (if breaking changes)
- README updates for new functionality

**Required MCP Tools:**
- `mcp__sequential-thinking__sequentialthinking` for documentation planning
- `mcp__filesystem__read_multiple_files` for documentation consistency
- `mcp__filesystem__edit_file` for documentation updates

**Validation Criteria:**
- All documentation reflects current implementation
- API docs match actual endpoints/responses
- User guides include new feature coverage
- Change log properly formatted and comprehensive
- No broken internal documentation links

**Error Handling:**
- Documentation gaps require immediate updates
- Inconsistencies between docs and code must be resolved
- Missing user guides block feature release
- All documentation validated before Step 4

### Step 4: Integration Validation & Deployment Readiness
**MANDATORY EXECUTION - FINAL VERIFICATION**

**Primary Responsibilities:**
- End-to-end workflow validation (CLI + Web GUI)
- Environment compatibility verification (dev/staging/prod)
- Deployment script validation and testing
- Rollback procedure confirmation and documentation
- Production readiness assessment checklist
- GitHub repository state verification

**Required Tools & Access:**
- GitHub access token for repository operations
- All MCP filesystem tools for comprehensive validation
- Test environment access for integration testing

**Validation Criteria:**
- All integration tests pass
- Deployment scripts execute without errors
- Rollback procedures tested and documented
- Environment variables properly configured
- GitHub repository clean and ready for release

**Error Handling:**
- Integration failures require immediate investigation
- Deployment issues block release
- Rollback problems need resolution before deployment
- Environment misconfigurations must be corrected

---

## POST-TASK EXECUTION REQUIREMENTS

**Mandatory Completion:**
- ALL 4 steps must complete successfully
- Each step requires explicit sign-off from assigned agent
- Failures in any step halt the deployment process
- All validation criteria must be met before proceeding

**MCP Tool Compliance:**
- Every agent MUST use required MCP tools
- Non-compliance results in work rejection
- Systematic thinking required for all complex decisions
- File operations must use mcp__filesystem__* tools

**GitHub Integration:**
- Valid GitHub access token required for repository operations
- All changes must be committed with proper commit messages
- Issues created for any validation failures
- Repository state verified before final approval

**Quality Gates:**
- Code review approval (Step 1) required before performance testing
- Performance validation (Step 2) required before documentation
- Documentation updates (Step 3) required before final validation
- Integration validation (Step 4) required before deployment approval

---

## EMERGENCY PROCEDURES

**Critical Failure Handling:**
- If any step fails critically, immediately halt all subsequent steps
- Create GitHub issues for all failures with detailed error information
- Notify user of failure status and required remediation actions
- Do not proceed until all issues are resolved and re-validated

**Rollback Requirements:**
- All changes must be easily reversible
- Rollback procedures tested as part of Step 4
- Emergency rollback contact and procedures documented
- Recovery time objectives (RTO) defined and tested
