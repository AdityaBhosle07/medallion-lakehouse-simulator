
"""
Silver layer: HR employees cleaning and standardization.
"""
import pandas as pd
import glob, os

def latest_bronze(source_name, bronze_dir="bronze"):
    files = sorted(glob.glob(os.path.join(bronze_dir, f"{source_name}_*.csv")))
    return files[-1]

def clean_hr_employees(bronze_dir="bronze"):
    df = pd.read_csv(latest_bronze("hr_employees", bronze_dir))
    df = df.drop_duplicates(subset="employee_id")
    df["department"] = df["department"].str.strip().str.title()
    df["hourly_rate"] = pd.to_numeric(df["hourly_rate"], errors="coerce").fillna(df["hourly_rate"].median())
    df["utilization_pct"] = pd.to_numeric(df["utilization_pct"], errors="coerce").clip(0, 1)
    df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")
    df = df.dropna(subset=["employee_id"])
    return df[["employee_id","employee_name","department","hire_date","hourly_rate","utilization_pct"]]

if __name__ == "__main__":
    os.makedirs("silver", exist_ok=True)
    clean_hr_employees().to_csv("silver/silver_employees.csv", index=False)
    print("[SILVER] silver_employees.csv written")
