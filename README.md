# Real-Time Credit Card Fraud Detection MLOps

Production-grade fraud detection pipeline processing credit card transactions in real-time with sub-100ms P99 latency.

## Architecture

```
Credit Card Transactions
        |
        v Kafka
Velocity + Geo + Behaviour Feature Engineering
        |
        v Redis Feature Store
Isolation Forest + XGBoost Ensemble
        |
        v Decision Engine (<100ms P99)
BLOCK | FLAG | ALLOW
        |
        v Feedback Loop
Evidently Drift Detection
        |
        v Airflow DAG
Auto Retrain -> Validate -> Canary Deploy
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Ingestion | Apache Kafka, Pydantic |
| Features | Redis (velocity, geo, behaviour) |
| Models | Isolation Forest + XGBoost ensemble |
| Serving | FastAPI (<100ms P99) |
| Drift | Evidently AI |
| Retraining | Apache Airflow |
| Monitoring | Prometheus, Grafana |

## Quick Start

```bash
docker compose up -d
make simulate
make serve
```

## License
MIT
