"""Reject Refund Command"""


class RejectRefundCommand:
    """Command to reject a refund"""

    def __init__(self, refund_id: str, reason: str):
        self.refund_id = refund_id
        self.reason = reason
