"""Payout Refund Command"""


class PayoutRefundCommand:
    """Command to payout a refund"""

    def __init__(self, refund_id: str):
        self.refund_id = refund_id
