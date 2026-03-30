from collections.abc import AsyncGenerator

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.database import get_session
from app.models.tenant import Tenant


async def get_db(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[AsyncSession, None]:
    """
    Re-exporta a sessão de banco como dependência nomeada.
    Centraliza aqui para facilitar substituição em testes.
    """
    yield session


async def get_current_tenant(
    x_api_key: str = Header(..., description="API Key do tenant (formato: sk_...)"),
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    """
    Autentica o tenant via API Key no header X-Api-Key.
    Usada em todas as rotas que recebem dados do cliente.

    Propositalmente simples: sem JWT aqui pois o fluxo de ingestão
    de eventos precisa de autenticação stateless e de baixa latência.
    """
    result = await db.execute(
        select(Tenant).where(
            Tenant.api_key == x_api_key,
            Tenant.is_active.is_(True),
        )
    )
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise UnauthorizedError("Invalid or inactive API key")
    return tenant
