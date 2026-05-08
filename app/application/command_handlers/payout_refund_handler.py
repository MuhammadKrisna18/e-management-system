"""Payout Refund Handler"""

from app.application.commands.payout_refund_command import PayoutRefundCommand


class PayoutRefundHandler:
    """Handler for PayoutRefundCommand"""

    def __init__(self, refund_repository, refund_payment_service):
        self.refund_repository = refund_repository
        self.refund_payment_service = refund_payment_service

    def handle(self, command: PayoutRefundCommand) -> None:
        """
        Handle refund payout
        
        Args:
            command: PayoutRefundCommand instance
        """
        refund = self.refund_repository.get_by_id(command.refund_id)
        
        # Process payout
        payout_result = self.refund_payment_service.process_payout(
            refund_id=command.refund_id,
            amount=refund.amount,
        )
        
        if payout_result["success"]:
            refund.payout()
            self.refund_repository.save(refund)
