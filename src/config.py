from __future__ import annotations

import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DEFAULT_DATABASE_PATH = DATA_DIR / "auto_repair.sqlite3"


def database_path() -> Path:
    return Path(os.getenv("AUTO_REPAIR_DB", str(DEFAULT_DATABASE_PATH))).expanduser()

