import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base declarativa compartilhada por todos os models.
    Alembic detecta as tabelas a partir do metadata desta classe.
    """
    pass


class TimestampMixin:
    """
    Mixin de auditoria — toda tabela herda created_at e updated_at.
    server_default delega o DEFAULT ao Postgres, garantindo consistência
    mesmo em inserções feitas fora da ORM (scripts, migrações manuais).
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
