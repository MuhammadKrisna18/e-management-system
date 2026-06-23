from datetime import datetime


class CreateTicketCategoryCommand:
    def __init__(
        self,
        event_id: str,
        name: str,
        price: float,
        quota: int,
        sales_start_date: datetime,
        sales_end_date: datetime
    ):
        self.event_id = event_id
        self.name = name
        self.price = price
        self.quota = quota
        self.sales_start_date = sales_start_date
        self.sales_end_date = sales_end_date
