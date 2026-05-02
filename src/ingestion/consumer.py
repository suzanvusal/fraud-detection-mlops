"""
src/ingestion/consumer.py
Day 5: Kafka consumer & dead-letter queue
Focus: Transaction consumer, DLQ routing, schema validation, offset management
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:07:56 — test: add consumer integration test with embedded Kafka

# 09:07:56 — refactor: move consumer config to Pydantic dataclass
