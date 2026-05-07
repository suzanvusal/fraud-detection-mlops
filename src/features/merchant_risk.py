"""
src/features/merchant_risk.py
Day 7: Geolocation & merchant risk features
Focus: Location-based features, merchant category risk, impossible travel detection
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 10:14:55 — test: add impossible travel tests with known coordinates

# 10:25:43 — fix: correct off-by-one error in merchant_risk
