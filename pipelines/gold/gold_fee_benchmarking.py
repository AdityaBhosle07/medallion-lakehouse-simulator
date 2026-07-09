
"""
Gold layer: Fee Benchmarking.
Business-ready dataset comparing fee structures and amounts by project type.
"""
import pandas as pd
import os

SILVER_PATH = "silver/silver_joined.csv"
GOLD_PATH = "gold"

def build_fee_benchmarking():
    df = pd.read_csv(SILVER_PATH)
    benchmark = df.groupby("project_type").agg(
        avg_budget=("budget", "mean"),
        avg_actual_cost=("actual_cost", "mean"),
        avg_total_invoiced=("total_invoiced", "mean"),
        project_count=("project_id", "count")
    ).reset_index()
    for col in ["avg_budget", "avg_actual_cost", "avg_total_invoiced"]:
        benchmark[col] = benchmark[col].round(2)
    return benchmark.sort_values("avg_total_invoiced", ascending=False)

if __name__ == "__main__":
    os.makedirs(GOLD_PATH, exist_ok=True)
    df = build_fee_benchmarking()
    df.to_csv(f"{GOLD_PATH}/gold_fee_benchmarking.csv", index=False)
    print(f"[GOLD] gold_fee_benchmarking.csv written with {len(df)} rows")
