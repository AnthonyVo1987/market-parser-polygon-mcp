# Code Style and Conventions

## Python Code Style

### General Conventions
- **Line Length**: 100 characters max (configured in black, isort, pylint)
- **Python Version**: 3.10+ (target: 3.12.3)
- **Formatter**: black with `--line-length 100`
- **Import Sorter**: isort with `--profile black --line-length 100`
- **Linter**: pylint with custom configuration

### Import Organization (isort)
```python
# Standard library imports
import os
import sys
from typing import Dict, List, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rich.console import Console

# First-party imports
from src.backend.config import settings
from src.backend.utils import helpers

# Local imports
from .models import User
```

**Import Sections (in order):**
1. FUTURE
2. STDLIB
3. THIRDPARTY
4. FIRSTPARTY
5. LOCALFOLDER

**Known packages:**
- Third-party: `openai`, `pydantic`, `rich`, `fastapi`, `uvicorn`, `agents`
- First-party: `src`

### Naming Conventions

**Variables and Functions:**
- `snake_case` for variables and functions
- Descriptive names (e.g., `get_stock_quote`, `market_status`)
- Private functions prefixed with `_` (e.g., `_get_polygon_client`)

**Classes:**
- `PascalCase` for class names
- Descriptive names (e.g., `AgentService`, `PolygonClient`)

**Constants:**
- `UPPER_SNAKE_CASE` for constants
- Defined at module level (e.g., `MAX_RESPONSE_TIME`, `DEFAULT_MODEL`)

**Type Hints:**
- Use type hints for function parameters and return types
- Import from `typing` module
- Example: `def get_quote(symbol: str) -> Dict[str, Any]:`

### Docstrings

**Format:** Generally minimal docstrings for prototyping
- Use docstrings for complex functions only
- Keep them concise and focused
- pylint configured with `missing-docstring` disabled

**Example:**
```python
def get_stock_quote(symbol: str) -> dict:
    """Get real-time stock quote for a symbol."""
    # Implementation
```

### Linting Configuration (.pylintrc)

**Disabled Checks (prototyping-friendly):**
- `missing-docstring` - Docstrings not required for all functions
- `invalid-name` - Flexible naming
- `too-few-public-methods` - Allow simple classes
- `too-many-arguments` - Allow many parameters for config
- `line-too-long` - Handled by black
- `broad-exception-caught` - Allow catching general exceptions

**Line Length:** 100 characters max

**Python Version:** 3.10

### Code Organization

**File Structure:**
```
src/backend/
├── main.py              # FastAPI app, endpoints, startup
├── config.py            # Configuration management
├── api_models.py        # Pydantic models for API
├── dependencies.py      # Dependency injection
├── cli.py              # CLI interface
├── services/           # Business logic
│   └── agent_service.py
├── tools/              # AI agent tools
│   ├── polygon_tools.py
│   └── finnhub_tools.py
├── utils/              # Helper functions
└── routers/            # API route handlers
```

**Module Organization:**
1. Imports (organized by isort)
2. Constants
3. Helper functions (private with `_` prefix)
4. Public functions
5. Classes (if any)
6. Main execution (if `__main__`)

## TypeScript/React Code Style

### General Conventions
- **Line Length**: No strict limit (Prettier handles formatting)
- **Formatter**: Prettier
- **Linter**: ESLint with TypeScript plugin
- **Type Checker**: TypeScript compiler (tsc)

### Naming Conventions

**Components:**
- `PascalCase` for component names (e.g., `ChatInterface`, `MessageList`)
- File names match component names (e.g., `ChatInterface.tsx`)

**Functions and Variables:**
- `camelCase` for functions and variables (e.g., `handleSubmit`, `apiUrl`)
- Descriptive names

**Hooks:**
- Prefix with `use` (e.g., `useDebounce`, `useConfig`)

**Types and Interfaces:**
- `PascalCase` for types and interfaces (e.g., `MessageType`, `ApiResponse`)
- Interface names without `I` prefix

**Constants:**
- `UPPER_SNAKE_CASE` for constants (e.g., `API_BASE_URL`)

### TypeScript

**Type Safety:**
- Use explicit types where helpful
- Prefer interfaces over types for objects
- Use `unknown` instead of `any` when possible
- ESLint configured to warn on `any` usage

**Type Annotations:**
```typescript
// Function parameters and return types
const fetchData = async (url: string): Promise<ApiResponse> => {
  // Implementation
};

// Interface for props
interface ChatProps {
  onSubmit: (message: string) => void;
  isLoading: boolean;
}

// Component with typed props
const Chat: React.FC<ChatProps> = ({ onSubmit, isLoading }) => {
  // Implementation
};
```

### React Conventions

**Component Structure:**
```typescript
// 1. Imports
import { useState, useEffect } from 'react';
import { ComponentProps } from './types';

// 2. Interface/Type definitions
interface ChatInterfaceProps {
  // ...
}

// 3. Component definition
const ChatInterface: React.FC<ChatInterfaceProps> = (props) => {
  // 4. Hooks
  const [state, setState] = useState();
  
  // 5. Event handlers
  const handleSubmit = () => {
    // ...
  };
  
  // 6. Effects
  useEffect(() => {
    // ...
  }, []);
  
  // 7. Render
  return (
    // JSX
  );
};

// 8. Export
export default ChatInterface;
```

**Hooks Rules:**
- Follow React Hooks rules (ESLint enforces)
- `exhaustive-deps` set to warn (prototyping-friendly)
- Use custom hooks for reusable logic

**Event Handlers:**
- Prefix with `handle` (e.g., `handleClick`, `handleSubmit`)
- Use arrow functions for inline handlers

### ESLint Configuration

**TypeScript Rules (prototyping-friendly):**
- `@typescript-eslint/no-unused-vars`: warn
- `@typescript-eslint/no-explicit-any`: warn
- `@typescript-eslint/no-unsafe-*`: warn (not error)
- `@typescript-eslint/explicit-function-return-type`: off
- `@typescript-eslint/explicit-module-boundary-types`: off

**React Rules:**
- `react/react-in-jsx-scope`: off (React 17+)
- `react/prop-types`: off (using TypeScript)
- `react-hooks/rules-of-hooks`: error
- `react-hooks/exhaustive-deps`: warn

**Import Rules:**
- Most import rules disabled (TypeScript handles resolution)
- `unused-imports/no-unused-imports`: error

### File Organization

**Frontend Structure:**
```
src/frontend/
├── main.tsx            # App entry point
├── App.tsx            # Root component
├── components/        # React components
│   ├── ChatInterface.tsx
│   ├── MessageList.tsx
│   └── PerformanceMetrics.tsx
├── hooks/            # Custom hooks
│   └── useDebounce.ts
├── services/         # API services
│   └── api.ts
├── types/           # TypeScript types
│   └── index.ts
├── utils/           # Helper functions
├── config/          # Configuration
└── styles/          # CSS/styling
```

## CSS/Styling Conventions

### General Rules
- **Tool**: PostCSS with cssnano for optimization
- **Approach**: Utility-first with custom CSS
- **Performance**: Optimized for Core Web Vitals

### Performance Optimizations
- **Avoid**: Backdrop filters, complex shadows, heavy gradients
- **Prefer**: Simple transitions (opacity, color)
- **Use**: Media queries instead of container queries
- **Minimize**: Reflows and repaints

### CSS Organization
```css
/* 1. CSS Reset/Normalize */
/* 2. CSS Variables */
:root {
  --primary-color: #0088cc;
}

/* 3. Base styles */
body {
  /* ... */
}

/* 4. Component styles */
.chat-interface {
  /* ... */
}

/* 5. Utility classes */
.text-center {
  text-align: center;
}
```

## Git Conventions

### Commit Messages
```
[CATEGORY] Brief description

- Detailed change 1
- Detailed change 2
- Test results (if applicable)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Categories:**
- `[FEATURE]` - New features
- `[FIX]` - Bug fixes
- `[REFACTOR]` - Code refactoring
- `[DOCS]` - Documentation updates
- `[TEST]` - Testing updates
- `[PERF]` - Performance improvements
- `[INFRASTRUCTURE]` - Infrastructure/tooling
- `[SERENA]` - Serena memory updates

### Branch Naming
- `main` or `master` - Production branch
- `feature/feature-name` - Feature branches
- `fix/bug-name` - Bug fix branches

## Testing Conventions

### Test File Naming
- CLI tests: `CLI_test_regression.sh`
- Test reports: `test-reports/` directory

### Test Prompts
- **Use standardized prompts only** (see `test_prompts.md`)
- **Format**: "Quick Response Needed with minimal tool calls: [query]"
- **Expected response time**: 6-10 seconds
- **Success rate**: 100%

## Quality Standards

### Python Quality
- **Pylint Score**: 10.00/10 (target)
- **Black**: All files formatted
- **isort**: All imports organized
- **Type Hints**: Used where helpful

### TypeScript Quality
- **ESLint**: Max 150 warnings
- **TypeScript**: No compilation errors
- **Prettier**: All files formatted

### Performance Targets
- **First Contentful Paint**: < 300ms
- **Largest Contentful Paint**: < 500ms
- **Response Time**: < 10s (average ~6s)
- **Success Rate**: 100%
