"""
src/serving/feedback_ingester.py
Day 17: Prediction logging & feedback loop
Focus: Structured prediction logs, confirmed fraud labels, feedback ingestion
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 10:19:05 — refactor: use asyncpg for async PostgreSQL logging

# 10:19:05 — fix: feedback ingester failing on duplicate submissions

# 09:41:52 — refactor: extract magic number to constant in feedback_inges
