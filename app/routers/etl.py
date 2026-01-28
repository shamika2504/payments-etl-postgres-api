import os
from fastapi import APIRouter
from jobs.run_etl import run_etl_job

router = APIRouter()

@router.post("/etl/run")
def run_etl():
    dataset_path = os.getenv("DATASET_PATH", "./data/train_transaction.csv")
    result = run_etl_job(dataset_path=dataset_path)
    return result
