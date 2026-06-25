from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List

from app.infrastructure.config.container import get_container, Container
from app.presentation.schemas.event_schemas import (
    CreateEventRequest,
    CreateTicketCategoryRequest,
    EventResponse,
    EventDetailResponse,
    TicketCategoryResponse,
    EventSalesReportResponse,
    EventParticipantsResponse,
)
from app.application.commands.create_event_command import CreateEventCommand
from app.application.commands.publish_event_command import PublishEventCommand
from app.application.commands.cancel_event_command import CancelEventCommand
from app.application.commands.create_ticket_category_command import CreateTicketCategoryCommand
from app.application.commands.disable_ticket_category_command import DisableTicketCategoryCommand
from app.application.queries.get_available_events_query import GetAvailableEventsQuery
from app.application.queries.get_event_details_query import GetEventDetailsQuery
from app.application.queries.event_queries import GetEventSalesReportQuery, GetEventParticipantsQuery

router = APIRouter(prefix="/events", tags=["Events"])


def get_app_container() -> Container:
    return get_container()


def _map_event(agg) -> dict:
    e = agg.event
    return {
        "event_id": e.event_id,
        "name": e.name,
        "start_date": e.start_date,
        "end_date": e.end_date,
        "capacity": e.capacity,
        "status": e.status,
    }


def _map_event_detail(agg) -> dict:
    data = _map_event(agg)
    data["ticket_categories"] = [
        {
            "name": c.name,
            "price": c.price,
            "quota": c.quota,
            "sales_start_date": c.sales_start_date,
            "sales_end_date": c.sales_end_date,
            "is_active": c.is_active,
        }
        for c in agg.ticket_categories
    ]
    return data


# ── US1: Create Event ────────────────────────────────────────────────────────

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED,
             summary="US1 - Create Event")
def create_event(
    request: CreateEventRequest,
    container: Container = Depends(get_app_container),
):
    """Create a new event in Draft status."""
    try:
        command = CreateEventCommand(
            name=request.name,
            start_date=request.start_date,
            end_date=request.end_date,
            capacity=request.capacity,
        )
        agg = container.get_create_event_handler().handle(command)
        return _map_event(agg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US2: Publish Event ───────────────────────────────────────────────────────

@router.post("/{event_id}/publish", response_model=EventResponse,
             summary="US2 - Publish Event")
def publish_event(
    event_id: str,
    container: Container = Depends(get_app_container),
):
    """Publish an event so customers can book tickets."""
    try:
        command = PublishEventCommand(event_id=event_id)
        agg = container.get_publish_event_handler().handle(command)
        return _map_event(agg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US3: Cancel Event ────────────────────────────────────────────────────────

@router.post("/{event_id}/cancel", response_model=EventResponse,
             summary="US3 - Cancel Event")
def cancel_event(
    event_id: str,
    container: Container = Depends(get_app_container),
):
    """Cancel an event. All ticket categories will be disabled."""
    try:
        command = CancelEventCommand(event_id=event_id)
        agg = container.get_cancel_event_handler().handle(command)
        return _map_event(agg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US4: Create Ticket Category ──────────────────────────────────────────────

@router.post("/{event_id}/categories", response_model=EventDetailResponse,
             status_code=status.HTTP_201_CREATED,
             summary="US4 - Create Ticket Category")
def create_ticket_category(
    event_id: str,
    request: CreateTicketCategoryRequest,
    container: Container = Depends(get_app_container),
):
    """Add a ticket category to an event."""
    try:
        command = CreateTicketCategoryCommand(
            event_id=event_id,
            name=request.name,
            price=request.price,
            quota=request.quota,
            sales_start_date=request.sales_start_date,
            sales_end_date=request.sales_end_date,
        )
        agg = container.get_create_ticket_category_handler().handle(command)
        return _map_event_detail(agg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US5: Disable Ticket Category ─────────────────────────────────────────────

@router.post("/{event_id}/categories/{category_name}/disable",
             response_model=EventDetailResponse,
             summary="US5 - Disable Ticket Category")
def disable_ticket_category(
    event_id: str,
    category_name: str,
    container: Container = Depends(get_app_container),
):
    """Disable a ticket category so it can no longer be booked."""
    try:
        command = DisableTicketCategoryCommand(event_id=event_id, category_name=category_name)
        agg = container.get_disable_ticket_category_handler().handle(command)
        return _map_event_detail(agg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US6: View Available Events ───────────────────────────────────────────────

@router.get("", response_model=List[EventResponse],
            summary="US6 - View Available Events")
def get_available_events(
    container: Container = Depends(get_app_container),
):
    """List all published events available for booking."""
    query = GetAvailableEventsQuery()
    aggs = container.get_available_events_handler().handle(query)
    return [_map_event(a) for a in aggs]


# ── US7: View Event Details ──────────────────────────────────────────────────

@router.get("/{event_id}", response_model=EventDetailResponse,
            summary="US7 - View Event Details")
def get_event_details(
    event_id: str,
    container: Container = Depends(get_app_container),
):
    """Get full details of an event including ticket categories."""
    query = GetEventDetailsQuery(event_id=event_id)
    agg = container.get_event_details_handler().handle(query)
    if not agg:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    return _map_event_detail(agg)


# ── US19: View Event Sales Report ────────────────────────────────────────────

@router.get("/{event_id}/report/sales", response_model=EventSalesReportResponse,
            summary="US19 - View Event Sales Report")
def get_event_sales_report(
    event_id: str,
    container: Container = Depends(get_app_container),
):
    """Get sales report for an event (revenue, bookings per category)."""
    try:
        query = GetEventSalesReportQuery(event_id=event_id)
        report = container.get_event_sales_report_handler().handle(query)
        return {
            "event_id": report.event_id,
            "event_name": report.event_name,
            "category_sales": [
                {
                    "category_name": c.category_name,
                    "quota": c.quota,
                    "sold": c.sold,
                    "available": c.available,
                    "revenue": c.revenue,
                }
                for c in report.category_sales
            ],
            "booking_stats": {
                "pending_payment": report.booking_stats.pending_payment,
                "paid": report.booking_stats.paid,
                "expired": report.booking_stats.expired,
                "refunded": report.booking_stats.refunded,
            },
            "total_revenue": report.total_revenue,
            "report_generated_at": report.report_generated_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── US20: View Event Participants ─────────────────────────────────────────────

@router.get("/{event_id}/report/participants", response_model=EventParticipantsResponse,
            summary="US20 - View Event Participants")
def get_event_participants(
    event_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    container: Container = Depends(get_app_container),
):
    """Get list of participants (paid ticket holders) for an event."""
    try:
        query = GetEventParticipantsQuery(event_id=event_id, page=page, page_size=page_size)
        result = container.get_event_participants_handler().handle(query)
        return {
            "event_id": result.event_id,
            "event_name": result.event_name,
            "participants": [
                {
                    "customer_id": p.customer_id,
                    "ticket_category": p.ticket_category,
                    "ticket_code": p.ticket_code,
                    "check_in_status": p.check_in_status,
                    "checked_in_at": p.checked_in_at,
                }
                for p in result.participants
            ],
            "total": result.total,
            "page": result.page,
            "page_size": result.page_size,
            "total_pages": result.total_pages,
            "generated_at": result.generated_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
