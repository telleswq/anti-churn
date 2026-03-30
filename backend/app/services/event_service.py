import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate


class EventService:
    """
    Responsável pela ingestão e consulta de eventos.
    O método ingest_event também atualiza last_seen_at do usuário —
    esses dois writes ocorrem na mesma transação para garantir consistência.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def ingest_event(self, tenant_id: uuid.UUID, data: EventCreate) -> Event:
        user = await self._resolve_user(tenant_id, data.user_id)

        occurred_at = data.occurred_at or datetime.now(timezone.utc)

        event = Event(
            tenant_id=tenant_id,
            user_id=user.id,
            event_type=data.event_type,
            payload=data.payload,
            occurred_at=occurred_at,
        )

        # Mantém last_seen_at no valor mais recente entre os eventos
        if user.last_seen_at is None or occurred_at > user.last_seen_at:
            user.last_seen_at = occurred_at

        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def list_events_for_user(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, limit: int = 50
    ) -> list[Event]:
        result = await self.db.execute(
            select(Event)
            .where(Event.tenant_id == tenant_id, Event.user_id == user_id)
            .order_by(Event.occurred_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    # --- helpers privados ---

    async def _resolve_user(self, tenant_id: uuid.UUID, external_id: str) -> User:
        """Resolve external_id → User interno. Lança 404 se não encontrar."""
        result = await self.db.execute(
            select(User).where(
                User.tenant_id == tenant_id,
                User.external_id == external_id,
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError(f"User with external_id '{external_id}'")
        return user
