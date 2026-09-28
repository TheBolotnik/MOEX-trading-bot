"""Simulated broker for backtests — placeholder."""

from __future__ import annotations


class BacktestBroker:
    def submit_order(self, *_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise NotImplementedError("backtest.broker is not implemented yet")
