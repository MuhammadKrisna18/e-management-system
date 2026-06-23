"""Approve Refund Command Handler"""
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.value_objects.booking_status import BookingStatus


class ApproveRefundHandler:
    """
    Handler for ApproveRefundCommand.
    Implements User Story 16: Approve Refund
    
    An Event Organizer can approve a refund request.
    When approved, the refund status changes to Approved and related 
    tickets are marked as Cancelled.
    """

    def __init__(
        self,
        refund_repository: RefundRepository,
        booking_repository: BookingRepository
    ):
        """
        Initialize handler with required repositories.
        
        Args:
            refund_repository: RefundRepository instance
            booking_repository: BookingRepository instance
        """
        self.refund_repository = refund_repository
        self.booking_repository = booking_repository

    def handle(self, command) -> dict:
        """
        Handle ApproveRefundCommand.
        
        Args:
            command: ApproveRefundCommand with refund_id
            
        Returns:
            dict: Result with refund_id and status
            
        Raises:
            ValueError: If refund not found or not in Requested status
        """
        # Get refund
        refund_agg = self.refund_repository.get_by_id(command.refund_id)
        if not refund_agg:
            raise ValueError(f"Refund {command.refund_id} not found")

        refund = refund_agg.refund

        # Validation: Refund must be in Requested status
        if refund.status != "Requested":
            raise ValueError(
                f"Refund can only be approved if in Requested status. "
                f"Current status: {refund.status}"
            )

        # Approve refund
        refund_agg.approve_refund()

        # Get booking and mark as Refunded
        booking_agg = self.booking_repository.get_by_id(refund.booking_id)
        if booking_agg:
            booking_agg.booking.status = BookingStatus.REFUNDED

            # Cancel all tickets
            if hasattr(booking_agg, 'tickets') and booking_agg.tickets:
                for ticket in booking_agg.tickets:
                    ticket.cancel()

            # Save booking
            self.booking_repository.save(booking_agg)

        # Save refund
        self.refund_repository.save(refund_agg)

        return {
            "refund_id": refund.refund_id,
            "status": str(refund.status),
            "message": "Refund approved successfully"
        }
