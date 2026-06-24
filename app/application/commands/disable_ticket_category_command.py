class DisableTicketCategoryCommand:
    def __init__(self, event_id: str, category_name: str):
        self.event_id = event_id
        self.category_name = category_name
