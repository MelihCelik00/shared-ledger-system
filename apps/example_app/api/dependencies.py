from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# In production, this should be loaded from environment variables
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/ledger_db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields database sessions.
    
    Usage:
        @app.get("/")
        async def root(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 