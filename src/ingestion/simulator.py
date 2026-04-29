"""Realistic credit card transaction simulator with configurable fraud injection."""
from __future__ import annotations
import random
import time
import uuid
from datetime import datetime, timezone
from typing import Generator
from src.ingestion.schemas import (
    Transaction, MerchantInfo, CardholderProfile, TransactionType
)

MERCHANT_CATEGORIES = ["5411", "5812", "5912", "7011", "4111", "5999", "5651"]
COUNTRIES = ["US", "CA", "GB", "DE", "FR", "JP", "AU", "BR", "IN", "MX"]


def make_cardholder(card_id: str) -> CardholderProfile:
    return CardholderProfile(
        card_id=card_id,
        account_id=f"ACC-{uuid.uuid4().hex[:8].upper()}",
        home_country="US",
        avg_transaction=abs(random.gauss(85, 40)),
        total_transactions=random.randint(10, 5000),
    )


def make_merchant(is_fraud: bool = False) -> MerchantInfo:
    return MerchantInfo(
        merchant_id=f"MER-{uuid.uuid4().hex[:8].upper()}",
        name=f"Store {random.randint(1000, 9999)}",
        category_code=random.choice(MERCHANT_CATEGORIES),
        country=random.choice(COUNTRIES) if is_fraud else "US",
        is_online=random.random() < 0.3,
    )


def simulate_transaction(card_id: str, cardholder: CardholderProfile,
                          fraud_rate: float = 0.05) -> Transaction:
    is_fraud = random.random() < fraud_rate
    amount = (
        random.uniform(500, 5000) if is_fraud
        else abs(random.gauss(cardholder.avg_transaction, 30))
    )
    return Transaction(
        transaction_id=str(uuid.uuid4()),
        card_id=card_id,
        amount=max(0.01, round(amount, 2)),
        merchant=make_merchant(is_fraud),
        cardholder=cardholder,
        timestamp=datetime.now(timezone.utc),
        is_card_present=not is_fraud or random.random() > 0.5,
    )


def transaction_stream(
    n_cards: int = 100,
    fraud_rate: float = 0.05,
    rate_per_second: float = 10.0,
) -> Generator[Transaction, None, None]:
    cards = {
        f"CARD-{i:06d}": make_cardholder(f"CARD-{i:06d}")
        for i in range(n_cards)
    }
    interval = 1.0 / rate_per_second
    while True:
        card_id = random.choice(list(cards.keys()))
        yield simulate_transaction(card_id, cards[card_id], fraud_rate)
        time.sleep(interval)

# 10:07:02 — feat: add transaction ID generation with UUID4
