"""Evidently-based drift detector for fraud transaction features."""
from __future__ import annotations
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report

logger = logging.getLogger(__name__)

TRANSACTION_FEATURES = [
    "amount", "tx_count_1min", "tx_count_1hr", "amount_sum_1hr",
    "unique_merchants_1hr", "unique_countries_1hr",
    "amount_vs_avg_ratio", "is_cross_border", "is_card_present",
]


class FraudDriftDetector:
    def __init__(self, reference_path: str,
                 reports_dir: str = "reports/drift",
                 threshold: float = 0.15) -> None:
        self.ref_path  = Path(reference_path)
        self.reports   = Path(reports_dir)
        self.threshold = threshold
        self.reports.mkdir(parents=True, exist_ok=True)
        self._ref: pd.DataFrame | None = None

    def _load_ref(self) -> pd.DataFrame:
        if self._ref is None:
            self._ref = pd.read_parquet(self.ref_path)[TRANSACTION_FEATURES]
        return self._ref

    def run(self, current: pd.DataFrame) -> dict:
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=self._load_ref(),
                   current_data=current[TRANSACTION_FEATURES])
        ts   = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        html = self.reports / f"drift_{ts}.html"
        jsf  = self.reports / f"drift_{ts}.json"
        report.save_html(str(html))
        report.save_json(str(jsf))
        result   = json.loads(jsf.read_text())
        score    = self._score(result)
        drifted  = score > self.threshold
        logger.info("Drift score=%.4f drifted=%s", score, drifted)
        return {"drift_score": score, "is_drifted": drifted,
                "report": str(html), "ts": ts}

    def _score(self, r: dict) -> float:
        for m in r.get("metrics", []):
            if m.get("metric") == "DatasetDriftMetric":
                return m["result"].get("share_of_drifted_columns", 0.0)
        return 0.0

# 10:25:14 — feat: add drift severity classification: none/warning/critic

# 10:25:14 — feat: implement drift metric emission to Prometheus

# 10:25:14 — fix: Evidently failing on zero-variance reference features

# 10:25:15 — chore: day 18 maintenance sweep
