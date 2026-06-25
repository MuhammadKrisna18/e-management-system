from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.infrastructure.config.container import get_container, Container
from app.presentation.schemas.booking_schemas import (
    CreateBookingRequest,
    PayBookingRequest,
    BookingResponse,
    PurchasedTicketsResponse,
    CheckInTicketRequest,
    CheckInResponse,
    CalculatePriceRequest,
    CalculatePriceResponse,
)
from app.application.commands.create_booking_command import CreateBookingCommand
from app.application.commands.pay_booking_command import PayBookingCommand
from app.application.commands.expire_booking_command import ExpireBookingCommand
from app.application.commands.check_in_ticket_command import CheckInTicketCommand
from app.application.queries.ticket_queries import GetPurchasedTicketsQuery

router = APIRouter(tags=["Bookings"])


def get_app_container() -> Container:
    return get_container()


def _map_booking(agg) -> dict:
    b = agg.booking
    return {
        "booking_id": b.booking_id,
        "customer_id": b.customer_id,
        "event_id": b.event_id,
        "ticket_category_name": b.ticket_category_name,
        "quantity": b.quantity,
        "total_price": b.total_price.amount if hasattr(b.total_price, "amount") else float(b.total_price),
        "status": b.status.value if hasattr(b.status, "value") else str(b.status),
        "payment_deadline": b.payment_deadline.deadline,
    }


# ── US8: Create Booking ──────────────────────────────────────────────────────

@router.post(
    "/bookings",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="US8 - Create Booking",
)
def create_booking(
    request: CreateBookingRequest,
    container: Container = Depends(get_app_container),
):
    """Create a booking for a published event. Payment deadline is 15 minutes."""
    try:
        command = CreateBookingCommand(
            customer_id=request.customer_id,
            event_id=request.event_id,
            ticket_category_name=request.ticket_category_name,
            quantity=request.quantity,
        )
        agg = container.get_create_booking_handler().handle(command)
        return _map_booking(agg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US9: Calculate Booking Price ─────────────────────────────────────────────

@router.post(
    "/bookings/calculate-price",
    response_model=CalculatePriceResponse,
    summary="US9 - Calculate Booking Total Price",
)
def calculate_price(
    request: CalculatePriceRequest,
    container: Container = Depends(get_app_container),
):
    """Calculate total price before booking (ticket price × quantity)."""
    try:
        from app.domain.services.pricing_service import PricingService
        event_agg = container.event_repository.get_by_id(request.event_id)
        if not event_agg:
            raise ValueError(f"Event {request.event_id} not found")
        category = next(
            (c for c in event_agg.ticket_categories if c.name == request.ticket_category_name),
            None,
        )
        if not category:
            raise ValueError(f"Ticket category '{request.ticket_category_name}' not found")
        total = PricingService.calculate_total_price(category.price, request.quantity)
        return {"total_price": total.amount}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US10: Pay Booking ────────────────────────────────────────────────────────

@router.post(
    "/bookings/{booking_id}/pay",
    response_model=BookingResponse,
    summary="US10 - Pay Booking",
)
def pay_booking(
    booking_id: str,
    request: PayBookingRequest,
    container: Container = Depends(get_app_container),
):
    """Pay for a pending booking within the 15-minute deadline."""
    try:
        command = PayBookingCommand(booking_id=booking_id, amount=request.amount)
        agg = container.get_pay_booking_handler().handle(command)
        return _map_booking(agg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US11: Expire Booking ─────────────────────────────────────────────────────

@router.post(
    "/bookings/{booking_id}/expire",
    response_model=BookingResponse,
    summary="US11 - Expire Booking",
)
def expire_booking(
    booking_id: str,
    container: Container = Depends(get_app_container),
):
    """Expire a booking whose payment deadline has passed."""
    try:
        command = ExpireBookingCommand(booking_id=booking_id)
        container.get_expire_booking_handler().handle(command)
        agg = container.booking_repository.get_by_id(booking_id)
        return _map_booking(agg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US12: View Purchased Tickets ─────────────────────────────────────────────

@router.get(
    "/customers/{customer_id}/tickets",
    response_model=PurchasedTicketsResponse,
    summary="US12 - View Purchased Tickets",
)
def get_purchased_tickets(
    customer_id: str,
    container: Container = Depends(get_app_container),
):
    """Get all tickets for a customer from paid bookings."""
    query = GetPurchasedTicketsQuery(customer_id=customer_id)
    result = container.get_purchased_tickets_handler().handle(query)
    return {
        "customer_id": result.customer_id,
        "tickets": [
            {
                "ticket_code": t.ticket_code,
                "event_id": t.event_id,
                "event_name": t.event_name,
                "ticket_category": t.ticket_category,
                "status": t.status,
            }
            for t in result.tickets
        ],
    }


# ── US13 / US14: Check In Ticket ─────────────────────────────────────────────

@router.post(
    "/tickets/check-in",
    response_model=CheckInResponse,
    summary="US13 - Check In Ticket / US14 - Reject Invalid Check-in",
)
def check_in_ticket(
    request: CheckInTicketRequest,
    container: Container = Depends(get_app_container),
):
    """
    Check in a ticket at the event entrance.
    Returns 400 if ticket is invalid, already used, wrong event, or event cancelled.
    """
    try:
        command = CheckInTicketCommand(
            ticket_code=request.ticket_code,
            event_id=request.event_id,
        )
        container.get_check_in_ticket_handler().handle(command)
        return {"ticket_code": request.ticket_code, "message": "Check-in successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
