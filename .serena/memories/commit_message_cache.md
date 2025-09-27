feat: Remove UI Quick Analysis Button Prompts and User Input ticker functionality

- Remove ticker input box and all related code from ChatInterface_OpenAI.tsx
- Remove 3x analysis buttons (Snapshot, Support/Resistance, Technical Analysis) and all related code
- Delete AnalysisButtons.tsx and SharedTickerInput.tsx component files
- Remove related type definitions (AnalysisButtonType, AnalysisButtonProps, TickerInputProps, ButtonState)
- Clean up ticker-related placeholder text utilities
- Update welcome message to reflect streamlined interface
- Consolidate prompts to single source of truth in main.py (get_enhanced_agent_instructions function)
- GUI user AI chat input now inherits prompt from CLI backend main.py
- Eliminate duplicate redundant prompts for CLI vs GUI user input
- Streamline app with less complex AI Chatbot functionality
- Update README.md to reflect new streamlined interface
- Delete obsolete user-guide-analysis-buttons.md documentation
- Test UI changes with Playwright - all functionality working correctly
- Verify chat interface works properly without ticker/analysis buttons
- Fix import cleanup in ChatInterface_OpenAI.tsx (remove useDeferredValue, fix trailing comma)

This change simplifies the user experience by removing redundant UI elements and consolidating all prompts to a single source of truth in the backend, making the app more maintainable and consistent.