"""API Dependencies."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import BookRepository
from app.services import BookService


async def get_book_service(
    db: AsyncSession = None
) -> AsyncGenerator[BookService, None]:
    """
    Dependency для получения BookService.
    
    Args:
        db: Сессия базы данных (inject через Depends)
        
    Yields:
        BookService: Сервис для работы с книгами.
    """
    if db is None:
        async for session in get_db():
            db = session
            break
    
    repository = BookRepository(db)
    service = BookService(repository)
    yield service
