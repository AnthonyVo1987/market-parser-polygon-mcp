"""
JSON Debug Logger for Market Parser

This module provides comprehensive debug logging specifically for JSON workflows,
including raw JSON output, performance metrics, and detailed analysis tracking.

Features:
- Centralized JSON workflow logging
- Performance timing and metrics
- Raw JSON response logging
- Error condition debugging
- FSM state transition logging with JSON context
- Confidence scoring and validation tracking
"""

import json
import logging
import time
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import traceback


class LogLevel(Enum):
    """Custom log levels for JSON debugging"""
    JSON_TRACE = "JSON_TRACE"
    JSON_DEBUG = "JSON_DEBUG"
    JSON_INFO = "JSON_INFO"
    JSON_WARNING = "JSON_WARNING"
    JSON_ERROR = "JSON_ERROR"


@dataclass
class JsonWorkflowMetrics:
    """Container for JSON workflow performance metrics"""
    workflow_start_time: float
    json_extraction_time_ms: Optional[float] = None
    validation_time_ms: Optional[float] = None
    parsing_time_ms: Optional[float] = None
    dataframe_conversion_time_ms: Optional[float] = None
    total_workflow_time_ms: Optional[float] = None
    
    def complete_workflow(self):
        """Mark workflow as complete and calculate total time"""
        self.total_workflow_time_ms = (time.time() - self.workflow_start_time) * 1000
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for logging"""
        return {
            'json_extraction_time_ms': self.json_extraction_time_ms,
            'validation_time_ms': self.validation_time_ms,
            'parsing_time_ms': self.parsing_time_ms,
            'dataframe_conversion_time_ms': self.dataframe_conversion_time_ms,
            'total_workflow_time_ms': self.total_workflow_time_ms
        }


class JsonDebugLogger:
    """
    Comprehensive debug logger specifically designed for JSON workflows.
    
    Provides detailed logging for JSON extraction, validation, parsing,
    and UI updates with performance metrics and error tracking.
    """
    
    def __init__(self, logger_name: str = "json_debug", log_level: int = logging.DEBUG):
        """
        Initialize the JSON debug logger.
        
        Args:
            logger_name: Name for the logger instance
            log_level: Logging level for debug output
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        
        # Create file handler for JSON debug logs
        self._setup_json_log_file()
        
        # Track active workflows
        self._active_workflows: Dict[str, JsonWorkflowMetrics] = {}
        
        self.logger.info("🔍 JsonDebugLogger initialized with comprehensive JSON tracing")
    
    def _setup_json_log_file(self):
        """Setup dedicated file handler for JSON debug logs"""
        try:
            file_handler = logging.FileHandler('json_workflow_debug.log', mode='a', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # Enhanced formatter for JSON workflows
            formatter = logging.Formatter(
                '%(asctime)s - JSON_DEBUG - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            
            # Only add if not already added
            if not any(isinstance(h, logging.FileHandler) and 'json_workflow_debug.log' in str(h.baseFilename) 
                      for h in self.logger.handlers):
                self.logger.addHandler(file_handler)
                
        except Exception as e:
            self.logger.warning(f"Failed to setup JSON debug log file: {e}")
    
    def start_json_workflow(self, workflow_id: str, button_type: str, ticker: str, response_text: str) -> JsonWorkflowMetrics:
        """
        Start tracking a JSON workflow.
        
        Args:
            workflow_id: Unique identifier for this workflow
            button_type: Type of analysis button clicked
            ticker: Stock ticker symbol
            response_text: Raw AI response text
            
        Returns:
            JsonWorkflowMetrics instance for this workflow
        """
        metrics = JsonWorkflowMetrics(workflow_start_time=time.time())
        self._active_workflows[workflow_id] = metrics
        
        # Log workflow start with comprehensive analysis
        self.logger.info(f"🚀 WORKFLOW START [{workflow_id}] - {button_type.upper()} for {ticker}")
        self.logger.info(f"📄 Response size: {len(response_text)} characters")
        
        # Analyze raw response
        response_analysis = self._analyze_raw_response(response_text)
        self.logger.info(f"📊 Response analysis: {response_analysis}")
        
        # Log raw response content (first 500 chars)
        self.logger.debug(f"📄 Raw response preview [{workflow_id}]: {repr(response_text[:500])}")
        if len(response_text) > 500:
            self.logger.debug(f"📄 Raw response continuation [{workflow_id}]: {repr(response_text[500:1000])}")
        
        return metrics
    
    def log_json_extraction(self, workflow_id: str, extraction_time_ms: float, 
                           extracted_json: Optional[Dict[str, Any]], 
                           extraction_method: str, success: bool):
        """
        Log JSON extraction results.
        
        Args:
            workflow_id: Workflow identifier
            extraction_time_ms: Time taken for extraction
            extracted_json: Extracted JSON data (if successful)
            extraction_method: Method used for extraction
            success: Whether extraction was successful
        """
        if workflow_id in self._active_workflows:
            self._active_workflows[workflow_id].json_extraction_time_ms = extraction_time_ms
        
        if success and extracted_json:
            json_size = len(json.dumps(extracted_json))
            json_keys = list(extracted_json.keys()) if isinstance(extracted_json, dict) else 'non-dict'
            
            self.logger.info(f"✅ JSON EXTRACTION [{workflow_id}] - Success in {extraction_time_ms:.1f}ms")
            self.logger.info(f"📦 Extracted JSON: {json_size} chars, keys: {json_keys}, method: {extraction_method}")
            self.logger.debug(f"🔧 Complete extracted JSON [{workflow_id}]: {json.dumps(extracted_json, indent=2)}")
        else:
            self.logger.warning(f"❌ JSON EXTRACTION [{workflow_id}] - Failed in {extraction_time_ms:.1f}ms")
            self.logger.warning(f"🔧 Extraction method attempted: {extraction_method}")
    
    def log_schema_validation(self, workflow_id: str, validation_time_ms: float,
                             validation_result: Dict[str, Any], schema_type: str):
        """
        Log schema validation results.
        
        Args:
            workflow_id: Workflow identifier
            validation_time_ms: Time taken for validation
            validation_result: Validation result dictionary
            schema_type: Type of schema used
        """
        if workflow_id in self._active_workflows:
            self._active_workflows[workflow_id].validation_time_ms = validation_time_ms
        
        is_valid = validation_result.get('valid', False)
        error_message = validation_result.get('error_message', 'No error details')
        
        if is_valid:
            self.logger.info(f"✅ SCHEMA VALIDATION [{workflow_id}] - Success in {validation_time_ms:.1f}ms")
            self.logger.info(f"📋 Schema type: {schema_type}, version: {validation_result.get('schema_version', 'unknown')}")
        else:
            self.logger.warning(f"⚠️ SCHEMA VALIDATION [{workflow_id}] - Failed in {validation_time_ms:.1f}ms")
            self.logger.warning(f"❌ Validation error: {error_message}")
        
        self.logger.debug(f"📋 Complete validation result [{workflow_id}]: {validation_result}")
    
    def log_parsing_results(self, workflow_id: str, parsing_time_ms: float,
                           parse_result: Any, confidence: str, field_count: int, warnings: List[str]):
        """
        Log parsing results with confidence and field analysis.
        
        Args:
            workflow_id: Workflow identifier
            parsing_time_ms: Time taken for parsing
            parse_result: Parse result object
            confidence: Confidence level string
            field_count: Number of fields extracted
            warnings: List of parsing warnings
        """
        if workflow_id in self._active_workflows:
            self._active_workflows[workflow_id].parsing_time_ms = parsing_time_ms
        
        confidence_emoji = "🎯" if confidence == "high" else "⚡" if confidence == "medium" else "⚠️"
        
        self.logger.info(f"{confidence_emoji} PARSING RESULTS [{workflow_id}] - {confidence.upper()} confidence in {parsing_time_ms:.1f}ms")
        self.logger.info(f"📊 Extracted {field_count} fields with {len(warnings)} warnings")
        
        if warnings:
            self.logger.warning(f"⚠️ Parse warnings [{workflow_id}]: {warnings}")
        
        # Log pattern matching results if available
        if hasattr(parse_result, 'matched_patterns') and hasattr(parse_result, 'failed_patterns'):
            success_rate = len(parse_result.matched_patterns) / (len(parse_result.matched_patterns) + len(parse_result.failed_patterns)) if (parse_result.matched_patterns or parse_result.failed_patterns) else 0
            self.logger.info(f"🎯 Pattern success rate [{workflow_id}]: {success_rate:.1%} ({len(parse_result.matched_patterns)}/{len(parse_result.matched_patterns) + len(parse_result.failed_patterns)})")
    
    def log_dataframe_conversion(self, workflow_id: str, conversion_time_ms: float,
                                dataframe_shape: tuple, json_formatted: bool, 
                                json_size: int, json_keys: List[str]):
        """
        Log DataFrame conversion and JSON formatting results.
        
        Args:
            workflow_id: Workflow identifier
            conversion_time_ms: Time taken for conversion
            dataframe_shape: Shape of resulting DataFrame (rows, cols)
            json_formatted: Whether JSON was successfully formatted
            json_size: Size of formatted JSON
            json_keys: Top-level JSON keys
        """
        if workflow_id in self._active_workflows:
            self._active_workflows[workflow_id].dataframe_conversion_time_ms = conversion_time_ms
        
        self.logger.info(f"📊 DATAFRAME CONVERSION [{workflow_id}] - {dataframe_shape[0]} rows, {dataframe_shape[1]} cols in {conversion_time_ms:.1f}ms")
        
        if json_formatted:
            self.logger.info(f"✅ JSON formatting [{workflow_id}] - {json_size} chars with keys: {json_keys}")
        else:
            self.logger.warning(f"❌ JSON formatting failed [{workflow_id}] - using raw response fallback")
    
    def log_fsm_state_transition(self, workflow_id: str, from_state: str, to_state: str, 
                                 event: str, json_context: Dict[str, Any]):
        """
        Log FSM state transitions with JSON context.
        
        Args:
            workflow_id: Workflow identifier
            from_state: Previous FSM state
            to_state: New FSM state
            event: Transition event
            json_context: JSON-related context data
        """
        self.logger.info(f"🔄 FSM TRANSITION [{workflow_id}] - {from_state} → {to_state} (event: {event})")
        
        if json_context:
            self.logger.debug(f"📋 JSON context [{workflow_id}]: {json_context}")
    
    def log_error_condition(self, workflow_id: str, error: Exception, context: Dict[str, Any]):
        """
        Log error conditions with detailed context.
        
        Args:
            workflow_id: Workflow identifier
            error: Exception that occurred
            context: Error context information
        """
        self.logger.error(f"💥 ERROR [{workflow_id}] - {type(error).__name__}: {str(error)}")
        self.logger.error(f"📄 Error context [{workflow_id}]: {context}")
        self.logger.debug(f"📚 Stack trace [{workflow_id}]: {traceback.format_exc()}")
    
    def complete_workflow(self, workflow_id: str, final_confidence: str, 
                         final_field_count: int, ui_update_success: bool) -> Dict[str, Any]:
        """
        Complete workflow tracking and log final summary.
        
        Args:
            workflow_id: Workflow identifier
            final_confidence: Final confidence level
            final_field_count: Final number of extracted fields
            ui_update_success: Whether UI update was successful
            
        Returns:
            Complete workflow metrics dictionary
        """
        if workflow_id not in self._active_workflows:
            self.logger.warning(f"⚠️ Attempted to complete unknown workflow: {workflow_id}")
            return {}
        
        metrics = self._active_workflows[workflow_id]
        metrics.complete_workflow()
        
        confidence_emoji = "🎯" if final_confidence == "high" else "⚡" if final_confidence == "medium" else "⚠️"
        ui_emoji = "✅" if ui_update_success else "❌"
        
        self.logger.info(f"🏁 WORKFLOW COMPLETE [{workflow_id}] - {metrics.total_workflow_time_ms:.1f}ms total")
        self.logger.info(f"{confidence_emoji} Final result: {final_confidence} confidence, {final_field_count} fields")
        self.logger.info(f"{ui_emoji} UI update: {'successful' if ui_update_success else 'failed'}")
        
        # Log detailed performance breakdown
        metrics_dict = metrics.to_dict()
        self.logger.info(f"📈 Performance breakdown [{workflow_id}]: {metrics_dict}")
        
        # Cleanup completed workflow
        del self._active_workflows[workflow_id]
        
        return metrics_dict
    
    def _analyze_raw_response(self, text: str) -> Dict[str, Any]:
        """
        Analyze raw response text for JSON indicators.
        
        Args:
            text: Raw response text
            
        Returns:
            Analysis dictionary with various indicators
        """
        return {
            'total_length': len(text),
            'contains_json_block': '```json' in text.lower(),
            'contains_code_block': '```' in text,
            'contains_braces': '{' in text and '}' in text,
            'starts_with_brace': text.strip().startswith('{'),
            'ends_with_brace': text.strip().endswith('}'),
            'brace_count': text.count('{'),
            'quote_count': text.count('"'),
            'newline_count': text.count('\n'),
            'estimated_json_size': len(text) if text.strip().startswith('{') else 0,
            'potential_json_blocks': text.count('```json') + text.count('```JSON'),
            'has_error_indicators': any(indicator in text.lower() for indicator in ['error', 'failed', 'exception', 'invalid'])
        }
    
    def log_raw_json_output(self, workflow_id: str, button_type: str, 
                           formatted_json: str, is_valid_json: bool):
        """
        Log raw JSON output for debugging purposes.
        
        Args:
            workflow_id: Workflow identifier
            button_type: Type of analysis
            formatted_json: Formatted JSON string
            is_valid_json: Whether the JSON is valid
        """
        status = "VALID" if is_valid_json else "INVALID"
        self.logger.info(f"📄 RAW JSON OUTPUT [{workflow_id}] - {button_type.upper()} ({status})")
        self.logger.info(f"📄 JSON size: {len(formatted_json)} characters")
        
        # Always log the raw JSON for debugging (truncated if very large)
        if len(formatted_json) <= 2000:
            self.logger.debug(f"📄 Complete JSON [{workflow_id}]:\n{formatted_json}")
        else:
            self.logger.debug(f"📄 JSON preview [{workflow_id}] (first 2000 chars):\n{formatted_json[:2000]}...")
            self.logger.debug(f"📄 JSON end [{workflow_id}] (last 500 chars):\n...{formatted_json[-500:]}")
    
    def get_active_workflows(self) -> List[str]:
        """Get list of currently active workflow IDs"""
        return list(self._active_workflows.keys())
    
    def cleanup_stale_workflows(self, max_age_seconds: int = 300):
        """
        Clean up workflows that have been running too long.
        
        Args:
            max_age_seconds: Maximum age before considering a workflow stale
        """
        current_time = time.time()
        stale_workflows = []
        
        for workflow_id, metrics in self._active_workflows.items():
            age = current_time - metrics.workflow_start_time
            if age > max_age_seconds:
                stale_workflows.append(workflow_id)
        
        for workflow_id in stale_workflows:
            self.logger.warning(f"🧹 Cleaning up stale workflow: {workflow_id}")
            del self._active_workflows[workflow_id]


# Global instance for easy access
json_debug_logger = JsonDebugLogger()


def create_workflow_id(button_type: str, ticker: str) -> str:
    """
    Create a unique workflow ID for tracking.
    
    Args:
        button_type: Type of analysis button
        ticker: Stock ticker symbol
        
    Returns:
        Unique workflow identifier
    """
    timestamp = int(time.time() * 1000)  # millisecond precision
    return f"{button_type}_{ticker}_{timestamp}"


if __name__ == "__main__":
    # Quick test and demonstration
    print("🔍 JSON Debug Logger for Market Parser - Testing")
    print("=" * 60)
    
    # Test workflow
    test_workflow_id = create_workflow_id("snapshot", "AAPL")
    test_response = '{"snapshot_data": {"current_price": 150.25, "volume": 1000000}, "metadata": {"confidence": 0.95}}'
    
    # Start workflow
    metrics = json_debug_logger.start_json_workflow(
        test_workflow_id, "snapshot", "AAPL", test_response
    )
    
    # Log some test events
    json_debug_logger.log_json_extraction(
        test_workflow_id, 15.5, {"test": "data"}, "pattern_match", True
    )
    
    json_debug_logger.log_schema_validation(
        test_workflow_id, 8.2, {"valid": True, "schema_version": "1.0"}, "snapshot"
    )
    
    # Complete workflow
    final_metrics = json_debug_logger.complete_workflow(
        test_workflow_id, "high", 5, True
    )
    
    print(f"✅ Test completed. Final metrics: {final_metrics}")