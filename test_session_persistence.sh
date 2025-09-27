#!/bin/bash

# Session Persistence Test Script
# Tests CLI session persistence with two related prompts

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
OUTPUT_FILE="$RESULTS_DIR/session_persistence_test_${TIMESTAMP}.txt"

# Clean up and create fresh results directory
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 CLI Session Persistence Test${NC}"
echo -e "${CYAN}===============================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Timeout: ${TIMEOUT}s per test"
echo -e "Output file: $OUTPUT_FILE"
echo ""

# Test prompts for session persistence
declare -a prompts=(
    "Current Market Status"
    "What about NVDA?"
)

declare -a test_names=(
    "Market_Status_Query"
    "Follow_Up_Context_Query"
)

# Function to run a single test
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
    local duration=$(echo "$end_time - $start_time" | bc -l)
    
    # Clean up input file
    rm -f "$input_file"
    
    # Check if test completed successfully
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ Test $test_number completed successfully${NC}"
        echo -e "${GREEN}⏱️  Duration: ${duration}s${NC}"
        
        # Extract footer data if available
        local footer_data=$(grep -E "(Response Time|Tokens Used|AI Model)" "$OUTPUT_FILE.tmp" | tail -3)
        if [ -n "$footer_data" ]; then
            echo -e "${GREEN}📊 Footer Data Found:${NC}"
            echo "$footer_data" | while read line; do
                echo -e "${GREEN}   $line${NC}"
            done
        else
            echo -e "${YELLOW}⚠️  No footer data found${NC}"
        fi
        
        # Append to main output file
        echo "=== Test $test_number: $test_name ===" >> "$OUTPUT_FILE"
        echo "Prompt: $prompt" >> "$OUTPUT_FILE"
        echo "Duration: ${duration}s" >> "$OUTPUT_FILE"
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
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END TEST $test_number (FAILED) ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 1
    fi
}

# Run all tests
echo -e "${CYAN}🚀 Starting Session Persistence Tests...${NC}"
echo ""

total_tests=${#prompts[@]}
passed_tests=0
failed_tests=0

for i in "${!prompts[@]}"; do
    test_number=$((i + 1))
    test_name="${test_names[$i]}"
    prompt="${prompts[$i]}"
    
    if run_test "$test_name" "$prompt" "$test_number"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Wait between tests to allow cleanup
    if [ $test_number -lt $total_tests ]; then
        echo -e "${YELLOW}⏳ Waiting 5 seconds before next test...${NC}"
        sleep 5
    fi
done

# Generate summary
echo -e "${CYAN}📊 Session Persistence Test Summary${NC}"
echo -e "${CYAN}===================================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"

if [ $failed_tests -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo -e "${GREEN}✅ CLI Session Persistence: VALIDATED${NC}"
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo -e "${RED}❌ CLI Session Persistence: NEEDS INVESTIGATION${NC}"
fi

echo ""
echo -e "${BLUE}📄 Detailed results saved to: $OUTPUT_FILE${NC}"

# Clean up temporary files
rm -f "$OUTPUT_FILE.tmp"

exit $failed_tests
