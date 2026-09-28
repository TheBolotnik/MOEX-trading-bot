#!/usr/bin/env python3
"""Smoke script: verify settings and strategy.yaml load without broker calls."""

from __future__ import annotations

from app.config.settings import get_settings, load_strategy_config
from app.logging import setup_logging


def main() -> None:
    settings = get_settings()
    setup_logging(level=settings.log_level, log_dir=settings.log_dir)
    strategy = load_strategy_config()
    print("settings.ok", settings.database_url)
    print("strategy.ok", strategy.get("strategy_version"))


if __name__ == "__main__":
    main()
