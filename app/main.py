"""Application entrypoint (skeleton — no trading logic yet)."""

from __future__ import annotations

import logging

from app import __version__
from app.config.settings import get_settings, load_strategy_config
from app.logging import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Boot config and logging; trading pipeline is not wired yet."""
    settings = get_settings()
    setup_logging(level=settings.log_level, log_dir=settings.log_dir)
    strategy = load_strategy_config()

    logger.info(
        "MOEX Trading Signal Bot v%s started (sandbox=%s, strategy_version=%s)",
        __version__,
        settings.tinkoff_sandbox,
        strategy.get("strategy_version", "unknown"),
    )
    logger.info(
        "Skeleton only: no broker calls, indicators, or strategy engine yet."
    )


if __name__ == "__main__":
    main()
