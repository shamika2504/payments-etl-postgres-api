from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud
from app.schemas import PaginatedTransactions, TransactionOut

router = APIRouter()

@router.get("/transactions", response_model=PaginatedTransactions)
def get_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    total, items = crud.list_transactions(db, page=page, limit=limit)
    return {"page": page, "limit": limit, "total": total, "items": items}

@router.get("/transactions/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tx = crud.get_transaction(db, transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx
