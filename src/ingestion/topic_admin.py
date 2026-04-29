"""
src/ingestion/topic_admin.py
Day 2: Transaction schemas & Kafka producers
Focus: Pydantic schemas for credit card transactions, Kafka topic setup, transaction simulator
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 10:07:02 — feat: implement topic admin for Kafka topic management

# 10:07:02 — test: add schema validation tests for all transaction fields
