from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.infrastructure.config.container import get_container, Container
from app.presentation.schemas.booking_schemas import (
    CreateBookingRequest,
    PayBookingRequest,
    BookingResponse,
    PurchasedTicketsResponse,
    CalculatePriceRequest,
    CalculatePriceResponse
)
from app.application.commands.create_booking_command import CreateBookingCommand
from app.application.commands.pay_booking_command import PayBookingCommand
from app.application.commands.expire_booking_command import ExpireBookingCommand
from app.application.queries.ticket_queries import GetPurchasedTicketsQuery
from app.domain.services.pricing_service import PricingService

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
            amount=request.payment_amount
        )
        handler = container.get_pay_booking_handler()
        booking_aggregate = handler.handle(command)
        return booking_aggregate.booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-tickets/{customer_id}", response_model=PurchasedTicketsResponse)
def get_my_tickets(
    customer_id: str,
    container: Container = Depends(get_app_container)
):
    try:
        query = GetPurchasedTicketsQuery(customer_id=customer_id)
        handler = container.get_purchased_tickets_handler()
        return handler.handle(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{booking_id}/expire", response_model=BookingResponse)
def expire_booking(
    booking_id: str,
    container: Container = Depends(get_app_container)
):
    try:
        command = ExpireBookingCommand(booking_id=booking_id)
        handler = container.get_expire_booking_handler()
        booking_aggregate = handler.handle(command)
        return booking_aggregate.booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/calculate-price", response_model=CalculatePriceResponse)
def calculate_price(
    request: CalculatePriceRequest,
    container: Container = Depends(get_app_container)
):
    try:
        event_repo = container.event_repository
        event_agg = event_repo.get_by_id(request.event_id)
        if not event_agg:
            raise ValueError(f"Event {request.event_id} not found")
            
        category = next((cat for cat in event_agg.ticket_categories if cat.name == request.ticket_category_name), None)
        if not category:
             raise ValueError(f"Ticket category {request.ticket_category_name} not found")
             
        total_price = PricingService.calculate_total_price(category.price, request.quantity)
        
        return CalculatePriceResponse(total_price=total_price.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
