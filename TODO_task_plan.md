# 🔴 REVISED IMPLEMENTATION PLAN: Persistent Agent Architecture (Following b866f0a Principle)

## 🎯 ARCHITECTURE PRINCIPLE (from Commit b866f0a)

**Core Principle:** CLI = Single Source of Truth, GUI = Wrapper (Zero Duplication)

**Commit b866f0a Pattern:**
- ✅ Backend generates markdown (ONE place)
- ✅ CLI renders it with Rich
- ✅ GUI renders it with react-markdown
- ✅ No duplicate formatting code

**Applying Same Principle to Agent Persistence:**
- ✅ CLI creates persistent agent logic (ONE place)
- ✅ CLI mode uses it directly
- ✅ GUI mode calls CLI functions (no duplication)
- ✅ No duplicate agent creation code

---

## 📋 RESEARCH FINDINGS (CORRECTED)

### ✅ OpenAI Agents SDK Best Practices

**CORRECT Pattern:**
```python
# Create agent ONCE
agent = Agent(name="Assistant", instructions="...")
session = SQLiteSession("conversation_123")

# REUSE agent for all messages
result = await Runner.run(agent, "First message", session=session)
result = await Runner.run(agent, "Second message", session=session)
```

### ❌ Current Implementation (WRONG - Code Duplication)

**CLI (`src/backend/cli.py:76`):**
```python
async def _process_user_input(cli_session, user_input):
    analysis_agent = create_agent()  # ❌ DUPLICATE AGENT CREATION
    result = await Runner.run(analysis_agent, user_input, session=cli_session)
```

**GUI (`src/backend/routers/chat.py:80`):**
```python
async def chat_endpoint(request: ChatRequest):
    analysis_agent = create_agent()  # ❌ DUPLICATE AGENT CREATION
    result = await Runner.run(analysis_agent, stripped_message, session=shared_session)
```

**Problem:** Same agent creation and running logic in TWO places (violates b866f0a principle)

---

## 🔧 CORRECT ARCHITECTURE SOLUTION

### Execution Model (from main.py)

```python
# main.py
if __name__ == "__main__":
    if sys.argv[1] == "--server":
        # FastAPI mode: uvicorn.run(app)
    else:
        # CLI mode: asyncio.run(cli_async())
```

**Key Insight:** CLI and FastAPI are **mutually exclusive** - never run simultaneously.

### ✅ Revised Architecture (Zero Duplication)

```
┌─────────────────────────────────────────────────────────────┐
│ CLI Module (src/backend/cli.py) - SINGLE SOURCE OF TRUTH   │
│ ─────────────────────────────────────────────────────────── │
│ • initialize_persistent_agent() → Creates agent ONCE       │
│ • process_query(agent, session, input) → Core logic        │
└─────────────────────────────────────────────────────────────┘
         ↓                                  ↓
    ┌─────────┐                        ┌─────────┐
    │ CLI Mode│                        │ GUI Mode│
    │─────────│                        │─────────│
    │ Creates │                        │ Imports │
    │ agent   │                        │ CLI     │
    │ Calls   │                        │ Calls   │
    │ process │                        │ process │
    │ Prints  │                        │ Returns │
    │ output  │                        │ HTTP    │
    └─────────┘                        └─────────┘
```

**Key Changes:**
1. ✅ ONE `initialize_persistent_agent()` function in CLI (not duplicated)
2. ✅ ONE `process_query()` function in CLI (core business logic)
3. ✅ GUI router **imports and calls** CLI functions (no duplication)
4. ✅ Each mode creates its own agent instance using shared initialization
5. ✅ Zero code duplication (follows b866f0a principle)

---

## 📝 DETAILED TASK CHECKLIST

### 🔴 PHASE 1: RESEARCH ✅ COMPLETED

- [x] Research OpenAI Agents SDK persistence patterns
- [x] Analyze commit b866f0a architecture principle
- [x] Identify code duplication in CLI and GUI
- [x] Understand main.py execution model (CLI vs FastAPI modes)
- [x] Confirm GUI should call CLI functions (not duplicate logic)

---

### 🔴 PHASE 2: PLANNING ✅ IN PROGRESS

- [x] Revise implementation plan following b866f0a principle
- [x] Document CLI as single source of truth
- [x] Define shared functions approach (no duplication)
- [ ] Review plan for completeness before implementation

---

### 🔴 PHASE 3: IMPLEMENTATION

**🔴 CRITICAL: You MUST use Sequential-Thinking + Serena Tools for ALL tasks**

---

#### Task 3.1: Create Shared Agent Initialization in CLI
**File:** `src/backend/cli.py`
**Tool Requirement:** Serena `insert_after_symbol` or `insert_before_symbol`

**Actions:**
1. [ ] **Sequential-Thinking:** Plan new shared functions in CLI
2. [ ] **Serena `get_symbols_overview`:** Analyze current CLI structure
3. [ ] **Serena `insert_before_symbol`:** Add `initialize_persistent_agent()` function
4. [ ] Create function: `def initialize_persistent_agent() -> Agent`
5. [ ] Function calls `create_agent()` and returns agent instance
6. [ ] Add docstring explaining this is the single source of truth
7. [ ] **Sequential-Thinking:** Verify function placement and design

**Expected New Function:**
```python
def initialize_persistent_agent():
    """Initialize persistent agent for the session.

    This is the SINGLE SOURCE OF TRUTH for agent initialization.
    Both CLI and GUI modes use this function to create their agent instance.

    Returns:
        Agent: The initialized financial analysis agent
    """
    return create_agent()
```

---

#### Task 3.2: Create Shared Query Processing in CLI
**File:** `src/backend/cli.py`
**Tool Requirement:** Serena `insert_after_symbol`

**Actions:**
1. [ ] **Sequential-Thinking:** Plan shared query processing function
2. [ ] **Serena `insert_after_symbol`:** Add after `initialize_persistent_agent()`
3. [ ] Create function: `async def process_query(agent, session, user_input)`
4. [ ] Function runs `Runner.run()` and returns result
5. [ ] Function is pure business logic (no CLI-specific formatting)
6. [ ] Add docstring explaining this is core processing logic
7. [ ] **Sequential-Thinking:** Verify function signature and return value

**Expected New Function:**
```python
async def process_query(agent, session, user_input):
    """Process a user query using the persistent agent.

    This is the CORE BUSINESS LOGIC for query processing.
    Both CLI and GUI modes call this function (no duplication).

    Args:
        agent: The persistent agent instance
        session: The SQLite session for conversation memory
        user_input: The user's query string

    Returns:
        RunResult: The result from Runner.run()
    """
    result = await Runner.run(agent, user_input, session=session)
    return result
```

---

#### Task 3.3: Update CLI Mode to Use Shared Functions
**File:** `src/backend/cli.py`
**Tool Requirement:** Serena `replace_symbol_body` for multiple functions

**Actions:**
1. [ ] **Sequential-Thinking:** Plan CLI mode modifications
2. [ ] **Serena `find_symbol`:** Read `cli_async` function body
3. [ ] **Serena `replace_symbol_body`:** Modify `cli_async()`:
   - Create agent: `analysis_agent = initialize_persistent_agent()`
   - Pass agent to: `await _run_cli_loop(cli_session, analysis_agent)`
4. [ ] **Serena `find_symbol`:** Read `_run_cli_loop` function body
5. [ ] **Serena `replace_symbol_body`:** Add `analysis_agent` parameter
6. [ ] Update `_process_user_input()` call to pass agent
7. [ ] **Serena `find_symbol`:** Read `_process_user_input` function body
8. [ ] **Serena `replace_symbol_body`:** Modify `_process_user_input()`:
   - Add `analysis_agent` parameter
   - Remove `analysis_agent = create_agent()` line
   - Call: `result = await process_query(analysis_agent, cli_session, user_input)`
   - Keep metadata and error handling (CLI-specific wrapper)

**Expected Changes:**
```python
# cli_async() - Create agent once
async def cli_async():
    try:
        cli_session = SQLiteSession(settings.cli_session_name)
        analysis_agent = initialize_persistent_agent()  # ← SHARED FUNCTION
        print(f"🤖 Persistent agent initialized for session")

        await _run_cli_loop(cli_session, analysis_agent)  # ← Pass agent

# _run_cli_loop() - Pass agent through
async def _run_cli_loop(cli_session, analysis_agent):  # ← Add parameter
    while True:
        # ... input handling ...
        result = await _process_user_input(cli_session, analysis_agent, user_input)

# _process_user_input() - Use shared processing function
async def _process_user_input(cli_session, analysis_agent, user_input):  # ← Add parameter
    try:
        start_time = time.perf_counter()

        # REMOVE: analysis_agent = create_agent()  ← DELETE

        # Call shared processing function (core logic)
        result = await process_query(analysis_agent, cli_session, user_input)  # ← SHARED

        # CLI-specific metadata and formatting (keep this)
        processing_time = time.perf_counter() - start_time
        token_count = extract_token_count_from_context_wrapper(result)
        # ... rest of CLI-specific code ...
```

---

#### Task 3.4: Update GUI to Import and Use CLI Functions
**File:** `src/backend/routers/chat.py`
**Tool Requirement:** Serena `replace_symbol_body` for `chat_endpoint`

**Actions:**
1. [ ] **Sequential-Thinking:** Plan GUI router modifications
2. [ ] **Serena `find_symbol`:** Read `chat_endpoint` function body
3. [ ] Add imports: `from ..cli import initialize_persistent_agent, process_query`
4. [ ] **Serena `replace_symbol_body`:** Modify `chat_endpoint()`:
   - Remove `from ..services import create_agent` import (no longer needed)
   - Remove `analysis_agent = create_agent()` line
   - Get shared agent: `shared_agent = get_agent()` (from dependency)
   - Call: `result = await process_query(shared_agent, shared_session, stripped_message)`
   - Keep HTTP response wrapper (GUI-specific)
5. [ ] **Serena `find_referencing_symbols`:** Verify no other `create_agent()` calls

**Expected Changes:**
```python
# routers/chat.py - Import CLI functions
from ..cli import process_query  # ← IMPORT SHARED FUNCTION
from ..dependencies import get_session, get_agent  # ← Add get_agent

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    # Get shared resources
    shared_session = get_session()
    shared_agent = get_agent()  # ← Get agent from dependency

    # ... validation code (keep as-is) ...

    try:
        # REMOVE: analysis_agent = create_agent()  ← DELETE

        # Call shared processing function (core logic from CLI)
        result = await process_query(shared_agent, shared_session, stripped_message)  # ← SHARED

        response_text = str(result.final_output)

        # GUI-specific HTTP response wrapper (keep this)
        token_usage = extract_token_usage_from_context_wrapper(result)
        # ... rest of HTTP response code ...
```

---

#### Task 3.5: Update Dependencies for Shared Agent
**File:** `src/backend/dependencies.py`
**Tool Requirement:** Serena `insert_after_symbol` and `replace_symbol_body`

**Actions:**
1. [ ] **Sequential-Thinking:** Plan dependency injection for agent
2. [ ] **Serena `get_symbols_overview`:** Analyze dependencies structure
3. [ ] **Serena `find_symbol`:** Read `set_shared_resources` function
4. [ ] Add global: `shared_agent = None`
5. [ ] **Serena `replace_symbol_body`:** Update `set_shared_resources(session, agent)`
6. [ ] **Serena `insert_after_symbol`:** Add `get_agent()` function after `get_session()`

**Expected Changes:**
```python
# dependencies.py
shared_session = None
shared_agent = None  # ← ADD

def set_shared_resources(session, agent):  # ← Add agent parameter
    global shared_session, shared_agent
    shared_session = session
    shared_agent = agent  # ← ADD

def get_agent():  # ← NEW FUNCTION
    """Dependency to get shared agent instance."""
    if shared_agent is None:
        raise RuntimeError("Shared agent not initialized")
    return shared_agent
```

---

#### Task 3.6: Update FastAPI Lifespan for Shared Agent
**File:** `src/backend/main.py`
**Tool Requirement:** Serena `replace_symbol_body` for `lifespan`

**Actions:**
1. [ ] **Sequential-Thinking:** Plan lifespan modifications
2. [ ] Add import: `from .cli import initialize_persistent_agent`
3. [ ] Add global: `shared_agent = None`
4. [ ] **Serena `find_symbol`:** Read `lifespan` function body
5. [ ] **Serena `replace_symbol_body`:** Modify `lifespan()`:
   - Create agent: `shared_agent = initialize_persistent_agent()`
   - Update: `set_shared_resources(shared_session, shared_agent)`

**Expected Changes:**
```python
# main.py
from .cli import initialize_persistent_agent  # ← IMPORT SHARED FUNCTION

shared_session = None
shared_agent = None  # ← ADD

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    global shared_session, shared_agent  # ← ADD

    try:
        shared_session = SQLiteSession(settings.agent_session_name)
        shared_agent = initialize_persistent_agent()  # ← SHARED FUNCTION

        set_shared_resources(shared_session, shared_agent)  # ← ADD agent param
```

---

#### Task 3.7: Update Agent Instructions (Adaptive Formatting)
**File:** `src/backend/services/agent_service.py`
**Tool Requirement:** Serena `find_symbol` + `replace_symbol_body`

**Actions:**
1. [ ] **Sequential-Thinking:** Plan adaptive formatting instructions
2. [ ] **Serena `find_symbol`:** Read `get_enhanced_agent_instructions` function body
3. [ ] **Sequential-Thinking:** Determine best location in prompt
4. [ ] **Serena `replace_symbol_body`:** Add adaptive formatting guidance

**Expected Instructions Addition:**
```
**Adaptive Output Formatting:**
- For SIMPLE responses (few data points, quick answers): Use numbered or bulleted lists for speed and clarity
- For COMPLEX responses (extensive data, options chains, comparisons): Use markdown tables for better readability
- Let data complexity guide your formatting choice—prioritize user experience and clear presentation
```

---

### 🔴 PHASE 4: TESTING (MANDATORY CHECKPOINT)

**🔴 CRITICAL: You MUST run tests BEFORE claiming completion**

#### Task 4.1: Execute CLI Regression Test Suite

**Actions:**
1. [ ] **Sequential-Thinking:** Review what testing will validate
2. [ ] Execute: `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
3. [ ] Verify 100% pass rate
4. [ ] Verify test report generated
5. [ ] Check for errors or warnings
6. [ ] **Sequential-Thinking:** Analyze results and performance

**Success Criteria:**
- ✅ All tests pass (X/X PASS - 100%)
- ✅ Response times within baseline (< 15s avg)
- ✅ No errors or exceptions
- ✅ Agent persistence working
- ✅ Adaptive formatting visible

**If Tests Fail:**
1. [ ] **Sequential-Thinking:** Analyze failures
2. [ ] Use Serena tools to fix bugs
3. [ ] Re-run tests until 100% pass
4. [ ] Do NOT proceed until tests pass

---

### 🔴 PHASE 5: SERENA PROJECT MEMORY UPDATES

**Tool Requirement:** Serena `write_memory` and `read_memory`

#### Task 5.1: Update Tech Stack Memory

**Actions:**
1. [ ] **Sequential-Thinking:** Plan tech stack updates
2. [ ] **Serena `read_memory`:** Read tech_stack.md
3. [ ] **Serena `write_memory`:** Add persistent agent section

**Content to Add:**
```markdown
### Persistent Agent Architecture (October 2025)

**Architecture Principle:** CLI = Single Source of Truth, GUI = Wrapper (following b866f0a pattern)

**Implementation:**
- `initialize_persistent_agent()` in CLI - ONE function creates agent
- `process_query()` in CLI - ONE function processes queries
- CLI mode calls these functions directly
- GUI mode imports and calls same functions (no duplication)

**Benefits:**
- ✅ Zero code duplication (one agent creation pattern)
- ✅ GUI inherits CLI core logic (no duplicate processing)
- ✅ Token efficiency via prompt caching
- ✅ Performance optimization (no repeated initialization)
- ✅ Follows OpenAI Agents SDK best practices
```

---

#### Task 5.2: Update Project Architecture Memory

**Content to Add:**
```markdown
### Agent Lifecycle (Following b866f0a Zero-Duplication Principle)

**Pattern:** CLI owns core logic, GUI calls CLI functions

**CLI Module Functions:**
- `initialize_persistent_agent()` - Creates agent ONCE (single source of truth)
- `process_query(agent, session, input)` - Core processing logic (no duplication)

**CLI Mode:**
- Creates agent using `initialize_persistent_agent()`
- Calls `process_query()` for each message
- Adds CLI-specific formatting and output

**GUI Mode:**
- Creates agent in `lifespan()` using `initialize_persistent_agent()`
- Imports `process_query()` from CLI
- Adds HTTP response wrapper

**Zero Duplication:**
- ✅ ONE agent initialization function (in CLI)
- ✅ ONE query processing function (in CLI)
- ✅ GUI imports and calls CLI functions (no duplicate logic)
```

---

#### Task 5.3: Create Adaptive Formatting Memory

**Content:**
```markdown
# Adaptive Response Formatting Guide

## Overview
Agent intelligently chooses formatting based on data complexity (embedded in agent instructions).

## Formatting Rules

### Simple Responses → Lists
Use when:
- Few data points (< 5 items)
- Quick answers or summaries
- Single-dimension data

Example:
```
KEY TAKEAWAYS:
• TSLA showing bullish momentum
• Price above 50-day MA
• RSI at 62 (neutral-bullish)
```

### Complex Responses → Tables
Use when:
- Multiple data points (≥ 5 items)
- Multi-dimensional data (options chains)
- Comparisons or structured data

Example:
```markdown
| Strike | Premium | IV  | Delta |
|--------|---------|-----|-------|
| $150   | $5.20   | 45% | 0.65  |
```

## Implementation
Formatting guidance in `get_enhanced_agent_instructions()` in `agent_service.py`.
Agent automatically selects format—no explicit code logic needed.
```

---

### 🔴 PHASE 6: GIT COMMIT (ATOMIC COMMIT WORKFLOW)

**🔴 CRITICAL: Stage ALL files ONLY immediately before commit**

#### Task 6.1: Pre-Commit Verification

**Actions:**
1. [ ] **Sequential-Thinking:** Review all changes
2. [ ] Verify ALL code changes complete
3. [ ] Verify ALL tests passed
4. [ ] Verify ALL documentation updated
5. [ ] Verify ALL Serena memories updated
6. [ ] Run `git status` and `git diff`
7. [ ] **DO NOT run `git add` yet**

---

#### Task 6.2: Stage and Commit

```bash
git add -A
git status  # Verify all staged

git commit -m "$(cat <<'EOF'
[ARCHITECTURE] Implement persistent agent pattern - eliminate code duplication

Architecture Principle (following commit b866f0a):
- CLI = Single source of truth for core business logic
- GUI = Wrapper that calls CLI functions (zero duplication)

Problem Fixed:
- Both CLI and GUI were duplicating agent creation logic
- create_agent() called in two places (CLI and GUI routers)
- Runner.run() logic duplicated in two places
- Violated b866f0a zero-duplication principle

Solution Implemented:
- Created shared functions in CLI module:
  • initialize_persistent_agent() - ONE function creates agent
  • process_query() - ONE function processes queries
- CLI mode calls these functions directly
- GUI mode imports and calls same functions
- Zero code duplication achieved

Files Modified:
- src/backend/cli.py: Added shared functions, persistent agent in CLI
- src/backend/routers/chat.py: Import CLI functions, eliminate duplication
- src/backend/main.py: Create shared agent in lifespan using CLI function
- src/backend/dependencies.py: Add agent to shared resources
- src/backend/services/agent_service.py: Adaptive formatting instructions

Architecture Benefits:
✅ Zero code duplication (one agent creation, one processing logic)
✅ GUI inherits CLI core logic (no duplicate processing)
✅ Single source of truth maintained (CLI owns business logic)
✅ Token efficiency via prompt caching
✅ Performance optimization (no repeated agent initialization)
✅ Follows OpenAI Agents SDK best practices
✅ Follows b866f0a architecture principle

Testing:
- CLI regression suite: X/X PASSED (100% success rate)
- Response times: X.XXs average (within baseline)
- Test report: test-reports/test_cli_regression_YYYY-MM-DD_HH-MM.log

Documentation:
- .serena/memories/tech_stack.md: Persistent agent architecture
- .serena/memories/project_architecture.md: Agent lifecycle pattern
- .serena/memories/adaptive_formatting_guide.md: Formatting guide
- TODO_task_plan.md: Revised implementation plan
- CLAUDE.md: Updated task summary

Reference: OpenAI Agents SDK sessions.md + commit b866f0a architecture

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

git push
```

---

## 🎯 SUCCESS CRITERIA

### Architecture Compliance ✅
- [ ] CLI module has `initialize_persistent_agent()` function
- [ ] CLI module has `process_query()` function
- [ ] GUI router imports these functions from CLI
- [ ] No duplicate agent creation code
- [ ] No duplicate query processing code
- [ ] Follows b866f0a zero-duplication principle

### Code Changes ✅
- [ ] CLI creates agent once using shared function
- [ ] GUI creates agent once using shared function
- [ ] GUI calls CLI `process_query()` function
- [ ] No `create_agent()` calls in request handlers
- [ ] Adaptive formatting instructions added

### Testing ✅
- [ ] CLI regression suite passes (100%)
- [ ] Response times within baseline
- [ ] No errors or exceptions
- [ ] Agent persistence working
- [ ] Adaptive formatting visible

### Documentation ✅
- [ ] Serena memories updated
- [ ] CLAUDE.md updated with task summary
- [ ] Git commit includes all changes atomically

---

## 🚨 CRITICAL REMINDERS

### Architecture Principle (from b866f0a)
- ✅ CLI = Single source of truth (core business logic)
- ✅ GUI = Wrapper (calls CLI functions, adds HTTP layer)
- ✅ Zero code duplication
- ✅ Backend generates, frontend displays

### Tool Usage Requirements
- ✅ START every phase with Sequential-Thinking
- ✅ Use Serena tools for all code modifications
- ✅ Use tools continuously throughout
- ✅ Never use tools only once

### Testing Requirements
- ✅ MUST run `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
- ✅ MUST achieve 100% pass rate
- ✅ MUST show results to user
- ✅ Task incomplete without test execution

### Git Commit Requirements
- ✅ Complete ALL work BEFORE staging
- ✅ Stage ALL files with `git add -A` ONCE
- ✅ Commit within 60 seconds
- ✅ Include ALL changes atomically

---

## 📊 EXPECTED OUTCOMES

### Code Quality
- Cleaner architecture (CLI owns logic, GUI wraps it)
- Zero duplication (one agent pattern, one processing logic)
- Proper separation of concerns (core vs presentation)
- Follows established b866f0a pattern

### Performance
- Token efficiency (prompt caching)
- Faster responses (no repeated initialization)
- Better resource utilization

### Maintainability
- Changes only in CLI (GUI auto-inherits)
- Single source of truth for core logic
- Easier to understand and modify

---

## 🔍 VERIFICATION CHECKLIST

Before marking complete:
- [ ] CLI has `initialize_persistent_agent()` function
- [ ] CLI has `process_query()` function
- [ ] GUI imports and calls these CLI functions
- [ ] No duplicate agent creation code
- [ ] All tests pass (100% shown)
- [ ] All documentation updated
- [ ] Git commit created with all changes
- [ ] Architecture follows b866f0a principle

---

**END OF REVISED IMPLEMENTATION PLAN**
