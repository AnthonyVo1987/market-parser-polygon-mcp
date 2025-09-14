# Playwright Testing Quick Start Guide

**Market Parser Playwright Testing Commands - Safe Usage Guide**

This guide provides essential information for using the `/test_cli_full` and `/test_mcp_full` Playwright testing commands safely and effectively.

---

## ⚡ Quick Command Reference

### Basic Usage
```
/test_cli_full    # Execute B001-B016 tests using CLI methodology
/test_mcp_full    # Execute B001-B016 tests using MCP browser automation
```

### Expected Execution Time
- **CLI Method**: ~30-60 minutes (typically faster)
- **MCP Method**: ~45-90 minutes (more thorough browser automation)
- **Total Tests**: 16 tests (B001-B016)

---

## 🚨 Critical Prerequisites

### 1. Server Startup (MANDATORY)

**Option A: One-Click Startup (Recommended)**
```bash
cd /home/1000211866/Github/market-parser-polygon-mcp
npm run start:app
```

**Option B: Manual Server Startup**
```bash
# Terminal 1: Backend Server (Static Configuration)
cd /home/1000211866/Github/market-parser-polygon-mcp
uv run uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend Server (Static Configuration)
cd /home/1000211866/Github/market-parser-polygon-mcp
npm run frontend:dev
```

**Verify Servers are Running:**
```bash
# Check backend health (Static IP)
curl http://127.0.0.1:8000/health
# Expected: {"status":"ok"}

# Check frontend (Static IP)
curl http://127.0.0.1:3000/
# Expected: HTML response with React app
```

### 2. Environment Security Check

**Required Environment Variables:**
```bash
# Check your .env file contains:
grep -q "POLYGON_API_KEY" .env && echo "✓ Polygon API key found"
grep -q "OPENAI_API_KEY" .env && echo "✓ OpenAI API key found"
```

**Security Warning**: Never share or commit API keys. Keep your `.env` file private.

---

## 🎯 Command Selection Guide

### When to Use CLI Method (`/test_cli_full`)
- **Faster execution** - Direct command-line testing
- **Resource efficient** - Lower system resource usage
- **Debugging** - Better for troubleshooting specific issues
- **Development** - Quick validation during development

### When to Use MCP Method (`/test_mcp_full`)
- **Browser automation** - Tests actual user interactions
- **UI validation** - Verifies visual components work correctly  
- **Cross-browser testing** - Tests compatibility across browsers
- **Production testing** - More realistic user simulation

---

## 📋 Simple Usage Examples

### Execute CLI Testing
```
You: /test_cli_full

Expected Response:
- Tech-lead orchestrator analyzes requirements
- Specialist assigned to execute tests
- Progress tracking through B001-B016 tests
- Test report generated automatically
- Results committed to repository
```

### Execute MCP Browser Testing
```
You: /test_mcp_full

Expected Response:  
- Browser automation specialist assigned
- Single browser session opens
- B001-B016 tests execute sequentially
- Performance data collected
- Comprehensive report generated
```

---

## ⏱️ Expected Outcomes and Timing

### Performance Classifications
- **Good 😊**: ≤30 seconds per test (optimal)
- **OK 😐**: 31-60 seconds per test (acceptable)
- **Slow 😴**: 61-119 seconds per test (functional but slow)
- **Timeout ❌**: ≥120 seconds per test (needs investigation)

### Typical Results
```
CLI Method Results:
✅ B001-B005: Basic Tests (5-45 seconds each)
✅ B006-B010: Button Tests (15-60 seconds each)  
✅ B011-B016: Advanced Tests (20-90 seconds each)

Expected Success Rate: 85-95% (14-15/16 tests passing)
```

### Test Report Location
Reports are automatically saved as:
- `playwright_CLI_test_[timestamp].md` (CLI method)
- `playwright_MCP_test_[timestamp].md` (MCP method)

---

## 🛡️ Basic Security Guidelines

### Safe Environment Practices
1. **Isolated Testing**: Run tests in development environment only
2. **API Key Protection**: Never share API keys or commit them to version control
3. **Network Security**: Ensure testing environment is not accessible from external networks
4. **Resource Monitoring**: Monitor system resources during test execution

### Input Safety
- Tests use predefined, validated inputs (NVDA, SPY, GME, etc.)
- No user input is directly passed to system commands
- All test parameters are sanitized and validated

### Error Handling
- Tests continue execution even if individual tests fail
- No destructive operations are performed
- All changes are tracked and can be reverted if needed

---

## 🔧 Common Troubleshooting

### Server Not Running Issues
```
Problem: "Connection refused" or "Cannot reach server"
Solution:
1. Check both servers are started (see Prerequisites section)
2. Verify ports 8000 and 3000/3001/3002/3003 are available
3. Check for error messages in server terminals
```

### Port Conflicts
```
Problem: "Port already in use" 
Solution:
1. Frontend auto-selects available port (check terminal output)
2. Backend can be started on alternate port: --port 8001
3. Update CORS settings if using non-standard ports
```

### Environment Issues
```
Problem: "Missing API keys" or "Environment not configured"
Solution:  
1. Copy .env.example to .env
2. Add your actual API keys to .env file
3. Restart servers after updating environment
```

### Performance Issues
```
Problem: Tests running very slowly or timing out
Solution:
1. Check system resources (CPU, memory)
2. Ensure no other resource-intensive processes running
3. Consider using CLI method for faster execution
4. Monitor network connectivity for API calls
```

---

## 📊 Understanding Test Results

### Success Indicators
- **Green checkmarks (✅)**: Test passed successfully
- **Performance timing**: Actual execution time recorded
- **Response validation**: System responded appropriately
- **Schema compliance**: Output meets expected format

### Warning Indicators  
- **Yellow warnings (⚠️)**: Test passed but took longer than optimal
- **Slow performance**: Test completed but exceeded normal timing
- **Partial success**: Some features work, others need attention

### Failure Indicators
- **Red X marks (❌)**: Test failed to complete
- **Timeout errors**: Test exceeded maximum wait time
- **Connection errors**: Unable to communicate with servers
- **Validation errors**: Response didn't meet expected criteria

---

## 🚀 Best Practices for Safe Testing

### Before Testing
1. **Verify Prerequisites**: Ensure both servers are running and healthy
2. **Check Environment**: Confirm API keys are properly configured
3. **Resource Planning**: Ensure sufficient system resources available
4. **Backup Preparation**: Consider backing up important work before testing

### During Testing
1. **Monitor Progress**: Watch for error messages or unusual behavior
2. **Resource Monitoring**: Keep an eye on system performance
3. **Don't Interrupt**: Allow tests to complete naturally for accurate results
4. **Stay Available**: Be ready to address any issues that arise

### After Testing
1. **Review Results**: Examine test reports for insights and issues
2. **Document Issues**: Note any consistent failures or performance problems
3. **Clean Up**: Check for any temporary files or processes that need cleanup
4. **Share Insights**: Communicate important findings to the development team

---

## 🎓 Advanced Usage Tips

### Optimizing Performance
- Use CLI method for quick validation during development
- Use MCP method for thorough UI and integration testing
- Run tests during low-activity periods for better performance
- Consider system resource optimization before extended test runs

### Interpreting Results
- Focus on trends rather than individual test failures
- Pay attention to performance classifications and timing patterns
- Look for consistent failures that might indicate systemic issues
- Use test results to guide optimization and improvement efforts

### Troubleshooting Complex Issues
- Check server logs for detailed error information
- Use browser developer tools during MCP testing for additional insights
- Compare CLI vs MCP results to isolate browser-specific issues
- Monitor network traffic for API communication problems

---

## 📞 Support and Additional Resources

### When to Seek Help
- Consistent test failures across multiple runs
- Severe performance degradation or timeout issues
- Security concerns or suspicious behavior
- Server startup problems that persist after troubleshooting

### Documentation Resources
- **Full User Manual**: `docs/testing/Playwright_Testing_User_Manual.md`
- **Security Guidelines**: `docs/testing/Playwright_Testing_Security_Guide.md`
- **Quality Assurance**: `docs/testing/Playwright_Testing_QA_Guide.md`
- **Test Specifications**: `gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md`

### Emergency Procedures
If testing causes system instability:
1. **Stop Tests**: Interrupt current test execution if possible
2. **Kill Servers**: Stop both backend and frontend servers
3. **Check Processes**: Use `ps aux | grep node` and `ps aux | grep uvicorn` to find any hanging processes
4. **Clean Restart**: Restart servers following the startup procedure
5. **Report Issues**: Document the problem for investigation

---

## ✅ Quick Checklist

Before running any Playwright testing command:

- [ ] **Servers Running**: Both backend (port 8000) and frontend (port 3000+) are operational
- [ ] **Environment Set**: API keys are configured in .env file
- [ ] **Resources Available**: Sufficient CPU and memory for testing
- [ ] **Network Stable**: Good internet connection for API calls
- [ ] **Clean State**: No conflicting processes or previous test artifacts
- [ ] **Backup Complete**: Important work is saved and backed up

**Ready to test?** Choose your method and execute:
- For speed and efficiency: `/test_cli_full`
- For comprehensive browser testing: `/test_mcp_full`

---

*This guide prioritizes safety and simplicity while providing comprehensive testing capabilities. For advanced usage and detailed technical information, refer to the complete user manual and security guidelines.*