"""
Application Entry Point

Demonstrates complete workflow of the Event Ticketing & Booking System.
Shows how to use commands, queries, handlers, and the dependency container.
"""

from datetime import datetime, timedelta
import uuid

from app.infrastructure.config.container import get_container

from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.entities.booking import Booking

from app.application.commands.create_event_command import CreateEventCommand
from app.application.commands.publish_event_command import PublishEventCommand
from app.application.commands.create_booking_command import CreateBookingCommand
from app.application.commands.request_refund_command import RequestRefundCommand
from app.application.commands.approve_refund_command import ApproveRefundCommand
from app.application.commands.mark_refund_payout_command import MarkRefundPayoutCommand

from app.application.queries.get_available_events_query import GetAvailableEventsQuery
from app.application.queries.refund_queries import GetCustomerRefundsQuery
from app.application.queries.event_queries import GetEventSalesReportQuery


def main():
    """
    Main application demonstration.
    
    Shows:
    1. Creating and publishing an event
    2. Browsing available events
    3. Creating and paying for bookings
    4. Requesting and approving refunds
    5. Viewing reports
    """
    
    print("=" * 80)
    print("Event Ticketing & Booking System - Week 12 Infrastructure Demo")
    print("=" * 80)
    print()

    # Get dependency container
    container = get_container()

    # ==================== STEP 1: Create Event ====================
    print("STEP 1: Creating Event")
    print("-" * 80)

    create_event_handler = container.get_create_event_handler()
    
    event_cmd = CreateEventCommand(
        name="Python Conference 2024",
        description="Annual Python developer conference",
        start_date=datetime.now() + timedelta(days=30),
        end_date=datetime.now() + timedelta(days=31),
        location="Jakarta Convention Center",
        capacity=500,
        organizer_id="ORG001"
    )

    event_agg = create_event_handler.handle(event_cmd)
    event_id = event_agg.event.event_id
    
    print(f"✓ Event created: {event_agg.event.name}")
    print(f"  Event ID: {event_id}")
    print(f"  Status: {event_agg.event.status}")
    print()

    # ==================== STEP 2: Add Ticket Categories ====================
    print("STEP 2: Adding Ticket Categories")
    print("-" * 80)

    # Add VIP ticket category
    vip_category = TicketCategory(
        name="VIP",
        price=1500000.0,
        quota=100,
        sales_start=datetime.now(),
        sales_end=datetime.now() + timedelta(days=25),
        is_active=True
    )
    event_agg.add_ticket_category(vip_category)
    
    # Add Regular ticket category
    regular_category = TicketCategory(
        name="Regular",
        price=750000.0,
        quota=300,
        sales_start=datetime.now(),
        sales_end=datetime.now() + timedelta(days=25),
        is_active=True
    )
    event_agg.add_ticket_category(regular_category)

    print(f"✓ Added ticket categories:")
    for cat in event_agg.ticket_categories:
        print(f"  - {cat.name}: Rp {cat.price:,} (Quota: {cat.quota})")
    print()

    # Save event with categories
    event_id = container.event_repository.save(event_agg)

    # ==================== STEP 3: Publish Event ====================
    print("STEP 3: Publishing Event")
    print("-" * 80)

    publish_handler = container.get_publish_event_handler()
    
    publish_cmd = PublishEventCommand(event_id=event_id)
    published_event = publish_handler.handle(publish_cmd)
    
    print(f"✓ Event published successfully")
    print(f"  Status: {published_event.event.status}")
    print()

    # ==================== STEP 4: Browse Available Events ====================
    print("STEP 4: Browsing Available Events")
    print("-" * 80)

    get_events_handler = container.get_available_events_handler()
    query = GetAvailableEventsQuery()
    available_events = get_events_handler.handle(query)
    
    print(f"✓ Found {len(available_events)} published events:")
    for event in available_events:
        print(f"  - {event.name}")
        print(f"    Location: {event.location}")
        print(f"    Date: {event.start_date.strftime('%Y-%m-%d')}")
    print()

    # ==================== STEP 5: Create Booking ====================
    print("STEP 5: Creating Booking")
    print("-" * 80)

    create_booking_handler = container.get_create_booking_handler()
    
    customer_id = "CUST001"
    booking_cmd = CreateBookingCommand(
        customer_id=customer_id,
        event_id=event_id,
        ticket_category_name="VIP",
        quantity=2
    )

    booking_agg = create_booking_handler.handle(booking_cmd)
    booking_id = booking_agg.booking.booking_id
    
    print(f"✓ Booking created:")
    print(f"  Booking ID: {booking_id}")
    print(f"  Customer ID: {customer_id}")
    print(f"  Status: {booking_agg.booking.status}")
    print(f"  Payment deadline: {booking_agg.booking.payment_deadline}")
    print()

    # Save booking
    container.booking_repository.save(booking_agg)

    # ==================== STEP 6: Pay Booking ====================
    print("STEP 6: Paying for Booking")
    print("-" * 80)

    pay_handler = container.get_pay_booking_handler()
    from app.application.commands.pay_booking_command import PayBookingCommand
    
    pay_cmd = PayBookingCommand(
        booking_id=booking_id,
        payment_amount=3000000.0
    )

    paid_booking = pay_handler.handle(pay_cmd)
    
    print(f"✓ Booking paid successfully")
    print(f"  Status: {paid_booking.booking.status}")
    print(f"  Payment Reference: {paid_booking.booking.payment_reference}")
    print()

    # ==================== STEP 7: Request Refund ====================
    print("STEP 7: Requesting Refund")
    print("-" * 80)

    request_refund_handler = container.get_request_refund_handler()
    
    refund_cmd = RequestRefundCommand(booking_id=booking_id)
    refund_id = request_refund_handler.handle(refund_cmd)
    
    print(f"✓ Refund requested:")
    print(f"  Refund ID: {refund_id}")
    print(f"  Booking ID: {booking_id}")
    print()

    # ==================== STEP 8: Approve Refund ====================
    print("STEP 8: Approving Refund")
    print("-" * 80)

    approve_handler = container.get_approve_refund_handler()
    
    approve_cmd = ApproveRefundCommand(refund_id=refund_id)
    result = approve_handler.handle(approve_cmd)
    
    print(f"✓ Refund approved:")
    print(f"  Refund ID: {result['refund_id']}")
    print(f"  Status: {result['status']}")
    print()

    # ==================== STEP 9: Mark Refund as Paid Out ====================
    print("STEP 9: Marking Refund as Paid Out")
    print("-" * 80)

    payout_handler = container.get_mark_refund_payout_handler()
    
    payout_cmd = MarkRefundPayoutCommand(
        refund_id=refund_id,
        payment_reference="TXN202400123456"
    )
    result = payout_handler.handle(payout_cmd)
    
    print(f"✓ Refund paid out:")
    print(f"  Status: {result['status']}")
    print(f"  Payment Reference: {result['payment_reference']}")
    print()

    # ==================== STEP 10: View Sales Report ====================
    print("STEP 10: Viewing Event Sales Report")
    print("-" * 80)

    sales_handler = container.get_event_sales_report_handler()
    
    report_query = GetEventSalesReportQuery(event_id=event_id)
    report = sales_handler.handle(report_query)
    
    print(f"✓ Event Sales Report:")
    print(f"  Event: {report.event_name}")
    print(f"  Total Revenue: Rp {report.total_revenue:,.2f}")
    print(f"  Booking Stats:")
    print(f"    - Pending: {report.booking_stats.pending_payment}")
    print(f"    - Paid: {report.booking_stats.paid}")
    print(f"    - Expired: {report.booking_stats.expired}")
    print(f"    - Refunded: {report.booking_stats.refunded}")
    print()

    # ==================== Summary ====================
    print("=" * 80)
    print("Demo Completed Successfully!")
    print("=" * 80)
    print()
    print("Summary of Implemented Features:")
    print("✓ Create Event (User Story 1)")
    print("✓ Publish Event (User Story 2)")
    print("✓ Create Ticket Categories (User Story 4)")
    print("✓ View Available Events (User Story 6)")
    print("✓ Create Ticket Booking (User Story 8)")
    print("✓ Pay Booking (User Story 10)")
    print("✓ Request Refund (User Story 15)")
    print("✓ Approve Refund (User Story 16)")
    print("✓ Mark Refund as Paid Out (User Story 18)")
    print("✓ View Event Sales Report (User Story 19)")
    print()
    print("Infrastructure Components:")
    print("✓ Clean Architecture Layers (Domain, Application, Infrastructure)")
    print("✓ DDD Tactical Patterns (Aggregates, Entities, Value Objects)")
    print("✓ CQRS Pattern (Commands & Queries)")
    print("✓ Repository Pattern (In-Memory Implementation)")
    print("✓ Dependency Injection Container")
    print("✓ Value Objects with Enums (RefundStatus, BookingStatus, TicketStatus)")
    print()


if __name__ == "__main__":
    main()
