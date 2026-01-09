"""Database connection and session management."""

from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings

# Создание асинхронного движка для SQLAlchemy
engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession | Any, Any]:
    """
    Dependency для получения сессии БД.
    
    Yields:
        AsyncSession: Сессия базы данных.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
