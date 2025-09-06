# GPT-5 Financial Analysis Frontend

A modern React frontend for the GPT-5 OpenAI Agents SDK financial analysis application, featuring responsive design, button prompts, and real-time chat interface. Built with Vite, TypeScript, and optimized for cross-platform compatibility.

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- FastAPI backend running (see parent README)

### Development Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Start the FastAPI backend:**
```bash
# In the parent directory
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

3. **Start the React frontend:**
```bash
npm run dev
```

4. **Access the application:**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

## Project Structure

```
frontend_OpenAI/
├── src/
│   ├── components/
│   │   ├── ChatInterface_OpenAI.tsx    # Main chat container
│   │   ├── ChatInput_OpenAI.tsx        # Message input form
│   │   └── ChatMessage_OpenAI.tsx      # Individual message display
│   ├── services/
│   │   └── api_OpenAI.ts               # API service for FastAPI calls
│   ├── types/
│   │   └── chat_OpenAI.ts              # TypeScript interfaces
│   ├── App.tsx                         # Main app component
│   └── main.tsx                        # React entry point
├── package.json
├── vite.config.ts
├── tsconfig.json
└── index.html
```

## Features

### Core Functionality
- **Financial Analysis Chat**: Real-time conversation with GPT-5 financial agent
- **Button Prompts**: Quick-access analysis buttons for snapshot, technical, and support/resistance analysis
- **Markdown Support**: Rich text rendering with react-markdown
- **Cross-Platform Responsive**: Optimized for desktop, tablet, and mobile devices

### Technical Features  
- **TypeScript**: Full type safety with strict compiler settings
- **Error Boundaries**: Production-ready error handling with fallback UI
- **Accessibility**: WCAG 2.1 AA compliance with comprehensive ARIA support
- **Performance**: Optimized rendering with memoization and efficient state management
- **Testing**: Comprehensive test suite with Vitest and React Testing Library

### UI/UX Features
- **Responsive Design**: Dynamic message bubbles (85% mobile, 70% desktop)
- **Smart Scrolling**: Platform-optimized scrollbars and smooth interactions
- **Loading States**: Visual feedback during API operations
- **Error Recovery**: User-friendly error messages with retry options
- **Touch-Friendly**: 44px minimum touch targets for mobile accessibility

## API Integration

### Backend Requirements
The frontend integrates with the FastAPI backend running on `http://localhost:8000` with multiple endpoints:

#### Core Endpoints
- **`POST /api/v1/analysis/chat`**: Chat analysis with context
  ```json
  Request: { "message": "analyze AAPL", "chat_history": [], "analysis_type": "snapshot" }
  Response: { "response": "GPT-5 analysis...", "ticker_detected": "AAPL", "analysis_type": "snapshot" }
  ```

#### Button Prompt Endpoints  
- **`GET /api/v1/prompts/templates`**: Get available analysis templates
- **`POST /api/v1/prompts/generate`**: Generate prompts with ticker substitution
- **`POST /api/v1/analysis/snapshot`**: Stock snapshot analysis
- **`POST /api/v1/analysis/technical`**: Technical analysis indicators
- **`POST /api/v1/analysis/support-resistance`**: Support and resistance levels

#### System Endpoints
- **`GET /health`**: Basic health check
- **`GET /api/v1/system/status`**: Detailed system metrics

## Development Commands

### Development
- **`npm run dev`** - Start development server (http://localhost:3000)
- **`npm run lint`** - Run ESLint with TypeScript support
- **`npm run lint:fix`** - Auto-fix ESLint issues

### Live Server Integration
- **`npm run serve`** - Build and serve development version with Live Server
- **`npm run serve:staging`** - Build and serve staging version with Live Server
- **`npm run serve:production`** - Build and serve production version with Live Server
- **`npm run live-server:help`** - Display comprehensive Live Server usage information

### PWA Testing
- **`npm run test:pwa`** - Build development version for PWA testing
- **`npm run test:pwa:staging`** - Build staging version for PWA testing
- **`npm run test:pwa:production`** - Build production version for PWA testing

### Cross-Device Testing
- **`npm run cross-device:setup`** - Prepare production build for mobile/tablet testing
- **`npm run cross-device:staging`** - Prepare staging build for mobile/tablet testing

### Lighthouse CI Integration
- **`npm run lighthouse:live-server`** - Run Lighthouse CI with Live Server (production)
- **`npm run lighthouse:live-server:staging`** - Run Lighthouse CI with Live Server (staging)

### Testing
- **`npm run test`** - Run test suite with Vitest
- **`npm run test:ui`** - Run tests with UI dashboard
- **`npm run test:coverage`** - Generate coverage report

### Production
- **`npm run build`** - Build optimized production bundle
- **`npm run preview`** - Preview production build locally

### Type Checking
- **`npm run type-check`** - Run TypeScript compiler check

## Architecture & Design Patterns

### Component Architecture
```
App.tsx
└── ChatInterface_OpenAI.tsx
    ├── AnalysisButtons.tsx          # Button prompt container
    │   ├── AnalysisButton.tsx       # Individual analysis buttons
    │   └── usePromptAPI.ts          # API integration hook
    ├── ChatInput_OpenAI.tsx         # Message input with enhancement
    └── ChatMessage_OpenAI.tsx       # Message display with markdown
```

### State Management
- **React Hooks**: Modern functional components with `useState` and `useEffect`
- **Custom Hooks**: `usePromptAPI` for template management and API integration
- **Error Boundaries**: Production-ready error handling with graceful degradation
- **Context-Free**: Simple props-based data flow for maintainability

### Design Principles
- **TypeScript First**: Strict type checking with comprehensive interfaces
- **Accessibility**: WCAG 2.1 AA compliance with proper ARIA attributes
- **Performance**: Memoization, efficient re-rendering, and optimized API calls
- **Responsive Design**: Mobile-first approach with breakpoint optimization
- **Component Naming**: "_OpenAI" suffix for clear component identification

### Testing Strategy
- **Component Testing**: React Testing Library with user interaction focus
- **Hook Testing**: Custom hook validation with comprehensive scenarios
- **Integration Testing**: End-to-end API workflow validation
- **Accessibility Testing**: Automated a11y checks with jest-axe

### Code Quality
- **ESLint**: Strict linting with TypeScript and React rules
- **TypeScript**: 100% type coverage with strict compiler settings
- **Error Handling**: Comprehensive error boundaries and user feedback
- **Security**: XSS prevention and secure API communication

## Live Server Integration

The project includes comprehensive VS Code Live Server integration for production build testing, PWA validation, and cross-device testing.

### When to Use Live Server vs Vite

**Use Vite Development Server (`npm run dev`) for**:
- Active development with hot module replacement
- Rapid UI iteration and component development
- Source map debugging and development tools

**Use Live Server (`npm run serve`) for**:
- Testing actual production builds
- PWA service worker and offline functionality testing
- Cross-device testing on mobile and tablets
- Performance testing with Lighthouse CI
- Final QA and pre-deployment validation

### Quick Start with Live Server

1. **Install VS Code Live Server Extension**:
   - Open VS Code Extensions (Ctrl+Shift+P)
   - Search for "Live Server" by Ritwick Dey
   - Install the extension

2. **Build and Serve**:
   ```bash
   npm run serve  # Builds and provides usage instructions
   ```

3. **Start Live Server**:
   - Open Command Palette (Ctrl+Shift+P)
   - Run "Live Server: Open with Live Server"
   - Access at http://localhost:5500

### Environment-Specific Testing

**Development Environment** (Port 5500):
```bash
npm run serve
# Basic PWA testing and development build validation
```

**Staging Environment** (Port 5501):
```bash
npm run serve:staging
# Copy .vscode/live-server-staging.json settings when prompted
# Production-like testing with staging configuration
```

**Production Environment** (Port 5502):
```bash
npm run serve:production
# Copy .vscode/live-server-production.json settings when prompted
# Full production build testing and optimization validation
```

### PWA Testing Workflow

1. **Build PWA Version**:
   ```bash
   npm run test:pwa:production  # For production PWA testing
   ```

2. **Start Live Server** with production configuration

3. **Test PWA Features**:
   - Open DevTools > Application > Service Workers
   - Verify service worker registration and caching
   - Test offline functionality (disconnect network)
   - Check PWA install prompt (Chrome/Edge)
   - Validate manifest.json configuration

### Cross-Device Testing

1. **Prepare for Mobile Testing**:
   ```bash
   npm run cross-device:setup
   ```

2. **Find Your Local IP**:
   ```bash
   ipconfig    # Windows
   ifconfig    # macOS/Linux
   ```

3. **Start Live Server** and access from mobile devices:
   - Connect mobile device to same Wi-Fi network
   - Navigate to `http://YOUR_LOCAL_IP:5502`
   - Test responsive design and touch interactions

### Key Features

- **Multi-Environment Support**: Development, staging, and production configurations
- **PWA Optimization**: Service worker testing and offline functionality
- **SPA Routing**: Client-side routing support with fallback handling
- **API Proxy**: Automatic backend API proxying to localhost:8000
- **CORS Configuration**: Cross-device testing with proper CORS headers
- **Performance Testing**: Lighthouse CI integration for automated testing
- **Browser Isolation**: Incognito mode with separate debugging ports

### Comprehensive Documentation

For detailed usage instructions, troubleshooting, and advanced configuration, see:
**[LIVE_SERVER_USAGE.md](./LIVE_SERVER_USAGE.md)**

### Integration with Development Workflow

The Live Server integration complements the existing Vite development workflow:

1. **Development**: Use `npm run dev` for active coding
2. **Feature Testing**: Use `npm run serve` to test built features
3. **PWA Validation**: Use `npm run test:pwa:*` for service worker testing
4. **Mobile Testing**: Use `npm run cross-device:*` for responsive validation
5. **Performance Testing**: Use `npm run lighthouse:live-server` for CI integration
6. **Pre-Deployment**: Use `npm run serve:production` for final validation