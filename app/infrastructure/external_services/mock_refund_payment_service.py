from app.application.interfaces.refund_payment_service import RefundPaymentServiceInterface
import uuid

class MockRefundPaymentService(RefundPaymentServiceInterface):
    def process_refund_payout(self, refund_id: str, amount: float) -> str:
        # Simulate generating a payment reference
        reference = f"REF-{uuid.uuid4().hex[:8].upper()}"
        print(f"[MockRefundPaymentService] Processed refund {refund_id} for amount {amount}. Reference: {reference}")
        return reference
