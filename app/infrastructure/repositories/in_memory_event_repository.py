from typing import Dict, List, Optional
from app.domain.repositories.event_repository import EventRepository
from app.domain.aggregates.event_aggregate import EventAggregate


class InMemoryEventRepository(EventRepository):

    def __init__(self):
        self._events: Dict[str, EventAggregate] = {}
        self._event_counter = 0

    def save(self, event_aggregate: EventAggregate) -> str:
        if not event_aggregate.event.event_id:
            event_aggregate.event.event_id = self._generate_event_id()
        
        event_id = event_aggregate.event.event_id
        self._events[event_id] = event_aggregate
        return event_id

    def get_by_id(self, event_id: str) -> Optional[EventAggregate]:
        return self._events.get(event_id)

    def find_all(self) -> List[EventAggregate]:
        return list(self._events.values())

    def find_published(self) -> List[EventAggregate]:
        return [
            agg for agg in self._events.values()
            if agg.event.status == "Published"
        ]

    def delete(self, event_id: str) -> bool:
        if event_id in self._events:
            del self._events[event_id]
            return True
        return False

    def _generate_event_id(self) -> str:
        self._event_counter += 1
        return f"EV{self._event_counter:04d}"
