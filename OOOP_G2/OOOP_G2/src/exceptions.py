class HospitalError(Exception):
    """Base exception for domain-specific hospital system errors."""


class ValidationError(HospitalError):
    """Raised when user-supplied data fails validation."""


class RecordNotFoundError(HospitalError):
    """Raised when a requested patient, worker, or consultation is missing."""


class InvalidOperationError(HospitalError):
    """Raised when an operation is not valid for the current object state."""
