from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database import engine, Base
from app.routers import books


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan для инициализации приложения.
    
    ВАЖНО: Этот метод используется ТОЛЬКО для создания таблиц в dev-окружении.
    Любые изменения схемы БД (добавление/изменение колонок, таблиц и т.д.)
    должны выполняться через Alembic миграции, а не напрямую здесь.
    
    Для применения миграций используйте:
        alembic upgrade head
    
    Для создания новой миграции:
        alembic revision --autogenerate -m "описание изменений"
    """
    # Создаем все таблицы (только для dev, не изменяет существующие таблицы)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield


app = FastAPI(
    title=settings.project_name,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Обработчик ошибок валидации.
    Возвращает стандартный 422 для ошибок валидации.
    """
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors}
    )


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")
