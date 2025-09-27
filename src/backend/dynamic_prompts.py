"""
Dynamic Adaptive Prompting System for Financial Analysis

This module provides a comprehensive dynamic prompting system that allows users to customize
AI interactions without requiring code changes. The system replaces rigid prompt structures
with flexible, user-customizable approaches while maintaining core financial analysis functionality.

Features:
- Dynamic prompt generation with user customization
- Instruction parsing from user input
- Template engine with variable substitution
- Input validation and security
- Performance optimization with caching
- Fallback mechanisms for error handling

Author: AI Assistant
Date: September 26, 2025
"""

import logging
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""


class TemplateError(Exception):
    """Custom exception for template processing errors"""


@dataclass
class UserPreferences:
    """Data class for user preferences extracted from input"""

    verbosity: Optional[str] = None
    tool_usage: Optional[str] = None
    output_format: Optional[str] = None
    response_style: Optional[str] = None


class DynamicPromptManager:
    """
    Main class for dynamic prompt generation and customization.

    This class manages the entire dynamic prompting workflow including:
    - User instruction parsing
    - Preference validation
    - Template customization
    - Performance caching
    - Error handling and fallbacks
    """

    def __init__(self, base_template: str, config: Dict[str, Any]):
        self.base_template = base_template
        self.config = config
        self.instruction_parser = InstructionParser()
        self.template_engine = TemplateEngine()
        self.cache = PromptCache(max_size=config.get("cache_size", 100))
        self.validator = InputValidator(config.get("security_rules", {}))
        self.logger = logging.getLogger(__name__)

    def generate_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        """
        Generate a customized prompt based on user input and preferences.

        Args:
            user_input: The user's input message
            context: Additional context for prompt generation

        Returns:
            Customized prompt string
        """
        try:
            # Parse user instructions
            preferences = self.parse_user_instructions(user_input)

            # Validate preferences
            self.validator.validate_preferences(preferences)

            # Apply customizations to template
            customized_prompt = self.template_engine.apply_preferences(
                self.base_template, preferences, context
            )

            # Cache result for performance
            self.cache.store(user_input, customized_prompt)

            return customized_prompt
        except ValidationError as e:
            return self._handle_validation_error(e, user_input)
        except TemplateError as e:
            return self._handle_template_error(e, user_input)
        except Exception as e:
            return self._handle_general_error(e, user_input)

    def parse_user_instructions(self, user_input: str) -> UserPreferences:
        """
        Extract and validate user preferences from input text.

        Args:
            user_input: The user's input message

        Returns:
            UserPreferences object with extracted preferences
        """
        # Extract and validate user preferences
        raw_preferences = self.instruction_parser.extract_preferences(user_input)
        return self.validator.sanitize_preferences(raw_preferences)

    def _handle_validation_error(self, error: ValidationError, user_input: str) -> str:
        """Handle validation errors with logging and fallback"""
        self.logger.warning(f"Validation error for input: {user_input[:50]}... Error: {error}")
        return self._get_fallback_prompt()

    def _handle_template_error(self, error: TemplateError, user_input: str) -> str:
        """Handle template errors with logging and fallback"""
        self.logger.error(f"Template error for input: {user_input[:50]}... Error: {error}")
        return self._get_fallback_prompt()

    def _handle_general_error(self, error: Exception, user_input: str) -> str:
        """Handle general errors with logging and fallback"""
        self.logger.error(f"Unexpected error for input: {user_input[:50]}... Error: {error}")
        return self._get_fallback_prompt()

    def _get_fallback_prompt(self) -> str:
        """Return base template without customizations as fallback"""
        return self.base_template


class InstructionParser:
    """
    Parses user instructions from input text using regex patterns.

    This class extracts user preferences for verbosity, tool usage,
    output format, and response style from natural language input.
    """

    def __init__(self):
        self.patterns = {
            "verbosity": r"\[(verbose|minimal|standard|detailed|brief|concise)\]",
            "tool_usage": r"\[(use only|avoid|minimal tools?)(?:\s+([a-zA-Z_\s,]+))?\]",
            "output_format": r"\[(structured|narrative|bullet points?|JSON|markdown|plain)\]",
            "response_style": r"\[(formal|casual|technical|professional|friendly)\]",
        }

    def extract_preferences(self, user_input: str) -> Dict[str, Any]:
        """
        Extract user preferences from input text using regex patterns.

        Args:
            user_input: The user's input message

        Returns:
            Dictionary of extracted preferences
        """
        preferences = {}
        for key, pattern in self.patterns.items():
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    # For tool_usage, preserve the full instruction for template processing
                    if key == "tool_usage":
                        # Reconstruct the full instruction from the original input
                        full_match = matches[0]
                        if len(full_match) > 1 and full_match[1]:
                            preferences[key] = f"{full_match[0]} {full_match[1]}"
                        else:
                            preferences[key] = full_match[0]
                    else:
                        preferences[key] = (
                            matches[0][1]
                            if len(matches[0]) > 1 and matches[0][1]
                            else matches[0][0]
                        )
                else:
                    preferences[key] = matches[0]
        return preferences


class TemplateEngine:
    """
    Applies user preferences to prompt templates using variable substitution.

    This class handles the customization of prompt templates based on
    user preferences for verbosity, tool usage, output format, and style.
    """

    def __init__(self):
        self.template_vars = {
            "verbosity": self._get_verbosity_template,
            "tool_usage": self._get_tool_usage_template,
            "output_format": self._get_output_format_template,
            "response_style": self._get_response_style_template,
        }

    def apply_preferences(
        self, base_template: str, preferences: Any, context: Dict[str, Any]
    ) -> str:
        """
        Apply user preferences to the base template.

        Args:
            base_template: The base prompt template
            preferences: User preferences to apply (UserPreferences object or dict)
            context: Additional context for template processing

        Returns:
            Customized prompt template
        """
        template = base_template

        # Handle both UserPreferences object and dict
        if isinstance(preferences, dict):
            # Apply verbosity customization
            if preferences.get("verbosity"):
                template = self.template_vars["verbosity"](
                    template, preferences["verbosity"], context
                )

            # Apply tool usage customization
            if preferences.get("tool_usage"):
                template = self.template_vars["tool_usage"](
                    template, preferences["tool_usage"], context
                )

            # Apply output format customization
            if preferences.get("output_format"):
                template = self.template_vars["output_format"](
                    template, preferences["output_format"], context
                )

            # Apply response style customization
            if preferences.get("response_style"):
                template = self.template_vars["response_style"](
                    template, preferences["response_style"], context
                )
        else:
            # Apply verbosity customization
            if preferences.verbosity:
                template = self.template_vars["verbosity"](template, preferences.verbosity, context)

            # Apply tool usage customization
            if preferences.tool_usage:
                template = self.template_vars["tool_usage"](
                    template, preferences.tool_usage, context
                )

            # Apply output format customization
            if preferences.output_format:
                template = self.template_vars["output_format"](
                    template, preferences.output_format, context
                )

            # Apply response style customization
            if preferences.response_style:
                template = self.template_vars["response_style"](
                    template, preferences.response_style, context
                )

        return template

    def _get_verbosity_template(
        self, template: str, verbosity: str, _context: Dict[str, Any]
    ) -> str:
        """Apply verbosity customization to template"""
        verbosity_instructions = {
            "minimal": "Provide only essential information with minimal explanation.",
            "standard": "Provide balanced information with moderate detail.",
            "verbose": "Provide comprehensive information with detailed explanations.",
            "detailed": "Provide thorough analysis with extensive detail.",
            "brief": "Provide concise information with brief explanations.",
            "concise": "Provide essential information in the most concise format possible.",
        }
        instruction = verbosity_instructions.get(verbosity, verbosity_instructions["standard"])
        return template.replace("{verbosity_instruction}", instruction)

    def _get_tool_usage_template(
        self, template: str, tool_usage: str, _context: Dict[str, Any]
    ) -> str:
        """Apply tool usage customization to template"""
        if "use only" in tool_usage.lower():
            tools = tool_usage.lower().replace("use only", "").strip()
            return template.replace("{tool_restriction}", f"Use only the following tools: {tools}")
        elif "avoid" in tool_usage.lower():
            tools = tool_usage.lower().replace("avoid", "").strip()
            return template.replace(
                "{tool_restriction}", f"Avoid using the following tools: {tools}"
            )
        elif "minimal" in tool_usage.lower():
            return template.replace(
                "{tool_restriction}",
                "Use the minimum number of tools necessary to complete the task",
            )
        return template

    def _get_output_format_template(
        self, template: str, output_format: str, _context: Dict[str, Any]
    ) -> str:
        """Apply output format customization to template"""
        format_instructions = {
            "structured": "Format your response in a structured format with clear sections and bullet points.",
            "narrative": "Format your response as a flowing narrative with clear paragraphs.",
            "bullet points": "Format your response using bullet points for easy reading.",
            "json": "Format your response as valid JSON when appropriate.",
            "markdown": "Format your response using Markdown formatting.",
            "plain": "Format your response in plain text without special formatting.",
        }
        instruction = format_instructions.get(output_format, format_instructions["structured"])
        return template.replace("{format_instruction}", instruction)

    def _get_response_style_template(
        self, template: str, response_style: str, _context: Dict[str, Any]
    ) -> str:
        """Apply response style customization to template"""
        style_instructions = {
            "formal": "Use a formal, professional tone in your response.",
            "casual": "Use a casual, friendly tone in your response.",
            "technical": "Use a technical, precise tone with appropriate terminology.",
            "professional": "Use a professional, business-appropriate tone.",
            "friendly": "Use a warm, approachable tone in your response.",
        }
        instruction = style_instructions.get(response_style, style_instructions["professional"])
        return template.replace("{style_instruction}", instruction)


class InputValidator:
    """
    Validates and sanitizes user input for security and correctness.

    This class ensures that user instructions are safe, valid, and within
    acceptable parameters to prevent prompt injection and other security issues.
    """

    def __init__(self, security_rules: Dict[str, Any]):
        self.security_rules = security_rules
        self.allowed_verbs = ["verbose", "minimal", "standard", "detailed", "brief", "concise"]
        self.allowed_tools = [
            "get_snapshot_ticker",
            "get_market_status",
            "get_full_market_snapshot",
            "get_support_resistance_levels",
            "get_technical_analysis",
        ]
        self.allowed_formats = [
            "structured",
            "narrative",
            "bullet points",
            "json",
            "markdown",
            "plain",
        ]
        self.allowed_styles = ["formal", "casual", "technical", "professional", "friendly"]

    def validate_preferences(self, preferences: Any) -> None:
        """
        Validate user preferences against allowed values.

        Args:
            preferences: User preferences to validate (dict or UserPreferences object)

        Raises:
            ValidationError: If preferences contain invalid values
        """
        # Handle both dict and UserPreferences object
        if isinstance(preferences, dict):
            items = list(preferences.items())
        else:
            # UserPreferences object
            items = [
                (key, getattr(preferences, key))
                for key in ["verbosity", "tool_usage", "output_format", "response_style"]
                if hasattr(preferences, key)
            ]

        for key, value in items:
            if value is None:
                continue  # Skip None values
            if key == "verbosity" and value not in self.allowed_verbs:
                raise ValidationError(f"Invalid verbosity level: {value}")
            elif key == "tool_usage" and not self._validate_tool_usage(value):
                raise ValidationError(f"Invalid tool usage instruction: {value}")
            elif key == "output_format" and value not in self.allowed_formats:
                raise ValidationError(f"Invalid output format: {value}")
            elif key == "response_style" and value not in self.allowed_styles:
                raise ValidationError(f"Invalid response style: {value}")

    def _validate_tool_usage(self, tool_usage: str) -> bool:
        """Validate tool usage instructions"""
        if not tool_usage:
            return True

        tool_usage_lower = tool_usage.lower()
        if "use only" in tool_usage_lower:
            tools = tool_usage_lower.replace("use only", "").strip().split(",")
            return all(tool.strip() in self.allowed_tools for tool in tools)
        elif "avoid" in tool_usage_lower:
            tools = tool_usage_lower.replace("avoid", "").strip().split(",")
            return all(tool.strip() in self.allowed_tools for tool in tools)
        return True

    def sanitize_preferences(self, preferences: Dict[str, Any]) -> UserPreferences:
        """
        Sanitize user preferences by removing dangerous characters.

        Args:
            preferences: Raw preferences to sanitize

        Returns:
            Sanitized UserPreferences object
        """
        sanitized = UserPreferences()
        for key, value in preferences.items():
            if isinstance(value, str):
                # Remove potentially dangerous characters
                sanitized_value = re.sub(r'[<>"\']+', "", value).strip()
                setattr(sanitized, key, sanitized_value)
            else:
                setattr(sanitized, key, value)
        return sanitized


class PromptCache:
    """
    Caches generated prompts for performance optimization.

    This class implements an LRU cache for storing frequently used
    prompt configurations to improve response times.
    """

    def __init__(self, max_size: int = 100):
        self.cache: Dict[str, str] = {}
        self.max_size = max_size
        self.access_times: Dict[str, float] = {}

    def store(self, key: str, value: str) -> None:
        """
        Store a prompt in the cache.

        Args:
            key: Cache key (usually user input)
            value: Generated prompt to cache
        """
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = value
        self.access_times[key] = time.time()

    def get(self, key: str) -> Optional[str]:
        """
        Retrieve a prompt from the cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached prompt or None if not found
        """
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None

    def _evict_oldest(self) -> None:
        """Evict the least recently used item from cache"""
        if self.access_times:
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]


def create_dynamic_prompt_manager(
    base_template: str, config: Optional[Dict[str, Any]] = None
) -> DynamicPromptManager:
    """
    Factory function to create a DynamicPromptManager instance.

    Args:
        base_template: The base prompt template
        config: Configuration options for the manager

    Returns:
        Configured DynamicPromptManager instance
    """
    if config is None:
        config = {"cache_size": 100, "security_rules": {"max_input_length": 1000, "rate_limit": 10}}

    return DynamicPromptManager(base_template, config)
