from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.config.container import get_container, Container
from app.presentation.schemas.booking_schemas import (
    CreateBookingRequest,
    PayBookingRequest,
    BookingResponse
)
from app.application.commands.create_booking_command import CreateBookingCommand
from app.application.commands.pay_booking_command import PayBookingCommand

router = APIRouter(prefix="/bookings", tags=["Bookings"])

def get_app_container() -> Container:
    return get_container()

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    request: CreateBookingRequest,
    container: Container = Depends(get_app_container)
):
    try:
        command = CreateBookingCommand(
            customer_id=request.customer_id,
            event_id=request.event_id,
            ticket_category_name=request.ticket_category_name,
            quantity=request.quantity
        )
        handler = container.get_create_booking_handler()
        booking_aggregate = handler.handle(command)
        
        return booking_aggregate.booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{booking_id}/pay", response_model=BookingResponse)
def pay_booking(
    booking_id: str,
    request: PayBookingRequest,
    container: Container = Depends(get_app_container)
):
    try:
        command = PayBookingCommand(
            booking_id=booking_id,
            payment_amount=request.payment_amount
        )
        handler = container.get_pay_booking_handler()
        booking_aggregate = handler.handle(command)
        return booking_aggregate.booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
