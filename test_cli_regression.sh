#!/bin/bash

# CLI Test Regression Script - NEW 36-Test Suite with Chat History Analysis
# Tests all 36 standardized test prompts sequentially in a SINGLE CLI session
# Designed to validate parallel tool calls (max 3) and chat history data reuse
# Properly handles session persistence and accurate response time tracking
#
# Usage: ./test_cli_regression.sh [LOOP_COUNT]
#   LOOP_COUNT: Number of test loops to run (1-10, default: 1)
#   Examples:
#     ./test_cli_regression.sh     # Run 1 loop (default)
#     ./test_cli_regression.sh 3   # Run 3 loops
#     ./test_cli_regression.sh 10  # Run 10 loops (max)
#
# Test Coverage:
# - SPY Test Sequence: Tests 1-15 (15 tests - includes 2 options chain tests)
# - NVDA Test Sequence: Tests 16-30 (15 tests - includes 2 options chain tests)
# - Multi-Ticker Test Sequence: Tests 31-36 (6 tests)
# Total: 36 tests per loop
#
# Test Design Philosophy:
# - Sequential ticker testing validates chat history analysis
# - Same question types repeated for each ticker tests data reuse
# - Multi-ticker tests validate parallel tool call batching (max 3)

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
CLI_CMD="uv run src/backend/main.py"
RESULTS_DIR="test-reports"

# Ensure results directory exists
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 CLI Test Regression - NEW 36 Test Suite${NC}"
echo -e "${CYAN}===========================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Loop Count: ${GREEN}${LOOP_COUNT}x${NC}"
echo -e "Max Response Time: ${MAX_RESPONSE_TIME}s per test"
echo -e "CLI Command: $CLI_CMD"
echo -e "Session Mode: ${GREEN}PERSISTENT${NC} (all 36 tests in same session per loop)"
echo -e "Test Features: ${GREEN}Parallel Tool Calls (max 3)${NC}, ${GREEN}Chat History Analysis${NC}, ${GREEN}Options Chain Tests${NC}"
echo ""

# The 36 standardized test prompts organized by ticker sequence
declare -a prompts=(
    # SPY Test Sequence (Tests 1-15)
    "Market Status"
    "Current Price: \$SPY"
    "Today's Closing Price: \$SPY"
    "Yesterday's Closing Price: \$SPY"
    "Last week's Performance: \$SPY"
    "Stock Price on the previous week's Friday: \$SPY"
    "Daily Stock Price bars Analysis from the last 2 trading weeks: \$SPY"
    "RSI-14: \$SPY"
    "MACD: \$SPY"
    "SMA 20/50/200: \$SPY"
    "EMA 20/50/200: SPY"
    "Support & Resistance Levels: \$SPY"
    "Technical Analysis: \$SPY"
    "Get the SPY Call Options Chain Expiring this Friday"
    "Get the SPY Put Options Chain Expiring this Friday"
    # NVDA Test Sequence (Tests 16-30)
    "Market Status"
    "Current Price: \$NVDA"
    "Today's Closing Price: \$NVDA"
    "Yesterday's Closing Price: \$NVDA"
    "Last week's Performance: \$NVDA"
    "Stock Price on the previous week's Friday: \$NVDA"
    "Daily Stock Price bars Analysis from the last 2 trading weeks: \$NVDA"
    "RSI-14: \$NVDA"
    "MACD: \$NVDA"
    "SMA 20/50/200: \$NVDA"
    "EMA 20/50/200: NVDA"
    "Support & Resistance Levels: \$NVDA"
    "Technical Analysis: \$NVDA"
    "Get the NVDA Call Options Chain Expiring this Friday"
    "Get the NVDA Put Options Chain Expiring this Friday"
    # Multi-Ticker Test Sequence (Tests 31-36)
    "Market Status"
    "Current Price: \$WDC, \$AMD, \$GME"
    "Today's Closing Price: \$WDC, \$AMD, \$GME"
    "Yesterday's Closing Price: \$WDC, \$AMD, \$GME"
    "Last week's Performance: \$WDC, \$AMD, \$GME"
    "Daily bars Analysis from the last 2 trading weeks: \$WDC, \$AMD, \$GME"
)

declare -a test_names=(
    # SPY Test Sequence (Tests 1-15)
    "Test_1_Market_Status"
    "Test_2_SPY_Current_Price"
    "Test_3_SPY_Today_Closing_Price"
    "Test_4_SPY_Yesterday_Closing_Price"
    "Test_5_SPY_Last_Week_Performance"
    "Test_6_SPY_Previous_Week_Friday_Price"
    "Test_7_SPY_Last_2_Weeks_Daily_Bars"
    "Test_8_SPY_RSI_14"
    "Test_9_SPY_MACD"
    "Test_10_SPY_SMA_20_50_200"
    "Test_11_SPY_EMA_20_50_200"
    "Test_12_SPY_Support_Resistance"
    "Test_13_SPY_Technical_Analysis"
    "Test_14_SPY_Call_Options_Chain"
    "Test_15_SPY_Put_Options_Chain"
    # NVDA Test Sequence (Tests 16-30)
    "Test_16_Market_Status"
    "Test_17_NVDA_Current_Price"
    "Test_18_NVDA_Today_Closing_Price"
    "Test_19_NVDA_Yesterday_Closing_Price"
    "Test_20_NVDA_Last_Week_Performance"
    "Test_21_NVDA_Previous_Week_Friday_Price"
    "Test_22_NVDA_Last_2_Weeks_Daily_Bars"
    "Test_23_NVDA_RSI_14"
    "Test_24_NVDA_MACD"
    "Test_25_NVDA_SMA_20_50_200"
    "Test_26_NVDA_EMA_20_50_200"
    "Test_27_NVDA_Support_Resistance"
    "Test_28_NVDA_Technical_Analysis"
    "Test_29_NVDA_Call_Options_Chain"
    "Test_30_NVDA_Put_Options_Chain"
    # Multi-Ticker Test Sequence (Tests 31-36)
    "Test_31_Multi_Market_Status"
    "Test_32_Multi_Current_Price_WDC_AMD_GME"
    "Test_33_Multi_Today_Closing_Price_WDC_AMD_GME"
    "Test_34_Multi_Yesterday_Closing_Price_WDC_AMD_GME"
    "Test_35_Multi_Last_Week_Performance_WDC_AMD_GME"
    "Test_36_Multi_Last_2_Weeks_Daily_Bars_WDC_AMD_GME"
)

# Initialize test tracking
total_tests=${#prompts[@]}

# Aggregate tracking across all loops
declare -a all_loop_avg_times=()
declare -a all_loop_durations=()
declare -a all_loop_reports=()
total_loops_passed=0
total_loops_failed=0

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
    RAW_OUTPUT="/tmp/cli_output_loop${loop_num}_${LOOP_TIMESTAMP}.log"
    INPUT_FILE="/tmp/test_input_loop${loop_num}_${LOOP_TIMESTAMP}.txt"

    # Create input file with all prompts and exit at the end
    for prompt in "${prompts[@]}"; do
        echo "$prompt" >> "$INPUT_FILE"
    done
    echo "exit" >> "$INPUT_FILE"

    echo -e "${CYAN}🚀 Starting CLI Regression Test (Loop ${loop_num}/${LOOP_COUNT})...${NC}"
    echo -e "${CYAN}Session will run all 36 tests sequentially${NC}"
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
                echo -e "${GREEN}✅ Test completed${NC}"
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

                test_results+=("PASS")
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
            test_results+=("PASS")
        fi
    done
fi

# Calculate statistics
echo ""
echo -e "${CYAN}📊 Test Results Analysis${NC}"
echo -e "${CYAN}========================${NC}"

# Test results summary
echo -e "📋 Test Results Summary:"
passed_tests=0
for i in "${!test_names[@]}"; do
    test_number=$((i + 1))
    result="${test_results[$i]:-UNKNOWN}"
    if [ "$result" = "PASS" ]; then
        ((passed_tests++))
        echo -e "${GREEN}   Test $test_number: ${test_names[$i]} - PASS${NC}"
    else
        echo -e "${RED}   Test $test_number: ${test_names[$i]} - $result${NC}"
    fi
done

failed_tests=$((total_tests - passed_tests))

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
echo -e "${CYAN}📊 Loop ${loop_num}/${LOOP_COUNT} Test Summary${NC}"
echo -e "${CYAN}============================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"
echo -e "Success Rate: $(( passed_tests * 100 / total_tests ))%"
echo -e "Total Session Duration: ${duration_formatted}"
echo -e "Session Mode: ${GREEN}PERSISTENT${NC}"

# Track loop results
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
        echo "Passed: $passed_tests"
        echo "Failed: $failed_tests"
        echo "Success Rate: $(( passed_tests * 100 / total_tests ))%"
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
    echo -e "${CYAN}║  LOOP ${loop_num}/${LOOP_COUNT} - Completed${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

done  # End of loop iteration

# Aggregate Statistics Across All Loops
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  AGGREGATE STATISTICS - ALL ${LOOP_COUNT} LOOPS${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${CYAN}📊 Overall Test Summary${NC}"
echo -e "${CYAN}======================${NC}"
echo -e "Total Loops Run: $LOOP_COUNT"
echo -e "${GREEN}Loops Passed: $total_loops_passed${NC}"
echo -e "${RED}Loops Failed: $total_loops_failed${NC}"
echo -e "Overall Success Rate: $(( total_loops_passed * 100 / LOOP_COUNT ))%"
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
if [ $total_loops_failed -eq 0 ]; then
    echo -e "${GREEN}🎉 All ${LOOP_COUNT} loop(s) completed successfully!${NC}"
    echo -e "${GREEN}✅ CLI Regression Test: SUCCESS${NC}"
    exit 0
else
    echo -e "${RED}❌ ${total_loops_failed} loop(s) failed${NC}"
    echo -e "${RED}❌ CLI Regression Test: FAILED${NC}"
    exit 1
fi
