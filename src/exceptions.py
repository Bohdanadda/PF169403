"""Common exceptions for the cinema system."""


class ValidationError(Exception):
    """Raised when validation of input data fails."""
    pass


class ReservationError(Exception):
    """Raised when a reservation operation fails."""
    pass


class ScheduleConflictError(Exception):
    """Raised when there is a conflict in screening schedule."""
    pass


class PaymentError(Exception):
    """Raised when a payment operation fails."""
    pass
