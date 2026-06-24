

class DomainException(Exception):
    
    pass


class RefundException(DomainException):
    
    pass


class RefundNotFoundException(RefundException):
    
    pass


class InvalidRefundStatusException(RefundException):
    
    pass


class RefundDeadlinePassedException(RefundException):
    
    pass


class BookingException(DomainException):
    
    pass


class BookingNotFoundException(BookingException):
    
    pass


class InvalidBookingStatusException(BookingException):
    
    pass


class BookingPaymentDeadlinePassedException(BookingException):
    
    pass


class TicketException(DomainException):
    
    pass


class InvalidTicketStatusException(TicketException):
    
    pass


class TicketAlreadyCheckedException(TicketException):
    
    pass


class EventException(DomainException):
    
    pass


class EventNotFoundException(EventException):
    
    pass


class InvalidEventStatusException(EventException):
    
    pass


class EventPublishException(EventException):
    
    pass


class ValidationException(DomainException):
    
    pass
