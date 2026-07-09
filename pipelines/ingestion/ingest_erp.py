
"""
Ingestion: ERP (project management) source -> Bronze layer.
Simulates a scheduled pull from the firm's project management/ERP system.
"""
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bronze"))
from bronze_writer import write_bronze

def ingest_erp_projects(source_path="sources/erp_projects.csv"):
    df = pd.read_csv(source_path)
    return write_bronze(df, source_name="erp_projects")

if __name__ == "__main__":
    ingest_erp_projects()
