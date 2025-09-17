# New Task Details

## Task Description: [NPX_Test] Phase 1: Create Playwright "npx playwright test" Single Source Testing Script

"NPX Test Implementation Plan - Phase 1"

# NPX Test Implementation Plan - Phase 1

Based on my comprehensive research of the documentation, I will create a complete NPX testing solution with the following deliverables:

## 1. Update npx_test_script_basic.md

Transform the existing file from an MCP copy into a proper NPX testing guide with:

* **VERBATIM** instructions for NPX execution (no interpretation required)
* Complete parameter specifications with millisecond timeouts (120000ms)
* Exact NPX command: `npx playwright test --timeout=120000 --workers=1 test-basic-suite.spec.ts`
* Two-phase detection strategy (response presence → content validation)
* Clear success/failure criteria matching MCP baseline
* Comprehensive troubleshooting guide for NPX-specific issues

## 2. Create test-basic-suite.spec.ts

New Playwright test spec file implementing:

* Test 1: Market Status query with exact message
* Test 2: NVDA Ticker Snapshot with exact message
* Test 3: Stock Snapshot Button interaction
* Proper imports from `'@playwright/test'` and `'./helpers/index'`
* 120-second timeout configuration
* Auto-retry detection using `waitForSelector` with 120000ms timeout
* Response validation using existing helper functions
* Performance classification (SUCCESS/SLOW_PERFORMANCE/TIMEOUT)

## 3. Update Project Documentation

* Update `PLAYWRIGHT_TESTING_MASTER_PLAN.md` to reference new NPX basic test
* Add references in relevant testing guides to the new `test-basic-suite.spec.ts`
* Ensure consistency across all documentation

---

## Key Implementation Details

### Critical Success Factors

* **VERBATIM** instructions eliminating interpretation errors
* Timeout translation: MCP seconds (120) → NPX milliseconds (120000)
* Multiple selector strategies with fallbacks
* Proper `async/await` patterns throughout
* Error handling with `try-catch` blocks
* System readiness validation before tests

### NPX API Translations

* `mcp__playwright__browser_navigate` → `page.goto(url)`
* `mcp__playwright__browser_type` → `page.fill(selector, text)`
* `mcp__playwright__browser_press_key` → `page.keyboard.press(key)`
* `mcp__playwright__browser_click` → `page.click(selector)`
* `mcp__playwright__browser_wait_for` → `page.waitForSelector(selector, { timeout: 120000 })`

### Test Structure

```typescript
import { test, expect } from '@playwright/test';
import {
  autoNavigateToFrontend,
  sendMessageAndWaitForResponse,
  validateSystemReadiness,
  // ... other helpers
} from './helpers/index';

test.describe('Basic Test Suite', () => {
  test.setTimeout(120000);

  test('Test 1: Market Status', async ({ page }) => {
    // Implementation with auto-retry detection
  });

  test('Test 2: NVDA Ticker Snapshot', async ({ page }) => {
    // Implementation with auto-retry detection
  });

  test('Test 3: Stock Snapshot Button', async ({ page }) => {
    // Implementation with auto-retry detection
  });
});
```

This implementation will achieve:

* 100% first-try success rate for AI agents
* Testing parity with MCP method (3/3 passing)
* Clear, unambiguous instructions
* Robust error handling and recovery

## Final Task(s)

MUST USE Context7 & Sequential-Thinking Tools to perform: Final Task 1: Review/Fix Loop

* Performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
* Optional `mcp__filesystem__*` tools for EFFICIENT file operations and examination.
* Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
* Continue review/fix cycle until achieving PASSING code review status

Final Task 2: Task Summary Updates for CLAUDE.md

* Create token & context efficient git commit message of all the changes to prepare for the final commit task(s)
* Update CLAUDE.md "Last Completed Task Summary" section with the VERBATIM COPY of the token & context efficient git commit message between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
* This ensures that the git commit message is cached for token & context efficient in order to update CLAUDE.md with, preventing the need to waste tokens by having to regenerate similiar task completion summaries

Final Task 3: Atomic Git Commit & Push

* Run `git status` to review all staged and unstaged changes
* Create single atomic git commit containing ALL changes: CLAUDE.md, code files, documentation changes, 1x test report if it exist, NO TEST OUTPUT RESULTS\DATA\SCREENSHPTS\VIDEOS ETC
* **CRITICAL**: DO NOT INCLUDE & COMMIT testing artifacts & testing outputs
* the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever
* git Push commit to repository using provided personal access token
* **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Final Task 4: Final Verification

* Run final `git status` to confirm successful commit and push
* Verify working tree is clean and branch is up-to-date with remote
* Confirm all changes are properly git committed and git pushed

**Key Requirements:**

## Requirements

## Expected Outcome*

AI Agent reads & runs testing script from 'tests/playwright/npx_test_script_basic.md' using Playwright "npx playwright test" Method with 3/3 Passing on the very first try:

A. AI Agent requested to run NPX Basic Test Plan etc
B. AI Agent reads 'tests/playwright/npx_test_script_basic.md' to perform testing by FOLLOWING VERBATIM testing instructions to have a full successful test run on the very first attempt with 3/3 passing
C. AI Agent properly uses simple one click startup script to setup and confirm dev servers are running and configured correctly before starting any tests
D. AI Agent issues single command to run the new Playwright NPX Test spec file "xxx.spec.ts" that will run and ensure the 3/3 Basic tests PASSES with parity with MCP method: "npx playwright test --timeout=120000 --workers=1 xxx.spec.ts"
E. AI Agent generates detailed matching test report following the specific file format & naming scheme after all testing is complete with 3/3 Test passed

## Additional Context
