"""Pay Booking Command"""

from decimal import Decimal


class PayBookingCommand:
    """Command to pay for a booking"""

    def __init__(
        self,
        booking_id: str,
        amount: Decimal,
        payment_method: str,
        payment_reference: str,
    ):
        self.booking_id = booking_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_reference = payment_reference
