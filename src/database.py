from __future__ import annotations

import sqlite3
from pathlib import Path

from src.config import database_path


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    date_of_birth TEXT,
    preferred_contact TEXT CHECK (preferred_contact IN ('phone', 'email', 'text')),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    vin TEXT UNIQUE,
    license_plate TEXT UNIQUE,
    color TEXT,
    mileage INTEGER DEFAULT 0,
    engine_type TEXT,
    transmission TEXT,
    fuel_type TEXT,
    last_service_date TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    hire_date TEXT,
    salary_cents INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_person TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    website TEXT,
    account_number TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS service_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    complaint TEXT NOT NULL,
    diagnosis TEXT,
    estimate_cents INTEGER NOT NULL DEFAULT 0,
    opened_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_number TEXT NOT NULL UNIQUE,
    name TEXT,
    description TEXT NOT NULL,
    category TEXT,
    supplier_id INTEGER,
    quantity_on_hand INTEGER NOT NULL DEFAULT 0,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    reorder_point INTEGER NOT NULL DEFAULT 0,
    min_stock_level INTEGER NOT NULL DEFAULT 5,
    unit_cost_cents INTEGER NOT NULL DEFAULT 0,
    retail_price_cents INTEGER NOT NULL DEFAULT 0,
    location_bin TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    supplier TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

CREATE TABLE IF NOT EXISTS service_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    default_hours REAL,
    base_price_cents INTEGER,
    category TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    customer_id INTEGER,
    employee_id INTEGER,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'in_progress', 'completed', 'invoiced', 'cancelled')),
    start_date TEXT,
    completion_date TEXT,
    total_labor_hours REAL,
    labor_rate_cents INTEGER NOT NULL DEFAULT 12500,
    total_parts_cost_cents INTEGER NOT NULL DEFAULT 0,
    total_labor_cost_cents INTEGER NOT NULL DEFAULT 0,
    tax_amount_cents INTEGER NOT NULL DEFAULT 0,
    grand_total_cents INTEGER,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS job_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    service_type_id INTEGER,
    hours_spent REAL,
    price_charged_cents INTEGER,
    notes TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (service_type_id) REFERENCES service_types(id)
);

CREATE TABLE IF NOT EXISTS job_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    part_id INTEGER,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_cost_at_time_cents INTEGER NOT NULL,
    total_cost_cents INTEGER GENERATED ALWAYS AS (quantity * unit_cost_at_time_cents) STORED,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    vehicle_id INTEGER,
    job_id INTEGER,
    technician_id INTEGER,
    scheduled_start TEXT NOT NULL,
    scheduled_end TEXT,
    status TEXT NOT NULL DEFAULT 'scheduled',
    bay_number TEXT,
    service_duration_hours REAL NOT NULL DEFAULT 2.0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (technician_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    customer_id INTEGER,
    invoice_number TEXT NOT NULL UNIQUE,
    issue_date TEXT NOT NULL DEFAULT CURRENT_DATE,
    due_date TEXT,
    status TEXT NOT NULL DEFAULT 'unpaid',
    subtotal_cents INTEGER,
    tax_amount_cents INTEGER,
    total_amount_cents INTEGER NOT NULL,
    amount_paid_cents INTEGER NOT NULL DEFAULT 0,
    payment_method TEXT,
    notes TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE INDEX IF NOT EXISTS idx_vehicles_customer_id ON vehicles(customer_id);
CREATE INDEX IF NOT EXISTS idx_service_orders_vehicle_id ON service_orders(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_service_orders_status ON service_orders(status);
"""


POST_MIGRATION_SCHEMA = """
CREATE INDEX IF NOT EXISTS idx_jobs_vehicle_id ON jobs(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_parts_category ON parts(category);
CREATE INDEX IF NOT EXISTS idx_appointments_scheduled_start ON appointments(scheduled_start);
CREATE INDEX IF NOT EXISTS idx_appointments_time_bay
    ON appointments(scheduled_start, scheduled_end, bay_number);
CREATE INDEX IF NOT EXISTS idx_appointments_technician_id ON appointments(technician_id);

CREATE TRIGGER IF NOT EXISTS update_customers_timestamp
AFTER UPDATE ON customers
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE customers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_vehicles_timestamp
AFTER UPDATE ON vehicles
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE vehicles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_parts_timestamp
AFTER UPDATE ON parts
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE parts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_jobs_timestamp
AFTER UPDATE ON jobs
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE jobs SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
"""


MIGRATIONS: dict[str, list[tuple[str, str]]] = {
    "customers": [
        ("address", "ALTER TABLE customers ADD COLUMN address TEXT"),
        ("city", "ALTER TABLE customers ADD COLUMN city TEXT"),
        ("state", "ALTER TABLE customers ADD COLUMN state TEXT"),
        ("zip_code", "ALTER TABLE customers ADD COLUMN zip_code TEXT"),
        ("date_of_birth", "ALTER TABLE customers ADD COLUMN date_of_birth TEXT"),
        ("preferred_contact", "ALTER TABLE customers ADD COLUMN preferred_contact TEXT"),
        ("updated_at", "ALTER TABLE customers ADD COLUMN updated_at TEXT"),
    ],
    "vehicles": [
        ("color", "ALTER TABLE vehicles ADD COLUMN color TEXT"),
        ("engine_type", "ALTER TABLE vehicles ADD COLUMN engine_type TEXT"),
        ("transmission", "ALTER TABLE vehicles ADD COLUMN transmission TEXT"),
        ("fuel_type", "ALTER TABLE vehicles ADD COLUMN fuel_type TEXT"),
        ("last_service_date", "ALTER TABLE vehicles ADD COLUMN last_service_date TEXT"),
        ("notes", "ALTER TABLE vehicles ADD COLUMN notes TEXT"),
        ("updated_at", "ALTER TABLE vehicles ADD COLUMN updated_at TEXT"),
    ],
    "parts": [
        ("name", "ALTER TABLE parts ADD COLUMN name TEXT"),
        ("category", "ALTER TABLE parts ADD COLUMN category TEXT"),
        ("supplier_id", "ALTER TABLE parts ADD COLUMN supplier_id INTEGER REFERENCES suppliers(id)"),
        ("stock_quantity", "ALTER TABLE parts ADD COLUMN stock_quantity INTEGER NOT NULL DEFAULT 0"),
        ("min_stock_level", "ALTER TABLE parts ADD COLUMN min_stock_level INTEGER NOT NULL DEFAULT 5"),
        ("retail_price_cents", "ALTER TABLE parts ADD COLUMN retail_price_cents INTEGER NOT NULL DEFAULT 0"),
        ("location_bin", "ALTER TABLE parts ADD COLUMN location_bin TEXT"),
        ("is_active", "ALTER TABLE parts ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1"),
        ("created_at", "ALTER TABLE parts ADD COLUMN created_at TEXT"),
        ("updated_at", "ALTER TABLE parts ADD COLUMN updated_at TEXT"),
    ],
    "appointments": [
        ("technician_id", "ALTER TABLE appointments ADD COLUMN technician_id INTEGER REFERENCES employees(id)"),
        (
            "service_duration_hours",
            "ALTER TABLE appointments ADD COLUMN service_duration_hours REAL NOT NULL DEFAULT 2.0",
        ),
    ],
}


def connect(path: Path | None = None) -> sqlite3.Connection:
    db_path = path or database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _columns(connection: sqlite3.Connection, table_name: str) -> set[str]:
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"] for row in rows}


def _apply_migrations(connection: sqlite3.Connection) -> None:
    for table_name, migrations in MIGRATIONS.items():
        existing_columns = _columns(connection, table_name)
        for column_name, statement in migrations:
            if column_name not in existing_columns:
                connection.execute(statement)
                existing_columns.add(column_name)


def initialize(path: Path | None = None) -> Path:
    db_path = path or database_path()
    with connect(db_path) as connection:
        connection.executescript(SCHEMA)
        _apply_migrations(connection)
        connection.executescript(POST_MIGRATION_SCHEMA)
    return db_path
