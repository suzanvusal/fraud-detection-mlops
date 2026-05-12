"""FastAPI fraud scoring API — sub-100ms P99 latency."""
from __future__ import annotations
import logging
import os
import time
from contextlib import asynccontextmanager
import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel

logger = logging.getLogger(__name__)

SCORE_COUNTER = Counter("fraud_scores_total", "Scoring requests", ["decision"])
SCORE_LATENCY = Histogram("fraud_score_latency_seconds", "Scoring latency",
                           buckets=[0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.25, 0.5])

_model = None
_model_version = "unknown"
BLOCK_THRESHOLD = float(os.getenv("BLOCK_THRESHOLD", "0.85"))
FLAG_THRESHOLD  = float(os.getenv("FLAG_THRESHOLD",  "0.50"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _model, _model_version
    uri = os.getenv("MLFLOW_MODEL_URI", "models:/fraud-scorer/Production")
    try:
        _model = mlflow.pyfunc.load_model(uri)
        _model_version = os.getenv("MODEL_VERSION", "latest")
        logger.info("Model loaded from %s", uri)
    except Exception as exc:
        logger.warning("Model load failed: %s", exc)
    yield


app = FastAPI(title="Fraud Detection Scoring API", version="1.0.0", lifespan=lifespan)


class ScoreRequest(BaseModel):
    transaction_id: str
    card_id:        str
    amount:         float
    features:       dict[str, float]


class ScoreResponse(BaseModel):
    transaction_id: str
    fraud_score:    float
    decision:       str
    model_version:  str
    latency_ms:     float


@app.post("/score", response_model=ScoreResponse)
async def score(req: ScoreRequest):
    if _model is None:
        raise HTTPException(503, "Model not loaded")
    t0 = time.perf_counter()
    try:
        s  = float(_model.predict(pd.DataFrame([req.features]))[0])
        lat= (time.perf_counter() - t0) * 1000
        decision = ("BLOCK" if s >= BLOCK_THRESHOLD
                    else "FLAG" if s >= FLAG_THRESHOLD else "ALLOW")
        SCORE_COUNTER.labels(decision=decision).inc()
        SCORE_LATENCY.observe(lat / 1000)
        return ScoreResponse(
            transaction_id=req.transaction_id,
            fraud_score=round(s, 4),
            decision=decision,
            model_version=_model_version,
            latency_ms=round(lat, 2),
        )
    except Exception as exc:
        raise HTTPException(500, str(exc))


@app.post("/score/batch")
async def score_batch(requests: list[ScoreRequest]):
    return [await score(r) for r in requests]


@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": _model is not None}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# 10:32:59 — fix: model reload causing 200ms spike in P99
