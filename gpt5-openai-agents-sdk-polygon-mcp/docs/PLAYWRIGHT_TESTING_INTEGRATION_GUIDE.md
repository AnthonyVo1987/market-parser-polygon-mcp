# Playwright Testing Integration Guide

> **Single Source of Truth for Playwright Integration**  
> Comprehensive guide for implementing Playwright testing in our React/TypeScript/Vite/FastAPI stack

## Executive Summary & Recommendations

### Quick Decision Matrix

| Scenario | Recommended Method | Reason |
|----------|-------------------|--------|
| **AI Agent Testing** | **Method 3: MCP Server Integration** | 20+ tools, structured JSON responses, optimal token efficiency |
| **Interactive AI Testing** | **Method 3: MCP Server Integration** | Real-time DOM analysis, accessibility snapshots |
| **Human Development** | **Method 2: CLI Integration** | Mature ecosystem, universal compatibility |
| **Component Testing** | **Method 2: CLI with React CT** | Proven patterns, extensive documentation |
| **E2E Testing** | **Method 2 or 3** (preference: CLI for teams, MCP for AI) | Both methods equally capable |
| **CI/CD Integration** | **Method 2: CLI Integration** | Proven pipeline patterns, extensive tooling |
| **Prototype Testing** | **Method 3: MCP Server Integration** | Rapid iteration, AI-driven test generation |

### Recommended Approach for Our Stack

**Primary Recommendations by Use Case:**

**For AI Agents & Interactive Testing: Method 3 (MCP Server Integration)**
- 20+ specialized browser automation tools
- Structured JSON responses optimized for AI interpretation
- Token-efficient communication patterns
- Real-time accessibility snapshots and DOM analysis
- OpenAI GUI-specific integration patterns

**For Human Development Teams: Method 2 (CLI Integration)**
- Mature ecosystem with extensive React/TypeScript support
- Seamless Vite integration via `ctViteConfig`
- Proven CI/CD patterns and universal team compatibility
- Rich debugging tools and IDE integration

**For Hybrid Workflows: Combined Approach**
- Use Method 3 for AI-driven exploratory testing and rapid prototyping
- Use Method 2 for stable regression testing and CI/CD integration
- Cross-reference between methods for comprehensive coverage

### Implementation Timeline

- **Week 1**: Foundation setup (CLI method)
- **Week 2**: Component testing configuration
- **Week 3**: E2E testing implementation
- **Week 4**: CI/CD integration and optimization

## What is Playwright?

Playwright is a Node.js library for reliable end-to-end testing that enables testing across all modern browsers with a single API.

### Core Capabilities

- **Cross-Browser Testing**: Chromium, Firefox, WebKit (Safari)
- **Component Testing**: Isolated React component testing with `@playwright/experimental-ct-react`
- **E2E Testing**: Full application testing with real browser automation
- **Performance Testing**: Network monitoring, metrics collection, Lighthouse integration
- **Accessibility Testing**: Built-in accessibility tree inspection and validation
- **Parallel Execution**: Fast test execution across multiple workers
- **Auto-waiting**: Smart waiting for elements without explicit waits

### Benefits for React Testing

- **TypeScript First**: Native TypeScript support with excellent type safety
- **React Integration**: Purpose-built React component testing capabilities
- **Vite Support**: Seamless integration with Vite build system
- **Modern Patterns**: Support for React hooks, context, and modern patterns
- **Visual Testing**: Screenshot comparison and visual regression testing
- **Real Browser Testing**: Tests run in actual browsers, not jsdom

### Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Test Files    │    │   Playwright     │    │    Browsers     │
│  (.spec.ts)     │───▶│    Engine        │───▶│ Chromium/FF/WK  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Component/E2E   │
                       │   Test Runner    │
                       └──────────────────┘
```

## Method 1: MCP Server Integration

### Prerequisites & Requirements

- Node.js 18+ (LTS recommended)
- MCP client implementation
- TypeScript support (recommended)

### Step-by-step Installation

```bash
# Install the MCP server package
npm install -D @playwright/mcp@latest

# Install browser dependencies
npx @playwright/mcp@latest install
```

### MCP Client Configuration

Create `mcp-config.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {
        "NODE_ENV": "test"
      }
    }
  }
}
```

### Usage Examples for AI Agents

#### Basic Navigation and Interaction

```json
{
  "method": "navigate",
  "params": {
    "url": "http://localhost:3000"
  }
}
```

```json
{
  "method": "click",
  "params": {
    "selector": "[data-testid='chat-input']"
  }
}
```

#### Form Interaction with Structured Response

```json
{
  "method": "fill",
  "params": {
    "selector": "textarea[placeholder='Enter your message...']",
    "value": "What is the latest Apple stock price?"
  }
}
```

#### Accessibility Snapshot

```json
{
  "method": "getAccessibilityTree",
  "params": {
    "selector": ".chat-container"
  }
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "role": "region",
    "name": "Chat Interface",
    "children": [
      {
        "role": "textbox",
        "name": "Message input",
        "value": ""
      }
    ]
  },
  "screenshot": "base64-encoded-image"
}
```

### Pros and Cons

**Pros:**
- **AI-Optimized**: Structured JSON responses perfect for AI agents
- **Token Efficient**: Compact, parseable responses reduce token usage
- **Real-time Context**: Live accessibility snapshots
- **Deterministic**: Consistent JSON-based communication
- **Microsoft Official**: Direct Microsoft support and maintenance

**Cons:**
- **Infrastructure Dependency**: Requires MCP client setup
- **Newer Ecosystem**: Less community documentation
- **Learning Curve**: Different paradigm from traditional testing
- **Limited Tooling**: Fewer IDE integrations and debugging tools

### Best Practices

1. **Use for AI Scenarios**: Ideal when AI agents need to interpret test results
2. **Structured Assertions**: Leverage JSON responses for complex validations
3. **Accessibility Focus**: Utilize accessibility tree snapshots for comprehensive testing
4. **Error Handling**: Parse JSON error responses for detailed debugging
5. **Performance Monitoring**: Use structured performance metrics

## Method 2: CLI Integration

### Prerequisites & Requirements

- Node.js 18+ (LTS recommended)
- TypeScript 4.7+ (for type safety)
- React 18+ (for component testing)
- Vite 4+ (for build integration)

### Step-by-step Installation

```bash
# Install Playwright and React component testing
npm install -D @playwright/test @playwright/experimental-ct-react

# Install browsers
npx playwright install

# For TypeScript support (if not already present)
npm install -D typescript @types/node
```

### Configuration Examples

#### Basic Playwright Configuration (`playwright.config.ts`)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://127.0.0.1:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://127.0.0.1:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

#### Component Testing Configuration (`playwright-ct.config.ts`)

```typescript
import { defineConfig, devices } from '@playwright/experimental-ct-react';
import { resolve } from 'path';

export default defineConfig({
  testDir: './src/components/__tests__',
  fullyParallel: true,
  use: {
    trace: 'on-first-retry',
    ctViteConfig: {
      resolve: {
        alias: {
          '@': resolve(__dirname, './src'),
        },
      },
    },
  },
  
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

### Usage Examples

#### E2E Testing Example (`tests/chat-interface.spec.ts`)

```typescript
import { test, expect } from '@playwright/test';

test.describe('Chat Interface', () => {
  test('should send message and receive response', async ({ page }) => {
    await page.goto('/');
    
    // Wait for interface to load
    await expect(page.locator('[data-testid="chat-container"]')).toBeVisible();
    
    // Fill message input
    const messageInput = page.locator('textarea[placeholder*="message"]');
    await messageInput.fill('What is the latest AAPL stock price?');
    
    // Send message
    await page.keyboard.press('Enter');
    
    // Verify message appears in chat
    await expect(page.locator('.message-user')).toContainText('AAPL stock price');
    
    // Wait for AI response
    await expect(page.locator('.message-assistant')).toBeVisible({ timeout: 10000 });
    
    // Verify response contains expected elements
    const response = page.locator('.message-assistant').last();
    await expect(response).toContainText('📈');
    await expect(response).toContainText('KEY TAKEAWAYS');
  });

  test('should handle responsive design', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    const chatContainer = page.locator('[data-testid="chat-container"]');
    await expect(chatContainer).toHaveCSS('padding', '8px');
    
    // Test desktop viewport
    await page.setViewportSize({ width: 1200, height: 800 });
    await expect(chatContainer).toHaveCSS('padding', '24px');
  });
});
```

#### Component Testing Example (`src/components/__tests__/ChatInput.spec.tsx`)

```typescript
import { test, expect } from '@playwright/experimental-ct-react';
import ChatInput from '../ChatInput_OpenAI';

test.describe('ChatInput Component', () => {
  test('should render with proper placeholder', async ({ mount }) => {
    const component = await mount(<ChatInput onSendMessage={() => {}} />);
    
    await expect(component.locator('textarea')).toHaveAttribute(
      'placeholder',
      'Enter your message...'
    );
  });

  test('should handle multi-line input', async ({ mount }) => {
    const messages: string[] = [];
    const component = await mount(
      <ChatInput onSendMessage={(msg) => messages.push(msg)} />
    );
    
    const textarea = component.locator('textarea');
    
    // Type multi-line message
    await textarea.fill('Line 1\nLine 2\nLine 3');
    
    // Verify textarea expands
    const initialHeight = await textarea.evaluate(el => el.scrollHeight);
    expect(initialHeight).toBeGreaterThan(100);
    
    // Send with Enter
    await textarea.press('Enter');
    
    expect(messages[0]).toBe('Line 1\nLine 2\nLine 3');
  });

  test('should handle Shift+Enter for new lines', async ({ mount }) => {
    const component = await mount(<ChatInput onSendMessage={() => {}} />);
    const textarea = component.locator('textarea');
    
    await textarea.fill('First line');
    await textarea.press('Shift+Enter');
    await textarea.type('Second line');
    
    const value = await textarea.inputValue();
    expect(value).toBe('First line\nSecond line');
  });
});
```

### Pros and Cons

**Pros:**
- **Mature Ecosystem**: Extensive documentation and community support
- **Universal Compatibility**: Works with any shell environment
- **Rich Tooling**: IDE integrations, debugging tools, reporter options
- **Proven CI/CD**: Well-established pipeline patterns
- **Full Feature Access**: Complete API access without restrictions
- **Vite Integration**: Seamless build system integration

**Cons:**
- **Verbose Output**: Requires manual parsing for structured data
- **Token Heavy**: Verbose output increases token usage for AI agents
- **Setup Complexity**: More configuration files and setup steps

### Best Practices

1. **Use Page Object Model**: Organize selectors and actions
2. **Implement Auto-waiting**: Leverage built-in waiting mechanisms
3. **Parallel Testing**: Configure workers for faster execution
4. **Screenshot on Failure**: Enable debugging with visual evidence
5. **Trace on Retry**: Capture detailed execution traces
6. **Base URL Configuration**: Use relative URLs with baseURL setting
7. **Test Isolation**: Ensure tests don't depend on each other

## React-Specific Implementation

### Component Testing Setup

#### Test Structure
```
src/
├── components/
│   ├── ChatInput_OpenAI.tsx
│   ├── ChatMessage_OpenAI.tsx
│   └── __tests__/
│       ├── ChatInput.spec.tsx
│       ├── ChatMessage.spec.tsx
│       └── fixtures/
│           └── mockData.ts
```

#### Component Test with Context (`ChatMessage.spec.tsx`)

```typescript
import { test, expect } from '@playwright/experimental-ct-react';
import ChatMessage from '../ChatMessage_OpenAI';
import { ThemeProvider } from '../context/ThemeContext';

test.describe('ChatMessage Component', () => {
  test('should render user message correctly', async ({ mount }) => {
    const component = await mount(
      <ThemeProvider>
        <ChatMessage 
          message="What is AAPL trading at?"
          isUser={true}
        />
      </ThemeProvider>
    );
    
    await expect(component.locator('.message-user')).toBeVisible();
    await expect(component).toContainText('What is AAPL trading at?');
  });

  test('should render assistant message with markdown', async ({ mount }) => {
    const assistantMessage = `
# 📈 AAPL Stock Analysis

**Current Price**: $175.43
**Change**: +$2.15 (+1.24%)

## 📊 Key Takeaways
- Strong upward momentum
- Breaking resistance at $175
    `;
    
    const component = await mount(
      <ChatMessage message={assistantMessage} isUser={false} />
    );
    
    // Check markdown rendering
    await expect(component.locator('h1')).toContainText('📈 AAPL Stock Analysis');
    await expect(component.locator('strong')).toContainText('Current Price');
    await expect(component.locator('ul li')).toContainText('Strong upward momentum');
  });

  test('should handle responsive message bubbles', async ({ mount, page }) => {
    const component = await mount(
      <ChatMessage message="Test message" isUser={true} />
    );
    
    // Mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(component.locator('.message-bubble')).toHaveCSS('max-width', '85%');
    
    // Desktop viewport  
    await page.setViewportSize({ width: 1200, height: 800 });
    await expect(component.locator('.message-bubble')).toHaveCSS('max-width', '70%');
  });
});
```

### E2E Testing Configuration

#### FastAPI Backend Integration

```typescript
// tests/helpers/api.ts
export class APIHelper {
  constructor(private baseURL: string) {}

  async waitForHealthCheck() {
    const response = await fetch(`${this.baseURL}/health`);
    if (!response.ok) {
      throw new Error(`Backend health check failed: ${response.status}`);
    }
  }

  async getChatResponse(message: string) {
    const response = await fetch(`${this.baseURL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    return response.json();
  }
}
```

#### Full Stack E2E Test

```typescript
import { test, expect } from '@playwright/test';
import { APIHelper } from './helpers/api';

test.describe('Full Stack Integration', () => {
  let apiHelper: APIHelper;

  test.beforeEach(async () => {
    apiHelper = new APIHelper('http://localhost:8000');
    await apiHelper.waitForHealthCheck();
  });

  test('should complete full chat workflow', async ({ page }) => {
    await page.goto('/');
    
    // Verify connection to backend
    await expect(page.locator('[data-testid="status-indicator"]')).toHaveClass(/connected/);
    
    // Send financial query
    const messageInput = page.locator('textarea');
    await messageInput.fill('What is the current TSLA stock price and analyst sentiment?');
    await messageInput.press('Enter');
    
    // Wait for backend processing
    await expect(page.locator('.loading-indicator')).toBeVisible();
    await expect(page.locator('.loading-indicator')).toBeHidden({ timeout: 15000 });
    
    // Verify structured response
    const response = page.locator('.message-assistant').last();
    await expect(response).toContainText('🎯 KEY TAKEAWAYS');
    await expect(response).toContainText('📊 DETAILED ANALYSIS');
    
    // Verify financial emojis
    const responseText = await response.textContent();
    expect(responseText).toMatch(/📈|📉/); // Bullish or bearish indicator
    
    // Test export functionality
    await page.locator('[data-testid="export-button"]').click();
    const downloadPromise = page.waitForEvent('download');
    await page.locator('[data-testid="export-markdown"]').click();
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toMatch(/chat-export.*\.md/);
  });
});
```

### Responsive Testing Strategies

```typescript
import { test, expect, devices } from '@playwright/test';

const VIEWPORTS = {
  mobile: { width: 375, height: 667 },
  tablet: { width: 768, height: 1024 },
  desktop: { width: 1200, height: 800 },
  ultrawide: { width: 1920, height: 1080 }
};

test.describe('Responsive Design', () => {
  Object.entries(VIEWPORTS).forEach(([device, viewport]) => {
    test(`should work on ${device} (${viewport.width}x${viewport.height})`, async ({ page }) => {
      await page.setViewportSize(viewport);
      await page.goto('/');
      
      // Test layout adaptation
      const chatContainer = page.locator('[data-testid="chat-container"]');
      
      if (viewport.width <= 767) {
        // Mobile specific tests
        await expect(chatContainer).toHaveCSS('padding', '8px');
        await expect(page.locator('.message-bubble')).toHaveCSS('max-width', '85%');
        
        // Touch-friendly scrollbars
        await expect(page.locator('.chat-messages')).toHaveCSS('scrollbar-width', '10px');
      } else {
        // Desktop specific tests  
        await expect(chatContainer).toHaveCSS('padding', '24px');
        await expect(page.locator('.message-bubble')).toHaveCSS('max-width', '70%');
        
        // Thin scrollbars
        await expect(page.locator('.chat-messages')).toHaveCSS('scrollbar-width', '6px');
      }
      
      // Test interactive elements
      await page.locator('textarea').click();
      await page.locator('textarea').fill('Responsive test message');
      await page.keyboard.press('Enter');
      
      // Verify message appears correctly
      await expect(page.locator('.message-user').last()).toContainText('Responsive test message');
    });
  });
});
```

### Performance Testing Integration

```typescript
import { test, expect } from '@playwright/test';

test.describe('Performance Testing', () => {
  test('should meet performance benchmarks', async ({ page }) => {
    // Start performance monitoring
    await page.goto('/', { waitUntil: 'networkidle' });
    
    // Measure initial load
    const navigationTiming = await page.evaluate(() => JSON.stringify(performance.timing));
    const timing = JSON.parse(navigationTiming);
    const loadTime = timing.loadEventEnd - timing.navigationStart;
    
    expect(loadTime).toBeLessThan(3000); // 3 second load time
    
    // Test interaction performance
    const startTime = Date.now();
    
    await page.locator('textarea').fill('Performance test message');
    await page.locator('textarea').press('Enter');
    
    await expect(page.locator('.message-user').last()).toBeVisible();
    
    const interactionTime = Date.now() - startTime;
    expect(interactionTime).toBeLessThan(200); // 200ms interaction response
  });

  test('should handle memory usage efficiently', async ({ page }) => {
    await page.goto('/');
    
    // Get initial memory usage
    const initialMemory = await page.evaluate(() => (performance as any).memory?.usedJSHeapSize);
    
    // Simulate heavy usage
    for (let i = 0; i < 10; i++) {
      await page.locator('textarea').fill(`Message ${i}: This is a long message to test memory usage patterns`);
      await page.locator('textarea').press('Enter');
      await page.waitForTimeout(100);
    }
    
    // Check memory after heavy usage
    const finalMemory = await page.evaluate(() => (performance as any).memory?.usedJSHeapSize);
    
    if (initialMemory && finalMemory) {
      const memoryIncrease = finalMemory - initialMemory;
      expect(memoryIncrease).toBeLessThan(10 * 1024 * 1024); // Less than 10MB increase
    }
  });
});
```

### Code Examples

#### Custom Fixtures for React Testing

```typescript
// tests/fixtures.ts
import { test as base } from '@playwright/experimental-ct-react';
import type { ReactWrapper } from '@playwright/experimental-ct-react';

type TestFixtures = {
  chatComponent: ReactWrapper;
  mockApiResponse: (response: any) => Promise<void>;
};

export const test = base.extend<TestFixtures>({
  chatComponent: async ({ mount }, use) => {
    const component = await mount(
      <div data-testid="chat-wrapper">
        <ChatInterface />
      </div>
    );
    await use(component);
  },

  mockApiResponse: async ({ page }, use) => {
    await use(async (response) => {
      await page.route('**/api/chat', async route => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify(response)
        });
      });
    });
  },
});
```

#### Hook Testing Strategies

```typescript
// src/hooks/__tests__/useChatHistory.spec.tsx
import { test, expect } from '@playwright/experimental-ct-react';
import { useChatHistory } from '../useChatHistory';

function TestComponent() {
  const { messages, addMessage, clearHistory } = useChatHistory();
  
  return (
    <div>
      <div data-testid="message-count">{messages.length}</div>
      <button 
        data-testid="add-message"
        onClick={() => addMessage('Test message', true)}
      >
        Add Message
      </button>
      <button data-testid="clear-history" onClick={clearHistory}>
        Clear
      </button>
      <div data-testid="messages">
        {messages.map((msg, i) => (
          <div key={i} data-testid={`message-${i}`}>
            {msg.content}
          </div>
        ))}
      </div>
    </div>
  );
}

test.describe('useChatHistory Hook', () => {
  test('should manage message state correctly', async ({ mount }) => {
    const component = await mount(<TestComponent />);
    
    // Initial state
    await expect(component.locator('[data-testid="message-count"]')).toContainText('0');
    
    // Add message
    await component.locator('[data-testid="add-message"]').click();
    await expect(component.locator('[data-testid="message-count"]')).toContainText('1');
    await expect(component.locator('[data-testid="message-0"]')).toContainText('Test message');
    
    // Clear history
    await component.locator('[data-testid="clear-history"]').click();
    await expect(component.locator('[data-testid="message-count"]')).toContainText('0');
  });
});
```

## Decision Framework

## Method 3: MCP Server Integration (Advanced AI-Driven Testing)

> **Advanced Method for AI Agents**  
> Comprehensive MCP server integration for structured, AI-driven browser automation with enhanced OpenAI GUI testing capabilities

### Executive Overview

**Method 3: MCP Server Integration** provides the most advanced approach for AI-driven testing scenarios, offering structured JSON responses, comprehensive tool inventory, and optimized token efficiency. This method is specifically designed for AI agents that need to interpret test results and perform complex browser interactions.

**Key Advantages:**
- **20+ MCP Tools**: Complete browser automation toolkit
- **Structured Responses**: JSON-based output for AI interpretation
- **Token Efficiency**: Compact, parseable responses reduce AI token usage
- **Real-time Context**: Live accessibility snapshots and DOM analysis
- **OpenAI GUI Optimized**: Specific patterns for our React/TypeScript stack

### Prerequisites & Requirements

**System Requirements:**
- Node.js 18+ (LTS recommended)
- MCP client implementation (Claude Desktop, VS Code with MCP extension)
- TypeScript 4.7+ (for enhanced type safety)
- Python 3.10+ (for backend integration)
- Active internet connection (for browser downloads)

**Environment Setup:**
```bash
# Verify Node.js version
node --version  # Should be 18.0.0 or higher

# Verify MCP client availability
# For Claude Desktop: Check settings for MCP servers
# For VS Code: Install MCP extension

# Backend requirements
python --version  # Should be 3.10 or higher
uv --version      # Package manager verification
```

### Complete MCP Tool Inventory & Capabilities Matrix

#### Browser Management Tools

| Tool | Purpose | Parameters | Return Type | OpenAI GUI Use Case |
|------|---------|------------|-------------|---------------------|
| `browser_navigate` | Navigate to URL | `url: string` | Success status | Load chat interface |
| `browser_resize` | Resize browser window | `width: number, height: number` | Success status | Test responsive design |
| `browser_close` | Close current page | None | Success status | Cleanup after tests |
| `browser_install` | Install browser binaries | None | Installation status | Setup environment |

#### Core Interaction Tools

| Tool | Purpose | Parameters | Return Type | OpenAI GUI Use Case |
|------|---------|------------|-------------|---------------------|
| `browser_click` | Click element | `element: string, ref: string, button?: string, doubleClick?: boolean` | Click result | Send button, export buttons |
| `browser_type` | Type text into element | `element: string, ref: string, text: string, slowly?: boolean, submit?: boolean` | Type result | Message input, multi-line queries |
| `browser_press_key` | Press keyboard key | `key: string` | Key press result | Enter, Shift+Enter, Tab navigation |
| `browser_hover` | Hover over element | `element: string, ref: string` | Hover result | Tooltip triggers, button states |
| `browser_drag` | Drag and drop | `startElement: string, startRef: string, endElement: string, endRef: string` | Drag result | File uploads, reordering |

#### Form and Input Tools

| Tool | Purpose | Parameters | Return Type | OpenAI GUI Use Case |
|------|---------|------------|-------------|---------------------|
| `browser_fill_form` | Fill multiple form fields | `fields: Array<{name, type, ref, value}>` | Form fill result | Bulk input operations |
| `browser_select_option` | Select dropdown option | `element: string, ref: string, values: string[]` | Selection result | Template selection |
| `browser_file_upload` | Upload files | `paths: string[]` | Upload result | Document analysis uploads |

#### Testing & Verification Tools

| Tool | Purpose | Parameters | Return Type | OpenAI GUI Use Case |
|------|---------|------------|-------------|---------------------|
| `browser_snapshot` | Accessibility snapshot | None | Structured DOM tree | Page state verification |
| `browser_take_screenshot` | Visual screenshot | `element?: string, ref?: string, fullPage?: boolean, type?: 'png'\|'jpeg'` | Image data | Visual regression testing |
| `browser_evaluate` | Execute JavaScript | `function: string, element?: string, ref?: string` | Evaluation result | State inspection, custom logic |
| `browser_console_messages` | Get console logs | None | Console messages | Error detection |
| `browser_network_requests` | Get network activity | None | Network requests | API call verification |

#### Advanced Features

| Tool | Purpose | Parameters | Return Type | OpenAI GUI Use Case |
|------|---------|------------|-------------|---------------------|
| `browser_handle_dialog` | Handle alerts/dialogs | `accept: boolean, promptText?: string` | Dialog result | Confirmation handling |
| `browser_tabs` | Manage browser tabs | `action: 'list'\|'new'\|'close'\|'select', index?: number` | Tab management | Multi-tab testing |
| `browser_wait_for` | Wait for conditions | `text?: string, textGone?: string, time?: number` | Wait result | Response loading, state changes |

### OpenAI GUI-Specific Integration Patterns

#### Component Selector Reference

Based on our React application structure, here are the key selectors for MCP tool usage:

```typescript
// Primary Interface Elements
interface OpenAIGUISelectors {
  // Message Input Components
  messageInput: 'textarea[data-testid="message-input"]' | 'textarea[placeholder*="message"]';
  sendButton: '[data-testid="send-button"]' | 'button[type="submit"]';
  
  // Chat Interface Elements
  chatContainer: '[data-testid="chat-container"]' | '.chat-interface';
  messageUser: '.message-user' | '[data-message-type="user"]';
  messageAssistant: '.message-assistant' | '[data-message-type="assistant"]';
  
  // Template Buttons
  templateButtons: '.template-button' | '[data-testid^="template-"]';
  analysisTools: '[data-testid="analysis-tools"]';
  
  // Export Functionality
  exportButton: '[data-testid="export-button"]';
  exportMarkdown: '[data-testid="export-markdown"]';
  
  // Responsive Elements
  mobileMenu: '.mobile-menu' | '[data-testid="mobile-menu"]';
  desktopSidebar: '.desktop-sidebar' | '[data-testid="sidebar"]';
}
```

#### API Integration Points

Our OpenAI GUI integrates with these backend endpoints that can be monitored during MCP testing:

```typescript
// Backend API Endpoints for Monitoring
interface APIEndpoints {
  health: '/health';                    // System health check
  chat: '/api/v1/chat';                // Main chat endpoint
  templates: '/api/templates';          // Template retrieval
  analysisTools: '/api/analysis-tools'; // Analysis tool options
  export: '/api/export';               // Export functionality
}
```

### Comprehensive Test Plan Implementation

#### Test Case 1: Basic Message Send Workflow

**Objective**: Verify basic chat functionality with MCP tools
**Tools Used**: `browser_navigate`, `browser_snapshot`, `browser_type`, `browser_click`, `browser_wait_for`

```json
[
  {
    "tool": "browser_navigate",
    "parameters": {
      "url": "http://localhost:3000"
    },
    "expected": "Navigation success"
  },
  {
    "tool": "browser_snapshot",
    "parameters": {},
    "expected": "Page structure with chat interface visible"
  },
  {
    "tool": "browser_type",
    "parameters": {
      "element": "Message input field",
      "ref": "textarea[data-testid='message-input']",
      "text": "What is the latest Apple stock price?"
    },
    "expected": "Text entered successfully"
  },
  {
    "tool": "browser_click",
    "parameters": {
      "element": "Send button",
      "ref": "[data-testid='send-button']"
    },
    "expected": "Message sent, loading state visible"
  },
  {
    "tool": "browser_wait_for",
    "parameters": {
      "textGone": "AI is responding",
      "time": 30
    },
    "expected": "Response received and displayed"
  },
  {
    "tool": "browser_snapshot",
    "parameters": {},
    "expected": "Chat history with user message and AI response"
  }
]
```

#### Test Case 2: Multi-line Input with Shift+Enter

**Objective**: Test advanced input handling
**Tools Used**: `browser_type`, `browser_press_key`, `browser_evaluate`

```json
[
  {
    "tool": "browser_navigate",
    "parameters": {
      "url": "http://localhost:3000"
    }
  },
  {
    "tool": "browser_type",
    "parameters": {
      "element": "Message input",
      "ref": "textarea[data-testid='message-input']",
      "text": "Analyze these stocks:"
    }
  },
  {
    "tool": "browser_press_key",
    "parameters": {
      "key": "Shift+Enter"
    },
    "expected": "New line created, no message sent"
  },
  {
    "tool": "browser_type",
    "parameters": {
      "element": "Message input",
      "ref": "textarea[data-testid='message-input']",
      "text": "- AAPL\n- MSFT\n- GOOGL"
    }
  },
  {
    "tool": "browser_evaluate",
    "parameters": {
      "function": "(element) => element.value.includes('\\n')",
      "element": "Message input",
      "ref": "textarea[data-testid='message-input']"
    },
    "expected": "Multi-line content verified"
  },
  {
    "tool": "browser_press_key",
    "parameters": {
      "key": "Enter"
    },
    "expected": "Multi-line message sent successfully"
  }
]
```

#### Test Case 3: Template Button Interaction

**Objective**: Test template button functionality
**Tools Used**: `browser_snapshot`, `browser_click`, `browser_network_requests`

```json
[
  {
    "tool": "browser_navigate",
    "parameters": {
      "url": "http://localhost:3000"
    }
  },
  {
    "tool": "browser_snapshot",
    "parameters": {},
    "expected": "Template buttons visible in interface"
  },
  {
    "tool": "browser_click",
    "parameters": {
      "element": "Technical Analysis button",
      "ref": "[data-testid='template-technical']"
    }
  },
  {
    "tool": "browser_network_requests",
    "parameters": {},
    "expected": "API call to /api/templates endpoint"
  },
  {
    "tool": "browser_wait_for",
    "parameters": {
      "text": "📊 Technical Analysis",
      "time": 15
    }
  },
  {
    "tool": "browser_snapshot",
    "parameters": {},
    "expected": "Technical analysis response with financial emojis"
  }
]
```

#### Test Case 4: Responsive Design Validation

**Objective**: Test responsive behavior across viewport sizes
**Tools Used**: `browser_resize`, `browser_evaluate`, `browser_snapshot`

```json
[
  {
    "tool": "browser_navigate",
    "parameters": {
      "url": "http://localhost:3000"
    }
  },
  {
    "tool": "browser_resize",
    "parameters": {
      "width": 375,
      "height": 667
    },
    "expected": "Mobile viewport applied"
  },
  {
    "tool": "browser_evaluate",
    "parameters": {
      "function": "() => window.getComputedStyle(document.querySelector('.message-bubble')).maxWidth"
    },
    "expected": "85% width for mobile"
  },
  {
    "tool": "browser_resize",
    "parameters": {
      "width": 1200,
      "height": 800
    },
    "expected": "Desktop viewport applied"
  },
  {
    "tool": "browser_evaluate",
    "parameters": {
      "function": "() => window.getComputedStyle(document.querySelector('.message-bubble')).maxWidth"
    },
    "expected": "70% width for desktop"
  },
  {
    "tool": "browser_snapshot",
    "parameters": {},
    "expected": "Desktop layout with proper spacing"
  }
]
```

### Real-world Usage Examples

#### Example 1: Complete Financial Query Test

```json
{
  "testName": "Complete Financial Query Workflow",
  "description": "End-to-end test of financial query with emoji validation",
  "steps": [
    {
      "tool": "browser_navigate",
      "parameters": { "url": "http://localhost:3000" },
      "validation": "Page loads successfully"
    },
    {
      "tool": "browser_type",
      "parameters": {
        "element": "Message input",
        "ref": "textarea[placeholder*='message']",
        "text": "What is the current NVIDIA stock price and market sentiment?"
      },
      "validation": "Query entered correctly"
    },
    {
      "tool": "browser_press_key",
      "parameters": { "key": "Enter" },
      "validation": "Message sent"
    },
    {
      "tool": "browser_wait_for",
      "parameters": { "text": "🎯 KEY TAKEAWAYS", "time": 45 },
      "validation": "AI response received with structured format"
    },
    {
      "tool": "browser_evaluate",
      "parameters": {
        "function": "() => document.querySelector('.message-assistant:last-child').textContent.includes('📈') || document.querySelector('.message-assistant:last-child').textContent.includes('📉')"
      },
      "validation": "Financial emoji indicators present"
    },
    {
      "tool": "browser_network_requests",
      "parameters": {},
      "validation": "Backend API calls successful"
    }
  ]
}
```

#### Example 2: Export Functionality Test

```json
{
  "testName": "Export Functionality Validation",
  "description": "Test chat export with download verification",
  "steps": [
    {
      "tool": "browser_navigate",
      "parameters": { "url": "http://localhost:3000" }
    },
    {
      "tool": "browser_type",
      "parameters": {
        "element": "Message input",
        "ref": "textarea",
        "text": "Generate a sample financial report for testing"
      }
    },
    {
      "tool": "browser_press_key",
      "parameters": { "key": "Enter" }
    },
    {
      "tool": "browser_wait_for",
      "parameters": { "textGone": "AI is responding", "time": 30 }
    },
    {
      "tool": "browser_click",
      "parameters": {
        "element": "Export button",
        "ref": "[data-testid='export-button']"
      }
    },
    {
      "tool": "browser_click",
      "parameters": {
        "element": "Export as Markdown",
        "ref": "[data-testid='export-markdown']"
      }
    },
    {
      "tool": "browser_evaluate",
      "parameters": {
        "function": "() => { const downloads = document.querySelectorAll('[download]'); return downloads.length > 0; }"
      },
      "validation": "Download initiated successfully"
    }
  ]
}
```

### Performance and Best Practices

#### Optimal Tool Sequencing

**Pattern 1: Navigation + Snapshot**
```json
[
  {"tool": "browser_navigate", "parameters": {"url": "..."}},
  {"tool": "browser_snapshot", "parameters": {}}
]
```
*Always take a snapshot after navigation to understand page structure*

**Pattern 2: Interaction + Validation**
```json
[
  {"tool": "browser_type", "parameters": {...}},
  {"tool": "browser_evaluate", "parameters": {...}}
]
```
*Validate interactions immediately to catch issues early*

**Pattern 3: Wait + Verify**
```json
[
  {"tool": "browser_wait_for", "parameters": {...}},
  {"tool": "browser_network_requests", "parameters": {}}
]
```
*Check network activity after waiting for async operations*

#### Token Efficiency Strategies

1. **Batch Related Operations**: Group logically related MCP calls
2. **Use Specific Selectors**: Avoid generic selectors that return large DOM trees
3. **Strategic Snapshots**: Take snapshots only when page state significantly changes
4. **Targeted Evaluations**: Use `browser_evaluate` for specific data extraction

#### Error Handling Patterns

```json
{
  "errorHandling": {
    "timeouts": {
      "navigation": 30,
      "interactions": 10,
      "apiResponses": 60
    },
    "retryPatterns": {
      "networkFailure": "Retry navigation up to 3 times",
      "elementNotFound": "Take snapshot and re-evaluate selectors",
      "timeoutExpired": "Check console messages and network requests"
    },
    "fallbackStrategies": {
      "primarySelectorFails": "Use alternative CSS selector or XPath",
      "javascriptDisabled": "Use pure click/type interactions",
      "slowResponse": "Increase timeout and add intermediate checks"
    }
  }
}
```

### Advanced MCP Integration Features

#### Custom JavaScript Evaluation

Use `browser_evaluate` for complex state inspection:

```json
{
  "tool": "browser_evaluate",
  "parameters": {
    "function": "() => { const msgs = document.querySelectorAll('.message-assistant'); const lastMsg = msgs[msgs.length-1]; return { hasEmoji: /📈|📉/.test(lastMsg.textContent), wordCount: lastMsg.textContent.split(' ').length, containsKeyTakeaways: lastMsg.textContent.includes('🎯 KEY TAKEAWAYS') }; }"
  }
}
```

#### Network Request Monitoring

Monitor API calls for integration validation:

```json
{
  "tool": "browser_network_requests",
  "parameters": {},
  "expectedPatterns": [
    {
      "url": "**/api/v1/chat",
      "method": "POST",
      "status": 200,
      "responseTimeMs": "< 5000"
    },
    {
      "url": "**/health",
      "method": "GET",
      "status": 200,
      "responseTimeMs": "< 1000"
    }
  ]
}
```

#### Accessibility Tree Analysis

Leverage structured accessibility data:

```json
{
  "tool": "browser_snapshot",
  "parameters": {},
  "analysis": {
    "checkFor": [
      "aria-labels on interactive elements",
      "proper heading hierarchy",
      "keyboard navigation support",
      "screen reader compatibility"
    ],
    "accessibilityValidation": {
      "forms": "All inputs have associated labels",
      "buttons": "All buttons have descriptive text or aria-label",
      "navigation": "Tab order is logical and complete"
    }
  }
}
```

### Troubleshooting & Common Issues

#### Issue: Element Not Found
**Symptoms**: MCP tools return "element not found" errors
**Solutions**:
1. Take a fresh `browser_snapshot` to see current page state
2. Use alternative selectors (CSS class, data attributes, XPath)
3. Wait for dynamic content with `browser_wait_for`
4. Check for overlapping elements or z-index issues

```json
{
  "troubleshootingSequence": [
    {"tool": "browser_snapshot", "purpose": "Inspect current DOM structure"},
    {"tool": "browser_console_messages", "purpose": "Check for JavaScript errors"},
    {"tool": "browser_evaluate", "parameters": {"function": "() => document.querySelector('your-selector')"}, "purpose": "Verify selector exists"}
  ]
}
```

#### Issue: Slow Response Times
**Symptoms**: Timeouts on `browser_wait_for` operations
**Solutions**:
1. Increase timeout values for AI responses (30-60 seconds)
2. Monitor network requests to identify bottlenecks
3. Check backend health endpoint status
4. Verify API keys and rate limits

```json
{
  "performanceDebugging": [
    {"tool": "browser_network_requests", "purpose": "Identify slow API calls"},
    {"tool": "browser_evaluate", "parameters": {"function": "() => performance.now()"}, "purpose": "Timestamp interactions"},
    {"tool": "browser_console_messages", "purpose": "Check for performance warnings"}
  ]
}
```

#### Issue: Responsive Design Problems
**Symptoms**: Elements not visible or improperly sized
**Solutions**:
1. Use `browser_resize` to test different viewport sizes
2. Evaluate computed styles with `browser_evaluate`
3. Take screenshots at different resolutions
4. Check CSS media query breakpoints

```json
{
  "responsiveDebugging": [
    {"tool": "browser_resize", "parameters": {"width": 375, "height": 667}},
    {"tool": "browser_evaluate", "parameters": {"function": "() => ({ width: window.innerWidth, height: window.innerHeight, devicePixelRatio: window.devicePixelRatio })"}},
    {"tool": "browser_take_screenshot", "parameters": {"fullPage": true}}
  ]
}
```

### Integration with Backend Systems

#### FastAPI Health Check Integration

```json
{
  "backendValidation": {
    "healthCheck": {
      "tool": "browser_evaluate",
      "parameters": {
        "function": "() => fetch('/health').then(r => r.json()).then(data => data.status === 'healthy')"
      }
    },
    "apiEndpointTests": [
      {
        "endpoint": "/api/v1/chat",
        "method": "POST",
        "expectedStatus": 200,
        "timeout": 30000
      },
      {
        "endpoint": "/api/templates",
        "method": "GET",
        "expectedStatus": 200,
        "timeout": 5000
      }
    ]
  }
}
```

#### Environment-Specific Configuration

```json
{
  "environments": {
    "development": {
      "baseUrl": "http://localhost:3000",
      "backendUrl": "http://localhost:8000",
      "timeouts": {
        "navigation": 10,
        "interaction": 5,
        "apiResponse": 30
      }
    },
    "staging": {
      "baseUrl": "https://staging.example.com",
      "backendUrl": "https://api-staging.example.com",
      "timeouts": {
        "navigation": 15,
        "interaction": 10,
        "apiResponse": 45
      }
    },
    "production": {
      "baseUrl": "https://app.example.com",
      "backendUrl": "https://api.example.com",
      "timeouts": {
        "navigation": 20,
        "interaction": 15,
        "apiResponse": 60
      }
    }
  }
}
```

### When to Use MCP vs CLI

#### Use MCP Server When:
- **AI Agent Testing**: AI systems need to interpret test results
- **Structured Data Requirements**: JSON responses are preferred
- **Token Efficiency**: Minimizing token usage for AI interactions
- **Accessibility Focus**: Leveraging structured accessibility snapshots
- **Real-time Analysis**: Need for live DOM and accessibility context
- **Interactive Debugging**: Step-by-step browser interaction with immediate feedback
- **Cross-platform Compatibility**: Testing across different operating systems
- **Dynamic Test Generation**: AI-generated test scenarios based on page analysis

#### Use CLI When:
- **Human Development**: Traditional development workflows
- **CI/CD Integration**: Established pipeline requirements
- **Component Testing**: React component isolation testing
- **Debugging Needs**: Rich debugging tools and IDE integration
- **Team Collaboration**: Universal tool compatibility requirements
- **Performance Testing**: Load testing and parallel execution
- **Regression Testing**: Stable, repeatable test suites
- **Enterprise Integration**: Integration with existing testing infrastructure

### Component vs E2E Testing Decisions

#### Component Testing (Use When):
- Testing isolated component behavior
- Validating props and state management
- Testing React hooks and context
- Rapid development feedback loops
- Unit-level testing requirements

#### E2E Testing (Use When):
- Testing complete user workflows
- Validating backend integration
- Cross-browser compatibility testing
- Performance and accessibility validation
- Production-like environment testing

### Integration with Current Stack

#### React/TypeScript Integration
```typescript
// Optimal configuration for our stack
export default defineConfig({
  use: {
    ctViteConfig: {
      resolve: {
        alias: {
          '@': resolve(__dirname, './src'),
        },
      },
      define: {
        'process.env.NODE_ENV': JSON.stringify('test'),
      },
    },
  },
});
```

#### Vite Integration Best Practices
- Use `ctViteConfig` for component testing configuration
- Leverage Vite's fast HMR for test development
- Configure aliases and environment variables
- Utilize Vite plugins for enhanced functionality

#### FastAPI Backend Testing
```typescript
// Backend health check pattern
test.beforeEach(async ({ page }) => {
  // Ensure backend is running
  await page.request.get('http://localhost:8000/health');
});
```

## Implementation Roadmap

### Phase 1: Foundation Setup (Week 1)

#### Day 1-2: Installation and Basic Configuration
```bash
# Install CLI method (recommended start)
npm install -D @playwright/test
npx playwright install

# Create basic config
npx playwright init
```

**Deliverables:**
- Basic `playwright.config.ts`
- First E2E test
- CI integration setup

#### Day 3-5: Component Testing Setup
```bash
# Install component testing
npm install -D @playwright/experimental-ct-react

# Create component config
touch playwright-ct.config.ts
```

**Deliverables:**
- Component testing configuration
- First component test
- Vite integration

#### Day 6-7: Team Training and Documentation
**Deliverables:**
- Team training session
- Internal documentation updates
- Best practices guide

### Phase 2: Component Testing (Week 2)

#### Core Component Test Suite
- ChatInput_OpenAI component tests
- ChatMessage_OpenAI component tests
- Responsive design tests
- Hook testing implementation

#### Advanced Component Testing
- Context provider testing
- Custom hook validation
- Performance component testing
- Accessibility component validation

### Phase 3: E2E Testing (Week 3)

#### Basic E2E Workflows
- User message sending
- AI response validation
- Export functionality testing
- Error handling validation

#### Advanced E2E Testing
- Cross-browser testing setup
- Performance testing integration
- Visual regression testing
- Full-stack integration tests

### Phase 4: CI/CD Integration (Week 4)

#### GitHub Actions Integration
```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
      with:
        node-version: 18
    - name: Install dependencies
      run: npm ci
    - name: Install Playwright Browsers
      run: npx playwright install --with-deps
    - name: Run Playwright tests
      run: npx playwright test
    - uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: playwright-report/
```

#### Performance Monitoring Integration
- Lighthouse CI integration
- Performance regression detection
- Bundle size impact analysis
- Core Web Vitals monitoring

## Troubleshooting & Common Issues

### Setup Problems and Solutions

#### Issue: Browser Installation Fails
```bash
# Solution: Install with dependencies
npx playwright install --with-deps

# For specific browsers only
npx playwright install chromium firefox
```

#### Issue: TypeScript Configuration Errors
```typescript
// Add to tsconfig.json
{
  "compilerOptions": {
    "types": ["@playwright/test"]
  }
}
```

#### Issue: Component Testing with Vite
```typescript
// Common Vite config issue
export default defineConfig({
  use: {
    ctViteConfig: {
      // Must include full Vite config here
      plugins: [react()],
      resolve: {
        alias: {
          '@': resolve(__dirname, './src'),
        },
      },
    },
  },
});
```

### Performance Optimization

#### Test Execution Speed
```typescript
// Optimize parallel execution
export default defineConfig({
  workers: process.env.CI ? 2 : undefined, // Limit workers in CI
  fullyParallel: true,
  
  // Reduce timeout for faster feedback
  timeout: 10000,
  expect: {
    timeout: 5000,
  },
});
```

#### Memory Usage Optimization
```typescript
// Prevent memory leaks
test.afterEach(async ({ page }) => {
  await page.close();
});

// Limit concurrent tests
export default defineConfig({
  workers: 1, // For memory-constrained environments
});
```

### Debugging Techniques

#### Debug Mode
```bash
# Run single test in debug mode
npx playwright test --debug tests/chat-interface.spec.ts

# Run with headed browser
npx playwright test --headed

# Generate trace
npx playwright test --trace on
```

#### Visual Debugging
```typescript
// Add to test for debugging
test('debug example', async ({ page }) => {
  await page.goto('/');
  
  // Pause execution
  await page.pause();
  
  // Take screenshot
  await page.screenshot({ path: 'debug.png', fullPage: true });
  
  // Get element screenshot
  await page.locator('.chat-container').screenshot({ path: 'element.png' });
});
```

#### Network Debugging
```typescript
test('network debugging', async ({ page }) => {
  // Listen to all network events
  page.on('response', response => {
    console.log(`${response.status()} ${response.url()}`);
  });
  
  // Mock specific endpoints
  await page.route('**/api/chat', route => {
    console.log('API call intercepted:', route.request().postData());
    route.continue();
  });
});
```

### Cross-Browser Compatibility Issues

#### Safari/WebKit Specific Issues
```typescript
// Handle Safari-specific behavior
test('webkit specific test', async ({ page, browserName }) => {
  test.skip(browserName !== 'webkit', 'WebKit specific test');
  
  // WebKit-specific assertions
  await expect(page.locator('.chat-input')).toHaveCSS('appearance', 'none');
});
```

#### Mobile Browser Testing
```typescript
// Mobile-specific testing
test.describe('Mobile Tests', () => {
  test.use({ 
    ...devices['iPhone 12'],
    // Override specific settings
    hasTouch: true,
  });

  test('mobile interaction', async ({ page }) => {
    // Mobile-specific test logic
    await page.tap('.mobile-button');
  });
});
```

## Reference & Advanced Configuration

### Complete Configuration Examples

#### Production-Ready Playwright Config
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // Global test settings
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  projects: [
    // Desktop browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    
    // Mobile browsers
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
    
    // Component testing project
    {
      name: 'components',
      testDir: './src/components/__tests__',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
  ],

  webServer: [
    {
      command: 'npm run dev',
      url: 'http://localhost:3000',
      reuseExistingServer: !process.env.CI,
      timeout: 120000,
    },
    {
      command: 'cd .. && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000',
      url: 'http://localhost:8000/health',
      reuseExistingServer: !process.env.CI,
      timeout: 60000,
    },
  ],
});
```

#### Component Testing Config with Advanced Vite Integration
```typescript
import { defineConfig, devices } from '@playwright/experimental-ct-react';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';

export default defineConfig({
  testDir: './src',
  testMatch: '**/__tests__/**/*.spec.{ts,tsx}',
  fullyParallel: true,
  
  use: {
    trace: 'on-first-retry',
    ctViteConfig: {
      plugins: [react()],
      resolve: {
        alias: {
          '@': resolve(__dirname, './src'),
          '@components': resolve(__dirname, './src/components'),
          '@hooks': resolve(__dirname, './src/hooks'),
          '@utils': resolve(__dirname, './src/utils'),
        },
      },
      define: {
        'process.env.NODE_ENV': JSON.stringify('test'),
        'import.meta.env.VITE_API_BASE_URL': JSON.stringify('http://localhost:8000'),
      },
      server: {
        deps: {
          inline: ['@testing-library/react', '@testing-library/jest-dom'],
        },
      },
    },
  },
  
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

### CI/CD Workflows

#### GitHub Actions Complete Workflow
```yaml
name: Playwright Tests
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  NODE_VERSION: 18

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Install Playwright browsers
      run: npx playwright install --with-deps ${{ matrix.browser }}
      
    - name: Setup Python for backend
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install backend dependencies
      run: |
        pip install uv
        uv install
        
    - name: Run Playwright tests
      run: npx playwright test --project=${{ matrix.browser }}
      env:
        CI: true
        BASE_URL: http://localhost:3000
        
    - name: Upload test reports
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: playwright-report-${{ matrix.browser }}
        path: |
          playwright-report/
          test-results/
        retention-days: 30

  component-tests:
    timeout-minutes: 30
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
        
    - run: npm ci
    - run: npx playwright install chromium
    - run: npx playwright test --config=playwright-ct.config.ts
      
    - uses: actions/upload-artifact@v4
      if: always()
      with:
        name: component-test-report
        path: playwright-report/
```

### Performance Tuning

#### Advanced Performance Configuration
```typescript
export default defineConfig({
  // Optimize for performance
  fullyParallel: true,
  workers: process.env.CI ? 2 : Math.max(1, Math.floor(require('os').cpus().length / 2)),
  
  // Reduce timeouts for faster feedback
  timeout: 30000,
  expect: {
    timeout: 10000,
  },
  
  use: {
    // Optimize browser settings
    launchOptions: {
      args: [
        '--disable-dev-shm-usage',
        '--disable-extensions',
        '--disable-gpu',
        '--no-sandbox',
        '--disable-web-security',
      ],
    },
    
    // Optimize screenshots and videos
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
  },
  
  // Global setup for performance
  globalSetup: require.resolve('./tests/global-setup'),
  globalTeardown: require.resolve('./tests/global-teardown'),
});
```

#### Global Setup and Teardown
```typescript
// tests/global-setup.ts
import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  // Pre-warm browsers
  const browser = await chromium.launch();
  await browser.newContext();
  await browser.close();
  
  // Setup test database or services
  console.log('Global setup completed');
}

export default globalSetup;
```

```typescript
// tests/global-teardown.ts
import { FullConfig } from '@playwright/test';

async function globalTeardown(config: FullConfig) {
  // Cleanup resources
  console.log('Global teardown completed');
}

export default globalTeardown;
```

### Testing Best Practices Summary

#### Test Organization
- Use descriptive test names
- Group related tests with `test.describe`
- Implement proper test isolation
- Use page object patterns for complex interactions

#### Assertion Strategies
- Use `expect(locator).toBeVisible()` instead of `expect(await locator.isVisible()).toBe(true)`
- Implement auto-waiting with proper expectations
- Use soft assertions for non-critical validations
- Implement custom matchers for domain-specific assertions

#### Data Management
- Use fixtures for test data
- Implement proper test cleanup
- Mock external dependencies
- Use environment-specific configurations

#### Debugging and Maintenance
- Enable trace collection for CI failures
- Implement proper error handling
- Use descriptive selectors and data-testid attributes
- Maintain test documentation and comments

---

## Conclusion

This guide provides a comprehensive foundation for implementing Playwright testing in our React/TypeScript/Vite/FastAPI stack. Choose the approach that best fits your team's needs and technical requirements, and follow the phased implementation roadmap for successful integration.

For additional support or questions, refer to the [official Playwright documentation](https://playwright.dev/) or consult with the development team.