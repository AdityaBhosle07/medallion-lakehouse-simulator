
"""
Serving layer: FastAPI app exposing Gold tables to dashboards/AI applications.
"""
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pandas as pd

import math
from fastapi import HTTPException

def clean_nans(records):
    for row in records:
        for k, v in row.items():
            if isinstance(v, float) and math.isnan(v):
                row[k] = None
    return records


app = FastAPI(title="Lake Flato Lakehouse Serving API", version="1.0")

GOLD_PATH = "gold"

@app.get("/")
def root():
    return {"message": "Medallion Lakehouse Serving API", "endpoints": [
        "/api/profitability", "/api/utilization", "/api/benchmarking"
    ]}

@app.get("/api/profitability")
def get_profitability():
    try:
        df = pd.read_csv(f"{GOLD_PATH}/gold_project_profitability.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="gold_project_profitability.csv not found. Run the Gold layer pipeline first.")
    records = df.to_dict(orient="records")
    records = clean_nans(records)
    return jsonable_encoder(records)

@app.get("/api/utilization")
def get_utilization():
    try:
        df = pd.read_csv(f"{GOLD_PATH}/gold_utilization_analytics.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="gold_utilization_analytics.csv not found. Run the Gold layer pipeline first.")
    records = df.to_dict(orient="records")
    records = clean_nans(records)
    return jsonable_encoder(records)

@app.get("/api/benchmarking")
def get_benchmarking():
    try:
        df = pd.read_csv(f"{GOLD_PATH}/gold_fee_benchmarking.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="gold_fee_benchmarking.csv not found. Run the Gold layer pipeline first.")
    records = df.to_dict(orient="records")
    records = clean_nans(records)
    return jsonable_encoder(records)
