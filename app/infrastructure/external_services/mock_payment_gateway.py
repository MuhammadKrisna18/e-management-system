import uuid
from app.application.interfaces.payment_gateway import PaymentGateway


class MockPaymentGateway(PaymentGateway):
    """Mock payment gateway for testing — always succeeds."""

    def charge(self, amount) -> str:
        txn_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        print(f"[MockPaymentGateway] Charged {amount}. Transaction ID: {txn_id}")
        return txn_id


# Alias used by container
MockPaymentGatewayService = MockPaymentGateway
