"""Mark Refund as Paid Out Command"""


class MarkRefundPayoutCommand:
    """
    Command to mark a refund as paid out.
    
    Used for User Story 18: Mark Refund as Paid Out
    """

    def __init__(self, refund_id: str, payment_reference: str):
        """
        Initialize MarkRefundPayoutCommand.
        
        Args:
            refund_id: ID of the refund to mark as paid out
            payment_reference: Reference ID from payment service
        """
        self.refund_id = refund_id
        self.payment_reference = payment_reference
