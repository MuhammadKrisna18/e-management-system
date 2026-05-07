# E-Management System
Event Ticketing & Booking System using Clean Architecture and Domain-Driven Design (DDD) by Krisna Putra & Arya Raka

---

# Week 8 — Project Structure

## Objectives

This week focuses on:
- Clean Architecture folder structure
- Initial business rules derived from user stories and acceptance criteria
- Initial domain model draft
- Initial ubiquitous language glossary

---

# Clean Architecture Folder Structure

```bash
E-MANAGEMENT-SYSTEM/
│
├── app/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── aggregates/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── events/
│   │   └── exceptions/
│   │
│   ├── application/
│   │   ├── commands/
│   │   ├── command_handlers/
│   │   ├── queries/
│   │   ├── query_handlers/
│   │   ├── dto/
│   │   └── interfaces/
│   │
│   ├── infrastructure/
│   │   ├── database/
│   │   ├── repositories/
│   │   ├── external_services/
│   │   └── migrations/
│   │
│   ├── presentation/
│   │   ├── api/
│   │   ├── controllers/
│   │   ├── schemas/
│   │   └── middleware/
│   │
│   ├── config/
│   └── main.py
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── integration/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# Initial Business Rules

## Event Rules
- Event end date cannot be earlier than start date
- Event capacity must be greater than zero
- Newly created event status must be `Draft`
- Only events with status `Draft` can be published
- Cancelled events cannot be published
- Published events must have at least one active ticket category
- Total ticket category quota cannot exceed event capacity

---

## Ticket Category Rules
- Ticket category must have:
  - Name
  - Price
  - Quota
  - Sales start date
  - Sales end date
- Ticket price cannot be negative
- Ticket quota must be greater than zero
- Ticket sales period must end before or on the event start date
- Disabled ticket categories cannot be purchased

---

## Booking Rules
- Booking can only be created for Published events
- Booking quantity must be greater than zero
- Booking quantity cannot exceed remaining quota
- Customer cannot have more than one active booking for the same event
- Newly created booking status must be `PendingPayment`
- Booking must have payment deadline

---

## Payment Rules
- Only bookings with status `PendingPayment` can be paid
- Booking cannot be paid after payment deadline
- Payment amount must equal total booking price
- Successful payment changes booking status to `Paid`

---

## Ticket Rules
- Each ticket must have unique ticket code
- Ticket statuses:
  - Active
  - CheckedIn
  - Cancelled
- Checked-in ticket cannot be checked in again

---

## Refund Rules
- Refund can only be requested for Paid bookings
- Refund cannot be requested if ticket already checked in
- Refund statuses:
  - Requested
  - Approved
  - Rejected
  - PaidOut
- Rejected refund must include rejection reason

---

# Initial Domain Model Draft

## Aggregates

### Event Aggregate
Root Aggregate:
- Event

Contains:
- TicketCategory

Responsibilities:
- Create Event
- Publish Event
- Cancel Event
- Validate Event Capacity

---

### Booking Aggregate
Root Aggregate:
- Booking

Contains:
- Ticket

Responsibilities:
- Reserve Tickets
- Calculate Total Price
- Handle Payment
- Expire Booking

---

### Refund Aggregate
Root Aggregate:
- Refund

Responsibilities:
- Request Refund
- Approve Refund
- Reject Refund
- Mark Refund as PaidOut

---

# Main Entities

| Entity | Description |
|---|---|
| Event | Represents an event |
| TicketCategory | Represents ticket type |
| Booking | Represents customer booking |
| Ticket | Represents generated ticket |
| Refund | Represents refund request |
| Customer | Represents customer |
| Organizer | Represents event organizer |

---

# Value Objects

| Value Object | Description |
|---|---|
| Money | Represents amount and currency |
| EventSchedule | Represents event start and end date |
| TicketCode | Unique ticket identifier |
| PaymentDeadline | Booking expiration deadline |

---

# Initial Domain Events

| Domain Event | Description |
|---|---|
| EventCreated | Triggered after event creation |
| EventPublished | Triggered after event published |
| EventCancelled | Triggered after event cancelled |
| TicketCategoryCreated | Triggered after ticket category created |
| TicketCategoryDisabled | Triggered after ticket category disabled |
| TicketReserved | Triggered after booking created |
| BookingPaid | Triggered after successful payment |
| BookingExpired | Triggered after booking expired |
| TicketCheckedIn | Triggered after successful check-in |
| RefundRequested | Triggered after refund requested |
| RefundApproved | Triggered after refund approved |
| RefundRejected | Triggered after refund rejected |
| RefundPaidOut | Triggered after refund payout completed |

---

# Ubiquitous Language Glossary

| Term | Meaning |
|---|---|
| Event | An activity organized by Event Organizer |
| Event Organizer | User who creates and manages events |
| Customer | User who books and purchases tickets |
| Gate Officer | User who validates tickets |
| Ticket Category | Ticket type such as VIP or Regular |
| Booking | Temporary ticket reservation |
| PendingPayment | Waiting for customer payment |
| Paid | Booking payment completed |
| Expired | Payment deadline passed |
| Ticket | Proof of attendance |
| Ticket Code | Unique ticket identifier |
| Check-in | Ticket validation process |
| Refund | Returning money to customer |
| Money | Value object for amount and currency |
| Sales Period | Ticket selling period |
| Payment Deadline | Deadline for booking payment |

---

# Technology Stack

| Technology | Usage |
|---|---|
| Python | Main Programming Language |
| FastAPI | Backend REST API Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database Migration |
| Pytest | Unit Testing |

---

# How to Run the Project

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows
```bash
venv\Scripts\activate
```

### Linux / Mac
```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

