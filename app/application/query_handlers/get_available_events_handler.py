"""Get Available Events Handler"""

from app.application.queries.get_available_events_query import GetAvailableEventsQuery
from typing import List


class GetAvailableEventsHandler:
    """Handler for GetAvailableEventsQuery"""

    def __init__(self, event_repository):
        self.event_repository = event_repository

    def handle(self, query: GetAvailableEventsQuery) -> List[dict]:
        """
        Handle getting available events
        
        Args:
            query: GetAvailableEventsQuery instance
            
        Returns:
            List of available events
        """
        events = self.event_repository.find_available(
            skip=query.skip,
            limit=query.limit,
            search=query.search,
            start_date=query.start_date,
            end_date=query.end_date,
        )
        
        return [event.to_dict() for event in events]
