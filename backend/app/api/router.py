from fastapi import APIRouter

from app.api.v1 import events, health, users

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(events.router)
