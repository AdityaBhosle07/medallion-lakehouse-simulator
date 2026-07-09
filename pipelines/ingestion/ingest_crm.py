
"""
Ingestion: CRM source -> Bronze layer.
"""
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bronze"))
from bronze_writer import write_bronze

def ingest_crm_clients(source_path="sources/crm_clients.csv"):
    df = pd.read_csv(source_path)
    return write_bronze(df, source_name="crm_clients")

if __name__ == "__main__":
    ingest_crm_clients()
