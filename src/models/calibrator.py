"""
src/models/calibrator.py
Day 14: Ensemble model: Isolation Forest + XGBoost
Focus: Score fusion, ensemble weighting, combined fraud scoring
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 11:23:39 — perf: parallelise IF and XGBoost inference

# 10:29:10 — fix: handle None input edge case in calibrator

# 09:56:05 — test: add assertion for return type in calibrator

# 12:05:28 — chore: add logging statement to calibrator

# 12:42:32 — fix: remove unused import in calibrator
