#!/usr/bin/env python3
"""Business-specific launcher for Precision Auto Repair & Diagnostics."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared_automation.daily_market_report import BusinessDefaults, run_cli

if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            BusinessDefaults(
                name="Precision Auto Repair & Diagnostics",
                keywords=["Los Angeles auto repair", "vehicle maintenance", "auto recall"],
                business_dir=Path(__file__).resolve().parent,
            )
        )
    )
