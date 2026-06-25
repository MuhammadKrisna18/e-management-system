class RequestRefundCommand:

    def __init__(self, booking_id: str, reason: str):
        self.booking_id = booking_id
        self.reason = reason