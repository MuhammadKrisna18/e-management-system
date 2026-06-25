

class GetEventSalesReportQuery:

    def __init__(self, event_id: str):
        self.event_id = event_id


class GetEventParticipantsQuery:

    def __init__(self, event_id: str, page: int = 1, page_size: int = 50):
        self.event_id = event_id
        self.page = page
        self.page_size = page_size

class GetAvailableEventsQuery:
    def __init__(self, date: str = None, location: str = None):
        self.date = date
        self.location = location

class GetEventDetailsQuery:
    def __init__(self, event_id: str):
        self.event_id = event_id
