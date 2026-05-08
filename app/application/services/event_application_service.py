"""Event Application Service"""

from typing import List, Optional
from datetime import datetime
from app.application.dto.event_dto import EventDTO
from app.application.commands.create_event_command import CreateEventCommand
from app.application.commands.publish_event_command import PublishEventCommand
from app.application.commands.cancel_event_command import CancelEventCommand
from app.application.queries.get_available_events_query import GetAvailableEventsQuery
from app.application.queries.get_event_detail_query import GetEventDetailQuery


class EventApplicationService:
    """Application service for event operations"""

    def __init__(
        self,
        create_event_handler,
        publish_event_handler,
        cancel_event_handler,
        get_available_events_handler,
        get_event_detail_handler,
        event_repository,
    ):
        self.create_event_handler = create_event_handler
        self.publish_event_handler = publish_event_handler
        self.cancel_event_handler = cancel_event_handler
        self.get_available_events_handler = get_available_events_handler
        self.get_event_detail_handler = get_event_detail_handler
        self.event_repository = event_repository

    def create_event(
        self,
        name: str,
        description: str,
        location: str,
        start_date: datetime,
        end_date: datetime,
        organizer_id: str,
        max_capacity: int,
    ) -> str:
        """Create a new event"""
        command = CreateEventCommand(
            name=name,
            description=description,
            location=location,
            start_date=start_date,
            end_date=end_date,
            organizer_id=organizer_id,
            max_capacity=max_capacity,
        )
        return self.create_event_handler.handle(command)

    def publish_event(self, event_id: str) -> None:
        """Publish an event"""
        command = PublishEventCommand(event_id=event_id)
        self.publish_event_handler.handle(command)

    def cancel_event(self, event_id: str, reason: str) -> None:
        """Cancel an event"""
        command = CancelEventCommand(event_id=event_id, reason=reason)
        self.cancel_event_handler.handle(command)

    def get_available_events(
        self,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[dict]:
        """Get available events"""
        query = GetAvailableEventsQuery(
            skip=skip,
            limit=limit,
            search=search,
            start_date=start_date,
            end_date=end_date,
        )
        return self.get_available_events_handler.handle(query)

    def get_event_detail(self, event_id: str) -> Optional[dict]:
        """Get event details"""
        query = GetEventDetailQuery(event_id=event_id)
        return self.get_event_detail_handler.handle(query)
