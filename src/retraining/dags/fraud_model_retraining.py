"""
src/retraining/dags/fraud_model_retraining.py
Day 23: Airflow retraining DAG
Focus: Airflow setup, drift-triggered retraining DAG, dataset assembly
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 10:51:57 — fix: Airflow requires FERNET_KEY on startup
