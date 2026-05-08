"""Check-in Ticket Command"""

from datetime import datetime


class CheckinTicketCommand:
    """Command to check in a ticket"""

    def __init__(self, ticket_id: str, location: str, checked_in_at: datetime):
        self.ticket_id = ticket_id
        self.location = location
        self.checked_in_at = checked_in_at
