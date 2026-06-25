from datetime import datetime
from app.domain.value_objects.refund_status import RefundStatus
from app.domain.value_objects.money import Money


class Refund:

    def __init__(
        self,
        refund_id: str,
        booking_id: str,
        customer_id: str,
        event_id: str,
        refund_amount: Money,
        refund_deadline: datetime,
        reason: str,
    ):
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.event_id = event_id
        self.refund_amount = refund_amount
        self.refund_deadline = refund_deadline
        self.reason = reason
        
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
        if check_date is None:
            check_date = datetime.now()
        return check_date > self.refund_deadline