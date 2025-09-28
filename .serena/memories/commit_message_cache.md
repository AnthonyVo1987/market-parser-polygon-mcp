feat: implement comprehensive codebase refactoring and GUI response time fix

- **Dead Code Cleanup**: Remove unused comments, empty blocks, and dead code from main.py
- **Agent Creation Factory**: Extract duplicate agent creation logic into reusable create_agent() function
- **Configuration Consolidation**: Merge EnvironmentSettings, ConfigSettings, and Settings into single consolidated class
- **CSS Optimization**: Remove performance-related comments and optimize frontend styles
- **Response Time Bug Fix**: Fix GUI footer not displaying response time by resolving field name mismatch between backend (snake_case) and frontend (camelCase)
- **API Model Enhancement**: Add field aliases to ResponseMetadata for backward compatibility
- **Testing Completion**: Achieve 100% CLI test success rate and verify GUI functionality
- **Documentation**: Create comprehensive TODO_task_plan.md with implementation details

**Technical Changes:**
- src/backend/main.py: Consolidated config, added timing, extracted agent factory
- src/backend/api_models.py: Added field aliases for camelCase compatibility  
- src/frontend/index.css: Removed performance comments, optimized styles
- TODO_task_plan.md: Created detailed implementation plan

**Testing Results:**
- CLI: 7/7 tests passed (100% success rate)
- GUI: Response time display fixed, all functionality verified
- Linting: 9.91/10 score maintained