"""
tests/unit/test_isolation_forest.py
Day 12: Isolation Forest anomaly detector
Focus: Isolation Forest training, contamination tuning, anomaly scoring
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:20:44 — feat: implement online anomaly scoring for streaming data
