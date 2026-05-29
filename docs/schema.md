# SQLite Schema

`src/database.py` is the source of truth for schema creation and lightweight migrations.
Running `python -m src.main init-db` creates or updates the SQLite database at
`data/auto_repair.sqlite3` unless `AUTO_REPAIR_DB` points somewhere else.

## Core Tables

### `customers`

Customer contact profile and communication preferences.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `first_name` | TEXT | Required |
| `last_name` | TEXT | Required |
| `phone` | TEXT | Optional |
| `email` | TEXT | Optional |
| `address` | TEXT | Optional |
| `city` | TEXT | Optional |
| `state` | TEXT | Optional |
| `zip_code` | TEXT | Optional |
| `date_of_birth` | TEXT | Optional |
| `preferred_contact` | TEXT | `phone`, `email`, or `text` |
| `notes` | TEXT | Optional |
| `created_at` | TEXT | Defaults to current timestamp |
| `updated_at` | TEXT | Maintained by trigger |

### `vehicles`

Vehicles owned by customers.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `customer_id` | INTEGER | Required; references `customers.id` |
| `year` | INTEGER | Required |
| `make` | TEXT | Required |
| `model` | TEXT | Required |
| `vin` | TEXT | Unique when present |
| `license_plate` | TEXT | Unique when present |
| `color` | TEXT | Optional |
| `mileage` | INTEGER | Defaults to `0` |
| `engine_type` | TEXT | Optional |
| `transmission` | TEXT | Optional |
| `fuel_type` | TEXT | Optional |
| `last_service_date` | TEXT | Optional |
| `notes` | TEXT | Optional |
| `created_at` | TEXT | Defaults to current timestamp |
| `updated_at` | TEXT | Maintained by trigger |

### `employees`

Shop staff and technician records.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `first_name` | TEXT | Required |
| `last_name` | TEXT | Required |
| `role` | TEXT | Required |
| `email` | TEXT | Unique when present |
| `phone` | TEXT | Optional |
| `hire_date` | TEXT | Optional |
| `salary_cents` | INTEGER | Optional |
| `is_active` | INTEGER | Defaults to `1` |
| `notes` | TEXT | Optional |
| `created_at` | TEXT | Defaults to current timestamp |

### `suppliers`

Vendor account and contact records.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `name` | TEXT | Required |
| `contact_person` | TEXT | Optional |
| `phone` | TEXT | Optional |
| `email` | TEXT | Optional |
| `address` | TEXT | Optional |
| `website` | TEXT | Optional |
| `account_number` | TEXT | Optional |
| `notes` | TEXT | Optional |
| `created_at` | TEXT | Defaults to current timestamp |

### `parts`

Inventory catalog and stock levels.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `part_number` | TEXT | Required and unique |
| `name` | TEXT | Optional |
| `description` | TEXT | Required |
| `category` | TEXT | Optional |
| `supplier_id` | INTEGER | Optional; references `suppliers.id` |
| `quantity_on_hand` | INTEGER | Defaults to `0` |
| `stock_quantity` | INTEGER | Defaults to `0` |
| `reorder_point` | INTEGER | Defaults to `0` |
| `min_stock_level` | INTEGER | Defaults to `5` |
| `unit_cost_cents` | INTEGER | Defaults to `0` |
| `retail_price_cents` | INTEGER | Defaults to `0` |
| `location_bin` | TEXT | Optional |
| `is_active` | INTEGER | Defaults to `1` |
| `supplier` | TEXT | Legacy/free-text supplier field |
| `created_at` | TEXT | Defaults to current timestamp |
| `updated_at` | TEXT | Maintained by trigger |

## Work Tables

### `service_orders`

Customer complaints and initial service intake.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `customer_id` | INTEGER | Required; references `customers.id` |
| `vehicle_id` | INTEGER | Required; references `vehicles.id` |
| `status` | TEXT | Defaults to `open` |
| `complaint` | TEXT | Required |
| `diagnosis` | TEXT | Optional |
| `estimate_cents` | INTEGER | Defaults to `0` |
| `opened_at` | TEXT | Defaults to current timestamp |
| `closed_at` | TEXT | Optional |

### `service_types`

Reusable service catalog entries.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `name` | TEXT | Required |
| `description` | TEXT | Optional |
| `default_hours` | REAL | Optional |
| `base_price_cents` | INTEGER | Optional |
| `category` | TEXT | Optional |
| `is_active` | INTEGER | Defaults to `1` |

### `jobs`

Repair jobs and final costing.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `vehicle_id` | INTEGER | Required; references `vehicles.id` |
| `customer_id` | INTEGER | Optional; references `customers.id` |
| `employee_id` | INTEGER | Optional; references `employees.id` |
| `status` | TEXT | `pending`, `in_progress`, `completed`, `invoiced`, or `cancelled` |
| `start_date` | TEXT | Optional |
| `completion_date` | TEXT | Optional |
| `total_labor_hours` | REAL | Optional |
| `labor_rate_cents` | INTEGER | Defaults to `12500` |
| `total_parts_cost_cents` | INTEGER | Defaults to `0` |
| `total_labor_cost_cents` | INTEGER | Defaults to `0` |
| `tax_amount_cents` | INTEGER | Defaults to `0` |
| `grand_total_cents` | INTEGER | Optional |
| `notes` | TEXT | Optional |
| `created_at` | TEXT | Defaults to current timestamp |
| `updated_at` | TEXT | Maintained by trigger |

### `job_services`

Services performed on a job.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `job_id` | INTEGER | Required; references `jobs.id` |
| `service_type_id` | INTEGER | Optional; references `service_types.id` |
| `hours_spent` | REAL | Optional |
| `price_charged_cents` | INTEGER | Optional |
| `notes` | TEXT | Optional |

### `job_parts`

Parts consumed by a job.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `job_id` | INTEGER | Required; references `jobs.id` |
| `part_id` | INTEGER | Optional; references `parts.id` |
| `quantity` | INTEGER | Defaults to `1` |
| `unit_cost_at_time_cents` | INTEGER | Required |
| `total_cost_cents` | INTEGER | Generated as `quantity * unit_cost_at_time_cents` |

### `appointments`

Scheduled bay and technician appointments.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `customer_id` | INTEGER | Optional; references `customers.id` |
| `vehicle_id` | INTEGER | Optional; references `vehicles.id` |
| `job_id` | INTEGER | Optional; references `jobs.id` |
| `technician_id` | INTEGER | Optional; references `employees.id` |
| `scheduled_start` | TEXT | Required |
| `scheduled_end` | TEXT | Optional |
| `status` | TEXT | Defaults to `scheduled` |
| `bay_number` | TEXT | Optional |
| `service_duration_hours` | REAL | Defaults to `2.0` |
| `created_at` | TEXT | Defaults to current timestamp |

### `invoices`

Billing records tied to jobs and customers.

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary key |
| `job_id` | INTEGER | Optional; references `jobs.id` |
| `customer_id` | INTEGER | Optional; references `customers.id` |
| `invoice_number` | TEXT | Required and unique |
| `issue_date` | TEXT | Defaults to current date |
| `due_date` | TEXT | Optional |
| `status` | TEXT | Defaults to `unpaid` |
| `subtotal_cents` | INTEGER | Optional |
| `tax_amount_cents` | INTEGER | Optional |
| `total_amount_cents` | INTEGER | Required |
| `amount_paid_cents` | INTEGER | Defaults to `0` |
| `payment_method` | TEXT | Optional |
| `notes` | TEXT | Optional |

## Indexes And Triggers

Indexes are created for common lookup fields:

- `vehicles.customer_id`
- `service_orders.vehicle_id`
- `service_orders.status`
- `jobs.vehicle_id`
- `jobs.status`
- `parts.category`
- `appointments.scheduled_start`
- `appointments.scheduled_start`, `appointments.scheduled_end`, `appointments.bay_number`
- `appointments.technician_id`

Timestamp triggers maintain `updated_at` on `customers`, `vehicles`, `parts`, and `jobs`.
