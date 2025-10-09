# TODO Task Plan: Fix AI Agent TA Tool Enforcement & Remove Options Tool

## Research Summary

**Completed Research Findings:**

1. **TA Tool Enforcement Issue**: Agent instructions allow chat history reuse too liberally - AI Agent approximates SMA-20 from 20-day OHLC data instead of fetching via `get_ta_sma` tool
2. **Options Tool References Found**:
   - `src/backend/services/agent_service.py`: 6 references (import, tools list, instructions)
   - `src/backend/tools/polygon_tools.py`: 7 references (function definition + docstrings)
   - `test_cli_regression.sh`: 4 test cases (2 for SPY, 2 for NVDA)

---

## Implementation Plan

### Phase 1: Agent Instructions Updates (TA Tool Enforcement)

**File**: `src/backend/services/agent_service.py`

**Task 1.1**: Update RULE #8 to Prohibit TA Approximation

- [ ] Use Serena `find_symbol` to read `get_enhanced_agent_instructions` function body
- [ ] Locate RULE #8 section on Technical Analysis
- [ ] Add explicit enforcement rule BEFORE the existing RULE #8 content:

```
🔴 CRITICAL TA TOOL ENFORCEMENT RULES:
- **NEVER APPROXIMATE** technical analysis indicator values
- **MUST FETCH** each requested indicator via dedicated TA tool calls
- **DATA REUSE ALLOWED ONLY IF**: The EXACT same indicator was previously fetched
  - ✅ CORRECT: User requests SMA-20, you already fetched SMA-20 → Reuse existing SMA-20 data
  - ❌ WRONG: User requests SMA-20, you have 20-day OHLC bars → MUST fetch SMA-20 via get_ta_sma
  - ❌ WRONG: "Approximating SMA-20 from latest 20-day window data"
- **EACH TA INDICATOR IS UNIQUE**: SMA-20 ≠ OHLC bars, EMA-50 ≠ SMA-50, RSI-14 ≠ MACD
- **NO EXCEPTIONS**: If user requests SMA 20/50/200, you MUST fetch all three via tool calls (unless previously fetched in this conversation)
```

- [ ] Update the existing RULE #8 content to reference this new enforcement section
- [ ] Add example scenarios showing correct vs incorrect TA tool usage

**Task 1.2**: Update RULE #9 Chat History Analysis for TA

- [ ] Locate RULE #9 examples section
- [ ] Update examples to show correct TA tool behavior:
  - **Scenario**: User requests "SPY SMA 20/50/200", no existing TA data
  - **CORRECT**: Make 3 tool calls: `get_ta_sma(ticker='SPY', window=20)`, `get_ta_sma(ticker='SPY', window=50)`, `get_ta_sma(ticker='SPY', window=200)`
  - **WRONG**: Fetch OHLC bars and approximate SMA-20 from 20-day window

**Task 1.3**: Update "Tools Used" Transparency Requirement

- [ ] Add note that ALL TA tool calls must be explicitly listed
- [ ] Emphasize that approximations or derived values must never appear in "Tools Used"

---

### Phase 2: Remove Options Tool References

**Task 2.1**: Remove from Agent Service

**File**: `src/backend/services/agent_service.py`

- [ ] Use Serena `find_symbol` to read the `create_agent` function
- [ ] Remove `get_options_quote_single,` from the tools list (line 383)
- [ ] Use Serena `search_for_pattern` to find the import statement
- [ ] Remove `get_options_quote_single,` from imports (line 13)

**Task 2.2**: Remove from Agent Instructions

**File**: `src/backend/services/agent_service.py` (within `get_enhanced_agent_instructions`)

- [ ] Remove `get_options_quote_single` from the supported tools list (line 35)
  - Update count from "11 SUPPORTED TOOLS" to "10 SUPPORTED TOOLS"
- [ ] **DELETE ENTIRE RULE #3** (lines 62-73):
  - Section title: "RULE #3: OPTIONS = ALWAYS USE get_options_quote_single()"
  - All examples and descriptions
  - Display requirements for options
- [ ] Remove options example from correct tool calls section (line 267)
- [ ] Update RULE numbering: Current RULE #4 becomes RULE #3, RULE #5 becomes RULE #4, etc.
- [ ] Search for any other "option" references in instructions and remove

**Task 2.3**: Update Decision Tree and Examples

- [ ] Remove options-related decision points from the DECISION TREE section
- [ ] Remove options examples from "EXAMPLES OF CORRECT TOOL CALLS"
- [ ] Remove any "WRONG" examples that reference options

**Task 2.4**: Remove Tool Definition (Keep for Reference)

**File**: `src/backend/tools/polygon_tools.py`

- [ ] Use Serena `find_symbol` to locate `get_options_quote_single` function (line 589)
- [ ] **COMMENT OUT** the entire function (lines 589-660) with a note:
  ```python
  # REMOVED: get_options_quote_single tool - replaced by future full options chain tool
  # Removal date: 2025-10-08
  # Reason: Single quote tool inefficient, will be replaced with full options chain fetcher
  ```
- [ ] Keep the commented code for reference/future implementation
- [ ] Update any docstrings in other functions that reference `get_options_quote_single`

---

### Phase 3: Remove Options Test Cases

**File**: `test_cli_regression.sh`

**Task 3.1**: Remove SPY Options Test Cases

- [ ] Use standard Read tool to view test_cli_regression.sh around lines 85-86
- [ ] Remove line 85: `"Get First 3 Call Option Quotes expiring this Friday above current price (show strike prices): \$SPY"`
- [ ] Remove line 86: `"Get First 3 Put Option Quotes expiring this Friday below current price (show strike prices): \$SPY"`

**Task 3.2**: Remove NVDA Options Test Cases

- [ ] Use standard Read tool to view test_cli_regression.sh around lines 101-102
- [ ] Remove line 101: `"Get First 3 Call Option Quotes expiring this Friday above current price (show strike prices): \$NVDA"`
- [ ] Remove line 102: `"Get First 3 Put Option Quotes expiring this Friday below current price (show strike prices): \$NVDA"`

**Task 3.3**: Update Test Count

- [ ] Verify total test count in script header/comments
- [ ] Update from 35 tests to 31 tests (removed 4 options tests)
- [ ] Update any expected pass count assertions

---

### Phase 4: CLI Testing & Validation

**Task 4.1**: Run Test Suite

- [ ] Execute: `./test_cli_regression.sh`
- [ ] Wait for completion (approximately 5-6 minutes)
- [ ] Capture test report filename

**Task 4.2**: Verify Response Content (CRITICAL)

🔴 **MANDATORY**: Must verify ACTUAL response content, NOT just PASS status

- [ ] Use Read tool to open the test report log file
- [ ] **FOR TA TESTS** (e.g., Test 10 "SPY SMA"):
  - [ ] Find the "Tools Used" section in the response
  - [ ] Verify ALL requested indicators were fetched (SMA-20, SMA-50, SMA-200)
  - [ ] Confirm NO approximation language (e.g., "approximated from 20-day window")
  - [ ] Check that response shows actual fetched values, not derived/calculated values
- [ ] **FOR OPTIONS TESTS**:
  - [ ] Verify the 4 options test cases no longer exist
  - [ ] Confirm no errors related to missing options tool
- [ ] **FOR OTHER TESTS**:
  - [ ] Spot-check 5-10 random tests to ensure responses contain actual data
  - [ ] Verify responses are coherent and not hallucinated

**Task 4.3**: Document Findings

- [ ] Create validation report with:
  - Total tests run (should be 31)
  - Pass/fail count
  - TA test verification results (did agent fetch all indicators?)
  - Any issues or anomalies found
  - Response content quality assessment

---

### Phase 5: Report to User

**Task 5.1**: Prepare Test Results Summary

- [ ] Summarize test execution results
- [ ] Highlight TA tool enforcement verification
- [ ] Note options tool removal success
- [ ] Flag any issues or concerns

**Task 5.2**: Present to User for Review

- [ ] **DO NOT** proceed with Serena updates yet
- [ ] **DO NOT** commit changes yet
- [ ] Present findings and await user confirmation
- [ ] If issues found, return to implementation phase

---

## Success Criteria

- ✅ All 31 tests pass (35 original - 4 options tests removed)
- ✅ TA tests show ALL requested indicators fetched via tool calls
- ✅ NO approximation language in TA responses
- ✅ Options tool completely removed from agent service
- ✅ Options instructions removed from agent instructions
- ✅ Options test cases removed from test suite
- ✅ Test response content verified manually (not just PASS status)
- ✅ User reviews and approves results before final commits

---

## Tools to Use

**Sequential-Thinking**: For complex analysis and decision-making throughout implementation

**Serena Tools**:
- `find_symbol`: Locate functions to edit
- `search_for_pattern`: Find all references to remove
- `replace_symbol_body`: Update agent instructions function (if body replacement needed)
- `replace_lines`: For targeted line-by-line edits

**Standard Tools**:
- `Read`: View test results and verify content
- `Edit`: Make precise text replacements in agent instructions and test script
- `Bash`: Run test suite

---

## Risk Mitigation

**Risk 1**: Agent instructions become too strict and refuse valid requests
- **Mitigation**: Include clear examples of when data reuse IS allowed
- **Testing**: Verify multi-turn conversations still work correctly

**Risk 2**: Removing options tool breaks other functionality
- **Mitigation**: Comment out tool code instead of deleting, keep for reference
- **Testing**: Run full test suite to ensure no cascade failures

**Risk 3**: Test verification misses subtle issues
- **Mitigation**: Read actual response content, not just PASS/FAIL status
- **Testing**: Manually verify TA tool calls in "Tools Used" sections

**Risk 4**: Rule renumbering causes confusion in instructions
- **Mitigation**: Carefully update all cross-references to rule numbers
- **Testing**: Read through entire instructions to ensure coherence

---

## Implementation Notes

- **CRITICAL**: This is a RESEARCH → PLANNING phase. Do NOT implement yet until user approves plan.
- After implementation, testing is MANDATORY before any commits
- Response content verification is NON-NEGOTIABLE (per user's explicit requirement)
- User must review test results before proceeding to Serena updates/commits
