"""
Domain Exceptions

Custom exception classes for domain layer.
Provides specific error types for business rule violations.
"""


class DomainException(Exception):
    """Base exception for all domain layer errors."""
    
    pass


class RefundException(DomainException):
    """Base exception for refund-related errors."""
    
    pass


class RefundNotFoundException(RefundException):
    """Raised when refund record is not found."""
    
    pass


class InvalidRefundStatusException(RefundException):
    """Raised when refund status doesn't allow the operation."""
    
    pass


class RefundDeadlinePassedException(RefundException):
    """Raised when refund request deadline has passed."""
    
    pass


class BookingException(DomainException):
    """Base exception for booking-related errors."""
    
    pass


class BookingNotFoundException(BookingException):
    """Raised when booking record is not found."""
    
    pass


class InvalidBookingStatusException(BookingException):
    """Raised when booking status doesn't allow the operation."""
    
    pass


class BookingPaymentDeadlinePassedException(BookingException):
    """Raised when payment deadline has passed."""
    
    pass


class TicketException(DomainException):
    """Base exception for ticket-related errors."""
    
    pass


class InvalidTicketStatusException(TicketException):
    """Raised when ticket status doesn't allow the operation."""
    
    pass


class TicketAlreadyCheckedException(TicketException):
    """Raised when trying to check in already checked-in ticket."""
    
    pass


class EventException(DomainException):
    """Base exception for event-related errors."""
    
    pass


class EventNotFoundException(EventException):
    """Raised when event record is not found."""
    
    pass


class InvalidEventStatusException(EventException):
    """Raised when event status doesn't allow the operation."""
    
    pass


class EventPublishException(EventException):
    """Raised when event cannot be published."""
    
    pass


class ValidationException(DomainException):
    """Raised when domain validation fails."""
    
    pass
