"""
Database session configuration for MariaDB (FATS/reference) and Postgres (Summit Logging).
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

# Keep separate declarative bases per database domain.
Base = declarative_base()  # MariaDB models (existing FATS/reference)
SummitBase = declarative_base()  # Postgres Summit Logging models

# MariaDB engine/session (existing behavior)
mariadb_engine = create_async_engine(
    settings.mariadb_async_database_url,
    echo=False,
    pool_size=20,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_timeout=60,
    connect_args={
        "charset": "utf8mb4",
        "autocommit": False,
        "connect_timeout": 10,
    },
)
mariadb_async_session = sessionmaker(
    mariadb_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Postgres engine/session (new Summit Logging domain)
summit_engine = create_async_engine(
    settings.summit_async_database_url,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_timeout=60,
)
summit_async_session = sessionmaker(
    summit_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def _session_dependency(session_factory):
    async with session_factory() as session:
        try:
            yield session
        except Exception as exc:
            logger.error("Database session error: %s", exc, exc_info=True)
            await session.rollback()
            raise


async def get_mariadb_db():
    """
    MariaDB dependency for existing FATS/reference endpoints.
    """
    async for session in _session_dependency(mariadb_async_session):
        yield session


async def get_summit_db():
    """
    Postgres dependency for Summit Logging endpoints.
    """
    async for session in _session_dependency(summit_async_session):
        yield session


# clients engine/session (users, sessions, staff, props — legacy MariaDB)
clients_engine = create_async_engine(
    settings.clients_async_database_url,
    echo=False,
    pool_size=5,
    max_overflow=5,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_timeout=60,
    connect_args={
        "charset": "utf8mb4",
        "autocommit": False,
        "connect_timeout": 10,
    },
)
clients_async_session = sessionmaker(
    clients_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_clients_db():
    """
    MariaDB dependency for the `clients` database
    (users, sessions, staff, props, alloc, etc.)
    """
    async for session in _session_dependency(clients_async_session):
        yield session


# Backward-compatible aliases used by existing code.
engine = mariadb_engine
async_session = mariadb_async_session
get_db = get_mariadb_db
