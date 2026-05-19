from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import sqlite3
from typing import Any

from src.models import ServiceOrder


@dataclass(frozen=True)
class AppointmentSlot:
    start: datetime
    end: datetime
    bay_number: str
    technician_id: int | None
    is_available: bool
    conflicts: list[str]


def open_service_order(connection: sqlite3.Connection, order: ServiceOrder) -> int:
    cursor = connection.execute(
        """
        INSERT INTO service_orders (
            customer_id, vehicle_id, status, complaint, diagnosis, estimate_cents
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            order.customer_id,
            order.vehicle_id,
            order.status,
            order.complaint,
            order.diagnosis,
            order.estimate_cents,
        ),
    )
    connection.commit()
    return int(cursor.lastrowid)


def open_orders(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return connection.execute(
        """
        SELECT
            so.id,
            so.status,
            so.complaint,
            so.estimate_cents,
            c.first_name || ' ' || c.last_name AS customer_name,
            v.year || ' ' || v.make || ' ' || v.model AS vehicle
        FROM service_orders so
        JOIN customers c ON c.id = so.customer_id
        JOIN vehicles v ON v.id = so.vehicle_id
        WHERE so.status != 'closed'
        ORDER BY so.opened_at ASC
        """
    ).fetchall()


class MaintenanceScheduler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def check_conflicts(
        self,
        proposed_start: datetime,
        duration_hours: float = 2.0,
        bay_number: str | None = None,
        technician_id: int | None = None,
    ) -> list[dict[str, Any]]:
        proposed_end = proposed_start + timedelta(hours=duration_hours)
        query = """
            SELECT
                a.id,
                a.scheduled_start,
                a.scheduled_end,
                a.bay_number,
                a.status,
                c.first_name || ' ' || c.last_name AS customer,
                v.year || ' ' || v.make || ' ' || v.model AS vehicle,
                a.technician_id
            FROM appointments a
            JOIN customers c ON c.id = a.customer_id
            JOIN vehicles v ON v.id = a.vehicle_id
            WHERE a.status NOT IN ('cancelled', 'completed')
              AND a.scheduled_start < ?
              AND COALESCE(a.scheduled_end, a.scheduled_start) > ?
        """
        params: list[Any] = [_to_db_datetime(proposed_end), _to_db_datetime(proposed_start)]

        if bay_number:
            query += " AND a.bay_number = ?"
            params.append(bay_number)
        if technician_id:
            query += " AND a.technician_id = ?"
            params.append(technician_id)

        rows = self.connection.execute(query, params).fetchall()
        return [
            {
                "appointment_id": row["id"],
                "start": row["scheduled_start"],
                "end": row["scheduled_end"],
                "bay": row["bay_number"],
                "status": row["status"],
                "customer": row["customer"],
                "vehicle": row["vehicle"],
                "technician_id": row["technician_id"],
            }
            for row in rows
        ]

    def find_available_slots(
        self,
        vehicle_id: int,
        days_ahead: int = 14,
        service_duration_hours: float = 2.0,
        preferred_bay: str | None = None,
        technician_id: int | None = None,
        max_slots: int = 8,
    ) -> list[AppointmentSlot]:
        start_hour = 8
        end_hour = 17
        current = datetime.now(UTC).replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_date = current + timedelta(days=days_ahead)
        bay_number = preferred_bay or "1"
        available_slots: list[AppointmentSlot] = []

        while current < end_date:
            if current.weekday() >= 5:
                current = (current + timedelta(days=1)).replace(hour=start_hour)
                continue

            for hour in range(start_hour, end_hour):
                slot_start = current.replace(hour=hour)
                slot_end = slot_start + timedelta(hours=service_duration_hours)
                if slot_end.hour > end_hour or (slot_end.hour == end_hour and slot_end.minute > 0):
                    continue

                conflicts = self.check_conflicts(
                    slot_start,
                    service_duration_hours,
                    bay_number=preferred_bay,
                    technician_id=technician_id,
                )
                slot = AppointmentSlot(
                    start=slot_start,
                    end=slot_end,
                    bay_number=bay_number,
                    technician_id=technician_id,
                    is_available=not conflicts,
                    conflicts=[f"{conflict['customer']} - {conflict['vehicle']}" for conflict in conflicts],
                )
                if slot.is_available:
                    available_slots.append(slot)
                    if len(available_slots) >= max_slots:
                        return available_slots

            current = (current + timedelta(days=1)).replace(hour=start_hour)

        return available_slots

    def book_appointment(
        self,
        customer_id: int,
        vehicle_id: int,
        scheduled_start: datetime,
        duration_hours: float = 2.0,
        bay_number: str | None = None,
        technician_id: int | None = None,
        job_id: int | None = None,
    ) -> int:
        conflicts = self.check_conflicts(
            scheduled_start,
            duration_hours,
            bay_number=bay_number,
            technician_id=technician_id,
        )
        if conflicts:
            summaries = ", ".join(f"{item['customer']} ({item['vehicle']})" for item in conflicts)
            raise ValueError(f"Appointment conflicts with: {summaries}")

        scheduled_end = scheduled_start + timedelta(hours=duration_hours)
        cursor = self.connection.execute(
            """
            INSERT INTO appointments (
                customer_id,
                vehicle_id,
                job_id,
                technician_id,
                scheduled_start,
                scheduled_end,
                status,
                bay_number,
                service_duration_hours
            )
            VALUES (?, ?, ?, ?, ?, ?, 'scheduled', ?, ?)
            """,
            (
                customer_id,
                vehicle_id,
                job_id,
                technician_id,
                _to_db_datetime(scheduled_start),
                _to_db_datetime(scheduled_end),
                bay_number,
                duration_hours,
            ),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def suggest_maintenance_with_conflicts(self, vehicle_id: int) -> dict[str, Any]:
        slots = self.find_available_slots(vehicle_id=vehicle_id)
        return {
            "vehicle_id": vehicle_id,
            "recommended_task": {
                "name": "General maintenance inspection",
                "estimated_hours": 2.0,
            },
            "available_slots": [
                {
                    "start": slot.start.isoformat(),
                    "end": slot.end.isoformat(),
                    "bay": slot.bay_number,
                    "available": slot.is_available,
                }
                for slot in slots[:5]
            ],
            "urgent_conflicts": bool(self.check_conflicts(datetime.now(UTC), 4.0)),
        }


def _to_db_datetime(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.isoformat(timespec="seconds")
