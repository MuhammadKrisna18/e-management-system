"""Get Event Detail Handler"""

from app.application.queries.get_event_detail_query import GetEventDetailQuery


class GetEventDetailHandler:
    """Handler for GetEventDetailQuery"""

    def __init__(self, event_repository):
        self.event_repository = event_repository

    def handle(self, query: GetEventDetailQuery) -> dict:
        """
        Handle getting event details
        
        Args:
            query: GetEventDetailQuery instance
            
        Returns:
            Event details
        """
        event = self.event_repository.get_by_id(query.event_id)
        return event.to_dict() if event else None
