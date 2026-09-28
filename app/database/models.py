"""SQLAlchemy ORM models — table stubs only, no business logic."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    figi: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    instrument_uid: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sector: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    lot_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Candle(Base):
    __tablename__ = "candles"
    __table_args__ = (
        UniqueConstraint(
            "instrument_id",
            "timeframe",
            "timestamp",
            name="uq_candle_instrument_tf_ts",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    instrument_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    timeframe: Mapped[str] = mapped_column(String(8), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)


class SignalRecord(Base):
    """Persisted signal journal row — generation logic lives elsewhere."""

    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    instrument_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    action: Mapped[str] = mapped_column(String(16), nullable=False)
    setup: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    timeframe: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    market_regime: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    sector: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    entry_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    stop_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    risk_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    position_size: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
