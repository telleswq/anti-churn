from pydantic import BaseModel


class BaseResponse(BaseModel):
    """
    Base para todos os schemas de resposta.
    from_attributes=True habilita criação a partir de objetos ORM
    sem precisar converter manualmente para dict.
    """

    model_config = {"from_attributes": True}


class HealthResponse(BaseModel):
    status: str
    service: str


class DBHealthResponse(BaseModel):
    status: str
    database: str
