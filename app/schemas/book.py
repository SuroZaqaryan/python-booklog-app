"""Book Pydantic schemas."""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    """Базовая схема книги."""

    name: str
    genre: Optional[str] = None
    author: Optional[str] = None


class BookCreate(BookBase):
    """Схема для создания книги. Жанр может быть любым строковым значением."""

    pass


class BookPublic(BookBase):
    """Схема книги для публичного API."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class BookStatusPublic(BaseModel):
    """Схема статуса книги для публичного API."""

    label: str
    value: str
