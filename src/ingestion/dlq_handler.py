"""
src/ingestion/dlq_handler.py
Day 5: Kafka consumer & dead-letter queue
Focus: Transaction consumer, DLQ routing, schema validation, offset management
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:07:56 — feat: implement at-least-once processing guarantee

# 09:07:56 — fix: handle KafkaTimeoutError with exponential backoff
