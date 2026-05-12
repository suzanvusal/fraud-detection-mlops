"""
src/serving/response_models.py
Day 15: FastAPI sub-100ms inference endpoint
Focus: FastAPI serving, async inference, response caching, latency optimisation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)
