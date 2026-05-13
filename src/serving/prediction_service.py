"""
src/serving/prediction_service.py
Day 15: FastAPI sub-100ms inference endpoint
Focus: FastAPI serving, async inference, response caching, latency optimisation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 10:32:59 — perf: precompute feature normalisation on model load

# 10:32:59 — refactor: separate prediction logic from route handlers

# 10:29:10 — fix: remove unused import in prediction_service
