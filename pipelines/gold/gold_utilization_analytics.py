
"""
Gold layer: Utilization Analytics.
Business-ready dataset summarizing employee utilization by department.
"""
import pandas as pd
import os

EMPLOYEES_PATH = "silver/silver_employees.csv"
GOLD_PATH = "gold"

def build_utilization_analytics():
    df = pd.read_csv(EMPLOYEES_PATH)
    dept_summary = df.groupby("department").agg(
        avg_utilization_pct=("utilization_pct", "mean"),
        avg_hourly_rate=("hourly_rate", "mean"),
        headcount=("employee_id", "count")
    ).reset_index()
    dept_summary["avg_utilization_pct"] = (dept_summary["avg_utilization_pct"] * 100).round(1)
    dept_summary["avg_hourly_rate"] = dept_summary["avg_hourly_rate"].round(2)
    return dept_summary.sort_values("avg_utilization_pct", ascending=False)

if __name__ == "__main__":
    os.makedirs(GOLD_PATH, exist_ok=True)
    df = build_utilization_analytics()
    df.to_csv(f"{GOLD_PATH}/gold_utilization_analytics.csv", index=False)
    print(f"[GOLD] gold_utilization_analytics.csv written with {len(df)} rows")
