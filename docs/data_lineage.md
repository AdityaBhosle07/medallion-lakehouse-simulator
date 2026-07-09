# Data Lineage

This document traces every Gold-layer field back to its Bronze source, so any output
can be audited and understood end-to-end.

## gold_project_profitability.csv

| Gold Field | Traced Back To | Bronze Source |
|---|---|---|
| project_id, project_name, project_type, status | silver_projects.csv | bronze/erp_projects_*.csv |
| budget, actual_cost | silver_projects.csv | bronze/erp_projects_*.csv |
| total_invoiced, invoice_count | silver_joined.csv (aggregated from invoices) | bronze/finance_invoices_*.csv |
| profit, profit_margin_pct, budget_variance | Derived (Gold-layer calculation) | Computed from budget, actual_cost, total_invoiced |

## gold_utilization_analytics.csv

| Gold Field | Traced Back To | Bronze Source |
|---|---|---|
| department | silver_employees.csv | bronze/hr_employees_*.csv |
| avg_utilization_pct, avg_hourly_rate | silver_employees.csv (aggregated) | bronze/hr_employees_*.csv |
| headcount | silver_employees.csv (count) | bronze/hr_employees_*.csv |

## gold_fee_benchmarking.csv

| Gold Field | Traced Back To | Bronze Source |
|---|---|---|
| project_type | silver_projects.csv | bronze/erp_projects_*.csv |
| avg_budget, avg_actual_cost | silver_projects.csv (aggregated) | bronze/erp_projects_*.csv |
| avg_total_invoiced | silver_joined.csv (aggregated from invoices) | bronze/finance_invoices_*.csv |

## Cross-System Join Keys

- `client_id` — links ERP projects to CRM clients
- `relationship_manager` (maps to `employee_id`) — links CRM clients to HR employees
- `project_id` — links ERP projects to Finance invoices

## Audit Columns (present on all Bronze records)

- `_source` — name of the originating system
- `_load_timestamp` — UTC timestamp of ingestion
- `_ingestion_batch_id` — unique identifier for the ingestion run
