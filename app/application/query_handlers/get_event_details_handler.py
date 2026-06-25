from datetime import datetime
from app.application.dto.event_dto import EventDetailResponse, TicketCategoryDetailDto

class GetEventDetailsHandler:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def handle(
        self,
        query
    ) -> EventDetailResponse:

        agg = self.repository.get_by_id(query.event_id)
        if not agg:
            raise ValueError("Event not found")
            
        now = datetime.now()
        categories = []
        for cat in agg.ticket_categories:
            if not cat.is_active:
                continue
                
            status = "Available"
            if now < cat.sales_start_date:
                status = "Coming Soon"
            elif now > cat.sales_end_date:
                status = "Sales Closed"
            elif cat.quota <= 0:
                status = "Sold Out"
                
            categories.append(TicketCategoryDetailDto(
                name=cat.name,
                price=cat.price,
                status=status
            ))
            
        return EventDetailResponse(
            event_id=agg.event.event_id,
            name=agg.event.name,
            description="TBA",
            start_date=agg.event.start_date,
            location="Virtual / TBA",
            organizer="Organizer TBA",
            ticket_categories=categories
        )