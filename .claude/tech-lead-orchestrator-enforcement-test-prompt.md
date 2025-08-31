# Tech-Lead-Orchestrator Enforcement Test Prompt

**COPY AND PASTE THIS TEMPLATE FOR ANY TASK REQUIRING PROPER TECH-LEAD ORCHESTRATION**

---

## MANDATORY PROTOCOL ENFORCEMENT

**YOU ARE PROHIBITED FROM PERFORMING ANY IMPLEMENTATION WORK.** 

Your ONLY role is orchestration through THREE MANDATORY PHASES. Any deviation results in IMMEDIATE TASK FAILURE.

### CRITICAL VIOLATION CONSEQUENCES
- ❌ **If you write code** → TASK FAILED
- ❌ **If you create files directly** → TASK FAILED  
- ❌ **If you provide summaries instead of deliverables** → TASK FAILED
- ❌ **If you skip MCP tool enforcement** → TASK FAILED
- ❌ **If you don't follow three-phase workflow** → TASK FAILED

---

## PHASE 1: RESEARCH (MANDATORY)

**STEP 1.1: Invoke Tech-Lead-Orchestrator**
```
Use @tech-lead-orchestrator to analyze the following task: [INSERT TASK DESCRIPTION]
```

**STEP 1.2: Validate Tech-Lead Response**
MUST contain ALL of these elements or REJECT and retry:
- ✅ Task Analysis (2-3 bullets)
- ✅ Technology stack detected
- ✅ Agent Assignments (numbered tasks → exact @agent-names)
- ✅ Execution Order (parallel/sequential)
- ✅ Available Agents list from system context
- ✅ Instructions to Main Agent

**STEP 1.3: Present Research Findings**
Present tech-lead's findings to user and state:
"Research phase complete. Proceeding to Planning phase with the following agent assignments: [list exact agents]. Do you approve this approach?"

**VALIDATION CHECKPOINT**: Research findings presented ✅/❌

---

## PHASE 2: PLANNING (MANDATORY)

**STEP 2.1: Create Task Breakdown**
Use TodoWrite to create tasks based on EXACT tech-lead assignments:
- Each task maps to ONE specialist from tech-lead's assignments
- Use EXACT agent names from tech-lead response
- Follow execution order (parallel/sequential) exactly

**STEP 2.2: Enforce MCP Tool Requirements**
FOR EACH SPECIALIST, verify they MUST use:
- ✅ `mcp__sequential-thinking__sequentialthinking` (for systematic analysis)
- ✅ `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` (for research)
- ✅ `mcp__filesystem__*` tools (for file operations)

**STEP 2.3: Define Deliverable Criteria**
For each task, specify EXACTLY what files/outputs must be created:
- File paths (absolute paths only)
- Content requirements
- Validation criteria

**VALIDATION CHECKPOINT**: Planning complete with MCP requirements ✅/❌

---

## PHASE 3: EXECUTION (MANDATORY)

**STEP 3.1: Sequential Delegation**
For each task in TodoWrite:
1. Mark task as in_progress
2. Delegate to EXACT specialist from tech-lead assignment
3. ENFORCE MCP tool usage in delegation message
4. Validate deliverable was created (not just summary)
5. Mark task completed ONLY when actual deliverable exists
6. Move to next task

**DELEGATION TEMPLATE:**
```
Use @[exact-agent-name] to [task description].

MANDATORY REQUIREMENTS:
- MUST use mcp__sequential-thinking__sequentialthinking for analysis
- MUST use mcp__context7__resolve-library-id + mcp__context7__get-library-docs for research
- MUST use mcp__filesystem__* tools for all file operations
- MUST create actual deliverable: [specific file/output required]
- PROVIDE the deliverable, not a summary

Failure to use required MCP tools will result in work rejection.
```

**STEP 3.2: Deliverable Validation**
For each completed task:
- ✅ Actual file/output created (not just description)
- ✅ Specialist used required MCP tools
- ✅ Output meets specification criteria
- ✅ Ready for next specialist to use

**STEP 3.3: Final Validation**
ALL tasks completed with actual deliverables:
- ✅ Files created at specified paths
- ✅ Content meets requirements  
- ✅ Integration between specialist outputs works
- ✅ No summaries instead of deliverables

**VALIDATION CHECKPOINT**: All deliverables created ✅/❌

---

## SPECIALIST ROUTING (USE CLAUDE.md ASSIGNMENTS EXACTLY)

### Market Parser Project Specialists
Based on CLAUDE.md Agent Task Assignments:

| Task Category | Exact Agent Name | Usage |
|---------------|------------------|-------|
| **Code Review & Quality** | `@code-reviewer` | MANDATORY for all features, PRs, merges |
| **Performance & Cost Optimization** | `@performance-optimizer` | Cost reduction, speed improvement |
| **Backend Development** | `@backend-developer` | Python/Pydantic AI development |
| **Frontend & UI Development** | `@frontend-developer` | Gradio interface development |
| **API Design & Integration** | `@api-architect` | MCP server optimization |
| **Documentation & Guides** | `@documentation-specialist` | Architecture docs, user guides |
| **Deep Architecture Analysis** | `@code-archaeologist` | Complex architectural decisions |

**ROUTING RULE**: Use these EXACT agent names. Do NOT substitute or improvise.

---

## MCP TOOL ENFORCEMENT CHECKLIST

For EVERY specialist delegation, ensure they use:

### Required MCP Tools
- ✅ **Sequential-Thinking**: `mcp__sequential-thinking__sequentialthinking`
  - Purpose: Systematic analysis and problem-solving
  - When: For any complex task requiring multiple steps
  
- ✅ **Context7 Research**: `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs`
  - Purpose: Up-to-date documentation and library research
  - When: Working with external libraries or frameworks
  
- ✅ **Filesystem Operations**: `mcp__filesystem__*` (read, write, edit, list, etc.)
  - Purpose: Efficient and correct file operations
  - When: Any task involving file creation/modification

### Enforcement Message Template
```
CRITICAL: You MUST use the following MCP tools for this task:
1. mcp__sequential-thinking__sequentialthinking for systematic analysis
2. mcp__context7__* tools for library research if needed  
3. mcp__filesystem__* tools for all file operations

Failure to use these tools will result in work rejection and task restart.
```

---

## EXAMPLE USAGE

### Task: "Add user authentication to the market parser application"

**PHASE 1: RESEARCH**
```
Use @tech-lead-orchestrator to analyze the following task: Add user authentication to the market parser application with secure session management and role-based access control.
```

*Tech-lead responds with agent assignments and execution plan*

Present findings: "Research complete. Tech-lead recommends using @backend-developer for authentication logic, @api-architect for secure endpoints, @frontend-developer for login UI, and @code-reviewer for security validation. Proceed?"

**PHASE 2: PLANNING**
*Create TodoWrite with tasks mapped to exact specialists*

**PHASE 3: EXECUTION**
```
Use @backend-developer to implement user authentication models and session management.

MANDATORY REQUIREMENTS:
- MUST use mcp__sequential-thinking__sequentialthinking for analysis
- MUST use mcp__context7__resolve-library-id + mcp__context7__get-library-docs for research
- MUST use mcp__filesystem__* tools for file operations
- MUST create actual deliverable: Authentication models in src/auth/models.py
- PROVIDE the deliverable, not a summary
```

*Continue for each specialist until all deliverables created*

---

## FAILURE DETECTION

### Signs of Protocol Violation
- ❌ "I'll implement..." (should be "I'll delegate to...")
- ❌ "Here's a summary of what was done" (should be actual files)
- ❌ Using generic agent names not from CLAUDE.md
- ❌ Skipping MCP tool enforcement
- ❌ Missing deliverable validation
- ❌ Providing status reports instead of outputs

### Recovery Protocol
If violations detected:
1. STOP execution immediately
2. Restart from PHASE 1
3. Re-read this protocol
4. Ensure strict compliance

---

## SUCCESS CRITERIA

### Task Complete When ALL True:
- ✅ Three-phase workflow followed exactly
- ✅ Tech-lead-orchestrator used for research phase
- ✅ All specialists used exact names from CLAUDE.md
- ✅ MCP tools enforced for every specialist
- ✅ Actual deliverables created (not summaries)
- ✅ Files exist at specified absolute paths
- ✅ Integration between specialist outputs works
- ✅ Final validation passed

### Final Deliverable Report Format:
```
## ORCHESTRATION COMPLETE

### Phase Results:
- ✅ RESEARCH: Tech-lead analysis completed
- ✅ PLANNING: Task breakdown with MCP enforcement  
- ✅ EXECUTION: All specialists completed with deliverables

### Created Deliverables:
- [Absolute file path 1]: [Description]
- [Absolute file path 2]: [Description]
- [etc...]

### Specialist Contributions:
- @[agent-name]: [Specific deliverable created]
- @[agent-name]: [Specific deliverable created]

### Validation Status:
- ✅ All files created successfully
- ✅ MCP tools used by all specialists
- ✅ Integration validated
- ✅ Ready for use
```

---

**REMEMBER: Your role is ORCHESTRATION ONLY. Never implement. Always delegate. Always validate deliverables.**

---

## TEMPLATE USAGE INSTRUCTIONS

1. **Copy this entire prompt** for any multi-step task
2. **Insert your task description** in Phase 1, Step 1.1
3. **Follow the phases sequentially** - no skipping
4. **Enforce MCP tools** for every specialist
5. **Validate deliverables** at each checkpoint
6. **Use exact agent names** from CLAUDE.md assignments

This protocol ensures proper tech-lead orchestration and prevents the implementation/summary failures we've experienced.