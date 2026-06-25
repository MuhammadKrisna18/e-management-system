"""
Week 13 - Presentation Layer
FastAPI application entry point.

Run with:
    uvicorn app.api:app --reload --port 8000

Swagger UI: http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
"""
from fastapi import FastAPI

from app.presentation.api.event_api import router as event_router
from app.presentation.api.booking_api import router as booking_router
from app.presentation.api.refund_api import router as refund_router
from app.presentation.middleware.cors import add_cors_middleware
from app.presentation.middleware.error_handler import add_exception_handlers

app = FastAPI(
    title="Event Management System",
    description=(
        "Event Ticketing & Booking System — Week 13 Presentation Layer.\n\n"
        "## User Stories Covered\n"
        "- **US1** Create Event\n"
        "- **US2** Publish Event\n"
        "- **US3** Cancel Event\n"
        "- **US4** Create Ticket Category\n"
        "- **US5** Disable Ticket Category\n"
        "- **US6** View Available Events\n"
        "- **US7** View Event Details\n"
        "- **US8** Create Booking\n"
        "- **US10** Pay Booking\n"
        "- **US11** Expire Booking\n"
        "- **US12** View Purchased Tickets\n"
        "- **US13** Check In Ticket\n"
        "- **US14** Reject Invalid Check-in\n"
        "- **US15** Request / View Refunds\n"
        "- **US16** Approve Refund\n"
        "- **US17** Reject Refund\n"
        "- **US18** Mark Refund as Paid Out\n"
        "- **US19** View Event Sales Report\n"
        "- **US20** View Event Participants\n"
    ),
    version="1.0.0",
)

# Middleware
add_cors_middleware(app)
add_exception_handlers(app)

# Routers
app.include_router(event_router)
app.include_router(booking_router)
app.include_router(refund_router)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "Event Management System"}
