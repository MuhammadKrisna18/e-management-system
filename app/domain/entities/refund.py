"""Refund Entity"""
from datetime import datetime
from app.domain.value_objects.refund_status import RefundStatus
from app.domain.value_objects.money import Money


class Refund:
    """
    Entity representing a refund request.
    
    A refund is created when a customer requests a refund for their booking.
    The refund goes through a lifecycle: Requested -> Approved/Rejected -> PaidOut
    """

    def __init__(
        self,
        refund_id: str,
        booking_id: str,
        customer_id: str,
        event_id: str,
        refund_amount: Money,
        refund_deadline: datetime,
    ):
        """
        Initialize refund entity.
        
        Args:
            refund_id: Unique refund identifier
            booking_id: Associated booking ID
            customer_id: Customer requesting refund
            event_id: Event associated with booking
            refund_amount: Amount to be refunded (Money value object)
            refund_deadline: Deadline to request refund
        """
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.event_id = event_id
        self.refund_amount = refund_amount
        self.refund_deadline = refund_deadline
        
        # State management
        self.status = RefundStatus.REQUESTED
        self.created_at = datetime.now()
        self.approved_at = None
        self.rejected_at = None
        self.paid_out_at = None
        
        # Additional information
        self.rejection_reason = None
        self.payment_reference = None
    
    def is_expired(self, check_date: datetime = None) -> bool:
        """
        Check if refund request deadline has expired.
        
        Args:
            check_date: Date to check against (default: now)
            
        Returns:
            bool: True if refund deadline has passed
        """
        if check_date is None:
            check_date = datetime.now()
        return check_date > self.refund_deadline