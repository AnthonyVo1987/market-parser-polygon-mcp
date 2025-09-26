# Task Completion Workflow - Market Parser Project

## Pre-Commit Checklist

### 1. Code Quality Checks

```bash
# Run all quality checks
npm run check:all

# This includes:
# - Linting (Python + TypeScript)
# - Formatting (Prettier)
# - Type checking (TypeScript)
```

### 2. Fix Code Quality Issues

```bash
# Auto-fix linting issues
npm run lint:fix

# This runs:
# - Python: black + isort
# - TypeScript: ESLint --fix
```

### 3. Manual Quality Verification

```bash
# Check Python code quality
uv run pylint src/backend/ tests/

# Check TypeScript code quality
npm run lint:js

# Verify formatting
npm run format:check

# Type checking
npm run type-check
```

## Testing Workflow

### 1. Standardized Test Prompts

**CRITICAL**: Always use the standardized test prompts for consistent testing:

```bash
# Test prompts (copy exactly as written):
1. "Quick Response Needed with minimal tool calls: What is the current Market Status?"
2. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Single Stock Snapshot NVDA"
3. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Full Market Snapshot: SPY, QQQ, IWM"
4. "Quick Response Needed with minimal tool calls: Based on Market Status Date, what was the closing price of GME today?"
5. "Quick Response Needed with minimal tool calls: Based on Market Status Date, how is SOUN performance doing this week?"
6. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Top Market Movers Today for Gainers"
7. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Top Market Movers Today for Losers"
8. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Support & Resistance Levels NVDA"
9. "Quick Response Needed with minimal tool calls: Based on Market Status Date, Technical Analysis SPY"
```

### 2. Performance Testing

```bash
# Test all environments
npm run test:perf:all

# Individual environment tests
npm run test:perf:dev      # Development
npm run test:perf:staging  # Staging
npm run test:perf:prod     # Production
```

### 3. Lighthouse Testing

```bash
# Run Lighthouse CI
npm run lighthouse

# With live server
npm run lighthouse:live-server
```

### 4. PWA Testing

```bash
# Test PWA functionality
npm run test:pwa

# Test on different environments
npm run test:pwa:staging
npm run test:pwa:production
```

## Build Verification

### 1. Build All Environments

```bash
# Production build
npm run build

# Staging build
npm run build:staging

# Development build
npm run build:development
```

### 2. Verify Build Output

```bash
# Check build artifacts
ls -la dist/

# Verify bundle size
npm run analyze

# Check for build errors
npm run build 2>&1 | grep -i error
```

## Application Testing

### 1. Start Application

```bash
# One-click startup
./start-app.sh

# Verify servers are running
npm run status
```

### 2. Health Checks

```bash
# Backend health check
curl http://127.0.0.1:8000/health

# Frontend health check
curl http://127.0.0.1:3000

# API endpoints test
curl http://127.0.0.1:8000/api/models
```

### 3. Functional Testing

```bash
# Test with standardized prompts
# Use the 9 standardized test prompts listed above
# Expected response time: 30-60 seconds
# Verify response format and content
```

## Performance Verification

### 1. Core Web Vitals

- **First Contentful Paint (FCP)**: Target < 256ms
- **Largest Contentful Paint (LCP)**: Target < 500ms
- **Cumulative Layout Shift (CLS)**: Target < 0.1
- **Time to Interactive (TTI)**: Target < 1s

### 2. Performance Monitoring

```bash
# React performance scan
npm run perf:scan

# Bundle analysis
npm run perf:bundle

# Memory usage check
# Target: 13.8MB heap size
```

### 3. AI Performance

- **Response time**: 20-40% improvement with quick response optimization
- **Rate limiting**: No errors with proper model configuration
- **Token usage**: Monitor with OpenAI metadata
- **Model selection**: GPT-5 Nano (200K TPM) vs Mini (500K TPM)

## Code Review Checklist

### 1. Python Code Review

- [ ] Type hints used where appropriate
- [ ] Error handling implemented
- [ ] Pydantic models for API validation
- [ ] Async/await patterns used correctly
- [ ] Logging implemented with context
- [ ] No hardcoded values (use config)
- [ ] Functions are focused and single-purpose

### 2. TypeScript Code Review

- [ ] TypeScript types defined
- [ ] React hooks used correctly
- [ ] Error boundaries implemented
- [ ] Loading states handled
- [ ] Accessibility considerations
- [ ] Performance optimizations (memo, useMemo, useCallback)
- [ ] Clean component structure

### 3. API Review

- [ ] Request/response models defined
- [ ] Error responses standardized
- [ ] Rate limiting implemented
- [ ] CORS configuration correct
- [ ] Input validation present
- [ ] Response caching appropriate

## Deployment Checklist

### 1. Pre-Deployment

- [ ] All tests passing
- [ ] Code quality checks passing
- [ ] Performance tests passing
- [ ] Build successful
- [ ] Environment variables configured
- [ ] API keys valid and accessible

### 2. Deployment Steps

```bash
# 1. Build production version
npm run build

# 2. Test production build
npm run serve:production

# 3. Run Lighthouse tests
npm run lighthouse:live-server

# 4. Verify all functionality
# Use standardized test prompts
```

### 3. Post-Deployment

- [ ] Health checks passing
- [ ] API endpoints responding
- [ ] Frontend loading correctly
- [ ] PWA functionality working
- [ ] Performance metrics acceptable
- [ ] Error monitoring active

## Error Handling Verification

### 1. Backend Error Handling

- [ ] API errors return proper HTTP status codes
- [ ] Error messages are user-friendly
- [ ] Sensitive information not exposed
- [ ] Logging captures error context
- [ ] Graceful degradation implemented

### 2. Frontend Error Handling

- [ ] Error boundaries catch React errors
- [ ] Loading states shown during API calls
- [ ] Error messages displayed to users
- [ ] Retry mechanisms implemented
- [ ] Offline handling (PWA)

### 3. AI Error Handling

- [ ] Rate limiting errors handled
- [ ] Model selection fallback
- [ ] Timeout handling
- [ ] Invalid input validation
- [ ] Response parsing errors

## Documentation Updates

### 1. Code Documentation

- [ ] README.md updated if needed
- [ ] API documentation current
- [ ] Configuration changes documented
- [ ] New features documented
- [ ] Troubleshooting guide updated

### 2. Testing Documentation

- [ ] Test prompts documented
- [ ] Performance benchmarks updated
- [ ] Known issues documented
- [ ] Workarounds documented

## Final Verification

### 1. Complete System Test

```bash
# 1. Start application
./start-app.sh

# 2. Wait for servers to be ready
sleep 10

# 3. Run health checks
npm run status

# 4. Test with standardized prompts
# Use all 9 standardized test prompts

# 5. Verify performance
npm run perf:all

# 6. Check for errors
# Monitor console for any errors
```

### 2. Success Criteria

- [ ] All standardized test prompts respond within 30-60 seconds
- [ ] No linting errors or warnings
- [ ] All builds successful
- [ ] Performance metrics meet targets
- [ ] No runtime errors
- [ ] PWA functionality working
- [ ] Cross-browser compatibility verified

## Troubleshooting Common Issues

### 1. Build Failures

```bash
# Clean and rebuild
npm run clean:full

# Check for dependency issues
npm audit

# Verify Node.js version
node --version  # Should be >= 18.0.0
```

### 2. Runtime Errors

```bash
# Check server logs
# Backend: Check terminal running uvicorn
# Frontend: Check browser console

# Verify environment variables
cat .env | grep API_KEY

# Check port availability
netstat -tlnp | grep -E ":(8000|3000)"
```

### 3. Performance Issues

```bash
# Check bundle size
npm run analyze

# Monitor memory usage
npm run perf:scan

# Run Lighthouse analysis
npm run lighthouse
```

## Commit and Push

### 1. Git Workflow

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "feat: add new feature description"

# Push to remote
git push origin branch-name
```

### 2. Commit Message Format

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes
- **refactor**: Code refactoring
- **test**: Test additions/changes
- **perf**: Performance improvements
- **chore**: Maintenance tasks

### 3. Branch Management

- **main**: Production-ready code
- **develop**: Development branch
- **feature/**: Feature branches
- **hotfix/**: Emergency fixes
- **cli_gui_optimizations**: Current optimization branch
