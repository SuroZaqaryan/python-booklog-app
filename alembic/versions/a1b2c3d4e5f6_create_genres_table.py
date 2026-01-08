"""create genres table

Revision ID: a1b2c3d4e5f6
Revises: d90f7540b0bb
Create Date: 2026-01-08 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'd90f7540b0bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create genres table and populate with initial data."""
    connection = op.get_bind()
    
    # Проверяем, существует ли таблица genres
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    if 'genres' not in tables:
        # Создаем таблицу genres, если её нет
        op.create_table(
            'genres',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_genres_id'), 'genres', ['id'], unique=False)
        op.create_index(op.f('ix_genres_name'), 'genres', ['name'], unique=True)
    
    # Заполняем таблицу начальными данными (если их еще нет)
    genres = [
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
    
    # Проверяем, есть ли уже данные в таблице
    result = connection.execute(sa.text("SELECT COUNT(*) FROM genres"))
    count = result.scalar()
    
    # Вставляем жанры только если таблица пустая
    if count == 0:
        for genre in genres:
            connection.execute(
                sa.text("INSERT INTO genres (name) VALUES (:name)"),
                {"name": genre}
            )


def downgrade() -> None:
    """Remove genres table."""
    op.drop_index(op.f('ix_genres_name'), table_name='genres')
    op.drop_index(op.f('ix_genres_id'), table_name='genres')
    op.drop_table('genres')
