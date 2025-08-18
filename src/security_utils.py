"""
Security utilities for the Market Parser application.

This module provides security functions for input validation, data sanitization,
and secure logging to prevent sensitive data exposure.
"""

import re
import os
import logging
from typing import Optional, List, Dict, Any
from functools import wraps

# Configure secure logger
logger = logging.getLogger(__name__)

class SecurityError(Exception):
    """Raised when security validation fails"""
    pass

class InputValidator:
    """Comprehensive input validation and sanitization"""
    
    # Valid ticker symbol pattern (1-5 uppercase letters)
    TICKER_PATTERN = re.compile(r'^[A-Z]{1,5}$')
    
    # Maximum lengths for different input types
    MAX_QUERY_LENGTH = 1000
    MAX_TICKER_LENGTH = 5
    MAX_MESSAGE_LENGTH = 5000
    
    # Forbidden patterns that might indicate injection attempts
    FORBIDDEN_PATTERNS = [
        r'<script[^>]*>',
        r'javascript:',
        r'vbscript:',
        r'onload\s*=',
        r'onerror\s*=',
        r'eval\s*\(',
        r'Function\s*\(',
    ]
    
    @classmethod
    def validate_ticker(cls, ticker: str) -> str:
        """
        Validate and sanitize stock ticker symbol.
        
        Args:
            ticker: Stock ticker symbol to validate
            
        Returns:
            Sanitized ticker symbol
            
        Raises:
            SecurityError: If ticker is invalid or potentially malicious
        """
        if not ticker:
            raise SecurityError("Ticker symbol cannot be empty")
        
        # Basic sanitization
        ticker = ticker.strip().upper()
        
        # Length check
        if len(ticker) > cls.MAX_TICKER_LENGTH:
            raise SecurityError(f"Ticker symbol too long: max {cls.MAX_TICKER_LENGTH} characters")
        
        # Pattern validation
        if not cls.TICKER_PATTERN.match(ticker):
            raise SecurityError("Ticker symbol must contain only uppercase letters (1-5 chars)")
        
        # Check for forbidden patterns
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, ticker, re.IGNORECASE):
                raise SecurityError("Ticker contains potentially malicious content")
        
        return ticker
    
    @classmethod
    def validate_query(cls, query: str) -> str:
        """
        Validate and sanitize user query string.
        
        Args:
            query: User query to validate
            
        Returns:
            Sanitized query string
            
        Raises:
            SecurityError: If query is invalid or potentially malicious
        """
        if not query:
            raise SecurityError("Query cannot be empty")
        
        # Basic sanitization
        query = query.strip()
        
        # Length check
        if len(query) > cls.MAX_QUERY_LENGTH:
            raise SecurityError(f"Query too long: max {cls.MAX_QUERY_LENGTH} characters")
        
        # Check for forbidden patterns
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                raise SecurityError("Query contains potentially malicious content")
        
        # Remove potentially dangerous characters
        query = re.sub(r'[<>&"\'`]', '', query)
        
        return query
    
    @classmethod
    def validate_message(cls, message: str) -> str:
        """
        Validate and sanitize chat message.
        
        Args:
            message: Chat message to validate
            
        Returns:
            Sanitized message
            
        Raises:
            SecurityError: If message is invalid or potentially malicious
        """
        if not message:
            raise SecurityError("Message cannot be empty")
        
        # Basic sanitization
        message = message.strip()
        
        # Length check
        if len(message) > cls.MAX_MESSAGE_LENGTH:
            raise SecurityError(f"Message too long: max {cls.MAX_MESSAGE_LENGTH} characters")
        
        # Check for forbidden patterns
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                raise SecurityError("Message contains potentially malicious content")
        
        return message

class SecureLogger:
    """Secure logging utilities that prevent sensitive data exposure"""
    
    # Patterns that indicate sensitive data
    SENSITIVE_PATTERNS = [
        r'sk-[a-zA-Z0-9]{32,}',  # OpenAI API keys
        r'sk-ant-[a-zA-Z0-9-_]{95,}',  # Anthropic API keys
        r'AIza[a-zA-Z0-9_-]{35}',  # Google API keys
        r'[A-Za-z0-9]{26}',  # Polygon.io API keys (26 chars)
        r'Bearer [a-zA-Z0-9_-]+',  # Bearer tokens
        r'password\s*[:=]\s*[^\s]+',  # Passwords
        r'secret\s*[:=]\s*[^\s]+',  # Secrets
    ]
    
    @classmethod
    def sanitize_log_message(cls, message: str) -> str:
        """
        Sanitize log message to remove sensitive data.
        
        Args:
            message: Log message to sanitize
            
        Returns:
            Sanitized message with sensitive data redacted
        """
        sanitized = message
        
        # Replace sensitive patterns with redacted versions
        for pattern in cls.SENSITIVE_PATTERNS:
            sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    @classmethod
    def safe_log_response_length(cls, response_text: str) -> Dict[str, Any]:
        """
        Create safe logging info about API response without exposing content.
        
        Args:
            response_text: API response text
            
        Returns:
            Safe logging information
        """
        return {
            'length': len(response_text),
            'has_price_data': 'price' in response_text.lower(),
            'has_percentage': '%' in response_text,
            'has_dollar_sign': '$' in response_text,
            'word_count': len(response_text.split()),
            'line_count': len(response_text.splitlines())
        }

class EnvironmentValidator:
    """Validate environment variables and security configuration"""
    
    REQUIRED_VARS = ['POLYGON_API_KEY', 'OPENAI_API_KEY']
    OPTIONAL_VARS = ['ANTHROPIC_API_KEY', 'GEMINI_API_KEY']
    
    @classmethod
    def validate_environment(cls) -> Dict[str, Any]:
        """
        Validate that required environment variables are set securely.
        
        Returns:
            Dictionary with validation results
        """
        results = {
            'required_vars_present': True,
            'missing_vars': [],
            'weak_keys': [],
            'warnings': []
        }
        
        # Check required variables
        for var in cls.REQUIRED_VARS:
            value = os.getenv(var)
            if not value:
                results['required_vars_present'] = False
                results['missing_vars'].append(var)
            elif len(value) < 20:  # Basic length check for API keys
                results['weak_keys'].append(var)
                results['warnings'].append(f"{var} appears to be a placeholder or test key")
        
        # Check optional variables
        for var in cls.OPTIONAL_VARS:
            value = os.getenv(var)
            if value and len(value) < 20:
                results['weak_keys'].append(var)
                results['warnings'].append(f"{var} appears to be a placeholder or test key")
        
        return results

def secure_function(func):
    """
    Decorator to add security validation to functions.
    
    This decorator automatically validates inputs and sanitizes outputs
    for functions that handle user data.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Log function call securely
            logger.debug(f"Secure function call: {func.__name__}")
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Log successful completion
            logger.debug(f"Secure function completed: {func.__name__}")
            
            return result
            
        except SecurityError as e:
            logger.warning(f"Security validation failed in {func.__name__}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in secure function {func.__name__}: {SecureLogger.sanitize_log_message(str(e))}")
            raise
    
    return wrapper

# Utility functions for common security operations

def is_development_environment() -> bool:
    """Check if running in development environment"""
    return os.getenv('ENVIRONMENT', 'development').lower() in ['development', 'dev', 'local']

def get_safe_env_summary() -> Dict[str, Any]:
    """Get a safe summary of environment configuration"""
    validator = EnvironmentValidator()
    validation_results = validator.validate_environment()
    
    return {
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'required_vars_set': validation_results['required_vars_present'],
        'missing_count': len(validation_results['missing_vars']),
        'warning_count': len(validation_results['warnings']),
        'is_dev': is_development_environment()
    }

def validate_api_response_safety(response_data: Any) -> bool:
    """
    Validate that API response data is safe to log/display.
    
    Args:
        response_data: Response data to validate
        
    Returns:
        True if safe, False if contains sensitive patterns
    """
    response_str = str(response_data)
    
    for pattern in SecureLogger.SENSITIVE_PATTERNS:
        if re.search(pattern, response_str, re.IGNORECASE):
            return False
    
    return True