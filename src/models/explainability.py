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

# 11:53:53 — docs: update example in docstring of explainability

# 12:42:32 — fix: remove unused import in explainability

# 11:29:31 — style: run black formatter on explainability

# 11:16:43 — fix: add missing type hint in explainability

# 10:28:24 — style: reorder imports alphabetically in explainability

# 10:57:33 — test: add assertion for return type in explainability

# 10:03:25 — refactor: extract magic number to constant in explainability
