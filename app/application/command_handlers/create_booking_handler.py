"""Create Booking Handler"""

from app.application.commands.create_booking_command import CreateBookingCommand


class CreateBookingHandler:
    """Handler for CreateBookingCommand"""

    def __init__(self, booking_repository, ticket_category_repository):
        self.booking_repository = booking_repository
        self.ticket_category_repository = ticket_category_repository

    def handle(self, command: CreateBookingCommand) -> str:
        """
        Handle booking creation
        
        Args:
            command: CreateBookingCommand instance
            
        Returns:
            Booking ID
        """
        from app.domain.entities.booking import Booking

        booking = Booking(
            user_id=command.user_id,
            event_id=command.event_id,
            ticket_items=command.ticket_items,
            attendee_name=command.attendee_name,
            attendee_email=command.attendee_email,
        )

        self.booking_repository.save(booking)
        return booking.id
