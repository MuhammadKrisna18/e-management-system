"""Mock Refund Payment Service Implementation"""
from typing import Dict
from app.application.services.refund_payment_service import RefundPaymentService


class MockRefundPaymentService(RefundPaymentService):
    """
    Mock implementation of RefundPaymentService.
    Simulates refund processing for development and testing.
    """

    def __init__(self):
        """Initialize mock service with refund transaction tracking."""
        self._refund_transactions: Dict[str, dict] = {}
        self._transaction_counter = 0

    def process_refund(
        self, 
        account_number: str, 
        refund_amount: float, 
        reference_id: str
    ) -> str:
        """
        Process refund and return transaction reference.
        
        Args:
            account_number: Customer bank account
            refund_amount: Refund amount
            reference_id: Booking/refund reference
            
        Returns:
            str: Refund transaction reference
            
        Raises:
            ValueError: If parameters invalid
        """
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
        """
        Verify refund transaction status.
        
        Args:
            transaction_id: Refund transaction reference
            
        Returns:
            str: Status (processed, pending, completed, failed)
        """
        if transaction_id not in self._refund_transactions:
            return "failed"
        
        return self._refund_transactions[transaction_id]["status"]

    def cancel_refund(self, transaction_id: str) -> bool:
        """
        Cancel refund transaction (only if pending).
        
        Args:
            transaction_id: Refund transaction reference
            
        Returns:
            bool: True if cancelled, False if not found or already processed
        """
        if transaction_id not in self._refund_transactions:
            return False
        
        transaction = self._refund_transactions[transaction_id]
        if transaction["status"] == "pending":
            transaction["status"] = "cancelled"
            return True
        
        return False

    def _generate_transaction_id(self) -> str:
        """
        Generate unique refund transaction ID.
        
        Returns:
            str: Generated transaction ID
        """
        self._transaction_counter += 1
        return f"RFD{self._transaction_counter:06d}"
