from pydantic import BaseModel
from typing import Optional, List

class TransactionOut(BaseModel):
    transaction_id: int
    transaction_dt: int
    amount: float
    product_cd: Optional[str] = None
    card1: Optional[int] = None
    card2: Optional[int] = None
    card4: Optional[str] = None
    card6: Optional[str] = None
    addr1: Optional[int] = None
    addr2: Optional[int] = None
    is_fraud: Optional[bool] = None

    class Config:
        from_attributes = True

class PaginatedTransactions(BaseModel):
    page: int
    limit: int
    total: int
    items: List[TransactionOut]

class SummaryMetrics(BaseModel):
    total_transactions: int
    total_amount: float
    avg_amount: float
    fraud_rate: Optional[float] = None

class AnomalyItem(BaseModel):
    transaction_id: int
    amount: float
    reason: str

class AnomaliesResponse(BaseModel):
    method: str
    threshold: float
    count: int
    items: List[AnomalyItem]
