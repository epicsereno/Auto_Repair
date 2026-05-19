from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    first_name: str
    last_name: str
    phone: str | None = None
    email: str | None = None
    notes: str | None = None
    id: int | None = None

