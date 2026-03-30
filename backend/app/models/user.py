import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """
    Usuário do sistema do cliente (não o usuário do Anti-Churn em si).
    external_id é o ID que o cliente usa no próprio produto — mantemos
    o vínculo para correlacionar eventos sem exigir que o cliente mude IDs.

    Constraint única em (tenant_id, external_id) garante que o mesmo
    usuário não seja criado duas vezes para o mesmo tenant.
    """

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("tenant_id", "external_id", name="uq_users_tenant_external"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    external_id: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # JSONB permite armazenar atributos extras do cliente sem schema rígido
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    # Atualizado a cada evento recebido — usado no cálculo de inatividade
    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="users")  # type: ignore[name-defined]
    events: Mapped[list["Event"]] = relationship("Event", back_populates="user")  # type: ignore[name-defined]
