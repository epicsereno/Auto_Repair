from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Vehicle:
    customer_id: int
    year: int
    make: str
    model: str
    vin: str | None = None
    license_plate: str | None = None
    mileage: int = 0
    id: int | None = None

