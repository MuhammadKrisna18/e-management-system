"""Get Purchased Tickets Handler"""

from app.application.queries.get_purchased_tickets_query import GetPurchasedTicketsQuery
from typing import List


class GetPurchasedTicketsHandler:
    """Handler for GetPurchasedTicketsQuery"""

    def __init__(self, booking_repository):
        self.booking_repository = booking_repository

    def handle(self, query: GetPurchasedTicketsQuery) -> List[dict]:
        """
        Handle getting purchased tickets
        
        Args:
            query: GetPurchasedTicketsQuery instance
            
        Returns:
            List of purchased tickets
        """
        bookings = self.booking_repository.find_by_user(
            user_id=query.user_id,
            skip=query.skip,
            limit=query.limit,
            status=query.status,
        )
        
        return [booking.to_dict() for booking in bookings]
