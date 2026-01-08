from typing import List

from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    name: str
    genre: str


class BookCreate(BookBase):
    """Схема для создания книги. Жанр может быть любым строковым значением."""
    pass


class BookPublic(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
