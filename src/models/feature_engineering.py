"""
src/models/feature_engineering.py
Day 11: MLflow experiment tracking & data pipeline
Focus: MLflow server, experiment config, training data assembly, feature matrix
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 09:23:42 — fix: SMOTE failing with very low fraud rate
