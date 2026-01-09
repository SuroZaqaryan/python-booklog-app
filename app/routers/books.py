from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import BookModel, GenreModel
from app.enums import BookStatus
from app.schemas import BookCreate, BookPublic, BookStatusPublic

router = APIRouter(prefix="/book", tags=["book"])

@router.get("/statuses", response_model=list[BookStatusPublic])
async def get_book_statuses():
    return [
        BookStatusPublic(
            value=status.value,
            label=_status_label(status)
        )
        for status in BookStatus
    ]


def _status_label(status: BookStatus) -> str:
    return {
        BookStatus.WANT_TO_READ: "Хочу прочитать",
        BookStatus.READING: "Читаю",
        BookStatus.FINISHED: "Прочитал",
        BookStatus.DROPPED: "Бросил",
    }[status]

@router.get("/genres", response_model=List[str])
async def get_genres(db: AsyncSession = Depends(get_db)):
    """Возвращает список рекомендуемых жанров из базы данных."""
    result = await db.execute(select(GenreModel.name).order_by(GenreModel.name))
    genres = result.scalars().all()
    return list(genres)


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
    data = BookModel(**book.model_dump())
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    data = await db.execute(select(BookModel).where(BookModel.id == book_id))
    result = data.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code = 404, detail = "Task not found")

    await db.delete(result)
    await db.commit()
    return None

