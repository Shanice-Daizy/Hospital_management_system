"""Small validation helpers used by the outpatient system."""

from datetime import date, datetime


def validate_non_empty_text(value, field_name):
    """Return trimmed text, or raise ValueError when it is blank."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be blank.")
    return value.strip()
