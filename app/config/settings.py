"""Application settings loaded from environment and strategy.yaml."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Runtime settings from .env / environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    tinkoff_token: str = Field(default="", alias="TINKOFF_TOKEN")
    tinkoff_sandbox: bool = Field(default=True, alias="TINKOFF_SANDBOX")
    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str = Field(default="", alias="TELEGRAM_CHAT_ID")
    database_url: str = Field(
        default="sqlite:///./data/moex_bot.db",
        alias="DATABASE_URL",
    )
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_dir: str = Field(default="logs", alias="LOG_DIR")
    strategy_config_path: str = Field(
        default="app/config/strategy.yaml",
        alias="STRATEGY_CONFIG_PATH",
    )

    @property
    def strategy_path(self) -> Path:
        path = Path(self.strategy_config_path)
        return path if path.is_absolute() else PROJECT_ROOT / path


def load_strategy_config(path: Path | None = None) -> dict[str, Any]:
    """Load strategy.yaml as a plain dict (thresholds stay out of code)."""
    settings = get_settings()
    config_path = path or settings.strategy_path
    if not config_path.exists():
        raise FileNotFoundError(f"Strategy config not found: {config_path}")
    with config_path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Strategy config must be a mapping: {config_path}")
    return data


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
