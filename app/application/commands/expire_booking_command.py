"""Expire Booking Command"""


class ExpireBookingCommand:
    """Command to expire a booking"""

    def __init__(self, booking_id: str):
        self.booking_id = booking_id
