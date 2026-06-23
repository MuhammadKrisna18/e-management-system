class ApproveRefundCommand:
    """
    Command to approve a refund request.
    
    Used for User Story 16: Approve Refund
    """

    def __init__(self, refund_id: str):
        """
        Initialize ApproveRefundCommand.
        
        Args:
            refund_id: ID of the refund to approve
        """
        self.refund_id = refund_id