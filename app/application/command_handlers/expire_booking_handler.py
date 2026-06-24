
from app.application.commands.expire_booking_command import ExpireBookingCommand
from app.domain.repositories.booking_repository import BookingRepository


class ExpireBookingHandler:

    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def handle(self, command: ExpireBookingCommand) -> str:
        booking_agg = self.booking_repository.get_by_id(command.booking_id)
        if not booking_agg:
            raise ValueError(f"Booking {command.booking_id} not found")

        # Expire booking, this handles deadline checks and domain events
        booking_agg.expire_booking()

        # Save to repository
        self.booking_repository.save(booking_agg)

        return command.booking_id
