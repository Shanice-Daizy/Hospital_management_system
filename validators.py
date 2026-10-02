"""Small validation helpers used by the outpatient system."""

from datetime import date, datetime


def validate_non_empty_text(value, field_name):
    """Return trimmed text, or raise ValueError when it is blank."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be blank.")
    return value.strip()


def validate_name(value, field_name):
    """Validate a person's name."""
    return validate_non_empty_text(value, field_name)


def validate_phone(value):
    """Validate and trim a phone number."""
    return validate_non_empty_text(value, "Phone")
