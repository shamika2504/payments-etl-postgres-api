from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from cachetools import TTLCache
from app.db import get_db
from app import crud
from app.schemas import SummaryMetrics, AnomaliesResponse

router = APIRouter()

# Basic caching to show “engineering maturity”
_cache = TTLCache(maxsize=128, ttl=30)

@router.get("/metrics/summary", response_model=SummaryMetrics)
def metrics_summary(db: Session = Depends(get_db)):
    key = "summary"
    if key in _cache:
        return _cache[key]

    total, total_amount, avg_amount, fraud_rate = crud.summary_metrics(db)
    resp = {
        "total_transactions": total,
        "total_amount": total_amount,
        "avg_amount": avg_amount,
        "fraud_rate": fraud_rate,
    }
    _cache[key] = resp
    return resp

@router.get("/metrics/anomalies", response_model=AnomaliesResponse)
def anomalies(
    threshold: float = Query(4.0, ge=1.0, le=10.0),
    top_n: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db),
):
    mean, std, items = crud.anomalies_amount_zscore(db, threshold=threshold, limit=top_n)
    resp_items = [
        {"transaction_id": i.transaction_id, "amount": i.amount, "reason": f"z-score >= {threshold:.2f}"}
        for i in items
    ]
    return {
        "method": "zscore_amount",
        "threshold": threshold,
        "count": len(resp_items),
        "items": resp_items,
    }
