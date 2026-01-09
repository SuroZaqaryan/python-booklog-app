"""Books API endpoints."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import BookRepository
from app.schemas import BookCreate, BookPublic, BookStatusPublic
from app.services import BookService

router = APIRouter()
logger = logging.getLogger(__name__)


def get_book_service(db: AsyncSession = Depends(get_db)) -> BookService:
    """Dependency для получения BookService."""
    repository = BookRepository(db)
    return BookService(repository)


@router.get("/statuses", response_model=List[BookStatusPublic])
async def get_book_statuses():
    """
    Получить все возможные статусы книг.
    
    Returns:
        List[BookStatusPublic]: Список статусов с их метками.
    """
    return BookService.get_book_statuses()


@router.get("/genres", response_model=List[str])
async def get_genres(service: BookService = Depends(get_book_service)):
    """
    Получить список рекомендуемых жанров из базы данных.
    
    Returns:
        List[str]: Список жанров.
    """
    return await service.get_genres()


@router.get("", response_model=List[BookPublic])
async def get_books(service: BookService = Depends(get_book_service)):
    """
    Получить список всех книг.
    
    Returns:
        List[BookPublic]: Список книг.
    """
    try:
        return await service.get_all_books()
    except Exception as e:
        logger.error(f"Error in get_books: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("", response_model=BookPublic, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    service: BookService = Depends(get_book_service)
):
    """
    Создать новую книгу.
    
    Args:
        book: Данные для создания книги.
        
    Returns:
        BookPublic: Созданная книга.
    """
    return await service.create_book(book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    """
    Удалить книгу по ID.
    
    Args:
        book_id: ID книги для удаления.
        
    Raises:
        HTTPException: Если книга не найдена.
    """
    try:
        await service.delete_book(book_id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
