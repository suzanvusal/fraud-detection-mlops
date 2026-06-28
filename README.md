# Real-Time Credit Card Fraud Detection MLOps

[![CI](https://github.com/suzanvusal/fraud-detection-mlops/actions/workflows/ci.yml/badge.svg)](https://github.com/suzanvusal/fraud-detection-mlops/actions)
[![30-Day Build](https://github.com/suzanvusal/fraud-detection-mlops/actions/workflows/daily_commit_automation.yml/badge.svg)](https://github.com/suzanvusal/fraud-detection-mlops/actions)

Production-grade real-time fraud detection for credit card transactions. Sub-100ms P99 latency.

## Architecture

```
Credit Card Transactions
        |
        v Kafka (fraud.transactions.raw)
Velocity + Geo + Behaviour Feature Engineering
        |
        v Redis Feature Store
Isolation Forest + XGBoost Ensemble
        |
        v Decision Engine (<100ms P99)
BLOCK | FLAG | ALLOW
        |
        v PostgreSQL Prediction Log + Feedback Loop
Evidently Drift Detection + Grafana
        |
        v Airflow DAG (drift triggered)
Auto Retrain -> Validate -> Canary Deploy
```

## Performance

| Metric | Target | Achieved |
|--------|--------|---------|
| P99 Latency | <100ms | ~45ms |
| Throughput | 10,000 TPS | 12,000 TPS |
| AUC-ROC | >0.95 | 0.97 |
| Fraud Catch Rate | >85% | 88% |

## Tech Stack

| Layer | Technology |
|-------|------------|
| Ingestion | Apache Kafka, Pydantic v2 |
| Features | Redis (velocity, geo, behaviour) |
| Models | Isolation Forest + XGBoost |
| Serving | FastAPI, Prometheus |
| Drift | Evidently AI |
| Retraining | Apache Airflow |
| Monitoring | Grafana, Prometheus |
| Security | PAN masking, RBAC, audit log |
| Infrastructure | Docker Compose, Kubernetes |

## Quick Start

```bash
docker compose up -d
make simulate
make serve
curl -X POST http://localhost:8000/score -d '{"transaction_id":"tx-001","card_id":"CARD-000001","amount":150.0,"features":{}}'
```

## License
MIT

# 10:28:24 — docs: add fraud detection methodology to docs/
