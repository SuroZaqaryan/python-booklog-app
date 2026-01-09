"""Book ORM model."""

from sqlalchemy import Column, Integer, String

from app.models.base import Base


class BookModel(Base):
    """Модель книги."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    genre = Column(String, nullable=True)
    author = Column(String, nullable=True)
