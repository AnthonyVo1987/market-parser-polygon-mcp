"""
Stock Data Response Parser

This module provides comprehensive parsing capabilities for extracting structured
stock market data from AI-generated responses. It implements robust parsing with
multiple extraction strategies, data validation, and comprehensive error handling.

Classes:
    - ResponseParser: Main parser class with methods for different data types
    - ParseResult: Data container for parse results with confidence scoring
    - ValidationError: Custom exception for data validation failures

Features:
    - Multiple extraction patterns per data type for improved accuracy
    - Confidence scoring for parsed results
    - Data validation and normalization
    - Fallback strategies for parse failures
    - Comprehensive logging for debugging
    - Support for extracting attributes and metadata
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
from decimal import Decimal, InvalidOperation
import json


class ConfidenceLevel(Enum):
    """Confidence levels for parsed data quality"""
    HIGH = "high"        # > 80% patterns matched
    MEDIUM = "medium"    # 50-80% patterns matched
    LOW = "low"         # < 50% patterns matched
    FAILED = "failed"   # No meaningful data extracted


class DataType(Enum):
    """Types of stock data that can be parsed"""
    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"


@dataclass
class ParseResult:
    """Container for parsing results with metadata"""
    data_type: DataType
    raw_response: str
    parsed_data: Dict[str, Any]
    confidence: ConfidenceLevel
    matched_patterns: List[str] = field(default_factory=list)
    failed_patterns: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    parse_time_ms: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert parse result to dictionary for serialization"""
        return {
            'data_type': self.data_type.value,
            'parsed_data': self.parsed_data,
            'confidence': self.confidence.value,
            'matched_patterns': self.matched_patterns,
            'failed_patterns': self.failed_patterns,
            'attributes': self.attributes,
            'warnings': self.warnings,
            'parse_time_ms': self.parse_time_ms
        }
    
    def get_json_output(self) -> str:
        """Get formatted JSON output for display"""
        import json
        output_data = {
            'data_type': self.data_type.value,
            'confidence': self.confidence.value,
            'parsed_data': self.parsed_data,
            'metadata': {
                'matched_patterns': len(self.matched_patterns),
                'failed_patterns': len(self.failed_patterns),
                'parse_time_ms': self.parse_time_ms
            }
        }
        return json.dumps(output_data, indent=2)
    
    # DataFrame conversion methods removed for backend simplification
    # JSON output is now handled by get_json_output() method


class ValidationError(Exception):
    """Custom exception for data validation failures"""
    pass


class ResponseParser:
    """
    Dual-mode parser for extracting structured stock data from AI responses.
    
    This class implements conditional processing for button (JSON) and user (text)
    responses with lightweight parsing optimized for chat display.
    """
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the ResponseParser with dual-mode capabilities.
        
        Args:
            log_level: Logging level for parser operations
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # Initialize pattern libraries for JSON mode fallback
        self._snapshot_patterns = self._build_snapshot_patterns()
        self._sr_patterns = self._build_sr_patterns()
        self._technical_patterns = self._build_technical_patterns()
        
        # Data validators
        self._validators = self._build_validators()
        
        self.logger.info("ResponseParser initialized with dual-mode processing capabilities")
    
    # ====== Dual-Mode Processing API ======
    
    def process_response(self, response_text: str, source_type: str = 'user', 
                        data_type: Optional[DataType] = None, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Process response based on source type (button vs user) with appropriate handling.
        
        Args:
            response_text: Raw AI response text
            source_type: 'button' for structured data, 'user' for conversational text
            data_type: Type of structured data (for button responses)
            ticker: Stock ticker symbol for context
            
        Returns:
            Dict with processing results including formatted output for chat display
        """
        import time
        start_time = time.time()
        
        self.logger.info(f"Processing {source_type} response ({len(response_text)} chars)")
        
        try:
            if source_type == 'button' and data_type:
                # Button response: Parse JSON and format for chat
                return self._process_button_response(response_text, data_type, ticker)
            else:
                # User response: Pass through with basic formatting
                return self._process_user_response(response_text)
                
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.logger.error(f"Response processing failed after {processing_time:.1f}ms: {e}")
            return {
                'success': False,
                'content': f"⚠️ Response processing error: {str(e)}",
                'processing_time_ms': processing_time,
                'source_type': source_type,
                'error': str(e)
            }
    
    def _process_button_response(self, response_text: str, data_type: DataType, ticker: Optional[str]) -> Dict[str, Any]:
        """
        Process button response with JSON parsing and chat formatting.
        
        Args:
            response_text: AI response text
            data_type: Type of structured data expected
            ticker: Stock ticker symbol
            
        Returns:
            Dict with processed button response
        """
        import time
        start_time = time.time()
        
        # Try to parse structured data
        parse_result = self.parse_any(response_text, data_type, ticker)
        processing_time = (time.time() - start_time) * 1000
        
        # Format for chat display
        if parse_result.parsed_data and parse_result.confidence != ConfidenceLevel.FAILED:
            # Format JSON data for chat display
            json_content = self._format_json_for_chat(parse_result, data_type)
            formatted_content = f"{response_text}\n\n**📊 Extracted Data:**\n```json\n{json_content}\n```"
            
            return {
                'success': True,
                'content': formatted_content,
                'structured_data': parse_result.parsed_data,
                'confidence': parse_result.confidence.value,
                'processing_time_ms': processing_time,
                'source_type': 'button',
                'data_type': data_type.value,
                'warnings': parse_result.warnings
            }
        else:
            # Parsing failed, return response with warning
            warning_content = f"{response_text}\n\n⚠️ *Note: Could not extract structured data from response*"
            
            return {
                'success': False,
                'content': warning_content,
                'processing_time_ms': processing_time,
                'source_type': 'button',
                'data_type': data_type.value,
                'warnings': parse_result.warnings
            }
    
    def _process_user_response(self, response_text: str) -> Dict[str, Any]:
        """
        Process user response with pass-through handling.
        
        Args:
            response_text: AI response text
            
        Returns:
            Dict with processed user response
        """
        import time
        start_time = time.time()
        
        # Basic text cleanup for chat display
        cleaned_content = self._clean_text_response(response_text)
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'success': True,
            'content': cleaned_content,
            'processing_time_ms': processing_time,
            'source_type': 'user'
        }
    
    def _format_json_for_chat(self, parse_result: ParseResult, data_type: DataType) -> str:
        """
        Format parsed JSON data for chat display.
        
        Args:
            parse_result: Parsing result with structured data
            data_type: Type of structured data
            
        Returns:
            Formatted JSON string for chat display
        """
        import json
        
        # Create summary format for chat
        summary_data = {
            'analysis_type': data_type.value,
            'confidence': parse_result.confidence.value,
            'data': parse_result.parsed_data
        }
        
        # Add metadata if available
        if parse_result.attributes:
            summary_data['metadata'] = {
                'extraction_success_rate': parse_result.attributes.get('extraction_success_rate', 'unknown'),
                'total_fields': parse_result.attributes.get('total_fields', 0),
                'extracted_fields': parse_result.attributes.get('extracted_fields', 0)
            }
        
        return json.dumps(summary_data, indent=2)
    
    def _clean_text_response(self, text: str) -> str:
        """
        Clean user response text for chat display.
        
        Args:
            text: Raw response text
            
        Returns:
            Cleaned text for display
        """
        import re
        
        # Basic cleanup - remove excessive whitespace and normalize line endings
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Reduce multiple newlines
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)  # Normalize spaces and tabs
        cleaned = cleaned.strip()
        
        return cleaned
    
    # ====== Original Public API Methods (Maintained for Compatibility) ======
    
    def parse_stock_snapshot(self, text: str, ticker: Optional[str] = None) -> ParseResult:
        """
        Parse stock snapshot data from AI response.
        
        Args:
            text: Raw AI response text
            ticker: Stock ticker symbol for context
            
        Returns:
            ParseResult with parsed snapshot data
        """
        import time
        start_time = time.time()
        
        # Secure logging: Record parsing attempt without exposing sensitive data
        self.logger.info(f"Parsing stock snapshot from {len(text)} character response")
        self.logger.debug(f"Response contains key indicators: price={bool('price' in text.lower())}, percent={'%' in text}, dollar={'$' in text}")
        
        # CRITICAL DEBUG: Production bug investigation
        self.logger.error("🚨 CRITICAL DEBUG: Parser input analysis for production bug investigation")
        self.logger.error(f"Input type: {type(text)}")
        self.logger.error(f"Input length: {len(text)} characters")
        self.logger.error(f"Input repr (first 500 chars): {repr(text[:500])}")
        self.logger.error(f"Input content (first 500 chars):\n{text[:500]}")
        
        # Check for key financial indicators
        price_count = len(re.findall(r'price', text, re.IGNORECASE))
        dollar_count = text.count('$')
        percent_count = text.count('%')
        volume_count = len(re.findall(r'volume', text, re.IGNORECASE))
        
        self.logger.error(f"Financial indicators: price={price_count}, $={dollar_count}, %={percent_count}, volume={volume_count}")
        
        # Test critical patterns manually for detailed debugging
        test_patterns = {
            'current_price': r'(?:current\s+)?price[:\s]*\$?\s*([\d,]+\.\d+)',
            'percentage': r'([\+\-]?[\d\.]+)%',
            'dollar_value': r'\$\s*([\d,]+\.\d+)',
            'volume': r'volume[:\s]*([\d,]+(?:\.\d+)?[KMB]?)'
        }
        
        for name, pattern in test_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            self.logger.error(f"Pattern '{name}': {len(matches)} matches - {matches[:3]}")
        
        # Show context around each $ sign for debugging
        dollar_positions = [m.start() for m in re.finditer(r'\$', text)]
        for i, pos in enumerate(dollar_positions[:5]):  # Show first 5
            start = max(0, pos - 30)
            end = min(len(text), pos + 30)
            context = text[start:end]
            self.logger.error(f"$ context {i+1} at pos {pos}: ...{repr(context)}...")
        
        result = ParseResult(
            data_type=DataType.SNAPSHOT,
            raw_response=text,
            parsed_data={},
            confidence=ConfidenceLevel.FAILED
        )
        
        if ticker:
            result.attributes['ticker'] = ticker.upper()
        
        try:
            # Extract data using multiple pattern strategies
            extracted_data = {}
            matched_patterns = []
            failed_patterns = []
            
            for field_name, patterns in self._snapshot_patterns.items():
                self.logger.debug(f"Extracting {field_name}")
                value, pattern_used = self._extract_with_multiple_patterns(
                    text, patterns, field_name
                )
                
                if value is not None:
                    self.logger.debug(f"Found {field_name}='{value}' using pattern: {pattern_used}")
                    # Validate and clean the extracted value
                    try:
                        cleaned_value = self._validate_and_clean(field_name, value, 'snapshot')
                        extracted_data[field_name] = cleaned_value
                        matched_patterns.append(f"{field_name}:{pattern_used}")
                        self.logger.debug(f"Validated {field_name}: '{value}' -> '{cleaned_value}'")
                    except ValidationError as e:
                        self.logger.warning(f"Validation failed for {field_name}: {e}")
                        result.warnings.append(f"Validation failed for {field_name}: {e}")
                        failed_patterns.append(f"{field_name}:validation_failed")
                else:
                    self.logger.debug(f"No match for {field_name} (tried {len(patterns)} patterns)")
                    # Add detailed debug info for failed patterns
                    for i, pattern_info in enumerate(patterns):
                        self.logger.debug(f"  Pattern {i+1} ({pattern_info['name']}): '{pattern_info['pattern']}' - no match")
                    failed_patterns.append(f"{field_name}:no_match")
            
            result.parsed_data = extracted_data
            result.matched_patterns = matched_patterns
            result.failed_patterns = failed_patterns
            
            # Calculate confidence based on extraction success
            result.confidence = self._calculate_confidence(
                len(matched_patterns), len(self._snapshot_patterns), 'snapshot'
            )
            
            # Add metadata for JSON output  
            result.attributes.update({
                'total_fields': len(self._snapshot_patterns),
                'extracted_fields': len(extracted_data),
                'extraction_success_rate': f"{(len(extracted_data)/len(self._snapshot_patterns)*100):.1f}%"
            })
            
            self.logger.info(f"Snapshot parsing completed: {len(extracted_data)}/{len(self._snapshot_patterns)} fields ({(len(extracted_data)/len(self._snapshot_patterns)*100):.1f}% success rate)")
            self.logger.debug(f"Matched patterns count: {len(matched_patterns)}, Failed patterns count: {len(failed_patterns)}")
            
        except Exception as e:
            self.logger.error(f"Snapshot parsing failed: {e}")
            result.warnings.append(f"Parsing error: {str(e)}")
        
        result.parse_time_ms = (time.time() - start_time) * 1000
        return result
    
    def parse_support_resistance(self, text: str, ticker: Optional[str] = None) -> ParseResult:
        """
        Parse support and resistance levels from AI response.
        
        Args:
            text: Raw AI response text
            ticker: Stock ticker symbol for context
            
        Returns:
            ParseResult with parsed S&R data
        """
        import time
        start_time = time.time()
        
        self.logger.info(f"Parsing support/resistance from {len(text)} character response")
        
        result = ParseResult(
            data_type=DataType.SUPPORT_RESISTANCE,
            raw_response=text,
            parsed_data={},
            confidence=ConfidenceLevel.FAILED
        )
        
        if ticker:
            result.attributes['ticker'] = ticker.upper()
        
        try:
            extracted_data = {}
            matched_patterns = []
            failed_patterns = []
            
            for level_name, patterns in self._sr_patterns.items():
                value, pattern_used = self._extract_with_multiple_patterns(
                    text, patterns, level_name
                )
                
                if value is not None:
                    try:
                        cleaned_value = self._validate_and_clean(level_name, value, 'support_resistance')
                        extracted_data[level_name] = cleaned_value
                        matched_patterns.append(f"{level_name}:{pattern_used}")
                    except ValidationError as e:
                        result.warnings.append(f"Validation failed for {level_name}: {e}")
                        failed_patterns.append(f"{level_name}:validation_failed")
                else:
                    failed_patterns.append(f"{level_name}:no_match")
            
            result.parsed_data = extracted_data
            result.matched_patterns = matched_patterns
            result.failed_patterns = failed_patterns
            
            # Calculate confidence
            result.confidence = self._calculate_confidence(
                len(matched_patterns), len(self._sr_patterns), 'support_resistance'
            )
            
            # Validate S&R relationships
            self._validate_sr_relationships(extracted_data, result)
            
            result.attributes.update({
                'total_levels': len(self._sr_patterns),
                'extracted_levels': len(extracted_data),
                'support_levels': len([k for k in extracted_data.keys() if k.startswith('S')]),
                'resistance_levels': len([k for k in extracted_data.keys() if k.startswith('R')])
            })
            
            self.logger.info(f"S&R parsing completed: {len(extracted_data)}/{len(self._sr_patterns)} levels")
            
        except Exception as e:
            self.logger.error(f"S&R parsing failed: {e}")
            result.warnings.append(f"Parsing error: {str(e)}")
        
        result.parse_time_ms = (time.time() - start_time) * 1000
        return result
    
    def parse_technical_indicators(self, text: str, ticker: Optional[str] = None) -> ParseResult:
        """
        Parse technical indicators from AI response.
        
        Args:
            text: Raw AI response text
            ticker: Stock ticker symbol for context
            
        Returns:
            ParseResult with parsed technical data
        """
        import time
        start_time = time.time()
        
        self.logger.info(f"Parsing technical indicators from {len(text)} character response")
        
        result = ParseResult(
            data_type=DataType.TECHNICAL,
            raw_response=text,
            parsed_data={},
            confidence=ConfidenceLevel.FAILED
        )
        
        if ticker:
            result.attributes['ticker'] = ticker.upper()
        
        try:
            extracted_data = {}
            matched_patterns = []
            failed_patterns = []
            
            for indicator_name, patterns in self._technical_patterns.items():
                value, pattern_used = self._extract_with_multiple_patterns(
                    text, patterns, indicator_name
                )
                
                if value is not None:
                    try:
                        cleaned_value = self._validate_and_clean(indicator_name, value, 'technical')
                        extracted_data[indicator_name] = cleaned_value
                        matched_patterns.append(f"{indicator_name}:{pattern_used}")
                    except ValidationError as e:
                        result.warnings.append(f"Validation failed for {indicator_name}: {e}")
                        failed_patterns.append(f"{indicator_name}:validation_failed")
                else:
                    failed_patterns.append(f"{indicator_name}:no_match")
            
            result.parsed_data = extracted_data
            result.matched_patterns = matched_patterns
            result.failed_patterns = failed_patterns
            
            # Calculate confidence
            result.confidence = self._calculate_confidence(
                len(matched_patterns), len(self._technical_patterns), 'technical'
            )
            
            # Categorize indicators
            result.attributes.update({
                'total_indicators': len(self._technical_patterns),
                'extracted_indicators': len(extracted_data),
                'oscillators': len([k for k in extracted_data.keys() if k in ['RSI', 'MACD']]),
                'moving_averages': len([k for k in extracted_data.keys() if 'MA' in k]),
                'emas': len([k for k in extracted_data.keys() if k.startswith('EMA')]),
                'smas': len([k for k in extracted_data.keys() if k.startswith('SMA')])
            })
            
            self.logger.info(f"Technical parsing completed: {len(extracted_data)}/{len(self._technical_patterns)} indicators")
            
        except Exception as e:
            self.logger.error(f"Technical parsing failed: {e}")
            result.warnings.append(f"Parsing error: {str(e)}")
        
        result.parse_time_ms = (time.time() - start_time) * 1000
        return result
    
    def parse_any(self, text: str, data_type: DataType, ticker: Optional[str] = None) -> ParseResult:
        """
        Generic parser that routes to appropriate method based on data type.
        
        Args:
            text: Raw AI response text
            data_type: Type of data to parse
            ticker: Stock ticker symbol for context
            
        Returns:
            ParseResult with parsed data
        """
        if data_type == DataType.SNAPSHOT:
            return self.parse_stock_snapshot(text, ticker)
        elif data_type == DataType.SUPPORT_RESISTANCE:
            return self.parse_support_resistance(text, ticker)
        elif data_type == DataType.TECHNICAL:
            return self.parse_technical_indicators(text, ticker)
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    
    # ====== Pattern Building Methods ======
    
    def _build_snapshot_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build comprehensive patterns for stock snapshot data with enhanced AI response matching"""
        return {
            'current_price': [
                {
                    'pattern': r'(?:current\s+)?price[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'price_standard'
                },
                {
                    'pattern': r'trading\s+at[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'trading_at'
                },
                {
                    'pattern': r'\$\s*([\d,]+\.\d+)\s*(?:per\s+share|each)',
                    'flags': re.IGNORECASE,
                    'name': 'dollar_per_share'
                },
                {
                    'pattern': r'(?:stock|share)\s+is[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'stock_is'
                },
                {
                    'pattern': r'(?:currently|now)\s+trading[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'currently_trading'
                },
                {
                    'pattern': r'\b([\d,]+\.\d+)\s*(?:USD|dollars?)\b',
                    'flags': re.IGNORECASE,
                    'name': 'price_with_currency'
                }
            ],
            'percentage_change': [
                {
                    'pattern': r'(?:percentage|percent)(?:\s+)?change[:\s]*([\+\-]?[\d\.]+)\s*%',
                    'flags': re.IGNORECASE,
                    'name': 'percentage_change_explicit'
                },
                {
                    'pattern': r'([\+\-]?[\d\.]+)%\s*(?:change|today|daily|session)',
                    'flags': re.IGNORECASE,
                    'name': 'percent_change_standard'
                },
                {
                    'pattern': r'(?:up|down|gained|lost)[:\s]*([\+\-]?[\d\.]+)%',
                    'flags': re.IGNORECASE,
                    'name': 'up_down_percent'
                },
                {
                    'pattern': r'percentage[:\s]*([\+\-]?[\d\.]+)%',
                    'flags': re.IGNORECASE,
                    'name': 'percentage_generic'
                },
                {
                    'pattern': r'\(([\+\-]?[\d\.]+)%\)',
                    'flags': re.IGNORECASE,
                    'name': 'parentheses_percent'
                }
            ],
            'dollar_change': [
                {
                    'pattern': r'\$\s*[cC]hange[:\s]*([-+]?\s*\$?\s*[\d\.]+)',
                    'flags': re.IGNORECASE,
                    'name': 'dollar_change_with_spaces'
                },
                {
                    'pattern': r'\$\s*[cC]hange[:\s]*([\+\-]?\$?[\d\.]+)',
                    'flags': re.IGNORECASE,
                    'name': 'dollar_change_explicit'
                },
                {
                    'pattern': r'(?:dollar|\\$)(?:\s+)?change[:\s]*([\+\-]?\$?[\d\.]+)',
                    'flags': re.IGNORECASE,
                    'name': 'dollar_change_text'
                },
                {
                    'pattern': r'([\+\-]?\$?[\d\.]+)\s*(?:change|today|daily|session)',
                    'flags': re.IGNORECASE,
                    'name': 'dollar_change_standard'
                },
                {
                    'pattern': r'(?:gained|lost|gaining|losing)[:\s]*\$?([\+\-]?[\d\.]+)',
                    'flags': re.IGNORECASE,
                    'name': 'gained_lost'
                },
                {
                    'pattern': r'\(([\+\-]?\$?[\d\.]+)\)',
                    'flags': re.IGNORECASE,
                    'name': 'parentheses_dollar'
                }
            ],
            'volume': [
                {
                    'pattern': r'volume[:\s]*([\d,]+(?:\.\d+)?[KMB]?)',
                    'flags': re.IGNORECASE,
                    'name': 'volume_standard'
                },
                {
                    'pattern': r'traded[:\s]*([\d,]+(?:\.\d+)?[KMB]?)\s*shares',
                    'flags': re.IGNORECASE,
                    'name': 'traded_shares'
                },
                {
                    'pattern': r'([\d,]+(?:\.\d+)?[KMB]?)\s*shares\s*traded',
                    'flags': re.IGNORECASE,
                    'name': 'shares_traded_reverse'
                },
                {
                    'pattern': r'volume:\s*([\d,]+)',
                    'flags': re.IGNORECASE,
                    'name': 'volume_colon'
                }
            ],
            'vwap': [
                {
                    'pattern': r'VWAP\s*\([^)]+\)\s*[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'vwap_with_parenthetical'
                },
                {
                    'pattern': r'(?:vwap|volume\s+weighted)[:\s]*\$?([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'vwap_standard'
                },
                {
                    'pattern': r'VWAP[:\s]*\$?([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'vwap_caps'
                },
                {
                    'pattern': r'(?:volume\s+weighted\s+average\s+price)[:\s]*\$?([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'vwap_full_text'
                }
            ],
            'open': [
                {
                    'pattern': r'open[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'open_standard'
                },
                {
                    'pattern': r'opened\s+at[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'opened_at'
                },
                {
                    'pattern': r'opening[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'opening_price'
                }
            ],
            'high': [
                {
                    'pattern': r'high[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'high_standard'
                },
                {
                    'pattern': r'day\s+high[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'day_high'
                },
                {
                    'pattern': r'(?:52[\s-]?week|daily)\s+high[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'period_high'
                }
            ],
            'low': [
                {
                    'pattern': r'low[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'low_standard'
                },
                {
                    'pattern': r'day\s+low[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'day_low'
                },
                {
                    'pattern': r'(?:52[\s-]?week|daily)\s+low[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'period_low'
                }
            ],
            'close': [
                {
                    'pattern': r'close[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'close_standard'
                },
                {
                    'pattern': r'closed\s+at[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'closed_at'
                },
                {
                    'pattern': r'previous\s+close[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'previous_close'
                },
                {
                    'pattern': r'closing[:\s]*\$?\s*([\d,]+\.\d+)',
                    'flags': re.IGNORECASE,
                    'name': 'closing_price'
                }
            ]
        }
    
    def _build_sr_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build patterns for support and resistance levels"""
        patterns = {}
        
        # Support levels (S1, S2, S3)
        for i in range(1, 4):
            patterns[f'S{i}'] = [
                {
                    'pattern': fr'S{i}[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f's{i}_standard'
                },
                {
                    'pattern': fr'Support\s+{i}[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f's{i}_support_explicit'
                },
                {
                    'pattern': fr'(?:first|second|third)\s+support[:\s]*\$?([\d,]+\.?\d*)' if i == 1 else fr'(?:second|third)\s+support[:\s]*\$?([\d,]+\.?\d*)' if i == 2 else r'third\s+support[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f's{i}_ordinal'
                }
            ]
        
        # Resistance levels (R1, R2, R3)
        for i in range(1, 4):
            patterns[f'R{i}'] = [
                {
                    'pattern': fr'R{i}[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'r{i}_standard'
                },
                {
                    'pattern': fr'Resistance\s+{i}[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'r{i}_resistance_explicit'
                },
                {
                    'pattern': fr'(?:first|second|third)\s+resistance[:\s]*\$?([\d,]+\.?\d*)' if i == 1 else fr'(?:second|third)\s+resistance[:\s]*\$?([\d,]+\.?\d*)' if i == 2 else r'third\s+resistance[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'r{i}_ordinal'
                }
            ]
        
        return patterns
    
    def _build_technical_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build patterns for technical indicators"""
        patterns = {}
        
        # RSI patterns
        patterns['RSI'] = [
            {
                'pattern': r'RSI[:\s]+([\d\.]+)',
                'flags': re.IGNORECASE,
                'name': 'rsi_standard'
            },
            {
                'pattern': r'(?:relative\s+strength\s+index)[:\s]+([\d\.]+)',
                'flags': re.IGNORECASE,
                'name': 'rsi_full_name'
            }
        ]
        
        # MACD patterns
        patterns['MACD'] = [
            {
                'pattern': r'MACD[:\s]+([\d\.\-\+]+)',
                'flags': re.IGNORECASE,
                'name': 'macd_standard'
            },
            {
                'pattern': r'(?:moving\s+average\s+convergence\s+divergence)[:\s]+([\d\.\-\+]+)',
                'flags': re.IGNORECASE,
                'name': 'macd_full_name'
            }
        ]
        
        # EMA patterns (5, 10, 20, 50, 200)
        for period in [5, 10, 20, 50, 200]:
            patterns[f'EMA_{period}'] = [
                {
                    'pattern': fr'EMA\s*{period}[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'ema_{period}_standard'
                },
                {
                    'pattern': fr'{period}\s*(?:day|period)\s*EMA[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'ema_{period}_day'
                },
                {
                    'pattern': fr'exponential\s+moving\s+average\s+{period}[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'ema_{period}_full'
                }
            ]
        
        # SMA patterns (5, 10, 20, 50, 200)
        for period in [5, 10, 20, 50, 200]:
            patterns[f'SMA_{period}'] = [
                {
                    'pattern': fr'SMA\s*{period}[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'sma_{period}_standard'
                },
                {
                    'pattern': fr'{period}\s*(?:day|period)\s*SMA[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'sma_{period}_day'
                },
                {
                    'pattern': fr'simple\s+moving\s+average\s+{period}[:\s]*\$?([\d,]+\.?\d*)',
                    'flags': re.IGNORECASE,
                    'name': f'sma_{period}_full'
                }
            ]
        
        return patterns
    
    # ====== Helper Methods ======
    
    def _extract_with_multiple_patterns(self, text: str, patterns: List[Dict[str, Any]], 
                                       field_name: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Try multiple patterns to extract a value, returning first successful match.
        
        Args:
            text: Text to search in
            patterns: List of pattern dictionaries
            field_name: Name of field being extracted
            
        Returns:
            Tuple of (extracted_value, pattern_name) or (None, None)
        """
        for pattern_info in patterns:
            try:
                match = re.search(
                    pattern_info['pattern'], 
                    text, 
                    pattern_info.get('flags', 0)
                )
                if match:
                    value = match.group(1).strip()
                    if value:  # Ensure non-empty value
                        self.logger.debug(f"Extracted {field_name}='{value}' using pattern '{pattern_info['name']}'")
                        return value, pattern_info['name']
            except Exception as e:
                self.logger.debug(f"Pattern {pattern_info['name']} failed for {field_name}: {e}")
                continue
        
        return None, None
    
    def _validate_and_clean(self, field_name: str, value: str, data_type: str) -> str:
        """
        Validate and clean extracted values.
        
        Args:
            field_name: Name of the field
            value: Raw extracted value
            data_type: Type of data (snapshot, support_resistance, technical)
            
        Returns:
            Cleaned and validated value
            
        Raises:
            ValidationError: If validation fails
        """
        if not value or not value.strip():
            raise ValidationError("Empty value")
        
        cleaned_value = value.strip()
        
        # Get appropriate validator
        validator_key = f"{data_type}_{field_name}"
        if validator_key in self._validators:
            try:
                cleaned_value = self._validators[validator_key](cleaned_value)
            except Exception as e:
                raise ValidationError(f"Validation failed: {e}")
        else:
            # Generic cleaning
            cleaned_value = self._generic_clean(cleaned_value, field_name)
        
        return cleaned_value
    
    def _generic_clean(self, value: str, field_name: str) -> str:
        """Generic value cleaning for unspecified fields"""
        # Remove extra whitespace
        value = re.sub(r'\s+', ' ', value).strip()
        
        # Handle common price formats
        if any(keyword in field_name.lower() for keyword in ['price', 'level', 'vwap']):
            # Remove currency symbols and format as price
            value = re.sub(r'[$,]', '', value)
            try:
                float_val = float(value)
                return f"${float_val:.2f}"
            except ValueError:
                pass
        
        # Handle percentage values
        if 'percentage' in field_name.lower() or '%' in value:
            value = re.sub(r'[%]', '', value).strip()
            try:
                float_val = float(value)
                return f"{float_val:+.1f}%" if 'change' in field_name.lower() else f"{float_val:.1f}%"
            except ValueError:
                pass
        
        return value
    
    def _build_validators(self) -> Dict[str, callable]:
        """Build field-specific validators"""
        validators = {}
        
        # Snapshot validators
        validators['snapshot_current_price'] = self._validate_price
        validators['snapshot_open'] = self._validate_price
        validators['snapshot_high'] = self._validate_price
        validators['snapshot_low'] = self._validate_price
        validators['snapshot_close'] = self._validate_price
        validators['snapshot_vwap'] = self._validate_price
        validators['snapshot_percentage_change'] = self._validate_percentage
        validators['snapshot_dollar_change'] = self._validate_dollar_change
        validators['snapshot_volume'] = self._validate_volume
        
        # Support/Resistance validators
        for level in ['S1', 'S2', 'S3', 'R1', 'R2', 'R3']:
            validators[f'support_resistance_{level}'] = self._validate_price
        
        # Technical validators
        validators['technical_RSI'] = self._validate_rsi
        validators['technical_MACD'] = self._validate_macd
        
        # Moving average validators
        for period in [5, 10, 20, 50, 200]:
            validators[f'technical_EMA_{period}'] = self._validate_price
            validators[f'technical_SMA_{period}'] = self._validate_price
        
        return validators
    
    def _validate_price(self, value: str) -> str:
        """Validate and format price values"""
        # Remove currency symbols and commas
        cleaned = re.sub(r'[$,]', '', value)
        try:
            price_val = float(cleaned)
            if price_val < 0:
                raise ValidationError("Price cannot be negative")
            if price_val > 1000000:  # Reasonable upper bound
                raise ValidationError("Price seems unreasonably high")
            return f"${price_val:.2f}"
        except ValueError:
            raise ValidationError(f"Invalid price format: {value}")
    
    def _validate_percentage(self, value: str) -> str:
        """Validate and format percentage values"""
        cleaned = re.sub(r'[%+]', '', value).strip()
        try:
            pct_val = float(cleaned)
            if abs(pct_val) > 50:  # Reasonable daily change limit
                raise ValidationError("Percentage change seems unreasonably large")
            return f"{pct_val:+.1f}%"
        except ValueError:
            raise ValidationError(f"Invalid percentage format: {value}")
    
    def _validate_dollar_change(self, value: str) -> str:
        """Validate and format dollar change values"""
        cleaned = re.sub(r'[$]', '', value)
        try:
            change_val = float(cleaned)
            return f"${change_val:+.2f}"
        except ValueError:
            raise ValidationError(f"Invalid dollar change format: {value}")
    
    def _validate_volume(self, value: str) -> str:
        """Validate and format volume values"""
        cleaned = value.upper().replace(',', '')
        
        # Handle K, M, B suffixes
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if cleaned.endswith(suffix):
                try:
                    base_val = float(cleaned[:-1])
                    total_val = base_val * multiplier
                    return f"{int(total_val):,}"
                except ValueError:
                    continue
        
        # Try as plain number
        try:
            vol_val = int(float(cleaned))
            if vol_val < 0:
                raise ValidationError("Volume cannot be negative")
            return f"{vol_val:,}"
        except ValueError:
            raise ValidationError(f"Invalid volume format: {value}")
    
    def _validate_rsi(self, value: str) -> str:
        """Validate RSI values (0-100)"""
        try:
            rsi_val = float(value)
            if not (0 <= rsi_val <= 100):
                raise ValidationError("RSI must be between 0 and 100")
            return f"{rsi_val:.1f}"
        except ValueError:
            raise ValidationError(f"Invalid RSI format: {value}")
    
    def _validate_macd(self, value: str) -> str:
        """Validate MACD values"""
        try:
            macd_val = float(value)
            return f"{macd_val:.3f}"
        except ValueError:
            raise ValidationError(f"Invalid MACD format: {value}")
    
    def _calculate_confidence(self, matched_count: int, total_count: int, data_type: str) -> ConfidenceLevel:
        """Calculate confidence level based on extraction success rate"""
        if total_count == 0:
            return ConfidenceLevel.FAILED
        
        success_rate = matched_count / total_count
        
        if success_rate >= 0.8:
            return ConfidenceLevel.HIGH
        elif success_rate >= 0.5:
            return ConfidenceLevel.MEDIUM
        elif success_rate > 0:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.FAILED
    
    def _validate_sr_relationships(self, data: Dict[str, str], result: ParseResult) -> None:
        """Validate logical relationships between support and resistance levels"""
        try:
            # Extract numeric values for comparison
            support_values = []
            resistance_values = []
            
            for level, price_str in data.items():
                if level.startswith('S'):
                    price_val = float(re.sub(r'[$,]', '', price_str))
                    support_values.append((level, price_val))
                elif level.startswith('R'):
                    price_val = float(re.sub(r'[$,]', '', price_str))
                    resistance_values.append((level, price_val))
            
            # Sort levels
            support_values.sort(key=lambda x: int(x[0][1]))  # Sort by S1, S2, S3
            resistance_values.sort(key=lambda x: int(x[0][1]))  # Sort by R1, R2, R3
            
            # Validate support levels are in descending order
            for i in range(len(support_values) - 1):
                if support_values[i][1] <= support_values[i+1][1]:
                    result.warnings.append(f"Support levels may be out of order: {support_values[i][0]} should be > {support_values[i+1][0]}")
            
            # Validate resistance levels are in ascending order
            for i in range(len(resistance_values) - 1):
                if resistance_values[i][1] >= resistance_values[i+1][1]:
                    result.warnings.append(f"Resistance levels may be out of order: {resistance_values[i][0]} should be < {resistance_values[i+1][0]}")
            
            # Validate that resistance levels are above support levels
            if support_values and resistance_values:
                max_support = max(support_values, key=lambda x: x[1])[1]
                min_resistance = min(resistance_values, key=lambda x: x[1])[1]
                if max_support >= min_resistance:
                    result.warnings.append("Highest support level should be below lowest resistance level")
                    
        except Exception as e:
            result.warnings.append(f"Could not validate S&R relationships: {e}")
    
    def get_parsing_statistics(self) -> Dict[str, Any]:
        """Get statistics about the parser's pattern libraries"""
        return {
            'snapshot_patterns': len(self._snapshot_patterns),
            'sr_patterns': len(self._sr_patterns),
            'technical_patterns': len(self._technical_patterns),
            'total_patterns': sum(len(patterns) for patterns in [
                self._snapshot_patterns, self._sr_patterns, self._technical_patterns
            ]),
            'validators': len(self._validators)
        }
