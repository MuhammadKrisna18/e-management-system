"""Pay Booking Handler"""

from app.application.commands.pay_booking_command import PayBookingCommand


class PayBookingHandler:
    """Handler for PayBookingCommand"""

    def __init__(self, booking_repository, payment_service):
        self.booking_repository = booking_repository
        self.payment_service = payment_service

    def handle(self, command: PayBookingCommand) -> None:
        """
        Handle booking payment
        
        Args:
            command: PayBookingCommand instance
        """
        booking = self.booking_repository.get_by_id(command.booking_id)
        
        # Process payment
        payment_result = self.payment_service.process_payment(
            booking_id=command.booking_id,
            amount=command.amount,
            payment_method=command.payment_method,
            payment_reference=command.payment_reference,
        )
        
        if payment_result["success"]:
            booking.pay()
            self.booking_repository.save(booking)
