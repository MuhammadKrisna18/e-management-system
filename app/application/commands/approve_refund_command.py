"""Approve Refund Command"""


class ApproveRefundCommand:
    """Command to approve a refund"""

    def __init__(self, refund_id: str, notes: str = ""):
        self.refund_id = refund_id
        self.notes = notes
