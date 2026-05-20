"""
src/retraining/dataset_assembler.py
Day 23: Airflow retraining DAG
Focus: Airflow setup, drift-triggered retraining DAG, dataset assembly
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 10:51:57 — feat: add model_training task for both IF and XGBoost

# 10:51:57 — fix: Celery worker not picking up DAG changes

# 10:51:57 — fix: handle None input edge case in dataset_assembler
