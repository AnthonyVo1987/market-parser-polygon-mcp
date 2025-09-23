feat: Remove button validation system for performance optimization

- Remove validation system from SharedTickerInput component
- Remove validation system from ChatInput_OpenAI component  
- Delete validation utility files (validation.ts, useInputValidation.ts)
- Replace validation-based input handling with simple state management
- Remove validation error displays and validation-based CSS classes
- Remove validation-based ARIA attributes and accessibility features
- Maintain full input functionality without validation overhead
- Simplify component logic and reduce complexity

Performance improvements:
- Reduced JavaScript execution time (no validation calculations)
- Simplified state management (removed validation state)
- Cleaner component logic (less complex validation handling)
- Improved maintainability (removed validation dependencies)
- Faster input responsiveness (no validation checks on every keystroke)

Files modified:
- src/frontend/components/SharedTickerInput.tsx
- src/frontend/components/ChatInput_OpenAI.tsx

Files deleted:
- src/frontend/utils/validation.ts
- src/frontend/hooks/useInputValidation.ts

Phase 3 of CLI/GUI Performance Optimization Implementation Plan completed successfully.