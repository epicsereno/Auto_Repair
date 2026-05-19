# User Manual

## Daily Operations

Run the status command to inspect the current shop data counts:

```bash
python -m src.main status
```

Generate the daily operations snapshot:

```bash
python scripts/daily_market_report.py
```

Back up the database:

```bash
scripts/backup_db.sh
```

Check appointment availability for a vehicle:

```bash
python -m src.main available-slots 1 --hours 2.0
```

Book a demo appointment for the first vehicle:

```bash
python -m src.main book-demo-appointment
```

## Data Location

- Main database: `data/auto_repair.sqlite3`
- Backups: `data/backups/`
- Generated reports: `reports/generated/`
