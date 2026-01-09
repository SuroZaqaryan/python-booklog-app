"""Enums для приложения."""

from enum import Enum


class BookStatus(str, Enum):
    """Статусы чтения книги."""

    WANT_TO_READ = "want_to_read"
    READING = "reading"
    FINISHED = "finished"
    DROPPED = "dropped"
