# Runbook: Troubleshooting Pipeline Failures

## Issue: Ingestion script fails with "No bronze files found"
**Cause:** The source file is missing, moved, or misnamed.
**Fix:** Verify the file exists in `sources/` and matches the expected filename in the
ingestion script. Re-run the ingestion script.

## Issue: Silver script fails with a KeyError on a column
**Cause:** The source schema changed (a column was renamed, removed, or added upstream).
**Fix:** Check the latest Bronze file's columns against what the Silver script expects.
Update the Silver script's column mapping if the schema has legitimately changed, and note
the change in `docs/data_lineage.md`.

## Issue: Gold table has unexpected null or zero values
**Cause:** Usually a failed join (e.g., a `project_id` in Finance invoices that does not
exist in ERP projects) or a Silver-layer null that wasn't handled.
**Fix:** Check `pipeline_health_check.py` output first. Then inspect the specific Silver
table for orphaned keys using a simple anti-join (`merge(..., how="left", indicator=True)`).

## Issue: pipeline_health_check.py reports "STALE" data
**Cause:** An ingestion script did not run on schedule, or failed silently upstream.
**Fix:** Check the scheduler logs (`orchestration/scheduler.py` if configured) and re-run
the affected ingestion script manually.

## Issue: Serving API returns empty results
**Cause:** Gold tables were not regenerated after a Silver-layer change.
**Fix:** Re-run all scripts in `pipelines/gold/` in order after any Silver-layer update.

## General Debugging Order
1. Check Bronze — does the raw file exist and have rows?
2. Check Silver — did cleaning/joining produce the expected row count?
3. Check Gold — did aggregation logic run without silent failures (e.g., NaN from failed merges)?
4. Check Monitoring — run `pipeline_health_check.py` to catch freshness/row-count issues automatically.
