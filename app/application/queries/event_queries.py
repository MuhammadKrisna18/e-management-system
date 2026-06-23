"""Event Query Definitions"""


class GetEventSalesReportQuery:
    """
    Query to get sales report for an event.
    
    Used for User Story 19: View Event Sales Report
    """

    def __init__(self, event_id: str):
        """
        Initialize GetEventSalesReportQuery.
        
        Args:
            event_id: ID of the event
        """
        self.event_id = event_id


class GetEventParticipantsQuery:
    """
    Query to get participant list for an event.
    
    Used for User Story 20: View Event Participants
    """

    def __init__(self, event_id: str, page: int = 1, page_size: int = 50):
        """
        Initialize GetEventParticipantsQuery.
        
        Args:
            event_id: ID of the event
            page: Page number for pagination
            page_size: Number of participants per page
        """
        self.event_id = event_id
        self.page = page
        self.page_size = page_size
