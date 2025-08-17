# Feature Scope: Stock Data GUI Elements with AI-Driven Updates

## Executive Summary
This document outlines the feasibility, complexity, and implementation plan for adding GUI elements to the Market Parser application that display structured stock data populated by specific AI prompt actions triggered via buttons.

**Feasibility:** ✅ HIGH - Fully achievable with current Gradio framework  
**Complexity:** 🟡 MEDIUM - Requires careful state management and response parsing  
**Estimated Timeline:** 2-3 days for complete implementation  

## Feature Overview

### Core Requirements
1. **New GUI Elements** for displaying:
   - Stock Snapshot (current price, % change, $ change, volume, VWAP, OHLC)
   - Support & Resistance Levels (3 levels each)
   - Technical Analysis (RSI, MACD, EMA 5/10/20/50/200, SMA 5/10/20/50/200)

2. **Button Prompts** that insert predefined queries:
   - "Current Stock Snapshot" button
   - "Support & Resistance Levels" button
   - "Technical Analysis" button

3. **Selective Updates**:
   - ONLY button-triggered prompts update GUI elements
   - Regular chat interactions do NOT update these elements
   - Maintains separation between conversational AI and structured data display

## Technical Architecture

### Component Structure
```python
gr.Blocks() layout:
├── Header Section
├── Main Content (gr.Row)
│   ├── Chat Section (gr.Column, scale=2)
│   │   ├── Chatbot
│   │   ├── Message Input
│   │   └── Send/Clear Buttons
│   └── Data Display Section (gr.Column, scale=1)
│       ├── Stock Snapshot (gr.Dataframe)
│       ├── Support/Resistance (gr.Dataframe)
│       └── Technical Indicators (gr.Dataframe)
└── Quick Actions Section
    └── Button Row (Stock Snapshot | S&R | Technical)
```

### State Management
```python
# New state components
button_triggered = gr.State(False)
current_ticker = gr.State("")
parsed_data = gr.State({
    "snapshot": None,
    "support_resistance": None,
    "technical": None
})
```

### Data Flow
1. User clicks action button → Sets `button_triggered=True` → Inserts prompt
2. AI processes prompt → Returns formatted response
3. Response parser extracts structured data (only if `button_triggered=True`)
4. GUI elements update with parsed data
5. Reset `button_triggered=False` after update

## Dependencies & Requirements

### Existing Dependencies (Already in project)
- `gradio>=4.0.0` - UI framework
- `pydantic-ai-slim[openai,mcp]` - AI agent framework
- `pandas` - Data manipulation (via gradio)
- `python-dotenv` - Environment management

### No Additional Dependencies Required
The feature can be implemented entirely with existing packages.

## Button Prompt Templates

### Stock Snapshot Prompt
```
"Provide a comprehensive stock snapshot for [TICKER]. Include:
- Current price
- Percentage change
- $ Change
- Volume
- VWAP (Volume Weighted Average Price)
- Open
- High
- Low
- Close
Format numbers clearly with appropriate units."
```

### Support & Resistance Prompt
```
"Analyze support and resistance levels for [TICKER]. Provide:
- 3 support levels (S1, S2, S3) with prices
- 3 resistance levels (R1, R2, R3) with prices
- Brief explanation of each level's significance
Use recent price action and technical analysis."
```

### Technical Analysis Prompt
```
"Provide technical analysis indicators for [TICKER]:
- RSI (14-day)
- MACD (12,26,9) with signal line status
- Moving Averages: EMA and SMA for 5, 10, 20, 50, 200 days
- Current trend assessment based on these indicators
Include specific values and interpretations."
```

## Implementation Tasks

### Phase 1: UI Components (3-4 hours)
- [ ] Add gr.Dataframe for stock snapshot display
- [ ] Add gr.Dataframe for support/resistance levels
- [ ] Add gr.Dataframe for technical indicators
- [ ] Create button row with three action buttons
- [ ] Implement responsive layout with gr.Row/gr.Column

### Phase 2: State Management (2-3 hours)
- [ ] Implement button_triggered state flag
- [ ] Add current_ticker state for tracking active stock
- [ ] Create parsed_data state dictionary
- [ ] Modify handle_user_message to check trigger source
- [ ] Add state reset logic after updates

### Phase 3: Response Parsing (4-5 hours)
- [ ] Create ResponseParser class with methods:
  - `parse_stock_snapshot(text) -> dict`
  - `parse_support_resistance(text) -> dict`
  - `parse_technical_indicators(text) -> dict`
- [ ] Implement regex patterns for data extraction
- [ ] Add fallback handling for parse failures
- [ ] Create data validation functions

### Phase 4: Prompt Engineering (2-3 hours)
- [ ] Design button prompt templates with formatting instructions
- [ ] Add system prompt modifications for structured output
- [ ] Implement ticker extraction from user context
- [ ] Test prompt consistency across different stocks

### Phase 5: Integration & Testing (2-3 hours)
- [ ] Connect button clicks to prompt insertion
- [ ] Wire parser outputs to Dataframe updates
- [ ] Test button-triggered vs regular chat behavior
- [ ] Add loading states during processing
- [ ] Implement error handling and user feedback

## Code Examples

### Button Implementation
```python
import gradio as gr

# Button row with predefined prompts
with gr.Row():
    snapshot_btn = gr.Button("📊 Stock Snapshot", variant="secondary")
    sr_btn = gr.Button("📈 Support & Resistance", variant="secondary")
    tech_btn = gr.Button("🔧 Technical Analysis", variant="secondary")

# Button click handlers
def trigger_snapshot(ticker_state):
    ticker = ticker_state or 'the last mentioned stock'
    prompt = f"Provide a comprehensive stock snapshot for {ticker}. Include: Current price, Percentage change, $ Change, Volume, VWAP (Volume Weighted Average Price), Open, High, Low, Close. Format numbers clearly with appropriate units."
    return prompt, True  # Return prompt and set button_triggered flag

snapshot_btn.click(
    trigger_snapshot,
    inputs=[current_ticker],
    outputs=[msg, button_triggered]
).then(
    handle_user_message,
    inputs=[msg, chatbot, pyd_history_state, tracker_state, button_triggered],
    outputs=[msg, chatbot, pyd_history_state, tracker_state, costs, 
             snapshot_df, sr_df, tech_df]
)
```

### Response Parser Example
```python
import re
import pandas as pd

class ResponseParser:
    @staticmethod
    def parse_stock_snapshot(text: str) -> pd.DataFrame:
        """Extract stock snapshot data from AI response."""
        patterns = {
            'current_price': r'(?:price|trading at|current)[:\s]*\$?([\d,]+\.?\d*)',
            'percentage_change': r'(?:up|down|changed?)[:\s]*([\d\.\-\+]+)%',
            'dollar_change': r'(?:\$|\+|\-)([\d\.\-\+]+)(?:\s|$)',
            'volume': r'volume[:\s]*([\d,]+)',
            'vwap': r'(?:vwap|volume weighted)[:\s]*\$?([\d,]+\.?\d*)',
            'open': r'open[:\s]*\$?([\d,]+\.?\d*)',
            'high': r'high[:\s]*\$?([\d,]+\.?\d*)',
            'low': r'low[:\s]*\$?([\d,]+\.?\d*)',
            'close': r'close[:\s]*\$?([\d,]+\.?\d*)'
        }
        
        data = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data[key] = match.group(1)
        
        return pd.DataFrame([data]) if data else pd.DataFrame()
```

### Modified Message Handler
```python
import pandas as pd
from typing import Optional

async def handle_user_message(
    user_message: str,
    chat_history: list[dict],
    pyd_message_history: list | None,
    tracker: TokenCostTracker,
    cost_markdown: str,
    is_button_triggered: bool = False,
    snapshot_df: pd.DataFrame = None,
    sr_df: pd.DataFrame = None,
    tech_df: pd.DataFrame = None
):
    # Existing chat logic...
    response = await agent.run(user_message, message_history=pyd_message_history)
    output_text = getattr(response, "output", "") or ""
    
    # Parse and update dataframes ONLY if button-triggered
    if is_button_triggered:
        parser = ResponseParser()
        
        if "snapshot" in user_message.lower():
            snapshot_df = parser.parse_stock_snapshot(output_text)
        elif "support" in user_message.lower() or "resistance" in user_message.lower():
            sr_df = parser.parse_support_resistance(output_text)
        elif "technical" in user_message.lower():
            tech_df = parser.parse_technical_indicators(output_text)
    
    # Reset button trigger flag
    is_button_triggered = False
    
    return (
        "", chat_history, pyd_message_history, tracker, cost_markdown,
        is_button_triggered, snapshot_df, sr_df, tech_df
    )
```

## Challenges & Solutions

### Challenge 1: AI Response Consistency
**Problem:** AI may return data in varying formats  
**Solution:** 
- Add explicit formatting instructions to button prompts
- Use few-shot examples in system prompt
- Implement multiple regex patterns for flexibility

### Challenge 2: Data Extraction Reliability
**Problem:** Parsing unstructured text is error-prone  
**Solution:**
- Implement comprehensive error handling
- Display raw text as fallback
- Log parsing failures for debugging
- Consider asking AI to output in pseudo-structured format

### Challenge 3: UI Responsiveness
**Problem:** Processing and updates may cause lag  
**Solution:**
- Use async/await for non-blocking operations
- Show loading indicators during processing
- Update components incrementally
- Cache parsed data to avoid re-parsing

### Challenge 4: State Synchronization
**Problem:** Managing multiple state variables  
**Solution:**
- Use single source of truth pattern
- Implement state validation functions
- Clear documentation of state flow
- Add debug mode to trace state changes

## Success Metrics

1. **Functionality**
   - ✅ All three button types trigger appropriate prompts
   - ✅ Data displays update correctly from button prompts
   - ✅ Regular chat doesn't affect data displays
   - ✅ Error handling prevents crashes

2. **User Experience**
   - Response time < 3 seconds for data updates
   - Clear visual feedback during processing
   - Intuitive button labels and placement
   - Readable, well-formatted data displays

3. **Code Quality**
   - Modular, testable components
   - Comprehensive error handling
   - Clear documentation and comments
   - Follows existing code patterns

## Future Enhancements

1. **Phase 2 Features**
   - Auto-refresh data on timer
   - Export data to CSV/Excel
   - Historical data comparison
   - Chart visualizations

2. **Advanced Parsing**
   - ML-based response parsing
   - Confidence scores for extracted data
   - Multi-stock comparison views

3. **Customization**
   - User-defined button prompts
   - Configurable data display formats
   - Saved layouts/preferences

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Parsing failures | Medium | Low | Fallback to raw text display |
| UI layout issues | Low | Medium | Responsive design testing |
| Performance degradation | Low | Medium | Optimize parsing, use caching |
| State management bugs | Medium | High | Comprehensive testing, logging |

## Conclusion

This feature is **highly feasible** with **medium complexity**. The main technical challenges revolve around reliable response parsing and state management, both of which have clear solutions. The modular implementation approach allows for incremental development and testing, reducing overall project risk.

**Recommended Approach:** Implement in phases with Phase 1-3 as MVP, followed by iterative improvements based on user feedback.

**Total Estimated Time:** 15-20 hours of development + 5 hours testing/refinement

---

*Document Version: 1.0*  
*Created: December 2024*  
*Author: Market Parser Development Team*
