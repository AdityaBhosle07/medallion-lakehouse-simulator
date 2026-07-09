
"""
Ingestion: Finance invoices "REST API" source -> Bronze layer.
Simulates pulling paginated invoice data from an external finance API.
"""
import pandas as pd
import json, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bronze"))
from bronze_writer import write_bronze

def ingest_finance_invoices(source_path="sources/finance_invoices_api.json"):
    with open(source_path) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return write_bronze(df, source_name="finance_invoices")

if __name__ == "__main__":
    ingest_finance_invoices()
