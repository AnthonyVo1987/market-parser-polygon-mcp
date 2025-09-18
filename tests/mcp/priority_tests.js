/**
 * Priority Tests Implementation - TEST-P001 through TEST-P005
 * 
 * These are the 5 critical tests that must pass for system validation.
 * Focus on simple "PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity" requests
 * and basic functionality validation. Emojis are ALLOWED and encouraged in all responses.
 */

const { PlaywrightMCPTestFramework } = require('./test_framework');

class PriorityTestsSuite extends PlaywrightMCPTestFramework {
    constructor() {
        super();
    }

    /**
     * TEST-P001: Market Status Request
     * Purpose: Verify system responds to market status requests (any format acceptable)
     */
    async testP001_MarketStatusRequest() {
        return this.executeTest('TEST-P001', 'Market Status Request', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input the priority fast request
            const inputQuery = "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity";
            await this.inputMessage(inputQuery);
            
            // Send the message
            await this.sendMessage();
            
            // Wait for response (120 seconds timeout)
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Validate basic functionality (any format acceptable)
            const validation = this.validateBasicFunctionality(response, null, 'market_status');
            if (!validation.success) {
                throw new Error(`Basic functionality validation failed: ${validation.errors.join(', ')}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                response: response,
                validation: validation,
                hasStructuredContent: validation.hasStructuredContent,
                responseFormat: validation.responseFormat
            };
        });
    }

    /**
     * TEST-P002: Single Ticker NVDA Request
     * Purpose: Test individual ticker snapshot request (any format acceptable)
     */
    async testP002_SingleTickerNVDA() {
        return this.executeTest('TEST-P002', 'Single Ticker NVDA Request', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input priority fast request with ticker
            await this.inputMessage("Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity");
            
            // Click the Stock Snapshot button (Stock Snapshot)
            await this.clickStockSnapshotButton();
            
            // Wait for response (any format acceptable)
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Validate basic functionality
            const validation = this.validateBasicFunctionality(response, 'NVDA', 'ticker_snapshot');
            if (!validation.success) {
                throw new Error(`Basic functionality validation failed: ${validation.errors.join(', ')}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                response: response,
                validation: validation,
                ticker: 'NVDA',
                hasStructuredContent: validation.hasStructuredContent,
                responseFormat: validation.responseFormat
            };
        });
    }

    /**
     * TEST-P003: Single Ticker SPY Request
     * Purpose: Test individual ticker snapshot request (any format acceptable)
     */
    async testP003_SingleTickerSPY() {
        return this.executeTest('TEST-P003', 'Single Ticker SPY Request', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input priority fast request with ticker
            await this.inputMessage("Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity");
            
            // Click the Stock Snapshot button (Stock Snapshot)
            await this.clickStockSnapshotButton();
            
            // Wait for response (any format acceptable)
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Validate basic functionality
            const validation = this.validateBasicFunctionality(response, 'SPY', 'ticker_snapshot');
            if (!validation.success) {
                throw new Error(`Basic functionality validation failed: ${validation.errors.join(', ')}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                response: response,
                validation: validation,
                ticker: 'SPY',
                hasStructuredContent: validation.hasStructuredContent,
                responseFormat: validation.responseFormat
            };
        });
    }

    /**
     * TEST-P004: Single Ticker GME Request
     * Purpose: Test individual ticker snapshot request (any format acceptable)
     */
    async testP004_SingleTickerGME() {
        return this.executeTest('TEST-P004', 'Single Ticker GME Request', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input priority fast request with ticker
            await this.inputMessage("Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity");
            
            // Click the Stock Snapshot button (Stock Snapshot)
            await this.clickStockSnapshotButton();
            
            // Wait for response (any format acceptable)
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Validate basic functionality
            const validation = this.validateBasicFunctionality(response, 'GME', 'ticker_snapshot');
            if (!validation.success) {
                throw new Error(`Basic functionality validation failed: ${validation.errors.join(', ')}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                response: response,
                validation: validation,
                ticker: 'GME',
                hasStructuredContent: validation.hasStructuredContent,
                responseFormat: validation.responseFormat
            };
        });
    }

    /**
     * TEST-P005: Multi-Ticker Combined Request
     * Purpose: Test multiple ticker combined request (any format acceptable)
     */
    async testP005_MultiTickerCombined() {
        return this.executeTest('TEST-P005', 'Multi-Ticker Combined Request', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input priority fast request with multiple tickers
            await this.inputMessage("Full Market Snapshot with multiple Tickers: NVDA, SPY, QQQ, IWM: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity");
            
            // Click the Stock Snapshot button (Stock Snapshot)
            await this.clickStockSnapshotButton();
            
            // Wait for response (any format acceptable, may take longer for multiple tickers)
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Validate basic functionality with multiple tickers
            const validation = this.validateBasicFunctionality(response, 'NVDA,SPY,QQQ,IWM', 'multi_ticker');
            if (!validation.success) {
                throw new Error(`Basic functionality validation failed: ${validation.errors.join(', ')}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                response: response,
                validation: validation,
                expectedTickers: ['NVDA', 'SPY', 'QQQ', 'IWM'],
                hasStructuredContent: validation.hasStructuredContent,
                responseFormat: validation.responseFormat
            };
        });
    }

    /**
     * Helper method to navigate to the application
     */
    async navigateToApp() {
        this.testStartTime = Date.now();
        // This will be implemented using MCP Playwright tools
        console.log(`Navigating to ${this.baseUrl}`);
        // Actual MCP implementation will be added in the execution layer
    }

    /**
     * Helper method to input a message in the chat interface
     */
    async inputMessage(message) {
        console.log(`Inputting message: ${message}`);
        // This will be implemented using MCP Playwright tools
    }

    /**
     * Helper method to send a message
     */
    async sendMessage() {
        console.log('Sending message...');
        // This will be implemented using MCP Playwright tools
    }

    /**
     * Helper method to click the Stock Snapshot button (Stock Snapshot)
     */
    async clickStockSnapshotButton() {
        console.log('Clicking Stock Snapshot button (Stock Snapshot)...');
        // This will be implemented using MCP Playwright tools
    }

    /**
     * Helper method to wait for response with timeout
     */
    async waitForResponse(timeout) {
        console.log(`Waiting for response (timeout: ${timeout}ms)...`);
        // This will be implemented using MCP Playwright tools
        // Should return the response text/JSON
        return '{"placeholder": "response"}';
    }

    /**
     * Helper method to optionally parse JSON from response text
     * Returns null if response is not JSON (emojis and text responses are acceptable)
     */
    parseJSONFromResponse(responseText) {
        try {
            // Handle case where response might contain JSON within larger text
            const jsonStart = responseText.indexOf('{');
            const jsonEnd = responseText.lastIndexOf('}') + 1;
            
            if (jsonStart !== -1 && jsonEnd > jsonStart) {
                const jsonString = responseText.substring(jsonStart, jsonEnd);
                return JSON.parse(jsonString);
            } else {
                // Try parsing entire response as JSON
                return JSON.parse(responseText);
            }
        } catch (error) {
            // Gracefully handle non-JSON responses (emojis, text, conversational)
            // This is acceptable behavior - not all responses need to be JSON
            return null;
        }
    }

    /**
     * Run all priority tests in sequence
     */
    async runAllPriorityTests() {
        console.log('🚀 Starting Priority Tests Suite - 5 Critical Tests');
        console.log('Target: 100% pass rate required for system validation\n');

        const results = [];

        // Execute priority tests in sequence
        results.push(await this.testP001_MarketStatusRequest());
        results.push(await this.testP002_SingleTickerNVDA());
        results.push(await this.testP003_SingleTickerSPY());
        results.push(await this.testP004_SingleTickerGME());
        results.push(await this.testP005_MultiTickerCombined());

        // Generate priority test report
        const priorityPassRate = results.filter(r => r.status === 'PASS').length / results.length * 100;
        
        console.log('\nPriority Tests Summary:');
        console.log(`Total Tests: ${results.length}`);
        console.log(`Passed: ${results.filter(r => r.status === 'PASS').length}`);
        console.log(`Failed: ${results.filter(r => r.status === 'FAIL').length}`);
        console.log(`Pass Rate: ${priorityPassRate.toFixed(1)}%`);
        console.log(`Status: ${priorityPassRate >= 100 ? 'SYSTEM VALIDATED ✅' : 'CRITICAL ISSUES ❌'}`);

        return results;
    }
}

module.exports = { PriorityTestsSuite };