from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Part:
    part_number: str
    description: str
    quantity_on_hand: int = 0
    reorder_point: int = 0
    unit_cost_cents: int = 0
    supplier: str | None = None
    id: int | None = None

