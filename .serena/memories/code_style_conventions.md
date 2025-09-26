# Code Style and Conventions - Market Parser Project

## Python (Backend) Style Guide

### General Formatting

- **Line length**: 100 characters maximum (Black configuration)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes preferred for strings
- **Imports**: Sorted with isort using Black profile
- **Blank lines**: 2 lines between top-level definitions, 1 line between methods

### Naming Conventions

- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Good variable names**: `i,j,k,ex,Run,_,id,db,ai,ui,os,df,dt,fs,app,uv,mcp,ctx,api`

### Type Hints

- **Gradual adoption**: Type hints encouraged but not required
- **Return types**: Explicit return types for public functions
- **Import types**: `from typing import List, Dict, Optional, Union`
- **Pydantic models**: Use for API request/response validation

### Code Organization

```python
# Standard import order (handled by isort)
import os
import sys
from typing import List, Dict, Optional

import fastapi
import pydantic
from rich.console import Console

from src.backend.api_models import ChatRequest
from src.backend.utils import get_current_datetime_context
```

### Function and Class Structure

```python
class FinanceAnalysisAgent:
    """Agent for financial analysis using OpenAI GPT-5 models."""
    
    def __init__(self, model_id: str = "gpt-5-nano"):
        """Initialize the finance analysis agent."""
        self.model_id = model_id
        self.console = Console()
    
    async def analyze_market_data(
        self, 
        ticker: str, 
        analysis_type: str = "snapshot"
    ) -> Dict[str, Any]:
        """Analyze market data for a given ticker."""
        # Implementation here
        pass
```

### Error Handling

- **Use specific exceptions**: `ValueError`, `TypeError`, `RuntimeError`
- **Log errors**: Use structured logging with context
- **Graceful degradation**: Handle errors without crashing
- **User-friendly messages**: Provide clear error messages

### Documentation

- **Docstrings**: Not required (disabled in PyLint for prototyping)
- **Comments**: Use for complex logic explanation
- **Type hints**: Serve as inline documentation
- **README**: Comprehensive project documentation

## TypeScript/JavaScript (Frontend) Style Guide

### General Formatting

- **Line length**: 80 characters maximum (Prettier configuration)
- **Indentation**: 2 spaces (no tabs)
- **Quotes**: Single quotes preferred
- **Semicolons**: Required
- **Trailing commas**: ES5 style (objects, arrays)

### Naming Conventions

- **Variables and functions**: `camelCase`
- **Components**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Interfaces**: `PascalCase` with `I` prefix (optional)
- **Types**: `PascalCase`

### TypeScript Configuration

- **Strict mode**: Enabled with gradual adoption
- **Explicit types**: Encouraged but not required for prototyping
- **Interface definitions**: Use for component props and API responses
- **Generic types**: Use for reusable components

### React Component Structure

```typescript
interface ChatMessageProps {
  message: string;
  timestamp: Date;
  isUser: boolean;
  isLoading?: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  timestamp,
  isUser,
  isLoading = false,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const handleToggleExpansion = useCallback(() => {
    setIsExpanded(prev => !prev);
  }, []);
  
  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      {/* Component JSX */}
    </div>
  );
};

export default ChatMessage;
```

### Import Organization

```typescript
// React imports
import React, { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Third-party imports
import { format } from 'date-fns';
import { toast } from 'react-hot-toast';

// Local imports
import { ChatService } from '../services/ChatService';
import { MessageType } from '../types/ChatTypes';
import './ChatMessage.css';
```

### Hook Usage

- **Custom hooks**: Use for reusable logic
- **Hook naming**: Start with `use` prefix
- **Dependency arrays**: Always include in useEffect, useMemo, useCallback
- **State management**: Use useState for local state, context for global state

### Error Handling

```typescript
const [error, setError] = useState<string | null>(null);
const [isLoading, setIsLoading] = useState(false);

const handleSubmit = async (data: FormData) => {
  try {
    setIsLoading(true);
    setError(null);
    const result = await apiService.submitData(data);
    // Handle success
  } catch (err) {
    setError(err instanceof Error ? err.message : 'An error occurred');
  } finally {
    setIsLoading(false);
  }
};
```

## Configuration Files

### Python Configuration (pyproject.toml)

```toml
[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 100
known_first_party = ["src"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
disallow_untyped_defs = false  # Gradual adoption
```

### TypeScript Configuration (tsconfig.json)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### ESLint Configuration

- **TypeScript rules**: Gradual adoption with warnings
- **React rules**: Modern React 18+ patterns
- **Import rules**: Disabled (TypeScript handles imports)
- **Unused imports**: Error level (auto-fixable)

### Prettier Configuration

```javascript
module.exports = {
  semi: true,
  trailingComma: 'es5',
  singleQuote: true,
  printWidth: 80,
  tabWidth: 2,
  useTabs: false,
  jsxSingleQuote: true,
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: 'avoid',
  endOfLine: 'lf',
};
```

## File Organization

### Directory Structure

```
src/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── api_models.py        # Pydantic models
│   ├── prompt_templates.py  # AI prompt templates
│   ├── direct_prompts.py    # Direct prompt management
│   ├── optimized_agent_instructions.py # GPT-5 optimizations
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── frontend/
│   ├── components/          # React components
│   │   ├── Chat/
│   │   ├── Analysis/
│   │   └── Layout/
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API services
│   ├── types/              # TypeScript types
│   ├── utils/              # Frontend utilities
│   ├── config/             # Configuration
│   ├── styles/             # CSS files
│   ├── App.tsx             # Main app component
│   └── main.tsx            # Entry point
```

### File Naming

- **Python files**: `snake_case.py`
- **TypeScript files**: `PascalCase.tsx` for components, `camelCase.ts` for utilities
- **CSS files**: `kebab-case.css`
- **Configuration files**: `kebab-case.json` or `camelCase.config.js`

## Best Practices

### Code Quality

1. **Run linting before commits**: `npm run lint:fix`
2. **Use type hints**: Gradual adoption in Python, strict in TypeScript
3. **Handle errors gracefully**: Always include error handling
4. **Write tests**: Use standardized test prompts for E2E testing
5. **Document complex logic**: Comments for business logic

### Performance

1. **Minimize re-renders**: Use React.memo, useMemo, useCallback
2. **Optimize imports**: Tree-shaking friendly imports
3. **Lazy loading**: Code splitting for large components
4. **Caching**: Use appropriate caching strategies
5. **Bundle optimization**: Monitor bundle size

### Security

1. **Input validation**: Use Pydantic models for API validation
2. **Error handling**: Don't expose sensitive information
3. **Environment variables**: Store secrets in .env files
4. **CORS configuration**: Proper cross-origin settings
5. **Rate limiting**: Implement appropriate rate limits

### Maintainability

1. **Consistent naming**: Follow established conventions
2. **Modular design**: Separate concerns into different modules
3. **Configuration management**: Centralized configuration
4. **Version control**: Meaningful commit messages
5. **Documentation**: Keep README and docs updated
