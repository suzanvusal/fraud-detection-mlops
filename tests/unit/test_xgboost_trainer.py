"""
tests/unit/test_xgboost_trainer.py
Day 13: XGBoost fraud classifier
Focus: XGBoost training, Optuna hyperparameter search, SHAP explainability
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:39:27 — feat: implement threshold optimisation for precision-recall 
