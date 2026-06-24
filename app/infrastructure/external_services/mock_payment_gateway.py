"""Mock Payment Gateway Service Implementation"""
from typing import Dict, Optional
from app.application.interfaces.payment_gateway import PaymentGateway


class MockPaymentGatewayService(PaymentGateway):
    """
    Mock implementation of PaymentGatewayService.
    Simulates payment processing for development and testing.
    """

    def __init__(self):
        """Initialize mock service with transaction tracking."""
        self._transactions: Dict[str, dict] = {}
        self._transaction_counter = 0

    def charge(self, amount: float) -> str:
        """Implement PaymentGateway interface."""
        return self.process_payment(amount)

    def process_payment(
        self, amount: float, payment_method: str = "card"
    ) -> str:
        """
        Process payment and return transaction reference.
        
        Args:
            amount: Payment amount
            payment_method: Payment method (card, bank_transfer, etc)
            
        Returns:
            str: Transaction reference ID
            
        Raises:
            ValueError: If amount invalid
        """
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
        """
        Verify payment status.
        
        Args:
            transaction_id: Transaction reference ID
            
        Returns:
            bool: True if payment successful, False otherwise
        """
        if transaction_id not in self._transactions:
            return False
        return self._transactions[transaction_id]["status"] == "success"

    def cancel_payment(self, transaction_id: str) -> bool:
        """
        Cancel payment transaction.
        
        Args:
            transaction_id: Transaction reference ID
            
        Returns:
            bool: True if cancelled, False if not found
        """
        if transaction_id not in self._transactions:
            return False
        
        self._transactions[transaction_id]["status"] = "cancelled"
        return True

    def _generate_transaction_id(self) -> str:
        """
        Generate unique transaction ID.
        
        Returns:
            str: Generated transaction ID
        """
        self._transaction_counter += 1
        return f"TXN{self._transaction_counter:06d}"
