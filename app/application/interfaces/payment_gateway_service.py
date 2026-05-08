"""Payment Gateway Service Interface"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Any


class PaymentGatewayService(ABC):
    """Interface for payment gateway service"""

    @abstractmethod
    def process_payment(
        self,
        booking_id: str,
        amount: Decimal,
        payment_method: str,
        payment_reference: str,
    ) -> Dict[str, Any]:
        """
        Process payment for booking
        
        Args:
            booking_id: ID of the booking
            amount: Payment amount
            payment_method: Payment method (e.g., 'CARD', 'BANK_TRANSFER')
            payment_reference: Payment reference number
            
        Returns:
            Dictionary with payment result {success, transaction_id, message}
        """
        pass

    @abstractmethod
    def validate_payment(
        self,
        transaction_id: str,
    ) -> Dict[str, Any]:
        """
        Validate payment status
        
        Args:
            transaction_id: Payment transaction ID
            
        Returns:
            Dictionary with validation result {valid, status, amount}
        """
        pass
