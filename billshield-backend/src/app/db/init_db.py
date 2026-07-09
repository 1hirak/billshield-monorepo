from __future__ import annotations

from app.core.config import settings
from app.core.logging import get_logger
from app.db.base import Base
from app.db.session import engine

logger = get_logger(__name__)


def init_db() -> None:
    logger.info(f"Initialising database: {settings.DATABASE_URL[:50]}...")
    Base.metadata.create_all(bind=engine)

    if "sqlite" in settings.DATABASE_URL:
        import sqlite3
        from sqlalchemy import event

        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.execute("PRAGMA busy_timeout=5000;")
            cursor.close()

    logger.info("Database initialised.")


def drop_db() -> None:
    if settings.APP_ENV != "development":
        raise RuntimeError("Cannot drop database outside development environment.")
    logger.info("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("Database tables dropped.")
