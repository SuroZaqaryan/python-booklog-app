from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import BookModel
from app.schemas import BookCreate, BookPublic, VALID_GENRES

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/genres", response_model=List[str])
async def get_genres():
    """Возвращает список рекомендуемых жанров (для справки)."""
    return VALID_GENRES


@router.get("", response_model=List[BookPublic])
async def get_books(db: AsyncSession = Depends(get_db)):
    try:
        data = await db.execute(select(BookModel))
        result = data.scalars().all()
        return result
    except Exception as e:
        # Логируем ошибку для отладки
        import logging
        logging.error(f"Error in get_books: {str(e)}", exc_info=True)
        raise


@router.post("", response_model=BookPublic, status_code=201)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    """
    Создает новую книгу с указанным жанром.
    
    Жанр может быть любым строковым значением, указанным пользователем.
    """
    data = BookModel(**book.model_dump())
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data