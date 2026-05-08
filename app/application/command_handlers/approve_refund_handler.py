"""Approve Refund Handler"""

from app.application.commands.approve_refund_command import ApproveRefundCommand


class ApproveRefundHandler:
    """Handler for ApproveRefundCommand"""

    def __init__(self, refund_repository):
        self.refund_repository = refund_repository

    def handle(self, command: ApproveRefundCommand) -> None:
        """
        Handle refund approval
        
        Args:
            command: ApproveRefundCommand instance
        """
        refund = self.refund_repository.get_by_id(command.refund_id)
        refund.approve(notes=command.notes)
        self.refund_repository.save(refund)
