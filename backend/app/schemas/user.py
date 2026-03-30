import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import BaseResponse


class UserCreate(BaseModel):
    """Payload para criar/registrar um usuário do cliente."""

    external_id: str = Field(..., description="ID do usuário no sistema do cliente")
    email: str | None = None
    name: str | None = None
    metadata: dict | None = Field(default=None, description="Atributos extras do usuário")


class UserUpdate(BaseModel):
    """Campos opcionalmente atualizáveis. Apenas os enviados são alterados."""

    email: str | None = None
    name: str | None = None
    metadata: dict | None = None


class UserResponse(BaseResponse):
    id: uuid.UUID
    tenant_id: uuid.UUID
    external_id: str
    email: str | None
    name: str | None
    last_seen_at: datetime | None
    created_at: datetime
    updated_at: datetime
