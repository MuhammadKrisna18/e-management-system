"""Refund Repository Interface"""
from abc import ABC
from abc import abstractmethod
from typing import List, Optional


class RefundRepository(ABC):
    """
    Repository interface for Refund aggregate.
    
    Defines the contract for refund persistence operations.
    """

    @abstractmethod
    def save(self, refund_aggregate) -> str:
        """
        Save or update a refund aggregate.
        
        Args:
            refund_aggregate: RefundAggregate instance
            
        Returns:
            str: Refund ID
        """
        pass

    @abstractmethod
    def get_by_id(self, refund_id: str) -> Optional[object]:
        """
        Retrieve a refund by ID.
        
        Args:
            refund_id: Refund identifier
            
        Returns:
            RefundAggregate or None if not found
        """
        pass

    @abstractmethod
    def find_by_booking(self, booking_id: str) -> Optional[object]:
        """
        Find refund by booking ID.
        
        Args:
            booking_id: Booking identifier
            
        Returns:
            RefundAggregate or None if not found
        """
        pass

    @abstractmethod
    def find_by_customer(self, customer_id: str) -> List[object]:
        """
        Find all refunds by customer.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            List of RefundAggregate instances
        """
        pass

    @abstractmethod
    def find_approved_pending_payout(self) -> List[object]:
        """
        Find approved refunds pending payout.
        
        Returns:
            List of approved pending RefundAggregate instances
        """
        pass

    @abstractmethod
    def find_all(self) -> List[object]:
        """
        Find all refunds.
        
        Returns:
            List of RefundAggregate instances
        """
        pass

    @abstractmethod
    def delete(self, refund_id: str) -> bool:
        """
        Delete a refund by ID.
        
        Args:
            refund_id: Refund identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        pass