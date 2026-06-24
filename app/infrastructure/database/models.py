from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class EventModel(Base):
    __tablename__ = "events"
    
    event_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    
    # Relationships
    ticket_categories = relationship("TicketCategoryModel", back_populates="event", cascade="all, delete")
    bookings = relationship("BookingModel", back_populates="event", cascade="all, delete")

class TicketCategoryModel(Base):
    __tablename__ = "ticket_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(String, ForeignKey("events.event_id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quota = Column(Integer, nullable=False)
    sales_start_date = Column(DateTime, nullable=False)
    sales_end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    event = relationship("EventModel", back_populates="ticket_categories")

class BookingModel(Base):
    __tablename__ = "bookings"
    
    booking_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False)
    event_id = Column(String, ForeignKey("events.event_id"), nullable=False)
    ticket_category_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    payment_deadline = Column(DateTime, nullable=False)
    
    # Relationships
    event = relationship("EventModel", back_populates="bookings")
    tickets = relationship("TicketModel", back_populates="booking", cascade="all, delete")
    refund = relationship("RefundModel", back_populates="booking", uselist=False, cascade="all, delete")

class TicketModel(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_code = Column(String, unique=True, index=True, nullable=False)
    booking_id = Column(String, ForeignKey("bookings.booking_id"), nullable=False)
    event_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    
    # Relationships
    booking = relationship("BookingModel", back_populates="tickets")

class RefundModel(Base):
    __tablename__ = "refunds"
    
    refund_id = Column(String, primary_key=True, index=True)
    booking_id = Column(String, ForeignKey("bookings.booking_id"), unique=True, nullable=False)
    customer_id = Column(String, nullable=False)
    event_id = Column(String, nullable=False)
    refund_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    rejection_reason = Column(String, nullable=True)
    refund_deadline = Column(DateTime, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    payment_reference = Column(String, nullable=True)
    paid_out_at = Column(DateTime, nullable=True)
    
    # Relationships
    booking = relationship("BookingModel", back_populates="refund")
