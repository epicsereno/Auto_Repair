from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


TEXT_FILES: dict[str, str] = {
    "README.md": """# Auto Repair Shop Repository

This repository is organized for strategy, operations, service records,
inventory, reporting, and supporting automation.

## Structure

- `docs/`: documentation and internal reference material
- `config/`: configuration files
- `scripts/`: operational and reporting scripts
- `data/`: raw or generated data
- `reports/`: generated outputs
- `src/`: source code and reusable modules
- `archives/`: archived material
- `01_Strategy_Planning/` through `12_Technical_Manuals/`: business areas
""",
    ".gitignore": """*.log
__pycache__/
*.pyc
*.pyo
.DS_Store
data/raw/*
reports/*.tmp
*.bak
""",
    "LICENSE": "Add your chosen license text here.\n",
    "CONTRIBUTING.md": """# Contributing

## Workflow

1. Create a branch for each change.
2. Keep changes scoped and reviewable.
3. Open a pull request into `main` or `master`.
""",
    "docs/README.md": """# Documentation

Use this folder for procedures, checklists, dashboards, and internal guides.
""",
    "reports/README.md": """# Reports

Generated reports, logs, CSV exports, and workbook outputs belong here.
""",
    "01_Strategy_Planning/goals_objectives.md": """# Goals and Objectives

Document business goals, milestones, and KPIs here.
""",
    "01_Strategy_Planning/swot_analysis.xlsx": "Placeholder file. Replace with a real spreadsheet.\n",
    "01_Strategy_Planning/business_plan.pdf": "Placeholder file. Replace with a real PDF.\n",
    "10_Parts_Inventory/catalog.csv": "part_number,description,quantity\n",
    "config/market_monitor_config.json": """{
  "report_name": "daily_market_report",
  "output_directory": "reports",
  "enabled": true
}
""",
    "scripts/daily_market_report.py": """from __future__ import annotations

import datetime as dt
import os
from pathlib import Path


def main() -> None:
    report_date = os.getenv("REPORT_DATE") or dt.datetime.utcnow().isoformat()
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    log_file = reports_dir / "daily_market_report.log"
    log_file.write_text(f"Daily market report placeholder generated for {report_date}\\n")
    print(f"Generated placeholder report: {log_file}")


if __name__ == "__main__":
    main()
""",
    ".github/workflows/ci-cd.yml": """name: CI/CD Pipeline - Auto Repair Shop Repo

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff black pylint pyyaml

      - name: Run Python Linter (Ruff)
        run: ruff check . --output-format=github

      - name: Check code formatting (Black)
        run: black --check .

      - name: Run static analysis (Pylint)
        run: |
          pylint --disable=R,C $(find . -name "*.py" | grep -v __pycache__) || true

      - name: Validate JSON config
        run: python -m json.tool config/market_monitor_config.json || echo "No config found or invalid"

      - name: Check Markdown links & spelling
        uses: DavidAnson/markdownlint-cli2-action@v19
        with:
          globs: '**/*.md'

  generate-reports:
    needs: ci
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install pandas matplotlib openpyxl pyyaml

      - name: Run Daily Market Report
        run: |
          python scripts/daily_market_report.py
        env:
          REPORT_DATE: ${{ github.event.head_commit.timestamp }}

      - name: Upload generated reports
        uses: actions/upload-artifact@v4
        with:
          name: daily-market-reports
          path: |
            reports/*.log
            reports/*.csv
            reports/*.xlsx
          retention-days: 30
""",
    ".github/workflows/deploy.yml": """name: CD - Deploy Documentation / Reports

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'
      - '**.md'
      - 'index.html'

jobs:
  deploy-docs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          branch: gh-pages
          folder: .
          target-folder: .
          clean: false
""",
    ".github/workflows/validate-structure.yml": """name: Validate Repository Structure

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate-folders:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Verify required directories exist
        run: |
          required_dirs=(
            "01_Strategy_Planning" "02_Financials" "03_Legal_Compliance"
            "04_Marketing_Sales" "05_Operations" "06_Personnel_HR"
            "07_Assets_Inventory" "08_Reports_Analytics" "09_Service_Records"
            "10_Parts_Inventory" "11_Customer_History" "12_Technical_Manuals"
            "scripts" "config" "reports" "docs"
          )

          for dir in "${required_dirs[@]}"; do
            if [ ! -d "$dir" ]; then
              echo "Missing required directory: $dir"
              exit 1
            else
              echo "Found: $dir"
            fi
          done

          echo "Repository structure validation passed!"
""",
}


DIRECTORIES = [
    "docs",
    "config",
    "scripts",
    "data",
    "data/raw",
    "reports",
    "src",
    "archives",
    ".github/workflows",
    "01_Strategy_Planning",
    "01_Strategy_Planning/quarterly_reviews",
    "01_Strategy_Planning/meeting_notes",
    "02_Financials",
    "03_Legal_Compliance",
    "04_Marketing_Sales",
    "04_Marketing_Sales/vehicle_history",
    "04_Marketing_Sales/campaigns",
    "04_Marketing_Sales/customer_acquisition",
    "04_Marketing_Sales/pricing",
    "04_Marketing_Sales/leads",
    "05_Operations",
    "06_Personnel_HR",
    "07_Assets_Inventory",
    "07_Assets_Inventory/vehicles",
    "07_Assets_Inventory/equipment",
    "07_Assets_Inventory/tools",
    "07_Assets_Inventory/depreciation",
    "08_Reports_Analytics",
    "09_Service_Records",
    "09_Service_Records/templates",
    "09_Service_Records/completed_jobs",
    "09_Service_Records/warranties",
    "10_Parts_Inventory",
    "10_Parts_Inventory/suppliers",
    "10_Parts_Inventory/stock_levels",
    "10_Parts_Inventory/orders",
    "11_Customer_History",
    "12_Technical_Manuals",
]


GITKEEP_DIRS = [
    "data",
    "data/raw",
    "src",
    "archives",
    "01_Strategy_Planning/quarterly_reviews",
    "01_Strategy_Planning/meeting_notes",
    "02_Financials",
    "03_Legal_Compliance",
    "04_Marketing_Sales",
    "04_Marketing_Sales/vehicle_history",
    "04_Marketing_Sales/campaigns",
    "04_Marketing_Sales/customer_acquisition",
    "04_Marketing_Sales/pricing",
    "04_Marketing_Sales/leads",
    "05_Operations",
    "06_Personnel_HR",
    "07_Assets_Inventory",
    "07_Assets_Inventory/vehicles",
    "07_Assets_Inventory/equipment",
    "07_Assets_Inventory/tools",
    "07_Assets_Inventory/depreciation",
    "08_Reports_Analytics",
    "09_Service_Records",
    "09_Service_Records/templates",
    "09_Service_Records/completed_jobs",
    "09_Service_Records/warranties",
    "10_Parts_Inventory",
    "10_Parts_Inventory/suppliers",
    "10_Parts_Inventory/stock_levels",
    "10_Parts_Inventory/orders",
    "11_Customer_History",
    "12_Technical_Manuals",
]


def ensure_directories() -> None:
    for rel_path in DIRECTORIES:
        (ROOT / rel_path).mkdir(parents=True, exist_ok=True)


def ensure_text_files() -> None:
    for rel_path, content in TEXT_FILES.items():
        file_path = ROOT / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.write_text(content)


def ensure_gitkeeps() -> None:
    for rel_dir in GITKEEP_DIRS:
        gitkeep = ROOT / rel_dir / ".gitkeep"
        gitkeep.parent.mkdir(parents=True, exist_ok=True)
        if not gitkeep.exists():
            gitkeep.write_text("")


def main() -> None:
    ensure_directories()
    ensure_text_files()
    ensure_gitkeeps()
    print("Repository scaffold completed.")


if __name__ == "__main__":
    main()
