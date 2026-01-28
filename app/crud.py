from sqlalchemy.orm import Session
from sqlalchemy import func, Integer, case
from app.models import Transaction

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()

def list_transactions(db: Session, page: int, limit: int):
    limit = max(1, min(limit, 200))
    page = max(1, page)

    total = db.query(func.count(Transaction.transaction_id)).scalar() or 0
    offset = (page - 1) * limit

    items = (
        db.query(Transaction)
        .order_by(Transaction.transaction_id.asc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return total, items

def summary_metrics(db: Session):
    total = db.query(func.count(Transaction.transaction_id)).scalar() or 0
    total_amount = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).scalar() or 0.0
    avg_amount = db.query(func.coalesce(func.avg(Transaction.amount), 0.0)).scalar() or 0.0

    # Count frauds safely (works even if is_fraud has NULLs)
    fraud_count = db.query(
        func.coalesce(
            func.sum(
                case((Transaction.is_fraud.is_(True), 1), else_=0)
            ),
            0
        )
    ).scalar()

    fraud_rate = float(fraud_count) / float(total) if total > 0 else 0.0

    return int(total), float(total_amount), float(avg_amount), float(fraud_rate)

def anomalies_amount_zscore(db: Session, threshold: float, limit: int = 50):
    # Simple “scale signal” logic: statistical outlier detection (z-score)
    stats = db.query(
        func.avg(Transaction.amount),
        func.stddev_pop(Transaction.amount)
    ).first()

    mean = stats[0] or 0.0
    std = stats[1] or 0.0
    if std == 0:
        return mean, std, []

    # |x-mean| / std >= threshold
    items = (
        db.query(Transaction)
        .filter(func.abs(Transaction.amount - mean) / std >= threshold)
        .order_by(Transaction.amount.desc())
        .limit(limit)
        .all()
    )
    return float(mean), float(std), items
