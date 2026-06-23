class RefundRequested:
    pass


"""
Refund Domain Events

Events raised during refund lifecycle.
"""


class RefundRequested:
    """Event raised when refund is requested."""
    
    def __init__(self, refund_id: str, booking_id: str) -> None:
        """Initialize RefundRequested event."""
        self.refund_id: str = refund_id
        self.booking_id: str = booking_id
    
    def __str__(self) -> str:
        return f"RefundRequested(refund_id={self.refund_id})"


class RefundApproved:
    """Event raised when refund is approved."""
    
    def __init__(self, refund_id: str) -> None:
        """Initialize RefundApproved event."""
        self.refund_id: str = refund_id
    
    def __str__(self) -> str:
        return f"RefundApproved(refund_id={self.refund_id})"


class RefundRejected:
    """Event raised when refund is rejected."""
    
    def __init__(self, refund_id: str, reason: str) -> None:
        """Initialize RefundRejected event."""
        self.refund_id: str = refund_id
        self.reason: str = reason
    
    def __str__(self) -> str:
        return f"RefundRejected(refund_id={self.refund_id})"


class RefundPaidOut:
    """Event raised when refund is paid out."""
    
    def __init__(self, refund_id: str, payment_reference: str) -> None:
        """Initialize RefundPaidOut event."""
        self.refund_id: str = refund_id
        self.payment_reference: str = payment_reference
    
    def __str__(self) -> str:
        return f"RefundPaidOut(refund_id={self.refund_id})"