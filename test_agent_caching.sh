#!/bin/bash

# Agent Caching Test Script
# Tests that agents are cached and reused, showing decreasing creation times

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
OUTPUT_FILE="$RESULTS_DIR/agent_caching_test_${TIMESTAMP}.txt"

# Clean up and create fresh results directory
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 Agent Caching Functionality Test${NC}"
echo -e "${CYAN}===================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Timeout: ${TIMEOUT}s per test"
echo -e "Output file: $OUTPUT_FILE"
echo ""

# Test prompts for agent caching (similar requests to test caching)
declare -a prompts=(
    "Current Market Status"
    "Current Market Status"
    "Current Market Status"
)

declare -a test_names=(
    "First_Request_Agent_Creation"
    "Second_Request_Cache_Hit"
    "Third_Request_Cache_Hit"
)

# Function to run a single test and extract timing
run_test() {
    local test_name="$1"
    local prompt="$2"
    local test_number="$3"
    
    echo -e "${BLUE}📝 Test $test_number: $test_name${NC}"
    echo -e "${YELLOW}Prompt: '$prompt'${NC}"
    
    # Create temporary input file
    local input_file="/tmp/cli_input_${test_number}.txt"
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

# Run all tests and collect response times
echo -e "${CYAN}🚀 Starting Agent Caching Tests...${NC}"
echo ""

total_tests=${#prompts[@]}
passed_tests=0
failed_tests=0
declare -a response_times=()

for i in "${!prompts[@]}"; do
    test_number=$((i + 1))
    test_name="${test_names[$i]}"
    prompt="${prompts[$i]}"
    
    response_time=$(run_test "$test_name" "$prompt" "$test_number")
    if [ $? -eq 0 ]; then
        ((passed_tests++))
        if [ -n "$response_time" ] && [ "$response_time" != "0" ]; then
            response_times+=("$response_time")
        fi
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Wait between tests to allow cleanup
    if [ $test_number -lt $total_tests ]; then
        echo -e "${YELLOW}⏳ Waiting 3 seconds before next test...${NC}"
        sleep 3
    fi
done

# Analyze caching performance
echo -e "${CYAN}📊 Agent Caching Analysis${NC}"
echo -e "${CYAN}========================${NC}"

if [ ${#response_times[@]} -ge 2 ]; then
    first_time=${response_times[0]}
    second_time=${response_times[1]}
    third_time=${response_times[2]:-0}
    
    echo -e "First Request Time: ${first_time}s"
    echo -e "Second Request Time: ${second_time}s"
    if [ "$third_time" != "0" ]; then
        echo -e "Third Request Time: ${third_time}s"
    fi
    
    # Calculate improvement
    if [ "$second_time" != "0" ] && [ "$first_time" != "0" ]; then
        improvement=$(echo "$first_time - $second_time" | bc -l 2>/dev/null || echo "0")
        improvement_pct=$(echo "scale=1; $improvement * 100 / $first_time" | bc -l 2>/dev/null || echo "0")
        
        echo -e "${GREEN}📈 Performance Improvement: ${improvement}s (${improvement_pct}%)${NC}"
        
        if (( $(echo "$improvement > 0" | bc -l 2>/dev/null || echo "0") )); then
            echo -e "${GREEN}✅ Agent Caching: WORKING - Second request faster than first${NC}"
        else
            echo -e "${YELLOW}⚠️  Agent Caching: INCONCLUSIVE - No clear improvement detected${NC}"
        fi
    fi
else
    echo -e "${RED}❌ Insufficient data for caching analysis${NC}"
fi

# Generate summary
echo ""
echo -e "${CYAN}📊 Agent Caching Test Summary${NC}"
echo -e "${CYAN}============================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"

if [ $failed_tests -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo -e "${GREEN}✅ Agent Caching Functionality: VALIDATED${NC}"
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo -e "${RED}❌ Agent Caching Functionality: NEEDS INVESTIGATION${NC}"
fi

echo ""
echo -e "${BLUE}📄 Detailed results saved to: $OUTPUT_FILE${NC}"

# Clean up temporary files
rm -f "$OUTPUT_FILE.tmp"

exit $failed_tests
