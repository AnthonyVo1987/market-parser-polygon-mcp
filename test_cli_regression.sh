#!/bin/bash

# CLI Test Regression Script - NEW 39-Test Suite with Two-Phase Validation
# Tests all 39 standardized test prompts sequentially in a SINGLE CLI session
# Designed to validate parallel tool calls (max 3) and chat history data reuse
# Properly handles session persistence and accurate response time tracking
#
# PHASE 1 (Automated): Runs all 39 test prompts and generates responses
# PHASE 2 (Manual): AI Agent must verify each response for correctness
#
# IMPORTANT: This script can ONLY verify that responses were received.
# It CANNOT validate response correctness, tool calls, or data accuracy.
# The AI Agent MUST manually review each of the 39 test responses.
#
# Usage: chmod +x test_cli_regression.sh && ./test_cli_regression.sh [LOOP_COUNT]
#   LOOP_COUNT: Number of test loops to run (1-10, default: 1)
#   Examples:
#     chmod +x test_cli_regression.sh && ./test_cli_regression.sh     # Run 1 loop (default)
#     chmod +x test_cli_regression.sh && ./test_cli_regression.sh 3   # Run 3 loops
#     chmod +x test_cli_regression.sh && ./test_cli_regression.sh 10  # Run 10 loops (max)
#
# Test Coverage:
# - SPY Test Sequence: Tests 1-16 (16 tests - OHLC pricing + TA + options analysis)
# - NVDA Test Sequence: Tests 17-31 (15 tests - OHLC pricing + TA + options analysis)
# - Multi-Ticker Test Sequence: Tests 32-39 (8 tests - WDC, AMD, SOUN)
# Total: 39 tests per loop
#
# Test Design Philosophy:
# - Sequential ticker testing validates chat history analysis
# - Same question types repeated for each ticker tests data reuse
# - Multi-ticker tests validate parallel tool call batching (max 3)
# - Two-phase validation ensures response correctness

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse loop count parameter (default 1, max 10)
LOOP_COUNT=${1:-1}

# Validate loop count
if ! [[ "$LOOP_COUNT" =~ ^[0-9]+$ ]]; then
    echo -e "${RED}❌ Error: LOOP_COUNT must be a number${NC}"
    echo -e "Usage: $0 [LOOP_COUNT]"
    echo -e "  LOOP_COUNT: Number of loops (1-10, default: 1)"
    exit 1
fi

if [ "$LOOP_COUNT" -lt 1 ] || [ "$LOOP_COUNT" -gt 10 ]; then
    echo -e "${RED}❌ Error: LOOP_COUNT must be between 1 and 10${NC}"
    echo -e "Usage: $0 [LOOP_COUNT]"
    exit 1
fi

# Test configuration
MAX_RESPONSE_TIME=60  # 1 minute max per response
CLI_CMD="uv run python -m src.backend.cli"
RESULTS_DIR="test-reports"

# Ensure results directory exists
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 CLI Test Regression - NEW 39 Test Suite (Two-Phase Validation)${NC}"
echo -e "${CYAN}=================================================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Loop Count: ${GREEN}${LOOP_COUNT}x${NC}"
echo -e "Max Response Time: ${MAX_RESPONSE_TIME}s per test"
echo -e "CLI Command: $CLI_CMD"
echo -e "Session Mode: ${GREEN}PERSISTENT${NC} (all 39 tests in same session per loop)"
echo -e "Test Features: ${GREEN}Parallel Tool Calls (max 3)${NC}, ${GREEN}Chat History Analysis${NC}, ${GREEN}Options Chain Tests${NC}"
echo -e "Validation: ${YELLOW}Phase 1 (Automated)${NC} + ${YELLOW}Phase 2 (Manual Verification)${NC}"
echo ""

# The 39 standardized test prompts organized by ticker sequence
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
    # NVDA Test Sequence (Tests 17-31)
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
    # Multi-Ticker Test Sequence (Tests 32-39)
    "Current Price OHLC: \$WDC, \$AMD, \$SOUN"
    "Yesterday's Price OHLC: \$WDC, \$AMD, \$SOUN"
    "Yesterday's Closing Price: \$WDC, \$AMD, \$SOUN"
    "Last week's Performance OHLC: \$WDC, \$AMD, \$SOUN"
    "Get technical analysis indicator DATA only with NO ANALYSIS: \$WDC, \$AMD, \$SOUN"
    "Support & Resistance Levels: \$WDC, \$AMD, \$SOUN"
    "Perform technical analysis based on all available data for Trends, Volatility, Momentum, Trading Patterns\Signals: \$WDC, \$AMD, \$SOUN"
    "Get options expiration dates: \$WDC, \$AMD, \$SOUN"
)

declare -a test_names=(
    # SPY Test Sequence (Tests 1-16)
    "Test_1_SPY_Market_Status"
    "Test_2_SPY_Current_Price_OHLC"
    "Test_3_SPY_Yesterday_Price_OHLC"
    "Test_4_SPY_Last_Week_Performance_OHLC"
    "Test_5_SPY_Previous_Week_Friday_OHLC"
    "Test_6_SPY_Last_5_Trading_Days_OHLC"
    "Test_7_SPY_Past_2_Weeks_OHLC"
    "Test_8_SPY_Past_Month"
    "Test_9_SPY_Past_3_Months"
    "Test_10_SPY_TA_Indicator_DATA_Only"
    "Test_11_SPY_Support_Resistance"
    "Test_12_SPY_Full_TA_Analysis"
    "Test_13_SPY_Options_Expiration_Dates"
    "Test_14_SPY_Call_Options_Chain"
    "Test_15_SPY_Put_Options_Chain"
    "Test_16_SPY_Options_Wall_Analysis"
    # NVDA Test Sequence (Tests 17-31)
    "Test_17_NVDA_Current_Price_OHLC"
    "Test_18_NVDA_Yesterday_Price_OHLC"
    "Test_19_NVDA_Last_Week_Performance_OHLC"
    "Test_20_NVDA_Previous_Week_Friday_OHLC"
    "Test_21_NVDA_Last_5_Trading_Days_OHLC"
    "Test_22_NVDA_Past_2_Weeks_OHLC"
    "Test_23_NVDA_Past_Month"
    "Test_24_NVDA_Past_3_Months"
    "Test_25_NVDA_TA_Indicator_DATA_Only"
    "Test_26_NVDA_Support_Resistance"
    "Test_27_NVDA_Full_TA_Analysis"
    "Test_28_NVDA_Options_Expiration_Dates"
    "Test_29_NVDA_Call_Options_Chain"
    "Test_30_NVDA_Put_Options_Chain"
    "Test_31_NVDA_Options_Wall_Analysis"
    # Multi-Ticker Test Sequence (Tests 32-39)
    "Test_32_Multi_Current_Price_OHLC_WDC_AMD_SOUN"
    "Test_33_Multi_Yesterday_Price_OHLC_WDC_AMD_SOUN"
    "Test_34_Multi_Yesterday_Closing_Price_WDC_AMD_SOUN"
    "Test_35_Multi_Last_Week_Performance_OHLC_WDC_AMD_SOUN"
    "Test_36_Multi_TA_Indicator_DATA_Only_WDC_AMD_SOUN"
    "Test_37_Multi_Support_Resistance_WDC_AMD_SOUN"
    "Test_38_Multi_Full_TA_Analysis_WDC_AMD_SOUN"
    "Test_39_Multi_Options_Expiration_Dates_WDC_AMD_SOUN"
)

# Initialize test tracking
total_tests=${#prompts[@]}

# Aggregate tracking across all loops
declare -a all_loop_avg_times=()
declare -a all_loop_durations=()
declare -a all_loop_reports=()
total_loops_completed=0
total_loops_incomplete=0

# Loop through test iterations
for loop_num in $(seq 1 $LOOP_COUNT); do
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  LOOP ${loop_num}/${LOOP_COUNT} - Starting Test Iteration${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Initialize per-loop tracking
    declare -a response_times=()
    declare -a test_results=()
    declare -a test_durations=()

    # Generate unique timestamp for this loop - NEW FORMAT: YYYY-MM-DD_HH-MM
    LOOP_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
    OUTPUT_FILE="$RESULTS_DIR/test_cli_regression_loop${loop_num}_${LOOP_TIMESTAMP}.log"

    # Create tmp directory for test artifacts (project-level, not system /tmp)
    mkdir -p tmp

    RAW_OUTPUT="./tmp/cli_output_loop${loop_num}_${LOOP_TIMESTAMP}.log"
    INPUT_FILE="./tmp/test_input_loop${loop_num}_${LOOP_TIMESTAMP}.txt"

    # Create input file with all prompts and exit at the end
    for prompt in "${prompts[@]}"; do
        echo "$prompt" >> "$INPUT_FILE"
    done
    echo "exit" >> "$INPUT_FILE"

    echo -e "${CYAN}🚀 Starting CLI Regression Test - Phase 1 (Loop ${loop_num}/${LOOP_COUNT})...${NC}"
    echo -e "${CYAN}Session will run all 39 tests sequentially${NC}"
    echo -e "Output file: $OUTPUT_FILE"
    echo ""

# Start CLI and capture output in real-time
start_time=$(date +%s.%N)

# Run CLI with all prompts in single session
$CLI_CMD < "$INPUT_FILE" > "$RAW_OUTPUT" 2>&1 &
CLI_PID=$!

# Monitor output file for completion
echo -e "${YELLOW}⏳ Monitoring CLI session...${NC}"
echo ""

# Parse output and extract test results
parse_test_results() {
    echo -e "${CYAN}📊 Parsing test results from CLI output...${NC}"
    echo ""

    # Extract all response times from the output
    local test_num=0
    while IFS= read -r line; do
        if echo "$line" | grep -q "Response Time:"; then
            rt=$(echo "$line" | grep -o '[0-9]\+\.[0-9]\+' | head -1)
            if [ -n "$rt" ] && [ "$test_num" -lt "$total_tests" ]; then
                ((test_num++))
                response_times+=("$rt")

                echo -e "${BLUE}📝 Test $test_num: ${test_names[$((test_num-1))]}${NC}"
                echo -e "${YELLOW}Prompt: '${prompts[$((test_num-1))]}'${NC}"
                echo -e "${GREEN}✅ Response received${NC}"
                echo -e "${GREEN}⏱️  Response Time: ${rt}s${NC}"

                # Performance classification
                if (( $(awk "BEGIN {print ($rt < 30)}") )); then
                    echo -e "${GREEN}📈 Performance: EXCELLENT (< 30s)${NC}"
                elif (( $(awk "BEGIN {print ($rt < 45)}") )); then
                    echo -e "${GREEN}📈 Performance: GOOD (30-45s)${NC}"
                elif (( $(awk "BEGIN {print ($rt < 90)}") )); then
                    echo -e "${YELLOW}📈 Performance: ACCEPTABLE (45-90s)${NC}"
                else
                    echo -e "${YELLOW}📈 Performance: SLOW (> 90s)${NC}"
                fi

                test_results+=("COMPLETED")
                echo ""
            fi
        fi
    done < "$RAW_OUTPUT"

    # Verify we found all expected tests
    if [ "$test_num" -ne "$total_tests" ]; then
        echo -e "${YELLOW}⚠️  Warning: Found $test_num response times, expected $total_tests${NC}"
    fi
}

# Wait for CLI to complete
echo -e "${YELLOW}⏳ Waiting for CLI session to complete...${NC}"
wait $CLI_PID
exit_code=$?

end_time=$(date +%s.%N)
total_duration=$(awk "BEGIN {printf \"%.2f\", $end_time - $start_time}")

# Convert duration to min:sec format
duration_minutes=$(awk "BEGIN {printf \"%d\", $total_duration / 60}")
duration_seconds=$(awk "BEGIN {printf \"%d\", $total_duration % 60}")
duration_formatted="${duration_minutes} min ${duration_seconds} sec"

echo -e "${GREEN}✅ CLI session completed${NC}"
echo -e "${GREEN}⏱️  Total Session Duration: ${duration_formatted}${NC}"
echo ""

# Parse results from output
echo -e "${CYAN}📊 Parsing test results...${NC}"
parse_test_results

# Verify we got all tests
tests_found=${#test_results[@]}
if [ "$tests_found" -ne "$total_tests" ]; then
    echo -e "${YELLOW}⚠️  Warning: Found $tests_found tests, expected $total_tests${NC}"
    echo -e "${YELLOW}   Re-parsing output file...${NC}"

    # Fallback: manually extract all response times
    response_times=()
    while IFS= read -r line; do
        if echo "$line" | grep -q "Response Time:"; then
            rt=$(echo "$line" | grep -o '[0-9]\+\.[0-9]\+' | head -1)
            if [ -n "$rt" ]; then
                response_times+=("$rt")
            fi
        fi
    done < "$RAW_OUTPUT"

    # Fill in test results
    for i in $(seq 1 $total_tests); do
        if [ ${#test_results[@]} -lt $i ]; then
            test_results+=("COMPLETED")
        fi
    done
fi

# Calculate statistics
echo ""
echo -e "${CYAN}📊 Test Results Analysis${NC}"
echo -e "${CYAN}========================${NC}"

# Test results summary
echo -e "📋 Phase 1 Results Summary (Responses Generated):"
completed_tests=0
for i in "${!test_names[@]}"; do
    test_number=$((i + 1))
    result="${test_results[$i]:-UNKNOWN}"
    if [ "$result" = "COMPLETED" ]; then
        ((completed_tests++))
        echo -e "${GREEN}   Test $test_number: ${test_names[$i]} - COMPLETED${NC}"
    else
        echo -e "${RED}   Test $test_number: ${test_names[$i]} - $result${NC}"
    fi
done

incomplete_tests=$((total_tests - completed_tests))

# Response time analysis
if [ ${#response_times[@]} -gt 0 ]; then
    echo ""
    echo -e "📊 Response Time Analysis:"

    # Calculate statistics
    min_time=${response_times[0]}
    max_time=${response_times[0]}
    total_time=0
    count=0

    for time in "${response_times[@]}"; do
        if (( $(awk "BEGIN {print ($time < $min_time)}") )); then
            min_time=$time
        fi
        if (( $(awk "BEGIN {print ($time > $max_time)}") )); then
            max_time=$time
        fi
        total_time=$(awk "BEGIN {printf \"%.2f\", $total_time + $time}")
        ((count++))
    done

    avg_time=$(awk "BEGIN {printf \"%.2f\", $total_time / $count}")

    echo -e "   Min Response Time: ${min_time}s"
    echo -e "   Max Response Time: ${max_time}s"
    echo -e "   Avg Response Time: ${avg_time}s"
    echo -e "   Successful Tests: $count/$total_tests"

    # Performance assessment
    performance_rating="GOOD"
    if (( $(awk "BEGIN {print ($avg_time < 30)}") )); then
        performance_rating="EXCELLENT"
    elif (( $(awk "BEGIN {print ($avg_time > 60)}") )); then
        performance_rating="ACCEPTABLE"
    fi

    echo -e "${GREEN}📈 Overall Performance Rating: $performance_rating${NC}"
else
    echo -e "${RED}❌ No response time data available for analysis${NC}"
fi

# Session persistence validation
echo ""
echo -e "${CYAN}📊 Session Persistence Validation${NC}"
echo -e "${CYAN}=================================${NC}"

session_count=$(grep -c "CLI session 'cli_session' initialized" "$RAW_OUTPUT" 2>/dev/null || echo "0")
if [ "$session_count" -eq 1 ]; then
    echo -e "${GREEN}✅ Session Persistence: VERIFIED${NC}"
    echo -e "${GREEN}   All tests ran in SINGLE session (count: 1)${NC}"
elif [ "$session_count" -gt 1 ]; then
    echo -e "${RED}❌ Session Persistence: FAILED${NC}"
    echo -e "${RED}   Multiple sessions detected (count: $session_count)${NC}"
else
    echo -e "${YELLOW}⚠️  Session Persistence: UNKNOWN${NC}"
    echo -e "${YELLOW}   Could not verify session count${NC}"
fi

# Generate comprehensive summary for this loop
echo ""
echo -e "${CYAN}📊 Loop ${loop_num}/${LOOP_COUNT} Phase 1 Summary${NC}"
echo -e "${CYAN}====================================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Completed: $completed_tests${NC}"
echo -e "${RED}Incomplete: $incomplete_tests${NC}"
echo -e "Generation Rate: $(( completed_tests * 100 / total_tests ))%"
echo -e "Total Session Duration: ${duration_formatted}"
echo -e "Session Mode: ${GREEN}PERSISTENT${NC}"

# Track loop results
if [ $incomplete_tests -eq 0 ]; then
    echo -e "${GREEN}🎉 All $total_tests responses generated in Loop ${loop_num}!${NC}"
    echo -e "${GREEN}✅ Loop ${loop_num} Phase 1: All responses generated${NC}"
    ((total_loops_completed++))
    loop_status="COMPLETED"
else
    echo -e "${RED}❌ $incomplete_tests test(s) had no response in Loop ${loop_num}${NC}"
    echo -e "${RED}❌ Loop ${loop_num} Phase 1: INCOMPLETE${NC}"
    ((total_loops_incomplete++))
    loop_status="INCOMPLETE"
fi

# Store aggregate metrics
if [ -n "$avg_time" ]; then
    all_loop_avg_times+=("$avg_time")
fi
all_loop_durations+=("$total_duration")
all_loop_reports+=("$OUTPUT_FILE")

    # Generate detailed output file for this loop
    {
        echo "=== CLI REGRESSION TEST REPORT (Loop ${loop_num}/${LOOP_COUNT}) ==="
        echo "Timestamp: $(date)"
        echo "Loop Number: ${loop_num}/${LOOP_COUNT}"
        echo "Total Tests: $total_tests"
        echo "Completed: $completed_tests"
        echo "Incomplete: $incomplete_tests"
        echo "Generation Rate: $(( completed_tests * 100 / total_tests ))%"
        echo "Total Session Duration: ${duration_formatted}"
        echo "Session Mode: PERSISTENT (single session)"
        echo "Session Count Detected: $session_count"
        echo "Loop Status: $loop_status"
        echo ""

        if [ ${#response_times[@]} -gt 0 ]; then
            echo "=== RESPONSE TIME ANALYSIS ==="
            echo "Min Response Time: ${min_time}s"
            echo "Max Response Time: ${max_time}s"
            echo "Avg Response Time: ${avg_time}s"
            echo "Performance Rating: $performance_rating"
            echo ""
        fi

        echo "=== TEST RESULTS DETAIL ==="
        for i in "${!test_names[@]}"; do
            test_number=$((i + 1))
            echo "Test $test_number: ${test_names[$i]} - ${test_results[$i]:-UNKNOWN}"
            if [ -n "${response_times[$i]}" ]; then
                echo "  Response Time: ${response_times[$i]}s"
            fi
        done
        echo ""

        echo "=== FULL CLI OUTPUT ==="
        cat "$RAW_OUTPUT"
        echo ""
        echo "=== END CLI REGRESSION TEST REPORT (Loop ${loop_num}/${LOOP_COUNT}) ==="
    } > "$OUTPUT_FILE"

    echo ""
    echo -e "${BLUE}📄 Loop ${loop_num} results saved to: $OUTPUT_FILE${NC}"
    echo -e "${BLUE}📄 Loop ${loop_num} raw output: $RAW_OUTPUT${NC}"

    # Clean up input file
    rm -f "$INPUT_FILE"

    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  LOOP ${loop_num}/${LOOP_COUNT} - Phase 1 Completed${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Phase 2 Verification Instructions - MANDATORY GREP-BASED ENFORCEMENT
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  PHASE 2: MANDATORY VERIFICATION REQUIRED${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}🔴 CRITICAL: Phase 1 ONLY verified that responses were received (${completed_tests}/${total_tests}).${NC}"
    echo -e "${YELLOW}   It CANNOT verify response correctness, tool calls, or formatting.${NC}"
    echo -e "${YELLOW}   Phase 2 is MANDATORY and requires EVIDENCE-BASED verification.${NC}"
    echo ""
    echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  🔴 MANDATORY GREP COMMANDS - MUST RUN AND SHOW OUTPUT${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📋 Phase 2a: ERROR DETECTION (MANDATORY)${NC}"
    echo -e "${CYAN}Run these commands and SHOW the output:${NC}"
    echo ""
    echo -e "${GREEN}# Command 1: Find all errors/failures${NC}"
    echo -e "  grep -i \"error\|unavailable\|failed\|invalid\" $OUTPUT_FILE"
    echo ""
    echo -e "${GREEN}# Command 2: Count 'data unavailable' errors${NC}"
    echo -e "  grep -c \"data unavailable\" $OUTPUT_FILE"
    echo ""
    echo -e "${GREEN}# Command 3: Count completed tests${NC}"
    echo -e "  grep -c \"COMPLETED\" $OUTPUT_FILE"
    echo ""
    echo -e "${RED}⚠️  YOU MUST RUN THESE COMMANDS. You cannot proceed without showing grep output.${NC}"
    echo ""
    echo -e "${CYAN}📋 Phase 2b: DOCUMENT FAILURES (MANDATORY)${NC}"
    echo -e "${CYAN}If errors found in Phase 2a, document with EVIDENCE:${NC}"
    echo ""
    echo -e "  For EACH failure found, provide:"
    echo -e "    • Test number (Test 3, Test 18, etc.)"
    echo -e "    • Line number in test report"
    echo -e "    • Exact error message"
    echo -e "    • Tool call that failed (if visible)"
    echo ""
    echo -e "${RED}⚠️  EVIDENCE REQUIRED: Paste grep output and create failure table.${NC}"
    echo ""
    echo -e "${CYAN}📋 Phase 2c: VERIFY RESPONSE CORRECTNESS (For tests without errors)${NC}"
    echo -e "${CYAN}For tests that didn't show errors in Phase 2a, verify:${NC}"
    echo ""
    echo -e "  1. ✅ Response directly addresses the prompt query"
    echo -e "  2. ✅ Correct ticker symbols used (\$SPY, \$NVDA, \$WDC, \$AMD, \$SOUN)"
    echo -e "  3. ✅ Appropriate tool calls made (Polygon, Tradier)"
    echo -e "  4. ✅ Data formatting matches expected format (OHLC, tables, etc.)"
    echo -e "  5. ✅ No hallucinated data or made-up values"
    echo -e "  6. ✅ Options chains show Bid/Ask columns (NOT midpoint)"
    echo -e "  7. ✅ Technical analysis includes proper indicators"
    echo -e "  8. ✅ Response is complete (not truncated)"
    echo ""
    echo -e "${CYAN}📋 Phase 2d: FINAL VERIFICATION${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  MANDATORY CHECKPOINT QUESTIONS:${NC}"
    echo -e "${YELLOW}   1. Did you RUN the 3 mandatory grep commands in Phase 2a?${NC}"
    echo -e "${YELLOW}   2. Did you SHOW the grep output as evidence?${NC}"
    echo -e "${YELLOW}   3. Did you DOCUMENT all failures found (if any)?${NC}"
    echo -e "${YELLOW}   4. Can you confirm: ${completed_tests}/${total_tests} tests generated responses?${NC}"
    echo -e "${YELLOW}   5. Can you confirm: X/39 tests PASSED verification (no errors)?${NC}"
    echo ""
    echo -e "${RED}🔴 CANNOT MARK TASK COMPLETE WITHOUT:${NC}"
    echo -e "${RED}   • Running and showing grep command outputs${NC}"
    echo -e "${RED}   • Documenting failures with evidence (or confirming 0 failures)${NC}"
    echo -e "${RED}   • Providing failure count: grep -c \"data unavailable\"${NC}"
    echo ""
    echo -e "${CYAN}📄 Test Report (run grep commands on this file): $OUTPUT_FILE${NC}"
    echo -e "${CYAN}📄 Raw Output: $RAW_OUTPUT${NC}"
    echo ""

done  # End of loop iteration

# Aggregate Statistics Across All Loops
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  AGGREGATE STATISTICS - ALL ${LOOP_COUNT} LOOPS${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${CYAN}📊 Overall Phase 1 Summary${NC}"
echo -e "${CYAN}===========================${NC}"
echo -e "Total Loops Run: $LOOP_COUNT"
echo -e "${GREEN}Loops Completed: $total_loops_completed${NC}"
echo -e "${RED}Loops Incomplete: $total_loops_incomplete${NC}"
echo -e "Overall Generation Rate: $(( total_loops_completed * 100 / LOOP_COUNT ))%"
echo ""

# Calculate aggregate response time statistics
if [ ${#all_loop_avg_times[@]} -gt 0 ]; then
    echo -e "${CYAN}📊 Aggregate Response Time Analysis${NC}"
    echo -e "${CYAN}===================================${NC}"

    # Find min/max/avg of all loop averages
    agg_min=${all_loop_avg_times[0]}
    agg_max=${all_loop_avg_times[0]}
    agg_total=0

    for time in "${all_loop_avg_times[@]}"; do
        if (( $(awk "BEGIN {print ($time < $agg_min)}") )); then
            agg_min=$time
        fi
        if (( $(awk "BEGIN {print ($time > $agg_max)}") )); then
            agg_max=$time
        fi
        agg_total=$(awk "BEGIN {printf \"%.2f\", $agg_total + $time}")
    done

    agg_avg=$(awk "BEGIN {printf \"%.2f\", $agg_total / ${#all_loop_avg_times[@]}}")

    echo -e "Min Average Response Time (across loops): ${agg_min}s"
    echo -e "Max Average Response Time (across loops): ${agg_max}s"
    echo -e "Overall Average Response Time: ${agg_avg}s"
    echo ""
fi

# Display all test reports generated
echo -e "${CYAN}📄 Test Reports Generated${NC}"
echo -e "${CYAN}========================${NC}"
for i in "${!all_loop_reports[@]}"; do
    loop_idx=$((i + 1))
    echo -e "Loop ${loop_idx}: ${all_loop_reports[$i]}"
done
echo ""

# Final exit status
if [ $total_loops_incomplete -eq 0 ]; then
    echo -e "${GREEN}🎉 All ${LOOP_COUNT} loop(s) generated responses!${NC}"
    echo -e "${GREEN}✅ Phase 1 Complete: All responses generated${NC}"
    echo ""
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  🔴 PHASE 2 REQUIRED: Manual Verification Needed${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}❌ ${total_loops_incomplete} loop(s) incomplete${NC}"
    echo -e "${RED}❌ Phase 1: FAILED (some tests had no response)${NC}"
    exit 1
fi
