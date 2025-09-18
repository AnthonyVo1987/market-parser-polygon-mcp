# New Task Details

## Task Description: Complete Removal of Playwright CLI/NPX Testing & Dependencies

# Plan: Complete Removal of Playwright CLI/NPX Testing & Dependencies

## Summary

Complete removal of ALL Playwright CLI "npx playwright test" methods, dependencies, and packages while preserving Playwright MCP/Tools method as the single testing approach.

## Phase 1: Delete NPX-Only Files & Directories

### Files to Delete Completely

1. `/tests/playwright/npx_test_script_basic.md` - NPX-specific documentation
2. `/tests/playwright/test-basic-suite.spec.ts` - NPX test implementation
3. `/playwright.config.ts` - NPX Playwright configuration
4. `/tests/playwright/playwright_CLI_test_25-09-12_13-42.md` - NPX test report
5. All `/tests/playwright/test-b*.spec.ts` files (16 files) - NPX test specs
6. `/tests/playwright/integration-test.spec.ts` - NPX integration test
7. `/tests/playwright/ui-investigation.spec.ts` - NPX investigation test
8. `/tests/playwright/example.test.ts` - NPX example test

### Directories to Delete

1. `/tests/e2e/` - Entire duplicate test directory with NPX tests
2. `/tests/playwright/helpers/` - NPX helper functions (contains `@playwright` imports)
3. `/tests/playwright/test-results/` - NPX test artifacts and videos
4. `/playwright-report/` - NPX test reports (if exists)
5. `/node_modules/@playwright/` - Playwright NPM packages
6. `/node_modules/playwright/` - Playwright core packages
7. `/node_modules/playwright-core/` - Playwright core packages

### Documentation to Delete

1. `/docs/testing/` entire directory - All NPX-focused testing docs
2. `/docs/PLAYWRIGHT_SLASH_COMMANDS_BEST_PRACTICES.md` - Mixed NPX/MCP content

## Phase 2: Remove Playwright Dependencies

### 1. package.json

* Remove `@playwright/test` from `devDependencies` (line 113)
* Remove ALL test scripts (lines 50-71): All `test:*` scripts using `npx playwright`
* Keep all other scripts unchanged

### 2. package-lock.json

* Will be regenerated after `npm install`
* Currently contains `playwright`, `playwright-core`, `@playwright/test` entries

### 3. Uninstall Commands to Run

```bash
npm uninstall @playwright/test
npm prune  # Remove orphaned dependencies
rm -rf node_modules/@playwright node_modules/playwright*
```

## Phase 3: Update Mixed-Reference Files

### 1. CLAUDE.md

* Remove "Testing" section with NPX commands (lines 147-162)
* Update "Testing Strategy" section to reference only MCP tools method
* Update to state MCP Tools is the **ONLY** testing method

### 2. README.md

* Remove "Testing" commands section (lines 175-191)
* Replace with reference to MCP testing: `/tests/playwright/mcp_test_script_basic.md`
* Update to state testing is done via Playwright MCP tools only

### 3. .claude/commands/resync.md

* Update testing protocol section to reference only MCP method
* Remove all NPX testing references

### 4. GEMINI.md (if contains testing references)

* Update to reference only MCP testing method

### 5. .claude/templates/ files

* Remove any NPX test references from template files

## Phase 4: Update MCP Documentation

### 1. /docs/MCP_Tools_Usage_Guide/Playwright_MCP_Tools_Usage_Guide.md

* **CRITICAL**: Replace ALL "30-second polling" references with auto-retry logic
* Update ALL examples to use `start-app.sh` for server startup
* Remove outdated polling examples (lines 41-694 contain polling references)
* Add modern auto-retry detection pattern examples
* Ensure **NO** references to NPX commands remain

### 2. /tests/playwright/PLAYWRIGHT_TESTING_MASTER_PLAN.md

* Update to reflect MCP as **SINGLE** testing method
* Remove **ANY** dual-method comparisons
* Remove **ANY** NPX method references
* Ensure all examples use MCP tools exclusively

### 3. /tests/playwright/mcp_test_script_basic.md

* Verify as single source of truth for testing
* Ensure proper server startup with `start-app.sh`
* Confirm auto-retry logic documentation
* Remove any comparisons to NPX method

### 4. /tests/playwright/playwright_post-mortem_mcp_tools_testing_guide.md

* Update to remove any NPX references
* Focus only on MCP tools testing

## Phase 5: Clean Python Environment (No Changes Needed)

### pyproject.toml

* No Playwright dependencies found (Python project uses different testing)
* No changes required

## Final Task(s) to be performed only after all previous task(s) are completed

## Phase 6: Final Tasks

### 1. Comprehensive Review

* Use `sequential-thinking` MCP for systematic validation
* Use `context7` MCP for best practices research
* Verify **ALL** NPX references removed
* Verify **ALL** `@playwright/test` imports removed
* Ensure MCP documentation is complete

### 2. Update CLAUDE.md Task Summary

* Create concise git commit message
* Update "Last Completed Task Summary" section with:
    `refactor: Remove Playwright CLI/NPX testing in favor of MCP Tools method`
* Delete all NPX test files, configs, and dependencies
* Remove `@playwright/test` package and all related `node_modules`
* Update docs to use MCP Tools as single testing approach
* Replace 30s polling with auto-retry in MCP docs
* Clean `package.json` of all `npx playwright` scripts

### 3. Git Commit & Push

* Stage all changes (deletions and updates)
* Create atomic commit
* Push to repository

### 4. Final Verification

* Run `npm list @playwright/test` to confirm removal
* Run `git status` for clean working tree
* Verify successful push

## Expected Outcome

* Zero NPX/CLI Playwright references
* No `@playwright/test` package installed
* MCP Tools method as **ONLY** testing approach
* Updated docs with auto-retry (no polling)
* Clean `node_modules` without Playwright packages
* Reduced package size and dependencies

**Key Requirements:**

## Requirements

## Expected Outcome*

* All code, files, test scripts, and all documentation completely removed of any references and\or usage of Playwright CLI npx test method
* Playwright MCP\Tools Method left alone

## Additional Context

* We already have a robust and working Playwright MCP\Tools method so we don’t need the secondary backup CLI npx test method. We wanted to have two methods just in case one wasn’t working, but it’s requiring too much time energy effort to debug & get both methods working so we’ll just use the MCP\Tools method to test only
* Read for more context: tests/playwright/PLAYWRIGHT_TESTING_MASTER_PLAN.md
* Read for more context: tests/playwright/mcp_test_script_basic.md
* Read for more context: docs/MCP_Tools_Usage_Guide/Playwright_MCP_Tools_Usage_Guide.md
