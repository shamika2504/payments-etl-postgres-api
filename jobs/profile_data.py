import os
import time
import pandas as pd
from dotenv import load_dotenv

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

def profile_csv(dataset_path: str, sample_rows: int = 200_000):
    if not os.path.exists(dataset_path):
        return {"ok": False, "error": f"Dataset not found: {dataset_path}"}

    t0 = time.time()
    df = pd.read_csv(dataset_path, usecols=lambda c: c in KEEP_COLS, nrows=sample_rows)

    out = {
        "ok": True,
        "dataset_path": dataset_path,
        "rows_sampled": int(len(df)),
        "seconds": round(time.time() - t0, 2),
        "null_rates": {c: float(df[c].isna().mean()) for c in df.columns},
        "amount": {
            "min": float(df["TransactionAmt"].min()),
            "p50": float(df["TransactionAmt"].median()),
            "p95": float(df["TransactionAmt"].quantile(0.95)),
            "p99": float(df["TransactionAmt"].quantile(0.99)),
            "max": float(df["TransactionAmt"].max()),
        },
        "fraud_rate": float(df["isFraud"].mean()) if "isFraud" in df.columns else None,
        "top_product_cd": df["ProductCD"].value_counts().head(5).to_dict(),
        "top_card4": df["card4"].value_counts().head(5).to_dict(),
    }
    return out

if __name__ == "__main__":
    path = os.getenv("DATASET_PATH", "./data/train_transaction.csv")
    print(profile_csv(path))
