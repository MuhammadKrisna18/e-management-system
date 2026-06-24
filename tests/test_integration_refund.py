import pytest
import uuid
from datetime import datetime, timedelta
from app.domain.entities.refund import Refund
from app.domain.aggregates.refund_aggregate import RefundAggregate
from app.domain.value_objects.money import Money
from app.domain.value_objects.refund_status import RefundStatus
from app.infrastructure.repositories.in_memory_refund_repository import (
    InMemoryRefundRepository,
)


class TestRefundWorkflowIntegration:

    def setup_method(self):
        self.refund_repository = InMemoryRefundRepository()

    def test_complete_refund_approval_workflow(self):
        # Request refund
        refund_id = str(uuid.uuid4())
        refund_deadline = datetime.now() + timedelta(days=7)
        refund = Refund(
            refund_id=refund_id,
            booking_id="BK001",
            customer_id="CUST001",
            event_id="EV001",
            refund_amount=Money(500000.0),
            refund_deadline=refund_deadline,
        )

        refund_agg = RefundAggregate(refund)
        self.refund_repository.save(refund_agg)

        # Verify requested
        saved_refund = self.refund_repository.get_by_id(refund_id)
        assert saved_refund.refund.status == RefundStatus.REQUESTED

        # Approve refund
        saved_refund.approve_refund()
        self.refund_repository.save(saved_refund)

        # Verify approved
        approved_refund = self.refund_repository.get_by_id(refund_id)
        assert approved_refund.refund.status == RefundStatus.APPROVED
        assert approved_refund.refund.approved_at is not None

        # Mark as paid out
        payment_ref = "TXN987654"
        approved_refund.mark_as_paid_out(payment_ref)
        self.refund_repository.save(approved_refund)

        # Verify paid out
        paid_refund = self.refund_repository.get_by_id(refund_id)
        assert paid_refund.refund.status == RefundStatus.PAID_OUT
        assert paid_refund.refund.payment_reference == payment_ref
        assert paid_refund.refund.paid_out_at is not None

    def test_refund_rejection_workflow(self):
        # Request refund
        refund_id = str(uuid.uuid4())
        refund = Refund(
            refund_id=refund_id,
            booking_id="BK002",
            customer_id="CUST002",
            event_id="EV002",
            refund_amount=Money(1000000.0),
            refund_deadline=datetime.now() + timedelta(days=7),
        )

        refund_agg = RefundAggregate(refund)
        self.refund_repository.save(refund_agg)

        # Reject refund
        rejection_reason = "Ticket already checked in"
        saved_refund = self.refund_repository.get_by_id(refund_id)
        saved_refund.reject_refund(rejection_reason)
        self.refund_repository.save(saved_refund)

        # Verify rejected
        rejected_refund = self.refund_repository.get_by_id(refund_id)
        assert rejected_refund.refund.status == RefundStatus.REJECTED
        assert rejected_refund.refund.rejection_reason == rejection_reason
        assert rejected_refund.refund.rejected_at is not None

    def test_find_refund_by_booking(self):
        # Create refund for booking
        refund_id = str(uuid.uuid4())
        booking_id = "BK003"
        refund = Refund(
            refund_id=refund_id,
            booking_id=booking_id,
            customer_id="CUST003",
            event_id="EV003",
            refund_amount=Money(750000.0),
            refund_deadline=datetime.now() + timedelta(days=7),
        )

        refund_agg = RefundAggregate(refund)
        self.refund_repository.save(refund_agg)

        # Find by booking
        found_refund = self.refund_repository.find_by_booking(booking_id)
        assert found_refund is not None
        assert found_refund.refund.refund_id == refund_id

    def test_find_approved_pending_payout_refunds(self):
        # Create approved refund
        approved_id = str(uuid.uuid4())
        approved_refund = Refund(
            refund_id=approved_id,
            booking_id="BK004",
            customer_id="CUST004",
            event_id="EV004",
            refund_amount=Money(500000.0),
            refund_deadline=datetime.now() + timedelta(days=7),
        )
        approved_agg = RefundAggregate(approved_refund)
        approved_agg.approve_refund()
        self.refund_repository.save(approved_agg)

        # Create paid out refund
        paid_id = str(uuid.uuid4())
        paid_refund = Refund(
            refund_id=paid_id,
            booking_id="BK005",
            customer_id="CUST005",
            event_id="EV005",
            refund_amount=Money(300000.0),
            refund_deadline=datetime.now() + timedelta(days=7),
        )
        paid_agg = RefundAggregate(paid_refund)
        paid_agg.approve_refund()
        paid_agg.mark_as_paid_out("TXN123")
        self.refund_repository.save(paid_agg)

        # Find approved pending
        pending = self.refund_repository.find_approved_pending_payout()
        assert len(pending) == 1
        assert pending[0].refund.refund_id == approved_id

    def test_find_customer_refunds(self):
        customer_id = "CUST006"

        # Create multiple refunds
        for i in range(3):
            refund_id = str(uuid.uuid4())
            refund = Refund(
                refund_id=refund_id,
                booking_id=f"BK00{i}",
                customer_id=customer_id,
                event_id=f"EV00{i}",
                refund_amount=Money(100000.0 * (i + 1)),
                refund_deadline=datetime.now() + timedelta(days=7),
            )
            refund_agg = RefundAggregate(refund)
            self.refund_repository.save(refund_agg)

        # Find customer refunds
        customer_refunds = self.refund_repository.find_by_customer(customer_id)
        assert len(customer_refunds) == 3

    def test_refund_expiration_check(self):
        # Create refund with past deadline
        refund_deadline = datetime.now() - timedelta(days=1)
        refund = Refund(
            refund_id=str(uuid.uuid4()),
            booking_id="BK007",
            customer_id="CUST007",
            event_id="EV007",
            refund_amount=Money(200000.0),
            refund_deadline=refund_deadline,
        )

        # Check expiration
        assert refund.is_expired() is True
        assert refund.is_expired(datetime.now() - timedelta(days=2)) is False
