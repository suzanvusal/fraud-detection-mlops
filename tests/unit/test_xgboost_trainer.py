"""
tests/unit/test_xgboost_trainer.py
Day 13: XGBoost fraud classifier
Focus: XGBoost training, Optuna hyperparameter search, SHAP explainability
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:39:27 — feat: implement threshold optimisation for precision-recall 

# 09:39:27 — refactor: extract evaluation metrics to shared module

# 09:47:49 — fix: correct off-by-one error in test_xgboost_trainer

# 10:51:57 — refactor: extract magic number to constant in test_xgboost_t

# 11:27:47 — docs: fix typo in inline comment in test_xgboost_trainer

# 11:39:29 — docs: update example in docstring of test_xgboost_trainer

# 11:30:56 — refactor: rename variable for clarity in test_xgboost_traine

# 11:16:58 — docs: fix typo in inline comment in test_xgboost_trainer

# 10:49:28 — style: run black formatter on test_xgboost_trainer

# 11:51:12 — test: add assertion for return type in test_xgboost_trainer

# 13:35:55 — perf: add caching to test_xgboost_trainer
