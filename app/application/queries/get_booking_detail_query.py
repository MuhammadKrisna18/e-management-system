"""Get Booking Detail Query"""


class GetBookingDetailQuery:
    """Query to get booking details"""

    def __init__(self, booking_id: str):
        self.booking_id = booking_id
