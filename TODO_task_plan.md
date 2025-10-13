# TODO Task Plan - Test Suite Validation Framework Overhaul

**Date:** October 12, 2025
**Based On:** research_task_plan.md
**Status:** READY FOR IMPLEMENTATION
**Estimated Time:** 3-4 hours

---

## 🔴 CRITICAL: MANDATORY TOOL USAGE

**YOU MUST use Sequential-Thinking and Serena tools throughout ENTIRE implementation:**

- **START every implementation phase** with Sequential-Thinking for systematic approach
- **Use Serena tools** for code analysis, symbol manipulation, pattern searches
- **Use Sequential-Thinking** repeatedly for complex reasoning and planning
- **Use Standard Read/Write/Edit** only when Serena doesn't support the specific operation
- **NEVER stop using advanced tools** until task completion

---

## Phase 3: Implementation

### Task 3.1: Update test_cli_regression.sh with New Prompts

**Status:** ⏳ PENDING
**Tool Requirements:** Sequential-Thinking → Serena find_symbol → Read → Edit
**Estimated Time:** 15-20 minutes

**Subtasks:**

- [ ] 3.1.1: Use Sequential-Thinking to analyze new vs old prompt structure
- [ ] 3.1.2: Use Read to review current prompts array (lines 70-114)
- [ ] 3.1.3: Use Edit to replace prompts array with new 40 prompts:

```bash
declare -a prompts=(
    # SPY Test Sequence (Tests 1-16)
    "Market Status"
    "Current Price OHLC: \$SPY"
    "Yesterday's Price OHLC: \$SPY"
    "Last week's Performance OHLC: \$SPY"
    "Stock Price on the previous week's Friday OHLC: \$SPY"
    "Stock Price Performance the last 5 Trading Days OHLC: \$SPY"
    "Stock Price Performance the past 2 Weeks OHLC: \$SPY"
    "Stock Price Performance the past month: \$SPY"
    "Stock Price Performance the past 3 months: \$SPY"
    "Get technical analysis indicator DATA only with NO ANALYSIS: \$SPY"
    "Support & Resistance Levels: \$SPY"
    "Perform technical analysis based on all available data for Trends, Volatility, Momentum, Trading Patterns\Signals: \$SPY"
    "Get options expiration dates: \$SPY"
    "Get Call Options Chain Expiring this Friday: \$SPY"
    "Get Put Options Chain Expiring this Friday: \$SPY"
    "Analyze the Options Chain Data & provide potential Call & Put Wall(s) Strike Prices: \$SPY"

    # NVDA Test Sequence (Tests 17-32)
    "Current Price OHLC: \$NVDA"
    "Yesterday's Price OHLC: \$NVDA"
    "Last week's Performance OHLC: \$NVDA"
    "Stock Price on the previous week's Friday OHLC: \$NVDA"
    "Stock Price Performance the last 5 Trading Days OHLC: \$NVDA"
    "Stock Price Performance the past 2 Weeks OHLC: \$NVDA"
    "Stock Price Performance the past month: \$NVDA"
    "Stock Price Performance the past 3 months: \$NVDA"
    "Get technical analysis indicator DATA only with NO ANALYSIS: \$NVDA"
    "Support & Resistance Levels: \$NVDA"
    "Perform technical analysis based on all available data for Trends, Volatility, Momentum, Trading Patterns\Signals: \$NVDA"
    "Get options expiration dates for \$NVDA"
    "Get Call Options Chain Expiring this Friday: \$NVDA"
    "Get Put Options Chain Expiring this Friday: \$NVDA"
    "Analyze the Options Chain Data & provide potential Call & Put Wall(s) Strike Prices: \$NVDA"

    # Multi-Ticker Test Sequence (Tests 33-40)
    "Current Price OHLC: \$WDC, \$AMD, \$SOUN"
    "Yesterday's Price OHLC: \$WDC, \$AMD, \$SOUN"
    "Yesterday's Closing Price: \$WDC, \$AMD, \$SOUN"
    "Last week's Performance OHLC: \$WDC, \$AMD, \$SOUN"
    "Get technical analysis indicator DATA only with NO ANALYSIS: \$WDC, \$AMD, \$SOUN"
    "Support & Resistance Levels: \$WDC, \$AMD, \$SOUN"
    "Perform technical analysis based on all available data for Trends, Volatility, Momentum, Trading Patterns\Signals: \$WDC, \$AMD, \$SOUN"
    "Get options expiration dates: \$WDC, \$AMD, \$SOUN"
)
```

- [ ] 3.1.4: Use Edit to update test_names array (lines 116-160) to match new prompts
- [ ] 3.1.5: Use Edit to update header comment (lines 15-19) with new test counts

**Success Criteria:**
- ✅ Prompts array updated to exactly 40 prompts
- ✅ Test_names array matches new prompts
- ✅ Header comments reflect correct test distribution
- ✅ No syntax errors in bash arrays

---

### Task 3.2: Remove "PASS" Terminology from test_cli_regression.sh

**Status:** ⏳ PENDING
**Tool Requirements:** Sequential-Thinking → Read → Edit (multiple locations)
**Estimated Time:** 30-40 minutes

**Subtasks:**

- [ ] 3.2.1: Use Sequential-Thinking to plan terminology replacement strategy
- [ ] 3.2.2: Use Edit to replace line 246: `test_results+=("PASS")` → `test_results+=("COMPLETED")`
- [ ] 3.2.3: Use Edit to replace line 299: `test_results+=("PASS")` → `test_results+=("COMPLETED")`
- [ ] 3.2.4: Use Edit to update line 315: `if [ "$result" = "PASS" ]` → `if [ "$result" = "COMPLETED" ]`
- [ ] 3.2.5: Use Edit to update line 317 display:
  ```bash
  # OLD:
  echo -e "${GREEN}   Test $test_number: ${test_names[$i]} - PASS${NC}"

  # NEW:
  echo -e "${GREEN}   Test $test_number: ${test_names[$i]} - COMPLETED${NC}"
  ```
- [ ] 3.2.6: Use Edit to replace line 232:
  ```bash
  # OLD:
  echo -e "${GREEN}✅ Test completed${NC}"

  # NEW:
  echo -e "${GREEN}✅ Response received${NC}"
  ```
- [ ] 3.2.7: Use Edit to update lines 396-406 (loop status logic):
  ```bash
  # OLD:
  if [ $failed_tests -eq 0 ]; then
      echo -e "${GREEN}🎉 All $total_tests tests passed in Loop ${loop_num}!${NC}"
      echo -e "${GREEN}✅ Loop ${loop_num} CLI Regression Test: SUCCESS${NC}"
      ((total_loops_passed++))
      loop_status="PASS"
  else
      echo -e "${RED}❌ $failed_tests test(s) failed in Loop ${loop_num}${NC}"
      echo -e "${RED}❌ Loop ${loop_num} CLI Regression Test: FAILED${NC}"
      ((total_loops_failed++))
      loop_status="FAIL"
  fi

  # NEW:
  if [ $failed_tests -eq 0 ]; then
      echo -e "${GREEN}🎉 All $total_tests responses received in Loop ${loop_num}!${NC}"
      echo -e "${GREEN}✅ Loop ${loop_num} Phase 1: All responses generated${NC}"
      ((total_loops_completed++))
      loop_status="COMPLETED"
  else
      echo -e "${RED}❌ $failed_tests test(s) had no response in Loop ${loop_num}${NC}"
      echo -e "${RED}❌ Loop ${loop_num} Phase 1: INCOMPLETE${NC}"
      ((total_loops_incomplete++))
      loop_status="INCOMPLETE"
  fi
  ```
- [ ] 3.2.8: Use Edit to update variable names throughout:
  - `passed_tests` → `completed_tests`
  - `total_loops_passed` → `total_loops_completed`
  - `total_loops_failed` → `total_loops_incomplete`
- [ ] 3.2.9: Use Edit to update final exit status logic (lines 523-531):
  ```bash
  # OLD:
  if [ $total_loops_failed -eq 0 ]; then
      echo -e "${GREEN}🎉 All ${LOOP_COUNT} loop(s) completed successfully!${NC}"
      echo -e "${GREEN}✅ CLI Regression Test: SUCCESS${NC}"
      exit 0
  else
      echo -e "${RED}❌ ${total_loops_failed} loop(s) failed${NC}"
      echo -e "${RED}❌ CLI Regression Test: FAILED${NC}"
      exit 1
  fi

  # NEW:
  if [ $total_loops_incomplete -eq 0 ]; then
      echo -e "${GREEN}🎉 All ${LOOP_COUNT} loop(s) generated responses!${NC}"
      echo -e "${GREEN}✅ Phase 1 Complete: All responses generated${NC}"
      echo -e "${YELLOW}🔴 PHASE 2 REQUIRED: Manual verification needed${NC}"
      exit 0
  else
      echo -e "${RED}❌ ${total_loops_incomplete} loop(s) incomplete${NC}"
      echo -e "${RED}❌ Phase 1: FAILED (some tests had no response)${NC}"
      exit 1
  fi
  ```

**Success Criteria:**
- ✅ All "PASS" replaced with "COMPLETED"
- ✅ All "FAILED" replaced with "INCOMPLETE" (for no response)
- ✅ Variable names updated consistently
- ✅ No remaining "pass" references in output

---

### Task 3.3: Add Phase 2 Verification Instructions to Script

**Status:** ⏳ PENDING
**Tool Requirements:** Sequential-Thinking → Read → Edit
**Estimated Time:** 20-30 minutes

**Subtasks:**

- [ ] 3.3.1: Use Sequential-Thinking to design Phase 2 instructions format
- [ ] 3.3.2: Use Edit to add Phase 2 instructions after loop completion (after line 466):
  ```bash
  echo ""
  echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║  PHASE 2: MANUAL VERIFICATION REQUIRED${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo -e "${YELLOW}🔴 CRITICAL: Test script can ONLY verify that responses were received.${NC}"
  echo -e "${YELLOW}   It CANNOT verify response correctness, tool calls, or formatting.${NC}"
  echo ""
  echo -e "${CYAN}📋 Phase 2 Verification Checklist (for AI Agent):${NC}"
  echo ""
  echo -e "${CYAN}For EACH of the 40 test responses, verify:${NC}"
  echo -e "  1. ✅ Response directly addresses the prompt query"
  echo -e "  2. ✅ Correct ticker symbols used (\$SPY, \$NVDA, \$WDC, \$AMD, \$SOUN)"
  echo -e "  3. ✅ Appropriate tool calls made (Polygon, Finnhub, Tradier)"
  echo -e "  4. ✅ Data formatting matches expected format (OHLC, tables, etc.)"
  echo -e "  5. ✅ No hallucinated data or made-up values"
  echo -e "  6. ✅ Options chains show Bid/Ask columns (NOT midpoint)"
  echo -e "  7. ✅ Technical analysis includes proper indicators"
  echo -e "  8. ✅ Response is complete (not truncated)"
  echo ""
  echo -e "${YELLOW}⚠️  MANDATORY CHECKPOINT QUESTION:${NC}"
  echo -e "${YELLOW}   \"Did you verify the results of EACH test prompt to ensure${NC}"
  echo -e "${YELLOW}    the response was correct with proper tool calls and formatting?\"${NC}"
  echo ""
  echo -e "${CYAN}📄 Review the test report: $OUTPUT_FILE${NC}"
  echo -e "${CYAN}📄 Review the raw output: $RAW_OUTPUT${NC}"
  echo ""
  ```

- [ ] 3.3.3: Use Edit to update header comments (lines 1-25) to explain two-phase approach:
  ```bash
  # CLI Test Regression Script - NEW 40-Test Suite with Two-Phase Validation
  #
  # PHASE 1 (Automated): Runs all 40 test prompts and generates responses
  # PHASE 2 (Manual): AI Agent must verify each response for correctness
  #
  # IMPORTANT: This script can ONLY verify that responses were received.
  # It CANNOT validate response correctness, tool calls, or data accuracy.
  # The AI Agent MUST manually review each of the 40 test responses.
  ```

**Success Criteria:**
- ✅ Phase 2 instructions clearly displayed after test completion
- ✅ 8-point verification checklist included
- ✅ Mandatory checkpoint question included
- ✅ Header comments explain two-phase approach
- ✅ File paths provided for manual review

---

### Task 3.4: Update CLAUDE.md Documentation

**Status:** ⏳ PENDING
**Tool Requirements:** Sequential-Thinking → Read → Edit
**Estimated Time:** 15-20 minutes

**Subtasks:**

- [ ] 3.4.1: Use Sequential-Thinking to plan CLAUDE.md updates
- [ ] 3.4.2: Use Read to review testing checkpoint section (lines 86-128)
- [ ] 3.4.3: Use Edit to update line 100:
  ```markdown
  # OLD:
  - PASS CRITERIA: CONTENT OF TEST PROMPT RESPONS MATCHES THE EXPECTED RESPONSE, PROPER TOOL CALLS, AND RESPONSE FORMATTING

  # NEW:
  - PHASE 1: Script generates responses (automated)
  - PHASE 2: Manually verify EACH response matches expected response, proper tool calls, and correct formatting
  ```
- [ ] 3.4.4: Use Edit to update line 109:
  ```markdown
  # OLD:
  - Show pass/fail counts (must be X/X PASS)

  # NEW:
  - Show completion counts (must be X/X responses generated)
  - Confirm Phase 2 manual verification completed
  ```
- [ ] 3.4.5: Use Edit to update line 124:
  ```markdown
  # OLD:
  - 100% pass rate achieved with Phase 2: Test Prompt Response Verification for EACH test completed

  # NEW:
  - Phase 1 complete: All responses generated (X/X)
  - Phase 2 complete: Manual verification of EACH response performed
  ```
- [ ] 3.4.6: Use Edit to add new section after line 128:
  ```markdown

  ## 🔴 CRITICAL: Understanding Test Validation

  **Phase 1 (Automated by Script):**
  - Script runs all 40 test prompts
  - Script verifies a response was received for each prompt
  - Script reports "X/X COMPLETED" meaning X responses generated
  - **Script CANNOT validate response correctness**

  **Phase 2 (Manual by AI Agent):**
  - AI Agent must review EACH of the 40 responses
  - Verify response addresses prompt correctly
  - Verify proper tool calls made
  - Verify data formatting correct (OHLC, tables, Bid/Ask)
  - Verify no hallucinated or made-up data
  - **This step is MANDATORY before claiming tests "passed"**

  **Key Insight:**
  The script saying "40/40 COMPLETED" means "40 responses received" NOT "40 tests passed validation". Only after Phase 2 manual verification can you claim tests passed.
  ```

**Success Criteria:**
- ✅ CLAUDE.md explains two-phase approach clearly
- ✅ "PASS" language replaced with "COMPLETED" + "manually verified"
- ✅ New section explains what script can/cannot validate
- ✅ Key insight provided for AI agents

---

### Task 3.5: Update testing_procedures.md Memory

**Status:** ⏳ PENDING
**Tool Requirements:** Sequential-Thinking → Serena read_memory → Serena write_memory
**Estimated Time:** 20-25 minutes

**Subtasks:**

- [ ] 3.5.1: Use Sequential-Thinking to plan memory updates
- [ ] 3.5.2: Use Serena read_memory to load current testing_procedures.md
- [ ] 3.5.3: Add new section after "CLI Regression Test Suite" section:
  ```markdown

  ### Two-Phase Testing Approach (CRITICAL)

  **Phase 1: Automated Response Generation**
  - Script runs all 40 test prompts sequentially
  - Script verifies each prompt received a response
  - Script reports "X/X COMPLETED" = X responses generated
  - **Limitation:** Script cannot validate response correctness

  **Phase 2: Manual Response Verification**
  - AI Agent MUST review each of the 40 responses
  - Verify against 8-point criteria (see checklist below)
  - Document any issues found
  - Fix issues and re-run Phase 1 if needed
  - **THIS PHASE IS MANDATORY**

  **8-Point Verification Criteria:**

  For EACH test response, verify:

  1. ✅ **Response Addresses Prompt**: Response directly answers the question
  2. ✅ **Correct Tickers**: Proper ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
  3. ✅ **Proper Tool Calls**: Polygon, Finnhub, or Tradier tools called appropriately
  4. ✅ **Data Formatting**: OHLC data, tables, options chains formatted correctly
  5. ✅ **No Hallucinations**: All data appears legitimate, no made-up numbers
  6. ✅ **Options Bid/Ask**: Options chains show Bid and Ask columns (NOT midpoint)
  7. ✅ **TA Indicators**: Technical analysis includes proper metrics
  8. ✅ **Completeness**: Response not truncated, no errors unless expected

  **Mandatory Checkpoint Question:**
  "Did you verify the results of EACH test prompt to ensure the response was correct with proper tool calls and formatting?"

  **If answer is NO:** You have NOT completed testing. Return to Phase 2.
  **If answer is YES:** Testing is complete, proceed to documentation updates.
  ```

- [ ] 3.5.4: Update all "PASS" references throughout memory to "COMPLETED + manually verified"
- [ ] 3.5.5: Update expected performance section to clarify:
  ```markdown
  **Expected Performance (Oct 12, 2025 - Two-Phase Validation):**
  - **Phase 1**: 40 responses generated, ~7-8 minutes
  - **Phase 2**: Manual verification, ~60-90 minutes (varies by AI agent speed)
  - **Success Criteria**: Phase 1: 40/40 completed, Phase 2: All responses verified correct
  ```
- [ ] 3.5.6: Use Serena write_memory to save updated testing_procedures.md

**Success Criteria:**
- ✅ Two-phase approach documented comprehensively
- ✅ 8-point criteria clearly defined
- ✅ Mandatory checkpoint question included
- ✅ All "PASS" references updated
- ✅ Expected performance reflects two phases

---

### Task 3.6: Update task_completion_checklist.md Memory

**Status:** ⏳ PENDING
**Tool Requirements:** Sequential-Thinking → Serena read_memory → Serena write_memory
**Estimated Time:** 10-15 minutes

**Subtasks:**

- [ ] 3.6.1: Use Sequential-Thinking to plan checklist updates
- [ ] 3.6.2: Use Serena read_memory to load task_completion_checklist.md
- [ ] 3.6.3: Update testing section (around line 30):
  ```markdown
  #### CLI Regression Testing (Two-Phase Approach)

  **Phase 1: Generate Responses (Automated)**
  ```bash
  # Run CLI regression test suite (40 tests)
  chmod +x test_cli_regression.sh && ./test_cli_regression.sh

  # Expected Phase 1 results:
  # - 40/40 responses COMPLETED (100% generation rate)
  # - Average response time: ~6-8 seconds
  # - Test report generated in test-reports/
  ```

  **Phase 2: Verify Responses (Manual - MANDATORY)**
  - ✅ Review EACH of the 40 test responses in test report
  - ✅ Verify against 8-point criteria (see testing_procedures.md)
  - ✅ Answer checkpoint question: "Did you verify each response?"
  - ✅ Document any issues found
  - ✅ Fix issues and re-run Phase 1 if needed
  ```

- [ ] 3.6.4: Update line 62:
  ```markdown
  # OLD:
  - ✅ Verify 100% pass rate

  # NEW:
  - ✅ Verify Phase 1: 40/40 responses generated
  - ✅ Complete Phase 2: Manual verification of all responses
  ```

- [ ] 3.6.5: Update "WRONG" example (around line 70):
  ```markdown
  **WRONG:**
  ```
  1. Create 5 new tools ✅
  2. Update test suite file ✅
  3. RUN test suite: chmod +x test_cli_regression.sh && ./test_cli_regression.sh ✅
  4. Show results: 40/40 COMPLETED ✅
  5. Update documentation ✅
  6. Mark task complete ❌ (NEVER performed Phase 2 manual verification!)
  ```
  ```

- [ ] 3.6.6: Update "CORRECT" example:
  ```markdown
  **CORRECT:**
  ```
  1. Create 5 new tools ✅
  2. Update test suite file ✅
  3. RUN Phase 1: chmod +x test_cli_regression.sh && ./test_cli_regression.sh ✅
  4. Show Phase 1 results: 40/40 COMPLETED ✅
  5. PERFORM Phase 2: Manual verification of all 40 responses ✅
  6. Answer checkpoint: "Did you verify each response?" YES ✅
  7. Provide test report path ✅
  8. Update documentation with test results ✅
  9. Mark task complete ✅
  ```
  ```

- [ ] 3.6.7: Use Serena write_memory to save updated task_completion_checklist.md

**Success Criteria:**
- ✅ Two-phase approach in checklist
- ✅ Phase 2 marked as MANDATORY
- ✅ Examples updated to show Phase 2
- ✅ Checkpoint question referenced

---

### Task 3.7: Update Other Documentation Files

**Status:** ⏳ PENDING
**Tool Requirements:** Sequential-Thinking → Read → Edit
**Estimated Time:** 15-20 minutes

**Subtasks:**

- [ ] 3.7.1: Use Sequential-Thinking to plan updates for remaining docs
- [ ] 3.7.2: Update AGENTS.md (line 64):
  ```markdown
  # OLD:
  4. **Test Verification** → Verify 100% pass rate

  # NEW:
  4. **Test Verification** → Phase 1: Generate responses, Phase 2: Manually verify each response
  ```

- [ ] 3.7.3: Update project_onboarding_summary.md memory (lines 150, 216, 431):
  ```markdown
  # Line 150:
  # OLD: # - 100% pass rate expected
  # NEW: # - Phase 1: All responses generated, Phase 2: Manual verification required

  # Line 216:
  # OLD: 3. ✅ **Testing**: Run `./test_cli_regression.sh` (38 tests, must show 100% pass rate)
  # NEW: 3. ✅ **Testing**: Run `./test_cli_regression.sh` (40 tests, Phase 1: generate responses, Phase 2: verify manually)

  # Line 431:
  # OLD: ✅ **DO**: Run test suite, show 100% pass rate
  # NEW: ✅ **DO**: Run test suite (Phase 1), manually verify all responses (Phase 2)
  ```

- [ ] 3.7.4: Update docs/task_templates/new_research_details_template.md (line 90):
  ```markdown
  # OLD:
  - 100% pass rate achieved

  # NEW:
  - Phase 1: All responses generated successfully
  - Phase 2: Manual verification of all responses completed
  ```

**Success Criteria:**
- ✅ AGENTS.md updated
- ✅ project_onboarding_summary.md updated (3 locations)
- ✅ new_research_details_template.md updated
- ✅ Consistent language across all docs

---

## Phase 4: Testing

### Task 4.1: Execute test_cli_regression.sh (Phase 1)

**Status:** ⏳ PENDING
**Tool Requirements:** Bash
**Estimated Time:** 7-8 minutes

**Subtasks:**

- [ ] 4.1.1: Run test script:
  ```bash
  chmod +x test_cli_regression.sh && ./test_cli_regression.sh
  ```
- [ ] 4.1.2: Monitor output for completion
- [ ] 4.1.3: Verify test report generated in test-reports/
- [ ] 4.1.4: Note completion count (should be 40/40)
- [ ] 4.1.5: Note average response time
- [ ] 4.1.6: Save test report path for commit

**Success Criteria:**
- ✅ Script completes without errors
- ✅ 40/40 responses generated
- ✅ Test report created
- ✅ Phase 2 instructions displayed

---

### Task 4.2: Perform Phase 2 Manual Verification

**Status:** ⏳ PENDING
**Tool Requirements:** Read → Sequential-Thinking
**Estimated Time:** 60-90 minutes

**Subtasks:**

- [ ] 4.2.1: Use Read to open test report file
- [ ] 4.2.2: Use Sequential-Thinking to create verification tracking system
- [ ] 4.2.3: For EACH of 40 tests, verify 8-point criteria:

**Verification Template (use for each test):**
```
Test #: _____
Prompt: _____
✅/❌ 1. Response addresses prompt
✅/❌ 2. Correct ticker symbols
✅/❌ 3. Proper tool calls
✅/❌ 4. Data formatting correct
✅/❌ 5. No hallucinations
✅/❌ 6. Options Bid/Ask (if applicable)
✅/❌ 7. TA indicators (if applicable)
✅/❌ 8. Complete response
Issues Found: _____
```

- [ ] 4.2.4: Document ALL issues found in verification notes
- [ ] 4.2.5: Create summary of verification results
- [ ] 4.2.6: Answer checkpoint question: "Did you verify each response?" YES/NO

**Success Criteria:**
- ✅ All 40 tests verified against 8-point criteria
- ✅ All issues documented
- ✅ Verification notes created
- ✅ Checkpoint question answered YES

---

### Task 4.3: Fix Issues and Re-Test (If Needed)

**Status:** ⏳ PENDING (conditional)
**Tool Requirements:** Varies based on issues
**Estimated Time:** Varies (30-120 minutes)

**Subtasks:**

- [ ] 4.3.1: If issues found in Phase 2, categorize by type:
  - Agent instruction issues
  - Tool implementation issues
  - Prompt wording issues
  - Data format issues

- [ ] 4.3.2: Fix each issue category systematically
- [ ] 4.3.3: Re-run Phase 1: `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
- [ ] 4.3.4: Re-perform Phase 2 verification for affected tests
- [ ] 4.3.5: Repeat until all 40 tests verify correctly

**Success Criteria:**
- ✅ All issues resolved
- ✅ Phase 1 re-run successful
- ✅ Phase 2 re-verification shows all tests correct

---

## Phase 5: Final Atomic Commit

### Task 5.1: Verify ALL Work Complete (DO NOT STAGE YET)

**Status:** ⏳ PENDING
**Tool Requirements:** Bash (git status, git diff)
**Estimated Time:** 5 minutes

**Subtasks:**

- [ ] 5.1.1: Verify all code changes complete
- [ ] 5.1.2: Verify all tests run and verified
- [ ] 5.1.3: Verify all documentation updated
- [ ] 5.1.4: Verify test report exists
- [ ] 5.1.5: Run: `git status` to review all changed files
- [ ] 5.1.6: Run: `git diff` to review all changes
- [ ] 5.1.7: **DO NOT RUN git add YET**

**Success Criteria:**
- ✅ All tasks 3.1-3.7 complete
- ✅ All tasks 4.1-4.3 complete
- ✅ Test report generated
- ✅ All files present in git status

---

### Task 5.2: Stage Everything at Once

**Status:** ⏳ PENDING
**Tool Requirements:** Bash (git add)
**Estimated Time:** 1 minute

**Subtasks:**

- [ ] 5.2.1: Run ONCE: `git add -A`
- [ ] 5.2.2: Immediately verify: `git status`
- [ ] 5.2.3: Ensure ALL files staged, NOTHING unstaged

**Success Criteria:**
- ✅ All files staged in ONE command
- ✅ No unstaged files remaining
- ✅ Ready for immediate commit

---

### Task 5.3: Commit Immediately (Within 60 seconds)

**Status:** ⏳ PENDING
**Tool Requirements:** Bash (git commit)
**Estimated Time:** 2 minutes

**Subtasks:**

- [ ] 5.3.1: Run immediately after staging:
  ```bash
  git commit -m "$(cat <<'EOF'
  [TEST-FRAMEWORK] Two-Phase Test Validation Framework Implementation

  **Problem:** Test script reported "PASS" for any response received, regardless
  of correctness. This created false confidence where tests showed "40/40 PASSED"
  but responses could have hallucinated data, wrong tool calls, or incorrect formatting.

  **Solution:** Implemented two-phase testing approach:
  - Phase 1 (Automated): Script generates all 40 responses, reports "X/X COMPLETED"
  - Phase 2 (Manual): AI Agent verifies each response against 8-point criteria

  **Changes:**

  **Test Script (test_cli_regression.sh):**
  - Updated prompts array to new 40-prompt format with explicit OHLC terminology
  - Removed ALL "PASS/FAIL" terminology, replaced with "COMPLETED/INCOMPLETE"
  - Added Phase 2 verification instructions with 8-point checklist
  - Added mandatory checkpoint question for AI agents
  - Updated variable names: passed_tests → completed_tests
  - Updated header comments to explain two-phase approach

  **Documentation Updates:**
  - CLAUDE.md: Added section explaining what script can/cannot validate
  - AGENTS.md: Updated test verification language
  - testing_procedures.md: Added comprehensive two-phase documentation
  - task_completion_checklist.md: Updated examples to include Phase 2
  - project_onboarding_summary.md: Updated 3 references to testing approach
  - new_research_details_template.md: Updated testing language

  **Test Results:**
  - Phase 1: 40/40 responses generated successfully
  - Phase 2: Manual verification completed for all 40 responses
  - Average response time: [INSERT TIME]s
  - Test report: [INSERT TEST REPORT PATH]
  - Verification notes: All responses verified correct

  **Files Modified:**
  - test_cli_regression.sh (prompts, logic, output)
  - CLAUDE.md (testing sections)
  - AGENTS.md (test verification)
  - .serena/memories/testing_procedures.md
  - .serena/memories/task_completion_checklist.md
  - .serena/memories/project_onboarding_summary.md
  - docs/task_templates/new_research_details_template.md
  - research_task_plan.md (new)
  - TODO_task_plan.md (new)
  - [TEST REPORT FILE] (new)

  **Impact:**
  - Eliminates false positive "PASS" reports
  - Forces manual verification of response correctness
  - Provides clear 8-point criteria for validation
  - Improves AI agent understanding of test results
  - Reduces confusion about what "passed" means

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>
  EOF
  )"
  ```

**Success Criteria:**
- ✅ Commit created within 60 seconds of staging
- ✅ Commit message includes test results
- ✅ Commit message lists all files changed

---

### Task 5.4: Push Immediately

**Status:** ⏳ PENDING
**Tool Requirements:** Bash (git push)
**Estimated Time:** 1 minute

**Subtasks:**

- [ ] 5.4.1: Run immediately after commit: `git push`
- [ ] 5.4.2: Verify push succeeded: `git log -1`
- [ ] 5.4.3: Verify branch up to date: `git status`

**Success Criteria:**
- ✅ Push completed successfully
- ✅ Commit appears in git log
- ✅ Branch up to date with origin

---

## Summary Checklist

**Before claiming task complete, verify ALL items:**

### Phase 3: Implementation
- [ ] 3.1: Test prompts updated (40 new prompts)
- [ ] 3.2: "PASS" terminology removed from script
- [ ] 3.3: Phase 2 instructions added to script
- [ ] 3.4: CLAUDE.md updated
- [ ] 3.5: testing_procedures.md memory updated
- [ ] 3.6: task_completion_checklist.md memory updated
- [ ] 3.7: Other docs updated (AGENTS.md, etc.)

### Phase 4: Testing
- [ ] 4.1: Phase 1 test execution (40/40 responses)
- [ ] 4.2: Phase 2 manual verification (all 40 tests)
- [ ] 4.3: Issues fixed and re-tested (if needed)

### Phase 5: Commit
- [ ] 5.1: All work verified complete (no staging yet)
- [ ] 5.2: All files staged at once (git add -A)
- [ ] 5.3: Committed immediately (within 60s)
- [ ] 5.4: Pushed immediately

---

**END OF TODO TASK PLAN**
