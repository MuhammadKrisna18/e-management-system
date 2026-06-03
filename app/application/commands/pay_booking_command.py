class PayBookingCommand:

    def __init__(
        self,
        booking_id,
        amount
    ):
        self.booking_id = booking_id
        self.amount = amount