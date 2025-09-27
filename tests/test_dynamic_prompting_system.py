"""
Test suite for the Dynamic Adaptive Prompting System

This module provides comprehensive tests for the dynamic prompting system
including user instruction parsing, template customization, validation,
and integration with the existing Market Parser system.

Author: AI Assistant
Date: September 26, 2025
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime

# Import the dynamic prompting system components
from src.backend.dynamic_prompts import (
    DynamicPromptManager,
    InstructionParser,
    TemplateEngine,
    InputValidator,
    PromptCache,
    UserPreferences,
    ValidationError,
    TemplateError,
    create_dynamic_prompt_manager
)

from src.backend.dynamic_prompt_manager import MarketParserDynamicPromptManager
from src.backend.dynamic_prompt_integration import get_enhanced_agent_instructions


class TestUserPreferences(unittest.TestCase):
    """Test the UserPreferences data class"""
    
    def test_default_preferences(self):
        """Test default preference values"""
        prefs = UserPreferences()
        self.assertIsNone(prefs.verbosity)
        self.assertIsNone(prefs.tool_usage)
        self.assertIsNone(prefs.output_format)
        self.assertIsNone(prefs.response_style)
    
    def test_custom_preferences(self):
        """Test setting custom preferences"""
        prefs = UserPreferences(
            verbosity="verbose",
            tool_usage="minimal tools",
            output_format="structured",
            response_style="professional"
        )
        self.assertEqual(prefs.verbosity, "verbose")
        self.assertEqual(prefs.tool_usage, "minimal tools")
        self.assertEqual(prefs.output_format, "structured")
        self.assertEqual(prefs.response_style, "professional")


class TestInstructionParser(unittest.TestCase):
    """Test the InstructionParser class"""
    
    def setUp(self):
        self.parser = InstructionParser()
    
    def test_verbosity_parsing(self):
        """Test parsing verbosity instructions"""
        test_cases = [
            ("[verbose] Get NVDA price", {"verbosity": "verbose"}),
            ("[minimal] Show SPY data", {"verbosity": "minimal"}),
            ("[detailed] Analyze QQQ", {"verbosity": "detailed"}),
            ("[brief] What's GME price?", {"verbosity": "brief"}),
            ("[concise] Market status", {"verbosity": "concise"}),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.extract_preferences(input_text)
                self.assertEqual(result, expected)
    
    def test_tool_usage_parsing(self):
        """Test parsing tool usage instructions"""
        test_cases = [
            ("[use only get_snapshot_ticker] Get NVDA", {"tool_usage": "get_snapshot_ticker"}),
            ("[avoid get_market_status] Show data", {"tool_usage": "get_market_status"}),
            ("[minimal tools] Quick analysis", {"tool_usage": "minimal tools"}),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.extract_preferences(input_text)
                self.assertEqual(result, expected)
    
    def test_output_format_parsing(self):
        """Test parsing output format instructions"""
        test_cases = [
            ("[structured] Get data", {"output_format": "structured"}),
            ("[narrative] Tell me about NVDA", {"output_format": "narrative"}),
            ("[bullet points] Show results", {"output_format": "bullet points"}),
            ("[JSON] Format response", {"output_format": "JSON"}),
            ("[markdown] Display data", {"output_format": "markdown"}),
            ("[plain] Simple output", {"output_format": "plain"}),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.extract_preferences(input_text)
                self.assertEqual(result, expected)
    
    def test_response_style_parsing(self):
        """Test parsing response style instructions"""
        test_cases = [
            ("[formal] Analyze market", {"response_style": "formal"}),
            ("[casual] What's up with stocks?", {"response_style": "casual"}),
            ("[technical] Deep dive analysis", {"response_style": "technical"}),
            ("[professional] Business report", {"response_style": "professional"}),
            ("[friendly] Help me understand", {"response_style": "friendly"}),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.extract_preferences(input_text)
                self.assertEqual(result, expected)
    
    def test_multiple_preferences_parsing(self):
        """Test parsing multiple preferences in one input"""
        input_text = "[verbose] [structured] [professional] Get NVDA analysis"
        result = self.parser.extract_preferences(input_text)
        expected = {
            "verbosity": "verbose",
            "output_format": "structured",
            "response_style": "professional"
        }
        self.assertEqual(result, expected)
    
    def test_case_insensitive_parsing(self):
        """Test that parsing is case insensitive"""
        input_text = "[VERBOSE] [STRUCTURED] [PROFESSIONAL] Get data"
        result = self.parser.extract_preferences(input_text)
        expected = {
            "verbosity": "VERBOSE",
            "output_format": "STRUCTURED",
            "response_style": "PROFESSIONAL"
        }
        self.assertEqual(result, expected)
    
    def test_no_preferences_parsing(self):
        """Test parsing input with no preferences"""
        input_text = "Get NVDA price"
        result = self.parser.extract_preferences(input_text)
        self.assertEqual(result, {})


class TestTemplateEngine(unittest.TestCase):
    """Test the TemplateEngine class"""
    
    def setUp(self):
        self.engine = TemplateEngine()
        self.base_template = """Quick Response Needed: You are a financial analyst.

{verbosity_instruction}
{tool_restriction}
{format_instruction}
{style_instruction}

Provide financial analysis."""
    
    def test_verbosity_template_application(self):
        """Test applying verbosity customizations"""
        preferences = {"verbosity": "verbose"}
        context = {}
        
        result = self.engine.apply_preferences(self.base_template, preferences, context)
        
        self.assertIn("Provide comprehensive information with detailed explanations", result)
        self.assertNotIn("{verbosity_instruction}", result)
    
    def test_tool_usage_template_application(self):
        """Test applying tool usage customizations"""
        preferences = {"tool_usage": "use only get_snapshot_ticker"}
        context = {}
        
        result = self.engine.apply_preferences(self.base_template, preferences, context)
        
        self.assertIn("Use only the following tools: get_snapshot_ticker", result)
        self.assertNotIn("{tool_restriction}", result)
    
    def test_output_format_template_application(self):
        """Test applying output format customizations"""
        preferences = {"output_format": "structured"}
        context = {}
        
        result = self.engine.apply_preferences(self.base_template, preferences, context)
        
        self.assertIn("Format your response in a structured format", result)
        self.assertNotIn("{format_instruction}", result)
    
    def test_response_style_template_application(self):
        """Test applying response style customizations"""
        preferences = {"response_style": "professional"}
        context = {}
        
        result = self.engine.apply_preferences(self.base_template, preferences, context)
        
        self.assertIn("Use a professional, business-appropriate tone", result)
        self.assertNotIn("{style_instruction}", result)
    
    def test_multiple_preferences_application(self):
        """Test applying multiple preferences at once"""
        preferences = {
            "verbosity": "minimal",
            "output_format": "bullet points",
            "response_style": "casual"
        }
        context = {}
        
        result = self.engine.apply_preferences(self.base_template, preferences, context)
        
        self.assertIn("Provide only essential information", result)
        self.assertIn("Format your response using bullet points", result)
        self.assertIn("Use a casual, friendly tone", result)
        self.assertNotIn("{verbosity_instruction}", result)
        self.assertNotIn("{format_instruction}", result)
        self.assertNotIn("{style_instruction}", result)


class TestInputValidator(unittest.TestCase):
    """Test the InputValidator class"""
    
    def setUp(self):
        self.validator = InputValidator({})
    
    def test_valid_verbosity_validation(self):
        """Test validation of valid verbosity levels"""
        valid_verbs = ["verbose", "minimal", "standard", "detailed", "brief", "concise"]
        
        for verb in valid_verbs:
            with self.subTest(verb=verb):
                prefs = UserPreferences(verbosity=verb)
                # Should not raise an exception
                self.validator.validate_preferences({"verbosity": verb})
    
    def test_invalid_verbosity_validation(self):
        """Test validation of invalid verbosity levels"""
        with self.assertRaises(ValidationError):
            self.validator.validate_preferences({"verbosity": "invalid"})
    
    def test_valid_tool_usage_validation(self):
        """Test validation of valid tool usage instructions"""
        valid_instructions = [
            "use only get_snapshot_ticker",
            "avoid get_market_status",
            "minimal tools"
        ]
        
        for instruction in valid_instructions:
            with self.subTest(instruction=instruction):
                # Should not raise an exception
                self.validator.validate_preferences({"tool_usage": instruction})
    
    def test_invalid_tool_usage_validation(self):
        """Test validation of invalid tool usage instructions"""
        with self.assertRaises(ValidationError):
            self.validator.validate_preferences({"tool_usage": "use only invalid_tool"})
    
    def test_valid_output_format_validation(self):
        """Test validation of valid output formats"""
        valid_formats = ["structured", "narrative", "bullet points", "json", "markdown", "plain"]
        
        for format_type in valid_formats:
            with self.subTest(format=format_type):
                # Should not raise an exception
                self.validator.validate_preferences({"output_format": format_type})
    
    def test_invalid_output_format_validation(self):
        """Test validation of invalid output formats"""
        with self.assertRaises(ValidationError):
            self.validator.validate_preferences({"output_format": "invalid"})
    
    def test_valid_response_style_validation(self):
        """Test validation of valid response styles"""
        valid_styles = ["formal", "casual", "technical", "professional", "friendly"]
        
        for style in valid_styles:
            with self.subTest(style=style):
                # Should not raise an exception
                self.validator.validate_preferences({"response_style": style})
    
    def test_invalid_response_style_validation(self):
        """Test validation of invalid response styles"""
        with self.assertRaises(ValidationError):
            self.validator.validate_preferences({"response_style": "invalid"})
    
    def test_sanitize_preferences(self):
        """Test sanitization of user preferences"""
        raw_prefs = {
            "verbosity": "verbose<script>",
            "output_format": "structured<alert>",
            "response_style": "professional'"
        }
        
        sanitized = self.validator.sanitize_preferences(raw_prefs)
        
        self.assertEqual(sanitized.verbosity, "verbosescript")
        self.assertEqual(sanitized.output_format, "structuredalert")
        self.assertEqual(sanitized.response_style, "professional")


class TestPromptCache(unittest.TestCase):
    """Test the PromptCache class"""
    
    def setUp(self):
        self.cache = PromptCache(max_size=3)
    
    def test_cache_store_and_get(self):
        """Test storing and retrieving from cache"""
        key = "test_key"
        value = "test_prompt"
        
        self.cache.store(key, value)
        result = self.cache.get(key)
        
        self.assertEqual(result, value)
    
    def test_cache_miss(self):
        """Test cache miss behavior"""
        result = self.cache.get("nonexistent_key")
        self.assertIsNone(result)
    
    def test_cache_eviction(self):
        """Test cache eviction when max size is reached"""
        # Fill cache to max size
        for i in range(3):
            self.cache.store(f"key_{i}", f"value_{i}")
        
        # Add one more item to trigger eviction
        self.cache.store("key_3", "value_3")
        
        # Should have evicted the oldest item
        self.assertEqual(len(self.cache.cache), 3)
        self.assertIn("key_3", self.cache.cache)
    
    def test_cache_access_time_update(self):
        """Test that cache access updates access time"""
        key = "test_key"
        value = "test_prompt"
        
        self.cache.store(key, value)
        first_access_time = self.cache.access_times[key]
        
        # Access the item
        self.cache.get(key)
        second_access_time = self.cache.access_times[key]
        
        self.assertGreater(second_access_time, first_access_time)


class TestDynamicPromptManager(unittest.TestCase):
    """Test the DynamicPromptManager class"""
    
    def setUp(self):
        self.base_template = """Quick Response: You are a financial analyst.

{verbosity_instruction}
{tool_restriction}
{format_instruction}
{style_instruction}

Provide analysis."""
        
        self.config = {
            'cache_size': 10,
            'security_rules': {}
        }
        
        self.manager = DynamicPromptManager(self.base_template, self.config)
    
    def test_generate_prompt_with_preferences(self):
        """Test generating prompt with user preferences"""
        user_input = "[verbose] [structured] [professional] Get NVDA data"
        context = {}
        
        result = self.manager.generate_prompt(user_input, context)
        
        self.assertIn("comprehensive information with detailed explanations", result)
        self.assertIn("structured format", result)
        self.assertIn("professional, business-appropriate tone", result)
    
    def test_generate_prompt_without_preferences(self):
        """Test generating prompt without user preferences"""
        user_input = "Get NVDA data"
        context = {}
        
        result = self.manager.generate_prompt(user_input, context)
        
        # Should return base template with default values
        self.assertIn("Quick Response: You are a financial analyst", result)
    
    def test_validation_error_handling(self):
        """Test handling of validation errors"""
        user_input = "[invalid_verbosity] Get data"
        context = {}
        
        result = self.manager.generate_prompt(user_input, context)
        
        # Should return fallback prompt
        self.assertIn("Quick Response: You are a financial analyst", result)
    
    def test_template_error_handling(self):
        """Test handling of template errors"""
        # Mock template engine to raise error
        with patch.object(self.manager.template_engine, 'apply_preferences', side_effect=TemplateError("Test error")):
            user_input = "[verbose] Get data"
            context = {}
            
            result = self.manager.generate_prompt(user_input, context)
            
            # Should return fallback prompt
            self.assertIn("Quick Response: You are a financial analyst", result)
    
    def test_general_error_handling(self):
        """Test handling of general errors"""
        # Mock instruction parser to raise error
        with patch.object(self.manager.instruction_parser, 'extract_preferences', side_effect=Exception("Test error")):
            user_input = "[verbose] Get data"
            context = {}
            
            result = self.manager.generate_prompt(user_input, context)
            
            # Should return fallback prompt
            self.assertIn("Quick Response: You are a financial analyst", result)


class TestMarketParserDynamicPromptManager(unittest.TestCase):
    """Test the MarketParserDynamicPromptManager class"""
    
    def setUp(self):
        self.manager = MarketParserDynamicPromptManager()
    
    def test_get_enhanced_agent_instructions_without_input(self):
        """Test getting instructions without user input"""
        result = self.manager.get_enhanced_agent_instructions()
        
        self.assertIn("Quick Response Needed with minimal tool calls", result)
        self.assertIn("CURRENT DATE AND TIME CONTEXT", result)
        self.assertIn("TOOLS: Polygon.io MCP server", result)
    
    def test_get_enhanced_agent_instructions_with_input(self):
        """Test getting instructions with user input"""
        user_input = "[verbose] [structured] [professional] Get NVDA data"
        result = self.manager.get_enhanced_agent_instructions(user_input)
        
        self.assertIn("Quick Response Needed with minimal tool calls", result)
        self.assertIn("comprehensive information with detailed explanations", result)
        self.assertIn("structured format", result)
        self.assertIn("professional, business-appropriate tone", result)
    
    def test_get_cache_stats(self):
        """Test getting cache statistics"""
        stats = self.manager.get_cache_stats()
        
        self.assertIn("cache_size", stats)
        self.assertIn("max_size", stats)
        self.assertIn("hit_rate", stats)
    
    def test_clear_cache(self):
        """Test clearing the cache"""
        # Store something in cache first
        self.manager.dynamic_manager.cache.store("test", "value")
        self.assertEqual(len(self.manager.dynamic_manager.cache.cache), 1)
        
        # Clear cache
        self.manager.clear_cache()
        self.assertEqual(len(self.manager.dynamic_manager.cache.cache), 0)


class TestDynamicPromptIntegration(unittest.TestCase):
    """Test the dynamic prompt integration functions"""
    
    def test_get_enhanced_agent_instructions_without_input(self):
        """Test the integration function without user input"""
        result = get_enhanced_agent_instructions()
        
        self.assertIn("Quick Response Needed with minimal tool calls", result)
        self.assertIn("CURRENT DATE AND TIME CONTEXT", result)
    
    def test_get_enhanced_agent_instructions_with_input(self):
        """Test the integration function with user input"""
        user_input = "[verbose] [structured] [professional] Get NVDA data"
        result = get_enhanced_agent_instructions(user_input)
        
        self.assertIn("Quick Response Needed with minimal tool calls", result)
        self.assertIn("comprehensive information with detailed explanations", result)
        self.assertIn("structured format", result)
        self.assertIn("professional, business-appropriate tone", result)
    
    def test_get_dynamic_prompt_stats(self):
        """Test getting dynamic prompt statistics"""
        from src.backend.dynamic_prompt_integration import get_dynamic_prompt_stats
        
        stats = get_dynamic_prompt_stats()
        
        self.assertIn("cache_size", stats)
        self.assertIn("max_size", stats)
    
    def test_clear_dynamic_prompt_cache(self):
        """Test clearing the dynamic prompt cache"""
        from src.backend.dynamic_prompt_integration import clear_dynamic_prompt_cache
        
        # Should not raise an exception
        clear_dynamic_prompt_cache()


class TestCreateDynamicPromptManager(unittest.TestCase):
    """Test the create_dynamic_prompt_manager factory function"""
    
    def test_create_with_default_config(self):
        """Test creating manager with default config"""
        base_template = "Test template"
        manager = create_dynamic_prompt_manager(base_template)
        
        self.assertIsInstance(manager, DynamicPromptManager)
        self.assertEqual(manager.base_template, base_template)
        self.assertEqual(manager.config['cache_size'], 100)
    
    def test_create_with_custom_config(self):
        """Test creating manager with custom config"""
        base_template = "Test template"
        config = {'cache_size': 50, 'security_rules': {'test': 'value'}}
        manager = create_dynamic_prompt_manager(base_template, config)
        
        self.assertIsInstance(manager, DynamicPromptManager)
        self.assertEqual(manager.base_template, base_template)
        self.assertEqual(manager.config['cache_size'], 50)
        self.assertEqual(manager.config['security_rules']['test'], 'value')


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)