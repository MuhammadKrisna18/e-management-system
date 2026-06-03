class EventCreated:

    def __init__(self, event_name: str):
        self.event_name = event_name


class EventPublished:

    def __init__(self, event_name: str):
        self.event_name = event_name


class EventCancelled:

    def __init__(self, event_name: str):
        self.event_name = event_name


class TicketCategoryCreated:

    def __init__(self, category_name: str):
        self.category_name = category_name


class TicketCategoryDisabled:

    def __init__(self, category_name: str):
        self.category_name = category_name