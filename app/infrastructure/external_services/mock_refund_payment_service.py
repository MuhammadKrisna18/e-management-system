from typing import Dict
from app.application.interfaces.refund_payment_service import RefundPaymentService


class MockRefundPaymentService(RefundPaymentService):

    def __init__(self):
        self._refund_transactions: Dict[str, dict] = {}
        self._transaction_counter = 0

    def transfer(self, amount: float):
        # Just process dummy refund
        self.process_refund("dummy_account", amount, "dummy_ref")

    def process_refund(
        self, 
        account_number: str, 
        refund_amount: float, 
        reference_id: str
    ) -> str:
        if not account_number:
            raise ValueError("Account number required")
        
        if refund_amount <= 0:
            raise ValueError("Refund amount must be positive")

        transaction_id = self._generate_transaction_id()
        self._refund_transactions[transaction_id] = {
            "account": account_number,
            "amount": refund_amount,
            "reference": reference_id,
            "status": "processed",
        }
        return transaction_id

    def verify_refund_status(self, transaction_id: str) -> str:
        if transaction_id not in self._refund_transactions:
            return "failed"
        
        return self._refund_transactions[transaction_id]["status"]

    def cancel_refund(self, transaction_id: str) -> bool:
        if transaction_id not in self._refund_transactions:
            return False
        
        transaction = self._refund_transactions[transaction_id]
        if transaction["status"] == "pending":
            transaction["status"] = "cancelled"
            return True
        
        return False

    def _generate_transaction_id(self) -> str:
        self._transaction_counter += 1
        return f"RFD{self._transaction_counter:06d}"
