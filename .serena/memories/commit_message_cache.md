refactor: comprehensive code cleanup and dead code removal

Remove dead code, unused functions, and over-engineered monitoring classes
from the codebase to improve maintainability and performance.

BREAKING CHANGES:
- Removed prompt_templates.py (111 lines of disabled code)
- Removed utils/__init__.py (empty file)
- Removed 4 dead functions from main.py
- Removed 5 unused classes and variables
- Removed 4 over-engineered monitoring classes

Changes:
- Cleaned up empty pass statements and removed code comments
- Fixed ESLint warnings in frontend TypeScript files
- Resolved Python linting issues (9.95/10 rating)
- Verified CLI and GUI functionality with comprehensive testing
- Updated project memories with completion report

Files modified:
- src/backend/main.py: Major cleanup of dead code
- src/backend/api_models.py: Removed unused classes
- src/frontend/main.tsx: Fixed linting issues
- src/frontend/wdyr.ts: Fixed linting issues
- TODO_task_plan.md: Created implementation plan

Files removed:
- src/backend/prompt_templates.py
- src/backend/utils/__init__.py

Impact:
- ~500-600 lines of dead code removed
- Code quality rating: 9.95/10
- Both CLI and GUI versions tested and working
- All linting issues resolved
- Significantly improved maintainability

Closes: Code cleanup and optimization tasks