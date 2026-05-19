from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

from src.services.inventory import low_stock_parts
from src.services.scheduling import open_orders


def write_daily_snapshot(connection: sqlite3.Connection, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    orders = open_orders(connection)
    parts = low_stock_parts(connection)

    with output_path.open("w", newline="") as report_file:
        writer = csv.writer(report_file)
        writer.writerow(["section", "id_or_part", "summary", "status_or_quantity"])
        for order in orders:
            writer.writerow(["open_order", order["id"], order["vehicle"], order["status"]])
        for part in parts:
            writer.writerow(["low_stock_part", part["part_number"], part["description"], part["quantity_on_hand"]])

    return output_path

