# Testing Procedures Updated - January 9, 2025

## Testing Status: ✅ UPDATED FOR GPT-5 OPTIMIZATION

### Updated Test Prompts

#### Standardized Test Prompts (v2.0)
All test prompts now include "Quick Response Needed with minimal tool calls" prefix:

1. **Market Status**: "Quick Response Needed with minimal tool calls: What is the current Market Status?"
2. **Single Stock Snapshot**: "Quick Response Needed with minimal tool calls: Based on Market Status Date, Single Stock Snapshot NVDA"
3. **Full Market Snapshot**: "Quick Response Needed with minimal tool calls: Based on Market Status Date, Full Market Snapshot: SPY, QQQ, IWM"
4. **Closing Price**: "Quick Response Needed with minimal tool calls: Based on Market Status Date, what was the closing price of GME today?"
5. **Performance Analysis**: "Quick Response Needed with minimal tool calls: Based on Market Status Date, how is SOUN performance doing this week?"
6. **Support & Resistance**: "Quick Response Needed with minimal tool calls: Based on Market Status Date, Support & Resistance Levels NVDA"
7. **Technical Analysis**: "Quick Response Needed with minimal tool calls: Based on Market Status Date, Technical Analysis SPY"
8. **Top Gainers**: "Quick Response Needed with minimal tool calls: Based on Market Status Date, Top Market Movers Today for Gainers"
9. **Top Losers**: "Quick Response Needed with minimal tool calls: Based on Market Status Date, Top Market Movers Today for Losers"

### Updated Performance Expectations

#### Response Time Expectations
- **Previous**: 30-60 seconds
- **Current**: 20-45 seconds (improved with GPT-5 optimization)
- **Target**: < 30 seconds for excellent performance

#### Performance Classification
- **SUCCESS**: < 30 seconds (excellent performance with GPT-5 optimization)
- **GOOD**: 30-45 seconds (good performance, within expected range)
- **SLOW_PERFORMANCE**: 45-90 seconds (acceptable but investigate optimization)
- **TIMEOUT**: > 90 seconds (failure - investigate GPT-5 configuration)

### Testing Guidelines

#### For AI Agents
1. **Read test_prompts.md first** before any testing
2. **Select appropriate prompt** based on test requirements
3. **Copy prompt exactly** as written (includes "Quick Response Needed" prefix)
4. **Expect 20-45 second response time** (improved with GPT-5 optimization)
5. **Report actual response time** for performance classification
6. **Verify quick response optimization** is working correctly

#### For Test Documentation
1. **Reference test_prompts.md** in all test guides
2. **Include individual prompts** for quick reference
3. **Link to test_prompts.md** for comprehensive prompt list
4. **Update test_prompts.md** if prompts need modification

### GPT-5 Model Testing

#### Model Configuration Testing
- **Verify GPT-5 Models**: Confirm only GPT-5 Nano and Mini are available
- **Rate Limiting**: Test model-specific rate limits (200K TPM nano, 500K TPM mini)
- **Model Selection**: Verify proper model specification in Agent instances
- **Error Handling**: Test rate limiting error prevention

#### Quick Response Optimization Testing
- **Prompt Prefix**: Verify "Quick Response Needed" prefix in all responses
- **Response Speed**: Measure actual response times (target < 30 seconds)
- **Tool Call Efficiency**: Verify minimal tool calls for faster responses
- **Consistency**: Test across chatbot and button interfaces

### Performance Testing

#### Response Time Testing
- **Baseline**: Measure current response times
- **Target**: < 30 seconds for excellent performance
- **Monitoring**: Track response time improvements
- **Validation**: Verify 20-40% improvement over previous implementation

#### Rate Limiting Testing
- **Error Prevention**: Verify no "Request too large for gpt-4o" errors
- **Model Limits**: Test GPT-5 model-specific rate limits
- **Throughput**: Verify 6-16x higher throughput capacity
- **Stability**: Test system stability under high load

### Integration Testing

#### API Testing
- **Model Specification**: Verify proper model parameter in Agent instances
- **Rate Limiting**: Test model-specific rate limiting functionality
- **Configuration**: Validate GPT-5 configuration loading
- **Error Handling**: Test enhanced error handling and validation

#### Frontend Testing
- **Button Interface**: Test quick response optimization in button interactions
- **Chatbot Interface**: Test quick response optimization in chatbot
- **Performance**: Verify UI performance improvements maintained
- **User Experience**: Test enhanced user experience with faster responses

### Test Documentation

#### Updated Files
- **tests/playwright/test_prompts.md**: Updated with quick response optimization
- **README.md**: Updated test prompt references
- **API Integration Guide**: Updated testing procedures
- **Performance Guide**: Updated performance testing guidelines

#### Test Procedures
- **Standardized Prompts**: Use only updated test prompts
- **Performance Monitoring**: Track response times and improvements
- **Model Validation**: Verify GPT-5 model configuration
- **Optimization Verification**: Confirm quick response optimization working

### Quality Assurance

#### Test Validation
- **Response Time**: Verify 20-40% improvement in response times
- **Rate Limiting**: Confirm elimination of rate limiting errors
- **Model Usage**: Validate proper GPT-5 model usage
- **System Performance**: Confirm overall performance improvements

#### Regression Testing
- **UI Performance**: Verify 85%+ Core Web Vitals improvement maintained
- **Memory Usage**: Confirm 13.8MB heap size optimization preserved
- **Load Performance**: Verify 256ms First Contentful Paint maintained
- **Functionality**: Confirm all existing functionality preserved