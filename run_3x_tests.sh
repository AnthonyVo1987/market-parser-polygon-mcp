#!/bin/bash

# 5x Test Runs Script
# Runs test_consolidated.sh 5 times and captures each result

echo "🚀 Starting 3x Test Runs Analysis"
echo "================================="

# Create results directory
mkdir -p test_results/consolidated_3x_runs

# Run 5 tests
for i in {1..5}; do
    echo "📋 Starting Run $i of 3..."
    echo "Timestamp: $(date)"
    
    # Run the test with timeout
    timeout 120 ./test_consolidated.sh
    
    # Copy the result immediately
    if [ -f test_results/consolidated_test_results_*.txt ]; then
        cp test_results/consolidated_test_results_*.txt test_results/consolidated_3x_runs/run_${i}_results.txt
        echo "✅ Run $i completed and saved"
    else
        echo "❌ Run $i failed - no output file found"
    fi
    
    # Wait between runs
    if [ $i -lt 5 ]; then
        echo "⏳ Waiting 10s before next run..."
        sleep 10
    fi
done

echo "🎉 All 3 runs completed!"
echo "Results saved in: test_results/consolidated_3x_runs/"
ls -la test_results/consolidated_3x_runs/
