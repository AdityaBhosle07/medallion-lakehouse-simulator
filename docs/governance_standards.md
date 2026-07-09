# Data Governance and Quality Standards

## Principles
- Bronze data is immutable and never modified after ingestion — it serves as the audit trail.
- Silver-layer transformations must be deterministic and reproducible from Bronze.
- Data quality issues are surfaced (logged, flagged) rather than silently masked or dropped.

## Standards Applied
- **Deduplication:** All Silver tables deduplicate on their natural primary key.
- **Null Handling:** Numeric nulls are filled with sensible defaults (0 or median) and logged;
  records missing a primary key are dropped and counted.
- **Type Standardization:** Dates are parsed with `errors="coerce"` to catch malformed values
  rather than failing the whole pipeline silently.
- **Text Standardization:** Categorical text fields (status, department, industry) are trimmed
  and title-cased for consistent grouping in Gold aggregations.

## Ownership
- Each source has a designated ingestion script owner responsible for schema changes upstream.
- Gold table definitions are reviewed whenever a new business question requires a new metric.
