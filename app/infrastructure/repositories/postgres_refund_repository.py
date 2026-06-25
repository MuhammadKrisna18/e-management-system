from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.aggregates.refund_aggregate import RefundAggregate
from app.domain.entities.refund import Refund
from app.domain.value_objects.money import Money
from app.domain.value_objects.refund_status import RefundStatus
from app.infrastructure.database.models import RefundModel


class PostgresRefundRepository(RefundRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, aggregate: RefundAggregate) -> str:
        refund = aggregate.refund
        model = self.session.query(RefundModel).filter(RefundModel.refund_id == refund.refund_id).first()
        if not model:
            model = RefundModel(refund_id=refund.refund_id)
            self.session.add(model)

        model.booking_id = refund.booking_id
        model.customer_id = refund.customer_id
        model.event_id = refund.event_id
        model.refund_amount = refund.refund_amount.amount
        model.status = refund.status.value if hasattr(refund.status, 'value') else str(refund.status)
        model.rejection_reason = refund.rejection_reason
        model.refund_deadline = refund.refund_deadline
        model.approved_at = refund.approved_at
        model.rejected_at = refund.rejected_at
        model.payment_reference = refund.payment_reference
        model.paid_out_at = refund.paid_out_at
        self.session.commit()
        return refund.refund_id

    def get_by_id(self, refund_id: str) -> Optional[RefundAggregate]:
        model = self.session.query(RefundModel).filter(RefundModel.refund_id == refund_id).first()
        if not model:
            return None
        return self._to_aggregate(model)

    def find_by_booking(self, booking_id: str) -> Optional[RefundAggregate]:
        model = self.session.query(RefundModel).filter(RefundModel.booking_id == booking_id).first()
        if not model:
            return None
        return self._to_aggregate(model)

    def find_by_customer(self, customer_id: str) -> List[RefundAggregate]:
        models = self.session.query(RefundModel).filter(RefundModel.customer_id == customer_id).all()
        return [self._to_aggregate(m) for m in models]

    def find_approved_pending_payout(self) -> List[RefundAggregate]:
        models = self.session.query(RefundModel).filter(
            RefundModel.status == RefundStatus.APPROVED.value
        ).all()
        return [self._to_aggregate(m) for m in models]

    def find_all(self) -> List[RefundAggregate]:
        models = self.session.query(RefundModel).all()
        return [self._to_aggregate(m) for m in models]

    def delete(self, refund_id: str) -> bool:
        model = self.session.query(RefundModel).filter(RefundModel.refund_id == refund_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False

    def _to_aggregate(self, model: RefundModel) -> RefundAggregate:
        refund = Refund(
            refund_id=model.refund_id,
            booking_id=model.booking_id,
            customer_id=model.customer_id,
            event_id=model.event_id,
            refund_amount=Money(model.refund_amount),
            refund_deadline=model.refund_deadline,
        )
        refund.status = RefundStatus(model.status) if model.status else refund.status
        refund.rejection_reason = model.rejection_reason
        refund.approved_at = model.approved_at
        refund.rejected_at = model.rejected_at
        refund.payment_reference = model.payment_reference
        refund.paid_out_at = model.paid_out_at
        return RefundAggregate(refund)
