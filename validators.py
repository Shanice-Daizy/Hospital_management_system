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


def validate_positive_number(value, field_name):
    """Return a positive number as a float."""
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a number greater than zero.")
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{field_name} must be a number greater than zero."
        ) from error
    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")
    return number


def _validate_date(value, field_name):
    """Return a date object from a date or YYYY-MM-DD text."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError as error:
            raise ValueError(
                f"{field_name} must use the YYYY-MM-DD format."
            ) from error
    raise ValueError(f"{field_name} must be a valid date.")


def validate_date_of_birth(value):
    """Validate a date of birth and reject future dates."""
    birth_date = _validate_date(value, "Date of birth")
    if birth_date > date.today():
        raise ValueError("Date of birth cannot be in the future.")
    return birth_date
