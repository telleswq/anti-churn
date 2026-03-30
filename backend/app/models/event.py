import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Event(Base, TimestampMixin):
    """
    Registro imutável de comportamento do usuário.
    occurred_at é o timestamp do evento no sistema do cliente (pode ser
    retroativo). created_at (do mixin) é quando chegou no Anti-Churn.

    Índices em tenant_id + user_id + event_type cobrem as queries mais
    comuns do scoring engine sem precisar de índice composto por enquanto.
    """

    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # payload flexível — cada tipo de evento pode ter campos diferentes
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="events")  # type: ignore[name-defined]
