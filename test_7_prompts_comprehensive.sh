#!/bin/bash

# Comprehensive 7 Test Prompts Script
# Tests all 7 standardized test prompts sequentially with 60s timeout per test
# Based on tests/playwright/test_prompts.md

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test configuration
TIMEOUT=90
CLI_CMD="uv run src/backend/main.py"
RESULTS_DIR="test-reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$RESULTS_DIR/comprehensive_7_prompts_test_${TIMESTAMP}.txt"

# Ensure results directory exists
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 Comprehensive 7 Test Prompts Validation${NC}"
echo -e "${CYAN}=========================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Timeout: ${TIMEOUT}s per test (Total max: $(( TIMEOUT * 7 ))s)"
echo -e "Output file: $OUTPUT_FILE"
echo -e "CLI Command: $CLI_CMD"
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

# Function to run a single test
run_single_test() {
    local test_name="$1"
    local prompt="$2"
    local test_number="$3"
    
    echo -e "${BLUE}📝 Test $test_number: $test_name${NC}"
    echo -e "${YELLOW}Prompt: '$prompt'${NC}"
    
    # Create temporary input file
    local input_file="/tmp/test_input_${test_number}.txt"
    echo "$prompt" > "$input_file"
    echo "exit" >> "$input_file"
    
    # Run CLI with timeout and capture output
    local start_time=$(date +%s.%N)
    
    timeout $TIMEOUT $CLI_CMD < "$input_file" > "$OUTPUT_FILE.tmp" 2>&1
    local exit_code=$?
    
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc -l 2>/dev/null || echo "0")
    
    # Clean up input file
    rm -f "$input_file"
    
    # Extract response time from output
    local response_time=$(grep "Response Time:" "$OUTPUT_FILE.tmp" | grep -o '[0-9]\+\.[0-9]\+' | tail -1)
    local cache_stats=$(grep "cache stats:" "$OUTPUT_FILE.tmp" | tail -1)
    local success_indicator=$(grep -c "✅ Query processed successfully!" "$OUTPUT_FILE.tmp")
    
    # Check if test completed successfully
    if [ $exit_code -eq 0 ] && [ $success_indicator -gt 0 ]; then
        echo -e "${GREEN}✅ Test $test_number completed successfully${NC}"
        echo -e "${GREEN}⏱️  Duration: ${duration}s${NC}"
        if [ -n "$response_time" ]; then
            echo -e "${GREEN}📊 Response Time: ${response_time}s${NC}"
            
            # Performance classification
            if (( $(echo "$response_time < 30" | bc -l 2>/dev/null || echo "0") )); then
                echo -e "${GREEN}📈 Performance: EXCELLENT (< 30s)${NC}"
            elif (( $(echo "$response_time < 45" | bc -l 2>/dev/null || echo "0") )); then
                echo -e "${GREEN}📈 Performance: GOOD (30-45s)${NC}"
            elif (( $(echo "$response_time < 90" | bc -l 2>/dev/null || echo "0") )); then
                echo -e "${YELLOW}📈 Performance: SLOW (45-90s)${NC}"
            else
                echo -e "${RED}📈 Performance: TIMEOUT (> 90s)${NC}"
            fi
        fi
        if [ -n "$cache_stats" ]; then
            echo -e "${GREEN}🚀 Cache Stats: $cache_stats${NC}"
        fi
        
        # Append to main output file
        echo "=== Test $test_number: $test_name ===" >> "$OUTPUT_FILE"
        echo "Prompt: $prompt" >> "$OUTPUT_FILE"
        echo "Duration: ${duration}s" >> "$OUTPUT_FILE"
        echo "Response Time: ${response_time}s" >> "$OUTPUT_FILE"
        echo "Cache Stats: $cache_stats" >> "$OUTPUT_FILE"
        echo "Success Indicator: $success_indicator" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END TEST $test_number ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        # Return response time for analysis
        echo "$response_time"
        return 0
    else
        echo -e "${RED}❌ Test $test_number failed or timed out${NC}"
        echo -e "${RED}⏱️  Duration: ${duration}s${NC}"
        echo -e "${RED}📊 Exit Code: $exit_code${NC}"
        echo -e "${RED}📊 Success Indicator: $success_indicator${NC}"
        
        # Append failure to main output file
        echo "=== Test $test_number: $test_name (FAILED) ===" >> "$OUTPUT_FILE"
        echo "Prompt: $prompt" >> "$OUTPUT_FILE"
        echo "Duration: ${duration}s" >> "$OUTPUT_FILE"
        echo "Response Time: ${response_time}s" >> "$OUTPUT_FILE"
        echo "Success Indicator: $success_indicator" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END TEST $test_number (FAILED) ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 1
    fi
}

# Run all 7 tests sequentially
echo -e "${CYAN}🚀 Starting Comprehensive 7 Test Prompts Validation...${NC}"
echo ""

total_tests=${#prompts[@]}
passed_tests=0
failed_tests=0
declare -a response_times=()
declare -a test_results=()

for i in "${!prompts[@]}"; do
    test_number=$((i + 1))
    test_name="${test_names[$i]}"
    prompt="${prompts[$i]}"
    
    response_time=$(run_single_test "$test_name" "$prompt" "$test_number")
    test_result=$?
    
    if [ $test_result -eq 0 ]; then
        ((passed_tests++))
        test_results+=("PASS")
        if [ -n "$response_time" ] && [ "$response_time" != "0" ]; then
            response_times+=("$response_time")
        fi
    else
        ((failed_tests++))
        test_results+=("FAIL")
    fi
    
    echo ""
    
    # Brief delay between tests
    if [ $test_number -lt $total_tests ]; then
        echo -e "${YELLOW}⏳ Brief pause before next test...${NC}"
        sleep 2
    fi
done

# Comprehensive analysis
echo -e "${CYAN}📊 Comprehensive Test Analysis${NC}"
echo -e "${CYAN}=============================${NC}"

# Test results summary
echo -e "📋 Test Results Summary:"
for i in "${!test_names[@]}"; do
    test_number=$((i + 1))
    result="${test_results[$i]}"
    if [ "$result" = "PASS" ]; then
        echo -e "${GREEN}   Test $test_number: ${test_names[$i]} - PASS${NC}"
    else
        echo -e "${RED}   Test $test_number: ${test_names[$i]} - FAIL${NC}"
    fi
done

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
        performance_rating="SLOW"
    fi
    
    echo -e "${GREEN}📈 Overall Performance Rating: $performance_rating${NC}"
else
    echo -e "${RED}❌ No response time data available for analysis${NC}"
fi

# Generate comprehensive summary
echo ""
echo -e "${CYAN}📊 Comprehensive Test Summary${NC}"
echo -e "${CYAN}============================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"
echo -e "Success Rate: $(( passed_tests * 100 / total_tests ))%"

if [ $failed_tests -eq 0 ]; then
    echo -e "${GREEN}🎉 All 7 tests passed!${NC}"
    echo -e "${GREEN}✅ Comprehensive Validation: SUCCESS${NC}"
    echo -e "${GREEN}✅ All standardized test prompts working correctly${NC}"
else
    echo -e "${RED}❌ $failed_tests test(s) failed${NC}"
    echo -e "${RED}❌ Comprehensive Validation: NEEDS INVESTIGATION${NC}"
fi

# Append summary to output file
echo "" >> "$OUTPUT_FILE"
echo "=== COMPREHENSIVE TEST SUMMARY ===" >> "$OUTPUT_FILE"
echo "Timestamp: $(date)" >> "$OUTPUT_FILE"
echo "Total Tests: $total_tests" >> "$OUTPUT_FILE"
echo "Passed: $passed_tests" >> "$OUTPUT_FILE"
echo "Failed: $failed_tests" >> "$OUTPUT_FILE"
echo "Success Rate: $(( passed_tests * 100 / total_tests ))%" >> "$OUTPUT_FILE"
echo "Max Timeout per Test: ${TIMEOUT}s" >> "$OUTPUT_FILE"
echo "Total Max Runtime: $(( TIMEOUT * total_tests ))s" >> "$OUTPUT_FILE"
if [ ${#response_times[@]} -gt 0 ]; then
    echo "Min Response Time: ${min_time}s" >> "$OUTPUT_FILE"
    echo "Max Response Time: ${max_time}s" >> "$OUTPUT_FILE"
    echo "Avg Response Time: ${avg_time}s" >> "$OUTPUT_FILE"
    echo "Performance Rating: $performance_rating" >> "$OUTPUT_FILE"
fi
echo "=== END COMPREHENSIVE TEST SUMMARY ===" >> "$OUTPUT_FILE"

echo ""
echo -e "${BLUE}📄 Detailed results saved to: $OUTPUT_FILE${NC}"

# Clean up temporary files
rm -f "$OUTPUT_FILE.tmp"

# Exit with appropriate code
if [ $failed_tests -eq 0 ]; then
    exit 0
else
    exit $failed_tests
fi
