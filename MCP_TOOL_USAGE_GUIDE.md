# 🛠️ MCP Server Tool Usage Guide - Comprehensive Reference

> **Target Audience**: AI Coding Agents  
> **Purpose**: Definitive guide for mandatory MCP tool usage across all 26 validated agent specialists  
> **Last Updated**: 2025-08-31 (Universal MCP Tool Enforcement - Post Validation)

## 📋 Executive Summary

This guide provides comprehensive documentation for the three primary MCP (Model Context Protocol) tools available in our development environment. **IMPORTANT: Based on comprehensive validation testing of all 26 agent specialists, MCP tools are now MANDATORY for ALL agents - no exceptions or waivers remain in effect.**

## 🚨 UNIVERSAL MCP TOOL ENFORCEMENT POLICY (2025-08-31)

### **MANDATORY MCP TOOL USAGE FOR ALL AGENTS**

**ALL 26 VALIDATED AGENT SPECIALISTS:**

- ✅ **REQUIRED to use MCP tools** - Universal enforcement based on successful validation testing
- ✅ **Sequential thinking mandatory** - All agents must use mcp__sequential-thinking__sequentialthinking
- ✅ **Context7 research required** - All agents must use mcp__context7__resolve-library-id and mcp__context7__get-library-docs
- ✅ **Filesystem tools mandatory** - All agents must use mcp__filesystem__* tools
- ✅ **Enhanced architecture standards maintained** - All protocols remain fully enforced
- ✅ **Standard Claude tools deprecated** - Read, Write, Edit, LS, Grep, Bash no longer acceptable for MCP-capable tasks

**VALIDATION RESULTS:**

- ✅ **238+ successful tool calls** across all 26 specialists
- ✅ **100% success rate** in comprehensive MCP testing
- ✅ **All agents validated** with sequential-thinking, context7, and filesystem tools
- ✅ **Zero failures** in MCP tool usage validation testing

## 🔄 Critical Usage Requirements by Role (UNIVERSAL MCP ENFORCEMENT)

### **@code-reviewer** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic code review analysis
- ✅ **REQUIRED: context7 research** - For researching latest security patterns and best practices
- ✅ **REQUIRED: filesystem tools** - For efficient multi-file code review operations
- ✅ **ENHANCED**: Focus on JSON schema validation and FSM integrity
- ✅ **ENHANCED**: Validate enhanced architecture patterns and security

### **@frontend-developer** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic UI/UX development planning
- ✅ **REQUIRED: context7 research** - For researching latest Gradio and frontend patterns
- ✅ **REQUIRED: filesystem tools** - For efficient frontend file operations
- ✅ **ENHANCED**: Gradio-specific JSON textbox optimization
- ✅ **ENHANCED**: Real-time UI updates and enhanced data visualization

### **@backend-developer** - MCP TOOLS MANDATORY (PRIMARY ARCHITECT)

- ✅ **REQUIRED: sequential-thinking** - For systematic architecture and backend planning
- ✅ **REQUIRED: context7 research** - For researching latest Python/Pydantic AI patterns
- ✅ **REQUIRED: filesystem tools** - For efficient backend file operations
- ✅ **ENHANCED**: Primary architect for 5-state FSM and JSON systems
- ✅ **ENHANCED**: Maintain dual parser architecture (JSON + regex fallback)
- ✅ **ENHANCED**: Lead schema validation and performance optimization

### **@performance-optimizer** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic performance analysis and optimization planning
- ✅ **REQUIRED: context7 research** - For researching latest optimization patterns and techniques
- ✅ **REQUIRED: filesystem tools** - For efficient performance monitoring file operations
- ✅ **ENHANCED**: JSON parsing optimization and schema validation performance
- ✅ **ENHANCED**: Cost optimization and resource usage monitoring

### **@documentation-specialist** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic documentation planning and organization
- ✅ **REQUIRED: context7 research** - For researching latest documentation patterns and standards
- ✅ **REQUIRED: filesystem tools** - For efficient documentation file operations
- ✅ **ENHANCED**: JSON architecture guides and schema documentation
- ✅ **ENHANCED**: Migration procedures and system simplification guides

### **@api-architect** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic API design and architecture planning
- ✅ **REQUIRED: context7 research** - For researching latest API patterns and MCP integration
- ✅ **REQUIRED: filesystem tools** - For efficient API development file operations
- ✅ **ENHANCED**: JSON response schemas and MCP integration patterns
- ✅ **ENHANCED**: Ensure API design consistency with enhanced architecture

### **@code-archaeologist** - MCP TOOLS MANDATORY

- ✅ **REQUIRED: sequential-thinking** - For systematic deep architecture analysis
- ✅ **REQUIRED: context7 research** - For researching architectural patterns and technical debt solutions
- ✅ **REQUIRED: filesystem tools** - For efficient deep codebase analysis operations
- ✅ **ENHANCED**: Deep insight for major architectural changes when needed
- ✅ **ENHANCED**: Support for backend-developer on complex architecture decisions

### **@tech-lead-orchestrator** - MCP TOOLS MANDATORY (CONTINUED ENFORCEMENT)

- ✅ **REQUIRED: sequential-thinking** - For systematic orchestration analysis
- ✅ **REQUIRED: context7** - For research of orchestration patterns
- ✅ **REQUIRED: filesystem** - For orchestration file operations

---

## 🔧 Tool 1: Context7 - Latest Documentation Research

### **Current Enforcement Status**

- **ALL AGENTS**: **REQUIRED** (Universal enforcement based on successful validation)
- **NO EXCEPTIONS**: All 26 specialists must use Context7 for research tasks

### **Purpose**

Context7 provides access to the most up-to-date documentation, best practices, and code examples for any library or framework. It's your primary tool for researching current development patterns.

### **When to Use (Orchestrator Only)**

- ✅ Researching latest framework versions (React 18+, Vue 3+, Gradio 4+, etc.)
- ✅ Finding current API syntax and best practices
- ✅ Getting code examples for modern patterns
- ✅ Understanding breaking changes between versions
- ✅ Before orchestrating any complex development delegation

### **When NOT to Use**

- ❌ For general programming concepts (use standard knowledge)
- ❌ For project-specific code (use filesystem tools)
- ❌ For debugging existing code (use other analysis tools)

### **Proper Tool Call Syntax (ALL AGENTS)**

#### Step 1: Resolve Library ID

```javascript
mcp_context7_resolve-library-id
Parameters:
{
  "libraryName": "exact-library-name"  // e.g., "gradio", "react", "fastapi"
}
```

#### Step 2: Get Documentation

```javascript
mcp_context7_get-library-docs
Parameters:
{
  "context7CompatibleLibraryID": "/org/project",     // From step 1 result
  "topic": "specific-topic",                          // Optional: focus area
  "tokens": 5000                                      // Optional: response size limit
}
```

### **Best Practices (ALL AGENTS)**

1. **Always resolve library ID first** - Don't guess the Context7 ID format
2. **Be specific with topics** - "async handling in gradio 4.0" vs just "gradio"
3. **Use appropriate token limits** - 5000-10000 for detailed research
4. **Document findings** - Save key patterns found for team reference

### **Common Mistakes to Avoid (ALL AGENTS)**

❌ **Wrong**: Guessing library IDs

```javascript
// DON'T DO THIS
"context7CompatibleLibraryID": "/gradio/gradio"  // Wrong format
```

✅ **Correct**: Always resolve first

```javascript
// Step 1: Resolve
mcp_context7_resolve-library-id({"libraryName": "gradio"})
// Result: "/gradio-app/gradio"

// Step 2: Use resolved ID
mcp_context7_get-library-docs({"context7CompatibleLibraryID": "/gradio-app/gradio"})
```

### **Supplementary Research Methods (ALL AGENTS)**

**IN ADDITION to mandatory MCP Context7 usage, agents may also:**

- Review existing project documentation and patterns
- Analyze current codebase implementation conventions
- Study framework usage examples in existing code
- Cross-reference MCP research with project-specific patterns
- **ENHANCED**: Focus on enhanced JSON architecture patterns
- **ENHANCED**: Study dual parser architecture and schema validation approaches

---

## 🧠 Tool 2: Sequential Thinking - Problem Decomposition

### **Current Enforcement Status for Sequential Thinking**

- **ALL AGENTS**: **REQUIRED** (Universal enforcement based on successful validation)
- **NO EXCEPTIONS**: All 26 specialists must use Sequential Thinking for complex analysis

### **Sequential Thinking Purpose**

Breaks down complex problems into manageable, step-by-step thought processes. Essential for planning, architecture decisions, and systematic problem-solving.

### **When to Use (Orchestrator Only)**

- ✅ Planning complex delegation strategies
- ✅ Orchestrating multi-component development tasks
- ✅ Strategic architecture and design decisions
- ✅ Complex team coordination analysis
- ✅ Before delegating any non-trivial development work

### **When NOT to Use**

- ❌ Simple, single-step tasks that don't require systematic breakdown
- ❌ Routine operations with obvious solutions
- ❌ Tasks with clear, predetermined approaches

### **Proper Tool Call Syntax (ALL AGENTS)**

```javascript
mcp_sequential-thinking_sequentialthinking
Parameters:
{
  "thought": "Your current thinking step",
  "nextThoughtNeeded": true/false,
  "thoughtNumber": 1,           // Current step number
  "totalThoughts": 5,           // Estimated total steps
  "isRevision": false,          // Optional: if revising previous thought
  "revisesThought": 2,          // Optional: which thought to revise
  "branchFromThought": 3,       // Optional: branching point
  "branchId": "alternative-a", // Optional: branch identifier
  "needsMoreThoughts": false    // Optional: if need to extend
}
```

### **Required Analysis Pattern for ALL AGENTS**

**When using Sequential Thinking, agents should follow this systematic approach:**

```markdown
## Sequential Thinking Analysis
### Thought 1: Understanding the Problem
- [Clear definition of what needs to be done]
- [Current state assessment]
- [Root cause identification]
- [Enhanced architecture impact assessment]

### Thought 2: Research and Context
- [Context7 research findings]
- [Relevant documentation patterns]
- [Best practices identified]
- [Enhanced JSON architecture considerations]

### Thought 3: Solution Planning
- [Step-by-step implementation approach]
- [Required resources and dependencies]
- [Risk assessment and mitigation]
- [Enhanced JSON architecture compliance]

### Thought 4: Implementation Strategy
- [Specific technical approaches]
- [Testing and validation plan]
- [Rollback considerations]
- [Coordination with primary architects]

### Thought 5: Success Validation
- [Measurable success criteria]
- [Testing procedures]
- [Quality verification steps]
- [Enhanced architecture standards verification]
```

---

## 📁 Tool 3: Filesystem - Efficient File Operations

### **Current Enforcement Status for Filesystem Tools**

- **ALL AGENTS**: **REQUIRED** (Universal enforcement based on successful validation)
- **NO EXCEPTIONS**: All 26 specialists must use MCP Filesystem tools

### **Filesystem Tool Purpose**

Provides comprehensive file system operations that are more efficient and reliable than terminal-based commands. Handles reading, writing, searching, and managing files and directories.

### **When to Use Filesystem Tools (ALL AGENTS)**

- ✅ Reading multiple files for orchestration analysis
- ✅ Searching for architectural patterns across codebase
- ✅ Getting comprehensive file/directory information
- ✅ Directory traversal for delegation planning
- ✅ Any orchestration-related file system operation

### **When NOT to Use Filesystem Tools**

- ❌ When you need git operations (use terminal/git tools)
- ❌ When you need to run executables
- ❌ For operations outside allowed directories

### **Filesystem Operations & Syntax (ALL AGENTS)**

#### File Reading Operations

```javascript
// Read single file
mcp_filesystem_read_text_file
{
  "path": "/full/path/to/file.py",
  "head": 50,     // Optional: first N lines
  "tail": 50      // Optional: last N lines
}

// Read multiple files efficiently
mcp_filesystem_read_multiple_files  
{
  "paths": ["/path/file1.py", "/path/file2.py"]
}

// Get file metadata
mcp_filesystem_get_file_info
{
  "path": "/path/to/file.py"
}
```

### **Deprecated File Operations (NO LONGER ACCEPTABLE)**

**DEPRECATED - These tools are NO LONGER acceptable for MCP-capable tasks:**

- ~~Claude Read tool~~ - Use mcp__filesystem__read_text_file instead
- ~~Claude LS tool~~ - Use mcp__filesystem__list_directory instead
- ~~Claude Write tool~~ - Use mcp__filesystem__write_file instead
- ~~Claude Edit tool~~ - Use mcp__filesystem__edit_file instead
- ~~Claude Grep tool~~ - Use filesystem search or Context7 instead
- **ENHANCED**: All file operations must use MCP filesystem tools for consistency
- **ENHANCED**: Coordinate with primary architects for file structure decisions

---



---

## 🖥️ Tool 5: VS Code Live Server Integration - Production Testing

### **Current Enforcement Status for Live Server Integration**

- **ALL FRONTEND AGENTS**: **RECOMMENDED** (Essential for production build testing and validation)
- **@frontend-developer, @react-component-architect, @vue-component-architect**: **MANDATORY** for production testing
- **@code-reviewer**: **MANDATORY** for validating production builds before approval
- **@performance-optimizer**: **MANDATORY** for production performance testing

### **Live Server Integration Purpose**

VS Code Live Server integration provides essential production build testing capabilities that complement MCP tools. Unlike Vite's development server (which serves in-memory builds), Live Server serves actual built files, making it critical for:

- **Production Build Testing**: Validating actual compiled/optimized code
- **PWA Functionality**: Service worker, offline mode, and installation testing
- **Cross-Device Testing**: Mobile and tablet validation on real devices
- **Performance Testing**: Lighthouse CI and production environment simulation
- **API Integration Testing**: Testing actual API proxy configurations in production builds

### **When to Use Live Server (FRONTEND AGENTS)**

- ✅ Testing actual production builds after development
- ✅ PWA service worker and offline functionality validation
- ✅ Cross-device testing on mobile and tablet devices
- ✅ Performance testing with Lighthouse CI integration
- ✅ API proxy configuration testing in built applications
- ✅ Final QA validation before deployment
- ✅ Environment-specific configuration testing (dev/staging/production)

### **When NOT to Use Live Server**

- ❌ Active development with hot module replacement needs (use Vite dev server)
- ❌ Source map debugging and development tools (use Vite dev server)
- ❌ Real-time TypeScript compilation during development (use Vite dev server)

### **Live Server Setup Requirements (FRONTEND AGENTS)**

#### Prerequisites

1. **VS Code Live Server Extension**:
   - Extension: "Live Server" by Ritwick Dey
   - Required for all production testing workflows

2. **Frontend Build Completed**:
   ```bash
   cd frontend
   npm run build  # Creates dist/ directory with built files
   ```

3. **Backend API Running**:
   ```bash
   cd gpt5-openai-agents-sdk-polygon-mcp
   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### **Environment-Specific Live Server Configuration**

#### Development Environment (Port 5500)

```bash
cd frontend
npm run serve
# Provides usage instructions and builds development version
# Access: http://localhost:5500
```

**Configuration**: Uses `.vscode/settings.json`:
```json
{
  "liveServer.settings.root": "./dist",
  "liveServer.settings.port": 5500,
  "liveServer.settings.proxy": [["/api", "http://localhost:8000"]],
  "liveServer.settings.spa": true,
  "liveServer.settings.cors": true
}
```

#### Staging Environment (Port 5501)

```bash
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm run serve:staging
# Copy .vscode/live-server-staging.json settings when prompted
# Access: http://localhost:5501
```

#### Production Environment (Port 5502)

```bash
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm run serve:production
# Copy .vscode/live-server-production.json settings when prompted
# Access: http://localhost:5502
```

### **PWA Testing with Live Server (FRONTEND AGENTS)**

#### Service Worker Validation Workflow

```bash
# 1. Build PWA version
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm run test:pwa:production

# 2. Start Live Server (production configuration)
npm run serve:production

# 3. Open in browser: http://localhost:5502
# 4. Open DevTools → Application → Service Workers
# 5. Verify service worker registration and caching strategies
# 6. Test offline functionality (toggle "Offline" checkbox)
```

#### PWA Installation Testing

1. **Desktop Installation**: Look for browser PWA install prompt (Chrome/Edge)
2. **Mobile Installation**: Test "Add to Home Screen" functionality
3. **Standalone Mode**: Validate app behavior after installation
4. **Manifest Validation**: Verify manifest.json configuration

### **Cross-Device Testing with Live Server (FRONTEND AGENTS)**

#### Mobile/Tablet Testing Setup

```bash
# 1. Prepare for cross-device testing
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm run cross-device:setup
# Shows local IP address for mobile access

# 2. Find your local IP (alternative methods)
ipconfig    # Windows
ifconfig    # macOS/Linux

# 3. Start Live Server with appropriate configuration
npm run serve  # or serve:staging, serve:production

# 4. Access from mobile devices on same Wi-Fi network
# http://[LOCAL_IP]:5500 (development)
# http://[LOCAL_IP]:5501 (staging)
# http://[LOCAL_IP]:5502 (production)
```

#### Cross-Device Validation Checklist

- [ ] **Responsive Design**: Layout adapts properly to mobile/tablet screens
- [ ] **Touch Interactions**: All buttons and interfaces work with touch
- [ ] **API Integration**: Backend API calls work correctly from mobile devices
- [ ] **PWA Features**: Installation prompts and offline functionality work
- [ ] **Performance**: Loading times and interactions are acceptable on mobile

### **API Integration Testing with Live Server (FRONTEND AGENTS)**

#### API Proxy Validation

```bash
# Test API endpoints through Live Server proxy
curl http://localhost:5500/api/v1/health      # Development
curl http://localhost:5501/api/v1/health      # Staging  
curl http://localhost:5502/api/v1/health      # Production

# Test specific API functionality
curl -X POST http://localhost:5500/api/v1/analysis/snapshot \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "analysis_type": "snapshot"}'
```

#### Frontend-Backend Integration Validation

1. **API Connectivity**: All `/api/*` requests properly proxied to backend
2. **CORS Configuration**: Cross-origin requests handled correctly
3. **Error Handling**: API errors properly displayed in production build
4. **Response Processing**: JSON responses correctly parsed and displayed
5. **Real-time Features**: WebSocket or polling functionality working

### **Integration with MCP Tools (FRONTEND AGENTS)**

#### Pattern 1: Research-Driven Live Server Setup

```javascript
// 1. Research latest PWA patterns (Context7)
mcp__context7__resolve_library_id({"libraryName": "workbox"})
mcp__context7__get_library_docs({...})

// 2. Plan Live Server testing strategy (Sequential Thinking)
mcp__sequential_thinking__sequentialthinking({
  "thought": "Planning comprehensive Live Server testing approach for PWA validation..."
})

// 3. Configure Live Server settings (Filesystem MCP)
mcp__filesystem__write_file({
  "path": "/project/.vscode/settings.json",
  "content": "Live Server configuration..."
})

// 4. Validate configuration in repository (git commands)
git add .vscode/settings.json
git commit -m "Configure Live Server for production testing"
git push origin main
```

#### Pattern 2: Production Build Testing Workflow

```javascript
// 1. Analyze current build process (Sequential Thinking)
mcp__sequential_thinking__sequentialthinking({
  "thought": "Analyzing production build requirements for Live Server testing..."
})

// 2. Build application for testing
// (Use npm run build via bash or appropriate build commands)

// 3. Validate build output (Filesystem MCP)
mcp__filesystem__directory_tree({
  "path": "/project/frontend_OpenAI/dist"
})

// 4. Test Live Server configuration
// (Start Live Server via VS Code or npm scripts)

// 5. Document testing results (git commands)
git add TESTING_RESULTS.md
git commit -m "Document Live Server testing validation"
git push origin main
```

### **Live Server vs Vite Development Server (FRONTEND AGENTS)**

#### When to Use Each Tool

**Use Vite Development Server (`npm run dev`) for**:
- Active development with hot module replacement (HMR)
- Real-time TypeScript compilation and error checking
- Source map debugging and development tools integration
- Rapid UI iteration and component development

**Use Live Server (`npm run serve`) for**:
- **Production Build Testing**: Validating actual compiled/optimized code
- **PWA Functionality**: Service worker, offline mode, and installation testing
- **Cross-Device Testing**: Mobile and tablet validation on real devices
- **Performance Testing**: Lighthouse CI and production environment simulation
- **Final QA Validation**: Pre-deployment testing with built application files

#### Development Workflow Integration

```bash
# Standard Development Phase
npm run dev  # Vite development server (Port 3000)

# Production Testing Phase
npm run build && npm run serve  # Live Server testing (Port 5500)

# Environment-Specific Testing
npm run serve:staging    # Port 5501
npm run serve:production # Port 5502

# Cross-Device Testing
npm run cross-device:setup  # Prepare for mobile testing
```

### **Performance Testing with Live Server (PERFORMANCE AGENTS)**

#### Lighthouse CI Integration

```bash
# Run Lighthouse CI with Live Server
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI

# Production performance testing
npm run lighthouse:live-server

# Staging performance testing
npm run lighthouse:live-server:staging

# Local Lighthouse testing
npm run lighthouse
```

#### Performance Validation Checklist

- [ ] **Load Times**: Initial page load under acceptable thresholds
- [ ] **Bundle Size**: JavaScript and CSS bundles optimized
- [ ] **PWA Score**: Progressive Web App score >90%
- [ ] **Accessibility**: Accessibility score >95%
- [ ] **Performance**: Performance score >85%
- [ ] **SEO**: SEO score optimized for production

### **Troubleshooting Live Server Issues (FRONTEND AGENTS)**

#### Common Issues and Solutions

**Live Server Not Starting**:
- Ensure VS Code Live Server extension is installed
- Check that port (5500/5501/5502) is not already in use
- Verify `.vscode/settings.json` configuration is valid JSON

**API Proxy Not Working**:
- Confirm FastAPI backend is running on `http://localhost:8000`
- Check proxy configuration in Live Server settings
- Verify CORS configuration in both frontend and backend

**PWA Features Not Working**:
- Ensure application is built with `npm run build`
- Check service worker registration in DevTools
- Verify manifest.json is accessible and valid

**Cross-Device Testing Issues**:
- Confirm all devices are on the same Wi-Fi network
- Check firewall settings allowing local network access
- Verify local IP address is correct and accessible

### **Live Server Documentation References**

For comprehensive Live Server usage instructions and advanced configuration:

- **Primary Documentation**: `/gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md`
- **Migration Guide**: Part III of `/gpt5-openai-agents-sdk-polygon-mcp/OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md`
- **Development Workflow**: `/DEVELOPMENT_WORKFLOW.md` (Live Server Integration section)
- **API Documentation**: `/gpt5-openai-agents-sdk-polygon-mcp/API_DOCUMENTATION.md` (Live Server Integration & Testing section)

---

## 🎭 Tool 6: Playwright MCP - Browser Testing Automation

### **Current Enforcement Status**

- **@frontend-developer, @react-component-architect, @code-reviewer**: **MANDATORY** for GUI testing and validation
- **@performance-optimizer**: **MANDATORY** for cross-browser performance testing
- **@api-architect**: **RECOMMENDED** for API integration testing via browser interfaces
- **ALL OTHER AGENTS**: **AVAILABLE** when browser automation testing is required

### **Playwright MCP Tool Purpose**

Playwright MCP provides comprehensive browser automation capabilities through structured JSON responses optimized for AI agents. These tools enable systematic testing of web applications with 20+ specialized browser automation tools, real-time accessibility snapshots, and token-efficient communication patterns.

**Core Capabilities:**
- **Cross-Browser Testing**: Chromium, Firefox, WebKit automation
- **Structured JSON Responses**: AI-optimized output for systematic analysis
- **Accessibility Testing**: Real-time accessibility tree inspection and DOM analysis
- **Performance Monitoring**: Network request analysis and performance metrics
- **Token Efficiency**: Compact, parseable responses reduce AI token usage
- **React Integration**: Optimized patterns for our React/TypeScript/Vite stack

### **When to Use Playwright MCP Tools (ALL AGENTS)**

- ✅ **GUI Testing and Validation**: Systematic testing of React component behavior
- ✅ **Cross-Browser Compatibility**: Testing across Chromium, Firefox, WebKit browsers
- ✅ **Accessibility Validation**: Structured accessibility tree analysis for compliance
- ✅ **API Integration Testing**: Testing frontend-backend API interactions through browser
- ✅ **Performance Analysis**: Monitoring network requests and browser performance metrics
- ✅ **Responsive Design Testing**: Validating mobile and desktop layouts with viewport management
- ✅ **User Workflow Validation**: End-to-end testing of complete user interactions
- ✅ **Real-time Debugging**: Interactive browser analysis with structured feedback

### **When NOT to Use Playwright MCP Tools**

- ❌ **Unit Testing**: Use Jest/Vitest for isolated component unit tests
- ❌ **Backend-Only Testing**: Use direct API testing tools for pure backend validation
- ❌ **Static Analysis**: Use linting and type checking tools for code analysis
- ❌ **Build Process Testing**: Use build system tools for compilation validation

### **Complete MCP Tool Inventory & Capabilities Matrix (ALL AGENTS)**

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

### **Proper Tool Call Syntax (ALL AGENTS)**

#### Basic Navigation and Page Analysis

```javascript
// Navigate to application
mcp__playwright__browser_navigate
{
  "url": "http://localhost:3000"
}

// Take accessibility snapshot for analysis
mcp__playwright__browser_snapshot
{
  // Returns structured DOM tree with accessibility information
}

// Resize for responsive testing
mcp__playwright__browser_resize
{
  "width": 375,
  "height": 667
}
```

#### User Interaction Testing

```javascript
// Type message in chat interface
mcp__playwright__browser_type
{
  "element": "Message input field",
  "ref": "textarea[data-testid='message-input']",
  "text": "What is the latest Apple stock price?"
}

// Click send button
mcp__playwright__browser_click
{
  "element": "Send button",
  "ref": "[data-testid='send-button']"
}

// Handle multi-line input with Shift+Enter
mcp__playwright__browser_press_key
{
  "key": "Shift+Enter"
}
```

#### Advanced Testing and Validation

```javascript
// Wait for AI response with timeout
mcp__playwright__browser_wait_for
{
  "text": "🎯 KEY TAKEAWAYS",
  "time": 30
}

// Execute JavaScript for custom validation
mcp__playwright__browser_evaluate
{
  "function": "() => { const msgs = document.querySelectorAll('.message-assistant'); const lastMsg = msgs[msgs.length-1]; return { hasEmoji: /📈|📉/.test(lastMsg.textContent), wordCount: lastMsg.textContent.split(' ').length, containsKeyTakeaways: lastMsg.textContent.includes('🎯 KEY TAKEAWAYS') }; }"
}

// Monitor network requests for API validation
mcp__playwright__browser_network_requests
{
  // Returns array of network requests with status, timing, and response data
}
```

#### Form and File Operations

```javascript
// Fill multiple form fields at once
mcp__playwright__browser_fill_form
{
  "fields": [
    {
      "name": "Message input",
      "type": "textbox",
      "ref": "textarea[placeholder*='message']",
      "value": "Analyze NVDA stock performance"
    }
  ]
}

// Upload file for analysis
mcp__playwright__browser_file_upload
{
  "paths": ["/path/to/document.pdf"]
}
```

### **Best Practices for Playwright MCP Usage (ALL AGENTS)**

#### 1. **Systematic Testing Approach**
- Use `browser_snapshot` after navigation to understand page structure before interactions
- Take screenshots at key validation points for visual documentation
- Monitor network requests to validate API integration during testing
- Use structured JavaScript evaluation for complex state validation

#### 2. **Token Efficiency Strategies**
- Batch related operations in logical sequences
- Use specific selectors to avoid large DOM tree returns
- Take snapshots only when page state significantly changes
- Leverage targeted JavaScript evaluation for specific data extraction

#### 3. **Error Handling and Debugging**
- Always check console messages after interactions for JavaScript errors
- Use `browser_wait_for` with appropriate timeouts for async operations
- Implement fallback selectors when primary selectors may fail
- Document unexpected behavior with screenshots and network request logs

#### 4. **Responsive Design Testing**
- Test multiple viewport sizes (mobile: 375x667, tablet: 768x1024, desktop: 1200x800)
- Validate touch interactions on mobile viewports
- Verify responsive layout changes with `browser_evaluate` for computed styles
- Test cross-device functionality with network request monitoring

### **Integration with Other MCP Tools (ALL AGENTS)**

#### Pattern 1: Research-Driven Browser Testing

```javascript
// 1. Research latest testing patterns (Context7)
mcp__context7__resolve_library_id({"libraryName": "playwright"})
mcp__context7__get_library_docs({"context7CompatibleLibraryID": "/microsoft/playwright", "topic": "browser automation best practices"})

// 2. Plan testing strategy (Sequential Thinking)
mcp__sequential_thinking__sequentialthinking({
  "thought": "Planning comprehensive browser testing approach for React chat interface..."
})

// 3. Execute browser testing (Playwright MCP)
mcp__playwright__browser_navigate({"url": "http://localhost:3000"})
mcp__playwright__browser_snapshot({})

// 4. Document results (git commands)
git add TESTING_RESULTS.md
git commit -m "Document Playwright MCP testing validation"
git push origin main
```

#### Pattern 2: Performance Testing with Cross-Tool Analysis

```javascript
// 1. Analyze current performance (Sequential Thinking)
mcp__sequential_thinking__sequentialthinking({
  "thought": "Analyzing performance requirements for browser testing..."
})

// 2. Execute performance testing (Playwright MCP)
mcp__playwright__browser_navigate({"url": "http://localhost:3000"})
mcp__playwright__browser_network_requests({})
mcp__playwright__browser_evaluate({"function": "() => performance.now()"})

// 3. Analyze local test files (Filesystem MCP)
mcp__filesystem__read_multiple_files({"paths": ["/tests/performance.spec.js", "/tests/integration.spec.js"]})

// 4. Update repository with findings (git commands)
git add tests/browser-performance.md
git commit -m "Update browser performance testing results"
git push origin main
```

#### Pattern 3: Component Testing with Accessibility Validation

```javascript
// 1. Research accessibility patterns (Context7)
mcp__context7__get_library_docs({"context7CompatibleLibraryID": "/w3c/wcag", "topic": "web accessibility guidelines"})

// 2. Plan accessibility testing (Sequential Thinking)
mcp__sequential_thinking__sequentialthinking({
  "thought": "Planning comprehensive accessibility validation for chat components..."
})

// 3. Execute accessibility testing (Playwright MCP)
mcp__playwright__browser_navigate({"url": "http://localhost:3000"})
mcp__playwright__browser_snapshot({})  // Returns structured accessibility tree
mcp__playwright__browser_evaluate({"function": "() => document.querySelectorAll('[aria-label], [role]').length"})

// 4. Validate component files (Filesystem MCP)
mcp__filesystem__read_text_file({"path": "/src/components/ChatInterface_OpenAI.tsx"})

// 5. Document accessibility findings (git commands)
git add accessibility-report.md
git commit -m "Document accessibility validation results"
git push origin main
```

### **OpenAI GUI-Specific Usage Patterns (FRONTEND AGENTS)**

#### Chat Interface Testing Workflow

```javascript
// Complete chat workflow validation
[
  {"tool": "browser_navigate", "parameters": {"url": "http://localhost:3000"}},
  {"tool": "browser_snapshot", "parameters": {}},
  {"tool": "browser_type", "parameters": {"element": "Message input", "ref": "textarea", "text": "What is NVDA trading at?"}},
  {"tool": "browser_click", "parameters": {"element": "Send button", "ref": "[data-testid='send-button']"}},
  {"tool": "browser_wait_for", "parameters": {"text": "🎯 KEY TAKEAWAYS", "time": 30}},
  {"tool": "browser_evaluate", "parameters": {"function": "() => document.querySelector('.message-assistant:last-child').textContent.includes('📈') || document.querySelector('.message-assistant:last-child').textContent.includes('📉')"}},
  {"tool": "browser_network_requests", "parameters": {}}
]
```

#### Responsive Design Validation

```javascript
// Cross-device testing sequence
[
  {"tool": "browser_resize", "parameters": {"width": 375, "height": 667}},  // Mobile
  {"tool": "browser_evaluate", "parameters": {"function": "() => window.getComputedStyle(document.querySelector('.message-bubble')).maxWidth"}},
  {"tool": "browser_resize", "parameters": {"width": 1200, "height": 800}}, // Desktop
  {"tool": "browser_evaluate", "parameters": {"function": "() => window.getComputedStyle(document.querySelector('.message-bubble')).maxWidth"}},
  {"tool": "browser_take_screenshot", "parameters": {"fullPage": true}}
]
```

#### Template Button and Export Testing

```javascript
// Template and export functionality validation
[
  {"tool": "browser_click", "parameters": {"element": "Technical Analysis template", "ref": "[data-testid='template-technical']"}},
  {"tool": "browser_wait_for", "parameters": {"text": "📊 Technical Analysis", "time": 15}},
  {"tool": "browser_click", "parameters": {"element": "Export button", "ref": "[data-testid='export-button']"}},
  {"tool": "browser_click", "parameters": {"element": "Export as Markdown", "ref": "[data-testid='export-markdown']"}},
  {"tool": "browser_evaluate", "parameters": {"function": "() => { const downloads = document.querySelectorAll('[download]'); return downloads.length > 0; }"}}
]
```

### **Environment-Specific Configuration (FRONTEND AGENTS)**

#### Development Environment Testing
```javascript
// Development testing configuration
{
  "environment": "development",
  "baseUrl": "http://localhost:3000",
  "backendUrl": "http://localhost:8000",
  "timeouts": {
    "navigation": 10,
    "interaction": 5,
    "apiResponse": 30
  }
}
```

#### Production Environment Testing
```javascript
// Production testing configuration
{
  "environment": "production",
  "baseUrl": "https://app.example.com",
  "backendUrl": "https://api.example.com",
  "timeouts": {
    "navigation": 20,
    "interaction": 15,
    "apiResponse": 60
  }
}
```

### **Troubleshooting Common Issues (ALL AGENTS)**

#### Element Not Found
**Symptoms**: MCP tools return "element not found" errors
**Solutions**:
1. Take fresh `browser_snapshot` to see current page state
2. Use alternative selectors (CSS class, data attributes, XPath)
3. Wait for dynamic content with `browser_wait_for`
4. Check for overlapping elements or z-index issues

```javascript
// Troubleshooting sequence
[
  {"tool": "browser_snapshot", "purpose": "Inspect current DOM structure"},
  {"tool": "browser_console_messages", "purpose": "Check for JavaScript errors"},
  {"tool": "browser_evaluate", "parameters": {"function": "() => document.querySelector('your-selector')"}, "purpose": "Verify selector exists"}
]
```

#### Slow Response Times
**Symptoms**: Timeouts on `browser_wait_for` operations
**Solutions**:
1. Increase timeout values for AI responses (30-60 seconds)
2. Monitor network requests to identify bottlenecks
3. Check backend health endpoint status
4. Verify API keys and rate limits

```javascript
// Performance debugging sequence
[
  {"tool": "browser_network_requests", "purpose": "Identify slow API calls"},
  {"tool": "browser_evaluate", "parameters": {"function": "() => performance.now()"}, "purpose": "Timestamp interactions"},
  {"tool": "browser_console_messages", "purpose": "Check for performance warnings"}
]
```

### **Best Practices Summary (ALL AGENTS)**

#### Test Organization and Execution
- **Systematic Approach**: Always start with navigation and snapshot
- **Token Efficiency**: Use targeted selectors and specific evaluations
- **Error Handling**: Monitor console messages and network requests
- **Documentation**: Take screenshots at key validation points

#### Integration with Development Workflow
- **Research First**: Use Context7 to understand latest testing patterns
- **Plan Systematically**: Use Sequential Thinking for complex test scenarios
- **Coordinate with Team**: Use GitHub MCP to document and share test results
- **Validate Comprehensively**: Test responsive design, accessibility, and performance

#### Quality Assurance Standards
- **Cross-Browser Testing**: Test on Chromium, Firefox, and WebKit
- **Responsive Validation**: Test mobile, tablet, and desktop viewports
- **Accessibility Compliance**: Use structured accessibility tree analysis
- **Performance Monitoring**: Track network requests and interaction timing
- **API Integration**: Validate frontend-backend communication through browser testing

---

## 🔄 Updated Tool Integration Patterns (Enhanced Architecture)

### **Pattern 1: Universal MCP Tool Usage**

```javascript
// 1. Research latest patterns (ALL AGENTS)
context7_resolve_library_id({"libraryName": "framework"})
context7_get_library_docs({...})

// 2. Plan implementation strategy (ALL AGENTS)
sequential_thinking({
  "thought": "Based on research, I need to implement enhanced JSON architecture work..."
})

// 3. Implement using MCP tools (ALL AGENTS)
// All agents implement using mcp__filesystem__* tools for local operations
// Use git commands for repository operations
// Focus on enhanced JSON architecture and coordination
```

### **Pattern 3: Playwright MCP Testing Workflow (ALL AGENTS)**

```javascript
// 1. Research testing best practices (Context7)
context7_resolve_library_id({"libraryName": "playwright"})
context7_get_library_docs({"context7CompatibleLibraryID": "/microsoft/playwright", "topic": "browser automation"})

// 2. Plan comprehensive testing strategy (Sequential Thinking)
sequential_thinking({
  "thought": "Planning systematic browser testing for React chat interface with accessibility validation..."
})

// 3. Execute browser testing workflow (Playwright MCP)
browser_navigate({"url": "http://localhost:3000"})
browser_snapshot({})  // Structured accessibility analysis
browser_type({"element": "Message input", "ref": "textarea", "text": "Test query"})
browser_wait_for({"text": "🎯 KEY TAKEAWAYS", "time": 30})
browser_network_requests({})  // API integration validation

// 4. Analyze test results and update codebase (Filesystem + Git)
filesystem_read_text_file({"path": "/src/components/ChatInterface.tsx"})  // Component analysis
// Use git commands for repository operations

// 5. Document findings and coordinate with team (git commands)
git add test-results.md
git commit -m "Document comprehensive testing coverage"
git push origin main
```

### **Pattern 2: Systematic Analysis and Implementation**

```javascript
// 1. Break down the problem (ALL AGENTS)
sequential_thinking({
  "thought": "Complex enhanced architecture task has components: JSON schema, FSM, UI integration..."
})

// 2. Research current best practices (ALL AGENTS)
context7_get_library_docs({...})

// 3. Examine current codebase (ALL AGENTS)
// Local files: filesystem_read_multiple_files({...})
// Use git commands for repository analysis

// 4. Implement coordinated tasks (ALL AGENTS)
// Primary architect (backend-developer) leads with secondary agent support
// All agents use MCP tools for consistency and efficiency
// Repository operations: Git commands
// Local operations: Filesystem MCP tools

// 5. Document and commit changes (git commands)
git add .
git commit -m "Implement systematic analysis and coordinated tasks"
git push origin main
```

---

## ✅ Updated Validation and Testing (Enhanced Architecture)

### **Tool Call Validation Checklist**

**FOR ALL AGENTS (MCP tools mandatory):**

- [ ] **Context7**: Have you resolved the library ID first?
- [ ] **Sequential Thinking**: Is the task complex enough to warrant step-by-step analysis?
- [ ] **Filesystem**: Are you using absolute paths from workspace root?
- [ ] **Git Commands**: Are you using git commands as PRIMARY for repository operations?
- [ ] **Evidence**: Can you provide specific evidence of MCP tool usage?
- [ ] **Enhanced Architecture**: Are you considering enhanced JSON architecture coordination?
- [ ] **Research**: Have you investigated latest patterns and best practices?
- [ ] **Implementation**: Are you using MCP tools for file operations and git commands for repository operations?
- [ ] **Documentation**: Have you documented your approach and decisions?
- [ ] **Coordination**: Are you properly coordinating with primary architects?
- [ ] **Tool Priority**: Are you using git commands as the only repository management method?

### **Quality Indicators**

**Good MCP tool usage (ALL AGENTS):**

- Specific, actionable MCP tool parameters
- Appropriate MCP tool selection for task requirements
- Parallel MCP execution when possible
- Clear integration between MCP tools
- **Enhanced**: Consideration of enhanced JSON architecture coordination
- Systematic analysis using Sequential Thinking
- Research through Context7 for latest patterns
- Efficient use of MCP Filesystem tools
- **PRIMARY**: Git commands for all repository operations
- Clear documentation of implementation decisions
- **Enhanced**: Following enhanced JSON architecture patterns
- **Enhanced**: Proper coordination with primary architects
- **Git Commands**: Proper use of git commands for all repository operations

---

## 📚 Updated Quick Reference (Enhanced Architecture)

### **Context7 Quick Commands (ALL AGENTS)**

```bash
# Research React patterns (ALL AGENTS)
resolve-library-id("react") → get-library-docs("/facebook/react", "hooks")

# Research Python async patterns (ALL AGENTS)
resolve-library-id("asyncio") → get-library-docs("/python/asyncio", "coroutines")

# Research JSON schema patterns (ALL AGENTS)
resolve-library-id("jsonschema") → get-library-docs("/python-jsonschema/jsonschema", "validation")

# Research Gradio patterns (ALL AGENTS)
resolve-library-id("gradio") → get-library-docs("/gradio-app/gradio", "interface")
```

### **Sequential Thinking Quick Commands (ALL AGENTS)**

```bash
# Start systematic analysis session (ALL AGENTS)
sequential-thinking("Planning implementation strategy for enhanced JSON architecture...")

# Continue with detailed planning (ALL AGENTS)
sequential-thinking("Need to coordinate with backend-developer as primary architect...")

# Problem decomposition (ALL AGENTS)
sequential-thinking("Breaking down complex task into manageable components...")
```

### **Filesystem Quick Commands (ALL AGENTS)**

```bash
# Project overview (ALL AGENTS)
directory_tree("/project/root")

# Multi-file read for analysis (ALL AGENTS)
read_multiple_files(["/src/json_parser.py", "/src/json_schemas.py"])

# Efficient file operations (ALL AGENTS)
read_text_file("/path/to/file.py")
write_file("/path/to/new_file.py", "content")
edit_file("/path/to/file.py", [{"oldText": "...", "newText": "..."}])
```



### **Playwright MCP Quick Commands (FRONTEND/TESTING AGENTS)**

```bash
# Basic browser operations (FRONTEND AGENTS)
browser_navigate({"url": "http://localhost:3000"})
browser_snapshot({})  # Structured accessibility analysis
browser_take_screenshot({"fullPage": true})

# User interaction testing (FRONTEND AGENTS)
browser_type({"element": "Message input", "ref": "textarea", "text": "Test message"})
browser_click({"element": "Send button", "ref": "[data-testid='send-button']"})
browser_press_key({"key": "Enter"})

# Advanced validation (FRONTEND AGENTS)
browser_wait_for({"text": "🎯 KEY TAKEAWAYS", "time": 30})
browser_evaluate({"function": "() => document.querySelector('.message-assistant').textContent.includes('📈')"})
browser_network_requests({})  # API integration validation

# Responsive and accessibility testing (FRONTEND AGENTS)
browser_resize({"width": 375, "height": 667})  # Mobile viewport
browser_fill_form({"fields": [{"name": "input", "type": "textbox", "ref": "textarea", "value": "test"}]})
browser_handle_dialog({"accept": true})
```

---

## 🚨 UNIVERSAL MCP TOOL REQUIREMENTS (Enhanced Architecture)

### **MCP Tool Requirements for ALL AGENTS**

**ALL 26 VALIDATED AGENTS MUST provide explicit evidence of MCP tool usage:**

1. **Sequential Thinking Evidence**:
   - Must show numbered thought progression from `mcp__sequential-thinking__sequentialthinking`
   - Include systematic problem breakdown and analysis steps
   - Document decision-making process clearly
   - **Enhanced**: Consider enhanced JSON architecture coordination

2. **Context7 Research Evidence** (when applicable):
   - Must show library ID resolution: `mcp__context7__resolve-library-id`
   - Must show documentation retrieval: `mcp__context7__get-library-docs`
   - Include specific research findings and patterns discovered
   - **Enhanced**: Research enhanced JSON architecture patterns

3. **Filesystem Operations Evidence** (when applicable):
   - Must use `mcp__filesystem__*` tools for all file operations
   - Include specific filesystem tool calls made
   - Document file operations performed for implementation
   - **Enhanced**: Focus on enhanced JSON architecture file analysis

### **UNIVERSAL MCP REQUIREMENTS (No Exceptions)**

**ALL SPECIALIST AGENTS MUST provide:**

- ✅ **MCP sequential thinking evidence** - Mandatory for complex tasks
- ✅ **MCP context7 research evidence** - Mandatory for research tasks
- ✅ **MCP filesystem operations evidence** - Mandatory for local file operations
- ✅ **Git operations evidence** - Use git commands for repository operations (ONLY method)
- ✅ Clear documentation of implementation approach and decisions
- ✅ Test scripts for bug fixes and validation procedures
- ✅ **Enhanced**: Evidence of enhanced JSON architecture compliance
- ✅ **Enhanced**: Proper coordination with primary architects

### **Universal Role Requirements (Enhanced Architecture)**

**ALL AGENTS (@tech-lead-orchestrator, @code-reviewer, @backend-developer, @frontend-developer, @documentation-specialist, @performance-optimizer, @api-architect, @code-archaeologist) MUST provide evidence of:**

```text
✅ mcp__sequential-thinking__sequentialthinking - Systematic analysis steps
✅ mcp__context7__resolve-library-id + get-library-docs - Research evidence  
✅ mcp__filesystem__* - Local file operations evidence
✅ git commands - Repository operations evidence (ONLY method for repository management)
✅ mcp__playwright__* - Browser testing automation (frontend/testing agents)
✅ Implementation decisions documented with clear reasoning
✅ Test scripts and validation procedures for bug fixes
✅ Enhanced: Evidence of enhanced JSON architecture compliance
✅ Enhanced: Proper coordination with primary architects (especially backend-developer)
```

### **Updated Evidence Examples (Enhanced Architecture + Live Server)**

**✅ Good MCP Tool Usage Evidence (ALL AGENTS)**:

```text
I used mcp__sequential-thinking__sequentialthinking to break down this enhanced architecture task:
Thought 1: Analyzed the requirements and enhanced JSON architecture coordination needs...
Thought 2: Researched latest patterns using Context7 for relevant libraries...
Thought 3: Planned implementation approach focusing on enhanced architecture integrity...
Thought 4: Coordinated with backend-developer as primary architect...
Thought 5: Validated approach against enhanced architecture standards...

I used mcp__context7__resolve-library-id to research enhanced JSON schema patterns...
I used mcp__filesystem__read_multiple_files to analyze current codebase structure...
I used git commands to analyze repository patterns and implement changes (git commands are the only repository management method)...

[FRONTEND AGENTS] I used Live Server integration for production build validation:
- Built application with npm run build
- Tested production build with npm run serve (Port 5500)
- Validated PWA functionality via Live Server environment
- Performed cross-device testing on mobile devices
- Verified API proxy configuration in production build
```

**❌ Unacceptable Evidence (Deprecated Approach)**:

```text
I performed systematic analysis of this task:
Step 1: Analyzed current structure using Read and LS tools... (DEPRECATED)
Step 2: Researched best practices through documentation review... (INSUFFICIENT - must use Context7)
Step 3: Implemented using Write and Edit tools... (DEPRECATED - must use MCP filesystem)
Step 4: Used git commands for repository operations... (CORRECT - git commands are the ONLY method)
```

## 🚨 Updated Enforcement Protocol (Enhanced Architecture)

### **Tool Usage Violations**

**For ALL AGENTS (Universal MCP Enforcement):**

1. **Not using MCP sequential-thinking** → Task lacks systematic analysis
2. **Not using MCP context7 research** → Implementation may use outdated patterns
3. **Not using MCP filesystem tools** → Local file operations inefficient and inconsistent
4. **Using deprecated Claude tools** → Non-compliance with MCP standards
5. **Enhanced**: Not considering enhanced JSON architecture coordination
6. **Enhanced**: Not following enhanced JSON architecture patterns
7. **Enhanced**: Not coordinating with primary architects

### **Quality Standards (All Agents - Universal MCP Enforcement)**

All tool usage must meet these standards:

- **Purposeful**: Clear reason for approach selection
- **Efficient**: Use most appropriate tools available
- **Complete**: All required analysis and documentation provided
- **Integrated**: Tools work together toward the goal
- **Enhanced**: Compliance with enhanced JSON architecture standards
- **Coordinated**: Proper coordination with primary architects

---

**FINAL REMINDER**:

- **ALL 26 AGENTS**: Must use MCP tools for all applicable tasks - no exceptions or waivers remain in effect
- **UNIVERSAL ENFORCEMENT**: Based on successful validation testing of all agent specialists
- **GIT COMMANDS ONLY**: Git commands are the ONLY method for repository operations - no GitHub MCP tools
- **DEPRECATED TOOLS**: Standard Claude tools (Read, Write, Edit, LS, Grep, Bash) are no longer acceptable for MCP-capable tasks
- **NO GITHUB MCP**: All GitHub MCP tools have been removed - use git commands exclusively
- **VALIDATION PROVEN**: 238+ successful tool calls demonstrate all agents can effectively use MCP tools
- All enhanced JSON architecture quality standards and development protocols remain fully enforced for all agents