from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """
    Exceção base do domínio. Lançada nos services e capturada pelo handler
    registrado no main.py — mantém o padrão de resposta consistente.
    """

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class NotFoundError(AppException):
    def __init__(self, resource: str) -> None:
        super().__init__(status_code=404, detail=f"{resource} not found")


class ConflictError(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=409, detail=detail)


class UnauthorizedError(AppException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(status_code=401, detail=detail)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
