"""
src/models/explainability.py
Day 13: XGBoost fraud classifier
Focus: XGBoost training, Optuna hyperparameter search, SHAP explainability
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:39:27 — feat: add model card generation as MLflow artifact

# 10:52:23 — perf: add caching to explainability

# 09:56:05 — fix: handle None input edge case in explainability
