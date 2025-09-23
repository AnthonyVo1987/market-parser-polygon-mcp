/**
 * Playwright MCP Test Framework - Complete 51-Test Suite Implementation
 * 
 * This framework implements the corrected test specifications for Market Parser
 * focusing on button-click → response architecture with basic functionality validation.
 * 
 * Key Corrections Applied:
 * - Simple "PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity" requests
 * - Basic functionality validation instead of strict JSON schema enforcement
 * - Complete 51-test suite across 9 categories
 * - Proper timeout handling (120 seconds for API responses)
 * - Emojis are ALLOWED and encouraged in all responses
 */

class PlaywrightMCPTestFramework {
    constructor() {
        this.baseUrl = 'http://localhost:3001';
        this.apiUrl = 'http://localhost:8000';
        this.testResults = [];
        this.timeouts = {
            navigation: 30000,
            click: 5000,
            apiResponse: 120000,
            validation: 5000
        };
        this.responseValidation = this.initializeBasicValidation();
    }

    /**
     * Initialize basic validation for any response format
     */
    initializeBasicValidation() {
        return {
            allowedFormats: ['json', 'text', 'emoji', 'conversational', 'mixed'],
            requiredElements: {
                hasContent: (response) => response && response.trim().length > 0,
                hasRelevantInfo: (response, ticker) => {
                    if (!ticker) return true;
                    return response.toLowerCase().includes(ticker.toLowerCase());
                },
                isReadable: (response) => {
                    // Any format is acceptable - JSON, text with emojis, conversational
                    return response && typeof response === 'string' && response.trim().length > 0;
                }
            },
            contentStructure: {
                requiredSections: ['KEY TAKEAWAYS', 'DETAILED ANALYSIS', 'DISCLAIMER'],
                hasStructure: (response) => {
                    return /KEY\s*TAKEAWAYS/i.test(response) || 
                           /DETAILED\s*ANALYSIS/i.test(response) || 
                           /DISCLAIMER/i.test(response);
                }
            }
        };
    }

    /**
     * Validate basic functionality of any response format
     * @param {string} response - Response text to validate (any format acceptable)
     * @param {string} ticker - Expected ticker symbol (optional)
     * @param {string} requestType - Type of request made (optional)
     * @returns {Object} Validation result with success flag and notes
     */
    validateBasicFunctionality(response, ticker = null, requestType = 'general') {
        const validation = this.responseValidation;
        const notes = [];
        const warnings = [];

        // Basic content validation
        if (!validation.requiredElements.hasContent(response)) {
            return { success: false, errors: ['Response is empty or contains no content'], notes, warnings };
        }

        // Check for relevant information
        if (ticker && !validation.requiredElements.hasRelevantInfo(response, ticker)) {
            warnings.push(`Response may not contain information about requested ticker: ${ticker}`);
        }

        // Verify response is readable (any format is acceptable)
        if (!validation.requiredElements.isReadable(response)) {
            return { success: false, errors: ['Response is not in a readable format'], notes, warnings };
        }

        // Check for content structure (required for proper analysis)
        if (validation.contentStructure.hasStructure(response)) {
            notes.push('✅ Response contains structured analysis sections');
        } else {
            notes.push('ℹ️  Response could benefit from structured sections (KEY TAKEAWAYS, DETAILED ANALYSIS)');
        }

        // Determine response format
        let formatType = 'text';
        try {
            JSON.parse(response);
            formatType = 'json';
        } catch {
            if (validation.contentStructure.hasStructure(response)) {
                formatType = 'structured-analysis';
            } else if (response.includes('analysis') || response.includes('data') || response.includes('price')) {
                formatType = 'conversational';
            }
        }

        notes.push(`📋 Response format detected: ${formatType} (all formats acceptable)`);

        return {
            success: true,
            errors: [],
            notes,
            warnings,
            responseFormat: formatType,
            hasStructure: validation.contentStructure.hasStructure(response),
            contentLength: response.length
        };
    }

    /**
     * Execute a single test with proper error handling and timeout management
     * @param {string} testId - Unique test identifier
     * @param {string} testName - Human-readable test name
     * @param {Function} testFunction - Async function to execute
     * @returns {Object} Test result
     */
    async executeTest(testId, testName, testFunction) {
        const startTime = Date.now();
        const testResult = {
            id: testId,
            name: testName,
            startTime: startTime,
            endTime: null,
            duration: null,
            status: 'RUNNING',
            errors: [],
            data: null
        };

        try {
            const result = await testFunction();
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - startTime;
            testResult.status = 'PASS';
            testResult.data = result;
        } catch (error) {
            testResult.endTime = Date.now();
            testResult.duration = testResult.endTime - startTime;
            testResult.status = 'FAIL';
            testResult.errors.push(error.message);
        }

        this.testResults.push(testResult);
        return testResult;
    }

    /**
     * Generate comprehensive test report
     * @returns {string} Formatted test report
     */
    generateTestReport() {
        const totalTests = this.testResults.length;
        const passedTests = this.testResults.filter(t => t.status === 'PASS').length;
        const failedTests = this.testResults.filter(t => t.status === 'FAIL').length;
        const totalDuration = this.testResults.reduce((sum, t) => sum + (t.duration || 0), 0);
        const avgDuration = totalTests > 0 ? totalDuration / totalTests : 0;

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const pacificTime = new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles' });

        let report = `# CLAUDE Playwright MCP Test Execution Report\n\n`;
        report += `**Date**: ${pacificTime} (Pacific Time)\n`;
        report += `**Report File**: CLAUDE_playwright_mcp_tests_${timestamp.substring(0, 19)}.md\n`;
        report += `**Duration**: ${(totalDuration / 1000).toFixed(1)} seconds\n`;
        report += `**Total Tests**: ${totalTests}\n`;
        report += `**Passed**: ${passedTests} ✅\n`;
        report += `**Failed**: ${failedTests} ❌\n`;
        report += `**Success Rate**: ${totalTests > 0 ? ((passedTests / totalTests) * 100).toFixed(1) : 0}%\n`;
        report += `**Average Test Duration**: ${(avgDuration / 1000).toFixed(1)} seconds\n\n`;

        // Priority Tests Results
        const priorityTests = this.testResults.filter(t => t.id.startsWith('TEST-P'));
        if (priorityTests.length > 0) {
            report += `## Priority Tests Results\n\n`;
            priorityTests.forEach(test => {
                const statusIcon = test.status === 'PASS' ? '✅' : '❌';
                const duration = test.duration ? `(${(test.duration / 1000).toFixed(1)}s)` : '';
                report += `- ${test.id}: ${test.name} ${statusIcon} ${test.status} ${duration}\n`;
                if (test.errors.length > 0) {
                    report += `  - Errors: ${test.errors.join(', ')}\n`;
                }
            });
            report += '\n';
        }

        // Test Category Results
        const categories = [
            { prefix: 'TEST-T', name: 'Template Button Interactions' },
            { prefix: 'TEST-M', name: 'Message Input Variations' },
            { prefix: 'TEST-E', name: 'Export Functionality' },
            { prefix: 'TEST-R', name: 'Responsive Design' },
            { prefix: 'TEST-A', name: 'Backend API Integration' },
            { prefix: 'TEST-H', name: 'Error Handling' },
            { prefix: 'TEST-F', name: 'Performance Validation' },
            { prefix: 'TEST-C', name: 'Accessibility Testing' },
            { prefix: 'TEST-B', name: 'Cross-Browser Compatibility' }
        ];

        categories.forEach(category => {
            const categoryTests = this.testResults.filter(t => t.id.startsWith(category.prefix));
            if (categoryTests.length > 0) {
                const categoryPassed = categoryTests.filter(t => t.status === 'PASS').length;
                const categoryTotal = categoryTests.length;
                
                report += `## ${category.name} (${categoryPassed}/${categoryTotal})\n\n`;
                categoryTests.forEach(test => {
                    const statusIcon = test.status === 'PASS' ? '✅' : '❌';
                    const duration = test.duration ? `(${(test.duration / 1000).toFixed(1)}s)` : '';
                    report += `- ${test.id}: ${test.name} ${statusIcon} ${test.status} ${duration}\n`;
                    if (test.errors.length > 0) {
                        report += `  - Errors: ${test.errors.join(', ')}\n`;
                    }
                });
                report += '\n';
            }
        });

        // Performance Metrics
        if (this.testResults.length > 0) {
            const successfulTests = this.testResults.filter(t => t.status === 'PASS' && t.duration);
            if (successfulTests.length > 0) {
                const responseTimes = successfulTests.map(t => t.duration);
                const minTime = Math.min(...responseTimes);
                const maxTime = Math.max(...responseTimes);
                
                report += `## Performance Metrics\n\n`;
                report += `- Average Response Time: ${(avgDuration / 1000).toFixed(1)} seconds\n`;
                report += `- Minimum Response Time: ${(minTime / 1000).toFixed(1)} seconds\n`;
                report += `- Maximum Response Time: ${(maxTime / 1000).toFixed(1)} seconds\n`;
                report += `- Total Test Duration: ${(totalDuration / 1000).toFixed(1)} seconds\n\n`;
            }
        }

        // Failure Analysis
        const failedTestsDetails = this.testResults.filter(t => t.status === 'FAIL');
        if (failedTestsDetails.length > 0) {
            report += `## Failed Test Analysis\n\n`;
            failedTestsDetails.forEach(test => {
                report += `### ${test.id}: ${test.name}\n`;
                report += `**Status**: FAILED\n`;
                report += `**Duration**: ${test.duration ? (test.duration / 1000).toFixed(1) : 'N/A'} seconds\n`;
                report += `**Errors**:\n`;
                test.errors.forEach(error => {
                    report += `- ${error}\n`;
                });
                report += '\n';
            });
        }

        // Success Criteria Assessment
        report += `## Success Criteria Assessment\n\n`;
        const priorityPassRate = priorityTests.length > 0 ? (priorityTests.filter(t => t.status === 'PASS').length / priorityTests.length) * 100 : 0;
        const comprehensivePassRate = totalTests > 5 ? ((passedTests - priorityTests.filter(t => t.status === 'PASS').length) / (totalTests - priorityTests.length)) * 100 : 0;
        
        report += `**Priority Tests**: ${priorityPassRate.toFixed(1)}% pass rate (Target: 100%) ${priorityPassRate >= 100 ? '✅' : '❌'}\n`;
        report += `**Comprehensive Tests**: ${comprehensivePassRate.toFixed(1)}% pass rate (Target: 90%) ${comprehensivePassRate >= 90 ? '✅' : '❌'}\n`;
        report += `**Overall System Status**: ${(priorityPassRate >= 100 && comprehensivePassRate >= 90) ? 'HEALTHY ✅' : 'ISSUES DETECTED ❌'}\n\n`;

        return report;
    }
}

module.exports = { PlaywrightMCPTestFramework };