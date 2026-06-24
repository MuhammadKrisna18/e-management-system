class DisableTicketCategoryHandler:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        event_aggregate = self.repository.get_by_id(command.event_id)
        if not event_aggregate:
            raise ValueError(f"Event {command.event_id} not found")

        event_aggregate.disable_ticket_category(command.category_name)
        
        self.repository.save(event_aggregate)
        return event_aggregate
