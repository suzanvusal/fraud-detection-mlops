"""
src/models/calibrator.py
Day 14: Ensemble model: Isolation Forest + XGBoost
Focus: Score fusion, ensemble weighting, combined fraud scoring
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 11:23:39 — perf: parallelise IF and XGBoost inference
