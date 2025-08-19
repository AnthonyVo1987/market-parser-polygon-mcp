"""
Unified Response Processing Manager for Market Parser

This module provides a single entry point for processing AI responses in dual-mode:
- Button responses: JSON parsing with structured data extraction
- User responses: Conversational text with basic formatting

Features:
- Automatic response type detection
- Conditional processing pipeline
- Chat-optimized output formatting
- Performance monitoring and error handling
- Integration with existing FSM and chat UI
"""

import logging
import time
from typing import Dict, Any, Optional, Union
from enum import Enum
import json

# Import processing components
from .response_parser import ResponseParser, DataType, ConfidenceLevel
from .json_parser import JsonParser, JsonDataType
from .schema_validator import SchemaValidator, AnalysisType


class ResponseType(Enum):
    """Response source types for conditional processing"""
    USER = "user"           # Conversational text response
    BUTTON = "button"       # Structured data response from button action


class ProcessingMode(Enum):
    """Processing modes for different use cases"""
    CHAT_OPTIMIZED = "chat_optimized"      # Optimized for chat interface display
    FULL_VALIDATION = "full_validation"    # Complete parsing and validation
    LIGHTWEIGHT = "lightweight"           # Minimal processing for performance


class ResponseManager:
    """
    Unified response processing manager with dual-mode conditional processing.
    
    This manager automatically detects response types and applies appropriate 
    processing pipelines optimized for the chat interface.
    """
    
    def __init__(self, processing_mode: ProcessingMode = ProcessingMode.CHAT_OPTIMIZED):
        """
        Initialize the response manager with specified processing mode.
        
        Args:
            processing_mode: Default processing mode for responses
        """
        self.logger = logging.getLogger(__name__)
        self.processing_mode = processing_mode
        
        # Initialize processing components
        self.regex_parser = ResponseParser(log_level=logging.INFO)
        self.json_parser = JsonParser(log_level=logging.INFO)
        self.schema_validator = SchemaValidator()
        
        # Type mappings between different parser systems
        self._data_type_mapping = {
            'snapshot': (DataType.SNAPSHOT, JsonDataType.SNAPSHOT, AnalysisType.SNAPSHOT),
            'support_resistance': (DataType.SUPPORT_RESISTANCE, JsonDataType.SUPPORT_RESISTANCE, AnalysisType.SUPPORT_RESISTANCE),
            'technical': (DataType.TECHNICAL, JsonDataType.TECHNICAL, AnalysisType.TECHNICAL)
        }
        
        # Performance tracking
        self._processing_stats = {
            'total_requests': 0,
            'button_requests': 0,
            'user_requests': 0,
            'successful_parses': 0,
            'failed_parses': 0,
            'avg_processing_time_ms': 0.0
        }
        
        self.logger.info(f"ResponseManager initialized in {processing_mode.value} mode")
    
    def process_response(self, response_text: str, source_type: str = 'user', 
                        data_type: Optional[str] = None, ticker: Optional[str] = None,
                        processing_mode: Optional[ProcessingMode] = None) -> Dict[str, Any]:
        """
        Main entry point for processing AI responses with conditional handling.
        
        Args:
            response_text: Raw AI response text
            source_type: 'button' for structured data, 'user' for conversational text
            data_type: Type of structured data ('snapshot', 'support_resistance', 'technical')
            ticker: Stock ticker symbol for context
            processing_mode: Override default processing mode
            
        Returns:
            Dict with processed response data optimized for chat display
        """
        start_time = time.time()
        mode = processing_mode or self.processing_mode
        
        self.logger.info(f"🔄 Processing {source_type} response ({len(response_text)} chars) in {mode.value} mode")
        
        # Update statistics
        self._processing_stats['total_requests'] += 1
        if source_type == 'button':
            self._processing_stats['button_requests'] += 1
        else:
            self._processing_stats['user_requests'] += 1
        
        try:
            # Detect response type and route to appropriate processor
            response_type = ResponseType.BUTTON if source_type == 'button' else ResponseType.USER
            
            if response_type == ResponseType.BUTTON and data_type:
                # Button response: Parse structured data
                result = self._process_button_response(response_text, data_type, ticker, mode)
            else:
                # User response: Pass through with formatting
                result = self._process_user_response(response_text, mode)
            
            # Add processing metadata
            processing_time = (time.time() - start_time) * 1000
            result['processing_time_ms'] = processing_time
            result['processing_mode'] = mode.value
            result['response_type'] = response_type.value
            
            # Update statistics
            if result.get('success', False):
                self._processing_stats['successful_parses'] += 1
            else:
                self._processing_stats['failed_parses'] += 1
            
            # Update average processing time
            total_time = (self._processing_stats['avg_processing_time_ms'] * 
                         (self._processing_stats['total_requests'] - 1) + processing_time)
            self._processing_stats['avg_processing_time_ms'] = total_time / self._processing_stats['total_requests']
            
            self.logger.info(f"✅ Response processed successfully in {processing_time:.1f}ms")
            return result
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self._processing_stats['failed_parses'] += 1
            
            self.logger.error(f"💥 Response processing failed after {processing_time:.1f}ms: {e}")
            
            return {
                'success': False,
                'content': f"⚠️ Response processing error: {str(e)}",
                'processing_time_ms': processing_time,
                'processing_mode': mode.value,
                'response_type': source_type,
                'error': str(e)
            }
    
    def _process_button_response(self, response_text: str, data_type: str, 
                               ticker: Optional[str], mode: ProcessingMode) -> Dict[str, Any]:
        """
        Process button response with structured data extraction.
        
        Args:
            response_text: AI response text
            data_type: Type of structured data expected
            ticker: Stock ticker symbol
            mode: Processing mode
            
        Returns:
            Dict with processed button response
        """
        self.logger.info(f"🔘 Processing button response for {data_type}")
        
        # Get type mappings
        if data_type not in self._data_type_mapping:
            return {
                'success': False,
                'content': f"⚠️ Unknown data type: {data_type}",
                'warnings': [f"Unsupported data type: {data_type}"]
            }
        
        regex_type, json_type, analysis_type = self._data_type_mapping[data_type]
        
        if mode == ProcessingMode.CHAT_OPTIMIZED:
            # Use JSON parser for chat-optimized processing
            return self.json_parser.process_for_chat(response_text, 'button', json_type, ticker)
            
        elif mode == ProcessingMode.LIGHTWEIGHT:
            # Use regex parser for lightweight processing
            return self.regex_parser.process_response(response_text, 'button', regex_type, ticker)
            
        else:  # FULL_VALIDATION
            # Use full validation pipeline
            return self._process_with_full_validation(response_text, json_type, analysis_type, ticker)
    
    def _process_user_response(self, response_text: str, mode: ProcessingMode) -> Dict[str, Any]:
        """
        Process user response with conversational text handling.
        
        Args:
            response_text: AI response text
            mode: Processing mode
            
        Returns:
            Dict with processed user response
        """
        self.logger.info("💬 Processing user response")
        
        # For user responses, all modes use simple text processing
        if mode == ProcessingMode.CHAT_OPTIMIZED:
            return self.json_parser.process_for_chat(response_text, 'user')
        else:
            return self.regex_parser.process_response(response_text, 'user')
    
    def _process_with_full_validation(self, response_text: str, json_type: JsonDataType, 
                                    analysis_type: AnalysisType, ticker: Optional[str]) -> Dict[str, Any]:
        """
        Process response with full JSON parsing and schema validation.
        
        Args:
            response_text: AI response text
            json_type: JSON data type
            analysis_type: Analysis type for validation
            ticker: Stock ticker symbol
            
        Returns:
            Dict with fully validated response
        """
        self.logger.info(f"🔍 Processing with full validation for {analysis_type.value}")
        
        try:
            # Parse JSON response
            parse_result = self.json_parser.parse_any(response_text, json_type, ticker)
            
            # Validate against schema if data was extracted
            validation_result = None
            if parse_result.parsed_data and parse_result.confidence != ConfidenceLevel.FAILED:
                validation_result = self.schema_validator.validate_for_chat(
                    parse_result.parsed_data, analysis_type
                )
            
            # Format comprehensive result
            if parse_result.confidence in [ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM]:
                json_display = json.dumps({
                    'analysis_type': json_type.value,
                    'confidence': parse_result.confidence.value,
                    'data': parse_result.parsed_data,
                    'validation': validation_result
                }, indent=2)
                
                formatted_content = f"{response_text}\n\n**📊 Extracted & Validated Data:**\n```json\n{json_display}\n```"
                
                return {
                    'success': True,
                    'content': formatted_content,
                    'structured_data': parse_result.parsed_data,
                    'confidence': parse_result.confidence.value,
                    'validation_result': validation_result,
                    'data_type': json_type.value
                }
            else:
                return {
                    'success': False,
                    'content': f"{response_text}\n\n⚠️ *Could not extract or validate structured data*",
                    'warnings': parse_result.warnings
                }
                
        except Exception as e:
            self.logger.error(f"Full validation processing failed: {e}")
            return {
                'success': False,
                'content': f"{response_text}\n\n⚠️ *Validation processing error: {str(e)}*",
                'error': str(e)
            }
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing performance statistics."""
        return self._processing_stats.copy()
    
    def reset_stats(self):
        """Reset processing statistics."""
        self._processing_stats = {
            'total_requests': 0,
            'button_requests': 0,
            'user_requests': 0,
            'successful_parses': 0,
            'failed_parses': 0,
            'avg_processing_time_ms': 0.0
        }
        self.logger.info("Processing statistics reset")
    
    def detect_response_structure(self, response_text: str) -> Dict[str, Any]:
        """
        Analyze response text to detect its structure and content type.
        
        Args:
            response_text: Raw response text to analyze
            
        Returns:
            Dict with structure analysis results
        """
        analysis = {
            'length': len(response_text),
            'has_json': '{' in response_text and '}' in response_text,
            'has_code_blocks': '```' in response_text,
            'has_json_block': '```json' in response_text.lower(),
            'line_count': response_text.count('\n') + 1,
            'likely_conversational': any(marker in response_text.lower() for marker in 
                                       ['let me', 'i can', 'here is', 'based on', 'analysis shows']),
            'likely_structured': any(marker in response_text for marker in 
                                   ['current_price', 'percentage_change', 'support_levels', 'RSI', 'MACD'])
        }
        
        # Suggest processing approach
        if analysis['has_json_block'] or analysis['likely_structured']:
            analysis['suggested_source_type'] = 'button'
        else:
            analysis['suggested_source_type'] = 'user'
        
        return analysis


# ====== Convenience Functions ======

def create_response_manager(mode: ProcessingMode = ProcessingMode.CHAT_OPTIMIZED) -> ResponseManager:
    """Create a response manager instance with specified mode."""
    return ResponseManager(mode)


def process_ai_response(response_text: str, source_type: str = 'user', 
                       data_type: Optional[str] = None, ticker: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for processing AI responses.
    
    Args:
        response_text: Raw AI response text
        source_type: 'button' for structured data, 'user' for conversational text  
        data_type: Type of structured data for button responses
        ticker: Stock ticker symbol for context
        
    Returns:
        Dict with processed response optimized for chat display
    """
    manager = create_response_manager()
    return manager.process_response(response_text, source_type, data_type, ticker)


if __name__ == "__main__":
    # Test the response manager
    print("🔧 Response Processing Manager - Test Suite")
    print("=" * 60)
    
    # Create manager
    manager = create_response_manager(ProcessingMode.CHAT_OPTIMIZED)
    
    # Test user response
    user_response = "Based on the current market conditions, AAPL is showing strong momentum with good volume support."
    user_result = manager.process_response(user_response, 'user')
    
    print(f"📱 User Response Processing:")
    print(f"   Success: {user_result['success']}")
    print(f"   Processing time: {user_result['processing_time_ms']:.1f}ms")
    print(f"   Content length: {len(user_result['content'])}")
    
    # Test button response (simulated)
    button_response = '{"snapshot_data": {"current_price": 150.25, "percentage_change": 2.5}}'
    button_result = manager.process_response(button_response, 'button', 'snapshot', 'AAPL')
    
    print(f"\n🔘 Button Response Processing:")
    print(f"   Success: {button_result['success']}")
    print(f"   Processing time: {button_result['processing_time_ms']:.1f}ms")
    
    # Show statistics
    stats = manager.get_processing_stats()
    print(f"\n📊 Processing Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n✅ Response Manager ready for integration!")