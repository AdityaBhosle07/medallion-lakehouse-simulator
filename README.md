# Medallion Lakehouse Simulator

A small-scale, end-to-end data lakehouse pipeline demonstrating the Medallion Architecture
(Bronze / Silver / Gold), built to mirror a real-world professional-services data engineering
use case: integrating ERP, HR, CRM, and Finance systems into business-ready, AI-consumable datasets.

## Architecture Overview

```
Sources (ERP, HR, CRM, Finance API)
        |
        v
   BRONZE (raw, immutable, audited)
        |
        v
   SILVER (cleaned, standardized, joined across systems)
        |
        v
    GOLD (business-ready: profitability, utilization, fee benchmarking)
        |
        v
  SERVING API (FastAPI) --> Dashboards / AI Applications
```

## Project Structure

- `sources/` — Simulated ERP, HR, CRM, and Finance ("API") source data
- `pipelines/ingestion/` — Scheduled ingestion scripts pulling from each source
- `pipelines/bronze/` — Bronze layer writer (raw, immutable, timestamped)
- `pipelines/silver/` — Cleaning, standardization, and cross-source joins
- `pipelines/gold/` — Business-ready aggregated tables
- `pipelines/monitoring/` — Pipeline health checks and anomaly detection
- `serving/api/` — FastAPI serving layer exposing Gold data
- `data_quality/` — Validation rules and quality reporting
- `docs/` — Architecture diagram, data lineage, and runbooks

## How to Run

```bash
# 1. Ingest all sources into Bronze
python pipelines/ingestion/ingest_erp.py
python pipelines/ingestion/ingest_hr.py
python pipelines/ingestion/ingest_crm.py
python pipelines/ingestion/ingest_finance_api.py

# 2. Clean and join into Silver
python pipelines/silver/clean_erp.py
python pipelines/silver/clean_hr.py
python pipelines/silver/clean_crm.py
python pipelines/silver/join_silver_tables.py

# 3. Build Gold tables
python pipelines/gold/gold_project_profitability.py
python pipelines/gold/gold_utilization_analytics.py
python pipelines/gold/gold_fee_benchmarking.py

# 4. Check pipeline health
python pipelines/monitoring/pipeline_health_check.py

# 5. Serve Gold data via API
uvicorn serving.api.main:app --reload
```

## Why This Project

This project was built to demonstrate the exact responsibilities of a production data engineering
role: building automated ingestion pipelines from multiple enterprise systems (ERP, HR, CRM,
Finance), implementing the Bronze/Silver/Gold medallion pattern, producing business-ready
analytics (profitability, utilization, fee benchmarking), exposing that data through a serving API,
and maintaining clear documentation and lineage so the system can be extended by others.

See `docs/data_lineage.md` for full field-level lineage and `docs/runbook_add_new_source.md` /
`docs/runbook_troubleshooting.md` for operational documentation.

## Serving API

FastAPI layer exposing Gold tables for dashboards and AI applications.

### Run the API
```bash
python -m uvicorn serving.api.main:app --reload
```

Visit interactive docs at `http://127.0.0.1:8000/docs`.

### Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/profitability` | Project-level budget, cost, invoicing, and profit margin data |
| `GET /api/utilization` | Team/resource utilization analytics |
| `GET /api/benchmarking` | Fee benchmarking across project types |

Each endpoint returns a 404 with a clear message if the corresponding Gold CSV hasn't been generated yet.

### Example
```bash
curl -X GET http://127.0.0.1:8000/api/profitability -H "accept: application/json"
```

### Testing
```bash
pip install requests
python test_api.py
```
