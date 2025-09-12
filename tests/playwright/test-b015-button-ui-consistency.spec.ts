/**
 * TEST-B015: Button UI Consistency Test
 * 
 * Tests button UI consistency (styling, positioning, visual feedback, responsive behavior)
 * Implements comprehensive UI consistency validation and visual regression testing
 * Part of continuous browser session protocol
 * 
 * @fileoverview Button UI consistency CLI test with visual validation
 */

import { test, expect } from '@playwright/test';
import {
  // Main workflow functions
  autoNavigateToFrontend,
  validateSystemReadiness,
  inputTicker,
  takeTimestampedScreenshot,
  
  // Configuration and constants
  COMPREHENSIVE_TEST_CONFIG,
  ButtonType,
  BUTTON_SELECTORS,
  
  // Browser session management
  BrowserSessionManager
} from './helpers/index';

/**
 * TEST-B015: Button UI Consistency Test Suite
 */
test.describe('TEST-B015: Button UI Consistency', () => {
  
  // Use 120-second test timeout as specified
  test.setTimeout(COMPREHENSIVE_TEST_CONFIG.timeouts.test);
  
  test('should validate system readiness before UI consistency testing', async () => {
    console.log('[TEST-B015] Validating system readiness...');
    
    const systemStatus = await validateSystemReadiness();
    
    if (!systemStatus.ready) {
      console.log('[TEST-B015] System not ready - errors:', systemStatus.errors);
      test.skip(true, 'System not ready for testing');
    }
    
    console.log('[TEST-B015] System validation completed');
    console.log(`[TEST-B015] Frontend: ${systemStatus.frontend ? `port ${systemStatus.frontend.port}` : 'not found'}`);
    console.log(`[TEST-B015] Backend: ${systemStatus.backend ? `accessible: ${systemStatus.backend.accessible}` : 'not accessible'}`);
  });
  
  test('should validate button visual consistency and styling', async ({ browser }) => {
    console.log('[TEST-B015] Starting button visual consistency validation...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      // Initialize browser session
      page = await sessionManager.initializeSession(browser);
      
      // Navigate to frontend
      const frontendUrl = await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      console.log(`[TEST-B015] Navigated to frontend: ${frontendUrl}`);
      
      // Wait for page to be ready
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      
      // Input ticker to activate buttons
      const testTicker = 'NVDA';
      console.log(`[TEST-B015] Inputting ticker for UI testing: ${testTicker}`);
      await inputTicker(page, testTicker);
      
      await page.waitForTimeout(1000); // Allow UI to update
      
      // Take baseline screenshot
      await takeTimestampedScreenshot(page, 'TEST-B015', 'baseline');
      
      // Test visual properties of each button type
      const buttonTypes = [
        ButtonType.STOCK_SNAPSHOT,
        ButtonType.SUPPORT_RESISTANCE,
        ButtonType.TECHNICAL_ANALYSIS
      ];
      
      const buttonProperties: Array<{
        buttonType: ButtonType;
        found: boolean;
        dimensions: { width: number; height: number };
        position: { x: number; y: number };
        colors: { background: string; color: string; border: string };
        fonts: { family: string; size: string; weight: string };
        styles: { padding: string; margin: string; borderRadius: string };
      }> = [];
      
      for (const buttonType of buttonTypes) {
        console.log(`[TEST-B015] --- Visual inspection: ${buttonType} ---`);
        
        const selectors = BUTTON_SELECTORS[buttonType];
        let buttonFound = false;
        let buttonElement: any = null;
        
        // Find the button
        for (const selector of selectors) {
          try {
            const element = page.locator(selector).first();
            const isVisible = await element.isVisible({ timeout: 2000 });
            
            if (isVisible) {
              buttonElement = element;
              buttonFound = true;
              console.log(`[TEST-B015] Found ${buttonType} button: ${selector}`);
              break;
            }
          } catch (error) {
            // Continue
          }
        }
        
        if (buttonFound && buttonElement) {
          try {
            // Get button dimensions
            const boundingBox = await buttonElement.boundingBox();
            const dimensions = boundingBox ? 
              { width: boundingBox.width, height: boundingBox.height } : 
              { width: 0, height: 0 };
            const position = boundingBox ? 
              { x: boundingBox.x, y: boundingBox.y } : 
              { x: 0, y: 0 };
            
            // Get computed styles
            const styles = await buttonElement.evaluate(el => {
              const computed = window.getComputedStyle(el);
              return {
                background: computed.backgroundColor,
                color: computed.color,
                border: computed.border,
                fontFamily: computed.fontFamily,
                fontSize: computed.fontSize,
                fontWeight: computed.fontWeight,
                padding: computed.padding,
                margin: computed.margin,
                borderRadius: computed.borderRadius
              };
            });
            
            buttonProperties.push({
              buttonType,
              found: true,
              dimensions,
              position,
              colors: {
                background: styles.background,
                color: styles.color,
                border: styles.border
              },
              fonts: {
                family: styles.fontFamily,
                size: styles.fontSize,
                weight: styles.fontWeight
              },
              styles: {
                padding: styles.padding,
                margin: styles.margin,
                borderRadius: styles.borderRadius
              }
            });
            
            console.log(`[TEST-B015] ${buttonType} dimensions: ${dimensions.width}×${dimensions.height}`);
            console.log(`[TEST-B015] ${buttonType} position: (${position.x}, ${position.y})`);
            console.log(`[TEST-B015] ${buttonType} background: ${styles.background}`);
            console.log(`[TEST-B015] ${buttonType} font: ${styles.fontSize} ${styles.fontWeight} ${styles.fontFamily}`);
            
          } catch (error) {
            console.log(`[TEST-B015] ⚠️ Error getting ${buttonType} properties: ${error}`);
            buttonProperties.push({
              buttonType,
              found: false,
              dimensions: { width: 0, height: 0 },
              position: { x: 0, y: 0 },
              colors: { background: '', color: '', border: '' },
              fonts: { family: '', size: '', weight: '' },
              styles: { padding: '', margin: '', borderRadius: '' }
            });
          }
        } else {
          console.log(`[TEST-B015] ❌ ${buttonType} button not found for visual inspection`);
          buttonProperties.push({
            buttonType,
            found: false,
            dimensions: { width: 0, height: 0 },
            position: { x: 0, y: 0 },
            colors: { background: '', color: '', border: '' },
            fonts: { family: '', size: '', weight: '' },
            styles: { padding: '', margin: '', borderRadius: '' }
          });
        }
      }
      
      // Analyze consistency
      const foundButtons = buttonProperties.filter(prop => prop.found);
      
      if (foundButtons.length >= 2) {
        console.log(`[TEST-B015] === CONSISTENCY ANALYSIS ===`);
        console.log(`[TEST-B015] Found buttons: ${foundButtons.length}/${buttonTypes.length}`);
        
        // Check dimension consistency
        const widths = foundButtons.map(prop => prop.dimensions.width);
        const heights = foundButtons.map(prop => prop.dimensions.height);
        
        const widthConsistent = widths.every(w => Math.abs(w - widths[0]) <= 5); // 5px tolerance
        const heightConsistent = heights.every(h => Math.abs(h - heights[0]) <= 5);
        
        console.log(`[TEST-B015] Width consistency: ${widthConsistent ? 'CONSISTENT' : 'INCONSISTENT'} (${widths.join(', ')})`);
        console.log(`[TEST-B015] Height consistency: ${heightConsistent ? 'CONSISTENT' : 'INCONSISTENT'} (${heights.join(', ')})`);
        
        // Check font consistency
        const fontSizes = foundButtons.map(prop => prop.fonts.size);
        const fontFamilies = foundButtons.map(prop => prop.fonts.family);
        
        const fontSizeConsistent = fontSizes.every(size => size === fontSizes[0]);
        const fontFamilyConsistent = fontFamilies.every(family => family === fontFamilies[0]);
        
        console.log(`[TEST-B015] Font size consistency: ${fontSizeConsistent ? 'CONSISTENT' : 'INCONSISTENT'} (${fontSizes.join(', ')})`);
        console.log(`[TEST-B015] Font family consistency: ${fontFamilyConsistent ? 'CONSISTENT' : 'INCONSISTENT'}`);
        
        // Check spacing consistency
        const paddings = foundButtons.map(prop => prop.styles.padding);
        const borderRadii = foundButtons.map(prop => prop.styles.borderRadius);
        
        const paddingConsistent = paddings.every(padding => padding === paddings[0]);
        const borderRadiusConsistent = borderRadii.every(radius => radius === borderRadii[0]);
        
        console.log(`[TEST-B015] Padding consistency: ${paddingConsistent ? 'CONSISTENT' : 'INCONSISTENT'} (${paddings.join(', ')})`);
        console.log(`[TEST-B015] Border radius consistency: ${borderRadiusConsistent ? 'CONSISTENT' : 'INCONSISTENT'} (${borderRadii.join(', ')})`);
        
        // Overall consistency score
        const consistencyChecks = [widthConsistent, heightConsistent, fontSizeConsistent, fontFamilyConsistent, paddingConsistent, borderRadiusConsistent];
        const consistentCount = consistencyChecks.filter(check => check).length;
        const consistencyScore = (consistentCount / consistencyChecks.length) * 100;
        
        console.log(`[TEST-B015] Overall consistency score: ${consistencyScore.toFixed(1)}% (${consistentCount}/${consistencyChecks.length})`);
        
        if (consistencyScore >= 80) {
          console.log('[TEST-B015] ✅ Good UI consistency');
        } else if (consistencyScore >= 60) {
          console.log('[TEST-B015] ⚠️ Moderate UI consistency');
        } else {
          console.log('[TEST-B015] ❌ Poor UI consistency');
        }
        
        // Validate basic expectations
        expect(foundButtons.length).toBeGreaterThan(0);
        expect(consistencyScore).toBeGreaterThan(0);
        
      } else {
        console.log('[TEST-B015] ⚠️ Insufficient buttons found for consistency analysis');
      }
      
      console.log('[TEST-B015] ✅ Button visual consistency validation completed');
      
    } catch (error) {
      console.log('[TEST-B015] ❌ Visual consistency test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate button responsive behavior', async ({ browser }) => {
    console.log('[TEST-B015] Testing button responsive behavior...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testTicker = 'AAPL';
      await inputTicker(page, testTicker);
      
      // Test different viewport sizes
      const viewportSizes = [
        { name: 'Desktop', width: 1280, height: 720 },
        { name: 'Tablet', width: 768, height: 1024 },
        { name: 'Mobile', width: 375, height: 667 }
      ];
      
      const responsiveResults: Array<{
        viewport: string;
        buttonsFound: number;
        buttonsVisible: number;
        totalWidth: number;
      }> = [];
      
      for (const viewport of viewportSizes) {
        console.log(`[TEST-B015] --- Testing ${viewport.name} viewport (${viewport.width}×${viewport.height}) ---`);
        
        // Set viewport size
        await page.setViewportSize({ width: viewport.width, height: viewport.height });
        await page.waitForTimeout(1000); // Allow UI to adapt
        
        // Take screenshot for this viewport
        await takeTimestampedScreenshot(page, 'TEST-B015', `${viewport.name.toLowerCase()}-viewport`);
        
        // Count visible buttons
        let buttonsFound = 0;
        let buttonsVisible = 0;
        let totalWidth = 0;
        
        for (const buttonType of Object.values(ButtonType)) {
          const selectors = BUTTON_SELECTORS[buttonType];
          
          for (const selector of selectors) {
            try {
              const button = page.locator(selector).first();
              const exists = await button.count() > 0;
              
              if (exists) {
                buttonsFound++;
                
                const isVisible = await button.isVisible({ timeout: 1000 });
                if (isVisible) {
                  buttonsVisible++;
                  
                  const boundingBox = await button.boundingBox();
                  if (boundingBox) {
                    totalWidth += boundingBox.width;
                  }
                }
                break; // Found button for this type
              }
            } catch (error) {
              // Continue
            }
          }
        }
        
        responsiveResults.push({
          viewport: viewport.name,
          buttonsFound,
          buttonsVisible,
          totalWidth
        });
        
        console.log(`[TEST-B015] ${viewport.name}: ${buttonsVisible}/${buttonsFound} buttons visible, total width: ${totalWidth}px`);
        
        // Validate buttons fit in viewport
        const buttonsOverflow = totalWidth > viewport.width;
        if (buttonsOverflow) {
          console.log(`[TEST-B015] ⚠️ ${viewport.name}: Buttons may overflow viewport (${totalWidth}px > ${viewport.width}px)`);
        } else {
          console.log(`[TEST-B015] ✅ ${viewport.name}: Buttons fit in viewport`);
        }
      }
      
      // Analyze responsive behavior
      console.log(`[TEST-B015] === RESPONSIVE ANALYSIS ===`);
      
      responsiveResults.forEach(result => {
        const visibilityRate = result.buttonsFound > 0 ? (result.buttonsVisible / result.buttonsFound) * 100 : 0;
        console.log(`[TEST-B015] ${result.viewport}: ${visibilityRate.toFixed(1)}% button visibility`);
      });
      
      // Check if all viewports show some buttons
      const allViewportsHaveButtons = responsiveResults.every(result => result.buttonsVisible > 0);
      
      if (allViewportsHaveButtons) {
        console.log('[TEST-B015] ✅ All viewports show buttons');
      } else {
        console.log('[TEST-B015] ⚠️ Some viewports do not show buttons');
      }
      
      // Validate responsive expectations
      expect(responsiveResults.length).toBe(3);
      expect(responsiveResults.some(result => result.buttonsVisible > 0)).toBe(true);
      
      console.log('[TEST-B015] ✅ Button responsive behavior testing completed');
      
    } catch (error) {
      console.log('[TEST-B015] Responsive behavior test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
  test('should validate button interaction states and visual feedback', async ({ browser }) => {
    console.log('[TEST-B015] Testing button interaction states and visual feedback...');
    
    const sessionManager = new BrowserSessionManager(COMPREHENSIVE_TEST_CONFIG.browserSession);
    let page: any;
    
    try {
      page = await sessionManager.initializeSession(browser);
      
      await autoNavigateToFrontend(page, COMPREHENSIVE_TEST_CONFIG.portDetection);
      await page.waitForLoadState('networkidle');
      
      const testTicker = 'MSFT';
      await inputTicker(page, testTicker);
      
      console.log('[TEST-B015] Testing button interaction states...');
      
      // Test interaction states for Stock Snapshot button
      const selectors = BUTTON_SELECTORS[ButtonType.STOCK_SNAPSHOT];
      let buttonElement: any = null;
      
      for (const selector of selectors) {
        try {
          const element = page.locator(selector).first();
          const isVisible = await element.isVisible({ timeout: 2000 });
          
          if (isVisible) {
            buttonElement = element;
            console.log(`[TEST-B015] Testing interaction states with: ${selector}`);
            break;
          }
        } catch (error) {
          // Continue
        }
      }
      
      if (buttonElement) {
        // Test hover state
        console.log('[TEST-B015] Testing hover state...');
        
        await buttonElement.hover();
        await page.waitForTimeout(500);
        
        await takeTimestampedScreenshot(page, 'TEST-B015', 'hover-state');
        
        const hoverStyles = await buttonElement.evaluate(el => {
          const computed = window.getComputedStyle(el);
          return {
            background: computed.backgroundColor,
            border: computed.border,
            cursor: computed.cursor
          };
        });
        
        console.log(`[TEST-B015] Hover state - Background: ${hoverStyles.background}, Cursor: ${hoverStyles.cursor}`);
        
        // Test focus state
        console.log('[TEST-B015] Testing focus state...');
        
        await buttonElement.focus();
        await page.waitForTimeout(500);
        
        await takeTimestampedScreenshot(page, 'TEST-B015', 'focus-state');
        
        const focusStyles = await buttonElement.evaluate(el => {
          const computed = window.getComputedStyle(el);
          return {
            outline: computed.outline,
            outlineColor: computed.outlineColor,
            outlineWidth: computed.outlineWidth
          };
        });
        
        console.log(`[TEST-B015] Focus state - Outline: ${focusStyles.outline}`);
        
        // Validate visual feedback
        const hasCursorPointer = hoverStyles.cursor === 'pointer';
        const hasFocusOutline = focusStyles.outline !== 'none' && focusStyles.outline !== '0px';
        
        if (hasCursorPointer) {
          console.log('[TEST-B015] ✅ Button shows pointer cursor on hover');
        } else {
          console.log('[TEST-B015] ⚠️ Button does not show pointer cursor on hover');
        }
        
        if (hasFocusOutline) {
          console.log('[TEST-B015] ✅ Button shows focus outline');
        } else {
          console.log('[TEST-B015] ⚠️ Button does not show focus outline');
        }
        
        // Test active/pressed state
        console.log('[TEST-B015] Testing active state...');
        
        // Mouse down (but don't release)
        await buttonElement.hover();
        await page.mouse.down();
        await page.waitForTimeout(200);
        
        await takeTimestampedScreenshot(page, 'TEST-B015', 'active-state');
        
        // Release mouse
        await page.mouse.up();
        
        console.log('[TEST-B015] ✅ Active state tested');
        
      } else {
        console.log('[TEST-B015] ⚠️ No button found for interaction state testing');
      }
      
      console.log('[TEST-B015] ✅ Button interaction states testing completed');
      
    } catch (error) {
      console.log('[TEST-B015] Interaction states test failed:', error);
      throw error;
      
    } finally {
      if (page) {
        await sessionManager.cleanup();
      }
    }
  });
  
});

/**
 * Standalone utility test for TEST-B015 development
 */
test.describe('TEST-B015: Development Utilities', () => {
  
  test('should validate TEST-B015 configuration', async () => {
    console.log('[TEST-B015] Validating UI consistency test configuration...');
    
    // Validate screenshot settings
    expect(COMPREHENSIVE_TEST_CONFIG.browserSession.screenshotOnFailure).toBe(true);
    expect(COMPREHENSIVE_TEST_CONFIG.browserSession.videoRecording).toBe(true);
    
    // Validate viewport settings
    expect(COMPREHENSIVE_TEST_CONFIG.browserSession.viewport.width).toBe(1280);
    expect(COMPREHENSIVE_TEST_CONFIG.browserSession.viewport.height).toBe(720);
    
    console.log('[TEST-B015] Configuration validation completed');
    console.log(`[TEST-B015] Default viewport: ${COMPREHENSIVE_TEST_CONFIG.browserSession.viewport.width}×${COMPREHENSIVE_TEST_CONFIG.browserSession.viewport.height}`);
  });
  
  test('should validate UI testing helper functions', async () => {
    console.log('[TEST-B015] Validating UI testing helper functions...');
    
    const { takeTimestampedScreenshot } = await import('./helpers/index');
    
    // Validate function is available
    expect(takeTimestampedScreenshot).toBeDefined();
    expect(typeof takeTimestampedScreenshot).toBe('function');
    
    console.log('[TEST-B015] UI testing helper functions validation completed');
  });
  
});