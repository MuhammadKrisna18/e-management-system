from typing import Optional
from sqlalchemy.orm import Session
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.aggregates.refund_aggregate import RefundAggregate
from app.domain.entities.refund import Refund
from app.domain.value_objects.money import Money
from app.infrastructure.database.models import RefundModel

class PostgresRefundRepository(RefundRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, aggregate: RefundAggregate) -> None:
        refund = aggregate.refund
        
        model = self.session.query(RefundModel).filter(RefundModel.refund_id == refund.refund_id).first()
        if not model:
            model = RefundModel(refund_id=refund.refund_id)
            self.session.add(model)
            
        model.booking_id = refund.booking_id
        model.customer_id = refund.customer_id
        model.event_id = refund.event_id
        model.refund_amount = refund.refund_amount.amount
        model.status = refund.status
        model.rejection_reason = refund.rejection_reason
        if refund.refund_deadline:
            model.refund_deadline = refund.refund_deadline.deadline
        model.approved_at = refund.approved_at
        model.rejected_at = refund.rejected_at
        model.payment_reference = refund.payment_reference
        model.paid_out_at = refund.paid_out_at
        
        self.session.commit()

    def get_by_id(self, refund_id: str) -> Optional[RefundAggregate]:
        model = self.session.query(RefundModel).filter(RefundModel.refund_id == refund_id).first()
        if not model:
            return None
            
        refund = Refund(
            booking_id=model.booking_id,
            customer_id=model.customer_id,
            event_id=model.event_id,
            refund_amount=Money(model.refund_amount)
        )
        refund.refund_id = model.refund_id
        refund.status = model.status
        refund.rejection_reason = model.rejection_reason
        refund.approved_at = model.approved_at
        refund.rejected_at = model.rejected_at
        refund.payment_reference = model.payment_reference
        refund.paid_out_at = model.paid_out_at
        
        from app.domain.value_objects.payment_deadline import PaymentDeadline
        if model.refund_deadline:
            refund.refund_deadline = PaymentDeadline(model.refund_deadline)
            
        return RefundAggregate(refund)

    def find_by_booking(self, booking_id: str) -> Optional[RefundAggregate]:
        model = self.session.query(RefundModel).filter(RefundModel.booking_id == booking_id).first()
        if not model:
            return None
        return self.get_by_id(model.refund_id)

    def find_by_customer(self, customer_id: str) -> list:
        models = self.session.query(RefundModel).filter(RefundModel.customer_id == customer_id).all()
        return [self.get_by_id(model.refund_id) for model in models if model]

    def find_approved_pending_payout(self) -> list:
        models = self.session.query(RefundModel).filter(RefundModel.status == "Approved").all()
        return [self.get_by_id(model.refund_id) for model in models if model]

    def find_all(self) -> list:
        models = self.session.query(RefundModel).all()
        return [self.get_by_id(model.refund_id) for model in models if model]

    def delete(self, refund_id: str) -> bool:
        model = self.session.query(RefundModel).filter(RefundModel.refund_id == refund_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
