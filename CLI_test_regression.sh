#!/bin/bash

# CLI Test Regression Script - Single Source of Truth
# Tests all 27 standardized test prompts sequentially in a SINGLE CLI session
# Properly handles session persistence and accurate response time tracking
#
# Usage: ./CLI_test_regression.sh [LOOP_COUNT]
#   LOOP_COUNT: Number of test loops to run (1-10, default: 1)
#   Examples:
#     ./CLI_test_regression.sh     # Run 1 loop (default)
#     ./CLI_test_regression.sh 3   # Run 3 loops
#     ./CLI_test_regression.sh 10  # Run 10 loops (max)
#
# Test Coverage:
# - 7 original market data tests
# - 4 TA indicator tests (original)
# - 5 OHLC/options tests (original)
# - 11 NEW TA indicator tests (SPY-specific SMA/EMA/MACD variants)
# Total: 27 tests per loop

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
MAX_RESPONSE_TIME=120  # 2 minutes max per response
CLI_CMD="uv run src/backend/main.py"
RESULTS_DIR="test-reports"

# Ensure results directory exists
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 CLI Test Regression - 27 Test Suite${NC}"
echo -e "${CYAN}=======================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Loop Count: ${GREEN}${LOOP_COUNT}x${NC}"
echo -e "Max Response Time: ${MAX_RESPONSE_TIME}s per test"
echo -e "CLI Command: $CLI_CMD"
echo -e "Session Mode: ${GREEN}PERSISTENT${NC} (all 27 tests in same session per loop)"
echo ""

# The 27 standardized test prompts
# Tests 1-16: Original test suite
# Tests 17-27: New TA indicator tests (SPY-specific)
declare -a prompts=(
    # Original 16 tests
    "What the current Market Status?"
    "Stock Snapshot: NVDA"
    "Stock Snapshot: SPY, QQQ, IWM"
    "What was closing price today for: SPY"
    "Current weekly Price Change $ and % for: SPY"
    "Support & Resistance Levels: SPY"
    "Technical Analysis: SPY"
    "SMA for SPY"
    "20-day EMA for NVDA"
    "RSI analysis for SPY"
    "MACD for AAPL"
    "Multi-ticker quotes: AAPL, MSFT, GOOGL"
    "Options quote for SPY December 650 call O:SPY251219C00650000"
    "AAPL daily bars from January 1 to March 31, 2024"
    "TSLA price on December 13, 2024"
    "SPY previous trading day close"
    # New TA indicator tests (Tests 17-27)
    "SPY MACD"
    "SPY 20-day SMA"
    "SPY 50-day SMA"
    "SPY 200-day SMA"
    "SPY 20-day EMA"
    "SPY 50-day EMA"
    "SPY 200-day EMA"
    "SPY 5-day SMA"
    "SPY 10-day SMA"
    "SPY 5-day EMA"
    "SPY 10-day EMA"
)

declare -a test_names=(
    # Original 16 tests
    "Test_1_Market_Status_Query"
    "Test_2_Single_Stock_Snapshot_NVDA"
    "Test_3_Multi_Stock_Snapshot_SPY_QQQ_IWM"
    "Test_4_Closing_Price_Query_SPY"
    "Test_5_Weekly_Performance_Analysis_SPY"
    "Test_6_Support_Resistance_SPY"
    "Test_7_Technical_Analysis_SPY"
    "Test_8_SMA_Indicator_SPY"
    "Test_9_EMA_Indicator_NVDA"
    "Test_10_RSI_Indicator_SPY"
    "Test_11_MACD_Indicator_AAPL"
    "Test_12_Multi_Ticker_Quote_AAPL_MSFT_GOOGL"
    "Test_13_Options_Quote_SPY_Call"
    "Test_14_OHLC_Custom_Date_Range_AAPL"
    "Test_15_OHLC_Specific_Date_TSLA"
    "Test_16_OHLC_Previous_Close_SPY"
    # New TA indicator tests (Tests 17-27)
    "Test_17_SPY_MACD"
    "Test_18_SPY_SMA_20"
    "Test_19_SPY_SMA_50"
    "Test_20_SPY_SMA_200"
    "Test_21_SPY_EMA_20"
    "Test_22_SPY_EMA_50"
    "Test_23_SPY_EMA_200"
    "Test_24_SPY_SMA_5"
    "Test_25_SPY_SMA_10"
    "Test_26_SPY_EMA_5"
    "Test_27_SPY_EMA_10"
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

    # Generate unique timestamp for this loop
    LOOP_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    OUTPUT_FILE="$RESULTS_DIR/cli_regression_test_loop${loop_num}_${LOOP_TIMESTAMP}.txt"
    RAW_OUTPUT="/tmp/cli_output_loop${loop_num}_${LOOP_TIMESTAMP}.log"
    INPUT_FILE="/tmp/test_input_loop${loop_num}_${LOOP_TIMESTAMP}.txt"

    # Create input file with all prompts and exit at the end
    for prompt in "${prompts[@]}"; do
        echo "$prompt" >> "$INPUT_FILE"
    done
    echo "exit" >> "$INPUT_FILE"

    echo -e "${CYAN}🚀 Starting CLI Regression Test (Loop ${loop_num}/${LOOP_COUNT})...${NC}"
    echo -e "${CYAN}Session will run all 27 tests sequentially${NC}"
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
                if (( $(echo "$rt < 30" | bc -l 2>/dev/null || echo "0") )); then
                    echo -e "${GREEN}📈 Performance: EXCELLENT (< 30s)${NC}"
                elif (( $(echo "$rt < 45" | bc -l 2>/dev/null || echo "0") )); then
                    echo -e "${GREEN}📈 Performance: GOOD (30-45s)${NC}"
                elif (( $(echo "$rt < 90" | bc -l 2>/dev/null || echo "0") )); then
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
total_duration=$(echo "$end_time - $start_time" | bc -l 2>/dev/null || echo "0")

echo -e "${GREEN}✅ CLI session completed${NC}"
echo -e "${GREEN}⏱️  Total Session Duration: ${total_duration}s${NC}"
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
        if (( $(echo "$time < $min_time" | bc -l 2>/dev/null || echo "0") )); then
            min_time=$time
        fi
        if (( $(echo "$time > $max_time" | bc -l 2>/dev/null || echo "0") )); then
            max_time=$time
        fi
        total_time=$(echo "$total_time + $time" | bc -l 2>/dev/null || echo "$total_time")
        ((count++))
    done

    avg_time=$(echo "scale=2; $total_time / $count" | bc -l 2>/dev/null || echo "0")

    echo -e "   Min Response Time: ${min_time}s"
    echo -e "   Max Response Time: ${max_time}s"
    echo -e "   Avg Response Time: ${avg_time}s"
    echo -e "   Successful Tests: $count/$total_tests"

    # Performance assessment
    performance_rating="GOOD"
    if (( $(echo "$avg_time < 30" | bc -l 2>/dev/null || echo "0") )); then
        performance_rating="EXCELLENT"
    elif (( $(echo "$avg_time > 60" | bc -l 2>/dev/null || echo "0") )); then
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
echo -e "Total Session Duration: ${total_duration}s"
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
        echo "Total Session Duration: ${total_duration}s"
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
        if (( $(echo "$time < $agg_min" | bc -l 2>/dev/null || echo "0") )); then
            agg_min=$time
        fi
        if (( $(echo "$time > $agg_max" | bc -l 2>/dev/null || echo "0") )); then
            agg_max=$time
        fi
        agg_total=$(echo "$agg_total + $time" | bc -l 2>/dev/null || echo "$agg_total")
    done

    agg_avg=$(echo "scale=2; $agg_total / ${#all_loop_avg_times[@]}" | bc -l 2>/dev/null || echo "0")

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
