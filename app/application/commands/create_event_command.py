class CreateEventCommand:

    def __init__(
        self,
        name,
        start_date,
        end_date,
        capacity
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.capacity = capacity