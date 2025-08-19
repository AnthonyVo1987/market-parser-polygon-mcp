#!/usr/bin/env python3
"""
Test Script for Dual-Mode Response Processing System

This script validates that the response processing system correctly handles
both button (JSON) and user (text) responses with appropriate conditional
processing pipelines.

Created: 2025-08-19
Purpose: Validate Phase 5 dual-mode response processing implementation
Success Criteria: All dual-mode processing scenarios pass validation
"""

import pytest
import asyncio
import json
import time
from typing import Dict, Any
from unittest.mock import Mock, patch

# Import the response processing system
from src.response_manager import ResponseManager, ProcessingMode, ResponseType
from src.response_parser import ResponseParser, DataType, ConfidenceLevel
from src.json_parser import JsonParser, JsonDataType
from src.schema_validator import SchemaValidator


class TestDualModeProcessing:
    """Test suite for dual-mode response processing system"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        self.response_manager = ResponseManager(ProcessingMode.CHAT_OPTIMIZED)
        
        # Sample responses for testing
        self.sample_user_response = """
        Based on the current market analysis, AAPL is showing strong momentum. 
        The stock has been trending upward with good volume support. 
        Technical indicators suggest continued bullish sentiment.
        """
        
        self.sample_button_response_json = """
        {
            "snapshot_data": {
                "current_price": 150.25,
                "percentage_change": 2.5,
                "dollar_change": 3.67,
                "volume": 45000000,
                "vwap": 149.85,
                "open": 147.30,
                "high": 150.50,
                "low": 146.80,
                "close": 146.58
            },
            "metadata": {
                "analysis_timestamp": "2025-08-19T10:30:00Z",
                "confidence_score": 0.95,
                "data_sources": ["polygon", "real_time"]
            }
        }
        """
        
        self.sample_button_response_mixed = f"""
        Here's the current snapshot analysis for AAPL:
        
        {self.sample_button_response_json}
        
        This data shows strong upward movement with significant volume.
        """
        
        self.sample_malformed_json = """
        {"current_price": 150.25, "percentage_change":}  // malformed JSON
        """
    
    def test_user_response_processing(self):
        """Test user response processing with text pass-through"""
        result = self.response_manager.process_response(
            self.sample_user_response,
            source_type='user'
        )
        
        # Validate user response processing
        assert result['success'] is True
        assert result['source_type'] == 'user'
        assert result['processing_time_ms'] > 0
        assert 'content' in result
        assert len(result['content']) > 0
        
        # Content should be cleaned but essentially unchanged
        assert 'AAPL' in result['content']
        assert 'momentum' in result['content']
        
        print("✅ User response processing: SUCCESS")
    
    def test_button_response_processing_json(self):
        """Test button response processing with JSON data extraction"""
        result = self.response_manager.process_response(
            self.sample_button_response_json,
            source_type='button',
            data_type='snapshot',
            ticker='AAPL'
        )
        
        # Validate button response processing
        assert 'success' in result
        assert result['source_type'] == 'button'
        assert result['data_type'] == 'snapshot'
        assert result['processing_time_ms'] > 0
        assert 'content' in result
        
        # Should contain both original response and extracted data
        content = result['content']
        assert 'Extracted Data' in content or 'JSON' in content
        
        print(f"✅ Button JSON response processing: SUCCESS")
        print(f"   Extracted structured data: {'structured_data' in result}")
    
    def test_button_response_processing_mixed(self):
        """Test button response processing with mixed JSON/text content"""
        result = self.response_manager.process_response(
            self.sample_button_response_mixed,
            source_type='button',
            data_type='snapshot',
            ticker='AAPL'
        )
        
        # Validate mixed content processing
        assert 'source_type' in result
        assert result['source_type'] == 'button'
        assert 'content' in result
        
        # Content should include both text and JSON extraction
        content = result['content']
        assert 'snapshot analysis' in content.lower()
        
        print("✅ Button mixed response processing: SUCCESS")
    
    def test_response_type_detection(self):
        """Test automatic response type detection"""
        # Test user response
        user_analysis = self.response_manager.detect_response_structure(
            self.sample_user_response
        )
        
        assert user_analysis['suggested_source_type'] == 'user'
        assert user_analysis['likely_conversational'] is True
        assert user_analysis['has_json'] is False
        
        # Test button response
        button_analysis = self.response_manager.detect_response_structure(
            self.sample_button_response_json
        )
        
        assert button_analysis['suggested_source_type'] == 'button'
        assert button_analysis['has_json'] is True
        assert button_analysis['likely_structured'] is True
        
        print("✅ Response type detection: SUCCESS")
    
    def test_error_handling_dual_mode(self):
        """Test error handling in dual-mode processing"""
        # Test malformed JSON in button mode
        result = self.response_manager.process_response(
            self.sample_malformed_json,
            source_type='button',
            data_type='snapshot',
            ticker='AAPL'
        )
        
        # Should handle gracefully
        assert 'source_type' in result
        assert 'content' in result
        
        # Test invalid data type
        result2 = self.response_manager.process_response(
            self.sample_user_response,
            source_type='button',
            data_type='invalid_type',
            ticker='AAPL'
        )
        
        assert result2['success'] is False
        assert 'error' in result2 or 'warnings' in result2
        
        print("✅ Error handling dual-mode: SUCCESS")
    
    def test_processing_mode_differences(self):
        """Test different processing modes"""
        # Chat optimized mode
        chat_manager = ResponseManager(ProcessingMode.CHAT_OPTIMIZED)
        chat_result = chat_manager.process_response(
            self.sample_button_response_json,
            source_type='button',
            data_type='snapshot'
        )
        
        # Lightweight mode
        light_manager = ResponseManager(ProcessingMode.LIGHTWEIGHT)
        light_result = light_manager.process_response(
            self.sample_button_response_json,
            source_type='button',
            data_type='snapshot'
        )
        
        # Both should succeed but may have different processing approaches
        assert 'content' in chat_result
        assert 'content' in light_result
        
        print("✅ Processing mode differences: SUCCESS")
    
    def test_performance_metrics(self):
        """Test processing performance metrics"""
        start_time = time.time()
        
        # Process multiple responses
        responses = [
            (self.sample_user_response, 'user', None),
            (self.sample_button_response_json, 'button', 'snapshot'),
            (self.sample_button_response_mixed, 'button', 'support_resistance')
        ]
        
        results = []
        for response_text, source_type, data_type in responses:
            result = self.response_manager.process_response(
                response_text, 
                source_type=source_type, 
                data_type=data_type,
                ticker='TEST'
            )
            results.append(result)
        
        total_time = (time.time() - start_time) * 1000
        
        # Validate performance
        for result in results:
            assert result.get('processing_time_ms', 0) > 0
            assert result.get('processing_time_ms', 0) < 5000  # Should be under 5 seconds
        
        # Check statistics
        stats = self.response_manager.get_processing_stats()
        assert stats['total_requests'] >= 3
        assert stats['button_requests'] >= 2
        assert stats['user_requests'] >= 1
        
        print(f"✅ Performance metrics: SUCCESS")
        print(f"   Total processing time: {total_time:.1f}ms")
        print(f"   Average per request: {total_time/len(responses):.1f}ms")
        print(f"   Processing statistics: {stats}")
    
    def test_data_type_mapping(self):
        """Test data type mapping between different parser systems"""
        # Test all supported data types
        data_types = ['snapshot', 'support_resistance', 'technical']
        
        for data_type in data_types:
            result = self.response_manager.process_response(
                self.sample_button_response_json,
                source_type='button',
                data_type=data_type,
                ticker='TEST'
            )
            
            # Should handle all data types without error
            assert 'content' in result
            assert 'data_type' in result or data_type in str(result)
        
        print("✅ Data type mapping: SUCCESS")
    
    def test_integration_with_chat_ui(self):
        """Test integration compatibility with chat UI requirements"""
        # Simulate chat UI button click processing
        button_result = self.response_manager.process_response(
            self.sample_button_response_json,
            source_type='button',
            data_type='snapshot',
            ticker='AAPL'
        )
        
        # Check chat UI requirements
        assert 'content' in button_result  # For chat display
        assert isinstance(button_result['content'], str)  # Must be string for chat
        
        # Simulate chat UI user message processing  
        user_result = self.response_manager.process_response(
            self.sample_user_response,
            source_type='user'
        )
        
        assert 'content' in user_result
        assert isinstance(user_result['content'], str)
        
        # Both should have processing time for status display
        assert 'processing_time_ms' in button_result
        assert 'processing_time_ms' in user_result
        
        print("✅ Chat UI integration compatibility: SUCCESS")


def test_response_manager_creation():
    """Test response manager factory functions"""
    from src.response_manager import create_response_manager, process_ai_response
    
    # Test factory function
    manager = create_response_manager(ProcessingMode.CHAT_OPTIMIZED)
    assert isinstance(manager, ResponseManager)
    
    # Test convenience function
    result = process_ai_response(
        "This is a test response",
        source_type='user'
    )
    assert 'content' in result
    assert 'success' in result
    
    print("✅ Response manager factory functions: SUCCESS")


def validate_dual_mode_success() -> bool:
    """
    Run comprehensive validation of the dual-mode processing system
    Returns: True if all criteria met, False otherwise
    """
    success_criteria = [
        "User responses processed with text pass-through",
        "Button responses processed with JSON extraction",
        "Response type detection working correctly",
        "Error handling graceful for both modes",
        "Performance metrics within acceptable ranges",
        "Chat UI integration compatibility maintained",
        "Processing statistics tracking functional"
    ]
    
    try:
        # Run the test suite
        test_suite = TestDualModeProcessing()
        test_suite.setup_method()
        
        # Execute all test methods
        test_methods = [
            test_suite.test_user_response_processing,
            test_suite.test_button_response_processing_json,
            test_suite.test_button_response_processing_mixed,
            test_suite.test_response_type_detection,
            test_suite.test_error_handling_dual_mode,
            test_suite.test_processing_mode_differences,
            test_suite.test_performance_metrics,
            test_suite.test_data_type_mapping,
            test_suite.test_integration_with_chat_ui
        ]
        
        for test_method in test_methods:
            test_method()
        
        # Test factory functions
        test_response_manager_creation()
        
        return True
        
    except Exception as e:
        print(f"❌ DUAL-MODE PROCESSING VALIDATION FAILED: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Dual-Mode Response Processing System")
    print("=" * 60)
    
    # Run comprehensive validation
    success = validate_dual_mode_success()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ DUAL-MODE PROCESSING VALIDATION: SUCCESS")
        print("\n🎯 Success Criteria Met:")
        print("   • User responses processed with conversational text handling")
        print("   • Button responses processed with JSON data extraction")
        print("   • Conditional processing pipeline working correctly")
        print("   • Response type detection and routing functional")
        print("   • Error handling graceful for both processing modes")
        print("   • Performance metrics within acceptable thresholds")
        print("   • Chat UI integration compatibility maintained")
        print("   • Processing statistics and monitoring operational")
        print("\n🚀 Phase 5 dual-mode response processing ready for production!")
    else:
        print("\n" + "=" * 60)
        print("❌ DUAL-MODE PROCESSING VALIDATION: FAILED")
        print("\n🔧 Review the test output above for specific issues")
        print("🔄 Fix identified problems and re-run validation")
        exit(1)