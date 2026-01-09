"""Book Service - бизнес-логика работы с книгами."""

from typing import List

from app.models import BookModel
from app.repositories import BookRepository
from app.schemas import BookCreate, BookStatusPublic
from app.utils.enums import BookStatus


class BookService:
    """Сервис для работы с книгами."""

    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def get_all_books(self) -> List[BookModel]:
        """Получить все книги."""
        return await self.repository.get_all()

    async def create_book(self, book_data: BookCreate) -> BookModel:
        """Создать новую книгу."""
        return await self.repository.create(book_data.model_dump())

    async def delete_book(self, book_id: int) -> None:
        """Удалить книгу по ID."""
        book = await self.repository.get_by_id(book_id)
        if book is None:
            raise ValueError(f"Book with id {book_id} not found")
        await self.repository.delete(book)

    async def get_genres(self) -> List[str]:
        """Получить список рекомендуемых жанров."""
        return await self.repository.get_all_genres()

    @staticmethod
    def get_book_statuses() -> List[BookStatusPublic]:
        """Получить все возможные статусы книг."""
        return [
            BookStatusPublic(
                value=status.value,
                label=BookService._get_status_label(status)
            )
            for status in BookStatus
        ]

    @staticmethod
    def _get_status_label(status: BookStatus) -> str:
        """Получить русское название статуса."""
        labels = {
            BookStatus.WANT_TO_READ: "Хочу прочитать",
            BookStatus.READING: "Читаю",
            BookStatus.FINISHED: "Прочитал",
            BookStatus.DROPPED: "Бросил",
        }
        return labels[status]
