class RequestRefundCommand:
    """
    Command to request a refund for a booking.
    
    Used for User Story 15: Request Refund
    """

    def __init__(self, booking_id: str):
        """
        Initialize RequestRefundCommand.
        
        Args:
            booking_id: ID of the booking to refund
        """
        self.booking_id = booking_id