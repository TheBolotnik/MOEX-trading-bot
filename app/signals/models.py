"""Signal domain models — structure only, no generation logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class SignalAction(str, Enum):
    BUY = "BUY"
    ADD = "ADD"
    HOLD = "HOLD"
    REDUCE = "REDUCE"
    SELL = "SELL"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Signal:
    """User-facing signal payload (filled by generator later)."""

    ticker: str
    action: SignalAction
    setup: Optional[str] = None
    regime: Optional[str] = None
    sector: Optional[str] = None
    entry_price: Optional[float] = None
    stop_price: Optional[float] = None
    risk_amount: Optional[float] = None
    position_size: Optional[float] = None
    reason: Optional[str] = None
    confidence: Optional[float] = None
    created_at: datetime = field(default_factory=_utc_now)
