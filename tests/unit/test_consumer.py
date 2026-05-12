"""
tests/unit/test_consumer.py
Day 5: Kafka consumer & dead-letter queue
Focus: Transaction consumer, DLQ routing, schema validation, offset management
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:07:56 — feat: add consumer group rebalance logging

# 10:32:59 — chore: day 15 maintenance sweep
