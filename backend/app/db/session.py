"""
Database session configuration for MariaDB
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from app.core.config import settings

# Create declarative base
Base = declarative_base()

# Create async engine for MariaDB with timeout and connection management
engine = create_async_engine(
    settings.async_database_url,
    echo=False,  # Disabled for better performance
    poolclass=QueuePool,
    pool_size=20,  # Increased for better concurrency
    max_overflow=20,  # Increased overflow
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_timeout=60,  # Increased timeout for getting connection from pool
    # Performance optimizations
    pool_reset_on_return='commit',
    # MariaDB specific settings
    connect_args={
        "charset": "utf8mb4",
        "autocommit": False,
        "connect_timeout": 10,  # Connection timeout in seconds (increased)
    }
)

# Create async session factory
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    """
    Dependency to get database session with proper cleanup
    Note: Commits should be done explicitly in service methods, not here
    """
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Database session error: {e}", exc_info=True)
            await session.rollback()  # Rollback on error
            raise
