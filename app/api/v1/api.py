"""API Router aggregator для v1."""

from fastapi import APIRouter

from app.api.v1.endpoints import books

api_router = APIRouter()

# Подключение всех endpoint'ов
api_router.include_router(books.router, prefix="/book", tags=["book"])
