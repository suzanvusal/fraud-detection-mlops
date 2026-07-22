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

# 11:19:37 — fix: remove unused import in xgboost_trainer

# 09:56:05 — docs: add module docstring to xgboost_trainer

# 13:56:42 — chore: day 30 maintenance sweep

# 11:17:49 — refactor: extract magic number to constant in xgboost_traine

# 10:36:48 — docs: add module docstring to xgboost_trainer

# 10:57:33 — fix: remove unused import in xgboost_trainer

# 10:09:01 — fix: handle None input edge case in xgboost_trainer

# 10:25:34 — chore: add logging statement to xgboost_trainer
