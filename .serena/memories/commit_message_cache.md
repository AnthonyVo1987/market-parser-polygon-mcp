feat: Standardize all AI prompts with new DATA FIRST output format

- Implement standardized output format across all AnalysisIntent prompts
- Add "A. DATA FIRST" section with bullet point format and 2 decimal points max
- Add "B. DETAILED ANALYSIS" section with max 3 key takeaways/insights
- Update SNAPSHOT prompt to focus on STOCK/OPTIONS snapshots specifically
- Update TECHNICAL prompt to include only RSI-14, MACD, EMA 20/50/200, SMA 20/50/200
- Remove redundant analysis descriptions and focus on data-driven responses
- Convert JSON response attributes to user-friendly terms
- Maintain quick response optimization and minimal tool call requirements
- Preserve real-time data access and current date/time context functionality
- Update main.py get_enhanced_agent_instructions() with new standardized format

Improves response consistency and data presentation across all analysis types.