from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.infrastructure.config.container import get_container, Container
from app.presentation.schemas.event_schemas import (
    CreateEventRequest,
    CreateTicketCategoryRequest,
    EventResponse
)
from app.application.commands.create_event_command import CreateEventCommand
from app.application.commands.create_ticket_category_command import CreateTicketCategoryCommand
from app.application.commands.publish_event_command import PublishEventCommand

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
