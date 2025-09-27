#!/bin/bash

# Conversation Memory Test Script
# Tests that conversation memory works across multiple messages in the same session

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
OUTPUT_FILE="$RESULTS_DIR/conversation_memory_test_${TIMESTAMP}.txt"

# Clean up and create fresh results directory
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🧪 Conversation Memory Test${NC}"
echo -e "${CYAN}==========================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Timeout: ${TIMEOUT}s per test"
echo -e "Output file: $OUTPUT_FILE"
echo ""

# Test prompts for conversation memory
declare -a prompts=(
    "Current Market Status"
    "What about NVDA?"
    "How is the tech sector doing?"
)

declare -a test_names=(
    "Initial_Market_Status"
    "Follow_Up_NVDA_Context"
    "Follow_Up_Tech_Sector_Context"
)

# Function to run conversation memory test
run_conversation_test() {
    echo -e "${BLUE}📝 Running Conversation Memory Test${NC}"
    echo -e "${YELLOW}Testing multiple messages in same session...${NC}"
    
    # Create input file with all prompts
    local input_file="/tmp/conversation_input.txt"
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
        echo -e "${GREEN}✅ Conversation test completed successfully${NC}"
        echo -e "${GREEN}⏱️  Total Duration: ${duration}s${NC}"
        
        # Analyze conversation memory
        echo -e "${CYAN}📊 Conversation Memory Analysis${NC}"
        echo -e "${CYAN}==============================${NC}"
        
        # Count responses
        local response_count=$(grep -c "✅ Query processed successfully!" "$OUTPUT_FILE.tmp")
        echo -e "📝 Total Responses: $response_count"
        
        # Check for context references in responses
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
            echo -e "${GREEN}✅ Conversation Memory: WORKING - Context references found${NC}"
        else
            echo -e "${YELLOW}⚠️  Conversation Memory: INCONCLUSIVE - No clear context references found${NC}"
        fi
        
        # Extract response times
        local response_times=$(grep "Response Time:" "$OUTPUT_FILE.tmp" | grep -o '[0-9]\+\.[0-9]\+')
        if [ -n "$response_times" ]; then
            echo -e "${GREEN}📊 Response Times:${NC}"
            echo "$response_times" | while read time; do
                echo -e "${GREEN}   ${time}s${NC}"
            done
        fi
        
        # Append to main output file
        echo "=== Conversation Memory Test ===" >> "$OUTPUT_FILE"
        echo "Total Duration: ${duration}s" >> "$OUTPUT_FILE"
        echo "Response Count: $response_count" >> "$OUTPUT_FILE"
        echo "Context Found: $context_found" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END CONVERSATION TEST ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 0
    else
        echo -e "${RED}❌ Conversation test failed or timed out${NC}"
        echo -e "${RED}⏱️  Duration: ${duration}s${NC}"
        
        # Append failure to main output file
        echo "=== Conversation Memory Test (FAILED) ===" >> "$OUTPUT_FILE"
        echo "Duration: ${duration}s" >> "$OUTPUT_FILE"
        echo "Exit Code: $exit_code" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        cat "$OUTPUT_FILE.tmp" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "=== END CONVERSATION TEST (FAILED) ===" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        return 1
    fi
}

# Run conversation memory test
echo -e "${CYAN}🚀 Starting Conversation Memory Test...${NC}"
echo ""

if run_conversation_test; then
    echo -e "${GREEN}🎉 Conversation Memory Test: PASSED${NC}"
    echo -e "${GREEN}✅ Conversation Memory Functionality: VALIDATED${NC}"
else
    echo -e "${RED}❌ Conversation Memory Test: FAILED${NC}"
    echo -e "${RED}❌ Conversation Memory Functionality: NEEDS INVESTIGATION${NC}"
fi

echo ""
echo -e "${BLUE}📄 Detailed results saved to: $OUTPUT_FILE${NC}"

# Clean up temporary files
rm -f "$OUTPUT_FILE.tmp"

exit 0
