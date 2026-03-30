from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings
from app.core.exceptions import AppException, app_exception_handler
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Código antes do `yield` roda no startup.
    Código depois do `yield` roda no shutdown.
    Substitui os deprecated @app.on_event handlers.
    """
    yield
    # Fecha o pool de conexões graciosamente no shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Anti-Churn AI",
        description="Análise de comportamento e prevenção de churn",
        version="0.1.0",
        lifespan=lifespan,
        # Esconde docs em produção — expõe apenas em debug
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]

    app.include_router(api_router)

    return app


app = create_app()
