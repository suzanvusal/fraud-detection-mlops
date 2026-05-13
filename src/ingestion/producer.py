"""Kafka producer for credit card transaction streaming."""
from __future__ import annotations
import json
import logging
import time
from dataclasses import dataclass
from typing import Any
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

logger = logging.getLogger(__name__)


@dataclass
class ProducerConfig:
    bootstrap_servers: str = "localhost:9092"
    topic:             str = "fraud.transactions.raw"
    retries:           int = 5
    batch_size:        int = 32768
    linger_ms:         int = 10
    compression_type:  str = "gzip"


class TransactionProducer:
    def __init__(self, config: ProducerConfig) -> None:
        self.config = config
        self._producer = None
        self._sent = 0
        self._errors = 0

    def connect(self) -> None:
        for attempt in range(self.config.retries):
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=self.config.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v, default=str).encode(),
                    key_serializer=lambda k: k.encode() if k else None,
                    retries=self.config.retries,
                    batch_size=self.config.batch_size,
                    linger_ms=self.config.linger_ms,
                    compression_type=self.config.compression_type,
                )
                logger.info("Connected to Kafka @ %s", self.config.bootstrap_servers)
                return
            except NoBrokersAvailable:
                wait = 2 ** attempt
                logger.warning("No broker, retrying in %ds", wait)
                time.sleep(wait)
        raise RuntimeError("Kafka connection failed")

    def send(self, transaction: dict[str, Any], key: str | None = None) -> None:
        assert self._producer, "Call connect() first"
        self._producer.send(self.config.topic, value=transaction, key=key)
        self._sent += 1

    def flush(self) -> None:
        if self._producer:
            self._producer.flush()

    def close(self) -> None:
        if self._producer:
            self._producer.close()

    @property
    def stats(self) -> dict:
        return {"sent": self._sent, "errors": self._errors}

# 10:07:02 — refactor: extract Kafka config to dataclass

# 10:07:02 — fix: correct off-by-one error in producer

# 09:07:56 — refactor: extract magic number to constant in producer

# 10:25:43 — fix: correct off-by-one error in producer

# 09:20:44 — chore: add logging statement to producer

# 10:32:59 — fix: remove unused import in producer

# 10:29:10 — docs: add module docstring to producer
