# Runbook: Adding a New Data Source

This guide explains how to onboard a new data source into the lakehouse, following the
existing Bronze -> Silver -> Gold pattern.

## Step 1: Add the Source
Place the new source file (CSV, JSON, or API response) into `sources/`, or point directly
to the live API endpoint if ingesting in real time.

## Step 2: Write an Ingestion Script
Create a new file in `pipelines/ingestion/`, following the pattern of `ingest_erp.py`:
1. Read the source data into a DataFrame.
2. Call `write_bronze(df, source_name="your_source_name")`.
3. Run the script to confirm a timestamped file appears in `bronze/`.

## Step 3: Write a Silver Cleaning Script
Create a new file in `pipelines/silver/`:
1. Load the latest Bronze file using the `latest_bronze()` helper pattern.
2. Deduplicate on the natural key (e.g., an ID column).
3. Standardize text fields (trim, title-case) and numeric fields (coerce, fill nulls).
4. Convert date fields with `pd.to_datetime(..., errors="coerce")`.
5. Output a clean, standardized Silver CSV.

## Step 4: Join Into Silver (If Applicable)
If the new source relates to existing entities (e.g., shares a `project_id` or `client_id`),
add a merge step in `join_silver_tables.py` to incorporate it into `silver_joined.csv`.

## Step 5: Update or Add Gold Tables
If the new source enables a new business metric, add a new script in `pipelines/gold/`,
or extend an existing Gold aggregation to include the new field.

## Step 6: Update Lineage Documentation
Add a new row to `docs/data_lineage.md` tracing any new Gold fields back to this source.

## Step 7: Add a Monitoring Check
Add the new source name to `EXPECTED_MIN_ROWS` in `pipeline_health_check.py` so pipeline
health monitoring covers it automatically.
