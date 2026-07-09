
"""
Bronze layer writer — writes raw, unmodified source data with audit metadata.
Preserves original data exactly as it arrived (append-only, immutable).
"""
import pandas as pd
import os
from datetime import datetime

BRONZE_PATH = "bronze"

def write_bronze(df: pd.DataFrame, source_name: str, load_ts: str = None) -> str:
    os.makedirs(BRONZE_PATH, exist_ok=True)
    load_ts = load_ts or datetime.utcnow().strftime("%Y%m%dT%H%M%S")

    df = df.copy()
    df["_source"] = source_name
    df["_load_timestamp"] = load_ts
    df["_ingestion_batch_id"] = f"{source_name}_{load_ts}"

    out_path = os.path.join(BRONZE_PATH, f"{source_name}_{load_ts}.csv")
    df.to_csv(out_path, index=False)
    print(f"[BRONZE] Wrote {len(df)} rows -> {out_path}")
    return out_path
