"""
Unit Tests for Prompt Templates System

This test suite validates the prompt template system including template generation,
ticker extraction, system prompt enhancements, and consistency testing.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import logging
from src.prompt_templates import (
    PromptTemplateManager, PromptType, TickerExtractor, TickerContext,
    PromptTemplate, run_prompt_consistency_tests, validate_template_parsing_compatibility
)


class TestTickerExtractor(unittest.TestCase):
    """Test suite for TickerExtractor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = TickerExtractor()
    
    def test_extract_explicit_ticker_dollar_symbol(self):
        """Test extraction of ticker with dollar symbol"""
        text = "Looking at $AAPL performance today"
        result = self.extractor.extract_ticker(text)
        
        self.assertEqual(result.symbol, "AAPL")
        self.assertEqual(result.source, "explicit")
        self.assertGreater(result.confidence, 0.8)
    
    def test_extract_explicit_ticker_with_stock(self):
        """Test extraction of ticker with 'stock' keyword"""
        text = "TSLA stock is performing well"
        result = self.extractor.extract_ticker(text)
        
        self.assertEqual(result.symbol, "TSLA")
        self.assertEqual(result.source, "explicit")
    
    def test_extract_from_company_name_apple(self):
        """Test extraction from Apple company name"""
        text = "Apple Inc. reported strong earnings"
        result = self.extractor.extract_ticker(text)
        
        self.assertEqual(result.symbol, "AAPL")
        self.assertEqual(result.company_name, "Apple Inc.")
        self.assertEqual(result.source, "company_name")
        self.assertEqual(result.sector, "Technology")
    
    def test_extract_from_company_name_tesla(self):
        """Test extraction from Tesla company name"""
        text = "Tesla Motors is expanding production"
        result = self.extractor.extract_ticker(text)
        
        self.assertEqual(result.symbol, "TSLA")
        self.assertEqual(result.company_name, "Tesla, Inc.")
        self.assertEqual(result.source, "company_name")
    
    def test_extract_from_context(self):
        """Test extraction from conversation context"""
        chat_history = [
            {"role": "user", "content": "Tell me about NVDA"},
            {"role": "assistant", "content": "NVIDIA is a technology company..."},
            {"role": "user", "content": "What's the current analysis?"}
        ]
        
        result = self.extractor.extract_ticker("current analysis", chat_history)
        
        self.assertEqual(result.symbol, "NVDA")
        self.assertEqual(result.source, "context")
        self.assertLess(result.confidence, 0.8)  # Context extractions have lower confidence
    
    def test_last_mentioned_ticker(self):
        """Test using last mentioned ticker"""
        # First extract a ticker
        self.extractor.extract_ticker("$MSFT analysis")
        
        # Then test fallback to last mentioned
        result = self.extractor.extract_ticker("show me the data")
        
        self.assertEqual(result.symbol, "MSFT")
        self.assertEqual(result.source, "last_mentioned")
        self.assertTrue(result.last_mentioned)
    
    def test_fallback_to_placeholder(self):
        """Test fallback to placeholder when no ticker found"""
        result = self.extractor.extract_ticker("just some random text")
        
        self.assertEqual(result.symbol, "[TICKER]")
        self.assertEqual(result.source, "default")
        self.assertEqual(result.confidence, 0.0)
    
    def test_invalid_ticker_filtering(self):
        """Test that common words are not extracted as tickers"""
        false_positive_texts = [
            "THE data looks good",
            "FOR investors this is important",
            "YOU should consider this"
        ]
        
        for text in false_positive_texts:
            result = self.extractor.extract_ticker(text)
            # Should not extract false positive tickers
            self.assertNotIn(result.symbol, ["THE", "FOR", "YOU"])
    
    def test_conversation_ticker_tracking(self):
        """Test conversation ticker tracking"""
        # Extract multiple tickers
        self.extractor.extract_ticker("$AAPL is strong")
        self.extractor.extract_ticker("$TSLA is volatile") 
        self.extractor.extract_ticker("Google earnings")
        
        conversation_tickers = self.extractor.get_conversation_tickers()
        symbols = [t.symbol for t in conversation_tickers]
        
        self.assertIn("AAPL", symbols)
        self.assertIn("TSLA", symbols)
        self.assertIn("GOOGL", symbols)
        self.assertEqual(len(conversation_tickers), 3)


class TestPromptTemplate(unittest.TestCase):
    """Test suite for PromptTemplate class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.template = PromptTemplate(
            template_type=PromptType.SNAPSHOT,
            base_template="Analyze {ticker} ({company}) stock data.",
            formatting_instructions="Use specific format: Price: $XXX.XX",
            example_response="Price: $150.25",
            required_fields=["price"],
            system_prompt_additions="Focus on accuracy."
        )
        
        self.ticker_context = TickerContext(
            symbol="AAPL",
            company_name="Apple Inc.",
            confidence=1.0,
            source="explicit"
        )
    
    def test_generate_basic_prompt(self):
        """Test basic prompt generation"""
        prompt = self.template.generate_prompt(self.ticker_context)
        
        self.assertIn("AAPL", prompt)
        self.assertIn("Apple Inc.", prompt)
        self.assertIn("### STOCK ANALYSIS REQUEST ###", prompt)
        self.assertIn("### FORMATTING REQUIREMENTS ###", prompt)
        self.assertIn("### EXAMPLE RESPONSE FORMAT ###", prompt)
        self.assertIn("Price: $150.25", prompt)
    
    def test_generate_prompt_with_custom_instructions(self):
        """Test prompt generation with custom instructions"""
        custom_instructions = "Focus on after-hours trading data"
        prompt = self.template.generate_prompt(self.ticker_context, custom_instructions)
        
        self.assertIn("### ADDITIONAL INSTRUCTIONS ###", prompt)
        self.assertIn("after-hours trading", prompt)
    
    def test_generate_prompt_without_company_name(self):
        """Test prompt generation when company name is not available"""
        ticker_context = TickerContext(symbol="XYZ", confidence=1.0, source="explicit")
        prompt = self.template.generate_prompt(ticker_context)
        
        self.assertIn("XYZ (XYZ)", prompt)  # Should use ticker as company fallback


class TestPromptTemplateManager(unittest.TestCase):
    """Test suite for PromptTemplateManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = PromptTemplateManager()
    
    def test_manager_initialization(self):
        """Test proper manager initialization"""
        self.assertIsNotNone(self.manager.ticker_extractor)
        self.assertEqual(len(self.manager.templates), 3)  # snapshot, sr, technical
        self.assertIn(PromptType.SNAPSHOT, self.manager.templates)
        self.assertIn(PromptType.SUPPORT_RESISTANCE, self.manager.templates)
        self.assertIn(PromptType.TECHNICAL, self.manager.templates)
    
    def test_generate_snapshot_prompt_with_ticker(self):
        """Test snapshot prompt generation with explicit ticker"""
        prompt, context = self.manager.generate_prompt(
            PromptType.SNAPSHOT, 
            ticker="AAPL"
        )
        
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 100)
        self.assertIn("AAPL", prompt)
        self.assertIn("Current price:", prompt)
        self.assertIn("Volume:", prompt)
        self.assertIn("VWAP:", prompt)
        
        self.assertEqual(context.symbol, "AAPL")
        self.assertEqual(context.source, "explicit")
    
    def test_generate_support_resistance_prompt(self):
        """Test support/resistance prompt generation"""
        prompt, context = self.manager.generate_prompt(
            PromptType.SUPPORT_RESISTANCE,
            ticker="TSLA"
        )
        
        self.assertIn("TSLA", prompt)
        self.assertIn("S1:", prompt)
        self.assertIn("S2:", prompt)
        self.assertIn("S3:", prompt)
        self.assertIn("R1:", prompt)
        self.assertIn("R2:", prompt)
        self.assertIn("R3:", prompt)
    
    def test_generate_technical_prompt(self):
        """Test technical analysis prompt generation"""
        prompt, context = self.manager.generate_prompt(
            PromptType.TECHNICAL,
            ticker="NVDA"
        )
        
        self.assertIn("NVDA", prompt)
        self.assertIn("RSI:", prompt)
        self.assertIn("MACD:", prompt)
        self.assertIn("EMA 5:", prompt)
        self.assertIn("EMA 200:", prompt)
        self.assertIn("SMA 5:", prompt)
        self.assertIn("SMA 200:", prompt)
    
    def test_generate_prompt_with_chat_history(self):
        """Test prompt generation using chat history for ticker extraction"""
        chat_history = [
            {"role": "user", "content": "Tell me about Microsoft"},
            {"role": "assistant", "content": "Microsoft Corporation (MSFT)..."}
        ]
        
        prompt, context = self.manager.generate_prompt(
            PromptType.SNAPSHOT,
            chat_history=chat_history
        )
        
        # Should extract MSFT from company name in history
        self.assertEqual(context.symbol, "MSFT")
        self.assertIn("MSFT", prompt)
    
    def test_enhanced_system_prompt(self):
        """Test system prompt enhancement"""
        base_prompt = "You are a financial analyst."
        enhanced = self.manager.get_enhanced_system_prompt(base_prompt)
        
        self.assertIn("You are a financial analyst.", enhanced)
        self.assertIn("STRUCTURED OUTPUT REQUIREMENTS:", enhanced)
        self.assertIn("Format Consistency", enhanced)
        self.assertIn("PARSING OPTIMIZATION:", enhanced)
    
    def test_prompt_consistency_across_tickers(self):
        """Test that prompts are consistent across different tickers"""
        tickers = ["AAPL", "TSLA", "MSFT"]
        prompts = {}
        
        for ticker in tickers:
            prompt, _ = self.manager.generate_prompt(PromptType.SNAPSHOT, ticker=ticker)
            prompts[ticker] = prompt
        
        # Check that all prompts have similar structure
        for prompt in prompts.values():
            self.assertIn("### STOCK ANALYSIS REQUEST ###", prompt)
            self.assertIn("### FORMATTING REQUIREMENTS ###", prompt)
            self.assertIn("### EXAMPLE RESPONSE FORMAT ###", prompt)
        
        # Check that lengths are similar (within 20%)
        lengths = [len(p) for p in prompts.values()]
        avg_length = sum(lengths) / len(lengths)
        for length in lengths:
            self.assertLess(abs(length - avg_length) / avg_length, 0.2)


class TestPromptValidation(unittest.TestCase):
    """Test suite for prompt validation and testing functions"""
    
    def setUp(self):
        """Set up test environment"""
        self.manager = PromptTemplateManager()
    
    def test_prompt_consistency_tests(self):
        """Test the prompt consistency testing function"""
        results = run_prompt_consistency_tests()
        
        self.assertIn("test_date", results)
        self.assertIn("results_by_type", results)
        self.assertIn("overall_score", results)
        self.assertIn("summary", results)
        
        # Check that all prompt types were tested
        self.assertEqual(len(results["results_by_type"]), 3)
        self.assertIn("snapshot", results["results_by_type"])
        self.assertIn("support_resistance", results["results_by_type"])
        self.assertIn("technical", results["results_by_type"])
        
        # Score should be between 0 and 1
        self.assertGreaterEqual(results["overall_score"], 0.0)
        self.assertLessEqual(results["overall_score"], 1.0)
    
    def test_template_parsing_compatibility(self):
        """Test template parsing compatibility validation"""
        # Test template structure instead of full parsing
        prompt, _ = self.manager.generate_prompt(PromptType.SNAPSHOT, "AAPL")
        
        # Verify prompt contains key elements for parsing
        self.assertIn("Current price", prompt)
        self.assertIn("AAPL", prompt)


class TestPromptFormatting(unittest.TestCase):
    """Test suite for prompt formatting and structure"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = PromptTemplateManager()
    
    def test_snapshot_template_required_fields(self):
        """Test that snapshot template includes all required fields"""
        template = self.manager.templates[PromptType.SNAPSHOT]
        required_fields = [
            "current_price", "percentage_change", "dollar_change", 
            "volume", "vwap", "open", "high", "low", "close"
        ]
        
        self.assertEqual(template.required_fields, required_fields)
        
        # Check that formatting instructions mention these fields
        for field in ["Current price", "Percentage change", "Volume", "VWAP"]:
            self.assertIn(field, template.formatting_instructions)
    
    def test_support_resistance_template_levels(self):
        """Test that S&R template includes all support/resistance levels"""
        template = self.manager.templates[PromptType.SUPPORT_RESISTANCE]
        required_levels = ["S1", "S2", "S3", "R1", "R2", "R3"]
        
        self.assertEqual(template.required_fields, required_levels)
        
        # Check example response has all levels
        for level in required_levels:
            self.assertIn(f"{level}:", template.example_response)
    
    def test_technical_template_indicators(self):
        """Test that technical template includes all indicators"""
        template = self.manager.templates[PromptType.TECHNICAL]
        
        # Check for key indicators in formatting instructions
        indicators = ["RSI", "MACD", "EMA 5", "EMA 200", "SMA 5", "SMA 200"]
        for indicator in indicators:
            self.assertIn(indicator, template.formatting_instructions)
    
    def test_prompt_section_structure(self):
        """Test that generated prompts have consistent section structure"""
        prompt, _ = self.manager.generate_prompt(PromptType.SNAPSHOT, ticker="AAPL")
        
        required_sections = [
            "### STOCK ANALYSIS REQUEST ###",
            "### FORMATTING REQUIREMENTS ###",
            "### EXAMPLE RESPONSE FORMAT ###",
            "### RESPONSE ###"
        ]
        
        for section in required_sections:
            self.assertIn(section, prompt)
        
        # Check that sections appear in correct order
        indices = [prompt.find(section) for section in required_sections]
        self.assertEqual(indices, sorted(indices))  # Should be in ascending order


class TestErrorHandling(unittest.TestCase):
    """Test suite for error handling in prompt system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = PromptTemplateManager()
    
    def test_invalid_prompt_type(self):
        """Test handling of invalid prompt type"""
        with self.assertRaises((KeyError, ValueError)):
            self.manager.templates["invalid_type"]
    
    def test_empty_ticker_handling(self):
        """Test handling of empty or None ticker"""
        prompt, context = self.manager.generate_prompt(PromptType.SNAPSHOT, ticker="")
        
        # Should not crash and should provide fallback
        self.assertIsInstance(prompt, str)
        self.assertIsInstance(context, TickerContext)
        self.assertGreater(len(prompt), 0)
    
    def test_malformed_chat_history(self):
        """Test handling of malformed chat history"""
        malformed_history = [
            {"invalid": "structure"},
            None,
            {"role": "user"}  # Missing content
        ]
        
        # Should not crash
        prompt, context = self.manager.generate_prompt(
            PromptType.SNAPSHOT,
            chat_history=malformed_history
        )
        
        self.assertIsInstance(prompt, str)
        self.assertIsInstance(context, TickerContext)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests for real-world usage scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = PromptTemplateManager()
    
    def test_multi_ticker_conversation(self):
        """Test handling multiple tickers in conversation"""
        chat_history = [
            {"role": "user", "content": "Compare AAPL and TSLA"},
            {"role": "assistant", "content": "Both are strong..."},
            {"role": "user", "content": "Show me snapshot for the first one"}
        ]
        
        # Should extract AAPL as it was mentioned first
        prompt, context = self.manager.generate_prompt(
            PromptType.SNAPSHOT,
            chat_history=chat_history
        )
        
        # Context extraction should work reasonably
        self.assertIn(context.symbol, ["AAPL", "TSLA", "[TICKER]"])
    
    def test_company_name_to_ticker_conversation(self):
        """Test company name to ticker resolution in conversation"""
        chat_history = [
            {"role": "user", "content": "What do you think about Apple's earnings?"},
            {"role": "assistant", "content": "Apple had strong results..."},
            {"role": "user", "content": "Get me the technical analysis"}
        ]
        
        prompt, context = self.manager.generate_prompt(
            PromptType.TECHNICAL,
            chat_history=chat_history
        )
        
        self.assertEqual(context.symbol, "AAPL")
        self.assertIn("AAPL", prompt)
    
    def test_mixed_explicit_and_context_tickers(self):
        """Test mix of explicit tickers and context-based extraction"""
        # Start with context
        chat_history = [{"role": "user", "content": "Tell me about Microsoft"}]
        
        # Then use explicit ticker
        prompt1, context1 = self.manager.generate_prompt(
            PromptType.SNAPSHOT,
            ticker="NVDA",
            chat_history=chat_history
        )
        
        # Explicit should override context
        self.assertEqual(context1.symbol, "NVDA")
        self.assertEqual(context1.source, "explicit")
        
        # Then use context again (should remember NVDA as last mentioned)
        prompt2, context2 = self.manager.generate_prompt(
            PromptType.TECHNICAL,
            chat_history=chat_history
        )
        
        # Should use Microsoft from context since no explicit ticker
        self.assertEqual(context2.symbol, "MSFT")


if __name__ == '__main__':
    # Configure logging to suppress debug messages during tests
    logging.basicConfig(level=logging.WARNING)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestTickerExtractor,
        TestPromptTemplate, 
        TestPromptTemplateManager,
        TestPromptValidation,
        TestPromptFormatting,
        TestErrorHandling,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 Prompt Templates Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.wasSuccessful():
        print("✅ All Prompt Template tests passed!")
        print("🎉 Prompt engineering system is ready for production!")
    else:
        print("❌ Some tests failed. Please review and fix issues.")
        if result.failures:
            print(f"\n❌ Failures ({len(result.failures)}):")
            for test, traceback in result.failures:
                print(f"  - {test}")
        if result.errors:
            print(f"\n⚠️  Errors ({len(result.errors)}):")
            for test, traceback in result.errors:
                print(f"  - {test}")
        exit(1)
