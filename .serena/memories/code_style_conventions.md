# Code Style and Conventions

## Python Backend Code Style

### Formatting Standards
- **Line Length**: 100 characters (Black and isort configured)
- **Formatter**: Black (v23.12.0+)
- **Import Sorting**: isort with Black profile
- **Linter**: pylint (v3.0.0+)
- **Type Checker**: mypy (v1.7.0+)

### Naming Conventions
- **Functions/Variables**: `snake_case`
  - Examples: `create_agent()`, `get_enhanced_agent_instructions()`, `shared_mcp_server`
- **Classes**: `PascalCase`
  - Examples: `ChatRequest`, `ChatResponse`, `Settings`
- **Constants**: `UPPER_SNAKE_CASE`
  - Examples: `MAX_TOKENS`, `DEFAULT_MODEL`
- **Private Functions/Variables**: Prefix with single underscore `_`
  - Example: `_internal_helper()`

### Type Hints
- **Required**: Type hints encouraged for function parameters and return types
- **Configuration**: mypy configured with gradual adoption
- **Example**:
```python
def create_agent(session: SQLiteSession, settings: Settings) -> Agent:
    """Create an agent with enhanced instructions."""
    pass
```

### Docstrings
- **Style**: Use descriptive docstrings for modules, classes, and functions
- **Format**: One-line docstrings for simple functions, multi-line for complex ones
- **Example**:
```python
def get_optimized_model_settings() -> dict:
    """Return optimized model settings for GPT-5-Nano."""
    return {...}
```

### Import Organization
- **Order** (isort configured):
  1. Future imports
  2. Standard library
  3. Third-party (openai, pydantic, rich, fastapi, uvicorn, agents)
  4. First-party (src)
  5. Local folder

- **Example**:
```python
from typing import Optional
import os

from openai import OpenAI
from pydantic import BaseModel
from rich.console import Console

from src.backend.config import Settings
from .utils import helper_function
```

### Code Quality Requirements
- **Pylint Score**: **10.00/10 (PERFECT SCORE - MAINTAINED)**
- **Zero Errors Policy**: No linting errors allowed
- **Zero Warnings Policy**: No linting warnings allowed
- **Type Safety**: Use type hints where applicable

## TypeScript/React Frontend Code Style

### Formatting Standards
- **Linter**: ESLint with TypeScript plugin
- **Formatter**: Prettier
- **Max Warnings**: 150 (configured, but **ZERO WARNINGS ACHIEVED**)
- **File Extensions**: `.tsx` for React components, `.ts` for utilities

### Naming Conventions
- **Components**: `PascalCase` with descriptive suffixes
  - Examples: `ChatInterface_OpenAI`, `ChatInput_OpenAI`, `ChatMessage_OpenAI`
- **Functions/Variables**: `camelCase`
  - Examples: `handleSubmit`, `messageText`, `isLoading`
- **Constants**: `UPPER_SNAKE_CASE` or `camelCase` depending on scope
- **Types/Interfaces**: `PascalCase`
  - Examples: `ChatRequest`, `Message`, `AgentResponse`

### Component Structure
- **Functional Components**: Use React functional components with hooks
- **File Organization**: One component per file
- **Example**:
```typescript
interface ChatMessageProps {
  message: string;
  sender: string;
  timestamp: number;
}

export function ChatMessage_OpenAI({ message, sender, timestamp }: ChatMessageProps) {
  return <div>...</div>;
}
```

### TypeScript Standards
- **Strict Mode**: TypeScript strict mode enabled
- **Type Safety**: Explicit types preferred over `any`
- **ESLint Disable Comments**: Only use when absolutely necessary with proper justification
- **Example of Acceptable `any` Usage**:
```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function createLazyComponent<T extends React.ComponentType<any>>(
  // ... third-party library interface requires any type
)
```

### React Patterns
- **Hooks**: Use React hooks (useState, useEffect, useCallback, useMemo)
- **Props**: Destructure props in function parameters
- **Performance**: Use React.memo for expensive components
- **State Management**: Local state with useState, context for global state

## Project-Specific Conventions

### Model Policy
- **GPT-5-Nano Only**: Project exclusively uses GPT-5-Nano
- **No GPT-5-Mini**: GPT-5-Mini completely removed per project policy
- **Breaking Change**: Recent update enforced GPT-5-Nano-only architecture

### File Naming
- **Backend Python**: `snake_case.py`
  - Examples: `agent_service.py`, `response_utils.py`, `api_models.py`
- **Frontend TypeScript**: `PascalCase.tsx` for components, `camelCase.ts` for utilities
  - Examples: `ChatInterface_OpenAI.tsx`, `config.ts`

### Directory Structure Conventions
- **Backend**:
  - `routers/`: API endpoint routers
  - `services/`: Business logic services
  - `utils/`: Utility functions
  - `api_models.py`: Pydantic models for API schemas
  - `config.py`: Configuration management

- **Frontend**:
  - `components/`: React components
  - `services/`: API services
  - `types/`: TypeScript type definitions
  - `utils/`: Utility functions
  - `config/`: Configuration files
  - `styles/`: CSS styles

### Code Organization
- **Single Responsibility**: Each module/component has one clear purpose
- **DRY Principle**: Avoid code duplication (test_utils.py created to eliminate duplication)
- **Separation of Concerns**: UI logic separate from business logic

### Error Handling
- **Backend**: Use FastAPI HTTPException with appropriate status codes
- **Frontend**: Use ErrorBoundary component for React error handling
- **Logging**: Use Rich console for backend, console methods for frontend

### Testing Conventions
- **Test Files**: Mirror source structure in tests/ directory
- **Test Utilities**: Shared utilities in test_utils.py
- **E2E Tests**: Playwright tests in tests/playwright/
- **Test Reports**: Generated in test-reports/ directory

## Git Commit Conventions

### Commit Message Format
```
[TYPE] Brief description

- Bullet point details
- Additional changes
- Breaking changes noted

BREAKING CHANGE: Description (if applicable)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Commit Types
- `[RE-INIT]`: Complete environment re-initialization
- `[feat]`: New feature
- `[fix]`: Bug fix
- `[refactor]`: Code refactoring
- `[docs]`: Documentation changes
- `[test]`: Test additions/changes
- `[chore]`: Maintenance tasks
- `[SERENA]`: Serena-related changes
- `[AGENTS]`: Agent-related changes
- `[UI]`: UI/Frontend changes
- `[LINT]`: Linting improvements

## Code Review Standards

### Before Committing
1. Run `npm run check:all` - **Must pass with ZERO errors and ZERO warnings**
2. Run `npm run lint` - Must pass with no errors, no warnings
3. Run `npm run type-check` - Must pass TypeScript validation
4. Run `npm run format:check` - Must pass Prettier formatting
5. Run tests if applicable (test_7_prompts_persistent_session.sh)
6. Verify changes don't break existing functionality

### Linting Scores (Current Achievement)
- **Python (Pylint)**: **10.00/10** (perfect score maintained)
- **JavaScript/TypeScript (ESLint)**: **0 errors, 0 warnings** (zero-warning achievement)
- **Prettier**: All files formatted correctly
- **TypeScript Type Check**: No errors

## Performance Considerations

### Frontend Optimization
- **Core Web Vitals**: 85%+ improvement target
- **First Contentful Paint**: ~256ms target
- **Memory Efficiency**: Optimized heap size ~13.8MB
- **Bundle Size**: Monitor with npm run analyze
- **Removed Components** (Oct 2025): ExportButtons, RecentMessageButtons, DebugPanel, exportHelpers (4 files deleted)
- **Consolidated Panels**: Status + Performance combined into single "System Status & Performance" panel

### Backend Optimization
- **Response Times**: Monitor with comprehensive test suite
- **Expected Range**: 10-37s for complex queries (varies with API calls)
- **Health Checks**: Sub-second response on /health endpoint

## Accessibility Standards

- **WCAG 2.1 AA Compliance**: Full compliance required
- **Semantic HTML**: Use proper HTML5 semantic elements
- **ARIA Labels**: Include where necessary for screen readers

## Documentation Standards

- **README.md**: Keep updated with project overview
- **CLAUDE.md**: AI assistant guidance and project rules
- **Code Comments**: Explain complex logic, not obvious code
- **API Documentation**: FastAPI auto-generates at /docs endpoint
- **Serena Memories**: Keep updated after significant changes

## Recent Code Quality Achievements (October 2025)

### UI Refactor
- **Files Removed**: 4 (ExportButtons.tsx, RecentMessageButtons.tsx, DebugPanel.tsx, exportHelpers.ts)
- **Net Code Reduction**: 1,043 lines removed
- **Panels Consolidated**: Status Information + Performance Metrics → Single "System Status & Performance" panel
- **CSS Improvements**: Increased spacing for better visual breathing room (gap values: var(--space-2/4) → 1-2rem)

### Linting Perfection
- **ESLint Warnings**: Reduced from 4 → 0
- **Method**: Added `eslint-disable-next-line` comments only where absolutely necessary
- **Files Affected**: performance.tsx (3 lines), wdyr.ts (1 line)
- **Justification**: Third-party library interfaces (React lazy loading, Why Did You Render)
- **Type Safety**: Fully maintained with explicit type assertions

### Testing Validation
- **Test Suite**: test_7_prompts_persistent_session.sh
- **Success Rate**: 100% (7/7 tests passing)
- **Performance**: EXCELLENT rating (avg 15-21s response times)
- **Session Persistence**: Verified (single session for all tests)