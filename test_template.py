#!/usr/bin/env python3

import sys
sys.path.append('src/backend')

from dynamic_prompts import TemplateEngine

# Test the template engine
engine = TemplateEngine()
base_template = """Quick Response Needed: You are a financial analyst.

{verbosity_instruction}
{tool_restriction}
{format_instruction}
{style_instruction}

Provide financial analysis."""

preferences = {"verbosity": "verbose"}
context = {}

print("Base template:")
print(base_template)
print("\n" + "="*50 + "\n")

result = engine.apply_preferences(base_template, preferences, context)
print("Result after applying preferences:")
print(result)
print("\n" + "="*50 + "\n")

print("Template variables found:")
print(f"verbosity_instruction in template: {'{verbosity_instruction}' in base_template}")
print(f"tool_restriction in template: {'{tool_restriction}' in base_template}")
print(f"format_instruction in template: {'{format_instruction}' in base_template}")
print(f"style_instruction in template: {'{style_instruction}' in base_template}")