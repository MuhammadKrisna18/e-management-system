class TicketCategory:
    def __init__(self, name: str, price: float, quota: int):
        if price < 0:
            raise ValueError("Price cannot be negative")

        if quota <= 0:
            raise ValueError("Quota must be greater than 0")

        self.name = name
        self.price = price
        self.quota = quota
        self.is_active = True
        
    def disable(self):
        self.is_active = False