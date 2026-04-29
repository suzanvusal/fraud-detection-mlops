#!/usr/bin/env python3
"""Bootstrap fraud-detection-mlops repo. Run once locally."""
import argparse
import subprocess
from pathlib import Path

DIRS = [
    "src/ingestion", "src/features", "src/models", "src/serving",
    "src/decision", "src/monitoring", "src/security", "src/retraining",
    "infra/docker", "infra/k8s", "infra/grafana/dashboards",
    "infra/prometheus", "infra/airflow",
    "tests/unit", "tests/integration", "tests/load",
    "notebooks", "docs/runbooks", "scripts", "configs",
    ".github/workflows", ".automation_state", "plan", "templates"
]

BASE_FILES = {
"README.md": """\
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
""",

"pyproject.toml": """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "fraud-detection-mlops"
version = "0.1.0"
description = "Real-time credit card fraud detection MLOps system"
requires-python = ">=3.11"
dependencies = [
    "kafka-python>=2.0.2",
    "redis>=5.0.1",
    "pydantic>=2.5.0",
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "xgboost>=2.0.2",
    "scikit-learn>=1.3.2",
    "mlflow>=2.9.2",
    "evidently>=0.4.11",
    "apache-airflow>=2.7.3",
    "prometheus-client>=0.19.0",
    "optuna>=3.4.0",
    "shap>=0.43.0",
    "numpy>=1.26.2",
    "pandas>=2.1.4",
    "asyncpg>=0.29.0",
    "orjson>=3.9.10",
    "pyyaml>=6.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "pytest-cov>=4.1.0",
    "black>=23.11.0",
    "ruff>=0.1.7",
    "mypy>=1.7.1",
    "locust>=2.19.1",
    "bandit>=1.7.6",
]

[tool.black]
line-length = 88

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
""",

"Makefile": """\
.PHONY: up down test lint serve simulate

up:
\tdocker compose up -d
\t@echo "✓ Stack started"

down:
\tdocker compose down -v

test:
\tpytest tests/ -v --cov=src --cov-report=term-missing

lint:
\truff check src/ tests/ --fix

serve:
\tuvicorn src.serving.api:app --reload --port 8000

simulate:
\tpython -m src.ingestion.simulator --transactions 10000 --fraud-rate 0.05

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
""",

"configs/base_config.yaml": """\
kafka:
  bootstrap_servers: "localhost:9092"
  topics:
    transactions: "fraud.transactions.raw"
    scored:       "fraud.transactions.scored"
    decisions:    "fraud.decisions"
    dlq:          "fraud.transactions.dlq"
  consumer_group: "fraud-detection-consumers"

redis:
  host: "localhost"
  port: 6379
  feature_ttl_seconds: 86400

mlflow:
  tracking_uri: "http://localhost:5000"
  experiment_name: "fraud-detection"
  model_name: "fraud-scorer"

serving:
  host: "0.0.0.0"
  port: 8000
  p99_target_ms: 100

decision:
  block_threshold: 0.85
  flag_threshold:  0.50

drift:
  check_interval_seconds: 21600
  data_drift_threshold: 0.15
  fraud_rate_spike_multiplier: 2.0
""",

".env.example": """\
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
REDIS_HOST=localhost
MLFLOW_TRACKING_URI=http://localhost:5000
DATABASE_URL=postgresql://fraud:fraud@localhost/fraud_db
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
BLOCK_THRESHOLD=0.85
FLAG_THRESHOLD=0.50
""",

".gitignore": """\
__pycache__/
*.py[cod]
.venv/
venv/
.env
*.egg-info/
dist/
.pytest_cache/
.coverage
htmlcov/
mlruns/
.mypy_cache/
data/
.DS_Store
""",

"src/__init__.py": '"""Real-Time Credit Card Fraud Detection MLOps System."""\n__version__ = "0.1.0"\n',
"src/ingestion/__init__.py": '"""Transaction ingestion: Kafka producers, schemas, simulators."""\n',
"src/features/__init__.py": '"""Feature engineering: velocity, geo, behaviour, feature store."""\n',
"src/models/__init__.py": '"""ML models: Isolation Forest, XGBoost, ensemble, MLflow."""\n',
"src/serving/__init__.py": '"""FastAPI scoring API with sub-100ms inference."""\n',
"src/decision/__init__.py": '"""Decision engine: block/flag/allow, rule engine, case management."""\n',
"src/monitoring/__init__.py": '"""Drift detection, Prometheus metrics, alerting."""\n',
"src/security/__init__.py": '"""Security: PAN masking, audit logging, RBAC."""\n',
"src/retraining/__init__.py": '"""Automated retraining: Airflow DAGs, validation, canary deployment."""\n',
"tests/__init__.py": "",
"tests/unit/__init__.py": "",
"tests/integration/__init__.py": "",
"tests/load/__init__.py": "",
"templates/__init__.py": "",
".automation_state/.gitkeep": "",

"infra/prometheus/prometheus.yml": """\
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: fraud-scoring-api
    static_configs:
      - targets: ["host.docker.internal:8000"]
    metrics_path: /metrics
""",
}


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True,
                        help="GitHub repo URL e.g. https://github.com/USER/fraud-detection-mlops.git")
    args = parser.parse_args()

    print("\n🚀 Bootstrapping fraud-detection-mlops repo...")
    print(f"   Remote: {args.repo}\n")

    print("📁 Creating directories...")
    for d in DIRS:
        Path(d).mkdir(parents=True, exist_ok=True)
    print(f"   ✓ {len(DIRS)} directories created")

    print("📝 Writing base files...")
    for filepath, content in BASE_FILES.items():
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"   ✓ {len(BASE_FILES)} files written")

    print("\n🔧 Initialising Git...")
    if not Path(".git").exists():
        run(["git", "init", "-b", "main"])
    run(["git", "config", "user.name", "MLOps Engineer"])
    run(["git", "config", "user.email", "86911143+suzanvusal@users.noreply.github.com"])
    run(["git", "remote", "remove", "origin"])
    run(["git", "remote", "add", "origin", args.repo])

    print("📦 Making initial commit...")
    run(["git", "add", "-A"])
    run(["git", "commit", "-m",
         "chore: bootstrap fraud-detection-mlops project\n\n"
         "- Real-time credit card fraud detection\n"
         "- Kafka + Feature Engineering + IF + XGBoost ensemble\n"
         "- FastAPI sub-100ms inference + Airflow retraining"])

    print("🚀 Pushing to GitHub...")
    result = run(["git", "push", "-u", "origin", "main"])
    if result.returncode == 0:
        print("   ✓ Pushed successfully!")
    else:
        print(f"   ⚠ Push failed: {result.stderr[:200]}")

    print("\n" + "="*55)
    print("  ✅ Bootstrap complete!")
    print("="*55)
    print("\nNext steps:")
    print("  1. Add AUTOMATION_PAT secret in GitHub repo Settings")
    print("  2. Actions → Run workflow → trigger Day 1")


if __name__ == "__main__":
    main()
