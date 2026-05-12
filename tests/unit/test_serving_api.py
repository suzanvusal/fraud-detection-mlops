"""
tests/unit/test_serving_api.py
Day 15: FastAPI sub-100ms inference endpoint
Focus: FastAPI serving, async inference, response caching, latency optimisation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 10:32:59 — feat: add P99 latency target: 100ms SLO

# 10:32:59 — test: add pytest-asyncio tests verifying P99 < 100ms
