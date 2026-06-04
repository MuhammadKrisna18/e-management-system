"""In-Memory Refund Repository Implementation"""
from typing import Dict, List, Optional
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.aggregates.refund_aggregate import RefundAggregate
from app.domain.value_objects.refund_status import RefundStatus


class InMemoryRefundRepository(RefundRepository):
    """
    In-memory implementation of RefundRepository.
    Stores RefundAggregates in memory for development and testing.
    """

    def __init__(self):
        """Initialize in-memory storage."""
        self._refunds: Dict[str, RefundAggregate] = {}

    def save(self, refund_aggregate: RefundAggregate) -> str:
        """
        Save refund aggregate.
        
        Args:
            refund_aggregate: RefundAggregate to save
            
        Returns:
            str: Refund ID
        """
        refund_id = refund_aggregate.refund.refund_id
        self._refunds[refund_id] = refund_aggregate
        return refund_id

    def get_by_id(self, refund_id: str) -> Optional[RefundAggregate]:
        """
        Retrieve refund by ID.
        
        Args:
            refund_id: Refund identifier
            
        Returns:
            RefundAggregate or None if not found
        """
        return self._refunds.get(refund_id)

    def find_by_booking(self, booking_id: str) -> Optional[RefundAggregate]:
        """
        Find refund by booking ID.
        
        Args:
            booking_id: Booking identifier
            
        Returns:
            RefundAggregate or None if not found
        """
        for refund_agg in self._refunds.values():
            if refund_agg.refund.booking_id == booking_id:
                return refund_agg
        return None

    def find_by_customer(self, customer_id: str) -> List[RefundAggregate]:
        """
        Find all refunds by customer.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            List of RefundAggregate instances
        """
        return [
            agg for agg in self._refunds.values()
            if agg.refund.customer_id == customer_id
        ]

    def find_approved_pending_payout(self) -> List[RefundAggregate]:
        """
        Find approved refunds pending payout.
        
        Returns:
            List of approved pending RefundAggregate instances
        """
        return [
            agg for agg in self._refunds.values()
            if agg.refund.status == RefundStatus.APPROVED
        ]

    def find_all(self) -> List[RefundAggregate]:
        """
        Find all refunds.
        
        Returns:
            List of RefundAggregate instances
        """
        return list(self._refunds.values())

    def delete(self, refund_id: str) -> bool:
        """
        Delete refund by ID.
        
        Args:
            refund_id: Refund identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        if refund_id in self._refunds:
            del self._refunds[refund_id]
            return True
        return False
