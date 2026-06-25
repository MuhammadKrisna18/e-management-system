from datetime import datetime
from app.application.dto.event_dto import AvailableEventDto, AvailableEventsResponse

class GetAvailableEventsHandler:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def handle(
        self,
        query
    ) -> AvailableEventsResponse:
        
        events_agg = self.repository.find_published()
        
        # Apply date/location filters if any
        # (Assuming query has date and location optionally)
        dtos = []
        for agg in events_agg:
            # Lowest ticket price
            lowest = min((cat.price for cat in agg.ticket_categories), default=0.0)
            
            dtos.append(AvailableEventDto(
                event_id=agg.event.event_id,
                name=agg.event.name,
                start_date=agg.event.start_date,
                location="Virtual / TBA", # Hardcoded for now
                lowest_ticket_price=lowest
            ))
            
        return AvailableEventsResponse(events=dtos)