"""
Database session configuration for MariaDB (FATS/reference/clients/sumlogs).
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

# Keep separate declarative bases per database domain.
Base = declarative_base()  # MariaDB models (existing FATS/reference)
SummitBase = declarative_base()  # Legacy sumlogs MariaDB (days, items, progs)

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


# sumlogs legacy MariaDB — Summit Logging (days, items, progs) + staff list
_sumlogs_sync_url = settings.sumlogs_database_url  # mysql+pymysql://...
_sumlogs_async_url = _sumlogs_sync_url.replace("mysql+pymysql://", "mysql+aiomysql://", 1) if _sumlogs_sync_url else ""

if _sumlogs_async_url:
    try:
        sumlogs_engine = create_async_engine(
            _sumlogs_async_url,
            echo=False,
            pool_size=10,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_timeout=15,
            connect_args={"charset": "utf8mb4", "connect_timeout": 10},
        )
        sumlogs_async_session = sessionmaker(
            sumlogs_engine, class_=AsyncSession, expire_on_commit=False
        )
    except Exception:
        sumlogs_engine = None
        sumlogs_async_session = None
else:
    sumlogs_engine = None
    sumlogs_async_session = None

# Summit API uses sumlogs MariaDB directly (same schema as legacy CGI).
summit_engine = sumlogs_engine
summit_async_session = sumlogs_async_session


async def get_summit_db():
    """MariaDB `sumlogs` dependency for Summit Logging endpoints."""
    if sumlogs_async_session is None:
        raise RuntimeError("SUMLOGS_DATABASE_URL is not configured")
    async for session in _session_dependency(sumlogs_async_session):
        yield session


async def get_sumlogs_db():
    """Async session for sumlogs (staff list, refer codes, etc.)."""
    if sumlogs_async_session is None:
        yield None
        return
    async for session in _session_dependency(sumlogs_async_session):
        yield session


# Remote legacy clients DB on opal server — clients.alloc (nightly OPAL program schedule)
_legacy_clients_url = settings.legacy_clients_database_url

if _legacy_clients_url:
    try:
        legacy_clients_engine = create_async_engine(
            _legacy_clients_url,
            echo=False,
            pool_size=3,
            max_overflow=3,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_timeout=15,
            connect_args={"charset": "utf8mb4", "connect_timeout": 10, "ssl": False},
        )
        legacy_clients_async_session = sessionmaker(
            legacy_clients_engine, class_=AsyncSession, expire_on_commit=False
        )
    except Exception:
        legacy_clients_engine = None
        legacy_clients_async_session = None
else:
    legacy_clients_engine = None
    legacy_clients_async_session = None


async def get_legacy_clients_db():
    """Remote opal:3306/clients — read-only access for nightly program schedule."""
    if legacy_clients_async_session is None:
        raise RuntimeError("LEGACY_CLIENTS_DATABASE_URL is not configured")
    async for session in _session_dependency(legacy_clients_async_session):
        yield session


# Backward-compatible aliases used by existing code.
engine = mariadb_engine
async_session = mariadb_async_session
get_db = get_mariadb_db
