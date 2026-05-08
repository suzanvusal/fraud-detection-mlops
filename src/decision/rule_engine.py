"""
src/decision/rule_engine.py
Day 9: Alert engine & real-time rules
Focus: Rule-based pre-filter, hard rules, soft rules, rule versioning
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 10:20:40 — refactor: move rule definitions to YAML config

# 09:23:43 — style: reorder imports alphabetically in rule_engine
