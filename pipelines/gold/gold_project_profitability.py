
"""
Gold layer: Project Profitability.
Business-ready aggregated dataset for project profitability analysis.
"""
import pandas as pd
import os

SILVER_PATH = "silver/silver_joined.csv"
GOLD_PATH = "gold"

def build_project_profitability():
    df = pd.read_csv(SILVER_PATH)
    df["profit"] = df["total_invoiced"] - df["actual_cost"]
    df["profit_margin_pct"] = (df["profit"] / df["total_invoiced"].replace(0, float("nan")) * 100).round(2)
    df["budget_variance"] = df["budget"] - df["actual_cost"]

    result = df[[
        "project_id","project_name","project_type","status",
        "budget","actual_cost","total_invoiced","profit","profit_margin_pct","budget_variance"
    ]].sort_values("profit", ascending=False)
    return result

if __name__ == "__main__":
    os.makedirs(GOLD_PATH, exist_ok=True)
    df = build_project_profitability()
    df.to_csv(f"{GOLD_PATH}/gold_project_profitability.csv", index=False)
    print(f"[GOLD] gold_project_profitability.csv written with {len(df)} rows")
