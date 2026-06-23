CREATE TABLE events (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL
);

CREATE TABLE bookings (
    id VARCHAR(50) PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL
);

CREATE TABLE refunds (
    id VARCHAR(50) PRIMARY KEY,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE ticket_categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quota INTEGER NOT NULL
);

CREATE TABLE tickets (
    id VARCHAR(50) PRIMARY KEY,
    ticket_code VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL
);