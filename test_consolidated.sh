#!/bin/bash

# Consolidated Multi-Test Script - All 7 Prompts, Single Output File
# Tests all 7 standardized prompts with 120s timeout each, outputs to single file

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
OUTPUT_FILE="$RESULTS_DIR/consolidated_test_results_${TIMESTAMP}.txt"

# Clean up and create fresh results directory
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

echo -e "${CYAN}🚀 Consolidated Multi-Test: All 7 Prompts${NC}"
echo -e "${CYAN}=========================================${NC}"
echo -e "Timestamp: $(date)"
echo -e "Timeout: ${TIMEOUT}s per test"
echo -e "Output file: $OUTPUT_FILE"
echo ""

# Test prompts
declare -a prompts=(
    "Current Market Status"
    "Single Stock Snapshot NVDA"
    "Full Market Snapshot: SPY, QQQ, IWM"
    "GME closing price today"
    "SOUN performance this week"
    "NVDA Support & Resistance Levels"
    "SPY Technical Analysis"
)

declare -a test_names=(
    "Market_Status_Query"
    "Single_Stock_Snapshot"
    "Full_Market_Snapshot"
    "Closing_Price_Query"
    "Performance_Analysis"
    "Support_Resistance"
    "Technical_Analysis"
)

# Initialize output file
echo "CONSOLIDATED TEST RESULTS - $(date)" > "$OUTPUT_FILE"
echo "=====================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Run tests
total_tests=${#prompts[@]}
passed=0
failed=0

for i in "${!prompts[@]}"; do
    test_num=$((i + 1))
    test_name="${test_names[$i]}"
    prompt="${prompts[$i]}"
    
    echo -e "${BLUE}📋 Test $test_num: $test_name${NC}"
    echo -e "${YELLOW}Prompt: $prompt${NC}"
    
    # Create temporary file for this test
    temp_file="/tmp/test_${test_num}_${TIMESTAMP}.txt"
    
    echo -e "${YELLOW}Running with ${TIMEOUT}s timeout...${NC}"
    
    # Write test header to consolidated file
    echo "TEST $test_num: $test_name" >> "$OUTPUT_FILE"
    echo "Prompt: $prompt" >> "$OUTPUT_FILE"
    echo "----------------------------------------" >> "$OUTPUT_FILE"
    
    if timeout $TIMEOUT bash -c "echo '$prompt' | $CLI_CMD" > "$temp_file" 2>&1; then
        echo -e "${GREEN}✅ Test $test_num PASSED${NC}"
        
        # Extract metrics
        response_time=$(grep "Response Time:" "$temp_file" | grep -o '[0-9]\+\.[0-9]\+' | head -1)
        model=$(grep "Model:" "$temp_file" | grep -o 'gpt-[0-9a-z-]\+' | head -1)
        tokens=$(grep "Tokens Used:" "$temp_file" | grep -o '[0-9,]\+' | head -1)
        
        if [ ! -z "$response_time" ]; then
            echo -e "   ⏱️  Response Time: ${response_time}s"
            if (( $(echo "$response_time < 60" | awk '{print ($1 < 60)}') )); then
                echo -e "   🎯 Under 60s target: ${GREEN}YES${NC}"
            else
                echo -e "   🎯 Under 60s target: ${RED}NO${NC}"
            fi
        fi
        
        if [ ! -z "$model" ]; then
            echo -e "   🤖 Model: $model"
        fi
        
        if [ ! -z "$tokens" ]; then
            echo -e "   🔢 Tokens: $tokens"
        fi
        
        # Write results to consolidated file
        echo "Status: PASSED" >> "$OUTPUT_FILE"
        if [ ! -z "$response_time" ]; then
            echo "Response Time: ${response_time}s" >> "$OUTPUT_FILE"
        fi
        if [ ! -z "$model" ]; then
            echo "Model: $model" >> "$OUTPUT_FILE"
        fi
        if [ ! -z "$tokens" ]; then
            echo "Tokens: $tokens" >> "$OUTPUT_FILE"
        fi
        echo "" >> "$OUTPUT_FILE"
        
        # Append full CLI output to consolidated file
        cat "$temp_file" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "========================================" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        ((passed++))
    else
        exit_code=$?
        echo -e "${RED}❌ Test $test_num FAILED${NC}"
        if [ $exit_code -eq 124 ]; then
            echo -e "   ⚠️  Reason: TIMEOUT (${TIMEOUT}s exceeded)"
            echo "Status: FAILED - TIMEOUT" >> "$OUTPUT_FILE"
        else
            echo -e "   ⚠️  Reason: ERROR (exit code: $exit_code)"
            echo "Status: FAILED - ERROR (exit code: $exit_code)" >> "$OUTPUT_FILE"
        fi
        echo "" >> "$OUTPUT_FILE"
        echo "========================================" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        ((failed++))
    fi
    
    # Clean up temp file
    rm -f "$temp_file"
    
    echo ""
    
    # Wait between tests
    if [ $test_num -lt $total_tests ]; then
        echo -e "${YELLOW}⏳ Waiting 5s before next test...${NC}"
        sleep 5
    fi
done

# Write summary to consolidated file
echo "SUMMARY" >> "$OUTPUT_FILE"
echo "=======" >> "$OUTPUT_FILE"
echo "Total Tests: $total_tests" >> "$OUTPUT_FILE"
echo "Passed: $passed" >> "$OUTPUT_FILE"
echo "Failed: $failed" >> "$OUTPUT_FILE"
echo "Success Rate: $(( passed * 100 / total_tests ))%" >> "$OUTPUT_FILE"
echo "Timestamp: $(date)" >> "$OUTPUT_FILE"

# Verification
file_count=$(ls -1 "$RESULTS_DIR" | wc -l)
echo -e "${CYAN}📊 Verification:${NC}"
echo -e "Expected files: 1"
echo -e "Actual files created: $file_count"

if [ $file_count -eq 1 ]; then
    echo -e "Status: ${GREEN}✅ CORRECT - Exactly 1 file created${NC}"
else
    echo -e "Status: ${RED}❌ ERROR - Expected 1 file, got $file_count${NC}"
fi

# Summary
echo -e "${CYAN}📊 Test Suite Complete!${NC}"
echo -e "${CYAN}======================${NC}"
echo -e "Total Tests: $total_tests"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
echo -e "Success Rate: $(( passed * 100 / total_tests ))%"
echo ""
echo -e "${CYAN}📄 Consolidated output file:${NC}"
echo -e "   $OUTPUT_FILE"
echo ""
echo -e "${CYAN}📄 Files in $RESULTS_DIR:${NC}"
ls -la "$RESULTS_DIR/"
