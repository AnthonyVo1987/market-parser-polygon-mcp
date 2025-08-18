#!/usr/bin/env python3
"""
Test Parser with Production Debug Logging
This will trigger the new debug logging in response_parser.py to capture
the exact data being processed in production scenarios.
"""

import logging
import asyncio
from src.response_parser import ResponseParser, DataType

# Configure logging to capture ERROR level debug messages
logging.basicConfig(
    level=logging.ERROR,  # Capture ERROR level which our debug uses
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('production_parser_debug.log'),
        logging.StreamHandler()
    ]
)

def test_parser_with_debug():
    """Test parser with various input scenarios to trigger debug logging"""
    
    parser = ResponseParser(log_level=logging.ERROR)
    
    # Test cases that might reveal the production issue
    test_cases = [
        {
            'name': 'Perfect Working Format (from debug investigation)',
            'text': '''Current price: $180.45  
Percentage change: -1.3%  
Dollar change: -$2.28  
Volume: 156,591,397 shares  
VWAP: $179.92  
Open: $181.88  
High: $181.90  
Low: $178.04  
Close: $180.45  ''',
            'ticker': 'NVDA'
        },
        {
            'name': 'Empty String (edge case)',
            'text': '',
            'ticker': 'NVDA'
        },
        {
            'name': 'None or Null-like (edge case)',
            'text': 'null',
            'ticker': 'NVDA'
        },
        {
            'name': 'Error Message (possible production case)',
            'text': 'Error: Unable to fetch data for NVDA',
            'ticker': 'NVDA'
        },
        {
            'name': 'Malformed Response (possible production case)',
            'text': 'I apologize, but I cannot retrieve the current stock data...',
            'ticker': 'NVDA'
        },
        {
            'name': 'JSON-like Response (wrong format)',
            'text': '{"current_price": 180.45, "percentage_change": -1.3}',
            'ticker': 'NVDA'
        }
    ]
    
    print("🚨 TESTING PARSER WITH DEBUG LOGGING")
    print("This will show EXACTLY what input causes 0/9 field extraction")
    print("Check production_parser_debug.log for detailed debug output")
    print("")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            result = parser.parse_stock_snapshot(test_case['text'], test_case['ticker'])
            
            # Print summary results
            print(f"✅ Confidence: {result.confidence.value}")
            print(f"✅ Fields extracted: {len(result.parsed_data)}/9")
            print(f"✅ Success rate: {len(result.parsed_data)/9*100:.1f}%")
            
            if len(result.parsed_data) == 0:
                print("🚨 FOUND THE BUG! This case produces 0/9 extraction")
                print("Check the debug log for exact details of why patterns fail")
            
            print(f"✅ Parsed data: {result.parsed_data}")
            print("")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            print("")
    
    print("=" * 60)
    print("INVESTIGATION COMPLETE")
    print("Check production_parser_debug.log for detailed analysis")
    print("Look for cases with 0 field extraction to identify the real bug")

if __name__ == "__main__":
    test_parser_with_debug()