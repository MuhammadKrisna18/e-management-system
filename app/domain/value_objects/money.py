class Money:
    def __init__(self, amount: float):
        if amount < 0:
            raise ValueError("Money cannot be negative")

        self.amount = amount

    def add(self, other):
        return Money(self.amount + other.amount)