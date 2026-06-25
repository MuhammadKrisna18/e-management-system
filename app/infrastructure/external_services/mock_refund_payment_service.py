import uuid
from app.application.interfaces.refund_payment_service import RefundPaymentService


class MockRefundPaymentService(RefundPaymentService):
    """Mock refund payment service for testing — always succeeds."""

    def transfer(self, amount) -> str:
        ref = f"REF-{uuid.uuid4().hex[:8].upper()}"
        print(f"[MockRefundPaymentService] Transferred {amount}. Reference: {ref}")
        return ref

    def process_refund(self, account_number: str, refund_amount: float, reference_id: str) -> str:
        """Process refund payout — used by main.py demo."""
        ref = f"REF-{uuid.uuid4().hex[:8].upper()}"
        print(f"[MockRefundPaymentService] Refund to {account_number}, amount={refund_amount}, ref={ref}")
        return ref

    def process_refund_payout(self, refund_id: str, amount: float) -> str:
        ref = f"REF-{uuid.uuid4().hex[:8].upper()}"
        print(f"[MockRefundPaymentService] Payout for refund {refund_id}, amount={amount}. Reference: {ref}")
        return ref

    def verify_refund_status(self, payment_reference: str) -> str:
        """Verify refund status — used by MarkRefundPayoutHandler."""
        return "completed"
