
class CheckInTicketCommand:
    
    def __init__(self, ticket_code: str, event_id: str):
        self.ticket_code = ticket_code
        self.event_id = event_id
