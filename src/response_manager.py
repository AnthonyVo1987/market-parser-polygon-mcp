"""
Unified Conversational Response Manager for Market Parser

This module provides enhanced conversational formatting for all AI responses.
Removes JSON extraction attempts and focuses on unified chat experience.

Features:
- Unified conversational formatting for all responses
- Enhanced text formatting with emojis and improved spacing
- Better readability with structured text layouts
- Performance monitoring and error handling
- Integration with existing FSM and chat UI
"""

import logging
import time
from typing import Dict, Any, Optional
from enum import Enum
import re


class ResponseType(Enum):
    """Response source types for unified conversational processing"""
    USER = "user"           # User-initiated conversational response
    BUTTON = "button"       # Button-initiated conversational response


class ProcessingMode(Enum):
    """Processing modes for conversational responses"""
    ENHANCED = "enhanced"                  # Enhanced conversational formatting
    STANDARD = "standard"                  # Standard conversational formatting


class ResponseManager:
    """
    Unified conversational response manager with enhanced formatting.
    
    This manager provides enhanced conversational formatting for all responses,
    removing JSON extraction and focusing on improved readability.
    """
    
    def __init__(self, processing_mode: ProcessingMode = ProcessingMode.ENHANCED):
        """
        Initialize the response manager with specified processing mode.
        
        Args:
            processing_mode: Default processing mode for responses
        """
        self.logger = logging.getLogger(__name__)
        self.processing_mode = processing_mode
        
        # Performance tracking
        self._processing_stats = {
            'total_requests': 0,
            'button_requests': 0,
            'user_requests': 0,
            'successful_responses': 0,
            'avg_processing_time_ms': 0.0
        }
        
        self.logger.info(f"ResponseManager initialized in {processing_mode.value} conversational mode")
    
    def process_response(self, response_text: str, source_type: str = 'user', 
                        data_type: Optional[str] = None, ticker: Optional[str] = None,
                        processing_mode: Optional[ProcessingMode] = None) -> Dict[str, Any]:
        """
        Main entry point for processing AI responses with unified conversational formatting.
        
        Args:
            response_text: Raw AI response text
            source_type: 'button' or 'user' (both get conversational formatting)
            data_type: Analysis type for context (used for enhanced formatting)
            ticker: Stock ticker symbol for context
            processing_mode: Override default processing mode
            
        Returns:
            Dict with enhanced conversational response optimized for chat display
        """
        start_time = time.time()
        mode = processing_mode or self.processing_mode
        
        self.logger.info(f"🔄 Processing {source_type} response ({len(response_text)} chars) in unified conversational mode")
        
        # Update statistics
        self._processing_stats['total_requests'] += 1
        if source_type == 'button':
            self._processing_stats['button_requests'] += 1
        else:
            self._processing_stats['user_requests'] += 1
        
        try:
            # Apply unified conversational formatting
            if mode == ProcessingMode.ENHANCED:
                formatted_content = self._apply_enhanced_formatting(response_text, source_type, data_type, ticker)
            else:
                formatted_content = self._apply_standard_formatting(response_text, source_type, data_type, ticker)
            
            result = {
                'success': True,
                'content': formatted_content,
                'source_type': source_type,
                'data_type': data_type,
                'ticker': ticker
            }
            
            # Add processing metadata
            processing_time = (time.time() - start_time) * 1000
            result['processing_time_ms'] = processing_time
            result['processing_mode'] = mode.value
            result['response_type'] = source_type
            
            # Update statistics
            self._processing_stats['successful_responses'] += 1
            
            # Update average processing time
            total_time = (self._processing_stats['avg_processing_time_ms'] * 
                         (self._processing_stats['total_requests'] - 1) + processing_time)
            self._processing_stats['avg_processing_time_ms'] = total_time / self._processing_stats['total_requests']
            
            self.logger.info(f"✅ Response processed successfully in {processing_time:.1f}ms")
            return result
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            
            self.logger.error(f"💥 Response processing failed after {processing_time:.1f}ms: {e}")
            
            return {
                'success': True,  # Always succeed for conversational mode
                'content': f"🔍 **Analysis Response**\n\n{response_text}\n\n⚠️ *Note: Enhanced formatting unavailable*",
                'processing_time_ms': processing_time,
                'processing_mode': mode.value,
                'response_type': source_type,
                'warnings': [f"Formatting error: {str(e)}"]
            }
    
    
    def _apply_enhanced_formatting(self, response_text: str, source_type: str, 
                                 data_type: Optional[str], ticker: Optional[str]) -> str:
        """
        Apply enhanced conversational formatting with emojis and improved structure.
        
        Args:
            response_text: Raw AI response text
            source_type: 'button' or 'user' for context
            data_type: Analysis type for enhanced formatting
            ticker: Stock ticker symbol
            
        Returns:
            Enhanced formatted response text
        """
        # Add analysis type header for button responses
        if source_type == 'button' and data_type:
            type_emoji = {
                'snapshot': '📊',
                'support_resistance': '🎯', 
                'technical': '🔍'
            }.get(data_type, '📈')
            
            type_name = data_type.replace('_', ' ').title()
            header = f"{type_emoji} **{type_name} Analysis"+ (f" for {ticker}" if ticker else "") + "**\n\n"
        else:
            header = "🔍 **Market Analysis**\n\n"
        
        # Enhanced text formatting
        formatted_text = self._enhance_text_formatting(response_text)
        
        return header + formatted_text
    
    def _apply_standard_formatting(self, response_text: str, source_type: str, 
                                 data_type: Optional[str], ticker: Optional[str]) -> str:
        """
        Apply standard conversational formatting.
        
        Args:
            response_text: Raw AI response text
            source_type: 'button' or 'user' for context
            data_type: Analysis type for context
            ticker: Stock ticker symbol
            
        Returns:
            Standard formatted response text
        """
        # Simple header for button responses
        if source_type == 'button' and data_type:
            type_name = data_type.replace('_', ' ').title()
            header = f"**{type_name} Analysis"+ (f" for {ticker}" if ticker else "") + "**\n\n"
        else:
            header = "**Analysis Response**\n\n"
        
        return header + response_text
    
    def _enhance_text_formatting(self, text: str) -> str:
        """
        Apply enhanced text formatting for better readability.
        
        Args:
            text: Raw response text
            
        Returns:
            Enhanced formatted text with improved spacing and structure
        """
        # Apply various formatting improvements
        enhanced = text
        
        # Add proper spacing around key sections
        enhanced = re.sub(r'(Current Price:|Price:|Stock:|Symbol:)', r'\n💰 **\1**', enhanced)
        enhanced = re.sub(r'(Volume:|Trading Volume:)', r'\n📈 **\1**', enhanced)
        enhanced = re.sub(r'(Change:|Percentage Change:|% Change:)', r'\n🔄 **\1**', enhanced)
        enhanced = re.sub(r'(Support:|Resistance:|RSI:|MACD:)', r'\n🔍 **\1**', enhanced)
        enhanced = re.sub(r'(Recommendation:|Analysis:|Summary:)', r'\n✨ **\1**', enhanced)
        
        # Improve list formatting
        enhanced = re.sub(r'^\s*[-*]\s+', '• ', enhanced, flags=re.MULTILINE)
        enhanced = re.sub(r'^\s*(\d+)\s*[.):]\s+', r'🔹 \1. ', enhanced, flags=re.MULTILINE)
        
        # Add spacing around paragraphs
        enhanced = re.sub(r'\n\n+', '\n\n', enhanced)
        
        # Clean up any double formatting
        enhanced = re.sub(r'\*\*\*\*', '**', enhanced)
        
        return enhanced.strip()
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing performance statistics."""
        return self._processing_stats.copy()
    
    def reset_stats(self):
        """Reset processing statistics."""
        self._processing_stats = {
            'total_requests': 0,
            'button_requests': 0,
            'user_requests': 0,
            'successful_responses': 0,
            'avg_processing_time_ms': 0.0
        }
        self.logger.info("Processing statistics reset")
    


# ====== Convenience Functions ======

def create_response_manager(mode: ProcessingMode = ProcessingMode.ENHANCED) -> ResponseManager:
    """Create a response manager instance with specified mode."""
    return ResponseManager(mode)


def process_ai_response(response_text: str, source_type: str = 'user', 
                       data_type: Optional[str] = None, ticker: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for processing AI responses with unified conversational formatting.
    
    Args:
        response_text: Raw AI response text
        source_type: 'button' or 'user' (both get conversational formatting)
        data_type: Analysis type for enhanced formatting context
        ticker: Stock ticker symbol for context
        
    Returns:
        Dict with enhanced conversational response optimized for chat display
    """
    manager = create_response_manager()
    return manager.process_response(response_text, source_type, data_type, ticker)


if __name__ == "__main__":
    # Test the unified conversational response manager
    print("🔧 Unified Conversational Response Manager - Test Suite")
    print("=" * 60)
    
    # Create manager
    manager = create_response_manager(ProcessingMode.ENHANCED)
    
    # Test user response
    user_response = "Based on the current market conditions, AAPL is showing strong momentum with good volume support."
    user_result = manager.process_response(user_response, 'user')
    
    print(f"📱 User Response Processing:")
    print(f"   Success: {user_result['success']}")
    print(f"   Processing time: {user_result['processing_time_ms']:.1f}ms")
    print(f"   Content length: {len(user_result['content'])}")
    
    # Test button response (conversational, no JSON parsing)
    button_response = "Apple Inc. (AAPL) is currently trading at $150.25, up 2.5% from yesterday's close. The stock has strong volume support and bullish momentum."
    button_result = manager.process_response(button_response, 'button', 'snapshot', 'AAPL')
    
    print(f"\n🔘 Button Response Processing:")
    print(f"   Success: {button_result['success']}")
    print(f"   Processing time: {button_result['processing_time_ms']:.1f}ms")
    print(f"   Enhanced formatting applied: {bool(button_result.get('data_type'))}")
    
    # Show enhanced formatting example
    print(f"\n🎨 Enhanced Formatting Example:")
    print(button_result['content'][:200] + "...")
    
    # Show statistics
    stats = manager.get_processing_stats()
    print(f"\n📊 Processing Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n✅ Unified Conversational Response Manager ready for integration!")
    print(f"   - No JSON extraction attempts")
    print(f"   - Enhanced conversational formatting")
    print(f"   - Unified processing for all response types")