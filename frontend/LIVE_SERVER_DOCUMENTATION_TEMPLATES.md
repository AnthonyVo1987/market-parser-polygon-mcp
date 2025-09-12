# Live Server Documentation Update Templates

**Comprehensive templates for standardizing Live Server information across all project documentation files**

**Date**: 2025-09-06  
**Purpose**: Standardize Live Server integration documentation across 20+ project files  
**Target**: All Markdown documentation files requiring Live Server information

---

## Table of Contents

1. [Template Overview](#template-overview)
2. [Category 1: Migration/Workflow Documentation Templates](#category-1-migrationworkflow-documentation-templates)
3. [Category 2: Frontend/Technical Documentation Templates](#category-2-frontendtechnical-documentation-templates)
4. [Category 3: API/Integration Documentation Templates](#category-3-apiintegration-documentation-templates)
5. [Category 4: General Project Documentation Templates](#category-4-general-project-documentation-templates)
6. [Category 5: User Guide Documentation Templates](#category-5-user-guide-documentation-templates)
7. [Consistent Terminology Guide](#consistent-terminology-guide)
8. [Content Sections Matrix](#content-sections-matrix)
9. [Implementation Guidelines](#implementation-guidelines)

---

## Template Overview

### Key Live Server Information Patterns

Based on the comprehensive `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md` guide, the following information patterns must be standardized across all documentation:

**Core Information Elements:**
- **Port Configuration**: 5500 (development), 5501 (staging), 5502 (production)
- **Usage Context**: When to use Live Server vs Vite development server
- **Commands**: `npm run serve`, `npm run serve:staging`, `npm run serve:production`
- **PWA Testing Procedures**: Service worker, offline functionality, installation testing
- **Cross-Device Testing**: Mobile and tablet testing on same Wi-Fi network
- **Configuration Management**: .vscode settings and environment-specific configurations
- **Troubleshooting Guidelines**: Common issues and solutions

**Template Principles:**
1. **Consistent Terminology**: Use exact same terms across all documents
2. **Appropriate Detail Level**: Match information depth to document purpose and audience
3. **Cross-References**: Link to comprehensive LIVE_SERVER_USAGE.md for details
4. **Integration**: Blend Live Server info naturally with existing content
5. **Completeness**: Ensure no critical Live Server information is missing

---

## Category 1: Migration/Workflow Documentation Templates

### Template 1A: Migration Guide Live Server Section

**Target Files:**
- `/gpt5-openai-agents-sdk-polygon-mcp/OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md`
- `/docs/enhanced-openai-gpt5-migration-plan.md`

**Template Content:**

```markdown
## Live Server Integration for Production Testing

### Overview

The VS Code Live Server integration provides comprehensive testing capabilities for production builds, PWA functionality, and cross-device validation. Unlike the Vite development server, Live Server serves the actual built application files, making it essential for:

- **Production Build Testing**: Validating actual built application performance
- **PWA Functionality Testing**: Service worker, offline mode, and installation prompts
- **Cross-Device Validation**: Mobile and tablet testing on real devices
- **Performance Testing**: Lighthouse CI and production-like environment simulation

### Environment-Specific Testing Configurations

**Development Environment (Port 5500):**
```bash
npm run serve
# Serves development build with basic PWA functionality
# Access: http://localhost:5500
```

**Staging Environment (Port 5501):**
```bash
npm run serve:staging
# Copy .vscode/live-server-staging.json settings when prompted
# Access: http://localhost:5501
```

**Production Environment (Port 5502):**
```bash
npm run serve:production
# Copy .vscode/live-server-production.json settings when prompted
# Access: http://localhost:5502
```

### Migration Integration Steps

1. **Install VS Code Live Server Extension**:
   - Extension: "Live Server" by Ritwick Dey
   - Required for all production testing workflows

2. **Build and Serve Workflow**:
   ```bash
   # Build for target environment
   npm run serve:production  # or serve:staging/serve
   
   # Start Live Server from VS Code
   # Command Palette → "Live Server: Open with Live Server"
   ```

3. **Cross-Device Testing Setup**:
   ```bash
   npm run cross-device:setup
   # Access from mobile: http://YOUR_LOCAL_IP:5502
   ```

### PWA Testing in Migration Context

Critical for validating Progressive Web App features post-migration:

```bash
npm run test:pwa:production
# Validates:
# - Service Worker registration and caching
# - Offline functionality
# - PWA installation prompts
# - Production-optimized performance
```

**PWA Validation Checklist:**
- [ ] Service worker registers successfully
- [ ] Static assets cached properly
- [ ] Application works offline
- [ ] Install prompt appears on supported browsers
- [ ] PWA manifest loads correctly

### Troubleshooting Migration Issues

**Common Live Server Migration Issues:**

1. **Port Conflicts During Migration**:
   ```bash
   # Kill processes using required ports
   lsof -ti:5500 | xargs kill -9  # Development
   lsof -ti:5501 | xargs kill -9  # Staging
   lsof -ti:5502 | xargs kill -9  # Production
   ```

2. **Configuration File Migration**:
   ```bash
   # Ensure Live Server configuration files are included
   cp .vscode/live-server-*.json ./migrated-project/.vscode/
   ```

3. **Mobile Testing Network Setup**:
   - Verify both devices on same Wi-Fi network
   - Check firewall settings for ports 5500-5502
   - Use local IP address for mobile access

### Integration with Migration Workflows

**For GitHub MCP Migration Method:**
- Include Live Server configuration files in bulk upload
- Add Live Server testing steps to automated validation

**For Traditional Git Migration:**
- Commit Live Server configurations with initial setup
- Document Live Server testing in migration validation

**For Local Manual Installation:**
- Copy Live Server configurations to local workspace
- Set up Live Server testing for local validation

> **📖 Complete Reference**: See `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md` for comprehensive Live Server documentation, troubleshooting, and advanced configuration options.
```

### Template 1B: Development Workflow Live Server Section

**Target Files:**
- `/DEVELOPMENT_WORKFLOW.md`

**Template Content:**

```markdown
## Live Server Integration in Development Workflow

### When to Use Live Server vs Vite

**Use Vite Development Server (`npm run dev`) When:**
- Active development with hot module replacement
- Rapid iteration on UI changes and components
- Debugging with source maps and development tools
- Initial feature development and component building

**Use Live Server When:**
- Testing production builds locally
- Validating PWA functionality (service worker, offline mode)
- Cross-device testing on mobile and tablets
- Performance testing with Lighthouse CI
- Pre-deployment validation and QA testing

### Live Server Commands in Development Workflow

**Build and Test Commands:**
```bash
# Development build testing
npm run serve
# Builds development version and provides Live Server instructions

# Staging environment testing  
npm run serve:staging
# Builds staging version with staging environment variables

# Production build validation
npm run serve:production
# Builds production version with full optimization
```

**PWA Testing Integration:**
```bash
# PWA functionality testing
npm run test:pwa                # Development PWA testing
npm run test:pwa:staging        # Staging PWA testing
npm run test:pwa:production     # Production PWA testing
```

**Cross-Device Testing Setup:**
```bash
# Prepare for mobile/tablet testing
npm run cross-device:setup     # Production cross-device setup
npm run cross-device:staging   # Staging cross-device setup
```

### Integration with Code Quality Workflow

**Pre-commit Live Server Validation:**
```bash
# Add to quality check workflow
npm run quality-check          # Standard quality checks
npm run serve:production       # Build production version
# Manual: Start Live Server and verify functionality
npm run lighthouse             # Performance validation
```

**Branch Testing Strategy:**
- **Feature Branches**: Use Vite dev server for development
- **Develop Branch**: Use Live Server for integration testing
- **Release Branches**: Mandatory Live Server testing across all environments
- **Main Branch**: Full Live Server validation including cross-device testing

### Live Server Configuration Management

**VS Code Settings Integration:**
```json
{
  "liveServer.settings.port": 5500,
  "liveServer.settings.useLocalIp": true,
  "liveServer.settings.cors": true,
  "liveServer.settings.ignoreFiles": [
    ".vscode/**",
    "**/node_modules/**", 
    "**/src/**"
  ]
}
```

**Environment-Specific Configurations:**
- Development: `.vscode/settings.json` (port 5500)
- Staging: `.vscode/live-server-staging.json` (port 5501)
- Production: `.vscode/live-server-production.json` (port 5502)

### Troubleshooting in Development Context

**Common Development Issues:**

1. **Live Server Extension Not Working**:
   ```bash
   # Reload VS Code window
   Ctrl+Shift+P → "Developer: Reload Window"
   ```

2. **Port Conflicts with Development Servers**:
   ```bash
   # Check running processes
   lsof -ti:5500,5501,5502,3000,8000 | xargs kill -9
   ```

3. **CORS Issues in Cross-Device Testing**:
   - Ensure `"liveServer.settings.cors": true` in VS Code settings
   - Verify mobile device on same network as development machine

> **📖 Comprehensive Guide**: For detailed Live Server setup, configuration, and troubleshooting, see `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md`.
```

---

## Category 2: Frontend/Technical Documentation Templates

### Template 2A: Frontend Technical Documentation Live Server Section

**Target Files:**
- `/gpt5-openai-agents-sdk-polygon-mcp/OpenAI_Vite_Optimization_Plan.md`
- `/gpt5-openai-agents-sdk-polygon-mcp/BUTTON_PROMPTS_ARCHITECTURE.md`

**Template Content:**

```markdown
## Live Server Integration for Frontend Testing

### Production Build Validation

Live Server provides essential capabilities for validating frontend optimizations and architecture in production-like environments:

**Key Testing Capabilities:**
- **Actual Build Testing**: Test the real built application, not development server
- **PWA Optimization Validation**: Service worker functionality and caching strategies
- **Performance Testing**: Lighthouse CI integration for optimization validation
- **Cross-Platform Testing**: Mobile and tablet responsive design validation

### Environment-Specific Frontend Testing

**Development Build Testing (Port 5500):**
```bash
npm run serve
# Tests development build with:
# - Basic bundling and optimization
# - Development PWA features
# - Local API proxy configuration
```

**Staging Build Testing (Port 5501):**
```bash
npm run serve:staging
# Tests staging build with:
# - Production-like optimization
# - Staging environment variables
# - Staging API endpoints
```

**Production Build Testing (Port 5502):**
```bash
npm run serve:production
# Tests production build with:
# - Full optimization and minification
# - Production environment variables
# - Production API endpoints
```

### PWA Architecture Testing

**Service Worker Validation:**
```bash
npm run test:pwa:production
# Validates:
# - Service worker registration and activation
# - Cache-first strategy implementation
# - Background sync functionality
# - Update notification system
```

**PWA Feature Testing Checklist:**
- [ ] Service worker registers and activates
- [ ] Static assets cached with proper strategies
- [ ] API responses cached appropriately
- [ ] Offline functionality works as expected
- [ ] Update prompts appear for new versions
- [ ] PWA installation prompts function correctly

### Performance Optimization Validation

**Lighthouse CI Integration:**
```bash
npm run lighthouse:live-server
# Runs comprehensive performance testing:
# - Performance metrics validation
# - PWA score verification
# - Accessibility compliance testing
# - Best practices evaluation
```

**Performance Testing Workflow:**
1. Build production version: `npm run serve:production`
2. Start Live Server on port 5502
3. Run Lighthouse CI: `npm run lighthouse:live-server`
4. Analyze results and optimize accordingly

### Cross-Device Frontend Testing

**Mobile Responsive Design Testing:**
```bash
npm run cross-device:setup
# Prepares production build for mobile testing
# Access from mobile: http://YOUR_LOCAL_IP:5502
```

**Mobile Testing Checklist:**
- [ ] Responsive breakpoints function correctly
- [ ] Touch interactions work properly
- [ ] PWA installation works on mobile browsers
- [ ] Performance acceptable on mobile networks
- [ ] Cross-browser compatibility verified

### Frontend Architecture Integration

**Component Architecture Testing:**
- Use Live Server to test actual component rendering in production builds
- Validate code splitting and lazy loading with real build artifacts
- Test dynamic imports and component loading strategies

**API Integration Testing:**
- Validate API proxy configuration in production-like environment
- Test error handling and fallback mechanisms
- Verify CORS configuration for cross-origin requests

### Troubleshooting Frontend Issues

**Common Frontend Testing Issues:**

1. **Component Not Loading in Production Build**:
   ```bash
   # Check browser console for module loading errors
   # Verify component imports and exports
   # Test with development build first: npm run serve
   ```

2. **API Calls Failing in Live Server**:
   ```bash
   # Verify proxy configuration in .vscode/settings.json
   # Check backend server is running on expected port
   # Validate CORS settings
   ```

3. **PWA Features Not Working**:
   ```bash
   # Clear browser cache and service workers
   # Check service worker registration in DevTools
   # Verify manifest.json loads correctly
   ```

> **📖 Detailed Reference**: See `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md` for complete Live Server configuration, troubleshooting, and advanced features.
```

### Template 2B: API Documentation Live Server Section

**Target Files:**
- `/gpt5-openai-agents-sdk-polygon-mcp/API_DOCUMENTATION.md`

**Template Content:**

```markdown
## Live Server for API Testing and Integration

### API Testing Environment Setup

Live Server provides a production-like environment for comprehensive API testing:

**Backend API Server:**
```bash
# Start backend API server
cd /path/to/backend
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend Live Server with API Integration:**
```bash
# Build and serve frontend with API proxy
npm run serve:production
# Start Live Server (will proxy /api calls to localhost:8000)
```

### Environment-Specific API Configuration

**Development API Testing (Port 5500):**
- API proxy: `localhost:8000`
- CORS enabled for local testing
- Development error handling and logging

**Staging API Testing (Port 5501):**
- Staging API endpoints (when configured)
- Production-like security settings
- Enhanced error handling

**Production API Testing (Port 5502):**
- Production API endpoints
- Full security configuration
- Optimized performance settings

### API Integration Testing Workflow

1. **Start Backend Server**:
   ```bash
   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

2. **Build Frontend for API Testing**:
   ```bash
   npm run serve:production  # Or staging/development
   ```

3. **Configure Live Server**:
   - Ensure proxy configuration in `.vscode/settings.json`
   - Verify CORS settings for API calls

4. **Test API Endpoints**:
   - Use frontend interface to test API calls
   - Monitor network tab for request/response validation
   - Test error handling and edge cases

### API Proxy Configuration

**Live Server Proxy Settings:**
```json
{
  "liveServer.settings.proxy": [
    ["/api", "http://localhost:8000"]
  ],
  "liveServer.settings.cors": true
}
```

### Cross-Device API Testing

**Mobile API Testing:**
```bash
npm run cross-device:setup
# Mobile access: http://YOUR_LOCAL_IP:5502
# API calls proxied through Live Server to backend
```

**API Testing Checklist for Cross-Device:**
- [ ] API calls function from mobile devices
- [ ] Response times acceptable on mobile networks
- [ ] Error handling works across devices
- [ ] Authentication flows work on mobile browsers

### API Testing Troubleshooting

**Common API Integration Issues:**

1. **API Calls Returning 404**:
   ```bash
   # Verify backend server is running
   curl http://localhost:8000/health
   
   # Check proxy configuration
   # Ensure API paths match proxy settings
   ```

2. **CORS Errors in Live Server**:
   ```json
   // Ensure CORS enabled in Live Server settings
   {
     "liveServer.settings.cors": true
   }
   ```

3. **Mobile Devices Cannot Reach API**:
   - Verify mobile device on same network
   - Check firewall settings
   - Use local IP address for access

> **📖 Complete API Testing Guide**: For comprehensive API testing procedures with Live Server, including authentication, error handling, and performance testing, see `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md`.
```

---

## Category 3: API/Integration Documentation Templates

### Template 3A: API Integration Guide Live Server Section

**Target Files:**
- `/docs/JSON_API_REFERENCE.md`
- `/docs/JSON_ARCHITECTURE_GUIDE.md`

**Template Content:**

```markdown
## Live Server for API Integration Testing

### API Development and Testing Workflow

Live Server enables comprehensive testing of API integrations in production-like environments:

**Full-Stack Testing Setup:**
```bash
# 1. Start Backend API Server
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

# 2. Build and Serve Frontend
npm run serve:production

# 3. Start Live Server for API Integration Testing
# Access: http://localhost:5502 (with API proxy to port 8000)
```

### API Proxy Configuration for Integration Testing

**Live Server API Proxy Setup:**
```json
{
  "liveServer.settings.proxy": [
    ["/api", "http://localhost:8000"],
    ["/chat", "http://localhost:8000"],
    ["/health", "http://localhost:8000"]
  ],
  "liveServer.settings.cors": true,
  "liveServer.settings.headers": {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization"
  }
}
```

### Environment-Specific API Integration

**Development API Integration (Port 5500):**
- Local API server: `localhost:8000`
- Development CORS settings
- Enhanced debugging and logging

**Staging API Integration (Port 5501):**
- Staging API endpoints (when available)
- Production-like security settings
- Integration with staging data sources

**Production API Integration (Port 5502):**
- Production API endpoints
- Full security configuration
- Optimized performance settings

### API Testing Procedures

**Basic API Integration Test:**
```bash
# 1. Verify backend health
curl http://localhost:8000/health

# 2. Test API through Live Server proxy
# Access frontend at http://localhost:5502
# All /api calls automatically proxied to backend

# 3. Monitor API calls in browser DevTools Network tab
```

**Cross-Device API Testing:**
```bash
npm run cross-device:setup
# Mobile access: http://YOUR_LOCAL_IP:5502
# API calls work through Live Server proxy
```

### API Integration Validation Checklist

**Frontend-Backend Communication:**
- [ ] API endpoints accessible through Live Server proxy
- [ ] Request/response format validation
- [ ] Error handling and fallback mechanisms
- [ ] Authentication and authorization flows

**Cross-Platform API Access:**
- [ ] API calls function from mobile devices
- [ ] Response times acceptable across devices
- [ ] Error messages display correctly on all platforms
- [ ] Data synchronization works across devices

### Troubleshooting API Integration Issues

**Common Integration Problems:**

1. **API Proxy Not Working**:
   ```bash
   # Check proxy configuration in .vscode/settings.json
   # Verify backend server running on correct port
   # Test direct API access: curl http://localhost:8000/health
   ```

2. **CORS Issues with API Calls**:
   ```json
   // Ensure CORS enabled and configured
   {
     "liveServer.settings.cors": true
   }
   ```

3. **Mobile Devices Cannot Access API**:
   - Verify device on same Wi-Fi network
   - Use local IP instead of localhost
   - Check firewall settings for ports 5500-5502

> **📖 Comprehensive API Testing**: For detailed API integration testing procedures, authentication setup, and troubleshooting, see `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md`.
```

---

## Category 4: General Project Documentation Templates

### Template 4A: Project Structure Live Server Section

**Target Files:**
- `/STRUCTURE.md`
- `/docs/DOCUMENTATION_INDEX.md`

**Template Content:**

```markdown
## Live Server Testing Infrastructure

### Live Server Configuration Files

```
project-root/
├── .vscode/
│   ├── settings.json                    # Development Live Server config (port 5500)
│   ├── live-server-staging.json        # Staging Live Server config (port 5501)
│   └── live-server-production.json     # Production Live Server config (port 5502)
├── gpt5-openai-agents-sdk-polygon-mcp/
│   └── frontend_OpenAI/
│       ├── LIVE_SERVER_USAGE.md         # Comprehensive Live Server documentation
│       ├── package.json                 # Live Server npm scripts
│       └── dist/                        # Built files served by Live Server
```

### Live Server Scripts and Commands

**Available npm Scripts:**
```bash
npm run serve                    # Development build + Live Server setup
npm run serve:staging           # Staging build + Live Server setup
npm run serve:production        # Production build + Live Server setup

npm run test:pwa                # PWA testing with Live Server
npm run test:pwa:staging        # Staging PWA testing
npm run test:pwa:production     # Production PWA testing

npm run cross-device:setup     # Cross-device testing preparation
npm run cross-device:staging   # Staging cross-device testing

npm run lighthouse:live-server  # Performance testing with Lighthouse CI
```

### Documentation Structure for Live Server

**Core Documentation Files:**
- **`LIVE_SERVER_USAGE.md`**: Comprehensive guide (primary reference)
- **Migration Guides**: Include Live Server testing steps
- **Development Workflow**: Integration with Live Server testing
- **API Documentation**: Live Server proxy configuration
- **User Guides**: Live Server testing for user validation

### Live Server Testing Integration Points

**Development Workflow Integration:**
- Pre-commit testing with production builds
- Branch testing strategy using Live Server
- Release validation with cross-device testing

**Documentation Integration:**
- All technical docs reference Live Server testing procedures
- User guides include Live Server validation steps
- Migration guides include Live Server setup requirements

> **📖 Master Reference**: `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md` contains complete Live Server documentation including setup, configuration, troubleshooting, and advanced usage.
```

### Template 4B: General Documentation Live Server Reference

**Target Files:**
- Various general documentation files

**Template Content:**

```markdown
## Live Server Testing

### Quick Reference

**Primary Commands:**
```bash
npm run serve              # Development testing (port 5500)
npm run serve:staging      # Staging testing (port 5501) 
npm run serve:production   # Production testing (port 5502)
```

**When to Use Live Server:**
- Testing production builds locally
- Validating PWA functionality (service worker, offline mode)
- Cross-device testing on mobile and tablets
- Performance testing with Lighthouse CI

**Key Features:**
- Multi-environment support (development/staging/production)
- PWA testing with service worker validation
- Cross-device testing with CORS enabled
- Performance testing integration

### Configuration

**VS Code Live Server Extension Required:**
- Install: "Live Server" by Ritwick Dey
- Automatic configuration via npm scripts

**Port Configuration:**
- Development: 5500
- Staging: 5501  
- Production: 5502

> **📖 Complete Guide**: For comprehensive Live Server setup, troubleshooting, and advanced configuration, see `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md`.
```

---

## Category 5: User Guide Documentation Templates

### Template 5A: User Guide Live Server Section

**Target Files:**
- `/docs/USER_GUIDE_CHAT_INTERFACE.md`
- `/docs/SIMPLIFIED_ARCHITECTURE_GUIDE.md`

**Template Content:**

```markdown
## Testing Your Application with Live Server

### For End Users - Application Validation

Live Server provides a way to test the application exactly as it would run in production:

**Quick Testing Steps:**
1. **Build the Application**:
   ```bash
   npm run serve:production
   ```

2. **Start Live Server**:
   - Open VS Code
   - Press Ctrl+Shift+P (Cmd+Shift+P on Mac)
   - Type "Live Server: Open with Live Server"
   - Press Enter

3. **Access Application**:
   - Local: `http://localhost:5502`
   - Mobile: `http://YOUR_LOCAL_IP:5502` (same Wi-Fi network)

### User Testing Scenarios

**Web Browser Testing:**
- Test all application features in production-like environment
- Validate responsive design across different screen sizes
- Test PWA installation if supported by browser

**Mobile Device Testing:**
```bash
npm run cross-device:setup
# Follow instructions to access from mobile device
# URL: http://YOUR_LOCAL_IP:5502
```

**PWA (App-like) Testing:**
```bash
npm run test:pwa:production
# Test offline functionality and app installation
```

### User Validation Checklist

**Basic Functionality:**
- [ ] Application loads correctly
- [ ] All features work as expected
- [ ] Responsive design adapts to screen size
- [ ] Performance is acceptable

**PWA Features (if applicable):**
- [ ] Install prompt appears in supported browsers
- [ ] Application works offline
- [ ] App-like experience when installed

**Mobile Testing:**
- [ ] Touch interactions work properly
- [ ] Text is readable on mobile screens
- [ ] Navigation is touch-friendly

### Common User Issues and Solutions

**Application Not Loading:**
1. Check that Live Server is running (green "Port: 5502" in VS Code status bar)
2. Try refreshing the browser page
3. Check browser console for error messages

**Mobile Device Cannot Connect:**
1. Ensure mobile device is on same Wi-Fi network
2. Use local IP address (not localhost) to access
3. Check that firewall allows connections on port 5502

**PWA Features Not Working:**
1. Clear browser cache and reload page
2. Check that you're using a supported browser (Chrome, Edge, Firefox)
3. Verify you're using HTTPS or localhost (required for PWA)

> **📖 Technical Details**: For complete Live Server setup and troubleshooting information, developers can reference `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md`.
```

---

## Consistent Terminology Guide

### Standard Terms and Commands

**ALWAYS Use These Exact Terms:**

| Concept | Correct Term | Avoid |
|---------|-------------|--------|
| **Port Numbers** | 5500 (development), 5501 (staging), 5502 (production) | "default port", "dev port" |
| **Commands** | `npm run serve`, `npm run serve:staging`, `npm run serve:production` | "build and serve", "start live server" |
| **Testing Types** | PWA testing, cross-device testing, performance testing | "app testing", "mobile testing" |
| **Configuration** | VS Code Live Server configuration | "Live Server config", "server settings" |
| **Extension** | "Live Server" by Ritwick Dey | "Live Server extension", "the extension" |

### Standard Phrases

**Consistent Descriptions:**
- **When to use**: "Unlike the Vite development server, Live Server serves the actual built application files"
- **PWA Testing**: "Service worker functionality, offline mode, and installation prompts"
- **Cross-Device**: "Mobile and tablet testing on same Wi-Fi network"
- **Performance**: "Lighthouse CI integration for production-like environment simulation"

### Command Format Standards

**Always format commands consistently:**
```bash
# Build and serve commands
npm run serve                    # Development (port 5500)
npm run serve:staging           # Staging (port 5501)
npm run serve:production        # Production (port 5502)

# PWA testing commands
npm run test:pwa                # Development PWA testing
npm run test:pwa:staging        # Staging PWA testing
npm run test:pwa:production     # Production PWA testing

# Cross-device testing commands
npm run cross-device:setup     # Production cross-device setup
npm run cross-device:staging   # Staging cross-device setup
```

---

## Content Sections Matrix

### What Information Goes Where

| Documentation Type | Live Server Content Level | Key Sections | Reference Level |
|-------------------|---------------------------|--------------|----------------|
| **Migration/Workflow** | Comprehensive | Setup, Integration, Testing, Troubleshooting | Primary implementation guide |
| **Frontend/Technical** | Detailed | Testing procedures, PWA validation, Performance | Technical implementation details |
| **API/Integration** | Moderate | Proxy configuration, API testing, CORS setup | Integration-focused information |
| **General Project** | Basic | Quick reference, structure, commands | Overview and quick reference |
| **User Guide** | Simple | Basic testing steps, common issues, user validation | User-friendly instructions |

### Section Structure Standards

**For Migration/Workflow Docs:**
```markdown
## Live Server Integration for [Purpose]

### Overview
- Why Live Server is needed for this context
- Key benefits and capabilities

### Environment-Specific Setup
- Development, staging, production configurations
- Specific commands and procedures

### Integration Steps
- Step-by-step implementation
- Validation procedures

### Troubleshooting
- Common issues and solutions
- Context-specific problems

### Reference
- Link to comprehensive LIVE_SERVER_USAGE.md guide
```

**For Technical Docs:**
```markdown
## Live Server for [Technical Area]

### [Technical Context] Testing
- Technical requirements and setup
- Specific testing procedures

### Configuration
- Technical configuration details
- Environment-specific settings

### Validation
- Technical validation procedures
- Testing checklists

### Troubleshooting
- Technical issues and solutions

### Reference
- Link to comprehensive documentation
```

**For User Guides:**
```markdown
## Testing with Live Server

### Quick Testing Steps
- Simple step-by-step instructions
- User-friendly language

### Common Issues
- User-focused problems and solutions
- Non-technical troubleshooting

### Reference
- Link to technical documentation
```

---

## Implementation Guidelines

### Template Application Process

1. **Identify Target Document**: Determine documentation category and appropriate template
2. **Locate Integration Point**: Find natural place to insert Live Server information
3. **Adapt Template Content**: Customize template to match document's purpose and audience
4. **Maintain Consistency**: Use exact terminology and command formats
5. **Add Cross-References**: Include link to comprehensive LIVE_SERVER_USAGE.md guide
6. **Validate Integration**: Ensure Live Server info flows naturally with existing content

### Quality Assurance Checklist

**Before Updating Documentation:**
- [ ] Correct template selected for document type
- [ ] Information level appropriate for target audience
- [ ] All standard terminology used consistently
- [ ] Commands formatted according to standards
- [ ] Cross-reference to LIVE_SERVER_USAGE.md included
- [ ] Content integrates naturally with existing documentation

**After Updating Documentation:**
- [ ] Live Server information complete and accurate
- [ ] No contradictions with existing content
- [ ] Links work correctly
- [ ] Formatting consistent with document style
- [ ] Information helpful for target audience

### Common Integration Points

**Where to Add Live Server Information:**
- **Setup/Installation sections**: Include Live Server extension requirement
- **Testing/Validation sections**: Add Live Server testing procedures
- **Development workflow sections**: Include Live Server in workflow steps
- **Troubleshooting sections**: Add Live Server-specific issues and solutions
- **Reference sections**: Add links to comprehensive Live Server documentation

### Avoiding Information Duplication

**Keep Detailed Information in Master Guide:**
- Complex configuration procedures
- Comprehensive troubleshooting
- Advanced usage scenarios
- Detailed technical explanations

**Include in Other Documents:**
- Context-specific usage instructions
- Integration with existing workflows
- Quick reference information
- Links to detailed documentation

---

## Conclusion

These templates ensure consistent, complete, and appropriate Live Server documentation across all project files. By following these templates and guidelines, every documentation file will include the necessary Live Server information at the right level of detail for its intended audience, while maintaining consistency in terminology and cross-references to the comprehensive master guide.

**Key Success Factors:**
1. **Use appropriate template** for each documentation category
2. **Maintain consistent terminology** across all documents
3. **Include proper cross-references** to the master LIVE_SERVER_USAGE.md guide
4. **Match information depth** to document purpose and audience
5. **Integrate naturally** with existing content flow

This systematic approach will ensure that no critical Live Server information is missing from any project documentation file while avoiding unnecessary duplication and maintaining professional documentation standards.