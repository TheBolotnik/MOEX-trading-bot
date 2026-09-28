"""Smoke tests: packages import and config loads (no broker / strategy logic)."""

from __future__ import annotations

import importlib

import pytest

PACKAGE_MODULES = [
    "app",
    "app.main",
    "app.config.settings",
    "app.api.tinkoff_client",
    "app.api.market_data",
    "app.api.portfolio",
    "app.api.sandbox",
    "app.database.database",
    "app.database.models",
    "app.market.regime",
    "app.market.sectors",
    "app.market.universe",
    "app.indicators.trend",
    "app.indicators.momentum",
    "app.indicators.volatility",
    "app.indicators.volume",
    "app.indicators.relative_strength",
    "app.smc.analyzer",
    "app.smc.confirmation",
    "app.strategy.breakout",
    "app.strategy.pullback",
    "app.strategy.ranking",
    "app.strategy.engine",
    "app.portfolio.manager",
    "app.portfolio.rotation",
    "app.portfolio.exposure",
    "app.risk.manager",
    "app.risk.position_size",
    "app.risk.stops",
    "app.signals.models",
    "app.signals.generator",
    "app.backtest.engine",
    "app.backtest.broker",
    "app.backtest.metrics",
    "app.telegram.bot",
    "app.telegram.handlers",
    "app.telegram.keyboards",
]


@pytest.mark.parametrize("module_name", PACKAGE_MODULES)
def test_module_imports(module_name: str) -> None:
    module = importlib.import_module(module_name)
    assert module is not None


def test_settings_and_strategy_load() -> None:
    from app.config.settings import get_settings, load_strategy_config

    get_settings.cache_clear()
    settings = get_settings()
    assert settings.database_url
    assert settings.strategy_path.exists()

    strategy = load_strategy_config()
    assert strategy["strategy_version"]
    assert "risk" in strategy
    assert strategy["risk"]["min_percent"] == 1.0


def test_signal_model_enum() -> None:
    from app.signals.models import Signal, SignalAction

    signal = Signal(ticker="SBER", action=SignalAction.HOLD)
    assert signal.action is SignalAction.HOLD
    assert signal.confidence is None


def test_tinkoff_client_is_stub() -> None:
    from app.api.tinkoff_client import TinkoffClient

    client = TinkoffClient(token="", sandbox=True)
    with pytest.raises(NotImplementedError):
        client.connect()


def test_main_entrypoint_runs(capsys: pytest.CaptureFixture[str]) -> None:
    from app.main import main

    main()  # should only log; no broker calls
