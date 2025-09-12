/**
 * UI Investigation Test
 * 
 * Captures actual frontend UI state to understand button availability
 */

import { test, expect } from '@playwright/test';

test.describe('UI Investigation', () => {
  
  test('should capture frontend UI state and buttons', async ({ page }) => {
    console.log('[UI-INVESTIGATION] Starting frontend UI analysis...');
    
    // Navigate to frontend
    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    console.log('[UI-INVESTIGATION] Page loaded, analyzing UI elements...');
    
    // Take screenshot
    await page.screenshot({ path: 'test-results/frontend-ui-state.png', fullPage: true });
    
    // Find all buttons
    const allButtons = await page.locator('button').all();
    console.log(`[UI-INVESTIGATION] Found ${allButtons.length} buttons total`);
    
    for (let i = 0; i < allButtons.length; i++) {
      const button = allButtons[i];
      const text = await button.textContent();
      const isVisible = await button.isVisible();
      const classes = await button.getAttribute('class');
      const id = await button.getAttribute('id');
      const dataTestId = await button.getAttribute('data-testid');
      
      console.log(`[UI-INVESTIGATION] Button ${i + 1}: text="${text}", visible=${isVisible}, classes="${classes}", id="${id}", data-testid="${dataTestId}"`);
    }
    
    // Check for specific financial button indicators
    const emojiButtons = await page.locator('button').getByText(/📈|📊|🎯|🔧/).all();
    console.log(`[UI-INVESTIGATION] Found ${emojiButtons.length} emoji-based buttons`);
    
    // Check for text-based buttons
    const financialTextButtons = await page.locator('button').filter({ hasText: /stock|snapshot|support|resistance|technical|analysis/i }).all();
    console.log(`[UI-INVESTIGATION] Found ${financialTextButtons.length} financial text-based buttons`);
    
    // Check for any divs that might be clickable but not buttons
    const clickableDivs = await page.locator('div[onclick], div[role="button"]').all();
    console.log(`[UI-INVESTIGATION] Found ${clickableDivs.length} clickable div elements`);
    
    // Capture page HTML for analysis
    const pageContent = await page.content();
    const buttonHtml = pageContent.match(/<button[^>]*>.*?<\/button>/gi) || [];
    console.log(`[UI-INVESTIGATION] Button HTML patterns found: ${buttonHtml.length}`);
    
    for (let i = 0; i < Math.min(buttonHtml.length, 5); i++) {
      console.log(`[UI-INVESTIGATION] Button HTML ${i + 1}: ${buttonHtml[i]}`);
    }
    
    // Check page title and URL
    const title = await page.title();
    const url = page.url();
    console.log(`[UI-INVESTIGATION] Page title: "${title}"`);
    console.log(`[UI-INVESTIGATION] Page URL: ${url}`);
    
    // Check for input elements
    const inputs = await page.locator('input, textarea').all();
    console.log(`[UI-INVESTIGATION] Found ${inputs.length} input elements`);
    
    for (let i = 0; i < inputs.length; i++) {
      const input = inputs[i];
      const placeholder = await input.getAttribute('placeholder');
      const type = await input.getAttribute('type');
      const isVisible = await input.isVisible();
      
      console.log(`[UI-INVESTIGATION] Input ${i + 1}: type="${type}", placeholder="${placeholder}", visible=${isVisible}`);
    }
    
    console.log('[UI-INVESTIGATION] UI investigation completed');
  });
  
});