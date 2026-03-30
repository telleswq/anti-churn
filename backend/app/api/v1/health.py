from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.common import DBHealthResponse, HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Liveness check — confirma que a API está de pé."""
    return HealthResponse(status="ok", service="anti-churn-ai")


@router.get("/db", response_model=DBHealthResponse)
async def db_health_check(db: AsyncSession = Depends(get_db)) -> DBHealthResponse:
    """Readiness check — confirma conectividade com o banco."""
    try:
        await db.execute(text("SELECT 1"))
        return DBHealthResponse(status="ok", database="connected")
    except Exception as exc:
        return DBHealthResponse(status="error", database=str(exc))
