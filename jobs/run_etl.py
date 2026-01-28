import os
import time
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv

from app.db import SessionLocal
from app.models import Transaction

load_dotenv()

KEEP_COLS = [
    "TransactionID",
    "TransactionDT",
    "TransactionAmt",
    "ProductCD",
    "card1",
    "card2",
    "card4",
    "card6",
    "addr1",
    "addr2",
    "isFraud",
]

def _safe_bool(x):
    if pd.isna(x):
        return None
    return bool(int(x))

def run_etl_job(dataset_path: str, chunksize: int = 50_000):
    if not os.path.exists(dataset_path):
        return {"ok": False, "error": f"Dataset not found at {dataset_path}"}

    start = time.time()
    total_rows = 0
    inserted = 0

    db: Session = SessionLocal()
    try:
        # simple idempotency: clear table before reload (demo-friendly)
        db.execute(text("DELETE FROM transactions"))
        db.commit()

        for chunk in pd.read_csv(dataset_path, usecols=lambda c: c in KEEP_COLS, chunksize=chunksize):
            # Normalize column names
            df = chunk.rename(columns={
                "TransactionID": "transaction_id",
                "TransactionDT": "transaction_dt",
                "TransactionAmt": "amount",
                "ProductCD": "product_cd",
                "isFraud": "is_fraud",
            })

            INT_COLS = ["transaction_id", "transaction_dt"]

            for c in INT_COLS:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

            # Convert pandas NA / NaN → Python None for SQLAlchemy
            df = df.replace({np.nan: None})
            df = df.astype(object).where(pd.notnull(df), None)

            if "is_fraud" in df.columns:
                df["is_fraud"] = df["is_fraud"].apply(_safe_bool)

            # Replace NaN with None for DB inserts
            records = df.where(pd.notnull(df), None).to_dict(orient="records")

            objs = [Transaction(**r) for r in records]
            db.bulk_save_objects(objs)
            db.commit()

            total_rows += len(records)
            inserted += len(records)

        elapsed = time.time() - start
        rps = inserted / elapsed if elapsed > 0 else inserted

        return {
            "ok": True,
            "dataset_path": dataset_path,
            "rows_loaded": inserted,
            "seconds": round(elapsed, 2),
            "rows_per_sec": round(rps, 2),
            "note": "Demo ETL clears table before reload for idempotency.",
        }

    except Exception as e:
        db.rollback()
        return {"ok": False, "error": str(e)}
    finally:
        db.close()
