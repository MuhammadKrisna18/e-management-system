from typing import Optional
from sqlalchemy.orm import Session
from app.domain.repositories.event_repository import EventRepository
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.value_objects.money import Money
from app.infrastructure.database.models import EventModel, TicketCategoryModel

class PostgresEventRepository(EventRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, event_aggregate: EventAggregate) -> None:
        event = event_aggregate.event
        
        event_model = self.session.query(EventModel).filter(EventModel.event_id == event.event_id).first()
        if not event_model:
            event_model = EventModel(event_id=event.event_id)
            self.session.add(event_model)
            
        event_model.name = event.name
        event_model.start_date = event.start_date
        event_model.end_date = event.end_date
        event_model.capacity = event.capacity
        event_model.status = event.status
        
        # Sync ticket categories
        existing_categories = {tc.name: tc for tc in event_model.ticket_categories}
        
        for category in event_aggregate.ticket_categories:
            if category.name in existing_categories:
                tc_model = existing_categories[category.name]
            else:
                tc_model = TicketCategoryModel(event_id=event.event_id, name=category.name)
                event_model.ticket_categories.append(tc_model)
            
            tc_model.price = category.price if isinstance(category.price, float) else float(category.price)
            tc_model.quota = category.quota
            tc_model.sales_start_date = category.sales_start_date
            tc_model.sales_end_date = category.sales_end_date
            tc_model.is_active = category.is_active
            
        self.session.commit()

    def get_by_id(self, event_id: str) -> Optional[EventAggregate]:
        event_model = self.session.query(EventModel).filter(EventModel.event_id == event_id).first()
        if not event_model:
            return None
            
        event = Event(
            name=event_model.name,
            start_date=event_model.start_date,
            end_date=event_model.end_date,
            capacity=event_model.capacity
        )
        event.event_id = event_model.event_id
        event.status = event_model.status
        
        aggregate = EventAggregate(event)
        
        for tc_model in event_model.ticket_categories:
            category = TicketCategory(
                name=tc_model.name,
                price=tc_model.price,
                quota=tc_model.quota,
                sales_start_date=tc_model.sales_start_date,
                sales_end_date=tc_model.sales_end_date,
                event_start_date=event_model.start_date
            )
            if not tc_model.is_active:
                category.disable()
            aggregate.ticket_categories.append(category)
            
        return aggregate
