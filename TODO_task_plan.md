# TODO Task Plan: Fix Gradio Performance Metrics Footer

**Date:** October 17, 2025
**Task:** [BUG] Add performance metrics footer to Gradio ChatInterface responses
**Estimated Time:** 15-20 minutes
**Status:** Ready for Implementation

---

## Overview

Fix Gradio ChatInterface to display performance metrics footer (Response Time, Tokens Used, Model) matching CLI and React frontend implementations. Root cause: `chat_with_agent()` only extracts response text and ignores available metadata.

---

## PHASE 3: IMPLEMENTATION

### Task 3.1: Add Required Imports to gradio_app.py

**File:** `src/backend/gradio_app.py`
**Location:** Top of file (after existing imports)
**Action:** Add missing imports for metadata extraction

**Required imports:**
```python
import time
from backend.utils.token_utils import extract_token_usage_from_context_wrapper
from backend.config import settings
```

**Serena Tool:** Use `mcp__serena__find_symbol` to read current imports, then `mcp__serena__insert_before_symbol` to add new imports

**Verification:**
- ✅ `import time` added
- ✅ `from backend.utils.token_utils import extract_token_usage_from_context_wrapper` added
- ✅ `from backend.config import settings` added
- ✅ No duplicate imports
- ✅ Imports follow project style (grouped: stdlib, third-party, local)

---

### Task 3.2: Modify chat_with_agent() Function - Add Time Measurement

**File:** `src/backend/gradio_app.py`
**Function:** `chat_with_agent(message: str, history: List)`
**Location:** Line 56 (before `result = await process_query(...)`)
**Action:** Add start time measurement

**Code to add:**
```python
        # Measure processing time for performance metrics
        start_time = time.perf_counter()
```

**Serena Tool:** Use `mcp__serena__find_symbol` with `name_path="chat_with_agent"`, `include_body=true` to read function, then use Sequential-Thinking to plan the edit

**Verification:**
- ✅ `start_time = time.perf_counter()` added before `process_query()` call
- ✅ Comment explains purpose
- ✅ Variable name matches CLI implementation pattern

---

### Task 3.3: Modify chat_with_agent() Function - Extract Metadata

**File:** `src/backend/gradio_app.py`
**Function:** `chat_with_agent(message: str, history: List)`
**Location:** Line 60 (after `result = await process_query(...)`)
**Action:** Extract performance metadata from result

**Code to add:**
```python
        # Calculate processing time
        processing_time = time.perf_counter() - start_time

        # Extract response text
        response_text = str(result.final_output)

        # Extract token usage using shared CLI utility (zero duplication)
        token_usage = extract_token_usage_from_context_wrapper(result)

        # Get model name from settings
        model_name = settings.available_models[0]  # "gpt-5-nano"
```

**Serena Tool:** Use `mcp__serena__replace_symbol_body` to replace the entire `chat_with_agent` function body with updated version

**Verification:**
- ✅ `processing_time` calculated immediately after `process_query()` returns
- ✅ `response_text` extracted from `result.final_output`
- ✅ `token_usage` extracted using shared utility function
- ✅ `model_name` extracted from settings
- ✅ Comments explain each extraction step

---

### Task 3.4: Modify chat_with_agent() Function - Format Performance Metrics Footer

**File:** `src/backend/gradio_app.py`
**Function:** `chat_with_agent(message: str, history: List)`
**Location:** After metadata extraction (before streaming logic)
**Action:** Create formatted footer string matching CLI output

**Code to add:**
```python
        # Format performance metrics footer (matching CLI format)
        footer = "\n\nPerformance Metrics:\n"
        footer += f"   Response Time: {processing_time:.3f}s\n"

        # Add token information if available
        if token_usage:
            token_count = token_usage.get("total_tokens")
            input_tokens = token_usage.get("input_tokens")
            output_tokens = token_usage.get("output_tokens")
            cached_input = token_usage.get("cached_input_tokens", 0)
            cached_output = token_usage.get("cached_output_tokens", 0)

            if token_count:
                footer += f"   Tokens Used: {token_count:,}"

                if input_tokens and output_tokens:
                    footer += f" (Input: {input_tokens:,}, Output: {output_tokens:,})"

                    # Show cache hit information if tokens were cached
                    if cached_input > 0 or cached_output > 0:
                        cache_parts = []
                        if cached_input > 0:
                            cache_parts.append(f"Cached Input: {cached_input:,}")
                        if cached_output > 0:
                            cache_parts.append(f"Cached Output: {cached_output:,}")
                        footer += f" | {', '.join(cache_parts)}"

                footer += "\n"

        # Add model information
        footer += f"   Model: {model_name}\n"

        # Append footer to response
        response_with_footer = response_text + footer
```

**Verification:**
- ✅ Footer starts with "\n\nPerformance Metrics:\n"
- ✅ Response time formatted with 3 decimal places
- ✅ Token count formatted with thousands separators (21,701)
- ✅ Input/output tokens displayed in parentheses
- ✅ Cached tokens shown when > 0 (matching CLI format)
- ✅ Model name displayed on separate line
- ✅ Footer appended to response_text

---

### Task 3.5: Modify chat_with_agent() Function - Update Streaming Logic

**File:** `src/backend/gradio_app.py`
**Function:** `chat_with_agent(message: str, history: List)`
**Location:** Streaming loop (currently streams `response_text`, change to `response_with_footer`)
**Action:** Stream complete response including footer

**Current code:**
```python
        # Gradio streaming: yield progressive chunks for better UX
        sentences = response_text.replace(". ", ".|").split("|")
        accumulated = ""
        for sentence in sentences:
            accumulated += sentence
            yield accumulated
            await asyncio.sleep(0.05)
```

**Updated code:**
```python
        # Gradio streaming: yield progressive chunks for better UX
        sentences = response_with_footer.replace(". ", ".|").split("|")
        accumulated = ""
        for sentence in sentences:
            accumulated += sentence
            yield accumulated
            await asyncio.sleep(0.05)
```

**Verification:**
- ✅ Changed `response_text` to `response_with_footer` in split logic
- ✅ Streaming logic unchanged (still progressive chunks)
- ✅ Sleep delay unchanged (0.05s for smooth UX)

---

### Task 3.6: Complete Implementation - Full Function Verification

**File:** `src/backend/gradio_app.py`
**Function:** `chat_with_agent(message: str, history: List)`
**Action:** Verify complete updated function

**Expected function structure:**
```python
async def chat_with_agent(message: str, history: List):
    """Process financial query using existing CLI core logic.

    ... [docstring unchanged] ...
    """
    try:
        # 1. Measure start time
        start_time = time.perf_counter()

        # 2. Call shared CLI processing function
        result = await process_query(agent, session, message)

        # 3. Calculate processing time
        processing_time = time.perf_counter() - start_time

        # 4. Extract response text
        response_text = str(result.final_output)

        # 5. Extract token usage
        token_usage = extract_token_usage_from_context_wrapper(result)

        # 6. Get model name
        model_name = settings.available_models[0]

        # 7. Format performance metrics footer
        footer = "\n\nPerformance Metrics:\n"
        footer += f"   Response Time: {processing_time:.3f}s\n"

        if token_usage:
            # ... [token formatting logic] ...

        footer += f"   Model: {model_name}\n"

        # 8. Append footer to response
        response_with_footer = response_text + footer

        # 9. Stream complete response
        sentences = response_with_footer.replace(". ", ".|").split("|")
        accumulated = ""
        for sentence in sentences:
            accumulated += sentence
            yield accumulated
            await asyncio.sleep(0.05)

    except Exception as e:
        # Error handling (unchanged)
        error_msg = f"❌ Error: Unable to process request.\n\nDetails: {str(e)}"
        yield error_msg
```

**Verification Checklist:**
- ✅ All imports present at top of file
- ✅ Time measurement added
- ✅ Metadata extraction added
- ✅ Footer formatting added
- ✅ Streaming updated to use `response_with_footer`
- ✅ Error handling unchanged
- ✅ Function docstring unchanged
- ✅ No code duplication (reuses shared utilities)

---

## PHASE 4: TESTING & VALIDATION

### Task 4.1: Manual Gradio Testing

**Action:** Launch Gradio and test with sample queries

**Steps:**
```bash
# 1. Start Gradio server
uv run python src/backend/gradio_app.py

# 2. Open browser: http://127.0.0.1:7860

# 3. Test queries:
#    - "What is the market status?"
#    - "What is SPY current price?"
#    - "Show me NVDA technical analysis"

# 4. Verify footer appears:
#    Performance Metrics:
#       Response Time: X.XXXs
#       Tokens Used: X,XXX (Input: X,XXX, Output: XXX)
#       Model: gpt-5-nano
```

**Verification:**
- ✅ Footer displays after every response
- ✅ Response time is reasonable (5-15s range)
- ✅ Token counts are non-zero positive integers
- ✅ Model name shows "gpt-5-nano"
- ✅ Format matches CLI output

**Serena Tool:** Use Sequential-Thinking to analyze test results and identify any issues

---

### Task 4.2: CLI Regression Test Suite (MANDATORY)

**Action:** Run full 39-test regression suite

**Command:**
```bash
chmod +x test_cli_regression.sh && ./test_cli_regression.sh
```

**Expected Results:**
- ✅ 39/39 tests COMPLETED
- ✅ 0 errors (grep verification)
- ✅ Average response time < 12s (EXCELLENT rating)
- ✅ Test report generated in `test-reports/`

**Phase 2 Verification (MANDATORY):**

**Phase 2a: ERROR DETECTION**
```bash
# Command 1: Find all errors/failures
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log

# Command 2: Count 'data unavailable' errors
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log

# Command 3: Count completed tests
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Expected grep outputs:**
- Command 1: NO ERRORS (empty or "✅ NO ERRORS FOUND")
- Command 2: 0
- Command 3: 40 (39 tests + 1 summary line)

**Phase 2c: RESPONSE CORRECTNESS VERIFICATION**

For all tests, verify:
1. ✅ Response directly addresses the prompt query
2. ✅ Correct ticker symbols used ($SPY, $NVDA, etc.)
3. ✅ Appropriate tool calls made (Polygon, Tradier)
4. ✅ Data formatting correct (OHLC, prices, changes)
5. ✅ No hallucinated data
6. ✅ Performance metrics footer NOT affected by code changes
7. ✅ Prompt caching still working (cached tokens visible)
8. ✅ Response is complete (not truncated)

**Phase 2d: CHECKPOINT QUESTIONS**

Answer ALL checkpoint questions with evidence:
1. ✅ Did you RUN the 3 mandatory grep commands in Phase 2a? **SHOW OUTPUT**
2. ✅ Did you DOCUMENT all failures found (or confirm 0 failures)? **PROVIDE TABLE OR "0 failures"**
3. ✅ Failure count from grep -c: **X failures**
4. ✅ Tests that generated responses: **39/39 COMPLETED**
5. ✅ Tests that PASSED verification (no errors): **39/39 PASSED**

**🔴 CANNOT PROCEED WITHOUT:**
- Running and showing grep outputs
- Documenting failures with evidence (or confirming 0 failures)
- Providing failure count
- Answering all 5 checkpoint questions with evidence

---

### Task 4.3: Gradio-Specific Validation

**Action:** Verify Gradio footer matches CLI/React format exactly

**Test Cases:**
1. **Simple Query** - "Market status"
   - Verify: Footer shows response time, tokens, model
   - Expected time: 3-6s
   - Expected tokens: 15K-25K range

2. **Complex Query** - "NVDA full technical analysis"
   - Verify: Footer shows higher token counts
   - Expected time: 8-15s
   - Expected tokens: 20K-30K range

3. **Repeat Query** (Test Prompt Caching)
   - Run same query twice
   - Verify: Second response shows "Cached Input: X,XXX"
   - Verify: Second response is faster

4. **Multi-Ticker Query** - "Compare WDC, AMD, SOUN prices"
   - Verify: Footer shows correct token usage for parallel calls
   - Expected time: 10-20s
   - Expected tokens: 25K-35K range

5. **Error Handling**
   - Test invalid query: "asdfasdf"
   - Verify: Error message displays, no broken footer

**Verification:**
- ✅ All 5 test cases pass
- ✅ Footer format consistent across all queries
- ✅ Token counts increase with query complexity
- ✅ Cached tokens display on repeat queries
- ✅ Error handling works correctly

---

## PHASE 5: DOCUMENTATION UPDATES

### Task 5.1: Update CLAUDE.md

**File:** `CLAUDE.md`
**Section:** Gradio ChatInterface (NEW) section
**Action:** Update example usage to show performance metrics footer

**Current example (incomplete):**
```markdown
### Gradio ChatInterface (NEW)

```bash
# Start single Gradio server
uv run python src/backend/gradio_app.py

# Access at http://127.0.0.1:7860
```
```

**Updated example (with footer):**
```markdown
### Gradio ChatInterface (NEW)

```bash
# Start single Gradio server
uv run python src/backend/gradio_app.py

# Access at http://127.0.0.1:7860
```

**Example Response:**
```
Market Status: CLOSED
After-hours: NO
Early-hours: NO
Exchanges: NASDAQ closed, NYSE closed, OTC closed
Server Time (UTC): 2025-10-18 01:50:12

Performance Metrics:
   Response Time: 5.135s
   Tokens Used: 21,701 (Input: 21,402, Output: 299)
   Model: gpt-5-nano
```
```

**Serena Tool:** Use `mcp__serena__search_for_pattern` to find Gradio section, then Read and Edit to update

**Verification:**
- ✅ Example updated to show footer
- ✅ Footer format matches actual output
- ✅ Token numbers realistic
- ✅ Markdown formatting correct

---

### Task 5.2: Update README.md

**File:** `README.md`
**Section:** Example Usage > Gradio ChatInterface (NEW)
**Action:** Add footer example to Gradio usage section

**Current section (incomplete):**
```markdown
### Gradio ChatInterface (NEW)

1. Open <http://127.0.0.1:7860>
2. Select an example or type your financial query
3. Get streaming responses with financial data and analysis
4. Examples included: Stock price queries, technical analysis, options chains, stock comparisons
```

**Updated section (with footer example):**
```markdown
### Gradio ChatInterface (NEW)

1. Open <http://127.0.0.1:7860>
2. Select an example or type your financial query
3. Get streaming responses with financial data, analysis, and performance metrics
4. Examples included: Stock price queries, technical analysis, options chains, stock comparisons

**Example Output:**
```
SPY current price: $664.39 (+$3.75, +0.57%)
Open: $659.50, High: $665.75, Low: $658.14
Previous close: $660.64
Market status: CLOSED

Performance Metrics:
   Response Time: 5.314s
   Tokens Used: 22,304 (Input: 21,920, Output: 384) | Cached Input: 10,496
   Model: gpt-5-nano
```
```

**Verification:**
- ✅ Example added to Gradio section
- ✅ Shows cached tokens (demonstrates prompt caching)
- ✅ Footer format matches CLI/React
- ✅ Markdown formatting correct

---

### Task 5.3: Update Serena Memory (project_architecture.md)

**File:** `.serena/memories/project_architecture.md`
**Section:** Gradio Implementation Details
**Action:** Update to document performance metrics footer addition

**Current section (outdated):**
```markdown
### Gradio Implementation Details (NEW - Oct 2025)

**Key Components:**

1. **Agent Initialization:** ...
2. **Chat Function (Async with Streaming):** ...
3. **ChatInterface Configuration:** ...
```

**Add new subsection:**
```markdown
4. **Performance Metrics Footer (Oct 17, 2025):**

Gradio now displays performance metrics footer matching CLI and React frontends.

**Implementation:**
```python
# Measure processing time
start_time = time.perf_counter()
result = await process_query(agent, session, message)
processing_time = time.perf_counter() - start_time

# Extract token usage (zero duplication - reuses CLI utility)
from backend.utils.token_utils import extract_token_usage_from_context_wrapper
token_usage = extract_token_usage_from_context_wrapper(result)

# Format footer
footer = "\n\nPerformance Metrics:\n"
footer += f"   Response Time: {processing_time:.3f}s\n"
# ... [token and model formatting] ...

# Append and stream
response_with_footer = response_text + footer
```

**Footer Format (matches CLI/React):**
```
Performance Metrics:
   Response Time: 5.135s
   Tokens Used: 21,701 (Input: 21,402, Output: 299) | Cached Input: 10,496
   Model: gpt-5-nano
```

**Architecture Consistency:**
- ✅ Reuses shared utilities (zero code duplication)
- ✅ Same footer format across all three interfaces (CLI, React, Gradio)
- ✅ Same metadata visibility for all users
```

**Verification:**
- ✅ New subsection added to Gradio section
- ✅ Implementation details documented
- ✅ Footer format example shown
- ✅ Architecture consistency noted

---

## PHASE 6: FINAL ATOMIC COMMIT

### Task 6.1: Verify All Work Complete (PRE-STAGING CHECKLIST)

**DO NOT RUN `git add` YET - Verify everything first:**

**Code Changes:**
- ✅ `src/backend/gradio_app.py` - Imports added
- ✅ `src/backend/gradio_app.py` - `chat_with_agent()` function updated
- ✅ All code changes tested manually
- ✅ All code changes tested via CLI regression suite

**Test Results:**
- ✅ Manual Gradio testing passed (5 test cases)
- ✅ CLI regression suite passed (39/39 tests)
- ✅ Phase 2 verification completed (grep outputs shown)
- ✅ Test report file generated

**Documentation:**
- ✅ `CLAUDE.md` updated with footer example
- ✅ `README.md` updated with footer example
- ✅ `.serena/memories/project_architecture.md` updated with implementation details

**Other:**
- ✅ `TODO_task_plan.md` - This file (will be committed as evidence)
- ✅ `research_task_plan.md` - Research findings (will be committed as evidence)

**⚠️ DO NOT PROCEED UNTIL ALL CHECKBOXES ARE ✅**

---

### Task 6.2: Review Changes Before Staging

**Command:**
```bash
git status  # Review ALL changed/new files
git diff src/backend/gradio_app.py  # Review gradio_app.py changes
git diff CLAUDE.md  # Review CLAUDE.md changes
git diff README.md  # Review README.md changes
git diff .serena/memories/project_architecture.md  # Review memory changes
```

**Verification:**
- ✅ All expected files show in `git status`
- ✅ No unexpected files modified
- ✅ Diff shows only intended changes
- ✅ No debug code or temporary changes present

---

### Task 6.3: Stage All Changes At Once

**⚠️ THIS IS THE FIRST TIME YOU RUN `git add` ⚠️**

**Command:**
```bash
git add -A  # Stage ALL files in ONE command
```

**Files to be staged:**
- `src/backend/gradio_app.py` (modified)
- `CLAUDE.md` (modified)
- `README.md` (modified)
- `.serena/memories/project_architecture.md` (modified)
- `test-reports/test_cli_regression_loop1_*.log` (new)
- `TODO_task_plan.md` (modified)
- `research_task_plan.md` (modified)

**Verification:**
- ✅ `git add -A` executed
- ✅ This was the FIRST time running `git add`
- ✅ All related files staged together

---

### Task 6.4: Verify Staging Immediately

**Command:**
```bash
git status  # Verify ALL files staged, NOTHING unstaged
```

**Expected output:**
```
Changes to be committed:
  modified:   .serena/memories/project_architecture.md
  modified:   CLAUDE.md
  modified:   README.md
  modified:   TODO_task_plan.md
  modified:   research_task_plan.md
  modified:   src/backend/gradio_app.py
  new file:   test-reports/test_cli_regression_loop1_2025-10-17_XX-XX.log
```

**Verification:**
- ✅ All expected files in "Changes to be committed"
- ✅ NO files in "Changes not staged for commit"
- ✅ NO files in "Untracked files" (except temp files)

**If anything missing:**
```bash
git add [missing-file]  # Add any missing files
git status  # Verify again
```

---

### Task 6.5: Create Atomic Commit (IMMEDIATELY after staging)

**⚠️ COMMIT WITHIN 60 SECONDS OF STAGING ⚠️**

**Command:**
```bash
git commit -m "$(cat <<'EOF'
[BUG FIX] Add Performance Metrics Footer to Gradio ChatInterface

**Problem:** Gradio ChatInterface displayed agent responses but was missing
the performance metrics footer that both CLI and React frontends provide.
Users had no visibility into response time, token usage, or model being used.

**Root Cause:** chat_with_agent() function only extracted result.final_output
text and completely ignored available performance metadata in the result object.

**Solution:** Modified chat_with_agent() to extract and format performance
metrics footer matching CLI/React implementations.

**Code Changes:**
1. src/backend/gradio_app.py (Modified):
   - Added imports: time, extract_token_usage_from_context_wrapper, settings
   - Added time measurement: start_time = time.perf_counter()
   - Added metadata extraction: processing_time, token_usage, model_name
   - Added footer formatting: Performance Metrics section
   - Updated streaming: Stream response_with_footer instead of response_text
   - Total changes: +30 lines in chat_with_agent() function

**Footer Format (matches CLI/React):**
```
Performance Metrics:
   Response Time: 5.135s
   Tokens Used: 21,701 (Input: 21,402, Output: 299) | Cached Input: 10,496
   Model: gpt-5-nano
```

**Testing & Validation:**
✅ Manual Gradio testing: 5 test cases passed
✅ CLI regression suite: 39/39 tests PASSED
✅ Phase 2a: 0 errors found (grep verified)
✅ Phase 2c: All responses verified correct
✅ Prompt caching verified: Cached tokens display correctly
✅ Performance: Average 9.27s (EXCELLENT rating)

**Documentation Updates:**
1. CLAUDE.md: Added footer example to Gradio section
2. README.md: Added footer example to Gradio usage
3. .serena/memories/project_architecture.md: Documented implementation

**Architecture Consistency:**
✅ Reuses shared utilities (zero code duplication)
✅ Same footer format across all interfaces (CLI, React, Gradio)
✅ Same metadata visibility for all users

**Files Changed:**
- Code: src/backend/gradio_app.py (1 file modified)
- Tests: test-reports/test_cli_regression_loop1_*.log (1 file new)
- Documentation: CLAUDE.md, README.md, project_architecture.md (3 files modified)
- Planning: TODO_task_plan.md, research_task_plan.md (2 files modified)
- Total: 7 files

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Verification:**
- ✅ Commit created successfully
- ✅ Commit within 60 seconds of staging
- ✅ Commit message follows project format
- ✅ Commit includes all staged files

---

### Task 6.6: Push to Remote Immediately

**Command:**
```bash
git push
```

**Verification:**
- ✅ Push successful
- ✅ All commits pushed to origin/master
- ✅ No conflicts or errors

---

### Task 6.7: Final Verification

**Command:**
```bash
git log -1 --format="%h %s"  # Show latest commit
git status  # Verify clean working tree
```

**Expected output:**
```
<commit-hash> [BUG FIX] Add Performance Metrics Footer to Gradio ChatInterface

On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```

**Verification:**
- ✅ Latest commit matches expected message
- ✅ Working tree is clean
- ✅ No uncommitted changes
- ✅ No untracked files (except temp files)

---

## Task Completion Checklist

**Phase 3: Implementation**
- [ ] Task 3.1: Add required imports to gradio_app.py
- [ ] Task 3.2: Add time measurement
- [ ] Task 3.3: Extract metadata (processing_time, token_usage, model_name)
- [ ] Task 3.4: Format performance metrics footer
- [ ] Task 3.5: Update streaming logic to use response_with_footer
- [ ] Task 3.6: Verify complete function implementation

**Phase 4: Testing & Validation**
- [ ] Task 4.1: Manual Gradio testing (5 test cases)
- [ ] Task 4.2: CLI regression suite (39 tests)
  - [ ] Run test suite
  - [ ] Phase 2a: Run 3 grep commands and SHOW outputs
  - [ ] Phase 2b: Document failures (or confirm 0 failures)
  - [ ] Phase 2c: Verify response correctness
  - [ ] Phase 2d: Answer all 5 checkpoint questions with evidence
- [ ] Task 4.3: Gradio-specific validation (5 test cases)

**Phase 5: Documentation Updates**
- [ ] Task 5.1: Update CLAUDE.md with footer example
- [ ] Task 5.2: Update README.md with footer example
- [ ] Task 5.3: Update .serena/memories/project_architecture.md

**Phase 6: Final Atomic Commit**
- [ ] Task 6.1: Verify all work complete (pre-staging checklist)
- [ ] Task 6.2: Review changes before staging
- [ ] Task 6.3: Stage all changes at once (FIRST `git add`)
- [ ] Task 6.4: Verify staging immediately
- [ ] Task 6.5: Create atomic commit (within 60 seconds)
- [ ] Task 6.6: Push to remote immediately
- [ ] Task 6.7: Final verification

---

## Success Criteria

**Implementation is successful when:**
- ✅ Gradio displays performance metrics footer after every response
- ✅ Footer format matches CLI output (same fields, same formatting)
- ✅ Response time is accurate (within 0.1s of actual duration)
- ✅ Token counts are correct (match OpenAI API response)
- ✅ Cached tokens display when prompt caching occurs
- ✅ All 39 CLI regression tests pass (100% success rate)
- ✅ No performance regression (response times remain <12s average)
- ✅ Documentation updated across all relevant files
- ✅ Atomic commit created and pushed to remote

---

## Estimated Time

- **Implementation:** 10 minutes
- **Testing:** 20 minutes (15 min CLI suite + 5 min manual)
- **Documentation:** 5 minutes
- **Commit:** 2 minutes
- **Total:** ~40 minutes

---

**Plan Status:** Ready for execution - all tasks clearly defined with verification criteria.
