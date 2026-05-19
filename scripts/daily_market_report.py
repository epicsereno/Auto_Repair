from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.database import connect, initialize
from src.services.reporting import write_daily_snapshot


def main() -> None:
    report_date = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    output_path = Path("reports/generated") / f"daily_market_report_{report_date}.csv"
    db_path = initialize()
    with connect(db_path) as connection:
        report_path = write_daily_snapshot(connection, output_path)
    print(f"Generated daily market report: {report_path}")


if __name__ == "__main__":
    main()
