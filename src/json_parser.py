"""
JSON-Based Response Parser for Market Parser

This module provides comprehensive JSON parsing capabilities for extracting structured
stock market data from AI-generated JSON responses. It replaces the regex-based
response_parser.py with robust JSON schema validation and extraction.

Classes:
    - JsonParser: Main parser class with methods for different data types
    - JsonParseResult: Data container for parse results with confidence scoring
    - JsonValidationError: Custom exception for JSON validation failures

Features:
    - JSON schema-based validation using json_schemas.py
    - Confidence scoring for parsed results
    - Data validation and normalization
    - Fallback strategies for malformed JSON
    - Comprehensive logging for debugging
    - Support for extracting attributes and metadata
    - Compatible API with response_parser.py for smooth transition
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
import datetime
import re
import time

# Import schema components
from .json_schemas import (
    SchemaRegistry, AnalysisType, SchemaVersion,
    SNAPSHOT_SCHEMA, SUPPORT_RESISTANCE_SCHEMA, TECHNICAL_SCHEMA
)


class ConfidenceLevel(Enum):
    """Confidence levels for parsed data quality"""
    HIGH = "high"        # Valid JSON with all required fields
    MEDIUM = "medium"    # Valid JSON with most required fields
    LOW = "low"         # Partial JSON or fallback parsing success
    FAILED = "failed"   # No meaningful data extracted


class JsonDataType(Enum):
    """Types of stock data that can be parsed"""
    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"


@dataclass
class JsonParseResult:
    """Container for JSON parsing results with metadata"""
    data_type: JsonDataType
    raw_response: str
    parsed_data: Dict[str, Any]
    confidence: ConfidenceLevel
    schema_validation: Dict[str, Any] = field(default_factory=dict)
    extraction_metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    parse_time_ms: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert parse result to dictionary for serialization"""
        return {
            'data_type': self.data_type.value,
            'parsed_data': self.parsed_data,
            'confidence': self.confidence.value,
            'schema_validation': self.schema_validation,
            'extraction_metadata': self.extraction_metadata,
            'warnings': self.warnings,
            'parse_time_ms': self.parse_time_ms
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert parsed data to DataFrame for display (compatible with UI)"""
        if not self.parsed_data:
            return pd.DataFrame({'Item': ['No Data'], 'Value': ['N/A']})
        
        if self.data_type == JsonDataType.SNAPSHOT:
            return self._to_snapshot_dataframe()
        elif self.data_type == JsonDataType.SUPPORT_RESISTANCE:
            return self._to_sr_dataframe()
        elif self.data_type == JsonDataType.TECHNICAL:
            return self._to_technical_dataframe()
        else:
            # Generic dataframe
            items = []
            for key, value in self.parsed_data.items():
                items.append({'Item': key, 'Value': str(value)})
            return pd.DataFrame(items)
    
    def _to_snapshot_dataframe(self) -> pd.DataFrame:
        """Convert snapshot JSON data to DataFrame"""
        items = []
        
        # Extract from nested JSON structure
        snapshot_data = self.parsed_data.get('snapshot_data', {})
        metadata = self.parsed_data.get('metadata', {})
        
        # Add key metrics in logical order
        if 'current_price' in snapshot_data:
            items.append({'Metric': 'Current Price', 'Value': f"${snapshot_data['current_price']:.2f}"})
        
        if 'percentage_change' in snapshot_data:
            items.append({'Metric': 'Percentage Change', 'Value': f"{snapshot_data['percentage_change']:+.1f}%"})
        
        if 'dollar_change' in snapshot_data:
            items.append({'Metric': 'Dollar Change', 'Value': f"${snapshot_data['dollar_change']:+.2f}"})
        
        if 'volume' in snapshot_data:
            items.append({'Metric': 'Volume', 'Value': f"{snapshot_data['volume']:,}"})
        
        if 'vwap' in snapshot_data:
            items.append({'Metric': 'VWAP', 'Value': f"${snapshot_data['vwap']:.2f}"})
        
        if 'open' in snapshot_data:
            items.append({'Metric': 'Open', 'Value': f"${snapshot_data['open']:.2f}"})
        
        if 'high' in snapshot_data:
            items.append({'Metric': 'High', 'Value': f"${snapshot_data['high']:.2f}"})
        
        if 'low' in snapshot_data:
            items.append({'Metric': 'Low', 'Value': f"${snapshot_data['low']:.2f}"})
        
        if 'close' in snapshot_data:
            items.append({'Metric': 'Previous Close', 'Value': f"${snapshot_data['close']:.2f}"})
        
        # Add metadata if available
        if 'confidence_score' in metadata:
            items.append({'Metric': 'Data Confidence', 'Value': f"{metadata['confidence_score']:.1%}"})
        
        return pd.DataFrame(items) if items else pd.DataFrame({'Metric': ['No Data'], 'Value': ['N/A']})
    
    def _to_sr_dataframe(self) -> pd.DataFrame:
        """Convert support/resistance JSON data to DataFrame"""
        items = []
        
        support_levels = self.parsed_data.get('support_levels', {})
        resistance_levels = self.parsed_data.get('resistance_levels', {})
        
        # Process support levels
        for level in ['S1', 'S2', 'S3']:
            if level in support_levels:
                level_data = support_levels[level]
                price = level_data.get('price', 0)
                strength = level_data.get('strength', 'unknown')
                confidence = level_data.get('confidence', 0)
                
                level_name = f"{level} (Support {level[1]})"
                value_str = f"${price:.2f} ({strength.title()}"
                if confidence:
                    value_str += f", {confidence:.0%}"
                value_str += ")"
                
                items.append({'Level': level_name, 'Price': value_str})
        
        # Process resistance levels
        for level in ['R1', 'R2', 'R3']:
            if level in resistance_levels:
                level_data = resistance_levels[level]
                price = level_data.get('price', 0)
                strength = level_data.get('strength', 'unknown')
                confidence = level_data.get('confidence', 0)
                
                level_name = f"{level} (Resistance {level[1]})"
                value_str = f"${price:.2f} ({strength.title()}"
                if confidence:
                    value_str += f", {confidence:.0%}"
                value_str += ")"
                
                items.append({'Level': level_name, 'Price': value_str})
        
        return pd.DataFrame(items) if items else pd.DataFrame({'Level': ['No Data'], 'Price': ['N/A']})
    
    def _to_technical_dataframe(self) -> pd.DataFrame:
        """Convert technical indicators JSON data to DataFrame"""
        items = []
        
        oscillators = self.parsed_data.get('oscillators', {})
        moving_averages = self.parsed_data.get('moving_averages', {})
        
        # Process oscillators
        if 'RSI' in oscillators:
            rsi_data = oscillators['RSI']
            value = rsi_data.get('value', 0)
            interpretation = rsi_data.get('interpretation', 'unknown')
            items.append({'Indicator': 'RSI', 'Value': f"{value:.1f} ({interpretation.title()})"})
        
        if 'MACD' in oscillators:
            macd_data = oscillators['MACD']
            value = macd_data.get('value', 0)
            signal = macd_data.get('signal', 0)
            histogram = macd_data.get('histogram', 0)
            interpretation = macd_data.get('interpretation', 'unknown')
            items.append({'Indicator': 'MACD', 'Value': f"{value:.3f} / {signal:.3f} ({interpretation.title()})"})
        
        # Process moving averages
        emas = moving_averages.get('exponential', {})
        smas = moving_averages.get('simple', {})
        
        for period in [5, 10, 20, 50, 200]:
            if f'EMA_{period}' in emas:
                items.append({'Indicator': f'EMA {period}', 'Value': f"${emas[f'EMA_{period}']:.2f}"})
            
            if f'SMA_{period}' in smas:
                items.append({'Indicator': f'SMA {period}', 'Value': f"${smas[f'SMA_{period}']:.2f}"})
        
        return pd.DataFrame(items) if items else pd.DataFrame({'Indicator': ['No Data'], 'Value': ['N/A']})


class JsonValidationError(Exception):
    """Custom exception for JSON validation failures"""
    pass


class JsonParser:
    """
    Dual-mode JSON parser for extracting structured stock data from AI responses.
    
    This class implements conditional processing for button (JSON) and user (text)
    responses with lightweight validation optimized for chat display.
    """
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the JsonParser.
        
        Args:
            log_level: Logging level for parser operations
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # Initialize schema registry
        self.schema_registry = SchemaRegistry()
        
        # Map our enum to schema enum
        self._type_mapping = {
            JsonDataType.SNAPSHOT: AnalysisType.SNAPSHOT,
            JsonDataType.SUPPORT_RESISTANCE: AnalysisType.SUPPORT_RESISTANCE,
            JsonDataType.TECHNICAL: AnalysisType.TECHNICAL
        }
        
        self.logger.info("JsonParser initialized with dual-mode processing and chat optimization")
    
    # ====== Dual-Mode Processing API ======
    
    def process_for_chat(self, response_text: str, source_type: str = 'user', 
                        data_type: Optional[JsonDataType] = None, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Process response for chat interface with conditional handling.
        
        Args:
            response_text: Raw AI response text
            source_type: 'button' for JSON parsing, 'user' for text pass-through
            data_type: Type of JSON data expected (for button responses)
            ticker: Stock ticker symbol for context
            
        Returns:
            Dict with chat-optimized processing results
        """
        import time
        start_time = time.time()
        
        self.logger.info(f"🔄 Processing {source_type} response for chat display")
        
        try:
            if source_type == 'button' and data_type:
                # Button response: Parse JSON with lightweight validation
                return self._process_button_for_chat(response_text, data_type, ticker)
            else:
                # User response: Pass through with basic formatting
                return self._process_user_for_chat(response_text)
                
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.logger.error(f"💥 Chat processing failed after {processing_time:.1f}ms: {e}")
            
            return {
                'success': False,
                'content': f"⚠️ Processing error: {str(e)}",
                'processing_time_ms': processing_time,
                'source_type': source_type,
                'error': str(e)
            }
    
    def _process_button_for_chat(self, response_text: str, data_type: JsonDataType, ticker: Optional[str]) -> Dict[str, Any]:
        """
        Process button response with JSON extraction for chat display.
        
        Args:
            response_text: AI response text
            data_type: Type of JSON data expected
            ticker: Stock ticker symbol
            
        Returns:
            Dict with chat-optimized button response
        """
        import time
        start_time = time.time()
        
        self.logger.info(f"🔘 Processing button response for {data_type.value}")
        
        # Parse JSON response
        parse_result = self._parse_json_response(response_text, data_type, ticker)
        processing_time = (time.time() - start_time) * 1000
        
        # Format for chat based on parsing success
        if parse_result.confidence in [ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM]:
            # Successful parsing - show response with JSON code block
            json_display = self._create_chat_json_display(parse_result)
            formatted_content = f"{response_text}\n\n**📊 Extracted Data:**\n```json\n{json_display}\n```"
            
            return {
                'success': True,
                'content': formatted_content,
                'structured_data': parse_result.parsed_data,
                'confidence': parse_result.confidence.value,
                'processing_time_ms': processing_time,
                'source_type': 'button',
                'data_type': data_type.value
            }
        else:
            # Parsing failed - show response with warning
            warning_msg = "⚠️ *Could not extract structured data from response*"
            formatted_content = f"{response_text}\n\n{warning_msg}"
            
            return {
                'success': False,
                'content': formatted_content,
                'processing_time_ms': processing_time,
                'source_type': 'button',
                'data_type': data_type.value,
                'warnings': parse_result.warnings
            }
    
    def _process_user_for_chat(self, response_text: str) -> Dict[str, Any]:
        """
        Process user response with minimal formatting for chat display.
        
        Args:
            response_text: AI response text
            
        Returns:
            Dict with chat-optimized user response
        """
        import time
        start_time = time.time()
        
        # Simple text cleanup for better chat display
        cleaned_content = self._clean_for_chat_display(response_text)
        processing_time = (time.time() - start_time) * 1000
        
        self.logger.info(f"✅ User response processed for chat in {processing_time:.1f}ms")
        
        return {
            'success': True,
            'content': cleaned_content,
            'processing_time_ms': processing_time,
            'source_type': 'user'
        }
    
    def _create_chat_json_display(self, parse_result: JsonParseResult) -> str:
        """
        Create JSON display optimized for chat interface.
        
        Args:
            parse_result: JSON parsing result
            
        Returns:
            Formatted JSON string for chat display
        """
        import json
        
        # Create simplified display format
        chat_data = {
            'analysis_type': parse_result.data_type.value,
            'confidence': parse_result.confidence.value,
            'data': parse_result.parsed_data
        }
        
        # Add processing metadata for transparency
        if parse_result.extraction_metadata:
            chat_data['processing_info'] = {
                'extraction_method': parse_result.extraction_metadata.get('extraction_method', 'json'),
                'processing_time_ms': parse_result.parse_time_ms
            }
        
        return json.dumps(chat_data, indent=2)
    
    def _clean_for_chat_display(self, text: str) -> str:
        """
        Clean text response for optimal chat display.
        
        Args:
            text: Raw response text
            
        Returns:
            Cleaned text for chat display
        """
        import re
        
        # Normalize whitespace and line breaks for chat
        cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Reduce excessive line breaks
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)  # Normalize spaces
        cleaned = cleaned.strip()
        
        return cleaned
    
    # ====== Original JSON Processing API (Maintained for Compatibility) ======
    
    def parse_stock_snapshot(self, text: str, ticker: Optional[str] = None) -> JsonParseResult:
        """
        Parse stock snapshot data from AI JSON response.
        
        Args:
            text: Raw AI response text (should contain JSON)
            ticker: Stock ticker symbol for context
            
        Returns:
            JsonParseResult with parsed snapshot data
        """
        return self._parse_json_response(
            text, JsonDataType.SNAPSHOT, ticker
        )
    
    def parse_support_resistance(self, text: str, ticker: Optional[str] = None) -> JsonParseResult:
        """
        Parse support and resistance levels from AI JSON response.
        
        Args:
            text: Raw AI response text (should contain JSON)
            ticker: Stock ticker symbol for context
            
        Returns:
            JsonParseResult with parsed S&R data
        """
        return self._parse_json_response(
            text, JsonDataType.SUPPORT_RESISTANCE, ticker
        )
    
    def parse_technical_indicators(self, text: str, ticker: Optional[str] = None) -> JsonParseResult:
        """
        Parse technical indicators from AI JSON response.
        
        Args:
            text: Raw AI response text (should contain JSON)
            ticker: Stock ticker symbol for context
            
        Returns:
            JsonParseResult with parsed technical data
        """
        return self._parse_json_response(
            text, JsonDataType.TECHNICAL, ticker
        )
    
    def parse_any(self, text: str, data_type: JsonDataType, ticker: Optional[str] = None) -> JsonParseResult:
        """
        Generic parser that routes to appropriate method based on data type.
        
        Args:
            text: Raw AI response text
            data_type: Type of data to parse
            ticker: Stock ticker symbol for context
            
        Returns:
            JsonParseResult with parsed data
        """
        if data_type == JsonDataType.SNAPSHOT:
            return self.parse_stock_snapshot(text, ticker)
        elif data_type == JsonDataType.SUPPORT_RESISTANCE:
            return self.parse_support_resistance(text, ticker)
        elif data_type == JsonDataType.TECHNICAL:
            return self.parse_technical_indicators(text, ticker)
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    
    # ====== Core Parsing Logic ======
    
    def _parse_json_response(self, text: str, data_type: JsonDataType, ticker: Optional[str] = None) -> JsonParseResult:
        """
        Core method to parse JSON response with schema validation and fallbacks.
        
        Args:
            text: Raw response text
            data_type: Type of data expected
            ticker: Optional ticker symbol
            
        Returns:
            JsonParseResult with parsed data and metadata
        """
        start_time = time.time()
        
        # 🔍 COMPREHENSIVE JSON DEBUG LOGGING
        self.logger.info(f"🚀 Starting JSON parsing for {data_type.value} from {len(text)} character response")
        
        # Log raw response for debugging (first 500 chars)
        self.logger.debug(f"📄 Raw response preview: {repr(text[:500])}")
        if len(text) > 500:
            self.logger.debug(f"📄 Raw response continuation: {repr(text[500:1000])}")
        
        # Analyze response structure for debugging
        json_indicators = {
            'contains_braces': '{' in text and '}' in text,
            'contains_json_block': '```json' in text.lower(),
            'contains_code_block': '```' in text,
            'brace_count': text.count('{'),
            'quote_count': text.count('"'),
            'starts_with_brace': text.strip().startswith('{'),
            'ends_with_brace': text.strip().endswith('}'),
            'estimated_json_size': len(text) if text.strip().startswith('{') else 0
        }
        
        self.logger.info(f"📊 Response analysis: {json_indicators}")
        
        # Log character distribution for debugging parsing issues
        special_chars = {'newlines': text.count('\n'), 'returns': text.count('\r'), 
                        'tabs': text.count('\t'), 'spaces': text.count(' ')}
        self.logger.debug(f"📈 Character distribution: {special_chars}")
        
        result = JsonParseResult(
            data_type=data_type,
            raw_response=text,
            parsed_data={},
            confidence=ConfidenceLevel.FAILED
        )
        
        if ticker:
            result.extraction_metadata['ticker'] = ticker.upper()
        
        try:
            # Step 1: Extract JSON from response with detailed logging
            self.logger.info(f"🔍 Step 1: Extracting JSON from {data_type.value} response")
            json_extraction_start = time.time()
            
            json_data = self._extract_json_from_text(text)
            json_extraction_time = (time.time() - json_extraction_start) * 1000
            
            if json_data is None:
                self.logger.warning(f"❌ No valid JSON extracted after {json_extraction_time:.1f}ms")
                self.logger.info(f"🔄 Attempting fallback parsing for {data_type.value}")
                return self._fallback_parse(text, data_type, ticker, result)
            
            # Log successful JSON extraction
            json_size = len(json.dumps(json_data))
            json_keys = list(json_data.keys()) if isinstance(json_data, dict) else 'non-dict'
            self.logger.info(f"✅ JSON extracted successfully in {json_extraction_time:.1f}ms")
            self.logger.info(f"📦 Extracted JSON size: {json_size} chars, keys: {json_keys}")
            self.logger.debug(f"🔧 Complete extracted JSON: {json.dumps(json_data, indent=2)}")
            
            # Step 2: Schema validation with comprehensive logging
            self.logger.info(f"🔍 Step 2: Validating {data_type.value} JSON against schema")
            validation_start = time.time()
            
            schema_type = self._type_mapping[data_type]
            validation_result = {'valid': False, 'error_message': 'Validation skipped'}
            
            try:
                self.logger.debug(f"📋 Using schema type: {schema_type}")
                validation_result = self.schema_registry.validate_response(json_data, schema_type)
                validation_time = (time.time() - validation_start) * 1000
                
                if validation_result.get('valid', False):
                    self.logger.info(f"✅ Schema validation successful in {validation_time:.1f}ms")
                    self.logger.debug(f"📊 Validation details: {validation_result}")
                else:
                    self.logger.warning(f"⚠️ Schema validation failed in {validation_time:.1f}ms")
                    self.logger.warning(f"❌ Validation error: {validation_result.get('error_message', 'Unknown')}")
                    
            except Exception as e:
                validation_time = (time.time() - validation_start) * 1000
                self.logger.error(f"💥 Schema validation exception in {validation_time:.1f}ms: {e}")
                validation_result = {'valid': False, 'error_message': f"Validation error: {str(e)}"}
            
            result.schema_validation = validation_result
            self.logger.debug(f"📋 Final validation result: {validation_result}")
            
            if validation_result.get('valid', False):
                # Valid JSON schema - high confidence
                result.parsed_data = json_data
                result.confidence = ConfidenceLevel.HIGH
                result.extraction_metadata['extraction_method'] = 'schema_validated'
                
                # Log successful schema validation with details
                data_fields = self._count_data_fields(json_data, data_type)
                self.logger.info(f"🎯 HIGH CONFIDENCE: Successfully validated {data_type.value} JSON against schema")
                self.logger.info(f"📊 Extracted data fields: {data_fields}")
                self.logger.debug(f"✅ Validated data structure: {json.dumps(json_data, indent=2)[:1000]}...")
                
            else:
                # Invalid or no schema validation - try partial extraction with detailed logging
                self.logger.info(f"🔍 Step 3: Schema validation failed, attempting partial extraction")
                self.logger.warning(f"❌ Schema validation issue: {validation_result.get('error_message', 'Unknown error')}")
                
                partial_extraction_start = time.time()
                extracted_data = self._extract_partial_data(json_data, data_type)
                partial_extraction_time = (time.time() - partial_extraction_start) * 1000
                
                if extracted_data:
                    result.parsed_data = extracted_data
                    result.confidence = ConfidenceLevel.MEDIUM
                    result.extraction_metadata['extraction_method'] = 'partial_json'
                    result.warnings.append(f"Schema validation issue but data extracted successfully")
                    
                    # Log partial extraction success
                    data_fields = self._count_data_fields(extracted_data, data_type)
                    self.logger.info(f"⚡ MEDIUM CONFIDENCE: Partial extraction successful in {partial_extraction_time:.1f}ms")
                    self.logger.info(f"📊 Partially extracted data fields: {data_fields}")
                    self.logger.debug(f"🔧 Partial data structure: {json.dumps(extracted_data, indent=2)}")
                else:
                    self.logger.warning(f"❌ Partial extraction failed in {partial_extraction_time:.1f}ms")
                    self.logger.info(f"🔄 Falling back to regex parsing for {data_type.value}")
                    return self._fallback_parse(text, data_type, ticker, result)
            
            # Step 4: Add comprehensive extraction metadata
            extraction_metadata = {
                'json_size_chars': len(json.dumps(json_data)),
                'schema_version': validation_result.get('schema_version', 'unknown'),
                'validation_timestamp': validation_result.get('validation_timestamp', 'unknown'),
                'json_extraction_time_ms': json_extraction_time,
                'validation_time_ms': validation_time if 'validation_time' in locals() else 0,
                'response_size_chars': len(text),
                'extraction_success_ratio': len(json.dumps(json_data)) / len(text) if len(text) > 0 else 0
            }
            result.extraction_metadata.update(extraction_metadata)
            
            self.logger.info(f"📈 Extraction metadata: {extraction_metadata}")
            
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            self.logger.error(f"💥 JSON parsing failed after {total_time:.1f}ms: {e}")
            self.logger.error(f"📄 Failed on response: {repr(text[:200])}...")
            result.warnings.append(f"Parsing error: {str(e)}")
            
            # Try fallback parsing as last resort with timing
            self.logger.info(f"🔄 Attempting emergency fallback parsing for {data_type.value}")
            fallback_start = time.time()
            
            try:
                fallback_result = self._fallback_parse(text, data_type, ticker, result)
                fallback_time = (time.time() - fallback_start) * 1000
                fallback_result.parse_time_ms = (time.time() - start_time) * 1000
                
                self.logger.info(f"🆘 Fallback parsing completed in {fallback_time:.1f}ms")
                return fallback_result
                
            except Exception as fallback_error:
                fallback_time = (time.time() - fallback_start) * 1000
                self.logger.error(f"💥 Fallback parsing also failed after {fallback_time:.1f}ms: {fallback_error}")
                result.warnings.append(f"Fallback parsing failed: {str(fallback_error)}")
        
        # Always set parse time and log final results
        total_parse_time = (time.time() - start_time) * 1000
        result.parse_time_ms = total_parse_time
        
        # Log final parsing summary
        self.logger.info(f"🏁 JSON parsing completed in {total_parse_time:.1f}ms")
        self.logger.info(f"📊 Final result: confidence={result.confidence.value}, fields={len(result.parsed_data)}, warnings={len(result.warnings)}")
        
        if result.warnings:
            self.logger.warning(f"⚠️ Parsing warnings: {result.warnings}")
            
        return result
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON object from text response, handling various formats.
        
        Args:
            text: Raw response text
            
        Returns:
            Parsed JSON object or None if no valid JSON found
        """
        self.logger.debug(f"🔍 Attempting JSON extraction from {len(text)} character text")
        
        # Strategy 1: Look for complete JSON objects with detailed logging
        json_patterns = [
            r'```json\s*(\{.*?\})\s*```',  # JSON code blocks
            r'```\s*(\{.*?\})\s*```',      # Generic code blocks
            r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})',  # Balanced braces
        ]
        
        self.logger.debug(f"📋 Strategy 1: Testing {len(json_patterns)} JSON patterns")
        
        for i, pattern in enumerate(json_patterns, 1):
            self.logger.debug(f"🔎 Testing pattern {i}: {pattern[:50]}...")
            matches = re.findall(pattern, text, re.DOTALL)
            self.logger.debug(f"📊 Pattern {i} found {len(matches)} potential matches")
            
            for j, match in enumerate(matches):
                try:
                    self.logger.debug(f"🧪 Attempting to parse match {j+1}: {repr(match[:100])}...")
                    parsed_json = json.loads(match)
                    self.logger.info(f"✅ Successfully parsed JSON using pattern {i}, match {j+1}")
                    self.logger.debug(f"🎯 Parsed JSON keys: {list(parsed_json.keys()) if isinstance(parsed_json, dict) else 'non-dict'}")
                    return parsed_json
                except json.JSONDecodeError as e:
                    self.logger.debug(f"❌ Match {j+1} failed to parse: {e}")
                    continue
        
        # Strategy 2: Try parsing the entire text as JSON
        self.logger.debug(f"📋 Strategy 2: Attempting to parse entire text as JSON")
        try:
            stripped_text = text.strip()
            self.logger.debug(f"🧪 Parsing entire text (length: {len(stripped_text)}): {repr(stripped_text[:100])}...")
            parsed_json = json.loads(stripped_text)
            self.logger.info(f"✅ Successfully parsed entire text as JSON")
            return parsed_json
        except json.JSONDecodeError as e:
            self.logger.debug(f"❌ Entire text parsing failed: {e}")
        
        # Strategy 3: Look for JSON-like structures and attempt repair
        self.logger.debug(f"📋 Strategy 3: Attempting JSON repair on malformed content")
        potential_json = self._attempt_json_repair(text)
        if potential_json:
            self.logger.debug(f"🔧 Repair attempt produced: {repr(potential_json[:100])}...")
            try:
                parsed_json = json.loads(potential_json)
                self.logger.info(f"✅ Successfully parsed repaired JSON")
                return parsed_json
            except json.JSONDecodeError as e:
                self.logger.debug(f"❌ Repaired JSON still failed to parse: {e}")
        else:
            self.logger.debug(f"❌ JSON repair could not extract valid structure")
        
        self.logger.warning(f"💀 All JSON extraction strategies failed")
        return None
    
    def _attempt_json_repair(self, text: str) -> Optional[str]:
        """
        Attempt to repair malformed JSON by fixing common issues.
        
        Args:
            text: Text that might contain malformed JSON
            
        Returns:
            Repaired JSON string or None
        """
        # Find JSON-like content
        json_start = text.find('{')
        json_end = text.rfind('}')
        
        if json_start == -1 or json_end == -1 or json_start >= json_end:
            return None
        
        potential_json = text[json_start:json_end + 1]
        
        # Common repairs
        repairs = [
            # Fix unquoted keys
            (r'(\w+):', r'"\1":'),
            # Fix single quotes to double quotes
            (r"'([^']*)'", r'"\1"'),
            # Fix trailing commas
            (r',(\s*[}\]])', r'\1'),
        ]
        
        for pattern, replacement in repairs:
            potential_json = re.sub(pattern, replacement, potential_json)
        
        return potential_json
    
    def _extract_partial_data(self, json_data: Dict[str, Any], data_type: JsonDataType) -> Dict[str, Any]:
        """
        Extract usable data from JSON that failed schema validation.
        
        Args:
            json_data: JSON object that failed validation
            data_type: Expected data type
            
        Returns:
            Extracted data dictionary
        """
        extracted = {}
        
        if data_type == JsonDataType.SNAPSHOT:
            # Look for snapshot-like data structures
            snapshot_fields = ['current_price', 'percentage_change', 'dollar_change', 
                             'volume', 'vwap', 'open', 'high', 'low', 'close']
            
            # Check root level first
            for field in snapshot_fields:
                if field in json_data:
                    extracted[field] = json_data[field]
            
            # Check nested snapshot_data
            if 'snapshot_data' in json_data:
                snapshot_data = json_data['snapshot_data']
                if isinstance(snapshot_data, dict):
                    for field in snapshot_fields:
                        if field in snapshot_data:
                            if 'snapshot_data' not in extracted:
                                extracted['snapshot_data'] = {}
                            extracted['snapshot_data'][field] = snapshot_data[field]
            
            # Extract metadata if available
            if 'metadata' in json_data and isinstance(json_data['metadata'], dict):
                extracted['metadata'] = json_data['metadata']
        
        elif data_type == JsonDataType.SUPPORT_RESISTANCE:
            # Look for support/resistance data
            sr_levels = ['S1', 'S2', 'S3', 'R1', 'R2', 'R3']
            
            # Check root level
            for level in sr_levels:
                if level in json_data:
                    extracted[level] = json_data[level]
            
            # Check nested structures
            if 'support_levels' in json_data:
                extracted['support_levels'] = json_data['support_levels']
            if 'resistance_levels' in json_data:
                extracted['resistance_levels'] = json_data['resistance_levels']
            if 'metadata' in json_data:
                extracted['metadata'] = json_data['metadata']
        
        elif data_type == JsonDataType.TECHNICAL:
            # Look for technical indicator data
            if 'oscillators' in json_data:
                extracted['oscillators'] = json_data['oscillators']
            if 'moving_averages' in json_data:
                extracted['moving_averages'] = json_data['moving_averages']
            if 'metadata' in json_data:
                extracted['metadata'] = json_data['metadata']
        
        # Log partial extraction results
        if extracted:
            self.logger.debug(f"🔧 Partial extraction successful: {len(extracted)} top-level keys")
            self.logger.debug(f"📊 Extracted keys: {list(extracted.keys())}")
        else:
            self.logger.debug(f"❌ Partial extraction found no usable data")
            
        return extracted
    
    def _fallback_parse(self, text: str, data_type: JsonDataType, ticker: Optional[str], 
                       result: JsonParseResult) -> JsonParseResult:
        """
        Fallback to regex-based parsing when JSON parsing fails.
        
        Args:
            text: Raw response text
            data_type: Expected data type
            ticker: Optional ticker symbol
            result: Existing result object to update
            
        Returns:
            Updated JsonParseResult with fallback data
        """
        fallback_start = time.time()
        self.logger.info(f"🆘 FALLBACK: Attempting regex-based parsing for {data_type.value}")
        self.logger.debug(f"📄 Fallback input preview: {repr(text[:200])}...")
        
        # Import and use the original regex parser as fallback
        try:
            from response_parser import ResponseParser, DataType
            
            # Map our types to legacy types
            legacy_type_map = {
                JsonDataType.SNAPSHOT: DataType.SNAPSHOT,
                JsonDataType.SUPPORT_RESISTANCE: DataType.SUPPORT_RESISTANCE,
                JsonDataType.TECHNICAL: DataType.TECHNICAL
            }
            
            legacy_parser = ResponseParser(log_level=logging.WARNING)  # Reduce noise
            legacy_result = legacy_parser.parse_any(text, legacy_type_map[data_type], ticker)
            
            if legacy_result.parsed_data:
                # Convert legacy result to our format with detailed logging
                result.parsed_data = legacy_result.parsed_data
                
                # Map confidence levels
                confidence_map = {
                    'high': ConfidenceLevel.HIGH,
                    'medium': ConfidenceLevel.MEDIUM,
                    'low': ConfidenceLevel.LOW,
                    'failed': ConfidenceLevel.FAILED
                }
                result.confidence = confidence_map.get(legacy_result.confidence.value, ConfidenceLevel.LOW)
                
                fallback_time = (time.time() - fallback_start) * 1000
                result.extraction_metadata['extraction_method'] = 'regex_fallback'
                result.extraction_metadata['fallback_patterns_matched'] = len(legacy_result.matched_patterns)
                result.extraction_metadata['fallback_time_ms'] = fallback_time
                result.warnings.extend(legacy_result.warnings)
                result.warnings.append("Used regex fallback parsing due to JSON extraction failure")
                
                self.logger.info(f"✅ Fallback parsing successful in {fallback_time:.1f}ms: {len(legacy_result.parsed_data)} fields extracted")
                self.logger.info(f"📊 Fallback confidence: {result.confidence.value}, patterns matched: {len(legacy_result.matched_patterns)}")
                self.logger.debug(f"🔧 Fallback extracted data: {legacy_result.parsed_data}")
            else:
                fallback_time = (time.time() - fallback_start) * 1000
                self.logger.error(f"💀 Fallback parsing failed in {fallback_time:.1f}ms - no data extracted")
                result.warnings.append("All parsing methods failed - no data extracted")
                
        except ImportError:
            fallback_time = (time.time() - fallback_start) * 1000
            self.logger.error(f"💥 Fallback parser not available after {fallback_time:.1f}ms")
            result.warnings.append("Fallback parser not available")
        except Exception as e:
            fallback_time = (time.time() - fallback_start) * 1000
            self.logger.error(f"💥 Fallback parsing failed after {fallback_time:.1f}ms: {e}")
            result.warnings.append(f"Fallback parsing failed: {e}")
        
        return result
    
    # ====== Utility Methods ======
    
    def _count_data_fields(self, data: Dict[str, Any], data_type: JsonDataType) -> Dict[str, int]:
        """
        Count extracted data fields for logging purposes.
        
        Args:
            data: Extracted data dictionary
            data_type: Type of data
            
        Returns:
            Dictionary with field counts
        """
        counts = {'total_keys': len(data)}
        
        if data_type == JsonDataType.SNAPSHOT:
            snapshot_data = data.get('snapshot_data', {})
            counts['snapshot_fields'] = len(snapshot_data) if isinstance(snapshot_data, dict) else 0
            counts['has_metadata'] = 'metadata' in data
            
        elif data_type == JsonDataType.SUPPORT_RESISTANCE:
            counts['support_levels'] = len(data.get('support_levels', {}))
            counts['resistance_levels'] = len(data.get('resistance_levels', {}))
            counts['has_metadata'] = 'metadata' in data
            
        elif data_type == JsonDataType.TECHNICAL:
            counts['oscillators'] = len(data.get('oscillators', {}))
            counts['moving_averages'] = len(data.get('moving_averages', {}))
            counts['has_metadata'] = 'metadata' in data
            
        return counts
    
    def get_parsing_statistics(self) -> Dict[str, Any]:
        """Get statistics about the parser's capabilities"""
        return {
            'supported_schemas': len(self.schema_registry.schemas),
            'schema_versions': [schema.get('version', 'unknown') for schema in self.schema_registry.schemas.values()],
            'has_fallback_parser': True,  # We have regex fallback
            'supported_data_types': [dt.value for dt in JsonDataType],
            'validation_enabled': True
        }
    
    def validate_json_response(self, json_data: Dict[str, Any], data_type: JsonDataType) -> Dict[str, Any]:
        """
        Validate JSON response against appropriate schema.
        
        Args:
            json_data: JSON data to validate
            data_type: Expected data type
            
        Returns:
            Validation result dictionary
        """
        schema_type = self._type_mapping[data_type]
        return self.schema_registry.validate_response(json_data, schema_type)


# ====== Compatibility Functions ======

def create_compatible_parser() -> JsonParser:
    """Create a JsonParser instance with logging configured for production"""
    return JsonParser(log_level=logging.INFO)


def parse_stock_data(text: str, data_type: str, ticker: Optional[str] = None) -> JsonParseResult:
    """
    Convenience function for parsing stock data with string data types.
    
    Args:
        text: Raw response text
        data_type: String data type ('snapshot', 'support_resistance', 'technical')
        ticker: Optional ticker symbol
        
    Returns:
        JsonParseResult with parsed data
    """
    parser = create_compatible_parser()
    
    # Map string types to enum
    type_map = {
        'snapshot': JsonDataType.SNAPSHOT,
        'support_resistance': JsonDataType.SUPPORT_RESISTANCE,
        'technical': JsonDataType.TECHNICAL
    }
    
    if data_type not in type_map:
        raise ValueError(f"Unknown data type: {data_type}. Supported: {list(type_map.keys())}")
    
    return parser.parse_any(text, type_map[data_type], ticker)


if __name__ == "__main__":
    # Quick test and demonstration
    print("🔧 JSON Parser for Market Parser - Ready for Production")
    print("=" * 60)
    
    parser = create_compatible_parser()
    stats = parser.get_parsing_statistics()
    
    print(f"📊 Parser Statistics:")
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    
    print(f"\n✅ JSON Parser initialized and ready to replace response_parser.py")
    print(f"🔗 Compatible API maintained for seamless integration")
    print(f"📋 Schema validation enabled with fallback support")