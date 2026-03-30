import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """
    Responsável por toda operação de User.
    Recebe a sessão por injeção — facilita testes (basta passar uma sessão
    de test em vez de mockar a classe inteira).
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, tenant_id: uuid.UUID, data: UserCreate) -> User:
        existing = await self._get_by_external_id(tenant_id, data.external_id)
        if existing:
            raise ConflictError(f"User with external_id '{data.external_id}' already exists")

        user = User(
            tenant_id=tenant_id,
            external_id=data.external_id,
            email=data.email,
            name=data.name,
            metadata_=data.metadata,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user(self, tenant_id: uuid.UUID, user_id: uuid.UUID) -> User:
        result = await self.db.execute(
            select(User).where(User.tenant_id == tenant_id, User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User")
        return user

    async def list_users(self, tenant_id: uuid.UUID) -> list[User]:
        result = await self.db.execute(
            select(User)
            .where(User.tenant_id == tenant_id)
            .order_by(User.created_at.desc())
        )
        return list(result.scalars().all())

    async def update_user(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, data: UserUpdate
    ) -> User:
        user = await self.get_user(tenant_id, user_id)
        update_data = data.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # --- helpers privados ---

    async def _get_by_external_id(
        self, tenant_id: uuid.UUID, external_id: str
    ) -> User | None:
        result = await self.db.execute(
            select(User).where(
                User.tenant_id == tenant_id,
                User.external_id == external_id,
            )
        )
        return result.scalar_one_or_none()
