from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceOrder:
    customer_id: int
    vehicle_id: int
    complaint: str
    status: str = "open"
    diagnosis: str | None = None
    estimate_cents: int = 0
    id: int | None = None

