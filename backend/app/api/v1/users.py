import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_tenant, get_db
from app.models.tenant import Tenant
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(
    payload: UserCreate,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    service = UserService(db)
    return await service.create_user(tenant_id=tenant.id, data=payload)


@router.get("", response_model=list[UserResponse])
async def list_users(
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
) -> list[UserResponse]:
    service = UserService(db)
    return await service.list_users(tenant_id=tenant.id)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    service = UserService(db)
    return await service.get_user(tenant_id=tenant.id, user_id=user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    service = UserService(db)
    return await service.update_user(tenant_id=tenant.id, user_id=user_id, data=payload)
