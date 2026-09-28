"""T-Invest API client stub — no network calls in skeleton stage."""

from __future__ import annotations

from typing import Any


class TinkoffClient:
    """Thin placeholder for T-Invest SDK integration.

    Real methods (get_instruments, get_candles, …) will be added later.
    Do not call the broker from this skeleton.
    """

    def __init__(self, token: str = "", sandbox: bool = True) -> None:
        self.token = token
        self.sandbox = sandbox
        self._connected = False

    def connect(self) -> None:
        """Reserved for SDK client setup. No-op in skeleton."""
        self._connected = False
        raise NotImplementedError("T-Invest client is not implemented yet")

    def get_instruments(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_candles(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_last_prices(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_portfolio(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError

    def get_positions(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        raise NotImplementedError
