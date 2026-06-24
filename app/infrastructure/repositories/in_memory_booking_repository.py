"""In-Memory Booking Repository Implementation"""
from datetime import datetime
from typing import Dict, List, Optional
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.value_objects.booking_status import BookingStatus


class InMemoryBookingRepository(BookingRepository):
    """
    In-memory implementation of BookingRepository.
    Stores BookingAggregates in memory for development and testing.
    """

    def __init__(self):
        """Initialize in-memory storage."""
        self._bookings: Dict[str, BookingAggregate] = {}
        self._booking_counter = 0

    def save(self, booking_aggregate: BookingAggregate) -> str:
        """
        Save booking aggregate.
        
        Args:
            booking_aggregate: BookingAggregate to save
            
        Returns:
            str: Booking ID
        """
        if not booking_aggregate.booking.booking_id:
            self._booking_counter += 1
            booking_aggregate.booking.booking_id = f"BKG{self._booking_counter:04d}"
            
        booking_id = booking_aggregate.booking.booking_id
        self._bookings[booking_id] = booking_aggregate
        return booking_id

    def get_by_id(self, booking_id: str) -> Optional[BookingAggregate]:
        """
        Retrieve booking by ID.
        
        Args:
            booking_id: Booking identifier
            
        Returns:
            BookingAggregate or None if not found
        """
        return self._bookings.get(booking_id)

    def find_by_customer_and_event(
        self, customer_id: str, event_id: str
    ) -> Optional[BookingAggregate]:
        """
        Find active booking by customer and event.
        
        Args:
            customer_id: Customer identifier
            event_id: Event identifier
            
        Returns:
            BookingAggregate or None if not found
        """
        for booking_agg in self._bookings.values():
            booking = booking_agg.booking
            if (booking.customer_id == customer_id 
                and booking.event_id == event_id
                and booking.status == BookingStatus.PENDING_PAYMENT):
                return booking_agg
        return None

    def find_by_customer(self, customer_id: str) -> List[BookingAggregate]:
        """
        Find all bookings by customer.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            List of BookingAggregate instances
        """
        return [
            agg for agg in self._bookings.values()
            if agg.booking.customer_id == customer_id
        ]

    def find_expired_pending(self) -> List[BookingAggregate]:
        """
        Find expired pending bookings.
        
        Returns:
            List of expired pending BookingAggregate instances
        """
        expired = []
        current_time = datetime.now()
        
        for booking_agg in self._bookings.values():
            booking = booking_agg.booking
            if (booking.status == BookingStatus.PENDING_PAYMENT
                and booking.is_payment_deadline_passed(current_time)):
                expired.append(booking_agg)
        
        return expired

    def find_all(self) -> List[BookingAggregate]:
        """
        Find all bookings.
        
        Returns:
            List of BookingAggregate instances
        """
        return list(self._bookings.values())

    def find_active_by_customer_and_event(
        self,
        customer_id: str,
        event_id: str
    ) -> List[BookingAggregate]:
        active_bookings = []
        for agg in self._bookings.values():
            booking = agg.booking
            if (booking.customer_id == customer_id and 
                booking.event_id == event_id and 
                booking.status in ["PendingPayment", "Paid"]):
                active_bookings.append(agg)
        return active_bookings

    def get_booked_quantity_for_category(
        self,
        event_id: str,
        ticket_category_name: str
    ) -> int:
        booked_qty = 0
        for agg in self._bookings.values():
            booking = agg.booking
            if (booking.event_id == event_id and 
                booking.ticket_category_name == ticket_category_name and
                booking.status in ["PendingPayment", "Paid"]):
                booked_qty += booking.quantity
        return booked_qty

    def delete(self, booking_id: str) -> bool:
        """
        Delete booking by ID.
        
        Args:
            booking_id: Booking identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        if booking_id in self._bookings:
            del self._bookings[booking_id]
            return True
        return False
