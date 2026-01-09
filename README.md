python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

python -m alembic revision --autogenerate -m "описание"  # Создать
python -m alembic upgrade head                            # Применить

# 📚 BookLog Backend

Backend API для приложения управления книгами на FastAPI.

## 🏗️ Архитектура

Проект построен по принципу **Clean Architecture** с четким разделением на слои:

```
app/
├── api/              # API Layer (REST endpoints)
├── services/         # Business Logic Layer
├── repositories/     # Data Access Layer
├── models/           # ORM Models (SQLAlchemy)
├── schemas/          # Pydantic Schemas (DTO)
├── core/             # Core (config, database)
└── utils/            # Utilities (enums, helpers)
```

Подробнее см. [ARCHITECTURE.md](ARCHITECTURE.md)

## 🚀 Быстрый старт

### Установка зависимостей

```bash
uv sync
```

### Запуск сервера

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Миграции БД

```bash
# Применить все миграции (первый запуск или после получения новых миграций)
python -m alembic upgrade head

# Создать новую миграцию (после изменения моделей)
python -m alembic revision --autogenerate -m "описание изменений"

# Проверить текущую версию БД
python -m alembic current

# Посмотреть историю миграций
python -m alembic history
```

**⚠️ Важно:** Изменения в моделях SQLAlchemy НЕ применяются автоматически!
После изменения модели нужно создать и применить миграцию.

📖 **Подробное руководство:** [ALEMBIC_GUIDE.md](ALEMBIC_GUIDE.md)

## 📖 Документация API

После запуска сервера доступна по адресам:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔗 Endpoints

### Books
- `GET /book` - получить все книги
- `POST /book` - создать книгу
- `DELETE /book/{id}` - удалить книгу
- `GET /book/genres` - получить список жанров
- `GET /book/statuses` - получить список статусов

## 📁 Структура проекта

```
backend/
├── alembic/                  # Миграции БД
│   └── versions/
├── app/
│   ├── api/                  # API Layer
│   │   ├── v1/
│   │   │   ├── endpoints/    # REST endpoints
│   │   │   └── api.py        # Router aggregator
│   │   └── deps.py           # Dependencies
│   ├── core/                 # Application core
│   │   ├── config.py         # Settings
│   │   └── database.py       # Database connection
│   ├── models/               # ORM models
│   │   ├── book.py
│   │   └── genre.py
│   ├── schemas/              # Pydantic schemas
│   │   └── book.py
│   ├── services/             # Business logic
│   │   └── book.py
│   ├── repositories/         # Data access
│   │   └── book.py
│   ├── utils/                # Utilities
│   │   └── enums.py
│   └── main.py               # Application entry point
├── books.db                  # SQLite database
├── pyproject.toml            # Dependencies
├── alembic.ini              # Alembic config
├── ARCHITECTURE.md          # Architecture docs
└── MIGRATION_GUIDE.md       # Migration guide
```

## 🛠️ Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **Alembic** - миграции БД
- **Pydantic** - валидация данных
- **aiosqlite** - асинхронный драйвер SQLite

## 📚 Дополнительно

- [ARCHITECTURE.md](ARCHITECTURE.md) - подробное описание архитектуры
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - руководство по рефакторингу проекта
- [ALEMBIC_GUIDE.md](ALEMBIC_GUIDE.md) - **полное руководство по работе с миграциями БД**