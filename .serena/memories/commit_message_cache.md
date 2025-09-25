feat: Optimize AI prompts for performance and response efficiency

- Remove "Provide data-driven insights with actionable recommendations" from all prompts
- Remove "and specific metrics" requirement from prompt instructions  
- Enforce maximum 3 Key Takeaways in all response formats
- Change Detailed Analysis format to numbered/bullet points only
- Remove all actionable recommendations from response templates
- Update main.py get_enhanced_agent_instructions() with optimized format
- Update direct_prompts.py DirectPromptManager system prompts for all analysis types
- Maintain quick response optimization and minimal tool call requirements
- Preserve real-time data access and current date/time context functionality

Improves response efficiency by reducing verbosity and focusing on data analysis over recommendations.