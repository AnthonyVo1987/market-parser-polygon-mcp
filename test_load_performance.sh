#!/bin/bash

# Load Performance Test Script
# Tests performance under load with multiple concurrent requests

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test configuration
TIMEOUT=120
CLI_CMD="uv run src/backend/main.py"
RESULTS_DIR="test_results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$RESULTS_DIR/load_performance_test_${TIMESTAMP}.txt"

# Clean up and create fresh results directory
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 Load Performance Test${NC}"
echo -e "${CYAN}=======================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Timeout: ${TIMEOUT}s per test"
echo -e "Output file: $OUTPUT_FILE"
echo ""

# Test prompts for load testing
declare -a prompts=(
    "Current Market Status"
    "Single Stock Snapshot NVDA"
    "GME closing price today"
    "SOUN performance this week"
    "Current Market Status"
)

declare -a test_names=(
    "Load_Test_1_Market_Status"
    "Load_Test_2_NVDA_Snapshot"
    "Load_Test_3_GME_Price"
    "Load_Test_4_SOUN_Performance"
    "Load_Test_5_Market_Status_Repeat"
)

# Function to run a single test
run_load_test() {
    local test_name="$1"
    local prompt="$2"
    local test_number="$3"
    
    echo -e "${BLUE}📝 Test $test_number: $test_name${NC}"
    echo -e "${YELLOW}Prompt: '$prompt'${NC}"
    
    # Create temporary input file
    local input_file="/tmp/load_input_${test_number}.txt"
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
    
    # Check if test completed successfully
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ Test $test_number completed successfully${NC}"
        echo -e "${GREEN}⏱️  Duration: ${duration}s${NC}"
        if [ -n "$response_time" ]; then
            echo -e "${GREEN}📊 Response Time: ${response_time}s${NC}"
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
        
        # Append failure to main output file
        echo "=== Test $test_number: $test_name (FAILED) ===" >> "$OUTPUT_FILE"
        echo "Prompt: $prompt" >> "$OUTPUT_FILE"
        echo "Duration: ${duration}s" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END TEST $test_number (FAILED) ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 1
    fi
}

# Run load tests with minimal delay to simulate load
echo -e "${CYAN}🚀 Starting Load Performance Tests...${NC}"
echo ""

total_tests=${#prompts[@]}
passed_tests=0
failed_tests=0
declare -a response_times=()

for i in "${!prompts[@]}"; do
    test_number=$((i + 1))
    test_name="${test_names[$i]}"
    prompt="${prompts[$i]}"
    
    response_time=$(run_load_test "$test_name" "$prompt" "$test_number")
    if [ $? -eq 0 ]; then
        ((passed_tests++))
        if [ -n "$response_time" ] && [ "$response_time" != "0" ]; then
            response_times+=("$response_time")
        fi
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Minimal delay between tests to simulate load
    if [ $test_number -lt $total_tests ]; then
        echo -e "${YELLOW}⏳ Load simulation: 1 second delay...${NC}"
        sleep 1
    fi
done

# Analyze load performance
echo -e "${CYAN}📊 Load Performance Analysis${NC}"
echo -e "${CYAN}============================${NC}"

if [ ${#response_times[@]} -gt 0 ]; then
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
    
    echo -e "📊 Response Time Statistics:"
    echo -e "   Min: ${min_time}s"
    echo -e "   Max: ${max_time}s"
    echo -e "   Avg: ${avg_time}s"
    echo -e "   Count: $count tests"
    
    # Performance assessment
    performance_rating="GOOD"
    if (( $(echo "$avg_time > 60" | bc -l 2>/dev/null || echo "0") )); then
        performance_rating="SLOW"
    elif (( $(echo "$avg_time < 30" | bc -l 2>/dev/null || echo "0") )); then
        performance_rating="EXCELLENT"
    fi
    
    echo -e "${GREEN}📈 Load Performance Rating: $performance_rating${NC}"
    
    # Check for performance degradation
    if [ ${#response_times[@]} -ge 2 ]; then
        first_time=${response_times[0]}
        last_time=${response_times[-1]}
        degradation=$(echo "$last_time - $first_time" | bc -l 2>/dev/null || echo "0")
        
        if (( $(echo "$degradation > 10" | bc -l 2>/dev/null || echo "0") )); then
            echo -e "${YELLOW}⚠️  Performance degradation detected: +${degradation}s${NC}"
        else
            echo -e "${GREEN}✅ No significant performance degradation${NC}"
        fi
    fi
else
    echo -e "${RED}❌ No response time data available for analysis${NC}"
fi

# Generate summary
echo ""
echo -e "${CYAN}📊 Load Performance Test Summary${NC}"
echo -e "${CYAN}================================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"

if [ $failed_tests -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo -e "${GREEN}✅ Load Performance: VALIDATED${NC}"
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo -e "${RED}❌ Load Performance: NEEDS INVESTIGATION${NC}"
fi

echo ""
echo -e "${BLUE}📄 Detailed results saved to: $OUTPUT_FILE${NC}"

# Clean up temporary files
rm -f "$OUTPUT_FILE.tmp"

exit $failed_tests
