from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    first_name: str
    last_name: str
    role: str
    phone: str | None = None
    email: str | None = None
    id: int | None = None

