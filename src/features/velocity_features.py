"""Transaction velocity features using Redis sliding windows."""
from __future__ import annotations
import logging
import time
from dataclasses import dataclass
import redis

logger = logging.getLogger(__name__)


@dataclass
class VelocityFeatures:
    card_id:              str
    tx_count_1min:        int
    tx_count_5min:        int
    tx_count_1hr:         int
    amount_sum_1min:      float
    amount_sum_1hr:       float
    unique_merchants_1hr: int
    unique_countries_1hr: int
    new_merchant_flag:    bool
    amount_vs_avg_ratio:  float


class VelocityFeatureEngine:
    """Real-time velocity features from Redis sorted sets."""

    WINDOWS = {"1min": 60, "5min": 300, "1hr": 3600}

    def __init__(self, r: redis.Redis) -> None:
        self._r = r

    def compute(self, card_id: str, amount: float,
                merchant_id: str, country: str,
                avg_amount: float = 85.0) -> VelocityFeatures:
        now  = time.time()
        pipe = self._r.pipeline()

        keys = {
            "tx":  f"vel:tx:{card_id}",
            "amt": f"vel:amt:{card_id}",
            "mer": f"vel:mer:{card_id}",
            "cty": f"vel:cty:{card_id}",
        }

        pipe.zadd(keys["tx"],  {str(now): now})
        pipe.zadd(keys["amt"], {f"{now}:{amount}": now})
        pipe.zadd(keys["mer"], {f"{now}:{merchant_id}": now})
        pipe.zadd(keys["cty"], {f"{now}:{country}": now})

        cutoff = now - self.WINDOWS["1hr"]
        for k in keys.values():
            pipe.zremrangebyscore(k, 0, cutoff)
            pipe.expire(k, 86400)
        pipe.execute()

        known = self._r.smembers(f"known:mer:{card_id}") or set()
        is_new = merchant_id.encode() not in known
        self._r.sadd(f"known:mer:{card_id}", merchant_id)
        self._r.expire(f"known:mer:{card_id}", 86400)

        return VelocityFeatures(
            card_id=card_id,
            tx_count_1min=self._count(keys["tx"], now, 60),
            tx_count_5min=self._count(keys["tx"], now, 300),
            tx_count_1hr=self._count(keys["tx"], now, 3600),
            amount_sum_1min=self._sum(keys["amt"], now, 60),
            amount_sum_1hr=self._sum(keys["amt"], now, 3600),
            unique_merchants_1hr=self._unique(keys["mer"], now, 3600),
            unique_countries_1hr=self._unique(keys["cty"], now, 3600),
            new_merchant_flag=is_new,
            amount_vs_avg_ratio=round(amount / avg_amount if avg_amount > 0 else 1.0, 4),
        )

    def _count(self, key: str, now: float, window: int) -> int:
        return self._r.zcount(key, now - window, now)

    def _sum(self, key: str, now: float, window: int) -> float:
        entries = self._r.zrangebyscore(key, now - window, now)
        total = 0.0
        for e in entries:
            parts = e.decode().split(":", 1)
            if len(parts) == 2:
                try:
                    total += float(parts[1])
                except ValueError:
                    pass
        return round(total, 2)

    def _unique(self, key: str, now: float, window: int) -> int:
        entries = self._r.zrangebyscore(key, now - window, now)
        vals = set()
        for e in entries:
            parts = e.decode().split(":", 1)
            if len(parts) == 2:
                vals.add(parts[1])
        return len(vals)

# 09:22:58 — feat: implement new merchant flag (first time card used at m
