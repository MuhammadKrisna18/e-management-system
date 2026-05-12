from app.domain.value_objects.money import Money


class PricingService:

    @staticmethod
    def calculate_total_price(ticket_price: float, quantity: int, service_fee: float = 0):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        subtotal = ticket_price * quantity
        total = subtotal + service_fee

        return Money(total)