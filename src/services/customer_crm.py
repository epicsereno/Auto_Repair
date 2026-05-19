from __future__ import annotations

import sqlite3

from src.models import Customer, Vehicle


def add_customer(connection: sqlite3.Connection, customer: Customer) -> int:
    cursor = connection.execute(
        """
        INSERT INTO customers (first_name, last_name, phone, email, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (customer.first_name, customer.last_name, customer.phone, customer.email, customer.notes),
    )
    connection.commit()
    return int(cursor.lastrowid)


def add_vehicle(connection: sqlite3.Connection, vehicle: Vehicle) -> int:
    cursor = connection.execute(
        """
        INSERT INTO vehicles (customer_id, year, make, model, vin, license_plate, mileage)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle.customer_id,
            vehicle.year,
            vehicle.make,
            vehicle.model,
            vehicle.vin,
            vehicle.license_plate,
            vehicle.mileage,
        ),
    )
    connection.commit()
    return int(cursor.lastrowid)


def customer_summary(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return connection.execute(
        """
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.phone,
            c.email,
            COUNT(v.id) AS vehicle_count
        FROM customers c
        LEFT JOIN vehicles v ON v.customer_id = c.id
        GROUP BY c.id
        ORDER BY c.last_name, c.first_name
        """
    ).fetchall()

