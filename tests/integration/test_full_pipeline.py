"""
tests/integration/test_full_pipeline.py
Day 22: Integration tests — full pipeline
Focus: End-to-end pipeline tests, fraud detection accuracy validation
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 11:19:37 — fix: fraud simulator generating unrealistic amounts
