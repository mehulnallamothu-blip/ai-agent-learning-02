"""Return the current local date and time as text."""

from datetime import datetime


def get_current_datetime() -> str:
    """Return the current date and time in a readable local format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
