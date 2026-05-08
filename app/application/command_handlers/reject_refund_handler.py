"""Reject Refund Handler"""

from app.application.commands.reject_refund_command import RejectRefundCommand


class RejectRefundHandler:
    """Handler for RejectRefundCommand"""

    def __init__(self, refund_repository):
        self.refund_repository = refund_repository

    def handle(self, command: RejectRefundCommand) -> None:
        """
        Handle refund rejection
        
        Args:
            command: RejectRefundCommand instance
        """
        refund = self.refund_repository.get_by_id(command.refund_id)
        refund.reject(reason=command.reason)
        self.refund_repository.save(refund)
