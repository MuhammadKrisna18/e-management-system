"""Get Participant List Query"""

from typing import Optional


class GetParticipantListQuery:
    """Query to get participant list"""

    def __init__(
        self,
        event_id: str,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
    ):
        self.event_id = event_id
        self.skip = skip
        self.limit = limit
        self.search = search
