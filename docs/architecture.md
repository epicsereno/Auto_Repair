# Architecture

The repository is organized around a small Python application core and a broader business operating file structure.

## Application Core

- `src/database.py` owns SQLite connection setup and schema initialization.
- `src/models/` contains dataclass domain objects.
- `src/services/` contains business operations for CRM, scheduling, inventory, and reporting.
- `src/main.py` exposes the local command-line interface.
- `scripts/` contains executable maintenance and reporting wrappers.

## Scheduling

`src/services/scheduling.py` includes conflict detection for appointments. It checks overlapping time windows and can optionally lock by bay number or technician. Appointment creation should go through `MaintenanceScheduler.book_appointment()` so conflicts are checked before insert.

## Data Flow

1. Initialize the database with `python -m src.main init-db`.
2. Add or import customers, vehicles, parts, and service orders through service functions.
3. Generate operational snapshots into `reports/generated/`.
4. Back up the SQLite database into `data/backups/`.

## API Direction

FastAPI is the natural next layer, but it should be added after the core service functions have tests. The API should call the existing service layer rather than duplicating SQL inside route handlers.
