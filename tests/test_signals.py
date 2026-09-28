"""Placeholder — signals tests."""


def test_signals_module_importable() -> None:
    from app.signals.models import SignalAction

    assert SignalAction.BUY.value == "BUY"
