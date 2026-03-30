import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_tenant, get_db
from app.models.tenant import Tenant
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=status.HTTP_202_ACCEPTED)
async def ingest_event(
    payload: EventCreate,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
) -> EventResponse:
    """
    Endpoint de ingestão de eventos. Retorna 202 Accepted para sinalizar
    que o evento foi recebido e será processado — preparado para virar
    fire-and-forget com Celery quando o worker for implementado.
    """
    service = EventService(db)
    return await service.ingest_event(tenant_id=tenant.id, data=payload)


@router.get("/user/{user_id}", response_model=list[EventResponse])
async def list_user_events(
    user_id: uuid.UUID,
    limit: int = 50,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
) -> list[EventResponse]:
    service = EventService(db)
    return await service.list_events_for_user(
        tenant_id=tenant.id, user_id=user_id, limit=limit
    )
