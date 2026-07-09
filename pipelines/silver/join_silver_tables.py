
"""
Silver layer: joins ERP + HR + CRM + Finance into unified, analysis-ready tables.
This is the core "Silver" step: combining related datasets across systems.
"""
import pandas as pd
import glob, os
from clean_erp import clean_erp_projects
from clean_hr import clean_hr_employees
from clean_crm import clean_crm_clients

def latest_bronze(source_name, bronze_dir="bronze"):
    files = sorted(glob.glob(os.path.join(bronze_dir, f"{source_name}_*.csv")))
    return files[-1]

def clean_finance_invoices(bronze_dir="bronze"):
    df = pd.read_csv(latest_bronze("finance_invoices", bronze_dir))
    df = df.drop_duplicates(subset="invoice_id")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df = df.dropna(subset=["invoice_id", "project_id"])
    return df[["invoice_id","project_id","amount","fee_type","invoice_date"]]

def build_joined_silver():
    projects = clean_erp_projects()
    employees = clean_hr_employees()
    clients = clean_crm_clients()
    invoices = clean_finance_invoices()

    projects_clients = projects.merge(clients, on="client_id", how="left")
    projects_full = projects_clients.merge(
        employees.rename(columns={"employee_id": "relationship_manager"}),
        on="relationship_manager", how="left", suffixes=("", "_manager")
    )
    invoices_summary = invoices.groupby("project_id").agg(
        total_invoiced=("amount", "sum"),
        invoice_count=("invoice_id", "count")
    ).reset_index()

    joined = projects_full.merge(invoices_summary, on="project_id", how="left")
    joined["total_invoiced"] = joined["total_invoiced"].fillna(0)
    joined["invoice_count"] = joined["invoice_count"].fillna(0)
    return joined

if __name__ == "__main__":
    os.makedirs("silver", exist_ok=True)
    df = build_joined_silver()
    df.to_csv("silver/silver_joined.csv", index=False)
    print(f"[SILVER] silver_joined.csv written with {len(df)} rows")
