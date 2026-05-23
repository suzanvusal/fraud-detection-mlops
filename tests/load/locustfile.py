"""
tests/load/locustfile.py
Day 26: Load testing & performance benchmarking
Focus: Locust load tests, sub-100ms P99 validation, throughput benchmarking
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:55:04 — fix: memory leak in feature store under sustained load
