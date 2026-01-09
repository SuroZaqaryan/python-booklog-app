"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.database import engine
from app.models import Base
from app.api.v1.api import api_router


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


# Создание приложения FastAPI
app = FastAPI(
    title=settings.project_name,
    lifespan=lifespan,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение API роутеров
app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Обработчик ошибок валидации.
    Возвращает стандартный 422 для ошибок валидации.
    
    Args:
        request: HTTP запрос.
        exc: Исключение валидации.
        
    Returns:
        JSONResponse: Ответ с деталями ошибки.
    """
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors}
    )


@app.get("/")
async def root():
    """
    Корневой endpoint - редирект на документацию.
    
    Returns:
        RedirectResponse: Редирект на документацию API.
    """
    return RedirectResponse(url="/api/docs")
