"""
pytest configuration and fixtures for OPAL backend tests
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.db.session import Base, get_db

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
TEST_SYNC_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

# Create session maker
TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test"""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestingSessionLocal() as session:
        yield session
    
    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(db_session) -> TestClient:
    """Create test client with database override"""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_fats_data():
    """Sample FATS entry data for testing"""
    return {
        "issue": "Test Issue",
        "idescribe": "<p>Test issue description</p>",
        "solution": "Test Solution",
        "sdescribe": "<p>Test solution description</p>",
        "operator": "Test Operator",
        "status": "Active",
        "section": "AO",
        "section2": ".none",
    }


@pytest.fixture
def sample_comment_data():
    """Sample comment data for testing"""
    return {
        "comment_text": "Test comment",
        "commenter": "Test User",
        "todo": "Test TODO",
        "solution": "Test solution comment",
    }


@pytest.fixture
async def create_test_fats(db_session):
    """Fixture to create a test FATS entry"""
    from app.models.fats_entry import FATSEntry
    from datetime import datetime
    
    fats = FATSEntry(
        idno=9999,
        issue="Test FATS Entry",
        idescribe="<p>Test description</p>",
        solution="Test solution",
        sdescribe="<p>Test solution details</p>",
        operator="pytest",
        status="Active",
        section="AO",
        section2=".none",
        datein=datetime.utcnow(),
    )
    db_session.add(fats)
    await db_session.commit()
    await db_session.refresh(fats)
    return fats

