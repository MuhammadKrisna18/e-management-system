from typing import Dict, List, Optional
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.aggregates.refund_aggregate import RefundAggregate
from app.domain.value_objects.refund_status import RefundStatus


class InMemoryRefundRepository(RefundRepository):

    def __init__(self):
        self._refunds: Dict[str, RefundAggregate] = {}

    def save(self, refund_aggregate: RefundAggregate) -> str:
        refund_id = refund_aggregate.refund.refund_id
        self._refunds[refund_id] = refund_aggregate
        return refund_id

    def get_by_id(self, refund_id: str) -> Optional[RefundAggregate]:
        return self._refunds.get(refund_id)

    def find_by_booking(self, booking_id: str) -> Optional[RefundAggregate]:
        for refund_agg in self._refunds.values():
            if refund_agg.refund.booking_id == booking_id:
                return refund_agg
        return None

    def find_by_customer(self, customer_id: str) -> List[RefundAggregate]:
        return [
            agg for agg in self._refunds.values()
            if agg.refund.customer_id == customer_id
        ]

    def find_approved_pending_payout(self) -> List[RefundAggregate]:
        return [
            agg for agg in self._refunds.values()
            if agg.refund.status == RefundStatus.APPROVED
        ]

    def find_all(self) -> List[RefundAggregate]:
        return list(self._refunds.values())

    def delete(self, refund_id: str) -> bool:
        if refund_id in self._refunds:
            del self._refunds[refund_id]
            return True
        return False
