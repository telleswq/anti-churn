import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import BaseResponse


class EventCreate(BaseModel):
    """
    Payload de ingestão de evento.
    user_id aqui é o external_id — o cliente não precisa conhecer
    os UUIDs internos do Anti-Churn.
    """

    user_id: str = Field(..., description="external_id do usuário no sistema do cliente")
    event_type: str = Field(..., description="Ex: login, feature_used, page_viewed")
    payload: dict | None = Field(default=None, description="Dados extras do evento")
    occurred_at: datetime | None = Field(
        default=None,
        description="Quando o evento ocorreu. Se omitido, usa o momento da ingestão.",
    )


class EventResponse(BaseResponse):
    id: uuid.UUID
    tenant_id: uuid.UUID
    user_id: uuid.UUID
    event_type: str
    payload: dict | None
    occurred_at: datetime
    created_at: datetime
