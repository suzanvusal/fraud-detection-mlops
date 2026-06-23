"""Canary deployment manager for fraud detection models."""
from __future__ import annotations
import logging
import time
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class CanaryPhase(str, Enum):
    IDLE        = "idle"
    RAMPING     = "ramping"
    COMPLETE    = "complete"
    ROLLED_BACK = "rolled_back"


@dataclass
class CanaryConfig:
    ramp_steps:       list[float] = None
    step_duration_s:  float = 3600.0
    max_error_rate:   float = 0.01
    max_fraud_rate_delta: float = 0.10

    def __post_init__(self):
        if self.ramp_steps is None:
            self.ramp_steps = [0.01, 0.05, 0.20, 0.50, 1.00]


@dataclass
class CanaryState:
    phase:            CanaryPhase = CanaryPhase.IDLE
    current_step:     int   = 0
    canary_share:     float = 0.0
    canary_errors:    int   = 0
    canary_requests:  int   = 0
    step_start_ts:    float = 0.0
    champion_version: str   = ""
    canary_version:   str   = ""


class CanaryManager:
    def __init__(self, config: CanaryConfig | None = None) -> None:
        self.config = config or CanaryConfig()
        self.state  = CanaryState()

    def start(self, champion: str, canary: str) -> None:
        self.state = CanaryState(
            phase=CanaryPhase.RAMPING,
            current_step=0,
            canary_share=self.config.ramp_steps[0],
            step_start_ts=time.time(),
            champion_version=champion,
            canary_version=canary,
        )
        logger.info("Canary started: %s → %s @ %.1f%%",
                    champion, canary, self.state.canary_share * 100)

    def record(self, is_canary: bool, is_error: bool) -> None:
        if is_canary:
            self.state.canary_requests += 1
            if is_error:
                self.state.canary_errors += 1

    def tick(self) -> CanaryPhase:
        if self.state.phase != CanaryPhase.RAMPING:
            return self.state.phase
        elapsed = time.time() - self.state.step_start_ts
        if elapsed < self.config.step_duration_s:
            return self.state.phase
        err_rate = self.state.canary_errors / max(1, self.state.canary_requests)
        if err_rate > self.config.max_error_rate:
            self._rollback(f"Error rate {err_rate:.2%}")
            return self.state.phase
        next_step = self.state.current_step + 1
        if next_step >= len(self.config.ramp_steps):
            self.state.phase = CanaryPhase.COMPLETE
            logger.info("Canary complete — 100%% on %s", self.state.canary_version)
        else:
            self.state.current_step = next_step
            self.state.canary_share = self.config.ramp_steps[next_step]
            self.state.step_start_ts = time.time()
            logger.info("Canary ramp → %.1f%%", self.state.canary_share * 100)
        return self.state.phase

    def _rollback(self, reason: str) -> None:
        logger.error("Canary rollback: %s", reason)
        self.state.phase = CanaryPhase.ROLLED_BACK
        self.state.canary_share = 0.0

# 10:52:23 — test: add integration test for canary deployment flow

# 10:52:23 — fix: rollback not updating model pointer atomically

# 12:42:32 — refactor: rename variable for clarity in canary_manager

# 11:16:35 — refactor: rename variable for clarity in canary_manager

# 12:06:43 — style: run black formatter on canary_manager

# 11:17:49 — fix: handle None input edge case in canary_manager
