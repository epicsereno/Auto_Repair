# API Notes

No HTTP API is active yet. The current interface is the CLI in `src/main.py`.

## CLI Commands

```bash
python -m src.main init-db
python -m src.main seed-demo
python -m src.main status
python -m src.main available-slots 1 --hours 2.0
python -m src.main book-demo-appointment
python -m src.main daily-snapshot --output reports/generated/daily_snapshot.csv
```

## Planned HTTP Resources

- `GET /customers`
- `POST /customers`
- `POST /customers/{customer_id}/vehicles`
- `GET /service-orders`
- `POST /service-orders`
- `GET /appointments/available-slots`
- `POST /appointments`
- `GET /parts/low-stock`
