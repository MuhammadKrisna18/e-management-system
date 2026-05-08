"""Get Booking Detail Handler"""

from app.application.queries.get_booking_detail_query import GetBookingDetailQuery


class GetBookingDetailHandler:
    """Handler for GetBookingDetailQuery"""

    def __init__(self, booking_repository):
        self.booking_repository = booking_repository

    def handle(self, query: GetBookingDetailQuery) -> dict:
        """
        Handle getting booking details
        
        Args:
            query: GetBookingDetailQuery instance
            
        Returns:
            Booking details
        """
        booking = self.booking_repository.get_by_id(query.booking_id)
        return booking.to_dict() if booking else None
