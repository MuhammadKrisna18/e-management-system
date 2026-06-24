

class TimeConstants:
    
    PAYMENT_DEADLINE_MINUTES = 15
    """Minutes to complete payment after booking creation."""
    
    REFUND_REQUEST_DEADLINE_DAYS = 7
    """Days after event to request refund."""
    
    SALES_END_BEFORE_EVENT_HOURS = 0
    """Hours before event start when ticket sales must end."""


class ErrorMessages:
    
    # Refund Errors
    REFUND_NOT_FOUND = "Refund {refund_id} not found"
    REFUND_MUST_BE_REQUESTED = "Refund must be in Requested status"
    REFUND_MUST_BE_APPROVED = "Refund must be in Approved status"
    REFUND_DEADLINE_PASSED = "Refund request deadline has passed"
    
    # Booking Errors
    BOOKING_NOT_FOUND = "Booking {booking_id} not found"
    BOOKING_MUST_BE_PAID = "Booking must be Paid for refund"
    BOOKING_PAYMENT_DEADLINE_PASSED = "Payment deadline has passed"
    BOOKING_INVALID_QUANTITY = "Quantity must be greater than 0"
    
    # Ticket Errors
    TICKET_ALREADY_CHECKED_IN = "Ticket already checked in"
    TICKET_CANNOT_CHECK_IN_CANCELLED = "Cancelled ticket cannot check in"
    TICKET_CHECKED_IN_REFUND_INVALID = "Refund cannot be requested if ticket has already been checked in"
    
    # Event Errors
    EVENT_NOT_FOUND = "Event {event_id} not found"
    EVENT_MUST_HAVE_ACTIVE_CATEGORIES = "Cannot publish event without active ticket category"
    EVENT_CANCELLED_CANNOT_PUBLISH = "Cancelled event cannot be published"
    
    # Validation Errors
    REJECTION_REASON_REQUIRED = "Rejection reason must be provided"
    PAYMENT_REFERENCE_REQUIRED = "Payment reference must be recorded"
    INVALID_AMOUNT = "Amount must be positive"
    INVALID_ACCOUNT_NUMBER = "Account number required"


class ValidationMessages:
    
    QUANTITY_TOO_HIGH = "Quantity must not exceed remaining ticket quota"
    QUOTA_EXCEEDS_CAPACITY = "Total quota exceeds event capacity"
    PRICE_CANNOT_BE_NEGATIVE = "Ticket price cannot be less than zero"
    CAPACITY_MUST_BE_POSITIVE = "Capacity must be greater than zero"
    END_DATE_BEFORE_START = "Event end date cannot be earlier than start date"
    TICKET_CODE_INVALID = "Invalid ticket code format"


class EventStatus:
    
    DRAFT = "Draft"
    PUBLISHED = "Published"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class BookingStatuses:
    
    PENDING_PAYMENT = "PendingPayment"
    PAID = "Paid"
    EXPIRED = "Expired"
    REFUNDED = "Refunded"


class RefundStatuses:
    
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID_OUT = "PaidOut"


class TicketStatuses:
    
    ACTIVE = "Active"
    CHECKED_IN = "CheckedIn"
    CANCELLED = "Cancelled"


class TicketCategoryStatus:
    
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class ServiceFee:
    
    PERCENTAGE = 0.05
    """Percentage-based service fee (5% default)."""
    
    MINIMUM = 10000.0
    """Minimum service fee (Rp 10,000)."""
