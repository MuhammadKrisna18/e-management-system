

class MarkRefundPayoutCommand:

    def __init__(self, refund_id: str, payment_reference: str):
        self.refund_id = refund_id
        self.payment_reference = payment_reference
