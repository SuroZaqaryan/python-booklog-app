"""Book Repository - работа с БД."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BookModel, GenreModel


class BookRepository:
    """Репозиторий для работы с книгами в БД."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[BookModel]:
        """Получить все книги."""
        result = await self.db.execute(select(BookModel))
        return list(result.scalars().all())

    async def get_by_id(self, book_id: int) -> Optional[BookModel]:
        """Получить книгу по ID."""
        result = await self.db.execute(
            select(BookModel).where(BookModel.id == book_id)
        )
        return result.scalar_one_or_none()

    async def create(self, book_data: dict) -> BookModel:
        """Создать новую книгу."""
        book = BookModel(**book_data)
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book

    async def delete(self, book: BookModel) -> None:
        """Удалить книгу."""
        await self.db.delete(book)
        await self.db.commit()

    async def get_all_genres(self) -> List[str]:
        """Получить все жанры из БД."""
        result = await self.db.execute(
            select(GenreModel.name).order_by(GenreModel.name)
        )
        genres = result.scalars().all()
        return list(genres)
