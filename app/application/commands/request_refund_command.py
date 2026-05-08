"""Request Refund Command"""

from decimal import Decimal


class RequestRefundCommand:
    """Command to request a refund"""

    def __init__(
        self,
        booking_id: str,
        amount: Decimal,
        reason: str,
    ):
        self.booking_id = booking_id
        self.amount = amount
        self.reason = reason
