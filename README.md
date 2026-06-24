# E-Management System

Sistem Event Ticketing & Booking menggunakan Clean Architecture dan Domain-Driven Design (DDD)

Disusun oleh:
- Krisna Putra
- Arya Raka

---

# Deskripsi Project

E-Management System merupakan sistem pemesanan dan pengelolaan tiket event yang dibangun menggunakan pendekatan:

- Clean Architecture
- Domain-Driven Design (DDD)

Sistem ini memungkinkan:
- Event Organizer membuat dan mengelola event
- Customer memesan dan membeli tiket
- Gate Officer melakukan validasi tiket
- System Admin mengelola proses refund

Project ini dikembangkan sebagai studi kasus mata kuliah:
**Konstruksi Perangkat Lunak (Software Construction)**

---

# Project Progress

- [x] **Week 8:** Project Structure (Clean Architecture, DDD, Ubiquitous Language)
- [x] **Week 9-10:** Domain Layer & Unit Tests (Aggregates, Entities, Repositories, Tests)
- [x] **Week 11:** Application Layer (Commands, Queries, DTOs, Handlers)
- [x] **Week 12:** Infrastructure Layer (PostgreSQL, Alembic, Repositories, Mock Services)
- [ ] **Week 13:** Presentation Layer (FastAPI Controllers, Endpoints, Integrations)

---

# Implemented Features (User Stories)
- [x] **US 1**: Create Event
- [x] **US 2**: Publish Event
- [x] **US 3**: Cancel Event
- [x] **US 4**: Create Ticket Category
- [x] **US 5**: Disable Ticket Category
- [x] **US 6**: View Available Events
- [x] **US 7**: View Event Details
- [x] **US 8**: Create Ticket Booking
- [x] **US 9**: Calculate Booking Total Price
- [x] **US 10**: Pay Booking
- [x] **US 11**: Expire Booking
- [x] **US 12**: View Purchased Tickets
- [x] **US 13**: Check In Ticket
- [x] **US 14**: Reject Invalid Ticket Check-in
- [x] **US 15**: Request Refund
- [x] **US 16**: Approve Refund
- [x] **US 17**: Reject Refund
- [x] **US 18**: Mark Refund as Paid Out
- [x] **US 19**: View Event Sales Report
- [x] **US 20**: View Event Participants

---

# Tujuan Project

Project ini bertujuan untuk:
- Menerapkan Clean Architecture
- Menerapkan DDD Tactical Pattern
- Memisahkan domain logic dari framework
- Membuat software yang maintainable dan scalable
- Mengimplementasikan business rules berdasarkan user stories

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

# Business Rules

## Event Rules

- Event end date tidak boleh lebih awal dari start date
- Kapasitas event harus lebih besar dari 0
- Status default event baru adalah `Draft`
- Event hanya dapat dipublish jika memiliki minimal satu ticket category aktif
- Event dengan status `Cancelled` tidak dapat dipublish
- Total quota ticket category tidak boleh melebihi kapasitas event

---

## Ticket Category Rules

- Ticket category harus memiliki:
  - Name
  - Price
  - Quota
  - Sales Start Date
  - Sales End Date
- Harga tiket tidak boleh negatif
- Quota tiket harus lebih besar dari 0
- Masa penjualan tiket harus selesai sebelum event dimulai
- Ticket category yang nonaktif tidak dapat dibeli

---

## Booking Rules

- Booking hanya dapat dibuat untuk event dengan status `Published`
- Quantity booking harus lebih besar dari 0
- Quantity booking tidak boleh melebihi quota tersisa
- Customer tidak dapat memiliki lebih dari satu booking aktif untuk event yang sama
- Status default booking baru adalah `PendingPayment`
- Booking memiliki payment deadline

---

## Payment Rules

- Hanya booking dengan status `PendingPayment` yang dapat dibayar
- Booking tidak dapat dibayar setelah payment deadline
- Jumlah pembayaran harus sesuai total booking
- Pembayaran berhasil mengubah status booking menjadi `Paid`

---

## Ticket Rules

- Setiap ticket memiliki kode unik
- Status ticket:
  - Active
  - CheckedIn
  - Cancelled
- Ticket yang sudah check-in tidak dapat digunakan kembali

---

## Refund Rules

- Refund hanya dapat diminta untuk booking dengan status `Paid`
- Refund tidak dapat dilakukan jika ticket sudah check-in
- Status refund:
  - Requested
  - Approved
  - Rejected
  - PaidOut
- Refund yang ditolak wajib memiliki alasan penolakan

---

# Domain Model

## Aggregates

### Event Aggregate

Aggregate Root:
- Event

Entity di dalam aggregate:
- TicketCategory

Responsibilities:
- Create Event
- Publish Event
- Cancel Event
- Validate Event Capacity

---

### Booking Aggregate

Aggregate Root:
- Booking

Entity di dalam aggregate:
- Ticket

Responsibilities:
- Reserve Ticket
- Calculate Total Price
- Handle Payment
- Expire Booking

---

### Refund Aggregate

Aggregate Root:
- Refund

Responsibilities:
- Request Refund
- Approve Refund
- Reject Refund
- Mark Refund as PaidOut

---

# Main Entities

| Entity | Deskripsi |
|---|---|
| Event | Merepresentasikan event |
| TicketCategory | Merepresentasikan jenis tiket |
| Booking | Merepresentasikan booking customer |
| Ticket | Merepresentasikan tiket |
| Refund | Merepresentasikan refund |
| Customer | Merepresentasikan customer |
| Organizer | Merepresentasikan event organizer |

---

# Value Objects

| Value Object | Deskripsi |
|---|---|
| Money | Representasi nominal uang |
| EventSchedule | Representasi jadwal event |
| TicketCode | Kode unik ticket |
| PaymentDeadline | Deadline pembayaran booking |

---

# Domain Events

| Domain Event | Deskripsi |
|---|---|
| EventCreated | Event berhasil dibuat |
| EventPublished | Event berhasil dipublish |
| EventCancelled | Event dibatalkan |
| TicketCategoryCreated | Ticket category dibuat |
| TicketCategoryDisabled | Ticket category dinonaktifkan |
| TicketReserved | Ticket berhasil direserve |
| BookingPaid | Booking berhasil dibayar |
| BookingExpired | Booking expired |
| TicketCheckedIn | Ticket berhasil check-in |
| RefundRequested | Refund diminta |
| RefundApproved | Refund disetujui |
| RefundRejected | Refund ditolak |
| RefundPaidOut | Refund berhasil dibayar |

---

# Repository Interfaces

Repository interface digunakan untuk memisahkan domain layer dari implementation database.

Repository yang digunakan:
- EventRepository
- BookingRepository
- RefundRepository

---

# Domain Services

Domain service digunakan untuk business logic yang tidak cocok ditempatkan pada entity.

Domain service yang digunakan:
- PricingService

Responsibilities:
- Menghitung total harga booking
- Menambahkan service fee
- Menghasilkan value object `Money`

---

# Application Service Interfaces

Interface external service yang direncanakan:

| Interface | Fungsi |
|---|---|
| PaymentGatewayInterface | Memproses pembayaran |
| NotificationServiceInterface | Mengirim notifikasi |
| RefundPaymentServiceInterface | Memproses refund payout |

---

# Ubiquitous Language Glossary

| Term | Meaning |
|---|---|
| Event | An activity organized by an Event Organizer and attended by customers. |
| Event Organizer | A user who creates and manages events. |
| Customer | A user who books and purchases tickets. |
| Gate Officer | A user who validates tickets during event check-in. |
| Ticket Category | A type of ticket, such as Regular, VIP, or Early Bird. |
| Quota | The maximum number of tickets available in a ticket category. |
| Booking | A temporary reservation before payment is completed. |
| Pending Payment | A booking status indicating that payment has not been completed. |
| Paid | A booking status indicating that payment has been completed. |
| Expired | A booking status indicating that the payment deadline has passed. |
| Ticket | Proof of attendance generated after a booking is paid. |
| Ticket Code | A unique code used to identify and validate a ticket. |
| Check-in | The process of validating a ticket when a participant enters the event venue. |
| Refund | The process of returning money to a customer. |
| Money | A value object representing an amount and currency. |
| Sales Period | The period during which a ticket category can be purchased. |
| Payment Deadline | The deadline for completing payment after a booking is created. |

---