from __future__ import annotations

import sqlite3

from src.models import Part


def upsert_part(connection: sqlite3.Connection, part: Part) -> int:
    connection.execute(
        """
        INSERT INTO parts (
            part_number, description, quantity_on_hand, reorder_point, unit_cost_cents, supplier
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(part_number) DO UPDATE SET
            description = excluded.description,
            quantity_on_hand = excluded.quantity_on_hand,
            reorder_point = excluded.reorder_point,
            unit_cost_cents = excluded.unit_cost_cents,
            supplier = excluded.supplier
        """,
        (
            part.part_number,
            part.description,
            part.quantity_on_hand,
            part.reorder_point,
            part.unit_cost_cents,
            part.supplier,
        ),
    )
    connection.commit()
    row = connection.execute("SELECT id FROM parts WHERE part_number = ?", (part.part_number,)).fetchone()
    return int(row["id"])


def low_stock_parts(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return connection.execute(
        """
        SELECT part_number, description, quantity_on_hand, reorder_point, supplier
        FROM parts
        WHERE quantity_on_hand <= reorder_point
        ORDER BY quantity_on_hand ASC, part_number ASC
        """
    ).fetchall()

