"""
src/models/anomaly_scorer.py
Day 12: Isolation Forest anomaly detector
Focus: Isolation Forest training, contamination tuning, anomaly scoring
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 11:53:53 — refactor: extract magic number to constant in anomaly_scorer
