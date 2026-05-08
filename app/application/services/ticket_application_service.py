"""Ticket Application Service"""

from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from app.application.dto.ticket_dto import TicketDTO
from app.application.commands.create_ticket_category_command import (
    CreateTicketCategoryCommand,
)
from app.application.commands.disable_ticket_category_command import (
    DisableTicketCategoryCommand,
)
from app.application.commands.checkin_ticket_command import CheckinTicketCommand
from app.application.queries.get_participant_list_query import GetParticipantListQuery


class TicketApplicationService:
    """Application service for ticket operations"""

    def __init__(
        self,
        create_ticket_category_handler,
        disable_ticket_category_handler,
        checkin_ticket_handler,
        get_participant_list_handler,
        ticket_category_repository,
        ticket_repository,
    ):
        self.create_ticket_category_handler = create_ticket_category_handler
        self.disable_ticket_category_handler = disable_ticket_category_handler
        self.checkin_ticket_handler = checkin_ticket_handler
        self.get_participant_list_handler = get_participant_list_handler
        self.ticket_category_repository = ticket_category_repository
        self.ticket_repository = ticket_repository

    def create_ticket_category(
        self,
        event_id: str,
        name: str,
        price: Decimal,
        quantity: int,
        description: str = "",
    ) -> str:
        """Create a new ticket category"""
        command = CreateTicketCategoryCommand(
            event_id=event_id,
            name=name,
            price=price,
            quantity=quantity,
            description=description,
        )
        return self.create_ticket_category_handler.handle(command)

    def disable_ticket_category(self, ticket_category_id: str) -> None:
        """Disable a ticket category"""
        command = DisableTicketCategoryCommand(ticket_category_id=ticket_category_id)
        self.disable_ticket_category_handler.handle(command)

    def checkin_ticket(
        self,
        ticket_id: str,
        location: str,
        checked_in_at: datetime,
    ) -> None:
        """Check in a ticket"""
        command = CheckinTicketCommand(
            ticket_id=ticket_id,
            location=location,
            checked_in_at=checked_in_at,
        )
        self.checkin_ticket_handler.handle(command)

    def get_event_participants(
        self,
        event_id: str,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
    ) -> List[dict]:
        """Get event participants"""
        query = GetParticipantListQuery(
            event_id=event_id,
            skip=skip,
            limit=limit,
            search=search,
        )
        return self.get_participant_list_handler.handle(query)
