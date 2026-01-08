"""add genre column to books table

Revision ID: d90f7540b0bb
Revises: 21d28dcb475b
Create Date: 2026-01-08 13:52:55.622418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd90f7540b0bb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add genre column to books table."""
    # Добавляем колонку genre как nullable (SQLite ограничения)
    op.add_column('books', sa.Column('genre', sa.String(), nullable=True))
    
    # Заполняем существующие записи значением по умолчанию
    op.execute("UPDATE books SET genre = 'Fantasy' WHERE genre IS NULL")
    
    # Примечание: В SQLite нельзя изменить nullable для существующей колонки без пересоздания таблицы.
    # NOT NULL ограничение обеспечивается на уровне модели SQLAlchemy (BookModel.genre.nullable=False)
    # и валидацией Pydantic. Для production можно добавить более сложную миграцию с пересозданием таблицы.


def downgrade() -> None:
    """Remove genre column from books table."""
    op.drop_column('books', 'genre')
