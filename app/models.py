from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Float, BigInteger, Boolean, DateTime, Index
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Transaction(Base):
    __tablename__ = "transactions"

    # Kaggle IEEE-CIS keys
    transaction_id = Column(BigInteger, primary_key=True, index=True)   # TransactionID
    transaction_dt = Column(BigInteger, index=True)                     # TransactionDT (seconds from reference)
    amount = Column(Float, index=True)                                  # TransactionAmt
    product_cd = Column(String(10), index=True)                         # ProductCD

    # Common card/address fields (exist in dataset)
    card1 = Column(BigInteger, index=True, nullable=True)
    card2 = Column(BigInteger, index=True, nullable=True)
    card4 = Column(String(32), index=True, nullable=True)
    card6 = Column(String(16), index=True, nullable=True)
    addr1 = Column(BigInteger, index=True, nullable=True)
    addr2 = Column(BigInteger, index=True, nullable=True)

    # Label (optional, but present in train)
    is_fraud = Column(Boolean, index=True, nullable=True)               # isFraud

    # Ingestion metadata
    ingested_at = Column(DateTime, default=datetime.utcnow, index=True)

Index("ix_transactions_amount_dt", Transaction.amount, Transaction.transaction_dt)
