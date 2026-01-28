from fastapi import FastAPI
from app.models import Base
from app.db import engine
from app.routers import health, etl, transactions, metrics

app = FastAPI(
    title="Payments ETL + Postgres API",
    description="ETL pipeline + Postgres-backed APIs using the IEEE-CIS transaction dataset.",
    version="1.0.0",
)

# Create tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(etl.router)
app.include_router(transactions.router)
app.include_router(metrics.router)

@app.get("/")
def root():
    return {"service": "payments-etl-postgres-api", "docs": "/docs", "health": "/health"}
