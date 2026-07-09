
"""
Silver layer: CRM clients cleaning and standardization.
"""
import pandas as pd
import glob, os

def latest_bronze(source_name, bronze_dir="bronze"):
    files = sorted(glob.glob(os.path.join(bronze_dir, f"{source_name}_*.csv")))
    return files[-1]

def clean_crm_clients(bronze_dir="bronze"):
    df = pd.read_csv(latest_bronze("crm_clients", bronze_dir))
    df = df.drop_duplicates(subset="client_id")
    df["industry"] = df["industry"].str.strip().str.title()
    df["client_since"] = pd.to_datetime(df["client_since"], errors="coerce")
    df = df.dropna(subset=["client_id"])
    return df[["client_id","client_name","industry","relationship_manager","client_since"]]

if __name__ == "__main__":
    os.makedirs("silver", exist_ok=True)
    clean_crm_clients().to_csv("silver/silver_clients.csv", index=False)
    print("[SILVER] silver_clients.csv written")
