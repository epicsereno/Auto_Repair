# 🔧 Precision Auto Works & Repair

[![Status](https://img.shields.io/badge/Status-Operational-brightgreen)]()
[![Industry](https://img.shields.io/badge/Industry-Automotive_Services-blue)]()
[![Platform](https://img.shields.io/badge/Empire-OS-gold)]()

**Live site:** https://epicsereno.github.io/Auto_Repair/

> To provide reliable, high-quality automotive maintenance and repair services with a focus on transparency, efficiency, and customer safety.

---

## 📂 Repository Structure

This repo intentionally separates the Python application from business operating
artifacts. The `src/` package owns executable behavior and the SQLite data model.
The numbered folders are planning, records, inventory, manuals, and other
business-document buckets.

| Directory | Focus |
| :--- | :--- |
| `src` | Python package for the CLI, SQLite schema, dataclass models, and services. |
| `scripts` | Maintenance, backup, and report-generation scripts. |
| `config` | JSON configuration for local tooling and reporting. |
| `data` | Local SQLite database, raw inputs, and backups ignored by Git where appropriate. |
| `docs` | Architecture, API direction, user docs, and schema documentation. |
| `reports` | Generated operational report outputs. |
| `archives` | Legacy files retained for reference during repo migration. |
| `01_Strategy_Planning` | Business growth, market analysis, and long-term service goals. |
| `02_Financials` | Profit/loss tracking, payroll, and equipment financing. |
| `03_Legal_Compliance` | Licensing, insurance, and environmental safety regulations. |
| `04_Marketing_Sales` | CRM, seasonal promotions, and reputation management. |
| `05_Operations` | Daily bay scheduling, workflow optimization, and quality control. |
| `06_Personnel_HR` | Technician certifications, training, and performance reviews. |
| `07_Assets_Inventory` | Lift maintenance, diagnostic tools, and heavy equipment tracking. |
| `08_Reports_Analytics` | Cycle time metrics, average repair order (ARO) analysis. |
| `09_Service_Records` | Digital archives of all vehicle maintenance performed. |
| `10_Parts_Inventory` | Real-time stock levels for OEM and aftermarket components. |
| `11_Customer_History` | Comprehensive client profiles and communication logs. |
| `12_Technical_Manuals` | Proprietary and manufacturer-specific repair procedures. |

---

## 🛠️ Operational Excellence

- **Diagnostic Precision:** Leveraging advanced OBD-II and proprietary scanning tools.
- **Parts Optimization:** Automated reorder points to ensure zero downtime for common repairs.
- **Customer Transparency:** Detailed digital inspections provided for every vehicle.

## Technical Stack

- **Runtime:** Python 3.11+
- **Storage:** SQLite at `data/auto_repair.sqlite3`
- **Application layer:** `src/` package with dataclass models and service modules
- **Automation:** `scripts/` for reporting, backups, and repo maintenance
- **Static site:** `index.html` is the GitHub Pages operations dashboard entry point

## Quick Start

```bash
cp .env.example .env
python -m src.main init-db
python -m src.main seed-demo
python -m src.main status
python scripts/daily_market_report.py
```

The generated SQLite database and report CSV files are ignored by Git so live operating data does not get committed accidentally.

## CLI Commands

| Command | Purpose |
| :--- | :--- |
| `python -m src.main init-db` | Create or update the SQLite schema. |
| `python -m src.main seed-demo` | Insert a demo customer, vehicle, service order, and part. |
| `python -m src.main status` | Print current customer, open-order, and low-stock counts. |
| `python -m src.main available-slots <vehicle_id>` | Show open appointment slots for a vehicle. |
| `python -m src.main book-demo-appointment` | Book a sample appointment for the first vehicle. |
| `python -m src.main daily-snapshot` | Write a CSV snapshot to `reports/generated/`. |

## Schema

The SQLite schema is documented in [`docs/schema.md`](docs/schema.md). It covers
customers, vehicles, employees, suppliers, service orders, jobs, appointments,
parts, invoices, indexes, and timestamp triggers.

## GitHub Pages

`index.html` is the static GitHub Pages entry point. Pushes to `main` that change
docs, Markdown, `index.html`, `.nojekyll`, or the deploy workflow publish the
site through `.github/workflows/deploy.yml`.

Live site: https://epicsereno.github.io/Auto_Repair/

In repository settings, **Pages > Build and deployment > Source** is set to
**GitHub Actions**.

## CI/CD

GitHub Actions currently runs three workflows:

- `.github/workflows/ci-cd.yml` checks Python formatting and linting on Python
  3.11 and 3.12, validates JSON config, runs Markdown linting, and uploads daily
  market report artifacts from `main`.
- `.github/workflows/deploy.yml` uploads the static site artifact and deploys it
  with GitHub Pages Actions.
- `.github/workflows/validate-structure.yml` verifies the expected business and
  support directories exist on pull requests.

---

## 🗺️ Business Roadmap

- [ ] **1. Facility Selection & Leasing:** Identify and secure a 2,500+ sq ft facility with high-traffic visibility and appropriate zoning.
- [ ] **2. Equipment Procurement:** Purchase and install hydraulic lifts, diagnostic scanners, and specialized tools.
- [ ] **3. Licensing & Permits:** Obtain automotive repair licenses, environmental permits, and business insurance.
- [ ] **4. Staff Recruitment:** Hire ASE-certified mechanics and a professional service advisor.
- [ ] **5. Parts Supplier Integration:** Establish accounts with major distributors for just-in-time delivery.
- [ ] **6. Shop Management Software:** Implement a system for work orders, invoicing, and customer history.
- [ ] **7. Local SEO & Marketing:** Launch website, optimize Google Business Profile, and start local search ads.
- [ ] **8. Operational Workflow Setup:** Define SOPs for vehicle intake, inspection, and quality control.
- [ ] **9. Fleet Service Outreach:** Pitch maintenance contracts to local businesses with vehicle fleets.
- [ ] **10. Grand Opening Event:** Host a community event with free inspections and introductory offers.

## Software Roadmap

- [ ] **Schema tests:** Add focused tests for schema creation and migration behavior.
- [ ] **Service tests:** Cover service orders, inventory reorder reporting, and appointment conflicts.
- [ ] **FastAPI layer:** Add HTTP endpoints after the local SQLite workflow is tested.
- [ ] **Report consolidation:** Separate shop operations reports from legacy market-report scripts.

## 🚀 Key Metrics

- **Fixed Right First Time (FRFT):** Our primary quality benchmark.
- **Bay Utilization:** Maximizing throughput across all service stations.
- **Parts Margin:** Balancing competitive pricing with healthy profitability.

---

*This repository is a managed unit of the Empire OS.*
