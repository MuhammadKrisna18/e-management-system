"""In-Memory Event Repository Implementation"""
from typing import Dict, List, Optional
from app.domain.repositories.event_repository import EventRepository
from app.domain.aggregates.event_aggregate import EventAggregate


class InMemoryEventRepository(EventRepository):
    """
    In-memory implementation of EventRepository.
    Stores EventAggregates in memory for development and testing.
    """

    def __init__(self):
        """Initialize in-memory storage."""
        self._events: Dict[str, EventAggregate] = {}
        self._event_counter = 0

    def save(self, event_aggregate: EventAggregate) -> str:
        """
        Save event aggregate and return event ID.
        
        Args:
            event_aggregate: EventAggregate to save
            
        Returns:
            str: Generated or existing event ID
        """
        if not event_aggregate.event.event_id:
            event_aggregate.event.event_id = self._generate_event_id()
        
        event_id = event_aggregate.event.event_id
        self._events[event_id] = event_aggregate
        return event_id

    def get_by_id(self, event_id: str) -> Optional[EventAggregate]:
        """
        Retrieve event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            EventAggregate or None if not found
        """
        return self._events.get(event_id)

    def find_all(self) -> List[EventAggregate]:
        """
        Find all events.
        
        Returns:
            List of EventAggregate instances
        """
        return list(self._events.values())

    def find_published(self) -> List[EventAggregate]:
        """
        Find all published events.
        
        Returns:
            List of published EventAggregate instances
        """
        return [
            agg for agg in self._events.values()
            if agg.event.status == "Published"
        ]

    def delete(self, event_id: str) -> bool:
        """
        Delete event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        if event_id in self._events:
            del self._events[event_id]
            return True
        return False

    def _generate_event_id(self) -> str:
        """
        Generate unique event ID with EV0000 format.
        
        Returns:
            str: Generated event ID
        """
        self._event_counter += 1
        return f"EV{self._event_counter:04d}"
