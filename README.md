# 💳 Payments Transactions ETL & Analytics API

A production-style backend system for ingesting, storing, and analyzing large-scale payments transaction data.  
This project focuses on **data engineering, backend APIs, and scale-readiness**, rather than model accuracy.

---

## 1️⃣ Business Problem

### What problem is being solved?

Financial institutions need to **ingest millions of payment transactions daily** and provide:

- Fast access to transaction records
- Aggregated metrics for fraud monitoring
- Early signals for anomalous transaction behavior

This system simulates a **payments analytics backend** that supports downstream fraud analysis and reporting teams.

### Metric to optimize

- **Throughput**: rows ingested per second
- **Latency**: API response time for analytics queries
- **Reliability**: idempotent ETL runs without data corruption

> This project intentionally optimizes **system performance and correctness**, not ML accuracy.

### Baseline to beat

- Naive CSV → DB ingestion without chunking
- Full-table scans for every analytics query

This project improves upon that by:
- Chunked ETL ingestion
- Pre-aggregated and optimized queries
- Pagination and basic caching

---

## 2️⃣ Data Pipeline

### Dataset

- **Source**: IEEE-CIS Fraud Detection Dataset (Kaggle)  
  https://www.kaggle.com/c/ieee-fraud-detection
- **Scale**: ~590,000 transactions
- **Original schema**: 400+ columns
- **Used schema**: 10 transaction-relevant columns

### Pipeline Flow

```text
CSV (Kaggle)
 → Column selection
 → Schema normalization
 → Type-safe casting
 → Chunked ingestion
 → PostgreSQL
```
### Key data challenges

- Extremely wide schema (400+ columns)
- Mixed numeric + categorical data
- Missing values and inconsistent types
- Large file size unsuitable for in-memory ingestion

### Feature engineering — WHY these columns?

Only fields relevant to transaction identity, amount, card metadata, and fraud labeling were retained:

- Reduces schema complexity
- Improves ingestion speed
- Matches real-world payments tables used in production systems

### Validation strategy

- Row count validation after ingestion
- Type validation before insert
- Idempotent ETL (table cleared before reload)
- Schema constraints enforced at DB level

---

## 3️⃣ Model / Analytics Development

This project intentionally does not train a predictive ML model.

### What experimentation was done?

- Batch profiling of transaction amounts
- Fraud-rate aggregation
- High-value transaction anomaly detection using statistical thresholds

### Why this approach?

In many production payment systems:

- Analytics precede ML.
- Clean ETL + reliable metrics are prerequisites for modeling.
- Rule-based and statistical checks are often deployed before ML.

This mirrors real enterprise pipelines.

---

## 4️⃣ Production Considerations

### Deployment strategy

- Local development using Docker Compose (Postgres)
- FastAPI service exposing ETL and analytics endpoints
- Stateless API design
- Database as the system of record

### Core APIs

- ```POST /etl/run``` — run ETL job
- ```GET /transactions``` — paginated transaction access
- ```GET /metrics/summary``` — aggregate metrics
- ```GET /metrics/anomalies``` — outlier detection
- ```GET /health``` — service health check

### Monitoring plan (conceptual)

- ETL runtime & rows/sec
- API latency per endpoint
- Error rate on DB inserts
- Daily transaction volume deltas

#### Failure modes & fallbacks

```
| Failure                 | Mitigation                   |
| ----------------------- | ---------------------------- |
| CSV schema change       | Explicit column selection    |
| Partial ETL failure     | Idempotent reload            |
| Large values overflow   | Safe casting + schema tuning |
| Heavy analytics queries | Pagination + caching         |
```

---

## 5️⃣ Scale Signals

### Current performance (local)

```
{
  "rows_loaded": 590540,
  "seconds": 51.23,
  "rows_per_sec": 11526.47
}
```

### What would change at larger scale?

- Partition tables by date
- Incremental ingestion instead of full reloads
- Redis for shared caching
- Materialized views for metrics
- Move batch jobs to Spark or scheduled workflows (Airflow)

---

## 6️⃣ Project Structure

```
payments-etl-postgres-api/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── etl.py
│       ├── transactions.py
│       └── metrics.py
│
├── jobs/
│   ├── run_etl.py
│   └── profile_data.py
│
├── data/
│   └── train_transaction.csv
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 7️⃣ Why This Project

This project was built to demonstrate:

- Backend API design
- Data engineering fundamentals
- ETL reliability at scale
- Real-world payments data handling
- Production thinking beyond toy ML models

It aligns closely with FinTech, payments, and enterprise data platform roles.

---

📌 License

MIT License