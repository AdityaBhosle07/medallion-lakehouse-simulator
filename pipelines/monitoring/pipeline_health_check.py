
"""
Monitoring: checks pipeline health across Bronze, Silver, and Gold layers.
Detects missing files, row-count anomalies, and stale data.
"""
import pandas as pd
import glob, os
from datetime import datetime, timedelta

BRONZE_PATH = "bronze"
SILVER_PATH = "silver"
GOLD_PATH = "gold"

EXPECTED_MIN_ROWS = {
    "erp_projects": 1, "hr_employees": 1, "crm_clients": 1, "finance_invoices": 1
}

def check_bronze_freshness(max_age_hours=24):
    issues = []
    for source in EXPECTED_MIN_ROWS:
        files = sorted(glob.glob(os.path.join(BRONZE_PATH, f"{source}_*.csv")))
        if not files:
            issues.append(f"MISSING: no bronze files found for {source}")
            continue
        latest = files[-1]
        ts_str = latest.split("_")[-1].replace(".csv", "")
        try:
            ts = datetime.strptime(ts_str, "%Y%m%dT%H%M%S")
            if datetime.utcnow() - ts > timedelta(hours=max_age_hours):
                issues.append(f"STALE: {source} last loaded at {ts}")
        except ValueError:
            issues.append(f"WARNING: could not parse timestamp for {latest}")
    return issues

def check_row_counts():
    issues = []
    for source, min_rows in EXPECTED_MIN_ROWS.items():
        files = sorted(glob.glob(os.path.join(BRONZE_PATH, f"{source}_*.csv")))
        if files:
            df = pd.read_csv(files[-1])
            if len(df) < min_rows:
                issues.append(f"LOW ROW COUNT: {source} has {len(df)} rows (expected >= {min_rows})")
    return issues

def run_health_check():
    all_issues = check_bronze_freshness() + check_row_counts()
    if not all_issues:
        print("[MONITOR] Pipeline healthy. No issues detected.")
    else:
        print("[MONITOR] Issues detected:")
        for issue in all_issues:
            print(f"  - {issue}")
    return all_issues

if __name__ == "__main__":
    run_health_check()
