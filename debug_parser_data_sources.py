#!/usr/bin/env python3
"""
CRITICAL BUG DEBUGGING: Parser Data Source Investigation

This script investigates the exact root cause of parser failure by:
1. Comparing response.output vs enhanced_response data sources
2. Testing parser against both formats with NVDA production case
3. Adding extensive debug logging to identify exact differences
4. Proving the data source mismatch hypothesis

HYPOTHESIS: Parser receives response.output but chat displays enhanced_response,
causing mismatch between what parser processes vs what user sees working.
"""

import os
import re
import asyncio
import logging
from typing import Dict, Any, Optional
from dotenv import find_dotenv, load_dotenv

# Import our systems
from response_parser import ResponseParser, DataType
from prompt_templates import PromptTemplateManager
from market_parser_demo import create_polygon_mcp_server, TokenCostTracker
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel

# Load environment
load_dotenv(find_dotenv())

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug_parser_investigation.log'),
        logging.StreamHandler()
    ]
)

class DataSourceInvestigator:
    """
    Investigates the exact data source mismatch between parser input 
    and chat display causing production failures.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.response_parser = ResponseParser(log_level=logging.DEBUG)
        self.setup_agent()
        
        # Production test case from logs - NVDA snapshot that fails
        self.production_test_case = {
            'ticker': 'NVDA',
            'query': 'Get current stock snapshot for NVDA',
            'expected_fields': [
                'current_price', 'percentage_change', 'dollar_change',
                'volume', 'open', 'high', 'low', 'close'
            ]
        }
    
    def setup_agent(self):
        """Setup agent exactly like chat_ui.py"""
        MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        server = create_polygon_mcp_server()
        model = OpenAIResponsesModel(MODEL_NAME)
        
        prompt_manager = PromptTemplateManager()
        base_system_prompt = (
            "You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. "
            "Use the latest data available. Always double check your math. "
            "For any questions about the current date, use the 'get_today_date' tool. "
            "For long or complex queries, break the query into logical subtasks and process each subtask in order."
        )
        
        enhanced_system_prompt = prompt_manager.get_enhanced_system_prompt(base_system_prompt)
        
        self.agent = Agent(
            model=model,
            mcp_servers=[server],
            system_prompt=enhanced_system_prompt,
        )
        
        @self.agent.tool
        def get_today_date(ctx) -> str:
            """Returns today's date in YYYY-MM-DD format."""
            import datetime
            return datetime.date.today().strftime("%Y-%m-%d")
    
    async def investigate_data_sources(self):
        """
        Main investigation: Compare exact data sources and identify mismatch
        """
        self.logger.info("=" * 80)
        self.logger.info("STARTING CRITICAL PARSER DATA SOURCE INVESTIGATION")
        self.logger.info("=" * 80)
        
        # Step 1: Get production response from agent
        production_response = await self.get_production_response()
        
        # Step 2: Compare data sources
        await self.compare_data_sources(production_response)
        
        # Step 3: Test parser against both formats
        await self.test_parser_against_formats(production_response)
        
        # Step 4: Identify exact fix needed
        await self.identify_fix_requirements(production_response)
        
        self.logger.info("=" * 80)
        self.logger.info("INVESTIGATION COMPLETE - Check results above")
        self.logger.info("=" * 80)
    
    async def get_production_response(self):
        """Get actual production response for NVDA snapshot"""
        self.logger.info(f"Getting production response for: {self.production_test_case['ticker']}")
        
        # Use snapshot prompt template like chat_ui.py would
        from prompt_templates import PromptType
        prompt_manager = PromptTemplateManager()
        structured_prompt, ticker_context = prompt_manager.generate_prompt(
            PromptType.SNAPSHOT, 
            ticker=self.production_test_case['ticker']
        )
        
        self.logger.info(f"Sending prompt: {structured_prompt}")
        
        response = await self.agent.run(structured_prompt)
        
        self.logger.info(f"Received response type: {type(response)}")
        self.logger.info(f"Response attributes: {dir(response)}")
        
        # Log the raw response output
        self.logger.info("RAW RESPONSE.OUTPUT:")
        self.logger.info(f"Type: {type(response.output)}")
        self.logger.info(f"Length: {len(response.output)} characters")
        self.logger.info(f"Content: {repr(response.output)}")
        self.logger.info(f"First 500 chars: {response.output[:500]}")
        
        return response
    
    async def compare_data_sources(self, production_response):
        """
        Compare response.output vs enhanced_response formats
        """
        self.logger.info("-" * 60)
        self.logger.info("COMPARING DATA SOURCES")
        self.logger.info("-" * 60)
        
        # This is what parser receives (response.output)
        raw_response = production_response.output
        
        # This is what chat displays (enhanced_response)
        confidence_emoji = "🎯"  # Would be determined by parsing
        ticker = self.production_test_case['ticker']
        enhanced_response = f"{confidence_emoji} **Snapshot Analysis for {ticker}**\n\n{raw_response}"
        
        self.logger.info("=" * 40)
        self.logger.info("RAW RESPONSE (what parser gets):")
        self.logger.info("=" * 40)
        self.logger.info(f"Type: {type(raw_response)}")
        self.logger.info(f"Length: {len(raw_response)}")
        self.logger.info(f"repr(): {repr(raw_response)}")
        self.logger.info(f"Content:\n{raw_response}")
        
        self.logger.info("=" * 40)
        self.logger.info("ENHANCED RESPONSE (what chat displays):")
        self.logger.info("=" * 40)
        self.logger.info(f"Type: {type(enhanced_response)}")
        self.logger.info(f"Length: {len(enhanced_response)}")
        self.logger.info(f"repr(): {repr(enhanced_response)}")
        self.logger.info(f"Content:\n{enhanced_response}")
        
        # Character-by-character comparison for first 200 chars
        self.logger.info("=" * 40)
        self.logger.info("CHARACTER-BY-CHARACTER COMPARISON (first 200 chars):")
        self.logger.info("=" * 40)
        
        raw_start = raw_response[:200]
        enhanced_start = enhanced_response[:200]
        
        for i, (r, e) in enumerate(zip(raw_start, enhanced_start)):
            if r != e:
                self.logger.info(f"DIFF at pos {i}: raw='{repr(r)}' enhanced='{repr(e)}'")
                break
        
        return raw_response, enhanced_response
    
    async def test_parser_against_formats(self, production_response):
        """
        Test parser against both raw and enhanced formats to prove mismatch
        """
        self.logger.info("-" * 60)
        self.logger.info("TESTING PARSER AGAINST BOTH FORMATS")
        self.logger.info("-" * 60)
        
        raw_response = production_response.output
        ticker = self.production_test_case['ticker']
        
        # Enhanced format (what chat displays)
        enhanced_response = f"🎯 **Snapshot Analysis for {ticker}**\n\n{raw_response}"
        
        # Test parser against RAW format (current situation)
        self.logger.info("=" * 40)
        self.logger.info("TESTING PARSER AGAINST RAW FORMAT (current)")
        self.logger.info("=" * 40)
        
        raw_result = self.response_parser.parse_stock_snapshot(raw_response, ticker)
        
        self.logger.info(f"RAW PARSING RESULTS:")
        self.logger.info(f"- Confidence: {raw_result.confidence.value}")
        self.logger.info(f"- Fields extracted: {len(raw_result.parsed_data)}/{len(self.production_test_case['expected_fields'])}")
        self.logger.info(f"- Extraction rate: {len(raw_result.parsed_data)/len(self.production_test_case['expected_fields'])*100:.1f}%")
        self.logger.info(f"- Parsed data: {raw_result.parsed_data}")
        self.logger.info(f"- Matched patterns: {raw_result.matched_patterns}")
        self.logger.info(f"- Failed patterns: {raw_result.failed_patterns}")
        self.logger.info(f"- Warnings: {raw_result.warnings}")
        
        # Test parser against ENHANCED format (what chat shows)
        self.logger.info("=" * 40)
        self.logger.info("TESTING PARSER AGAINST ENHANCED FORMAT (what chat shows)")
        self.logger.info("=" * 40)
        
        enhanced_result = self.response_parser.parse_stock_snapshot(enhanced_response, ticker)
        
        self.logger.info(f"ENHANCED PARSING RESULTS:")
        self.logger.info(f"- Confidence: {enhanced_result.confidence.value}")
        self.logger.info(f"- Fields extracted: {len(enhanced_result.parsed_data)}/{len(self.production_test_case['expected_fields'])}")
        self.logger.info(f"- Extraction rate: {len(enhanced_result.parsed_data)/len(self.production_test_case['expected_fields'])*100:.1f}%")
        self.logger.info(f"- Parsed data: {enhanced_result.parsed_data}")
        self.logger.info(f"- Matched patterns: {enhanced_result.matched_patterns}")
        self.logger.info(f"- Failed patterns: {enhanced_result.failed_patterns}")
        self.logger.info(f"- Warnings: {enhanced_result.warnings}")
        
        # Compare results
        self.logger.info("=" * 40)
        self.logger.info("COMPARISON SUMMARY:")
        self.logger.info("=" * 40)
        
        raw_success = len(raw_result.parsed_data)
        enhanced_success = len(enhanced_result.parsed_data)
        
        self.logger.info(f"Raw format extraction: {raw_success} fields")
        self.logger.info(f"Enhanced format extraction: {enhanced_success} fields")
        self.logger.info(f"Difference: {enhanced_success - raw_success} fields")
        
        if raw_success != enhanced_success:
            self.logger.error("🚨 CONFIRMED: Data source mismatch causes different parsing results!")
        else:
            self.logger.info("✅ Both formats produce same results")
        
        return raw_result, enhanced_result
    
    async def identify_fix_requirements(self, production_response):
        """
        Determine exact fix needed based on investigation results
        """
        self.logger.info("-" * 60)
        self.logger.info("IDENTIFYING FIX REQUIREMENTS")
        self.logger.info("-" * 60)
        
        raw_response = production_response.output
        
        # Detailed analysis of raw response format
        self.logger.info("ANALYZING RAW RESPONSE FORMAT:")
        
        # Check for key indicators in raw response
        has_price_indicators = bool(re.search(r'price', raw_response, re.IGNORECASE))
        has_dollar_signs = '$' in raw_response
        has_percentages = '%' in raw_response
        has_volume = bool(re.search(r'volume', raw_response, re.IGNORECASE))
        
        self.logger.info(f"- Contains 'price': {has_price_indicators}")
        self.logger.info(f"- Contains '$': {has_dollar_signs}")
        self.logger.info(f"- Contains '%': {has_percentages}")
        self.logger.info(f"- Contains 'volume': {has_volume}")
        
        # Test specific patterns that should match
        test_patterns = [
            (r'(?:current\s+)?price[:\s]*\$?\s*([\d,]+\.\d+)', "current_price"),
            (r'([\+\-]?[\d\.]+)%', "percentage_change"),
            (r'volume[:\s]*([\d,]+(?:\.\d+)?[KMB]?)', "volume"),
        ]
        
        self.logger.info("TESTING KEY PATTERNS AGAINST RAW RESPONSE:")
        for pattern, name in test_patterns:
            match = re.search(pattern, raw_response, re.IGNORECASE)
            if match:
                self.logger.info(f"✅ {name}: FOUND '{match.group(1)}' with pattern '{pattern}'")
            else:
                self.logger.info(f"❌ {name}: NO MATCH with pattern '{pattern}'")
        
        # Show sample context around key terms
        self.logger.info("CONTEXT ANALYSIS:")
        key_terms = ['price', 'volume', '%', '$']
        for term in key_terms:
            positions = [m.start() for m in re.finditer(re.escape(term), raw_response, re.IGNORECASE)]
            for pos in positions[:3]:  # Show first 3 occurrences
                start = max(0, pos - 50)
                end = min(len(raw_response), pos + 50)
                context = raw_response[start:end]
                self.logger.info(f"Context for '{term}' at pos {pos}: ...{context}...")
        
        # Determine if format or patterns need fixing
        self.logger.info("=" * 40)
        self.logger.info("FIX RECOMMENDATIONS:")
        self.logger.info("=" * 40)
        
        if has_price_indicators and has_dollar_signs:
            self.logger.info("✅ Raw response contains expected financial data indicators")
            self.logger.info("🔧 LIKELY FIX: Parser patterns need improvement to handle actual AI response format")
        else:
            self.logger.info("❌ Raw response missing expected financial indicators")
            self.logger.info("🔧 LIKELY FIX: AI prompt or response format needs adjustment")

def add_debug_logging_to_parser():
    """
    Add extensive debug logging to response_parser.py to track exact input
    """
    parser_debug_code = '''
    
    # CRITICAL DEBUG: Add at start of parse_stock_snapshot method (after line 183)
    
    # EXTENSIVE DEBUG LOGGING FOR BUG INVESTIGATION
    self.logger.error("🚨 CRITICAL DEBUG: Parser input analysis")
    self.logger.error(f"Input type: {type(text)}")
    self.logger.error(f"Input length: {len(text)} characters")
    self.logger.error(f"Input repr: {repr(text)}")
    self.logger.error(f"Input first 200 chars: {text[:200]}")
    self.logger.error(f"Input last 200 chars: {text[-200:]}")
    
    # Check for key financial indicators
    price_count = len(re.findall(r'price', text, re.IGNORECASE))
    dollar_count = text.count('$')
    percent_count = text.count('%')
    volume_count = len(re.findall(r'volume', text, re.IGNORECASE))
    
    self.logger.error(f"Financial indicators: price={price_count}, $={dollar_count}, %={percent_count}, volume={volume_count}")
    
    # Test critical patterns manually
    test_patterns = {
        'current_price': r'(?:current\s+)?price[:\s]*\$?\s*([\d,]+\.\d+)',
        'percentage': r'([\+\-]?[\d\.]+)%',
        'dollar_value': r'\$\s*([\d,]+\.\d+)',
        'volume': r'volume[:\s]*([\d,]+(?:\.\d+)?[KMB]?)'
    }
    
    for name, pattern in test_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        self.logger.error(f"Pattern '{name}': {len(matches)} matches - {matches[:3]}")
    
    # Show context around each $ sign
    for i, match in enumerate(re.finditer(r'\$', text)):
        start = max(0, match.start() - 30)
        end = min(len(text), match.start() + 30)
        context = text[start:end]
        self.logger.error(f"$ context {i+1}: ...{context}...")
        if i >= 5:  # Limit to first 5
            break
    '''
    
    print("🔧 DEBUG CODE TO ADD TO response_parser.py:")
    print(parser_debug_code)

async def main():
    """Run the complete investigation"""
    investigator = DataSourceInvestigator()
    
    print("🚨 STARTING CRITICAL BUG INVESTIGATION")
    print("This will prove the data source mismatch hypothesis")
    print("Check debug_parser_investigation.log for detailed results")
    
    await investigator.investigate_data_sources()
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Check debug_parser_investigation.log for detailed findings")
    print("2. Add debug logging to response_parser.py if needed")
    print("3. Fix identified data source mismatch")
    
    add_debug_logging_to_parser()

if __name__ == "__main__":
    asyncio.run(main())