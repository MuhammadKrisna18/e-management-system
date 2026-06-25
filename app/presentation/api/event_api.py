from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from app.infrastructure.config.container import get_container, Container
from app.presentation.schemas.event_schemas import (
    CreateEventRequest,
    CreateTicketCategoryRequest,
    EventResponse,
    AvailableEventsResponse,
    EventDetailResponse,
    EventSalesReportResponse,
    EventParticipantsResponse
)
from app.application.commands.create_event_command import CreateEventCommand
from app.application.commands.create_ticket_category_command import CreateTicketCategoryCommand
from app.application.commands.publish_event_command import PublishEventCommand
from app.application.commands.cancel_event_command import CancelEventCommand
from app.application.commands.disable_ticket_category_command import DisableTicketCategoryCommand
from app.application.commands.check_in_ticket_command import CheckInTicketCommand
from app.presentation.schemas.booking_schemas import TicketResponse
from app.application.queries.event_queries import GetEventSalesReportQuery, GetEventParticipantsQuery
from app.application.queries.event_queries import GetAvailableEventsQuery, GetEventDetailsQuery

router = APIRouter(prefix="/events", tags=["Events"])

def get_app_container() -> Container:
    return get_container()

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    request: CreateEventRequest,
    container: Container = Depends(get_app_container)
):
    try:
        command = CreateEventCommand(
            name=request.name,
            start_date=request.start_date,
            end_date=request.end_date,
            capacity=request.capacity
        )
        handler = container.get_create_event_handler()
        event_aggregate = handler.handle(command)
        

        return event_aggregate.event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{event_id}/categories", response_model=EventResponse)
def create_ticket_category(
    event_id: str,
    request: CreateTicketCategoryRequest,
    container: Container = Depends(get_app_container)
):
    try:
        command = CreateTicketCategoryCommand(
            event_id=event_id,
            name=request.name,
            price=request.price,
            quota=request.quota,
            sales_start_date=request.sales_start_date,
            sales_end_date=request.sales_end_date
        )
        handler = container.get_create_ticket_category_handler()
        event_aggregate = handler.handle(command)
        return event_aggregate.event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{event_id}/publish", response_model=EventResponse)
def publish_event(
    event_id: str,
    container: Container = Depends(get_app_container)
):
    try:
        command = PublishEventCommand(event_id=event_id)
        handler = container.get_publish_event_handler()
        event_aggregate = handler.handle(command)
        return event_aggregate.event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{event_id}/cancel", response_model=EventResponse)
def cancel_event(
    event_id: str,
    container: Container = Depends(get_app_container)
):
    try:
        command = CancelEventCommand(event_id=event_id)
        handler = container.get_cancel_event_handler()
        event_aggregate = handler.handle(command)
        return event_aggregate.event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{event_id}/ticket-categories/{category_name}/disable", response_model=EventResponse)
def disable_ticket_category(
    event_id: str,
    category_name: str,
    container: Container = Depends(get_app_container)
):
    try:
        command = DisableTicketCategoryCommand(event_id=event_id, category_name=category_name)
        handler = container.get_disable_ticket_category_handler()
        event_aggregate = handler.handle(command)
        return event_aggregate.event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{event_id}/tickets/{ticket_code}/check-in", response_model=TicketResponse)
def check_in_ticket(
    event_id: str,
    ticket_code: str,
    container: Container = Depends(get_app_container)
):
    try:
        command = CheckInTicketCommand(ticket_code=ticket_code, event_id=event_id)
        handler = container.get_check_in_ticket_handler()
        ticket = handler.handle(command)
        return ticket
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=AvailableEventsResponse)
def get_available_events(
    date: str = Query(None, description="Filter by date"),
    location: str = Query(None, description="Filter by location"),
    container: Container = Depends(get_app_container)
):
    query = GetAvailableEventsQuery(date=date, location=location)
    handler = container.get_available_events_handler()
    return handler.handle(query)

@router.get("/{event_id}", response_model=EventDetailResponse)
def get_event_details(
    event_id: str,
    container: Container = Depends(get_app_container)
):
    try:
        query = GetEventDetailsQuery(event_id=event_id)
        handler = container.get_event_details_handler()
        return handler.handle(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{event_id}/sales-report", response_model=EventSalesReportResponse)
def get_sales_report(
    event_id: str,
    container: Container = Depends(get_app_container)
):
    try:
        query = GetEventSalesReportQuery(event_id=event_id)
        handler = container.get_event_sales_report_handler()
        return handler.handle(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{event_id}/participants", response_model=EventParticipantsResponse)
def get_participants(
    event_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    container: Container = Depends(get_app_container)
):
    try:
        query = GetEventParticipantsQuery(event_id=event_id, page=page, page_size=page_size)
        handler = container.get_event_participants_handler()
        return handler.handle(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
