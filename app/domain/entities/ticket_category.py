from datetime import datetime


class TicketCategory:
    def __init__(
        self,
        name: str,
        price: float,
        quota: int,
        sales_start_date: datetime,
        sales_end_date: datetime,
        event_start_date: datetime
    ):
        if price < 0:
            raise ValueError("Price cannot be negative")

        if quota <= 0:
            raise ValueError("Quota must be greater than 0")

        if sales_end_date < sales_start_date:
            raise ValueError("Sales end date cannot be earlier than sales start date")

        if sales_end_date > event_start_date:
            raise ValueError(
                "Ticket sales period must end before or at event start date"
            )

        self.name = name
        self.price = price
        self.quota = quota
        self.sales_start_date = sales_start_date
        self.sales_end_date = sales_end_date

        self.is_active = True

    def disable(self):
        self.is_active = False