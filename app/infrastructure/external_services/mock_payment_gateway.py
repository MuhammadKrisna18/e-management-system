from typing import Dict, Optional
from app.application.interfaces.payment_gateway import PaymentGateway


class MockPaymentGatewayService(PaymentGateway):

    def __init__(self):
        self._transactions: Dict[str, dict] = {}
        self._transaction_counter = 0

    def charge(self, amount: float) -> str:
        return self.process_payment(amount)

    def process_payment(
        self, amount: float, payment_method: str = "card"
    ) -> str:
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        transaction_id = self._generate_transaction_id()
        self._transactions[transaction_id] = {
            "amount": amount,
            "method": payment_method,
            "status": "success",
        }
        return transaction_id

    def verify_payment(self, transaction_id: str) -> bool:
        if transaction_id not in self._transactions:
            return False
        return self._transactions[transaction_id]["status"] == "success"

    def cancel_payment(self, transaction_id: str) -> bool:
        if transaction_id not in self._transactions:
            return False
        
        self._transactions[transaction_id]["status"] = "cancelled"
        return True

    def _generate_transaction_id(self) -> str:
        self._transaction_counter += 1
        return f"TXN{self._transaction_counter:06d}"
