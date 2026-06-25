from datetime import datetime


class TicketCheckedIn:
    def __init__(self, ticket_code: str, event_id: str):
        self.ticket_code = ticket_code
        self.event_id = event_id
        self.occurred_at = datetime.now()
