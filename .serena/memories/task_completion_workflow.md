# Task Completion Workflow

## When a Task is Completed

### 1. Code Quality Checks (Required)
```bash
npm run lint                 # Check all code quality issues
npm run format:check         # Verify code formatting
npm run type-check          # TypeScript type validation
```

### 2. Auto-fix Issues (If Needed)
```bash
npm run lint:fix            # Auto-fix Python and JS/TS issues
npm run format              # Format JS/TS code
```

### 3. Testing (MCP Playwright Only)
- **Location**: `/tests/playwright/mcp_test_script_basic.md`
- **Method**: Playwright MCP Tools for browser automation
- **Coverage**: 3 core validations (Market Status, NVDA Ticker, Stock Snapshot Button)
- **No unit tests**: Manual testing acceptable for prototyping stage

### 4. Application Verification
```bash
npm run status              # Verify both servers are healthy
# Test one-click startup
./start-app.sh              # Should open browser automatically
```

### 5. Git Workflow
```bash
git add .                   # Stage changes
git commit -m "feat: description"  # Conventional commit
# Include Claude co-authorship in commit body
```

### 6. Documentation Updates (If Required)
- **Only if explicitly requested**: Don't proactively create docs
- **Prefer editing existing files**: Over creating new ones
- **Update CLAUDE.md**: If architectural changes made

## Performance Considerations
- **LOG_MODE=NONE**: Ensure logging is disabled for performance
- **Console interception**: Should be removed/disabled
- **API endpoint calls**: Minimize unnecessary backend calls

## Prototyping Stage Reminders
- **Don't over-engineer**: Focus on functional prototypes
- **Prioritize functionality**: Over optimization
- **Simple implementations**: Avoid complex architectural patterns