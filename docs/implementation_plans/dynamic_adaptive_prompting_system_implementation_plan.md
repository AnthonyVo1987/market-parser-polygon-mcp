# Dynamic Adaptive Prompting System - Implementation Plan

**Date**: September 26, 2025  
**Project**: Market Parser Polygon MCP  
**Feature**: Dynamic Adaptive Prompting System for CLI and GUI  
**Status**: Ready for Implementation

## Executive Summary

This document provides a comprehensive implementation plan for creating a dynamic and adaptive prompting system that allows users to customize their AI interactions without requiring code changes. The system will replace the current rigid prompt structure with a flexible, user-customizable approach while maintaining the core functionality of financial analysis.

## Current System Analysis

### Existing Architecture

- **CLI System**: Uses `get_enhanced_agent_instructions()` for generic prompts
- **GUI System**: Inherits CLI system prompts for user input
- **Button Prompts**: Uses `DirectPromptManager` with predefined analysis intents (SNAPSHOT, SUPPORT_RESISTANCE, TECHNICAL, GENERAL, MARKET_STATUS)
- **System Prompts**: Static, hardcoded instructions with fixed verbosity and tool usage patterns

### Key Requirements

1. **Unified System Prompts**: Make CLI and GUI system prompts identical
2. **Dynamic Adaptation**: Allow user customization of verbosity, tool usage, output format
3. **Preserve Button Functionality**: Keep existing button prompts unchanged
4. **User Override Support**: Enable users to specify preferences in their input
5. **Fallback Mechanisms**: Ensure system works when no user preferences are provided

## Implementation Plan

### Phase 1: System Architecture Design (Days 1-2)

#### Task 1.1: Unified System Prompt Architecture

- [ ] **1.1.1** Create new `DynamicPromptManager` class to replace current prompt system
- [ ] **1.1.2** Design base system prompt template with placeholder sections for customization
- [ ] **1.1.3** Define user override instruction parsing patterns (verbosity, tools, format, etc.)
- [ ] **1.1.4** Create prompt assembly logic to combine base prompt with user preferences
- [ ] **1.1.5** Implement fallback mechanism for when no user preferences are provided

#### Task 1.2: Integration with Existing Architecture

- [ ] **1.2.1** Analyze current `get_enhanced_agent_instructions()` function usage
- [ ] **1.2.2** Design integration points with existing `DirectPromptManager`
- [ ] **1.2.3** Create compatibility layer to ensure seamless transition
- [ ] **1.2.4** Plan migration strategy for existing prompt calls
- [ ] **1.2.5** Design testing framework for integration validation

#### Task 1.3: User Preference System

- [ ] **1.3.1** Design user preference data structure (verbosity, tool_usage, output_format, etc.)
- [ ] **1.3.2** Create preference parsing logic from user input
- [ ] **1.3.3** Implement preference validation and sanitization
- [ ] **1.3.4** Design preference persistence mechanism (optional)
- [ ] **1.3.5** Create preference inheritance system (session-level defaults)

### Phase 2: Core Implementation (Days 3-5)

#### Task 2.1: DynamicPromptManager Implementation

- [ ] **2.1.1** Implement base `DynamicPromptManager` class structure
- [ ] **2.1.2** Create prompt template system with variable substitution
- [ ] **2.1.3** Implement user instruction parsing and validation
- [ ] **2.1.4** Add prompt assembly and optimization logic
- [ ] **2.1.5** Implement error handling and fallback mechanisms

#### Task 2.2: User Instruction Parser

- [ ] **2.2.1** Create regex patterns for common user instruction formats
- [ ] **2.2.2** Implement instruction validation and sanitization
- [ ] **2.2.3** Add support for multiple instruction formats
- [ ] **2.2.4** Create instruction conflict resolution logic
- [ ] **2.2.5** Implement instruction precedence rules

#### Task 2.3: Prompt Template System

- [ ] **2.3.1** Design modular prompt template structure
- [ ] **2.3.2** Create template variable substitution system
- [ ] **2.3.3** Implement template inheritance and composition
- [ ] **2.3.4** Add template validation and error checking
- [ ] **2.3.5** Create template versioning and migration support

### Phase 3: Integration and Testing (Days 6-8)

#### Task 3.1: CLI Integration

- [ ] **3.1.1** Modify CLI prompt generation to use `DynamicPromptManager`
- [ ] **3.1.2** Update CLI user input processing to extract preferences
- [ ] **3.1.3** Implement CLI-specific prompt customization
- [ ] **3.1.4** Add CLI error handling and user feedback
- [ ] **3.1.5** Test CLI functionality with various user inputs

#### Task 3.2: GUI Integration

- [ ] **3.2.1** Modify GUI prompt generation to use `DynamicPromptManager`
- [ ] **3.2.2** Update GUI user input processing to extract preferences
- [ ] **3.2.3** Implement GUI-specific prompt customization
- [ ] **3.2.4** Add GUI error handling and user feedback
- [ ] **3.2.5** Test GUI functionality with various user inputs

#### Task 3.3: Button Prompt Preservation

- [ ] **3.3.1** Verify existing button prompts remain unchanged
- [ ] **3.3.2** Test button prompt functionality with new system
- [ ] **3.3.3** Ensure button prompts don't interfere with dynamic system
- [ ] **3.3.4** Add button prompt integration tests
- [ ] **3.3.5** Validate button prompt performance

### Phase 4: Advanced Features (Days 9-10)

#### Task 4.1: Advanced User Customization

- [ ] **4.1.1** Implement advanced verbosity controls (minimal, standard, detailed)
- [ ] **4.1.2** Add tool usage customization (specific tools, tool limits)
- [ ] **4.1.3** Create output format customization (structured, narrative, hybrid)
- [ ] **4.1.4** Implement response style customization (formal, casual, technical)
- [ ] **4.1.5** Add domain-specific customization options

#### Task 4.2: Performance Optimization

- [ ] **4.2.1** Implement prompt caching for common configurations
- [ ] **4.2.2** Add prompt optimization for token efficiency
- [ ] **4.2.3** Create performance monitoring for prompt generation
- [ ] **4.2.4** Implement lazy loading for prompt components
- [ ] **4.2.5** Add performance benchmarking and optimization

#### Task 4.3: Error Handling and Resilience

- [ ] **4.3.1** Implement comprehensive error handling for malformed instructions
- [ ] **4.3.2** Add graceful degradation when customization fails
- [ ] **4.3.3** Create error recovery mechanisms
- [ ] **4.3.4** Implement logging and monitoring for prompt issues
- [ ] **4.3.5** Add user-friendly error messages and suggestions

### Phase 5: Security and Validation (Days 11-12)

#### Task 5.1: Security Implementation

- [ ] **5.1.1** Implement input sanitization for user instructions
- [ ] **5.1.2** Add instruction validation to prevent prompt injection
- [ ] **5.1.3** Create security boundaries for user customization
- [ ] **5.1.4** Implement rate limiting for prompt generation
- [ ] **5.1.5** Add security logging and monitoring

#### Task 5.2: Input Validation

- [ ] **5.2.1** Create comprehensive input validation rules
- [ ] **5.2.2** Implement instruction format validation
- [ ] **5.2.3** Add content filtering for inappropriate instructions
- [ ] **5.2.4** Create validation error handling and user feedback
- [ ] **5.2.5** Implement validation performance optimization

#### Task 5.3: System Resilience

- [ ] **5.3.1** Implement fault tolerance for prompt generation failures
- [ ] **5.3.2** Add system resilience for external dependency failures
- [ ] **5.3.3** Create recovery mechanisms for system failures
- [ ] **5.3.4** Implement health checks and monitoring
- [ ] **5.3.5** Add automated recovery and restart capabilities

### Phase 6: Testing and Validation (Days 13-15)

#### Task 6.1: Unit Testing

- [ ] **6.1.1** Create unit tests for `DynamicPromptManager` class
- [ ] **6.1.2** Add unit tests for user instruction parsing
- [ ] **6.1.3** Implement unit tests for prompt template system
- [ ] **6.1.4** Create unit tests for error handling
- [ ] **6.1.5** Add unit tests for security features

#### Task 6.2: Integration Testing

- [ ] **6.2.1** Test CLI integration with dynamic prompting
- [ ] **6.2.2** Test GUI integration with dynamic prompting
- [ ] **6.2.3** Validate button prompt preservation
- [ ] **6.2.4** Test system resilience and error handling
- [ ] **6.2.5** Validate performance under load

#### Task 6.3: User Acceptance Testing

- [ ] **6.3.1** Test various user instruction formats
- [ ] **6.3.2** Validate user customization options
- [ ] **6.3.3** Test error handling and user feedback
- [ ] **6.3.4** Validate system performance and responsiveness
- [ ] **6.3.5** Test edge cases and boundary conditions

### Phase 7: Documentation and Deployment (Days 16-17)

#### Task 7.1: Documentation

- [ ] **7.1.1** Create user documentation for dynamic prompting features
- [ ] **7.1.2** Add developer documentation for system architecture
- [ ] **7.1.3** Create API documentation for new components
- [ ] **7.1.4** Add troubleshooting guide and FAQ
- [ ] **7.1.5** Create migration guide for existing users

#### Task 7.2: Deployment Preparation

- [ ] **7.2.1** Create deployment scripts and procedures
- [ ] **7.2.2** Implement configuration management for new features
- [ ] **7.2.3** Add monitoring and logging for production
- [ ] **7.2.4** Create rollback procedures and recovery plans
- [ ] **7.2.5** Validate deployment in staging environment

#### Task 7.3: Production Deployment

- [ ] **7.3.1** Deploy to production environment
- [ ] **7.3.2** Monitor system performance and stability
- [ ] **7.3.3** Validate all functionality in production
- [ ] **7.3.4** Collect user feedback and performance metrics
- [ ] **7.3.5** Document lessons learned and improvements

## Technical Specifications

### DynamicPromptManager Class Structure

```python
class DynamicPromptManager:
    def __init__(self, base_template: str, config: Dict[str, Any]):
        self.base_template = base_template
        self.config = config
        self.instruction_parser = InstructionParser()
        self.template_engine = TemplateEngine()
        self.cache = PromptCache(max_size=config.get('cache_size', 100))
        self.validator = InputValidator(config.get('security_rules', {}))
    
    def generate_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        try:
            # Parse user instructions
            preferences = self.parse_user_instructions(user_input)
            
            # Validate preferences
            self.validator.validate_preferences(preferences)
            
            # Apply customizations to template
            customized_prompt = self.template_engine.apply_preferences(
                self.base_template, preferences, context
            )
            
            # Cache result for performance
            self.cache.store(user_input, customized_prompt)
            
            return customized_prompt
        except ValidationError as e:
            return self._handle_validation_error(e, user_input)
        except TemplateError as e:
            return self._handle_template_error(e, user_input)
        except Exception as e:
            return self._handle_general_error(e, user_input)
    
    def parse_user_instructions(self, user_input: str) -> UserPreferences:
        # Extract and validate user preferences
        raw_preferences = self.instruction_parser.extract_preferences(user_input)
        return self.validator.sanitize_preferences(raw_preferences)
    
    def _handle_validation_error(self, error: ValidationError, user_input: str) -> str:
        # Log error and return fallback prompt
        logger.warning(f"Validation error for input: {user_input[:50]}... Error: {error}")
        return self._get_fallback_prompt()
    
    def _handle_template_error(self, error: TemplateError, user_input: str) -> str:
        # Log error and return fallback prompt
        logger.error(f"Template error for input: {user_input[:50]}... Error: {error}")
        return self._get_fallback_prompt()
    
    def _handle_general_error(self, error: Exception, user_input: str) -> str:
        # Log error and return fallback prompt
        logger.error(f"Unexpected error for input: {user_input[:50]}... Error: {error}")
        return self._get_fallback_prompt()
    
    def _get_fallback_prompt(self) -> str:
        # Return base template without customizations
        return self.base_template

class InstructionParser:
    def __init__(self):
        self.patterns = {
            'verbosity': r'\[(verbose|minimal|standard|detailed|brief|concise)\]',
            'tool_usage': r'\[(use only|avoid|minimal tools?)\s+([a-zA-Z_\s,]+)\]',
            'output_format': r'\[(structured|narrative|bullet points?|JSON|markdown|plain)\]',
            'response_style': r'\[(formal|casual|technical|professional|friendly)\]'
        }
    
    def extract_preferences(self, user_input: str) -> Dict[str, Any]:
        preferences = {}
        for key, pattern in self.patterns.items():
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            if matches:
                preferences[key] = matches[0] if isinstance(matches[0], str) else matches[0][1]
        return preferences

class TemplateEngine:
    def __init__(self):
        self.template_vars = {
            'verbosity': self._get_verbosity_template,
            'tool_usage': self._get_tool_usage_template,
            'output_format': self._get_output_format_template,
            'response_style': self._get_response_style_template
        }
    
    def apply_preferences(self, base_template: str, preferences: Dict[str, Any], context: Dict[str, Any]) -> str:
        template = base_template
        for key, value in preferences.items():
            if key in self.template_vars:
                template = self.template_vars[key](template, value, context)
        return template
    
    def _get_verbosity_template(self, template: str, verbosity: str, context: Dict[str, Any]) -> str:
        verbosity_instructions = {
            'minimal': 'Provide only essential information with minimal explanation.',
            'standard': 'Provide balanced information with moderate detail.',
            'verbose': 'Provide comprehensive information with detailed explanations.',
            'detailed': 'Provide thorough analysis with extensive detail.',
            'brief': 'Provide concise information with brief explanations.',
            'concise': 'Provide essential information in the most concise format possible.'
        }
        return template.replace('{verbosity_instruction}', verbosity_instructions.get(verbosity, verbosity_instructions['standard']))
    
    def _get_tool_usage_template(self, template: str, tool_usage: str, context: Dict[str, Any]) -> str:
        if 'use only' in tool_usage.lower():
            tools = tool_usage.lower().replace('use only', '').strip()
            return template.replace('{tool_restriction}', f'Use only the following tools: {tools}')
        elif 'avoid' in tool_usage.lower():
            tools = tool_usage.lower().replace('avoid', '').strip()
            return template.replace('{tool_restriction}', f'Avoid using the following tools: {tools}')
        elif 'minimal' in tool_usage.lower():
            return template.replace('{tool_restriction}', 'Use the minimum number of tools necessary to complete the task')
        return template
    
    def _get_output_format_template(self, template: str, output_format: str, context: Dict[str, Any]) -> str:
        format_instructions = {
            'structured': 'Format your response in a structured format with clear sections and bullet points.',
            'narrative': 'Format your response as a flowing narrative with clear paragraphs.',
            'bullet points': 'Format your response using bullet points for easy reading.',
            'json': 'Format your response as valid JSON when appropriate.',
            'markdown': 'Format your response using Markdown formatting.',
            'plain': 'Format your response in plain text without special formatting.'
        }
        return template.replace('{format_instruction}', format_instructions.get(output_format, format_instructions['structured']))
    
    def _get_response_style_template(self, template: str, response_style: str, context: Dict[str, Any]) -> str:
        style_instructions = {
            'formal': 'Use a formal, professional tone in your response.',
            'casual': 'Use a casual, friendly tone in your response.',
            'technical': 'Use a technical, precise tone with appropriate terminology.',
            'professional': 'Use a professional, business-appropriate tone.',
            'friendly': 'Use a warm, approachable tone in your response.'
        }
        return template.replace('{style_instruction}', style_instructions.get(response_style, style_instructions['professional']))

class InputValidator:
    def __init__(self, security_rules: Dict[str, Any]):
        self.security_rules = security_rules
        self.allowed_verbs = ['verbose', 'minimal', 'standard', 'detailed', 'brief', 'concise']
        self.allowed_tools = ['get_snapshot_ticker', 'get_market_status', 'get_full_market_snapshot', 'get_support_resistance_levels', 'get_technical_analysis']
        self.allowed_formats = ['structured', 'narrative', 'bullet points', 'json', 'markdown', 'plain']
        self.allowed_styles = ['formal', 'casual', 'technical', 'professional', 'friendly']
    
    def validate_preferences(self, preferences: Dict[str, Any]) -> None:
        for key, value in preferences.items():
            if key == 'verbosity' and value not in self.allowed_verbs:
                raise ValidationError(f"Invalid verbosity level: {value}")
            elif key == 'tool_usage' and not self._validate_tool_usage(value):
                raise ValidationError(f"Invalid tool usage instruction: {value}")
            elif key == 'output_format' and value not in self.allowed_formats:
                raise ValidationError(f"Invalid output format: {value}")
            elif key == 'response_style' and value not in self.allowed_styles:
                raise ValidationError(f"Invalid response style: {value}")
    
    def _validate_tool_usage(self, tool_usage: str) -> bool:
        # Check if tool usage instruction contains only allowed tools
        if 'use only' in tool_usage.lower():
            tools = tool_usage.lower().replace('use only', '').strip().split(',')
            return all(tool.strip() in self.allowed_tools for tool in tools)
        elif 'avoid' in tool_usage.lower():
            tools = tool_usage.lower().replace('avoid', '').strip().split(',')
            return all(tool.strip() in self.allowed_tools for tool in tools)
        return True
    
    def sanitize_preferences(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = {}
        for key, value in preferences.items():
            if isinstance(value, str):
                # Remove potentially dangerous characters
                sanitized[key] = re.sub(r'[<>"\']', '', value).strip()
            else:
                sanitized[key] = value
        return sanitized

class PromptCache:
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}
    
    def store(self, key: str, value: str) -> None:
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = value
        self.access_times[key] = time.time()
    
    def get(self, key: str) -> Optional[str]:
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None
    
    def _evict_oldest(self) -> None:
        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        del self.cache[oldest_key]
        del self.access_times[oldest_key]
```

### User Instruction Patterns

- **Verbosity**: `[verbose|minimal|standard]`, `[detailed|brief|concise]`
- **Tool Usage**: `[use only X tool]`, `[avoid Y tool]`, `[minimal tools]`
- **Output Format**: `[structured|narrative|bullet points]`, `[JSON|markdown|plain]`
- **Response Style**: `[formal|casual|technical]`, `[professional|friendly]`

### Configuration Options

```json
{
  "dynamic_prompting": {
    "enabled": true,
    "default_verbosity": "standard",
    "max_customization_depth": 3,
    "allow_tool_restrictions": true,
    "security_validation": true
  }
}
```

## Security Specifications

### Input Validation Requirements

- **Pattern Validation**: All user instructions must match predefined regex patterns
- **Whitelist Approach**: Only allow predefined verbosity levels, tools, formats, and styles
- **Character Filtering**: Remove potentially dangerous characters (<, >, ", ', script tags)
- **Length Limits**: Maximum 1000 characters per user instruction
- **Rate Limiting**: Maximum 10 customization attempts per minute per user

### Prompt Injection Prevention

- **Instruction Isolation**: User instructions are parsed and applied separately from main prompt
- **Template Sanitization**: All template variables are sanitized before substitution
- **Context Separation**: User preferences are isolated from system context
- **Validation Layers**: Multiple validation layers prevent malicious input propagation

### Security Monitoring

- **Input Logging**: Log all user instructions for security analysis
- **Anomaly Detection**: Monitor for unusual instruction patterns
- **Error Tracking**: Track validation failures and security violations
- **Audit Trail**: Maintain complete audit trail of all prompt customizations

## Risk Assessment and Mitigation

### High-Risk Areas

1. **Prompt Injection Security**: Implement comprehensive input validation
2. **Performance Impact**: Add caching and optimization mechanisms
3. **System Complexity**: Maintain clear separation of concerns
4. **User Experience**: Provide clear error messages and fallbacks

### Mitigation Strategies

1. **Security**: Multi-layer validation, sanitization, and monitoring
2. **Performance**: Caching, lazy loading, and performance monitoring
3. **Complexity**: Modular design, comprehensive testing, and documentation
4. **UX**: User-friendly error handling and clear feedback mechanisms

## Success Criteria

### Functional Requirements

- [ ] CLI and GUI use identical system prompts
- [ ] Users can customize verbosity, tool usage, and output format
- [ ] Button prompts remain unchanged and functional
- [ ] System gracefully handles malformed user instructions
- [ ] Performance impact is minimal (<5% overhead)

### Non-Functional Requirements

- [ ] System maintains security boundaries
- [ ] Error handling is comprehensive and user-friendly
- [ ] Documentation is complete and accurate
- [ ] Testing coverage is >90%
- [ ] Deployment is smooth and reversible

## Performance Benchmarks

### Response Time Targets

- **Prompt Generation**: <100ms for standard prompts, <200ms for complex customizations
- **Cache Hit Rate**: >80% for repeated user preferences
- **Memory Usage**: <50MB additional overhead for dynamic prompting system
- **CPU Usage**: <5% additional overhead during prompt generation

### Load Testing Criteria

- **Concurrent Users**: Support 100+ concurrent users without degradation
- **Request Rate**: Handle 1000+ requests per minute
- **Error Rate**: <0.1% error rate under normal load
- **Recovery Time**: <30 seconds for system recovery after failures

### Security Performance

- **Input Validation**: <10ms per validation check
- **Sanitization**: <5ms per input sanitization
- **Security Logging**: <1ms per security event log

## Testing Specifications

### Unit Testing Requirements

```python
# Example test cases for DynamicPromptManager
def test_verbosity_customization():
    manager = DynamicPromptManager(base_template, config)
    user_input = "Current market status [minimal]"
    result = manager.generate_prompt(user_input, {})
    assert "minimal explanation" in result

def test_tool_restriction():
    manager = DynamicPromptManager(base_template, config)
    user_input = "NVDA analysis [use only get_snapshot_ticker]"
    result = manager.generate_prompt(user_input, {})
    assert "Use only the following tools: get_snapshot_ticker" in result

def test_invalid_instruction_handling():
    manager = DynamicPromptManager(base_template, config)
    user_input = "Market status [invalid_verbosity]"
    result = manager.generate_prompt(user_input, {})
    assert result == manager.base_template  # Should fallback to base template

def test_security_validation():
    manager = DynamicPromptManager(base_template, config)
    user_input = "Market status [<script>alert('xss')</script>]"
    result = manager.generate_prompt(user_input, {})
    assert "<script>" not in result  # Should be sanitized
```

### Integration Testing Requirements

- **CLI Integration**: Test prompt generation with actual CLI user inputs
- **GUI Integration**: Test prompt generation with actual GUI user inputs
- **Button Prompt Preservation**: Verify existing button prompts remain unchanged
- **Error Handling**: Test system behavior under various error conditions
- **Performance**: Test system performance under load

### User Acceptance Testing Requirements

- **User Instruction Formats**: Test various user instruction formats
- **Customization Options**: Validate all user customization options work correctly
- **Error Messages**: Test user-friendly error messages and suggestions
- **Performance**: Validate system performance meets user expectations
- **Edge Cases**: Test boundary conditions and edge cases

### Security Testing Requirements

- **Input Validation**: Test input validation with malicious inputs
- **Prompt Injection**: Test resistance to prompt injection attacks
- **Rate Limiting**: Test rate limiting functionality
- **Access Control**: Test security boundaries and access controls
- **Logging**: Test security logging and monitoring

## Timeline Summary

- **Phase 1-2**: Architecture and Core Implementation (5 days)
- **Phase 3**: Integration and Testing (3 days)
- **Phase 4**: Advanced Features (2 days)
- **Phase 5**: Security and Validation (2 days)
- **Phase 6**: Testing and Validation (3 days)
- **Phase 7**: Documentation and Deployment (2 days)

**Total Estimated Duration**: 17 days

## Dependencies

### External Dependencies

- OpenAI Agents SDK (existing)
- Polygon MCP Server (existing)
- FastAPI and React (existing)

### Internal Dependencies

- Current prompt system architecture
- Existing button prompt functionality
- Configuration management system
- Testing framework

## Conclusion

This implementation plan provides a comprehensive roadmap for creating a dynamic and adaptive prompting system that enhances user experience while maintaining system security and performance. The phased approach ensures thorough testing and validation at each stage, minimizing risks and ensuring successful deployment.

The system will provide users with unprecedented control over their AI interactions while maintaining the robust functionality and security of the existing Market Parser application.
