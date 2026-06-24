

class GetEventSalesReportQuery:

    def __init__(self, event_id: str):
        self.event_id = event_id


class GetEventParticipantsQuery:

    def __init__(self, event_id: str, page: int = 1, page_size: int = 50):
        self.event_id = event_id
        self.page = page
        self.page_size = page_size
