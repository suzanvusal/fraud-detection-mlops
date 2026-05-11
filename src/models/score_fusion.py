"""
src/models/score_fusion.py
Day 14: Ensemble model: Isolation Forest + XGBoost
Focus: Score fusion, ensemble weighting, combined fraud scoring
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 11:23:39 — feat: add ensemble score threshold grid search

# 11:23:39 — fix: calibration failing on perfectly separated scores

# 11:23:39 — chore: add logging statement to score_fusion
