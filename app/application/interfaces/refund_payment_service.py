"""Refund Payment Service Interface"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Any


class RefundPaymentService(ABC):
    """Interface for refund payment service"""

    @abstractmethod
    def process_payout(
        self,
        refund_id: str,
        amount: Decimal,
    ) -> Dict[str, Any]:
        """
        Process refund payout
        
        Args:
            refund_id: ID of the refund
            amount: Payout amount
            
        Returns:
            Dictionary with payout result {success, payout_id, message}
        """
        pass

    @abstractmethod
    def check_payout_status(
        self,
        payout_id: str,
    ) -> Dict[str, Any]:
        """
        Check payout status
        
        Args:
            payout_id: Payout ID
            
        Returns:
            Dictionary with payout status {status, amount, processed_at}
        """
        pass
