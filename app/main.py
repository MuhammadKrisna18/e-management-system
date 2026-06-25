from fastapi import FastAPI
import uvicorn

from app.presentation.api import event_api, booking_api, refund_api
from app.presentation.middleware.cors import add_cors_middleware
from app.presentation.middleware.error_handler import add_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(
        title="Event Ticketing & Booking System",
        description="REST API for Event Ticketing and Booking Management",
        version="1.0.0"
    )

    add_cors_middleware(app)
    add_exception_handlers(app)

    app.include_router(event_api.router)
    app.include_router(booking_api.router)
    app.include_router(refund_api.router)

    return app

app = create_app()

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Event Ticketing & Booking System API!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
