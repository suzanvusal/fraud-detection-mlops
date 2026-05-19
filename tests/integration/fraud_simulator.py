"""
tests/integration/fraud_simulator.py
Day 22: Integration tests — full pipeline
Focus: End-to-end pipeline tests, fraud detection accuracy validation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 11:19:37 — test: verify DLQ routing on malformed transaction

# 11:19:37 — ci: run integration tests only on main branch
