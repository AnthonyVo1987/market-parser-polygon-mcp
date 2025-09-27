#!/bin/bash

# Memory Usage Test Script
# Tests memory usage with caching during multiple operations

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
OUTPUT_FILE="$RESULTS_DIR/memory_usage_test_${TIMESTAMP}.txt"

# Clean up and create fresh results directory
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 Memory Usage with Caching Test${NC}"
echo -e "${CYAN}=================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Timeout: ${TIMEOUT}s per test"
echo -e "Output file: $OUTPUT_FILE"
echo ""

# Function to get memory usage
get_memory_usage() {
    local process_name="$1"
    ps aux | grep "$process_name" | grep -v grep | awk '{print $4, $6}' | head -1
}

# Function to get system memory
get_system_memory() {
    free -h | grep "Mem:" | awk '{print $3, $7}'
}

# Test prompts for memory testing
declare -a prompts=(
    "Current Market Status"
    "Single Stock Snapshot NVDA"
    "Current Market Status"
    "Single Stock Snapshot NVDA"
)

declare -a test_names=(
    "First_Market_Status"
    "First_NVDA_Snapshot"
    "Second_Market_Status_Cache"
    "Second_NVDA_Snapshot_Cache"
)

# Function to run a single test and monitor memory
run_memory_test() {
    local test_name="$1"
    local prompt="$2"
    local test_number="$3"
    
    echo -e "${BLUE}📝 Test $test_number: $test_name${NC}"
    echo -e "${YELLOW}Prompt: '$prompt'${NC}"
    
    # Get initial memory usage
    local initial_memory=$(get_system_memory)
    local initial_process_memory=$(get_memory_usage "python.*main.py")
    
    echo -e "${CYAN}📊 Initial Memory: System=$initial_memory, Process=$initial_process_memory${NC}"
    
    # Create temporary input file
    local input_file="/tmp/memory_input_${test_number}.txt"
    echo "$prompt" > "$input_file"
    echo "exit" >> "$input_file"
    
    # Run CLI with timeout and capture output
    local start_time=$(date +%s.%N)
    
    timeout $TIMEOUT $CLI_CMD < "$input_file" > "$OUTPUT_FILE.tmp" 2>&1
    local exit_code=$?
    
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc -l 2>/dev/null || echo "0")
    
    # Get final memory usage
    local final_memory=$(get_system_memory)
    local final_process_memory=$(get_memory_usage "python.*main.py")
    
    echo -e "${CYAN}📊 Final Memory: System=$final_memory, Process=$final_process_memory${NC}"
    
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
        echo "Initial Memory: System=$initial_memory, Process=$initial_process_memory" >> "$OUTPUT_FILE"
        echo "Final Memory: System=$final_memory, Process=$final_process_memory" >> "$OUTPUT_FILE"
        echo "Cache Stats: $cache_stats" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END TEST $test_number ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 0
    else
        echo -e "${RED}❌ Test $test_number failed or timed out${NC}"
        echo -e "${RED}⏱️  Duration: ${duration}s${NC}"
        
        # Append failure to main output file
        echo "=== Test $test_number: $test_name (FAILED) ===" >> "$OUTPUT_FILE"
        echo "Prompt: $prompt" >> "$OUTPUT_FILE"
        echo "Duration: ${duration}s" >> "$OUTPUT_FILE"
        echo "Initial Memory: System=$initial_memory, Process=$initial_process_memory" >> "$OUTPUT_FILE"
        echo "Final Memory: System=$final_memory, Process=$final_process_memory" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END TEST $test_number (FAILED) ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 1
    fi
}

# Run all tests and monitor memory
echo -e "${CYAN}🚀 Starting Memory Usage Tests...${NC}"
echo ""

total_tests=${#prompts[@]}
passed_tests=0
failed_tests=0

for i in "${!prompts[@]}"; do
    test_number=$((i + 1))
    test_name="${test_names[$i]}"
    prompt="${prompts[$i]}"
    
    if run_memory_test "$test_name" "$prompt" "$test_number"; then
        ((passed_tests++))
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

# Generate memory usage summary
echo -e "${CYAN}📊 Memory Usage Analysis${NC}"
echo -e "${CYAN}========================${NC}"

# Get current system memory
current_memory=$(get_system_memory)
echo -e "Current System Memory: $current_memory"

# Check for memory leaks in process
process_memory=$(get_memory_usage "python.*main.py")
echo -e "Current Process Memory: $process_memory"

# Generate summary
echo ""
echo -e "${CYAN}📊 Memory Usage Test Summary${NC}"
echo -e "${CYAN}============================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"

if [ $failed_tests -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo -e "${GREEN}✅ Memory Usage with Caching: VALIDATED${NC}"
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo -e "${RED}❌ Memory Usage with Caching: NEEDS INVESTIGATION${NC}"
fi

echo ""
echo -e "${BLUE}📄 Detailed results saved to: $OUTPUT_FILE${NC}"

# Clean up temporary files
rm -f "$OUTPUT_FILE.tmp"

exit $failed_tests
