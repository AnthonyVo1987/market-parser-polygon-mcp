feat: Migrate sidebar UI components to bottom panels for full-width chat

- Restructure ChatInterface_OpenAI layout from two-panel grid to full-width main content
- Move all sidebar components (ticker input, analysis buttons, export buttons, debug panel, status info, performance metrics) to bottom control panels
- Eliminate right sidebar panel entirely to give AI chat window full screen width
- Update CSS from grid-template-columns: 1fr 350px to flexbox layout
- Maintain all existing functionality while improving user experience
- Enable vertical scrolling for bottom panels instead of horizontal sidebar
- Preserve responsive design for different screen sizes
- Test all button functionality (Snapshot, Technical, Support/Resistance) - all working correctly
- Test ticker input functionality - working correctly
- Create comprehensive task completion documentation in Serena memory

This change provides users with full-width AI chat interface while keeping all analysis tools accessible via bottom panels that can be scrolled or ignored as needed.