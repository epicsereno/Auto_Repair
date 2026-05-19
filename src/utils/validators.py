from __future__ import annotations


def require_positive_int(value: int, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"{field_name} must be zero or greater")


def require_text(value: str, field_name: str) -> None:
    if not value.strip():
        raise ValueError(f"{field_name} is required")

