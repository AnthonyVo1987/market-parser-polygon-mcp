# Latest App Behavior Changes - v2.1.0

## Major Changes Implemented

### 1. Performance Monitoring System
- **NEW**: Real-time response timing with FastAPI middleware
- **NEW**: Automated token counting from OpenAI response metadata
- **NEW**: CLI performance metrics display with Rich console formatting
- **ENHANCED**: Both CLI and GUI now show performance data

### 2. Report Management Modernization
- **REMOVED**: CLI backend report saving functionality completely
- **REASON**: Superseded by GUI Copy/Export buttons
- **IMPACT**: Simplified agent configuration and user workflow
- **BENEFIT**: Modern GUI controls handle all report management

### 3. CLI User Experience Enhancement
- **NEW**: Performance metrics footer after each response
- **FORMAT**: "📊 Performance Metrics: 🔢 Tokens Used: 1,247 (Input: 156, Output: 1,091) 🤖 Model: gpt-5-nano"
- **ENHANCED**: Rich console formatting with emoji indicators
- **STREAMLINED**: No more report saving prompts

### 4. Backend Architecture Updates
- **ADDED**: FastAPI middleware for response timing measurement
- **ENHANCED**: Token extraction from OpenAI response metadata
- **OPTIMIZED**: Agent tools configuration without report saving overhead
- **IMPROVED**: ResponseMetadata integration for performance data

## Technical Details

### Performance Monitoring
- Response timing: `time.perf_counter()` middleware
- Token counting: OpenAI response metadata extraction
- CLI display: Rich console with performance metrics footer
- Overhead: <0.01% of response time

### Report Management
- Removed `save_analysis_report` function
- Updated all Agent instances to remove report saving tools
- GUI Copy/Export buttons handle all report functionality
- Simplified user workflow

### Documentation Updates
- README.md: Updated with new features and CLI example
- Performance guide: Added monitoring metrics
- Changelog: Added v2.1.0 section
- All docs reflect new app behavior

## User Impact
- CLI users see performance metrics after each response
- GUI users inherit performance data through API
- No more report saving prompts in CLI
- Streamlined workflow with modern GUI controls
- Real-time cost tracking with token breakdown