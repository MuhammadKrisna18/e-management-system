"""Expire Booking Handler"""

from app.application.commands.expire_booking_command import ExpireBookingCommand


class ExpireBookingHandler:
    """Handler for ExpireBookingCommand"""

    def __init__(self, booking_repository):
        self.booking_repository = booking_repository

    def handle(self, command: ExpireBookingCommand) -> None:
        """
        Handle booking expiration
        
        Args:
            command: ExpireBookingCommand instance
        """
        booking = self.booking_repository.get_by_id(command.booking_id)
        booking.expire()
        self.booking_repository.save(booking)
