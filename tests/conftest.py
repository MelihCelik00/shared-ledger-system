import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine
)

from core.shared_ledger.models.base import Base
from core.shared_ledger.operations.base import LedgerOperationType
from apps.example_app.main import app
from apps.example_app.api.dependencies import get_db

# Test database URL - using the test container from docker-compose
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/test_ledger_db"

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, isolation_level="AUTOCOMMIT")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def test_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )
    
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()

@pytest_asyncio.fixture
async def test_client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with the test database session."""
    from core.shared_ledger.api.router import get_db as core_get_db
    
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[core_get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        
    app.dependency_overrides.clear()

@pytest.fixture
def test_owner_id() -> str:
    """Return a test owner ID."""
    return "test_owner"

@pytest.fixture
def test_operation() -> LedgerOperationType:
    """Return a test operation type."""
    return LedgerOperationType.CREDIT_ADD

@pytest.fixture
def test_amount() -> int:
    """Return a test amount."""
    return 100 