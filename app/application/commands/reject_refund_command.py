"""Reject Refund Command"""


class RejectRefundCommand:
    """
    Command to reject a refund request.
    
    Used for User Story 17: Reject Refund
    """

    def __init__(self, refund_id: str, reason: str):
        """
        Initialize RejectRefundCommand.
        
        Args:
            refund_id: ID of the refund to reject
            reason: Reason for rejection
        """
        self.refund_id = refund_id
        self.reason = reason
