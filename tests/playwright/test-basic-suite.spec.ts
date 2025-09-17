import { test, expect } from '@playwright/test';

test.describe('Basic Test Suite', () => {
  test.setTimeout(120000); // 120-second timeout for entire test suite

  test('Test 1: Market Status', async ({ page }) => {
    test.setTimeout(120000); // Also set per-test timeout

    // Step 1: Navigate to the application
    await page.goto('http://127.0.0.1:3000');
    await page.waitForLoadState('networkidle');

    // Step 2: Locate input field and send message
    const inputSelector = 'textarea[placeholder*="message"], .chat-input textarea, input[type="text"]';
    const messageInput = page.locator(inputSelector);
    
    await messageInput.fill('Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity');
    await messageInput.press('Enter');

    // Step 3: Wait for response with auto-retry detection
    await page.waitForSelector('text=🎯 KEY TAKEAWAYS', { timeout: 120000 });

    // Step 4: Comprehensive validation
    const validationResult = await page.evaluate(() => {
      const messages = document.querySelectorAll('.message-content');
      const lastMessage = messages[messages.length - 1]?.textContent || '';
      return {
        hasFinancialEmojis: /[📈📉💰🎯]/.test(lastMessage),
        contentLength: lastMessage.length,
        containsMarketData: /market|trading|status/i.test(lastMessage),
        responseFound: lastMessage.length > 0
      };
    });

    // Assert results
    expect(validationResult.responseFound).toBe(true);
    expect(validationResult.hasFinancialEmojis).toBe(true);
    expect(validationResult.containsMarketData).toBe(true);
    expect(validationResult.contentLength).toBeGreaterThan(50);
  });

  test('Test 2: NVDA Ticker Snapshot', async ({ page }) => {
    test.setTimeout(120000); // Also set per-test timeout

    // Step 1: Navigate to the application
    await page.goto('http://127.0.0.1:3000');
    await page.waitForLoadState('networkidle');

    // Step 2: Locate input field and send message
    const inputSelector = 'textarea[placeholder*="message"], .chat-input textarea, input[type="text"]';
    const messageInput = page.locator(inputSelector);
    
    await messageInput.fill('Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity');
    await messageInput.press('Enter');

    // Step 3: Auto-retry detection with fallback
    try {
      await page.waitForSelector('text=📈', { timeout: 120000 });
    } catch (error) {
      await page.waitForSelector(':text("NVIDIA")', { timeout: 120000 });
    }

    // Step 4: Comprehensive validation
    const validationResult = await page.evaluate(() => {
      const messages = document.querySelectorAll('.message-content');
      const lastMessage = messages[messages.length - 1]?.textContent || '';
      return {
        hasFinancialEmojis: /[📈📉💰🎯]/.test(lastMessage),
        contentLength: lastMessage.length,
        containsNVDA: /nvda|nvidia/i.test(lastMessage),
        hasStockData: /price|volume|share|stock/i.test(lastMessage),
        responseFound: lastMessage.length > 0
      };
    });

    // Assert results
    expect(validationResult.responseFound).toBe(true);
    expect(validationResult.hasFinancialEmojis).toBe(true);
    expect(validationResult.containsNVDA).toBe(true);
    expect(validationResult.hasStockData).toBe(true);
    expect(validationResult.contentLength).toBeGreaterThan(50);
  });

  test('Test 3: Stock Snapshot Button', async ({ page }) => {
    test.setTimeout(120000); // Also set per-test timeout

    // Step 1: Navigate to the application
    await page.goto('http://127.0.0.1:3000');
    await page.waitForLoadState('networkidle');

    // Step 2: Pre-populate input field
    const inputSelector = 'textarea[placeholder*="message"], .chat-input textarea, input[type="text"]';
    const messageInput = page.locator(inputSelector);
    await messageInput.fill('NVDA');

    // Step 3: Click the Stock Snapshot button
    const buttonSelector = 'button:has-text("📈"), button:has-text("Stock Snapshot"), [data-testid="stock-snapshot-button"]';
    await page.locator(buttonSelector).click();

    // Step 4: Auto-retry detection with fallback
    try {
      await page.waitForSelector('text=📈', { timeout: 120000 });
    } catch (error) {
      await page.waitForSelector(':text("Market Snapshot")', { timeout: 120000 });
    }

    // Step 5: Comprehensive validation
    const validationResult = await page.evaluate(() => {
      const messages = document.querySelectorAll('.message-content');
      const lastMessage = messages[messages.length - 1]?.textContent || '';
      return {
        hasFinancialEmojis: /[📈📉💰🎯]/.test(lastMessage),
        contentLength: lastMessage.length,
        hasSnapshotContent: /snapshot|stock|price|volume/i.test(lastMessage),
        buttonTriggered: /nvda|nvidia|snapshot|market/i.test(lastMessage),
        responseFound: lastMessage.length > 0
      };
    });

    // Assert results
    expect(validationResult.responseFound).toBe(true);
    expect(validationResult.hasFinancialEmojis).toBe(true);
    expect(validationResult.hasSnapshotContent).toBe(true);
    expect(validationResult.buttonTriggered).toBe(true);
    expect(validationResult.contentLength).toBeGreaterThan(50);
  });
});