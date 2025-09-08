/**
 * Priority Tests Implementation - TEST-P001 through TEST-P005
 * 
 * These are the 5 critical tests that must pass for system validation.
 * Focus on simple "Raw Output Format Only with NO verbosity" requests
 * and JSON schema validation.
 */

const { PlaywrightMCPTestFramework } = require('./test_framework');

class PriorityTestsSuite extends PlaywrightMCPTestFramework {
    constructor() {
        super();
    }

    /**
     * TEST-P001: Market Status Raw JSON
     * Purpose: Verify system can return raw market status data
     */
    async testP001_MarketStatusRawJSON() {
        return this.executeTest('TEST-P001', 'Market Status Raw JSON', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input the simple raw JSON request
            const inputQuery = "Raw Output Format Only with NO verbosity";
            await this.inputMessage(inputQuery);
            
            // Send the message
            await this.sendMessage();
            
            // Wait for response (120 seconds timeout)
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Parse JSON from response
            const jsonData = this.parseJSONFromResponse(response);
            
            // Validate against market status schema
            const validation = this.validateSchema(jsonData, 'marketStatus');
            if (!validation.success) {
                throw new Error(`Schema validation failed: ${validation.errors.join(', ')}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                jsonData: jsonData,
                validation: validation
            };
        });
    }

    /**
     * TEST-P002: Single Ticker NVDA Raw JSON
     * Purpose: Test individual ticker snapshot request
     */
    async testP002_SingleTickerNVDA() {
        return this.executeTest('TEST-P002', 'Single Ticker NVDA Raw JSON', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input ticker symbol first
            await this.inputMessage("NVDA");
            
            // Click the Stock Snapshot button (📈)
            await this.clickStockSnapshotButton();
            
            // Wait for JSON response
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Parse and validate JSON
            const jsonData = this.parseJSONFromResponse(response);
            
            const validation = this.validateSchema(jsonData, 'snapshot');
            if (!validation.success) {
                throw new Error(`Schema validation failed: ${validation.errors.join(', ')}`);
            }
            
            // Verify ticker symbol matches
            if (jsonData.metadata && jsonData.metadata.ticker_symbol !== 'NVDA') {
                throw new Error(`Expected ticker NVDA, got ${jsonData.metadata.ticker_symbol}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                jsonData: jsonData,
                validation: validation,
                ticker: 'NVDA'
            };
        });
    }

    /**
     * TEST-P003: Single Ticker SPY Raw JSON
     * Purpose: Test individual ticker snapshot request
     */
    async testP003_SingleTickerSPY() {
        return this.executeTest('TEST-P003', 'Single Ticker SPY Raw JSON', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input ticker symbol
            await this.inputMessage("SPY");
            
            // Click the Stock Snapshot button (📈)
            await this.clickStockSnapshotButton();
            
            // Wait for JSON response
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Parse and validate JSON
            const jsonData = this.parseJSONFromResponse(response);
            
            const validation = this.validateSchema(jsonData, 'snapshot');
            if (!validation.success) {
                throw new Error(`Schema validation failed: ${validation.errors.join(', ')}`);
            }
            
            // Verify ticker symbol matches
            if (jsonData.metadata && jsonData.metadata.ticker_symbol !== 'SPY') {
                throw new Error(`Expected ticker SPY, got ${jsonData.metadata.ticker_symbol}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                jsonData: jsonData,
                validation: validation,
                ticker: 'SPY'
            };
        });
    }

    /**
     * TEST-P004: Single Ticker GME Raw JSON
     * Purpose: Test individual ticker snapshot request
     */
    async testP004_SingleTickerGME() {
        return this.executeTest('TEST-P004', 'Single Ticker GME Raw JSON', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input ticker symbol
            await this.inputMessage("GME");
            
            // Click the Stock Snapshot button (📈)
            await this.clickStockSnapshotButton();
            
            // Wait for JSON response
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Parse and validate JSON
            const jsonData = this.parseJSONFromResponse(response);
            
            const validation = this.validateSchema(jsonData, 'snapshot');
            if (!validation.success) {
                throw new Error(`Schema validation failed: ${validation.errors.join(', ')}`);
            }
            
            // Verify ticker symbol matches
            if (jsonData.metadata && jsonData.metadata.ticker_symbol !== 'GME') {
                throw new Error(`Expected ticker GME, got ${jsonData.metadata.ticker_symbol}`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                jsonData: jsonData,
                validation: validation,
                ticker: 'GME'
            };
        });
    }

    /**
     * TEST-P005: Multi-Ticker Combined Raw JSON
     * Purpose: Test multiple ticker combined request
     */
    async testP005_MultiTickerCombined() {
        return this.executeTest('TEST-P005', 'Multi-Ticker Combined Raw JSON', async () => {
            // Navigate to application
            await this.navigateToApp();
            
            // Input multiple ticker symbols
            await this.inputMessage("NVDA, SPY, QQQ, IWM");
            
            // Click the Stock Snapshot button (📈)
            await this.clickStockSnapshotButton();
            
            // Wait for JSON response (may take longer for multiple tickers)
            const response = await this.waitForResponse(this.timeouts.apiResponse);
            
            // Parse JSON - expect array or object with multiple tickers
            const jsonData = this.parseJSONFromResponse(response);
            
            // Validate structure - could be array or object with ticker data
            let tickerCount = 0;
            const expectedTickers = ['NVDA', 'SPY', 'QQQ', 'IWM'];
            
            if (Array.isArray(jsonData)) {
                tickerCount = jsonData.length;
                // Validate each item in array
                jsonData.forEach((item, index) => {
                    const validation = this.validateSchema(item, 'snapshot');
                    if (!validation.success) {
                        throw new Error(`Item ${index} schema validation failed: ${validation.errors.join(', ')}`);
                    }
                });
            } else if (jsonData.metadata && jsonData.snapshot_data) {
                // Single object response - validate as snapshot
                const validation = this.validateSchema(jsonData, 'snapshot');
                if (!validation.success) {
                    throw new Error(`Schema validation failed: ${validation.errors.join(', ')}`);
                }
                tickerCount = 1;
            } else {
                // Check if it's an object with ticker keys
                const tickerKeys = Object.keys(jsonData).filter(key => 
                    expectedTickers.includes(key.toUpperCase())
                );
                tickerCount = tickerKeys.length;
            }
            
            // Verify we got data for multiple tickers
            if (tickerCount < 2) {
                throw new Error(`Expected multiple tickers, got data for ${tickerCount} tickers`);
            }
            
            return {
                responseTime: Date.now() - this.testStartTime,
                jsonData: jsonData,
                tickerCount: tickerCount,
                expectedTickers: expectedTickers
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
     * Helper method to click the Stock Snapshot button (📈)
     */
    async clickStockSnapshotButton() {
        console.log('Clicking Stock Snapshot button (📈)...');
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
     * Helper method to parse JSON from response text
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
            throw new Error(`Failed to parse JSON from response: ${error.message}\nResponse: ${responseText}`);
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
        results.push(await this.testP001_MarketStatusRawJSON());
        results.push(await this.testP002_SingleTickerNVDA());
        results.push(await this.testP003_SingleTickerSPY());
        results.push(await this.testP004_SingleTickerGME());
        results.push(await this.testP005_MultiTickerCombined());

        // Generate priority test report
        const priorityPassRate = results.filter(r => r.status === 'PASS').length / results.length * 100;
        
        console.log('\n📊 Priority Tests Summary:');
        console.log(`Total Tests: ${results.length}`);
        console.log(`Passed: ${results.filter(r => r.status === 'PASS').length}`);
        console.log(`Failed: ${results.filter(r => r.status === 'FAIL').length}`);
        console.log(`Pass Rate: ${priorityPassRate.toFixed(1)}%`);
        console.log(`Status: ${priorityPassRate >= 100 ? 'SYSTEM VALIDATED ✅' : 'CRITICAL ISSUES ❌'}`);

        return results;
    }
}

module.exports = { PriorityTestsSuite };