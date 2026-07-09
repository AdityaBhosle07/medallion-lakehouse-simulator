
"""
Silver layer: ERP projects cleaning and standardization.
- Removes duplicates
- Standardizes field names/types
- Handles missing values
"""
import pandas as pd
import glob, os

def latest_bronze(source_name, bronze_dir="bronze"):
    files = sorted(glob.glob(os.path.join(bronze_dir, f"{source_name}_*.csv")))
    if not files:
        raise FileNotFoundError(f"No bronze files found for {source_name}")
    return files[-1]

def clean_erp_projects(bronze_dir="bronze"):
    df = pd.read_csv(latest_bronze("erp_projects", bronze_dir))
    df = df.drop_duplicates(subset="project_id")
    df["status"] = df["status"].str.strip().str.title()
    df["project_type"] = df["project_type"].str.strip().str.title()
    df["budget"] = pd.to_numeric(df["budget"], errors="coerce").fillna(0)
    df["actual_cost"] = pd.to_numeric(df["actual_cost"], errors="coerce").fillna(0)
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df = df.dropna(subset=["project_id", "client_id"])
    return df[["project_id","project_name","client_id","project_type","status","budget","actual_cost","start_date"]]

if __name__ == "__main__":
    os.makedirs("silver", exist_ok=True)
    clean_erp_projects().to_csv("silver/silver_projects.csv", index=False)
    print("[SILVER] silver_projects.csv written")
