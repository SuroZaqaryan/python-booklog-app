"""Genre ORM model."""

from sqlalchemy import Column, Integer, String

from app.models.base import Base


class GenreModel(Base):
    """Модель жанра книги."""

    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
