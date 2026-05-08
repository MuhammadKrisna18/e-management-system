"""Request Refund Handler"""

from app.application.commands.request_refund_command import RequestRefundCommand


class RequestRefundHandler:
    """Handler for RequestRefundCommand"""

    def __init__(self, refund_repository, booking_repository):
        self.refund_repository = refund_repository
        self.booking_repository = booking_repository

    def handle(self, command: RequestRefundCommand) -> str:
        """
        Handle refund request
        
        Args:
            command: RequestRefundCommand instance
            
        Returns:
            Refund ID
        """
        from app.domain.entities.refund import Refund

        booking = self.booking_repository.get_by_id(command.booking_id)
        
        refund = Refund(
            booking_id=command.booking_id,
            amount=command.amount,
            reason=command.reason,
            status="PENDING",
        )

        self.refund_repository.save(refund)
        return refund.id
