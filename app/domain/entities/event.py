from datetime import datetime


class Event:
    def __init__(self, name: str, start_date: datetime, end_date: datetime, capacity: int):
        if end_date < start_date:
            raise ValueError("End date cannot be earlier than start date")

        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")

        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.capacity = capacity
        self.status = "Draft"  # default rule