# Standardized Test Prompts System - Updated 2025-01-09

## System Overview

**Purpose**: Ensure consistent, reliable testing with quick response times
**Response Time**: 30-60 seconds per test
**Usage**: Regression testing, validation, and quality assurance
**Status**: ✅ Fully implemented and documented

## Core Test Prompts (9 Total)

### 1. Market Status Check

**Prompt**: "What is the current Market Status?"
**Purpose**: Verify overall market data access and system health
**Expected Response**: Current market status, trading hours, key indices
**Performance**: Quick response (30-60 seconds)

### 2. Single Stock Snapshot

**Prompt**: "Based on Market Status Date, Single Stock Snapshot NVDA"
**Purpose**: Test individual stock data retrieval and analysis
**Expected Response**: NVDA stock data, price, volume, analysis
**Performance**: Quick response (30-60 seconds)

### 3. Full Market Snapshot

**Prompt**: "Based on Market Status Date, Full Market Snapshot: SPY, QQQ, IWM"
**Purpose**: Test multiple stock analysis and market overview
**Expected Response**: SPY, QQQ, IWM data with comparative analysis
**Performance**: Quick response (30-60 seconds)

### 4. Closing Price Query

**Prompt**: "Based on Market Status Date, what was the closing price of GME today?"
**Purpose**: Test specific price data retrieval
**Expected Response**: GME closing price and related data
**Performance**: Quick response (30-60 seconds)

### 5. Performance Analysis

**Prompt**: "Based on Market Status Date, how is SOUN performance doing this week?"
**Purpose**: Test performance analysis and trend evaluation
**Expected Response**: SOUN weekly performance analysis
**Performance**: Quick response (30-60 seconds)

### 6. Top Gainers

**Prompt**: "Based on Market Status Date, Top Market Movers Today for Gainers"
**Purpose**: Test market movers data and analysis
**Expected Response**: List of top gaining stocks with analysis
**Performance**: Quick response (30-60 seconds)

### 7. Top Losers

**Prompt**: "Based on Market Status Date, Top Market Movers Today for Losers"
**Purpose**: Test market movers data for declining stocks
**Expected Response**: List of top losing stocks with analysis
**Performance**: Quick response (30-60 seconds)

### 8. Support & Resistance

**Prompt**: "Based on Market Status Date, Support & Resistance Levels NVDA"
**Purpose**: Test technical analysis capabilities
**Expected Response**: NVDA support and resistance levels
**Performance**: Quick response (30-60 seconds)

### 9. Technical Analysis

**Prompt**: "Based on Market Status Date, Technical Analysis SPY"
**Purpose**: Test comprehensive technical analysis
**Expected Response**: SPY technical analysis with indicators
**Performance**: Quick response (30-60 seconds)

## Usage Guidelines

### Mandatory Rules

- ✅ Use ONLY these prompts for testing
- ✅ Copy prompts EXACTLY as written
- ✅ Expected response time: 30-60 seconds
- ❌ DO NOT create custom prompts
- ❌ DO NOT modify these prompts
- ❌ DO NOT use complex, open-ended queries

### Performance Classification

- **Quick Response**: 30-60 seconds
- **Minimal Tool Usage**: Efficient processing
- **Consistent Results**: Standardized format
- **Reliable Testing**: No false failures

### Integration Notes

- **CLI Testing**: Use with `uv run src/backend/main.py`
- **API Testing**: Use with chat endpoint
- **Frontend Testing**: Use with React interface
- **Documentation**: Reference `tests/playwright/test_prompts.md`

## Implementation Details

### File Locations

- **Main Documentation**: `tests/playwright/test_prompts.md`
- **CLAUDE.md**: Updated with test prompts
- **AGENTS.md**: Updated with test prompts
- **README.md**: Updated with test prompts
- **Test Guides**: All test execution guides updated

### Documentation Structure

1. **Individual Prompts**: All 9 prompts spelled out
2. **Reference File**: Link to `tests/playwright/test_prompts.md`
3. **Usage Guidelines**: Mandatory rules and procedures
4. **Performance Notes**: Response time expectations

### Testing Procedures

1. **Start Application**: Run backend and frontend servers
2. **Select Prompt**: Choose from standardized list
3. **Execute Test**: Run prompt through system
4. **Verify Response**: Check response time and content
5. **Document Results**: Record test outcomes

## Quality Assurance

### Response Time Validation

- **Target**: 30-60 seconds per test
- **Monitoring**: Track response times
- **Optimization**: Adjust for performance issues
- **Reporting**: Document performance metrics

### Content Validation

- **Accuracy**: Verify data correctness
- **Completeness**: Ensure comprehensive responses
- **Consistency**: Maintain standardized format
- **Quality**: High-quality analysis output

### System Health Monitoring

- **MCP Server**: Verify Polygon.io integration
- **API Endpoints**: Check backend functionality
- **Frontend**: Validate UI responsiveness
- **Database**: Ensure data integrity

## Maintenance and Updates

### Regular Validation

- **Weekly Testing**: Run all 9 prompts
- **Performance Review**: Monitor response times
- **Content Quality**: Verify analysis accuracy
- **System Health**: Check overall functionality

### Documentation Updates

- **Prompt Refinement**: Update based on testing results
- **Procedure Updates**: Improve testing procedures
- **Performance Tuning**: Optimize response times
- **Quality Enhancement**: Improve analysis quality

### Future Enhancements

- **Additional Prompts**: Expand test coverage
- **Performance Optimization**: Improve response times
- **Quality Metrics**: Enhanced validation procedures
- **Automation**: Automated testing integration

## Success Metrics

### Performance Metrics

- **Response Time**: 30-60 seconds average
- **Success Rate**: 95%+ successful responses
- **Error Rate**: <5% error rate
- **Consistency**: Standardized output format

### Quality Metrics

- **Accuracy**: High-quality analysis output
- **Completeness**: Comprehensive responses
- **Relevance**: Market-appropriate analysis
- **Usability**: Clear and actionable insights

### System Metrics

- **Uptime**: 99%+ system availability
- **Reliability**: Consistent performance
- **Scalability**: Handle multiple concurrent tests
- **Maintainability**: Easy to update and modify

## Troubleshooting

### Common Issues

1. **Slow Response**: Check MCP server status
2. **Missing Data**: Verify API key configuration
3. **Format Errors**: Check prompt formatting
4. **System Errors**: Review logs and configuration

### Resolution Procedures

1. **Identify Issue**: Analyze error messages
2. **Check Configuration**: Verify settings
3. **Restart Services**: Restart if necessary
4. **Document Issue**: Record for future reference

### Support Resources

- **Documentation**: Comprehensive guides available
- **Logs**: Detailed error logging
- **Configuration**: Well-documented settings
- **Community**: Support channels available
