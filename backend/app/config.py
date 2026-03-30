from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Todas as configurações vêm de variáveis de ambiente.
    pydantic-settings valida os tipos em startup — se DATABASE_URL estiver
    ausente ou malformada, a aplicação falha imediatamente com erro claro.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    debug: bool = False
    environment: str = "development"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/antichurn"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Security
    secret_key: str = "change-me-in-production"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]


# Singleton — importado em todo o projeto via `from app.config import settings`
settings = Settings()
