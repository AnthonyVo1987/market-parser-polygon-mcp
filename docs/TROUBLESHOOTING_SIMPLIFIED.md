# Troubleshooting Guide - Simplified Architecture

**Market Parser - Single Chat Interface Troubleshooting**

**Date**: 2025-08-19  
**Version**: 4.0.0  
**Target Audience**: Users and Developers  
**Architecture**: Simplified Single Chat Interface with Dual-Mode Processing

---

## Table of Contents

1. [Quick Start Troubleshooting](#quick-start-troubleshooting)
2. [Common User Issues](#common-user-issues)
3. [Chat Interface Problems](#chat-interface-problems)
4. [Button and Response Issues](#button-and-response-issues)
5. [Performance Problems](#performance-problems)
6. [Error Recovery](#error-recovery)
7. [Data Export Issues](#data-export-issues)
8. [System Configuration](#system-configuration)
9. [Developer Issues](#developer-issues)
10. [Advanced Diagnostics](#advanced-diagnostics)

---

## Quick Start Troubleshooting

### First Steps for Any Issue

1. **Check Chat Interface**: Is the conversation visible?
2. **Try Button Click**: Click any analysis button
3. **Check Browser Console**: Press F12 and look for errors
4. **Refresh Interface**: Press Ctrl+F5 (Cmd+Shift+R on Mac)
5. **Verify API Keys**: Check `.env` file configuration

### Emergency Recovery

**If nothing works:**
```bash
# Stop the application
Ctrl+C

# Clear any cached data
rm -rf __pycache__ logs/*.log

# Restart the application
uv run chat_ui.py
```

**If still having issues:**
- Check network connectivity
- Verify API key validity
- Review error logs in `logs/` directory
- Check system resources (memory, CPU)

---

## Common User Issues

### 1. Application Won't Start

**Symptoms:**
- Error when running `uv run chat_ui.py`
- Import errors or module not found
- Permission denied errors

**Solutions:**

#### Missing Dependencies
```bash
# Install all dependencies
uv install

# If using pip instead
pip install -r requirements.txt

# Install dev dependencies if needed
uv install --dev
```

#### Missing API Keys
```bash
# Check if .env file exists
ls -la .env

# Create from template if missing
cp .env.example .env

# Edit with your actual API keys
nano .env
```

**Required .env content:**
```env
POLYGON_API_KEY=your_polygon_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00
```

#### Permission Issues
```bash
# Check file permissions
ls -la market_parser_demo.py chat_ui.py

# Fix permissions if needed
chmod +x market_parser_demo.py chat_ui.py

# On Windows, run as administrator if needed
```

### 2. Web Interface Not Loading

**Symptoms:**
- Browser shows "This site can't be reached"
- Connection refused errors
- Blank page after starting application

**Solutions:**

#### Check Application Status
```bash
# Look for startup messages
uv run chat_ui.py

# Should see:
# Running on local URL:  http://127.0.0.1:7860
# To create a public link, set `share=True`
```

#### Network Configuration
```bash
# Check if port 7860 is available
netstat -an | grep 7860
# or on Windows:
netstat -an | findstr 7860

# Try different port if needed
export PORT=7861
uv run chat_ui.py
```

#### Browser Issues
- Try different browser (Chrome, Firefox, Safari)
- Clear browser cache and cookies
- Disable browser extensions temporarily
- Try incognito/private browsing mode

### 3. Slow or Unresponsive Interface

**Symptoms:**
- Long delays between messages
- Interface feels sluggish
- Loading indicators stuck

**Diagnostic Steps:**
```python
# Check system resources
import psutil

print(f"CPU Usage: {psutil.cpu_percent()}%")
print(f"Memory Usage: {psutil.virtual_memory().percent}%")
print(f"Disk Usage: {psutil.disk_usage('/').percent}%")
```

**Solutions:**
1. **Check System Resources**: Ensure adequate RAM and CPU
2. **Clear Browser Cache**: Remove cached data
3. **Restart Application**: Fresh start often helps
4. **Check Network**: Verify internet connection stability
5. **Review Logs**: Look for performance warnings

---

## Chat Interface Problems

### 1. Messages Not Appearing

**Symptoms:**
- User sends message but nothing appears
- Chat area remains empty
- No response from system

**Diagnostic Checklist:**
```python
# Check if chat interface is properly initialized
def diagnose_chat_interface():
    checks = {
        "gradio_version": check_gradio_version(),
        "javascript_errors": check_browser_console(),
        "websocket_connection": check_websocket_status(),
        "api_connectivity": test_api_connection()
    }
    return checks

def check_gradio_version():
    import gradio as gr
    return gr.__version__  # Should be 4.0.0+
```

**Solutions:**

#### Gradio Interface Reset
```python
# In chat_ui.py, force interface refresh
def refresh_chat_interface():
    global chat_interface
    chat_interface.close()
    chat_interface = create_new_interface()
    return "Interface refreshed"
```

#### Browser Connectivity
- Check browser's developer tools (F12)
- Look for WebSocket connection errors
- Verify no ad blockers interfering
- Try different browser or incognito mode

### 2. Dual-Mode Responses Not Working

**Symptoms:**
- Button clicks show conversational responses instead of JSON
- User messages show JSON instead of natural language
- Inconsistent response formats

**Diagnostic Code:**
```python
def diagnose_dual_mode():
    """Diagnose dual-mode response issues"""
    
    # Test mode detection
    user_input = {"type": "user_message", "content": "Test message"}
    button_input = {"type": "button_click", "analysis_type": "snapshot"}
    
    user_mode = detect_processing_mode(user_input)
    button_mode = detect_processing_mode(button_input)
    
    return {
        "user_mode_detected": user_mode,
        "button_mode_detected": button_mode,
        "mode_detection_working": user_mode != button_mode
    }
```

**Solutions:**

#### Fix Mode Detection
```python
# In src/response_manager.py
def detect_processing_mode(input_data):
    if isinstance(input_data, dict):
        if input_data.get("type") == "button_click":
            return ProcessingMode.STRUCTURED
        elif input_data.get("type") == "user_message":
            return ProcessingMode.CONVERSATIONAL
    
    # Default fallback
    return ProcessingMode.CONVERSATIONAL
```

#### Verify Response Routing
```python
# Check response routing logic
async def verify_response_routing():
    # Test conversational response
    conv_response = await process_user_message("What is AAPL's price?")
    assert isinstance(conv_response, str), "Conversational response should be string"
    
    # Test structured response
    struct_response = await process_button_click("stock_snapshot", {"ticker": "AAPL"})
    assert isinstance(struct_response, dict), "Structured response should be dict"
    assert "prompt_used" in struct_response, "Should include prompt visibility"
```

### 3. Chat History Issues

**Symptoms:**
- Previous messages disappear
- Chat history not preserved
- Export missing messages

**Solutions:**

#### Check Session State
```python
# Verify session state management
def check_chat_history():
    import gradio as gr
    
    # Check if session state is maintained
    if hasattr(gr, 'State'):
        state = gr.State(value=[])  # Initialize empty chat history
        return f"Session state available: {len(state.value)} messages"
    
    return "Session state not properly configured"
```

#### Fix History Persistence
```python
# Ensure proper history management
class ChatHistoryManager:
    def __init__(self):
        self.history = []
        self.max_history = 100  # Limit to prevent memory issues
    
    def add_message(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        
        # Trim history if too long
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_history_for_export(self):
        return self.history.copy()
```

---

## Button and Response Issues

### 1. Analysis Buttons Not Working

**Symptoms:**
- Clicking buttons has no effect
- No loading indicator appears
- Buttons appear disabled or grayed out

**Diagnostic Steps:**

#### Check Button State Management
```python
def diagnose_button_issues():
    """Diagnose button functionality issues"""
    
    # Check FSM state
    from stock_data_fsm import StateManager
    state_manager = StateManager()
    
    return {
        "current_state": state_manager.current_state,
        "can_trigger_button": state_manager.current_state == AppState.IDLE,
        "button_handlers_registered": check_button_handlers(),
        "javascript_errors": check_browser_console_errors()
    }

def check_button_handlers():
    """Verify button event handlers are properly registered"""
    # This would check Gradio interface configuration
    return "Button handlers registered"
```

#### Fix Button Configuration
```python
# In chat_ui.py, ensure proper button configuration
def create_analysis_buttons():
    with gr.Row():
        snapshot_btn = gr.Button("📊 Stock Snapshot", variant="primary")
        sr_btn = gr.Button("📈 Support & Resistance", variant="secondary") 
        technical_btn = gr.Button("🔍 Technical Analysis", variant="secondary")
    
    # Ensure proper event binding
    snapshot_btn.click(
        fn=handle_stock_snapshot,
        inputs=[],
        outputs=[chatbot, status_display]
    )
    
    return snapshot_btn, sr_btn, technical_btn
```

### 2. Missing JSON in Button Responses

**Symptoms:**
- Button clicks return conversational text instead of JSON
- No structured data visible
- Missing prompt visibility

**Solutions:**

#### Verify JSON Response Processing
```python
async def test_json_response_generation():
    """Test JSON response generation for button clicks"""
    
    # Test structured response
    response = await generate_structured_response("stock_snapshot", "AAPL")
    
    assert isinstance(response, dict), "Should return dictionary"
    assert "prompt_used" in response, "Should include prompt"
    assert "response" in response, "Should include AI response"
    
    return response

async def generate_structured_response(analysis_type: str, ticker: str):
    """Generate structured response for button clicks"""
    
    # Get appropriate prompt
    prompt = get_analysis_prompt(analysis_type, ticker)
    
    # Make AI call
    ai_response = await ai_client.generate(prompt)
    
    return {
        "type": "structured",
        "analysis_type": analysis_type,
        "ticker": ticker,
        "prompt_used": prompt,
        "response": ai_response,
        "timestamp": time.time()
    }
```

#### Fix Response Display
```python
def format_structured_response_for_chat(response: dict) -> str:
    """Format structured response for display in chat"""
    
    formatted = f"""
**System Prompt:**
```
{response['prompt_used']}
```

**AI Response:**
```json
{json.dumps(response['response'], indent=2)}
```

*Analysis Type: {response['analysis_type']}*
*Ticker: {response['ticker']}*
    """
    
    return formatted
```

### 3. Ticker Symbol Detection Issues

**Symptoms:**
- Buttons don't detect ticker from conversation
- Wrong ticker used in analysis
- "No ticker found" errors

**Diagnostic Code:**
```python
def diagnose_ticker_detection():
    """Diagnose ticker symbol detection issues"""
    
    test_messages = [
        "What is AAPL's current price?",
        "Show me Tesla information",
        "How is Microsoft doing?",
        "Give me Google stock data"
    ]
    
    results = {}
    for message in test_messages:
        detected = extract_ticker_from_message(message)
        results[message] = detected
    
    return results

def extract_ticker_from_message(message: str) -> Optional[str]:
    """Extract ticker symbol from message"""
    import re
    
    # Common stock patterns
    patterns = [
        r'\b([A-Z]{1,5})\b',  # All caps 1-5 letters
        r'\$([A-Z]{1,5})',    # With $ prefix
        r'ticker[:\s]+([A-Z]{1,5})',  # After "ticker:"
    ]
    
    # Company name to ticker mapping
    company_map = {
        'tesla': 'TSLA',
        'apple': 'AAPL',
        'microsoft': 'MSFT',
        'google': 'GOOGL',
        'amazon': 'AMZN'
    }
    
    message_lower = message.lower()
    
    # Check company names first
    for company, ticker in company_map.items():
        if company in message_lower:
            return ticker
    
    # Check ticker patterns
    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            return match.group(1)
    
    return None
```

---

## Performance Problems

### 1. Slow Response Times

**Symptoms:**
- Responses take longer than 5 seconds
- User interface feels unresponsive
- High latency in API calls

**Performance Diagnostic:**
```python
async def diagnose_performance_issues():
    """Comprehensive performance diagnostics"""
    
    import time
    import psutil
    
    # Measure response time components
    start_time = time.time()
    
    # API call timing
    api_start = time.time()
    await test_api_call()
    api_time = time.time() - api_start
    
    # Processing timing
    process_start = time.time()
    await test_response_processing()
    process_time = time.time() - process_start
    
    # System resources
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    
    total_time = time.time() - start_time
    
    return {
        "total_response_time": total_time,
        "api_call_time": api_time,
        "processing_time": process_time,
        "cpu_usage_percent": cpu_usage,
        "memory_usage_percent": memory_usage,
        "performance_issues": identify_performance_bottlenecks(api_time, process_time, cpu_usage, memory_usage)
    }

def identify_performance_bottlenecks(api_time, process_time, cpu_usage, memory_usage):
    """Identify performance bottlenecks"""
    issues = []
    
    if api_time > 3.0:
        issues.append("API response time too high (>3s)")
    if process_time > 1.0:
        issues.append("Processing time too high (>1s)")
    if cpu_usage > 80:
        issues.append("High CPU usage")
    if memory_usage > 80:
        issues.append("High memory usage")
    
    return issues if issues else ["No major performance issues detected"]
```

**Solutions:**

#### API Optimization
```python
# Implement response caching
class ResponseCache:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get(self, key: str):
        if key in self.cache:
            timestamp, response = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return response
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, response):
        self.cache[key] = (time.time(), response)
```

#### Processing Optimization
```python
# Use async processing for better performance
import asyncio

async def optimized_response_processing(user_input):
    """Process responses with performance optimization"""
    
    # Parallel preprocessing
    tasks = [
        extract_ticker_symbols(user_input),
        validate_input(user_input),
        prepare_context()
    ]
    
    preprocessing_results = await asyncio.gather(*tasks)
    
    # Main processing
    response = await generate_response(user_input, preprocessing_results)
    
    # Async post-processing
    asyncio.create_task(update_metrics(response))
    asyncio.create_task(cache_response(user_input, response))
    
    return response
```

### 2. High API Costs

**Symptoms:**
- Unexpectedly high API bills
- Token usage higher than expected
- Cost per request above targets

**Cost Diagnostic:**
```python
def diagnose_cost_issues():
    """Diagnose high API cost issues"""
    
    # Analyze recent token usage
    token_stats = analyze_token_usage()
    
    # Check prompt efficiency
    prompt_stats = analyze_prompt_efficiency()
    
    # Review caching effectiveness
    cache_stats = get_cache_statistics()
    
    return {
        "average_tokens_per_request": token_stats["average"],
        "token_usage_trend": token_stats["trend"],
        "prompt_efficiency_score": prompt_stats["efficiency"],
        "cache_hit_rate": cache_stats["hit_rate"],
        "cost_optimization_opportunities": identify_cost_savings()
    }

def analyze_token_usage():
    """Analyze token usage patterns"""
    # This would analyze actual usage logs
    return {
        "average": 250,  # tokens per request
        "trend": "stable",  # increasing/decreasing/stable
        "peak": 450,     # highest usage
        "minimum": 120   # lowest usage
    }

def identify_cost_savings():
    """Identify cost saving opportunities"""
    return [
        "Optimize prompt templates for brevity",
        "Implement more aggressive caching",
        "Use conversation context more efficiently",
        "Batch similar requests when possible"
    ]
```

**Cost Reduction Solutions:**
```python
# Implement cost tracking and alerts
class CostTracker:
    def __init__(self):
        self.daily_limit = 10.00  # $10 daily limit
        self.current_usage = 0.0
        
    def track_request(self, input_tokens: int, output_tokens: int):
        # gpt-5-mini pricing
        input_cost = (input_tokens / 1_000_000) * 0.25
        output_cost = (output_tokens / 1_000_000) * 2.00
        total_cost = input_cost + output_cost
        
        self.current_usage += total_cost
        
        if self.current_usage > self.daily_limit:
            raise CostLimitExceededError(f"Daily cost limit exceeded: ${self.current_usage:.4f}")
        
        return total_cost

# Optimize prompts for cost efficiency
OPTIMIZED_PROMPTS = {
    "stock_snapshot": "Stock data for {ticker}: price, change, volume, market cap. JSON format.",
    "technical_analysis": "Technical indicators for {ticker}: RSI, MACD, trend. JSON.",
    "support_resistance": "S&R levels for {ticker}: 3 support, 3 resistance. JSON."
}
```

---

## Error Recovery

### 1. Non-blocking Error Recovery

**The simplified architecture ensures errors don't freeze the system:**

#### Error Recovery Mechanism
```python
async def handle_error_with_recovery(error: Exception, context: dict):
    """Handle errors with immediate recovery capability"""
    
    # Log error for diagnostics
    logger.error(f"Error occurred: {error}", extra={"context": context})
    
    # Create user-friendly error message
    error_message = create_user_friendly_error(error)
    
    # Provide recovery options
    recovery_options = get_recovery_options(error, context)
    
    # Update chat with error and recovery instructions
    error_response = {
        "type": "error",
        "message": error_message,
        "recovery_options": recovery_options,
        "retry_available": True,
        "context_preserved": True
    }
    
    # System remains responsive
    return error_response

def create_user_friendly_error(error: Exception) -> str:
    """Convert technical errors to user-friendly messages"""
    
    error_messages = {
        "ConnectionError": "Unable to connect to the service. Please check your internet connection.",
        "TimeoutError": "Request timed out. The service might be busy - please try again.",
        "APIError": "Service temporarily unavailable. Please retry in a moment.",
        "ValidationError": "Invalid input detected. Please check your request and try again.",
        "RateLimitError": "Rate limit exceeded. Please wait a moment before trying again."
    }
    
    error_type = type(error).__name__
    return error_messages.get(error_type, f"An unexpected error occurred: {str(error)}")

def get_recovery_options(error: Exception, context: dict) -> List[str]:
    """Get specific recovery options for the error"""
    
    base_options = ["Click any analysis button to retry", "Send a new message to continue"]
    
    if isinstance(error, ConnectionError):
        base_options.extend([
            "Check your internet connection",
            "Verify API keys in .env file"
        ])
    elif isinstance(error, TimeoutError):
        base_options.extend([
            "Wait a moment and try again",
            "Try a simpler request first"
        ])
    
    return base_options
```

### 2. Common Error Scenarios and Solutions

#### API Connection Errors
```python
async def handle_api_connection_error():
    """Handle API connection issues"""
    
    # Test connectivity
    connectivity_test = await test_api_connectivity()
    
    if not connectivity_test["success"]:
        return {
            "error_type": "connection",
            "message": "Unable to connect to OpenAI API",
            "solutions": [
                "Check internet connection",
                "Verify OpenAI API key",
                "Check API service status",
                "Try again in a few moments"
            ],
            "retry_in_seconds": 30
        }
    
    return {"status": "Connection OK"}

async def test_api_connectivity():
    """Test API connectivity"""
    try:
        # Simple API test
        response = await openai_client.test_connection()
        return {"success": True, "response_time": response.time}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

#### Data Processing Errors
```python
def handle_data_processing_error(raw_response: str, error: Exception):
    """Handle data processing errors with fallback"""
    
    try:
        # Attempt fallback processing
        fallback_result = attempt_fallback_processing(raw_response)
        
        return {
            "type": "warning",
            "message": "Partial data processing successful",
            "data": fallback_result,
            "note": "Some data may be incomplete"
        }
        
    except Exception as fallback_error:
        return {
            "type": "error", 
            "message": "Unable to process response data",
            "raw_response": raw_response[:500] + "..." if len(raw_response) > 500 else raw_response,
            "solutions": [
                "Try the same request again",
                "Use a different analysis type",
                "Check if ticker symbol is correct"
            ]
        }

def attempt_fallback_processing(raw_response: str):
    """Attempt to extract useful data from malformed response"""
    
    # Try to extract key-value pairs with regex
    import re
    
    patterns = {
        "price": r'(?:price|current)[:\s]*\$?([0-9]+\.?[0-9]*)',
        "change": r'(?:change|up|down)[:\s]*([+-]?[0-9]+\.?[0-9]*)',
        "volume": r'(?:volume)[:\s]*([0-9,]+)'
    }
    
    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, raw_response, re.IGNORECASE)
        if match:
            extracted_data[key] = match.group(1)
    
    return extracted_data if extracted_data else {"raw_text": raw_response}
```

#### State Management Errors
```python
def handle_fsm_error(current_state, attempted_transition, error):
    """Handle FSM state management errors"""
    
    # Reset to safe state
    safe_state = AppState.IDLE
    
    error_info = {
        "error_type": "state_management",
        "current_state": current_state.value,
        "attempted_transition": attempted_transition.value if attempted_transition else "unknown",
        "error_message": str(error),
        "recovery_action": f"Reset to {safe_state.value} state"
    }
    
    # Log for debugging
    logger.warning(f"FSM error: {error_info}")
    
    # Return to idle state for recovery
    return safe_state, error_info
```

---

## Data Export Issues

### 1. Export Functionality Problems

**Symptoms:**
- Export button doesn't respond
- Downloaded files are empty
- Incomplete conversation history in export

**Diagnostic Steps:**
```python
def diagnose_export_issues():
    """Diagnose export functionality issues"""
    
    # Check conversation history
    history_status = check_conversation_history()
    
    # Test export generation
    export_test = test_export_generation()
    
    # Check browser download capability
    download_test = test_browser_downloads()
    
    return {
        "conversation_history": history_status,
        "export_generation": export_test,
        "browser_downloads": download_test
    }

def check_conversation_history():
    """Check if conversation history is properly stored"""
    global chat_history
    
    return {
        "history_available": len(chat_history) > 0,
        "message_count": len(chat_history),
        "latest_message": chat_history[-1] if chat_history else None
    }

def test_export_generation():
    """Test export file generation"""
    try:
        # Generate test export
        test_export = generate_export_data(["Test message 1", "Test response 1"])
        return {
            "generation_successful": True,
            "export_size": len(test_export),
            "export_format": "markdown"
        }
    except Exception as e:
        return {
            "generation_successful": False,
            "error": str(e)
        }
```

**Solutions:**

#### Fix Export Generation
```python
def generate_export_data(conversation_history: List[dict]) -> str:
    """Generate export data from conversation history"""
    
    export_content = f"""# Market Parser Conversation Export
Generated: {datetime.now().isoformat()}
Total Messages: {len(conversation_history)}

---

"""
    
    for i, message in enumerate(conversation_history, 1):
        if isinstance(message, dict):
            role = message.get("role", "user")
            content = message.get("content", "")
            timestamp = message.get("timestamp", time.time())
            
            export_content += f"""## Message {i} ({role})
**Timestamp:** {datetime.fromtimestamp(timestamp).isoformat()}

{content}

---

"""
    
    return export_content

def create_downloadable_file(content: str, filename: str = None) -> str:
    """Create downloadable file from content"""
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"market_parser_export_{timestamp}.md"
    
    # In Gradio, return content with filename for download
    return content, filename
```

#### Browser Download Issues
```python
def test_browser_downloads():
    """Test if browser can handle downloads"""
    
    # Check if running in supported browser
    user_agent_hints = [
        "Chrome",
        "Firefox", 
        "Safari",
        "Edge"
    ]
    
    # This would be implemented client-side
    return {
        "download_capability": True,  # Assume modern browser
        "popup_blockers": "Check if popup blockers are disabled",
        "download_location": "Check browser download settings"
    }
```

### 2. Export Format Issues

**Symptoms:**
- Exported data is malformed
- JSON structure is incorrect
- Missing conversation context

**Solutions:**

#### Improve Export Formatting
```python
class ConversationExporter:
    """Enhanced conversation export with multiple formats"""
    
    def __init__(self):
        self.supported_formats = ["markdown", "json", "csv", "txt"]
    
    def export_conversation(self, conversation: List[dict], format_type: str = "markdown") -> str:
        """Export conversation in specified format"""
        
        if format_type == "markdown":
            return self.export_as_markdown(conversation)
        elif format_type == "json":
            return self.export_as_json(conversation)
        elif format_type == "csv":
            return self.export_as_csv(conversation)
        elif format_type == "txt":
            return self.export_as_text(conversation)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def export_as_markdown(self, conversation: List[dict]) -> str:
        """Export as formatted markdown"""
        
        md_content = f"""# Market Parser Analysis Session
**Export Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Total Interactions:** {len(conversation)}  
**Session Duration:** {self.calculate_session_duration(conversation)}

---

"""
        
        for i, msg in enumerate(conversation, 1):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", time.time())
            
            if role == "user":
                md_content += f"""### 🗣️ User Message {i}
*{datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")}*

{content}

"""
            else:
                md_content += f"""### 🤖 AI Response {i}
*{datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")}*

{self.format_ai_response(content)}

---

"""
        
        return md_content
    
    def export_as_json(self, conversation: List[dict]) -> str:
        """Export as structured JSON"""
        
        export_data = {
            "export_metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "4.0.0",
                "format": "json",
                "message_count": len(conversation)
            },
            "conversation": conversation,
            "summary": self.generate_conversation_summary(conversation)
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def format_ai_response(self, content: str) -> str:
        """Format AI response for better readability"""
        
        # Check if content is JSON
        try:
            json_data = json.loads(content)
            return f"""```json
{json.dumps(json_data, indent=2)}
```"""
        except json.JSONDecodeError:
            # Regular text response
            return content
    
    def calculate_session_duration(self, conversation: List[dict]) -> str:
        """Calculate session duration"""
        
        if len(conversation) < 2:
            return "N/A"
        
        start_time = min(msg.get("timestamp", 0) for msg in conversation)
        end_time = max(msg.get("timestamp", 0) for msg in conversation)
        
        duration = end_time - start_time
        
        if duration < 60:
            return f"{duration:.0f} seconds"
        elif duration < 3600:
            return f"{duration/60:.1f} minutes"
        else:
            return f"{duration/3600:.1f} hours"
    
    def generate_conversation_summary(self, conversation: List[dict]) -> dict:
        """Generate conversation summary"""
        
        tickers_mentioned = set()
        analysis_types = set()
        user_messages = 0
        ai_responses = 0
        
        for msg in conversation:
            if msg.get("role") == "user":
                user_messages += 1
                # Extract tickers from user messages
                content = msg.get("content", "")
                tickers = self.extract_tickers_from_text(content)
                tickers_mentioned.update(tickers)
            else:
                ai_responses += 1
                # Extract analysis types
                if "analysis_type" in msg:
                    analysis_types.add(msg["analysis_type"])
        
        return {
            "tickers_analyzed": list(tickers_mentioned),
            "analysis_types_used": list(analysis_types),
            "user_messages": user_messages,
            "ai_responses": ai_responses,
            "total_interactions": len(conversation)
        }
    
    def extract_tickers_from_text(self, text: str) -> List[str]:
        """Extract ticker symbols from text"""
        import re
        
        # Pattern for ticker symbols
        ticker_pattern = r'\b[A-Z]{1,5}\b'
        potential_tickers = re.findall(ticker_pattern, text.upper())
        
        # Filter out common words that aren't tickers
        common_words = {"THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HER", "WAS", "ONE", "OUR", "HAD", "BUT", "WHAT", "UP", "OUT", "IF", "ABOUT", "WHO", "GET", "WHICH", "GO", "ME"}
        
        return [ticker for ticker in potential_tickers if ticker not in common_words]
```

---

## System Configuration

### 1. Environment Variable Issues

**Common Problems:**
- API keys not loaded
- Incorrect pricing configuration
- Missing required variables

**Diagnostic Script:**
```python
def diagnose_environment_config():
    """Diagnose environment configuration issues"""
    
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    required_vars = {
        "POLYGON_API_KEY": "Polygon.io API key",
        "OPENAI_API_KEY": "OpenAI API key"
    }
    
    optional_vars = {
        "OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M": "0.25",
        "OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M": "2.00",
        "OPENAI_MODEL": "gpt-5-mini",
        "HOST": "127.0.0.1",
        "PORT": "7860"
    }
    
    config_status = {}
    
    # Check required variables
    for var, description in required_vars.items():
        value = os.getenv(var)
        config_status[var] = {
            "description": description,
            "configured": value is not None,
            "value_length": len(value) if value else 0,
            "status": "✅ OK" if value else "❌ MISSING"
        }
    
    # Check optional variables
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        config_status[var] = {
            "description": f"Optional: {var}",
            "configured": True,
            "value": value,
            "status": "✅ OK"
        }
    
    return config_status

def fix_environment_config():
    """Generate .env template with correct values"""
    
    env_template = """# Market Parser Environment Configuration
# Copy this file to .env and fill in your actual API keys

# Required: Polygon.io API Key
POLYGON_API_KEY=your_polygon_api_key_here

# Required: OpenAI API Key  
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Pricing for cost tracking (USD per 1M tokens)
OPENAI_GPT5_MINI_INPUT_PRICE_PER_1M=0.25
OPENAI_GPT5_MINI_OUTPUT_PRICE_PER_1M=2.00

# Optional: Model selection (default: gpt-5-mini)
OPENAI_MODEL=gpt-5-mini

# Optional: Server configuration
HOST=127.0.0.1
PORT=7860
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_template)
    
    return "Created .env.template - copy to .env and add your API keys"
```

### 2. Dependencies and Version Issues

**Diagnostic Steps:**
```python
def check_dependencies():
    """Check all dependencies and versions"""
    
    import importlib
    import sys
    
    required_packages = {
        "gradio": ">=4.0.0",
        "pydantic-ai-slim": ">=0.1.0", 
        "python-dotenv": ">=0.19.0",
        "rich": ">=10.0.0",
        "asyncio": "built-in",
        "time": "built-in",
        "json": "built-in"
    }
    
    dependency_status = {}
    
    for package, version_req in required_packages.items():
        try:
            if package in ["asyncio", "time", "json"]:
                # Built-in modules
                module = importlib.import_module(package)
                dependency_status[package] = {
                    "installed": True,
                    "version": "built-in",
                    "requirement": version_req,
                    "status": "✅ OK"
                }
            else:
                module = importlib.import_module(package.replace("-", "_"))
                version = getattr(module, "__version__", "unknown")
                dependency_status[package] = {
                    "installed": True,
                    "version": version,
                    "requirement": version_req,
                    "status": "✅ OK"
                }
        except ImportError:
            dependency_status[package] = {
                "installed": False,
                "version": "not installed",
                "requirement": version_req,
                "status": "❌ MISSING"
            }
    
    # Check Python version
    python_version = sys.version_info
    dependency_status["python"] = {
        "installed": True,
        "version": f"{python_version.major}.{python_version.minor}.{python_version.micro}",
        "requirement": ">=3.8",
        "status": "✅ OK" if python_version >= (3, 8) else "❌ TOO OLD"
    }
    
    return dependency_status

def fix_dependencies():
    """Generate commands to fix dependency issues"""
    
    commands = [
        "# Install/update all dependencies",
        "uv install",
        "",
        "# Alternative: using pip",
        "pip install -r requirements.txt",
        "",
        "# Install development dependencies",
        "uv install --dev",
        "",
        "# Update specific packages if needed",
        "uv add gradio@latest",
        "uv add pydantic-ai-slim@latest"
    ]
    
    return "\n".join(commands)
```

---

## Developer Issues

### 1. Development Environment Setup

**Common Issues:**
- Import path problems
- Module not found errors
- IDE configuration issues

**Solutions:**

#### Fix Import Paths
```python
# Add to your IDE's Python path or create setup.py
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now imports should work
from src.response_manager import ResponseManager
from stock_data_fsm.manager import StateManager
```

#### IDE Configuration
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.analysis.extraPaths": ["./src", "./stock_data_fsm"]
}
```

### 2. Testing Issues

**Common Problems:**
- Tests not finding modules
- Mock objects not working
- Async test issues

**Testing Setup:**
```python
# tests/conftest.py
import pytest
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mock_ai_client():
    """Mock AI client for testing"""
    class MockAIClient:
        async def generate(self, prompt):
            return {"ticker": "AAPL", "price": 150.00}
    
    return MockAIClient()

@pytest.fixture
def sample_conversation():
    """Sample conversation data for testing"""
    return [
        {"role": "user", "content": "What is AAPL's price?", "timestamp": time.time()},
        {"role": "assistant", "content": "AAPL is trading at $150.00", "timestamp": time.time()}
    ]
```

#### Run Tests
```bash
# Run all tests
uv run pytest tests/

# Run with coverage
uv run pytest tests/ --cov=src --cov=stock_data_fsm

# Run specific test file
uv run pytest tests/test_simplified_architecture.py -v

# Run tests with detailed output
uv run pytest tests/ -v --tb=short
```

---

## Advanced Diagnostics

### 1. System Health Check

```python
async def comprehensive_system_health_check():
    """Comprehensive system health diagnostic"""
    
    health_report = {
        "timestamp": datetime.now().isoformat(),
        "system_info": get_system_info(),
        "dependency_check": check_dependencies(),
        "environment_config": diagnose_environment_config(),
        "performance_metrics": await get_performance_metrics(),
        "api_connectivity": await test_all_api_connections(),
        "fsm_status": check_fsm_health(),
        "memory_usage": get_memory_usage(),
        "recent_errors": get_recent_errors()
    }
    
    # Generate health score
    health_report["overall_health"] = calculate_health_score(health_report)
    
    return health_report

def get_system_info():
    """Get system information"""
    import platform
    import psutil
    
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "disk_space": psutil.disk_usage('/').free
    }

async def test_all_api_connections():
    """Test all external API connections"""
    
    connection_tests = {}
    
    # Test OpenAI API
    try:
        openai_test = await test_openai_connection()
        connection_tests["openai"] = {"status": "✅ OK", "details": openai_test}
    except Exception as e:
        connection_tests["openai"] = {"status": "❌ ERROR", "error": str(e)}
    
    # Test Polygon.io API
    try:
        polygon_test = await test_polygon_connection()
        connection_tests["polygon"] = {"status": "✅ OK", "details": polygon_test}
    except Exception as e:
        connection_tests["polygon"] = {"status": "❌ ERROR", "error": str(e)}
    
    return connection_tests

def calculate_health_score(health_report: dict) -> dict:
    """Calculate overall system health score"""
    
    score_components = {
        "dependencies": 0,
        "environment": 0,
        "api_connectivity": 0,
        "performance": 0,
        "memory": 0
    }
    
    # Score dependencies (0-20 points)
    deps = health_report["dependency_check"]
    working_deps = sum(1 for dep in deps.values() if "✅" in str(dep.get("status", "")))
    score_components["dependencies"] = min(20, (working_deps / len(deps)) * 20)
    
    # Score environment config (0-20 points)
    env_config = health_report["environment_config"]
    working_config = sum(1 for cfg in env_config.values() if cfg.get("configured", False))
    score_components["environment"] = min(20, (working_config / len(env_config)) * 20)
    
    # Score API connectivity (0-30 points)
    api_tests = health_report["api_connectivity"]
    working_apis = sum(1 for api in api_tests.values() if "✅" in api.get("status", ""))
    score_components["api_connectivity"] = min(30, (working_apis / len(api_tests)) * 30)
    
    # Score performance (0-20 points)
    # This would be based on actual performance metrics
    score_components["performance"] = 18  # Assume good performance
    
    # Score memory usage (0-10 points)
    memory_usage = health_report.get("memory_usage", {}).get("percent", 0)
    if memory_usage < 60:
        score_components["memory"] = 10
    elif memory_usage < 80:
        score_components["memory"] = 7
    else:
        score_components["memory"] = 3
    
    total_score = sum(score_components.values())
    
    return {
        "total_score": total_score,
        "max_score": 100,
        "percentage": total_score,
        "grade": get_health_grade(total_score),
        "component_scores": score_components
    }

def get_health_grade(score: float) -> str:
    """Convert health score to grade"""
    if score >= 90:
        return "A (Excellent)"
    elif score >= 80:
        return "B (Good)"
    elif score >= 70:
        return "C (Fair)"
    elif score >= 60:
        return "D (Poor)"
    else:
        return "F (Critical)"
```

### 2. Automated Issue Resolution

```python
class AutoResolver:
    """Automated issue resolution system"""
    
    def __init__(self):
        self.resolution_strategies = {
            "api_connection": self.resolve_api_connection,
            "dependency_missing": self.resolve_dependency_issue,
            "environment_config": self.resolve_environment_issue,
            "performance_slow": self.resolve_performance_issue,
            "memory_high": self.resolve_memory_issue
        }
    
    async def auto_resolve_issues(self, health_report: dict):
        """Attempt to automatically resolve detected issues"""
        
        issues_detected = self.detect_issues(health_report)
        resolution_results = {}
        
        for issue_type, issue_details in issues_detected.items():
            if issue_type in self.resolution_strategies:
                try:
                    result = await self.resolution_strategies[issue_type](issue_details)
                    resolution_results[issue_type] = {"status": "resolved", "details": result}
                except Exception as e:
                    resolution_results[issue_type] = {"status": "failed", "error": str(e)}
            else:
                resolution_results[issue_type] = {"status": "no_auto_resolution", "manual_steps": self.get_manual_steps(issue_type)}
        
        return resolution_results
    
    def detect_issues(self, health_report: dict) -> dict:
        """Detect issues from health report"""
        
        issues = {}
        
        # Check API connectivity
        api_tests = health_report.get("api_connectivity", {})
        failed_apis = [api for api, status in api_tests.items() if "❌" in status.get("status", "")]
        if failed_apis:
            issues["api_connection"] = failed_apis
        
        # Check dependencies
        deps = health_report.get("dependency_check", {})
        missing_deps = [dep for dep, info in deps.items() if not info.get("installed", True)]
        if missing_deps:
            issues["dependency_missing"] = missing_deps
        
        # Check environment config
        env_config = health_report.get("environment_config", {})
        missing_config = [cfg for cfg, info in env_config.items() if not info.get("configured", False)]
        if missing_config:
            issues["environment_config"] = missing_config
        
        return issues
    
    async def resolve_api_connection(self, failed_apis: list):
        """Attempt to resolve API connection issues"""
        
        resolution_steps = []
        
        for api in failed_apis:
            if api == "openai":
                # Check API key
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    resolution_steps.append("Set OPENAI_API_KEY in .env file")
                elif len(api_key) < 20:
                    resolution_steps.append("OPENAI_API_KEY appears to be invalid (too short)")
                else:
                    resolution_steps.append("Verify OPENAI_API_KEY is correct")
            
            elif api == "polygon":
                # Check API key
                api_key = os.getenv("POLYGON_API_KEY")
                if not api_key:
                    resolution_steps.append("Set POLYGON_API_KEY in .env file")
                else:
                    resolution_steps.append("Verify POLYGON_API_KEY is correct")
        
        return resolution_steps
    
    async def resolve_dependency_issue(self, missing_deps: list):
        """Attempt to resolve dependency issues"""
        
        install_commands = []
        
        for dep in missing_deps:
            if dep in ["gradio", "pydantic-ai-slim", "python-dotenv", "rich"]:
                install_commands.append(f"uv add {dep}")
        
        return {
            "install_commands": install_commands,
            "alternative": "Run 'uv install' to install all dependencies"
        }
```

---

## Conclusion

This troubleshooting guide provides comprehensive solutions for common issues with the simplified Market Parser architecture. The system's design prioritizes:

- **Non-blocking error recovery**: Issues don't freeze the interface
- **Clear error messages**: User-friendly explanations and solutions
- **Immediate recovery**: Click any button to retry after errors
- **Comprehensive diagnostics**: Tools to identify and resolve issues
- **Automated resolution**: Self-healing capabilities where possible

### Key Troubleshooting Principles

1. **System Never Freezes**: The simplified architecture ensures the interface remains responsive
2. **Context Preservation**: Errors don't lose conversation history or progress
3. **Clear Recovery Path**: Every error provides specific recovery instructions
4. **Diagnostic Tools**: Comprehensive tools for identifying root causes
5. **Performance Monitoring**: Real-time metrics to prevent issues

### Quick Reference

**Most Common Issues:**
- API key configuration → Check `.env` file
- Button not working → Click any button to retry
- Slow responses → Check network and system resources
- Export problems → Verify conversation history exists
- Import errors → Check Python path and dependencies

**Emergency Recovery:**
1. Refresh browser (Ctrl+F5)
2. Restart application
3. Check API keys
4. Clear cache and logs
5. Run system health check

The simplified architecture makes troubleshooting much easier compared to the previous complex system, with most issues being self-resolving or requiring simple retry actions.