"""
src/models/xgboost_trainer.py
Day 13: XGBoost fraud classifier
Focus: XGBoost training, Optuna hyperparameter search, SHAP explainability
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:39:27 — feat: add business metric: fraud caught rate at 0.1% false p

# 09:39:27 — fix: SHAP values failing on sparse feature matrix
