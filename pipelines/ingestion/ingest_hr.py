
"""
Ingestion: HR system source -> Bronze layer.
"""
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bronze"))
from bronze_writer import write_bronze

def ingest_hr_employees(source_path="sources/hr_employees.csv"):
    df = pd.read_csv(source_path)
    return write_bronze(df, source_name="hr_employees")

if __name__ == "__main__":
    ingest_hr_employees()
