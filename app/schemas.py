from typing import List

from pydantic import BaseModel, ConfigDict

# Список рекомендуемых жанров (для справки, не для валидации)
VALID_GENRES = [
    "Fantasy",
    "Science Fiction (Sci-Fi)",
    "Romance",
    "Mystery",
    "Thriller & Suspense",
    "Horror",
    "Historical Fiction",
    "Action & Adventure",
    "Literary Fiction",
    "Contemporary Fiction",
    "Dystopian",
    "Magical Realism",
    "Paranormal",
    "Western",
    "Graphic Novel",
    "Young Adult (YA)",
    "Middle Grade",
    "Children's",
    "Women's Fiction",
    "Satire"
]


class BookBase(BaseModel):
    name: str
    genre: str


class BookCreate(BookBase):
    """Схема для создания книги. Жанр может быть любым строковым значением."""
    pass


class BookPublic(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
