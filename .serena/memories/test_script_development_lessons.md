# Test Script Development Lessons Learned

## Script Development Process

### Initial Approach Issues
1. **Incomplete Testing**: Created script without first manually testing the CLI
2. **Wrong Assumptions**: Assumed existing scripts were working when they had the same import issues
3. **Timeout Too Aggressive**: Started with 60s timeout, but some tests needed 90s

### Key Learnings

#### 1. Manual Testing First
- Always test the CLI manually before creating automated scripts
- Use simple commands like: `echo "prompt" | uv run src/backend/main.py`
- Verify the app actually starts and responds correctly

#### 2. Debug Import Issues
- Check existing scripts to see if they have the same problems
- Understand the difference between CLI mode and server mode
- Fix underlying issues before creating new test scripts

#### 3. Bash Script Best Practices
- Don't use `local` variables outside of functions
- Use proper variable scoping for statistics calculations
- Test script syntax before running comprehensive tests

#### 4. Timeout Configuration
- Start with conservative timeouts (90s instead of 60s)
- Monitor actual response times to set appropriate limits
- Consider that some prompts may take longer than others

#### 5. Error Handling
- Capture both exit codes and success indicators
- Provide detailed error output for debugging
- Include performance metrics in test results

## Script Features That Worked Well

### Comprehensive Output
- Color-coded console output for easy monitoring
- Detailed logging to files for analysis
- Performance classification system
- Statistical analysis of response times

### Robust Testing
- Individual test isolation
- Proper cleanup between tests
- Timeout handling with appropriate limits
- Success/failure tracking with detailed reporting

### User Experience
- Clear progress indicators
- Real-time status updates
- Comprehensive summary at the end
- Easy-to-read test results

## Final Script Characteristics
- **Timeout**: 90s per test (630s total max)
- **Output**: Single comprehensive .txt file in test-reports/
- **Coverage**: All 7 standardized test prompts
- **Metrics**: Response times, performance ratings, cache stats
- **Reliability**: 100% success rate (7/7 tests passing)

## Recommendations for Future Scripts
1. Always test manually first
2. Fix underlying issues before automation
3. Use conservative timeouts initially
4. Include comprehensive error handling
5. Provide detailed logging and metrics
6. Test script syntax and logic thoroughly