from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

# create_async_engine usa asyncpg por baixo dos panos (driver no DATABASE_URL).
# pool_size=10 / max_overflow=20 é um ponto de partida razoável para SaaS;
# ajuste conforme métricas reais de conexão.
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # loga SQL apenas em debug — nunca em prod
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,   # detecta conexões mortas antes de usá-las
)

# expire_on_commit=False evita lazy-load após commit em contexto async,
# onde a sessão já pode ter sido fechada.
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency do FastAPI. O `async with` garante que a sessão é fechada
    mesmo se a rota lançar exceção — sem leak de conexões.
    """
    async with AsyncSessionLocal() as session:
        yield session
