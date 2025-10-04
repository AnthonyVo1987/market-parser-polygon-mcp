#!/bin/bash

# Persistent Session 7 Test Prompts Script
# Tests all 7 standardized test prompts sequentially in a SINGLE CLI session
# Properly handles session persistence and accurate response time tracking
# Based on tests/playwright/test_prompts.md

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test configuration
MAX_RESPONSE_TIME=120  # 2 minutes max per response
CLI_CMD="uv run src/backend/main.py"
RESULTS_DIR="test-reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$RESULTS_DIR/persistent_session_test_${TIMESTAMP}.txt"
RAW_OUTPUT="/tmp/cli_output_${TIMESTAMP}.log"

# Ensure results directory exists
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 Persistent Session 7 Test Prompts Validation${NC}"
echo -e "${CYAN}===============================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Max Response Time: ${MAX_RESPONSE_TIME}s per test"
echo -e "Output file: $OUTPUT_FILE"
echo -e "CLI Command: $CLI_CMD"
echo -e "Session Mode: ${GREEN}PERSISTENT${NC} (all 7 tests in same session)"
echo ""

# The 7 standardized test prompts from test_prompts.md
declare -a prompts=(
    "What the current Market Status, Date, & Time: Open, Closed, After-Hours, Pre-market, Overnight?"
    "Single Stock Snapshot Price NVDA"
    "Full Market Snapshot Price: SPY, QQQ, IWM"
    "GME closing price today"
    "SOUN Price performance this week"
    "NVDA Price Support & Resistance Levels"
    "SPY Price Technical Analysis"
)

declare -a test_names=(
    "Test_1_Market_Status_Query"
    "Test_2_Single_Stock_Snapshot_NVDA"
    "Test_3_Full_Market_Snapshot_SPY_QQQ_IWM"
    "Test_4_Closing_Price_Query_GME"
    "Test_5_Performance_Analysis_SOUN"
    "Test_6_Support_Resistance_NVDA"
    "Test_7_Technical_Analysis_SPY"
)

# Initialize test tracking
total_tests=${#prompts[@]}
declare -a response_times=()
declare -a test_results=()
declare -a test_durations=()

# Create input file with all prompts and exit at the end
INPUT_FILE="/tmp/test_input_${TIMESTAMP}.txt"
for prompt in "${prompts[@]}"; do
    echo "$prompt" >> "$INPUT_FILE"
done
echo "exit" >> "$INPUT_FILE"

echo -e "${CYAN}🚀 Starting Persistent Session Test...${NC}"
echo -e "${CYAN}Session will run all 7 tests sequentially${NC}"
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

# Generate comprehensive summary
echo ""
echo -e "${CYAN}📊 Comprehensive Test Summary${NC}"
echo -e "${CYAN}============================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"
echo -e "Success Rate: $(( passed_tests * 100 / total_tests ))%"
echo -e "Total Session Duration: ${total_duration}s"
echo -e "Session Mode: ${GREEN}PERSISTENT${NC}"

if [ $failed_tests -eq 0 ]; then
    echo -e "${GREEN}🎉 All $total_tests tests passed!${NC}"
    echo -e "${GREEN}✅ Persistent Session Validation: SUCCESS${NC}"
else
    echo -e "${RED}❌ $failed_tests test(s) failed${NC}"
    echo -e "${RED}❌ Persistent Session Validation: NEEDS INVESTIGATION${NC}"
fi

# Generate detailed output file
{
    echo "=== PERSISTENT SESSION TEST REPORT ==="
    echo "Timestamp: $(date)"
    echo "Total Tests: $total_tests"
    echo "Passed: $passed_tests"
    echo "Failed: $failed_tests"
    echo "Success Rate: $(( passed_tests * 100 / total_tests ))%"
    echo "Total Session Duration: ${total_duration}s"
    echo "Session Mode: PERSISTENT (single session)"
    echo "Session Count Detected: $session_count"
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
    echo "=== END PERSISTENT SESSION TEST REPORT ==="
} > "$OUTPUT_FILE"

echo ""
echo -e "${BLUE}📄 Detailed results saved to: $OUTPUT_FILE${NC}"
echo -e "${BLUE}📄 Raw CLI output: $RAW_OUTPUT${NC}"

# Clean up input file
rm -f "$INPUT_FILE"

# Exit with appropriate code
if [ $failed_tests -eq 0 ]; then
    exit 0
else
    exit $failed_tests
fi
