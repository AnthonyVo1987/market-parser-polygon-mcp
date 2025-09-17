import { test, expect } from '@playwright/test';

test.describe('Basic Test Suite', () => {
  test.setTimeout(120000); // 120-second timeout for entire test suite

  test('Test 1: Market Status', async ({ page }) => {
    test.setTimeout(120000); // Also set per-test timeout

    // Step 1: Navigate to the application
    await page.goto('http://127.0.0.1:3000');
    await page.waitForLoadState('networkidle');

    // Step 2: Locate input field using modern Playwright locators
    const messageInput = page.getByPlaceholder(/message/i).or(
      page.locator('.chat-input textarea')
    ).or(
      page.locator('input[type="text"]')
    );

    await messageInput.fill('Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity');
    await messageInput.press('Enter');

    // Step 3: Wait for response with auto-retry detection
    await page.waitForSelector('text=🎯 KEY TAKEAWAYS', { timeout: 120000 });

    // Step 4: Web-first assertions using modern Playwright patterns
    const lastMessage = page.locator('.message-content').last();

    // Assert response exists and is visible
    await expect(lastMessage).toBeVisible({ timeout: 5000 });

    // Assert financial content using web-first assertions
    await expect(lastMessage).toContainText(/[📈📉💰🎯]/);
    await expect(lastMessage).toContainText(/market|trading|status/i);

    // Assert minimum content length using evaluate for complex validation
    const contentLength = await lastMessage.textContent();
    expect(contentLength?.length || 0).toBeGreaterThan(50);
  });

  test('Test 2: NVDA Ticker Snapshot', async ({ page }) => {
    test.setTimeout(120000); // Also set per-test timeout

    // Step 1: Navigate to the application
    await page.goto('http://127.0.0.1:3000');
    await page.waitForLoadState('networkidle');

    // Step 2: Locate input field using modern Playwright locators
    const messageInput = page.getByPlaceholder(/message/i).or(
      page.locator('.chat-input textarea')
    ).or(
      page.locator('input[type="text"]')
    );

    await messageInput.fill('Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity');
    await messageInput.press('Enter');

    // Step 3: Auto-retry detection with fallback
    try {
      await page.waitForSelector('text=📈', { timeout: 120000 });
    } catch (error) {
      await page.waitForSelector(':text("NVIDIA")', { timeout: 120000 });
    }

    // Step 4: Web-first assertions using modern Playwright patterns
    const lastMessage = page.locator('.message-content').last();

    // Assert response exists and is visible
    await expect(lastMessage).toBeVisible({ timeout: 5000 });

    // Assert NVDA-specific content using web-first assertions
    await expect(lastMessage).toContainText(/[📈📉💰🎯]/);
    await expect(lastMessage).toContainText(/nvda|nvidia/i);
    await expect(lastMessage).toContainText(/price|volume|share|stock/i);

    // Assert minimum content length
    const contentLength = await lastMessage.textContent();
    expect(contentLength?.length || 0).toBeGreaterThan(50);
  });

  test('Test 3: Stock Snapshot Button', async ({ page }) => {
    test.setTimeout(120000); // Also set per-test timeout

    // Step 1: Navigate to the application
    await page.goto('http://127.0.0.1:3000');
    await page.waitForLoadState('networkidle');

    // Step 2: Pre-populate input field using modern locators
    const messageInput = page.getByPlaceholder(/message/i).or(
      page.locator('.chat-input textarea')
    ).or(
      page.locator('input[type="text"]')
    );
    await messageInput.fill('NVDA');

    // Step 3: Click Stock Snapshot button using modern role-based locator
    const snapshotButton = page.getByRole('button', { name: /stock snapshot|📈/i }).or(
      page.getByTestId('stock-snapshot-button')
    ).or(
      page.locator('button:has-text("📈")')
    );
    await snapshotButton.click();

    // Step 4: Auto-retry detection with fallback
    try {
      await page.waitForSelector('text=📈', { timeout: 120000 });
    } catch (error) {
      await page.waitForSelector(':text("Market Snapshot")', { timeout: 120000 });
    }

    // Step 5: Web-first assertions for button-triggered response
    const lastMessage = page.locator('.message-content').last();

    // Assert response exists and is visible
    await expect(lastMessage).toBeVisible({ timeout: 5000 });

    // Assert button-triggered snapshot content
    await expect(lastMessage).toContainText(/[📈📉💰🎯]/);
    await expect(lastMessage).toContainText(/snapshot|stock|price|volume/i);
    await expect(lastMessage).toContainText(/nvda|nvidia|snapshot|market/i);

    // Assert minimum content length
    const contentLength = await lastMessage.textContent();
    expect(contentLength?.length || 0).toBeGreaterThan(50);
  });
});