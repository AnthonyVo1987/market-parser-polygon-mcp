# VS Code Live Server Integration Guide

Comprehensive documentation for the VS Code Live Server integration with the GPT-5 Financial Analysis Frontend.

## Table of Contents

1. [Overview](#overview)
2. [When to Use Live Server vs Vite](#when-to-use-live-server-vs-vite)
3. [Quick Start Guide](#quick-start-guide)
4. [Environment Configurations](#environment-configurations)
5. [PWA Testing Procedures](#pwa-testing-procedures)
6. [Cross-Device Testing](#cross-device-testing)
7. [Package.json Scripts Documentation](#packagejson-scripts-documentation)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Configuration](#advanced-configuration)

## Overview

The VS Code Live Server integration provides a comprehensive testing environment for production builds, PWA functionality, and cross-device validation. Unlike the Vite development server, Live Server serves the actual built application files, making it ideal for:

- Testing production builds locally
- Validating PWA service worker functionality
- Cross-device testing on mobile and tablets
- Performance testing with Lighthouse CI
- Production-like environment simulation

### Key Features

- **Multi-Environment Support**: Development (port 5500), Staging (port 5501), Production (port 5502)
- **PWA Optimization**: Service worker testing, offline functionality, installation prompts
- **Cross-Device Testing**: CORS enabled for mobile device testing
- **SPA Routing**: Client-side routing support with fallback to index.html
- **API Proxy**: Automatic proxy configuration for backend API calls
- **Enhanced Browser Configuration**: Incognito mode with debugging ports for isolated testing

## When to Use Live Server vs Vite

### Use Vite Development Server When:

- **Active Development**: Code changes with hot module replacement
- **Rapid Iteration**: Testing UI changes and component development
- **Debugging**: Source map support and development tools
- **Initial Development**: Building features and components

```bash
# Vite development commands
npm run dev              # Development with hot reload
npm run dev:staging      # Staging environment with hot reload
npm run dev:production   # Production environment with hot reload
```

### Use Live Server When:

- **Production Build Testing**: Testing the actual built application
- **PWA Functionality**: Service worker, offline mode, installation testing
- **Cross-Device Testing**: Mobile and tablet testing on real devices
- **Performance Testing**: Lighthouse CI and performance validation
- **Production Simulation**: Testing in production-like environment
- **Final QA**: Pre-deployment validation and testing

```bash
# Live Server testing commands
npm run serve                    # Development build testing
npm run serve:staging           # Staging build testing  
npm run serve:production        # Production build testing
```

## Quick Start Guide

### Prerequisites

1. **Install VS Code Live Server Extension**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Live Server" by Ritwick Dey
   - Install the extension

2. **Ensure Backend is Running**:
   ```bash
   # In the parent directory
   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Basic Usage

1. **Build and Prepare**:
   ```bash
   npm run serve
   ```
   This will:
   - Build the development version
   - Display usage instructions
   - Set up the dist/ folder for serving

2. **Start Live Server**:
   - Open VS Code Command Palette (Ctrl+Shift+P)
   - Type "Live Server: Open with Live Server"
   - Press Enter

3. **Access Application**:
   - Local: `http://localhost:5500`
   - Network: `http://YOUR_LOCAL_IP:5500`

### Environment-Specific Testing

**Staging Environment**:
```bash
npm run serve:staging
# Then copy .vscode/live-server-staging.json settings to .vscode/settings.json
# Start Live Server (will use port 5501)
```

**Production Environment**:
```bash
npm run serve:production  
# Then copy .vscode/live-server-production.json settings to .vscode/settings.json
# Start Live Server (will use port 5502)
```

## Environment Configurations

### Development Environment (Port 5500)

**Configuration File**: `.vscode/settings.json`

**Features**:
- Development build testing
- Basic PWA functionality
- API proxy to localhost:8000
- CORS enabled for cross-device testing
- Chrome incognito with debugging port 9222

**Usage**:
```bash
npm run serve
# Serves development build on http://localhost:5500
```

### Staging Environment (Port 5501)

**Configuration File**: `.vscode/live-server-staging.json`

**Features**:
- Staging build with staging environment variables
- Production-like testing without full optimization
- Chrome incognito with debugging port 9223
- Staging API endpoints (when configured)

**Usage**:
```bash
npm run serve:staging
# Copy staging config to settings.json when prompted
# Serves staging build on http://localhost:5501
```

### Production Environment (Port 5502)

**Configuration File**: `.vscode/live-server-production.json`

**Features**:
- Full production build testing
- Optimized bundle and assets
- Production API endpoints
- Chrome incognito with debugging port 9224
- Enhanced security and optimization

**Usage**:
```bash
npm run serve:production
# Copy production config to settings.json when prompted  
# Serves production build on http://localhost:5502
```

### Configuration Switching

**Manual Method**:
1. Copy desired config to `.vscode/settings.json`:
   ```bash
   cp .vscode/live-server-staging.json .vscode/settings.json
   ```
2. Restart Live Server

**Automated Method** (via package.json scripts):
The serve commands provide clear instructions for configuration switching.

## PWA Testing Procedures

### Basic PWA Testing

1. **Build PWA-Ready Application**:
   ```bash
   npm run test:pwa
   ```

2. **Start Live Server** on port 5500

3. **Open Browser DevTools**:
   - Press F12
   - Navigate to "Application" tab
   - Check "Service Workers" section

4. **Verify PWA Features**:
   - Service Worker registration
   - Cache storage functionality
   - Offline mode (disconnect network)
   - Install prompt (if supported)

### Environment-Specific PWA Testing

**Staging PWA Testing**:
```bash
npm run test:pwa:staging
# Use staging Live Server config (port 5501)
# Test staging-specific PWA functionality
```

**Production PWA Testing**:
```bash
npm run test:pwa:production  
# Use production Live Server config (port 5502)
# Test production PWA functionality
```

### PWA Validation Checklist

- [ ] Service Worker registers successfully
- [ ] Static assets cached properly
- [ ] Application works offline
- [ ] Install prompt appears (desktop Chrome)
- [ ] PWA manifest loads correctly
- [ ] Icons and theme colors display properly
- [ ] App behaves like native app when installed

### PWA Troubleshooting

**Service Worker Not Registering**:
- Check browser console for errors
- Verify service worker file exists in dist/
- Ensure HTTPS (if required) or localhost exception

**Caching Issues**:
- Clear browser cache and storage
- Check DevTools > Application > Storage
- Verify service worker update mechanism

**Install Prompt Not Showing**:
- Ensure PWA criteria are met (HTTPS, manifest, service worker)
- Check Chrome DevTools > Application > Manifest
- Test on supported browsers (Chrome, Edge, Firefox)

## Cross-Device Testing

### Setup for Cross-Device Testing

1. **Build and Prepare**:
   ```bash
   npm run cross-device:setup
   ```
   This prepares the production build with network access enabled.

2. **Find Your Local IP Address**:
   ```bash
   # Windows
   ipconfig
   
   # macOS/Linux  
   ifconfig
   ```

3. **Start Live Server** with network access enabled

4. **Access from Mobile Devices**:
   - Connect mobile device to same Wi-Fi network
   - Open browser and navigate to: `http://YOUR_LOCAL_IP:5502`

### Staging Cross-Device Testing

```bash
npm run cross-device:staging
# Builds staging version for mobile testing
# Access via http://YOUR_LOCAL_IP:5501
```

### Mobile Testing Checklist

- [ ] Application loads on mobile browsers
- [ ] Touch interactions work properly  
- [ ] Responsive design adapts to screen size
- [ ] PWA install prompt works on mobile
- [ ] API calls function correctly
- [ ] Service worker operates on mobile
- [ ] Offline functionality works

### Tablet Testing

- [ ] Layout adapts to tablet screen sizes
- [ ] Touch targets are appropriately sized
- [ ] Landscape and portrait orientations work
- [ ] PWA functionality on tablet browsers

### Cross-Device Troubleshooting

**Cannot Access from Mobile Device**:
- Verify devices are on same network
- Check firewall settings
- Ensure Live Server is configured with `useLocalIp: true`
- Try accessing from computer browser using local IP first

**CORS Errors**:
- Verify CORS is enabled in Live Server configuration
- Check browser console for specific CORS errors
- Ensure API proxy is configured correctly

## Package.json Scripts Documentation

### Build and Serve Scripts

**Core Serving Commands**:
```bash
npm run serve                    # Build development + serve instructions
npm run serve:staging           # Build staging + serve instructions  
npm run serve:production        # Build production + serve instructions
```

Each serve command:
1. Builds the appropriate environment version
2. Provides clear usage instructions
3. Explains configuration requirements
4. Shows the correct port and URL

### PWA Testing Scripts

**PWA Testing Commands**:
```bash
npm run test:pwa                # Development PWA testing
npm run test:pwa:staging        # Staging PWA testing
npm run test:pwa:production     # Production PWA testing
```

Each PWA test command:
1. Builds the PWA-optimized version
2. Provides PWA testing instructions
3. Explains how to verify service worker functionality
4. Shows DevTools inspection steps

### Cross-Device Testing Scripts

**Cross-Device Setup Commands**:
```bash
npm run cross-device:setup     # Production cross-device setup
npm run cross-device:staging   # Staging cross-device setup
```

Each cross-device command:
1. Builds the appropriate version
2. Explains network IP discovery
3. Provides mobile access instructions
4. Confirms CORS configuration

### Lighthouse CI Integration

**Lighthouse Testing Commands**:
```bash
npm run lighthouse:live-server          # Production Lighthouse with Live Server
npm run lighthouse:live-server:staging  # Staging Lighthouse with Live Server
```

Each Lighthouse command:
1. Builds the optimized version
2. Provides Live Server startup instructions
3. Shows Lighthouse CI execution commands
4. Explains performance testing scope

### Help and Utilities

**Utility Commands**:
```bash
npm run live-server:help        # Display comprehensive help information
```

The help command provides:
- Available configuration files overview
- Quick start instructions
- Feature explanations
- Mobile testing setup guidance

## Troubleshooting

### Common Issues and Solutions

#### Live Server Extension Not Working

**Symptoms**:
- "Live Server: Open with Live Server" not available in Command Palette
- Extension appears installed but not functioning

**Solutions**:
1. **Reload VS Code Window**:
   - Press Ctrl+Shift+P
   - Type "Developer: Reload Window"
   
2. **Reinstall Extension**:
   - Uninstall Live Server extension
   - Restart VS Code
   - Reinstall Live Server extension

3. **Check Extension Version**:
   - Ensure you have "Live Server" by Ritwick Dey
   - Update to latest version if available

#### Port Already in Use

**Symptoms**:
- Error: "Port 5500 is already in use"
- Live Server fails to start

**Solutions**:
1. **Kill Process Using Port**:
   ```bash
   # Windows
   netstat -ano | findstr :5500
   taskkill /PID <PID_NUMBER> /F
   
   # macOS/Linux
   lsof -ti:5500 | xargs kill -9
   ```

2. **Use Different Port**:
   - Modify port number in `.vscode/settings.json`
   - Update any hardcoded references

3. **Stop Other Live Server Instances**:
   - Check VS Code status bar for running Live Server
   - Click "Port: 5500" to stop if running

#### 404 Errors on Page Refresh

**Symptoms**:
- Application works initially but 404 on page refresh
- Direct URL navigation fails

**Solutions**:
1. **Verify SPA Configuration**:
   - Ensure `"liveServer.settings.spa": true` in settings
   - Check that index.html exists in dist/ folder

2. **Check Build Output**:
   ```bash
   npm run build
   ls dist/  # Verify index.html exists
   ```

3. **Verify Router Configuration**:
   - Ensure React Router is configured for browser history
   - Check that routes are properly defined

#### API Calls Failing

**Symptoms**:
- Frontend loads but API calls return errors
- CORS errors in browser console

**Solutions**:
1. **Verify Backend Running**:
   ```bash
   # Check if backend is accessible
   curl http://localhost:8000/health
   ```

2. **Check Proxy Configuration**:
   - Verify proxy settings in `.vscode/settings.json`:
     ```json
     "liveServer.settings.proxy": [
       ["/api", "http://localhost:8000"]
     ]
     ```

3. **Enable CORS**:
   - Ensure `"liveServer.settings.cors": true` is set
   - Verify CORS headers configuration

4. **Check Network Tab**:
   - Open DevTools > Network
   - Verify API calls are being proxied correctly
   - Check for 404 or CORS errors

#### PWA Features Not Working

**Symptoms**:
- Service worker not registering
- Install prompt not appearing
- Offline functionality failing

**Solutions**:
1. **Build PWA Version**:
   ```bash
   npm run build  # Ensure PWA features are built
   ```

2. **Check Service Worker**:
   - DevTools > Application > Service Workers
   - Verify registration and activation
   - Check for console errors

3. **Verify HTTPS/Localhost**:
   - PWA features require HTTPS or localhost
   - Check browser security requirements

4. **Clear Cache**:
   - DevTools > Application > Storage
   - Click "Clear Storage" > "Clear site data"
   - Reload and test again

#### Mobile Device Cannot Connect

**Symptoms**:
- Desktop works but mobile shows connection error
- Mobile device cannot reach the server

**Solutions**:
1. **Verify Network Connection**:
   - Ensure both devices on same Wi-Fi network
   - Test with computer's IP address from desktop browser first

2. **Check Firewall**:
   - Windows: Allow port 5500-5502 through Windows Firewall
   - macOS: Check System Preferences > Security & Privacy > Firewall
   - Router: Ensure ports are not blocked

3. **Verify Live Server Configuration**:
   ```json
   "liveServer.settings.useLocalIp": true,
   "liveServer.settings.host": "localhost"
   ```

4. **Find Correct IP Address**:
   ```bash
   # Find active network interface IP
   ipconfig /all  # Windows - look for Wi-Fi adapter
   ifconfig | grep inet  # macOS/Linux - look for active interface
   ```

### Getting Help

If you encounter issues not covered here:

1. **Check Package.json Scripts**:
   ```bash
   npm run live-server:help  # Comprehensive help information
   ```

2. **Review Configuration Files**:
   - `.vscode/settings.json` (development)
   - `.vscode/live-server-staging.json` (staging)
   - `.vscode/live-server-production.json` (production)

3. **Verify Build Output**:
   ```bash
   npm run build
   ls -la dist/  # Check for required files
   ```

4. **Test Backend Separately**:
   ```bash
   curl http://localhost:8000/health  # Verify backend accessibility
   ```

## Advanced Configuration

### HTTPS Configuration

For production-like HTTPS testing, you can enable HTTPS in Live Server configurations:

```json
{
  "liveServer.settings.https": {
    "enable": true,
    "cert": "/path/to/certificate.crt",
    "key": "/path/to/private.key",
    "passphrase": "optional-passphrase"
  }
}
```

**Generating Self-Signed Certificates**:
```bash
# Create self-signed certificate for local testing
openssl req -x509 -newkey rsa:4096 -keyout localhost.key -out localhost.crt -days 365 -nodes
```

### Custom Headers Configuration

The Live Server configurations include custom headers for PWA and CORS support:

```json
{
  "liveServer.settings.headers": {
    "Service-Worker-Allowed": "/",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY"
  }
}
```

### Performance Optimization

**Browser Configuration for Performance Testing**:
```json
{
  "liveServer.settings.AdvanceCustomBrowserCmdLine": "chrome --incognito --remote-debugging-port=9222 --disable-web-security --user-data-dir=/tmp/chrome-dev-session --enable-features=VaapiVideoDecoder --disable-features=VizDisplayCompositor"
}
```

**Ignore Patterns Optimization**:
```json
{
  "liveServer.settings.ignoreFiles": [
    ".vscode/**",
    "**/node_modules/**",
    "**/src/**",
    "**/*.map",
    "**/.env*",
    "**/package*.json",
    "**/tsconfig*.json",
    "**/vite.config*",
    "**/test*",
    "**/*.test.*",
    "**/*.spec.*"
  ]
}
```

### Integration with Development Workflow

**VS Code Tasks Integration**:
Create `.vscode/tasks.json` for integrated workflows:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Build and Serve Production",
      "type": "shell",
      "command": "npm",
      "args": ["run", "serve:production"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    },
    {
      "label": "Cross-Device Testing Setup",  
      "type": "shell",
      "command": "npm",
      "args": ["run", "cross-device:setup"],
      "group": "test",
      "dependsOn": "Build and Serve Production"
    }
  ]
}
```

**Keyboard Shortcuts**:
Add to `.vscode/keybindings.json`:

```json
[
  {
    "key": "ctrl+shift+l",
    "command": "extension.liveServer.goOnline",
    "when": "editorTextFocus"
  },
  {
    "key": "ctrl+shift+k", 
    "command": "extension.liveServer.goOffline",
    "when": "editorTextFocus"
  }
]
```

### Monitoring and Debugging

**Browser DevTools Integration**:
The configurations include remote debugging ports for advanced debugging:

- Development: Port 9222
- Staging: Port 9223  
- Production: Port 9224

**Access Remote DevTools**:
```
http://localhost:9222  # Development debugging
http://localhost:9223  # Staging debugging
http://localhost:9224  # Production debugging
```

**Performance Monitoring**:
```bash
# Monitor Live Server performance
npm run lighthouse:live-server
# Provides detailed performance metrics
```

### Security Considerations

**Production Configuration**:
- Incognito mode isolates testing sessions
- Separate user data directories prevent pollution
- CORS configured for development only
- HTTPS available for production-like testing

**Development vs Production**:
- Development: Relaxed security for testing
- Staging: Intermediate security configuration
- Production: Enhanced security headers and validation

This configuration provides a comprehensive, secure, and flexible Live Server integration suitable for all stages of the development and testing lifecycle.