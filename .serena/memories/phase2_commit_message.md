feat: Remove GUI response time features for performance optimization

- Remove processingTime from MessageFormattingOptions and FormattedMessage interfaces
- Remove latestResponseTime from ChatState and responseTime from ChatAction types
- Remove response time calculations and display from ChatInterface component
- Remove response time display from ChatMessage component timestamp area
- Remove processingTime and response_time from MessageMetadata and ResponseMetadata types
- Remove response time CSS classes while preserving message count and status styling
- Update DebugPanel props to remove responseTime parameter
- Maintain full chat functionality without response time overhead

Performance improvements:
- Reduced JavaScript execution time (no response time calculations)
- Simplified state management (removed response time state)
- Cleaner UI (no response time display clutter)
- Improved maintainability (less complex code)

Files modified:
- src/frontend/utils/messageFormatting.ts
- src/frontend/components/ChatInterface_OpenAI.tsx
- src/frontend/components/ChatMessage_OpenAI.tsx
- src/frontend/types/chat_OpenAI.ts
- src/frontend/types/index.ts
- src/frontend/index.css

Phase 2 of CLI/GUI Performance Optimization Implementation Plan completed successfully.