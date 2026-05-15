"""Pydantic schemas for credit card transaction data."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TransactionType(str, Enum):
    PURCHASE   = "purchase"
    WITHDRAWAL = "withdrawal"
    TRANSFER   = "transfer"
    REFUND     = "refund"


class MerchantInfo(BaseModel):
    merchant_id:   str
    name:          str
    category_code: str
    country:       str
    city:          Optional[str] = None
    is_online:     bool = False


class CardholderProfile(BaseModel):
    card_id:            str
    account_id:         str
    home_country:       str
    avg_transaction:    float = 0.0
    total_transactions: int   = 0
    fraud_history:      bool  = False


class Transaction(BaseModel):
    transaction_id:   str
    card_id:          str
    amount:           float = Field(gt=0, description="Amount in USD")
    currency:         str   = "USD"
    merchant:         MerchantInfo
    cardholder:       CardholderProfile
    transaction_type: TransactionType = TransactionType.PURCHASE
    timestamp:        datetime
    ip_country:       Optional[str] = None
    device_id:        Optional[str] = None
    is_card_present:  bool = True
    is_confirmed_fraud: Optional[bool] = None

    @field_validator("amount")
    @classmethod
    def amount_reasonable(cls, v: float) -> float:
        if v > 1_000_000:
            raise ValueError("Amount exceeds maximum limit")
        return round(v, 2)

    @property
    def is_cross_border(self) -> bool:
        return self.cardholder.home_country != self.merchant.country

    @property
    def is_high_value(self) -> bool:
        return self.amount > 1000

    def to_kafka_dict(self) -> dict:
        return self.model_dump(mode="json")

# 10:07:02 — docs: add module docstring to schemas

# 10:08:22 — chore: add logging statement to schemas

# 10:08:22 — docs: update example in docstring of schemas

# 10:25:43 — docs: update example in docstring of schemas

# 09:23:43 — chore: day 11 maintenance sweep

# 10:29:10 — fix: remove unused import in schemas

# 10:25:15 — docs: add module docstring to schemas
