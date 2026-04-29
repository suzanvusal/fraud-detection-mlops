"""Unit tests for transaction schemas."""
import uuid
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from src.ingestion.schemas import Transaction, MerchantInfo, CardholderProfile


def make_tx(**overrides) -> dict:
    base = dict(
        transaction_id=str(uuid.uuid4()),
        card_id="CARD-000001",
        amount=85.50,
        merchant=dict(merchant_id="MER-001", name="Store", category_code="5411", country="US"),
        cardholder=dict(card_id="CARD-000001", account_id="ACC-001", home_country="US"),
        timestamp=datetime.now(timezone.utc),
    )
    base.update(overrides)
    return base


def test_valid_transaction():
    t = Transaction(**make_tx())
    assert t.amount == 85.50

def test_amount_rounded():
    t = Transaction(**make_tx(amount=85.999))
    assert t.amount == 86.0

def test_negative_amount_rejected():
    with pytest.raises(ValidationError):
        Transaction(**make_tx(amount=-10.0))

def test_zero_amount_rejected():
    with pytest.raises(ValidationError):
        Transaction(**make_tx(amount=0))

def test_exceeds_max_amount():
    with pytest.raises(ValidationError):
        Transaction(**make_tx(amount=2_000_000))

def test_is_high_value():
    t = Transaction(**make_tx(amount=1500.0))
    assert t.is_high_value

def test_not_high_value():
    t = Transaction(**make_tx(amount=50.0))
    assert not t.is_high_value
