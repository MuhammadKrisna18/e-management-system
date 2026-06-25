import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DomainException,
    ValidationException,
    BookingNotFoundException,
    EventNotFoundException,
    RefundNotFoundException,
    TicketException,
    InvalidBookingStatusException,
    InvalidRefundStatusException,
    InvalidEventStatusException,
)

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""

    @app.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException):
        return JSONResponse(
            status_code=422,
            content={"error": "Validation Error", "detail": str(exc)},
        )

    @app.exception_handler(BookingNotFoundException)
    async def booking_not_found_handler(request: Request, exc: BookingNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"error": "Booking Not Found", "detail": str(exc)},
        )

    @app.exception_handler(EventNotFoundException)
    async def event_not_found_handler(request: Request, exc: EventNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"error": "Event Not Found", "detail": str(exc)},
        )

    @app.exception_handler(RefundNotFoundException)
    async def refund_not_found_handler(request: Request, exc: RefundNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"error": "Refund Not Found", "detail": str(exc)},
        )

    @app.exception_handler(TicketException)
    async def ticket_exception_handler(request: Request, exc: TicketException):
        return JSONResponse(
            status_code=422,
            content={"error": "Ticket Error", "detail": str(exc)},
        )

    @app.exception_handler(InvalidBookingStatusException)
    async def invalid_booking_status_handler(request: Request, exc: InvalidBookingStatusException):
        return JSONResponse(
            status_code=422,
            content={"error": "Invalid Booking Status", "detail": str(exc)},
        )

    @app.exception_handler(InvalidRefundStatusException)
    async def invalid_refund_status_handler(request: Request, exc: InvalidRefundStatusException):
        return JSONResponse(
            status_code=422,
            content={"error": "Invalid Refund Status", "detail": str(exc)},
        )

    @app.exception_handler(InvalidEventStatusException)
    async def invalid_event_status_handler(request: Request, exc: InvalidEventStatusException):
        return JSONResponse(
            status_code=422,
            content={"error": "Invalid Event Status", "detail": str(exc)},
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=422,
            content={"error": "Business Rule Violation", "detail": str(exc)},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={"error": "Bad Request", "detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error("Unexpected error: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": "An unexpected error occurred."},
        )
