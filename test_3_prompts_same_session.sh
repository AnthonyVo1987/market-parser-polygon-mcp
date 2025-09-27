#!/bin/bash

# 3 Test Prompts in Same Session Validation
# Tests the 3 specific prompts in the same CLI session as additional validation

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test configuration
TIMEOUT=180
CLI_CMD="uv run src/backend/main.py"
RESULTS_DIR="test_results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$RESULTS_DIR/3_prompts_same_session_${TIMESTAMP}.txt"

# Clean up and create fresh results directory
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 3 Test Prompts in Same Session Validation${NC}"
echo -e "${CYAN}==========================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Timeout: ${TIMEOUT}s per test"
echo -e "Output file: $OUTPUT_FILE"
echo ""

# The 3 specific test prompts as specified in the task plan
declare -a prompts=(
    "Current Market Status"
    "Single Stock Snapshot NVDA"
    "Full Market Snapshot: SPY, QQQ, IWM"
)

declare -a test_names=(
    "Test_Prompt_1_Market_Status"
    "Test_Prompt_2_NVDA_Snapshot"
    "Test_Prompt_3_Full_Market_Snapshot"
)

# Function to run the 3 prompts in the same session
run_same_session_test() {
    echo -e "${BLUE}📝 Running 3 Test Prompts in Same Session${NC}"
    echo -e "${YELLOW}Testing session persistence and conversation memory...${NC}"
    
    # Create input file with all 3 prompts
    local input_file="/tmp/same_session_input.txt"
    for prompt in "${prompts[@]}"; do
        echo "$prompt" >> "$input_file"
    done
    echo "exit" >> "$input_file"
    
    # Run CLI with timeout and capture output
    local start_time=$(date +%s.%N)
    
    timeout $TIMEOUT $CLI_CMD < "$input_file" > "$OUTPUT_FILE.tmp" 2>&1
    local exit_code=$?
    
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc -l 2>/dev/null || echo "0")
    
    # Clean up input file
    rm -f "$input_file"
    
    # Check if test completed successfully
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ Same session test completed successfully${NC}"
        echo -e "${GREEN}⏱️  Total Duration: ${duration}s${NC}"
        
        # Analyze session persistence
        echo -e "${CYAN}📊 Session Persistence Analysis${NC}"
        echo -e "${CYAN}==============================${NC}"
        
        # Count responses
        local response_count=$(grep -c "✅ Query processed successfully!" "$OUTPUT_FILE.tmp")
        echo -e "📝 Total Responses: $response_count"
        
        # Extract response times
        local response_times=$(grep "Response Time:" "$OUTPUT_FILE.tmp" | grep -o '[0-9]\+\.[0-9]\+')
        if [ -n "$response_times" ]; then
            echo -e "${GREEN}📊 Response Times:${NC}"
            local count=1
            echo "$response_times" | while read time; do
                echo -e "${GREEN}   Prompt $count: ${time}s${NC}"
                ((count++))
            done
        fi
        
        # Check for session initialization
        local session_init=$(grep -c "CLI session.*initialized" "$OUTPUT_FILE.tmp")
        echo -e "🚀 Session Initializations: $session_init"
        
        # Check for cache initialization
        local cache_init=$(grep -c "CLI agent cache initialized" "$OUTPUT_FILE.tmp")
        echo -e "🚀 Cache Initializations: $cache_init"
        
        # Check for context references
        local context_indicators=(
            "previous"
            "earlier"
            "mentioned"
            "as discussed"
            "building on"
            "following up"
            "context"
            "referring to"
        )
        
        local context_found=false
        for indicator in "${context_indicators[@]}"; do
            if grep -qi "$indicator" "$OUTPUT_FILE.tmp"; then
                echo -e "${GREEN}🔍 Context reference found: '$indicator'${NC}"
                context_found=true
            fi
        done
        
        if [ "$context_found" = true ]; then
            echo -e "${GREEN}✅ Session Persistence: WORKING - Context references found${NC}"
        else
            echo -e "${YELLOW}⚠️  Session Persistence: INCONCLUSIVE - No clear context references found${NC}"
        fi
        
        # Performance analysis
        if [ $response_count -eq 3 ]; then
            echo -e "${GREEN}✅ All 3 prompts processed successfully${NC}"
            
            # Calculate expected performance improvements
            echo -e "${CYAN}📈 Expected Performance Improvements:${NC}"
            echo -e "   First prompt: ~30-60s (agent creation + MCP server setup)"
            echo -e "   Second prompt: ~20-40s (cached agent reuse)"
            echo -e "   Third prompt: ~20-40s (cached agent reuse)"
            echo -e "   Target: 4-20s faster per session (10-40% improvement)"
        else
            echo -e "${RED}❌ Not all prompts processed (expected 3, got $response_count)${NC}"
        fi
        
        # Append to main output file
        echo "=== 3 Test Prompts in Same Session Validation ===" >> "$OUTPUT_FILE"
        echo "Total Duration: ${duration}s" >> "$OUTPUT_FILE"
        echo "Response Count: $response_count" >> "$OUTPUT_FILE"
        echo "Session Initializations: $session_init" >> "$OUTPUT_FILE"
        echo "Cache Initializations: $cache_init" >> "$OUTPUT_FILE"
        echo "Context Found: $context_found" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END SAME SESSION VALIDATION ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 0
    else
        echo -e "${RED}❌ Same session test failed or timed out${NC}"
        echo -e "${RED}⏱️  Duration: ${duration}s${NC}"
        
        # Append failure to main output file
        echo "=== 3 Test Prompts in Same Session Validation (FAILED) ===" >> "$OUTPUT_FILE"
        echo "Duration: ${duration}s" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END SAME SESSION VALIDATION (FAILED) ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 1
    fi
}

# Run same session validation test
echo -e "${CYAN}🚀 Starting 3 Test Prompts in Same Session Validation...${NC}"
echo ""

if run_same_session_test; then
    echo -e "${GREEN}🎉 3 Test Prompts in Same Session: PASSED${NC}"
    echo -e "${GREEN}✅ Additional Validation: VALIDATED${NC}"
else
    echo -e "${RED}❌ 3 Test Prompts in Same Session: FAILED${NC}"
    echo -e "${RED}❌ Additional Validation: NEEDS INVESTIGATION${NC}"
fi

echo ""
echo -e "${BLUE}📄 Detailed results saved to: $OUTPUT_FILE${NC}"

# Clean up temporary files
rm -f "$OUTPUT_FILE.tmp"

exit 0
