"""
src/features/window_aggregator.py
Day 6: Velocity feature engineering
Focus: Transaction velocity, frequency, amount patterns per card and merchant
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:22:58 — docs: update example in docstring of window_aggregator

# 09:23:43 — refactor: extract magic number to constant in window_aggrega
