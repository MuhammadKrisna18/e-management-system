from app.application.interfaces.payment_gateway import PaymentGatewayInterface
from app.domain.value_objects.money import Money

class MockPaymentGateway(PaymentGatewayInterface):
    def process_payment(self, booking_id: str, amount: Money) -> bool:
        # Simulate payment processing
        print(f"[MockPaymentGateway] Processing payment for Booking {booking_id} of amount {amount.amount}")
        return True
