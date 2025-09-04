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