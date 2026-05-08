"""Booking Application Service"""

from typing import List, Optional
from decimal import Decimal
from app.application.dto.booking_dto import BookingDTO
from app.application.commands.create_booking_command import CreateBookingCommand
from app.application.commands.pay_booking_command import PayBookingCommand
from app.application.commands.expire_booking_command import ExpireBookingCommand
from app.application.queries.get_purchased_tickets_query import GetPurchasedTicketsQuery


class BookingApplicationService:
    """Application service for booking operations"""

    def __init__(
        self,
        create_booking_handler,
        pay_booking_handler,
        expire_booking_handler,
        get_purchased_tickets_handler,
        booking_repository,
    ):
        self.create_booking_handler = create_booking_handler
        self.pay_booking_handler = pay_booking_handler
        self.expire_booking_handler = expire_booking_handler
        self.get_purchased_tickets_handler = get_purchased_tickets_handler
        self.booking_repository = booking_repository

    def create_booking(
        self,
        user_id: str,
        event_id: str,
        ticket_items: List[dict],
        attendee_name: str,
        attendee_email: str,
    ) -> str:
        """Create a new booking"""
        command = CreateBookingCommand(
            user_id=user_id,
            event_id=event_id,
            ticket_items=ticket_items,
            attendee_name=attendee_name,
            attendee_email=attendee_email,
        )
        return self.create_booking_handler.handle(command)

    def pay_booking(
        self,
        booking_id: str,
        amount: Decimal,
        payment_method: str,
        payment_reference: str,
    ) -> None:
        """Pay for a booking"""
        command = PayBookingCommand(
            booking_id=booking_id,
            amount=amount,
            payment_method=payment_method,
            payment_reference=payment_reference,
        )
        self.pay_booking_handler.handle(command)

    def expire_booking(self, booking_id: str) -> None:
        """Expire a booking"""
        command = ExpireBookingCommand(booking_id=booking_id)
        self.expire_booking_handler.handle(command)

    def get_user_bookings(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
    ) -> List[dict]:
        """Get user's bookings"""
        query = GetPurchasedTicketsQuery(
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status,
        )
        return self.get_purchased_tickets_handler.handle(query)
