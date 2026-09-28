"""SQLAlchemy engine / session factory — placeholder."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Engine is created later when DATABASE_URL wiring is implemented.
SessionLocal: sessionmaker | None = None


class Base(DeclarativeBase):
    """Declarative base for ORM models."""


def init_db(_database_url: str) -> None:
    """Create engine and tables. Not wired in skeleton stage."""
    raise NotImplementedError("database.init_db is not implemented yet")


def get_session():  # type: ignore[no-untyped-def]
    """Yield a DB session. Not wired in skeleton stage."""
    raise NotImplementedError("database.get_session is not implemented yet")
