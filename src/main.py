from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
from pathlib import Path

from src.database import connect, initialize
from src.models import Customer, Part, ServiceOrder, Vehicle
from src.services.customer_crm import add_customer, add_vehicle, customer_summary
from src.services.inventory import low_stock_parts, upsert_part
from src.services.reporting import write_daily_snapshot
from src.services.scheduling import MaintenanceScheduler, open_orders, open_service_order


def seed_demo_data() -> None:
    db_path = initialize()
    with connect(db_path) as connection:
        customer_id = add_customer(connection, Customer("Demo", "Customer", phone="555-0100"))
        vehicle_id = add_vehicle(
            connection,
            Vehicle(customer_id=customer_id, year=2018, make="Toyota", model="Camry", mileage=84200),
        )
        open_service_order(
            connection,
            ServiceOrder(
                customer_id=customer_id,
                vehicle_id=vehicle_id,
                complaint="Oil change, brake inspection, and intermittent check engine light.",
                estimate_cents=18900,
            ),
        )
        upsert_part(connection, Part("OF-4967", "Oil filter", quantity_on_hand=3, reorder_point=5, supplier="Local"))
    print(f"Seeded demo shop data in {db_path}")


def show_status() -> None:
    db_path = initialize()
    with connect(db_path) as connection:
        customers = customer_summary(connection)
        orders = open_orders(connection)
        low_stock = low_stock_parts(connection)

    print(f"Database: {db_path}")
    print(f"Customers: {len(customers)}")
    print(f"Open service orders: {len(orders)}")
    print(f"Low-stock parts: {len(low_stock)}")


def write_report(output_path: Path) -> None:
    db_path = initialize()
    with connect(db_path) as connection:
        report_path = write_daily_snapshot(connection, output_path)
    print(f"Wrote report: {report_path}")


def show_available_slots(vehicle_id: int, hours: float) -> None:
    db_path = initialize()
    with connect(db_path) as connection:
        scheduler = MaintenanceScheduler(connection)
        slots = scheduler.find_available_slots(vehicle_id=vehicle_id, service_duration_hours=hours)

    if not slots:
        print("No available slots found.")
        return

    for slot in slots:
        print(f"{slot.start.isoformat()} to {slot.end.isoformat()} | bay {slot.bay_number}")


def book_demo_appointment() -> None:
    db_path = initialize()
    with connect(db_path) as connection:
        vehicle = connection.execute(
            """
            SELECT v.id AS vehicle_id, c.id AS customer_id
            FROM vehicles v
            JOIN customers c ON c.id = v.customer_id
            ORDER BY v.id
            LIMIT 1
            """
        ).fetchone()
        if not vehicle:
            raise SystemExit("No vehicle found. Run `python -m src.main seed-demo` first.")

        scheduler = MaintenanceScheduler(connection)
        start = datetime.now(UTC).replace(minute=0, second=0, microsecond=0) + timedelta(days=1)
        appointment_id = scheduler.book_appointment(
            customer_id=vehicle["customer_id"],
            vehicle_id=vehicle["vehicle_id"],
            scheduled_start=start,
            duration_hours=2.0,
            bay_number="1",
        )
    print(f"Booked demo appointment: {appointment_id}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Auto repair shop operations CLI")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("init-db", help="Create or update the SQLite database schema")
    subcommands.add_parser("seed-demo", help="Insert sample customer, vehicle, order, and part data")
    subcommands.add_parser("status", help="Print shop data counts")
    subcommands.add_parser("book-demo-appointment", help="Book a demo appointment for the first vehicle")

    slots_parser = subcommands.add_parser("available-slots", help="Print available appointment slots")
    slots_parser.add_argument("vehicle_id", type=int)
    slots_parser.add_argument("--hours", type=float, default=2.0)

    report_parser = subcommands.add_parser("daily-snapshot", help="Write a daily CSV operations snapshot")
    report_parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/generated/daily_snapshot.csv"),
        help="CSV output path",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init-db":
        print(f"Initialized database: {initialize()}")
    elif args.command == "seed-demo":
        seed_demo_data()
    elif args.command == "status":
        show_status()
    elif args.command == "book-demo-appointment":
        book_demo_appointment()
    elif args.command == "available-slots":
        show_available_slots(args.vehicle_id, args.hours)
    elif args.command == "daily-snapshot":
        write_report(args.output)


if __name__ == "__main__":
    main()
