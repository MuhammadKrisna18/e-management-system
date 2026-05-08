"""Get Participant List Handler"""

from app.application.queries.get_participant_list_query import GetParticipantListQuery
from typing import List


class GetParticipantListHandler:
    """Handler for GetParticipantListQuery"""

    def __init__(self, booking_repository):
        self.booking_repository = booking_repository

    def handle(self, query: GetParticipantListQuery) -> List[dict]:
        """
        Handle getting participant list
        
        Args:
            query: GetParticipantListQuery instance
            
        Returns:
            List of participants
        """
        participants = self.booking_repository.find_participants(
            event_id=query.event_id,
            skip=query.skip,
            limit=query.limit,
            search=query.search,
        )
        
        return [participant.to_dict() for participant in participants]
