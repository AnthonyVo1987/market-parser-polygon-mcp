import re

# Test the regex pattern
test_string = "verbose<script>"
print(f"Input: {test_string}")
print(f"Input repr: {repr(test_string)}")

# Test with correct pattern
pattern = r'[<>"\']+'
result = re.sub(pattern, '', test_string)
print(f"Pattern: {pattern}")
print(f"Result: {result}")
print(f"Result repr: {repr(result)}")

# Test individual characters
print("\nTesting individual characters:")
print(f"< in string: {'<' in test_string}")
print(f"> in string: {'>' in test_string}")
print(f"< removed: {test_string.replace('<', '')}")
print(f"> removed: {test_string.replace('>', '')}")
print(f"Both removed: {test_string.replace('<', '').replace('>', '')}")