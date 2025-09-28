"""DateTime utilities for the Market Parser application."""

from datetime import datetime


def get_current_datetime_context():
    """Generate current date/time context for AI agent prompts."""
    now = datetime.now()
    return f"""
CURRENT DATE AND TIME CONTEXT:
- Today's date: {now.strftime('%A, %B %d, %Y')}
- Current time: {now.strftime('%I:%M %p %Z')}
- ISO format: {now.strftime('%Y-%m-%d %H:%M:%S')}
- Market status: {'Open' if now.weekday() < 5 and 9 <= now.hour < 16 else 'Closed'}

IMPORTANT: Always use the current date and time above for all financial analysis.
Do NOT use training data cutoff dates or outdated information.
"""